"""Data access: DuckDB connection for the pipeline, cached Parquet loaders for the app, source/licence text."""
from __future__ import annotations

from pathlib import Path

import duckdb
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

    load_table = st.cache_data(show_spinner=False)(read_processed)
else:
    load_table = read_processed


SOURCE_CAPTION = (
    "Source: French Ministry of Health (SISE-Eaux) — « Résultats du contrôle sanitaire de l'eau distribuée "
    "commune par commune », data.gouv.fr, Licence Ouverte 2.0, updated 5 Oct 2026."
)
