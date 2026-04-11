from pathlib import Path

import numpy as np
import pandas as pd

from examples.ch02.data_transform import transform_file


def test_transform_csv_to_parquet_and_numpy(tmp_path: Path) -> None:
    raw_csv = tmp_path / "raw_data.csv"
    raw_csv.write_text(
        (
            "user_id,score,joined,status\n"
            "1,10,2026-04-01,active\n"
            "2,,2026-03-15,inactive\n"
            "3,7,invalid,pending\n"
        ),
        encoding="utf-8",
    )

    schema = {
        "user_id": "int",
        "score": "float",
        "joined": "datetime",
        "status": "string",
    }
    processed_path = tmp_path / "processed" / "ch02_data.parquet"
    snapshot_path = tmp_path / "processed" / "ch02_data.npy"

    result_parquet, result_snapshot = transform_file(
        source_path=raw_csv,
        processed_path=processed_path,
        snapshot_path=snapshot_path,
        schema=schema,
    )

    assert result_parquet.exists()
    assert result_snapshot.exists()

    df = pd.read_parquet(result_parquet)
    assert list(df.columns) == ["user_id", "score", "joined", "status"]
    assert df["user_id"].dtype == "Int64"
    assert pd.isna(df.loc[1, "score"])
    assert df["joined"].isna().sum() == 1

    snapshot = np.load(result_snapshot, allow_pickle=True)
    assert snapshot.shape[0] == 3
    assert snapshot.dtype.names == tuple(schema.keys())
