"""第二章範例：資料格式轉換與快照產生。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".json", ".xlsx", ".xls", ".npy", ".parquet"}


def read_data_source(source_path: Path) -> pd.DataFrame:
    suffix = source_path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"不支援的資料格式：{suffix}")

    if suffix == ".csv":
        return pd.read_csv(source_path, dtype=str)
    if suffix in {".xls", ".xlsx"}:
        return pd.read_excel(source_path, dtype=str)
    if suffix == ".json":
        return pd.read_json(source_path, orient="records")
    if suffix == ".npy":
        raw = np.load(source_path, allow_pickle=True)
        return pd.DataFrame(raw)
    return pd.read_parquet(source_path)


def normalize_table(df: pd.DataFrame, schema: dict[str, str]) -> pd.DataFrame:
    normalized = df.copy()
    normalized.columns = normalized.columns.str.strip()

    for column, col_type in schema.items():
        if column not in normalized.columns:
            normalized[column] = pd.NA

        if col_type == "string":
            normalized[column] = normalized[column].astype("string")
        elif col_type == "int":
            normalized[column] = pd.to_numeric(normalized[column], errors="coerce").astype("Int64")
        elif col_type == "float":
            normalized[column] = pd.to_numeric(normalized[column], errors="coerce").astype("Float64")
        elif col_type in {"datetime", "date"}:
            normalized[column] = pd.to_datetime(normalized[column], errors="coerce")
        elif col_type == "category":
            normalized[column] = normalized[column].astype("string").astype("category")
        else:
            raise ValueError(f"不支援的欄位型別：{col_type}")

    return normalized[list(schema.keys())]


def save_parquet(df: pd.DataFrame, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(target_path, engine="pyarrow", index=False)


def save_numpy_snapshot(df: pd.DataFrame, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    array = df.to_records(index=False)
    np.save(target_path, array)


def transform_file(
    source_path: Path,
    processed_path: Path,
    snapshot_path: Path,
    schema: dict[str, str],
) -> tuple[Path, Path]:
    df = read_data_source(source_path)
    normalized = normalize_table(df, schema)
    save_parquet(normalized, processed_path)
    save_numpy_snapshot(normalized, snapshot_path)
    return processed_path, snapshot_path
