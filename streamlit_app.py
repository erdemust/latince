from __future__ import annotations

import csv
import io
import random
import re
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Botanical Latin Quiz",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_TITLE = "🌿 Botanical Latin Quiz"
DEFAULT_CSV = Path(__file__).parent / "botanical_terms.csv"

REQUIRED_COLUMNS = [
    "latin",
    "answer",
    "options",
    "plant",
    "plant_name",
    "explanation",
]

OPTION_SEPARATOR = ","

st.title(APP_TITLE)
st.caption(
    "Learn botanical Latin through interactive multiple-choice quizzes."
)


# ============================================================
# CSV LOADING AND VALIDATION
# ============================================================

def decode_csv(raw_bytes: bytes) -> str:
    """Decode CSV bytes using common encodings."""
    for encoding in ("utf-8-sig", "utf-8", "cp1254", "latin-1"):
        try:
            return raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(
        "Could not decode the CSV file. Save it as UTF-8 and try again."
    )


def normalize_column_name(name: str) -> str:
    """Normalize column names without changing their meaning."""
    return name.strip().lower().lstrip("\ufeff")


def parse_csv_text(text: str):
    """
    Parse a CSV document with Python's CSV reader.

    Strict parsing is attempted first. If quoting is malformed,
    a diagnostic error is returned instead of silently corrupting data.
    """
    try:
        reader = csv.reader(
            io.StringIO(text, newline=""),
            strict=True,
            skipinitialspace=True,
        )

        rows = list(reader)

    except csv.Error as exc:
        raise ValueError(
            f"Malformed CSV quoting: {exc}. "
            "Check quotation marks and commas in the CSV file."
        ) from exc

    if not rows:
        raise ValueError("The CSV file is empty.")

    # Remove completely empty lines.
    rows = [
        row for row in rows
        if any(str(cell).strip() for cell in row)
    ]

    if not rows:
        raise ValueError("The CSV file contains no data.")

    headers = [
        normalize_column_name(cell)
        for cell in rows[0]
    ]

    if len(headers) != len(set(headers)):
        raise ValueError(
            "Duplicate column names found. "
            "Every CSV column must have a unique name."
        )

    missing = [
        column for column in REQUIRED_COLUMNS
        if column not in headers
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}. "
            f"Expected columns: {', '.join(REQUIRED_COLUMNS)}."
        )

    expected = len(headers)
    valid_rows = []
    errors = []

    for line_number, row in enumerate(rows[1:], start=2):
        if len(row) != expected:
            errors.append(
                f"Line {line_number}: expected {expected} fields, "
                f"found {len(row)}."
            )
            continue

        valid_rows.append(row)

    if errors:
        preview = "\n".join(errors[:10])

        raise ValueError(
            "CSV structure validation failed.\n\n"
            f"{preview}\n\n"
            "No rows were silently discarded. Correct the indicated "
            "lines in the source CSV and upload it again."
        )

    if not valid_rows:
        raise ValueError("The CSV contains headers but no data rows.")

    df = pd.DataFrame(valid_rows, columns=headers)

    # Keep all columns as text.
    for column in df.columns:
        df[column] = df[column].fillna("").astype(str).str.strip()

    # Required fields.
    for column in ("latin", "answer", "options"):
        empty_mask = df[column].eq("")

        if empty_mask.any():
            bad_rows = [
                str(index + 2)
                for index in df.index[empty_mask][:10]
            ]

            raise ValueError(
                f"Required field '{column}' is empty "
                f"on CSV line(s): {', '.join(bad_rows)}."
            )

    # Remove exact duplicate records.
    df = df.drop_duplicates().reset_index(drop=True)

    return df


def split_options(value: str) -> list[str]:
    """
    Split the options field on commas.

    This expects each options cell to contain four comma-separated
    choices, as in the supplied dataset.
    """
    return [
        option.strip()
        for option in value.split(OPTION_SEPARATOR)
        if option.strip()
    ]


def validate_questions(df: pd.DataFrame):
    """Validate answer choices and remove duplicate choices per question."""
    cleaned_rows = []
    warnings = []

    for index, row in df.iterrows():
        options = split_options(row["options"])
        answer = row["answer"].strip()

        # Remove duplicate choices while preserving their order.
        unique_options = list(dict.fromkeys(options))

        if len(unique_options) < 2:
            warnings.append(
                f"'{row['latin']}': fewer than two distinct options."
            )
            continue

        # Ensure the correct answer exists among the choices.
        if answer.casefold() not in {
            option.casefold() for option in unique_options
        }:
            warnings.append(
                f"'{row['latin']}': the answer does not match any option."
            )
            continue

        # Save the validated choices.
        row = row.copy()
        row["options_list"] = unique_options
        cleaned_rows.append(row)

    # Ensure at least one valid question remains.
    if not cleaned_rows:
        raise ValueError(
            "No valid questions found. Check the options and answers "
            "in your CSV file."
        )

    result = pd.DataFrame(cleaned_rows).reset_index(drop=True)

    return result, warnings
