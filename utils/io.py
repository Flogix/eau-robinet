"""Data access: DuckDB connection for the pipeline, cached Parquet loaders for the app, source/licence text.

The app only reads data/processed/ (small, committed tables). Heavy work is done by the scripts.
"""
from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

import config


def connect_duckdb(database: str = ":memory:") -> duckdb.DuckDBPyConnection:
    """DuckDB connection tuned for this machine (out-of-core, spill to data/interim/duckdb_tmp)."""
    config.DUCKDB_TMP.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(database)
    con.execute(f"SET memory_limit='{config.DUCKDB_MEMORY_LIMIT}'")
    con.execute(f"SET threads={config.DUCKDB_THREADS}")
    con.execute(f"SET temp_directory='{config.DUCKDB_TMP.as_posix()}'")
    con.execute("SET preserve_insertion_order=false")
    return con


def processed_path(name: str) -> Path:
    return config.PROCESSED / f"{name}.parquet"


def read_processed(name: str) -> pd.DataFrame:
    """Read a table from data/processed/ (no caching; the app uses load_table)."""
    return pd.read_parquet(processed_path(name))


def _streamlit_running() -> bool:
    try:
        from streamlit import runtime
        return runtime.exists()
    except ImportError:  # pragma: no cover
        return False


if _streamlit_running():  # the app caches loads; scripts and tests read directly
    import streamlit as st

    def cached(func):
        return st.cache_data(show_spinner=False)(func)

    def cached_resource(func):
        return st.cache_resource(show_spinner=False)(func)
else:
    def cached(func):
        return func

    cached_resource = cached

load_table = cached(read_processed)


SOURCE_CAPTION = (
    "Source: French Ministry of Health (SISE-Eaux) — « Résultats du contrôle sanitaire de l'eau distribuée "
    "commune par commune », data.gouv.fr, Licence Ouverte 2.0, updated 5 Oct 2026."
)
SOURCE_SHORT = "Source: Ministry of Health, data.gouv.fr (Licence Ouverte 2.0, updated 5 Oct 2026)."


# --- Geography helpers ---------------------------------------------------------------------------
def dep_of_network(codes: pd.Series) -> pd.Series:
    """Department of a network from its code: '001000003' -> '01', '02A…' -> '2A', '971…' -> '971'."""
    c = codes.astype(str)
    return pd.Series(np.where(c.str[:2] == "97", c.str[:3], c.str[1:3]), index=codes.index)


def normalize(text: str) -> str:
    """Lower-case, no accents, no punctuation: 'Saint-Étienne' -> 'saint etienne' (commune search)."""
    t = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode()
    return " ".join("".join(ch if ch.isalnum() else " " for ch in t.lower()).split())


@cached
def departments() -> pd.DataFrame:
    return read_processed("dim_departements")


@cached
def departments_geojson() -> dict:
    with open(config.PROCESSED / "departements.geojson", encoding="utf-8") as f:
        return json.load(f)


@cached
def communes() -> pd.DataFrame:
    """Current communes with their typology and current score (one row per INSEE code of the dataset)."""
    dim = read_processed("dim_communes")
    sc = read_processed("commune_scores")
    d = dim.merge(sc, on="insee", how="left")
    d["search"] = d["nom"].map(normalize)
    d["label"] = d["nom"] + " (" + d["dep"].fillna("?") + ")"
    return d


def search_communes(query: str, limit: int = 30) -> pd.DataFrame:
    """Communes whose name contains the query (accents ignored); names starting with it first, then by population."""
    q = normalize(query)
    d = communes()
    d = d[d["is_current"]]
    if not q:
        return d.iloc[0:0]
    hit = d[d["search"].str.contains(q, regex=False)].copy()
    hit["rank"] = np.where(hit["search"] == q, 0, np.where(hit["search"].str.startswith(q), 1, 2))
    return hit.sort_values(["rank", "population"], ascending=[True, False]).head(limit)


# --- Network-level detail (queried on demand, never loaded whole) -----------------------------------
@cached_resource
def _app_duckdb() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute("SET memory_limit='256MB'")
    con.execute("SET threads=2")
    return con


@cached
def network_history(networks: tuple[str, ...]) -> pd.DataFrame:
    """Key parameters × year for a few networks (udi_param_year has 5 million rows: filtered in DuckDB)."""
    if not networks:
        return pd.DataFrame()
    path = processed_path("udi_param_year").as_posix()
    placeholders = ", ".join("?" for _ in networks)
    return _app_duckdb().execute(
        f"SELECT * FROM read_parquet('{path}') WHERE cdreseau IN ({placeholders}) ORDER BY annee",
        list(networks)).df()


@cached
def network_params(networks: tuple[str, ...]) -> pd.DataFrame:
    """Current-window parameter rows (udi_param_window) for a few networks."""
    w = load_table("udi_param_window")
    return w[w["cdreseau"].isin(networks)].copy()
