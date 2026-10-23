from __future__ import annotations

import csv
import io
import random
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

st.title(APP_TITLE)
st.caption(
    "Learn botanical Latin through interactive multiple-choice quizzes."
)


# ============================================================
# SESSION STATE
# ============================================================

def initialize_state():
    defaults = {
        "quiz_questions": [],
        "current_question": 0,
        "score": 0,
        "answered": False,
        "selected_answer": None,
        "quiz_finished": False,
        "quiz_started": False,
        "question_results": [],
        "quiz_config": None,
        "question_selections": {},
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz():
    st.session_state.quiz_questions = []
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.quiz_finished = False
    st.session_state.quiz_started = False
    st.session_state.question_results = []
    st.session_state.quiz_config = None
    st.session_state.question_selections = {}


initialize_state()


# ============================================================
# FAILSAFE CSV LOADING
# ============================================================

def decode_csv(raw_bytes: bytes) -> str:
    """Decode CSV files with common encodings."""

    for encoding in ("utf-8-sig", "utf-8", "cp1254", "latin-1"):
        try:
            return raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(
        "Could not decode the CSV file. Save it as UTF-8."
    )


def parse_csv_text(text: str) -> pd.DataFrame:
    """
    Parse CSV safely.

    Correctly quoted commas are preserved.
    Rows with missing fields are rejected with diagnostics.
    Extra fields are repaired only when the explanation field
    can be reconstructed without ambiguity.
    """

    if not text or not text.strip():
        raise ValueError("The CSV file is empty.")

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
            "Check quotation marks in your CSV file."
        ) from exc

    rows = [
        row for row in rows
        if any(str(cell).strip() for cell in row)
    ]

    if not rows:
        raise ValueError("The CSV contains no records.")

    headers = [
        str(value).strip().lower().lstrip("\ufeff")
        for value in rows[0]
    ]

    if len(headers) != len(set(headers)):
        raise ValueError(
            "Duplicate column names found in the CSV."
        )

    missing = [
        column for column in REQUIRED_COLUMNS
        if column not in headers
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {', '.join(missing)}. "
            f"Required columns: {', '.join(REQUIRED_COLUMNS)}."
        )

    has_category = "category" in headers

    if not has_category:
        headers.append("category")

    expected_fields = len(headers)
    explanation_index = headers.index("explanation")

    valid_rows = []
    errors = []
    recovered_lines = []

    for line_number, original in enumerate(rows[1:], start=2):
        row = [str(value).strip() for value in original]

        # Compatibility with the six-column CSV format.
        if not has_category and len(row) == expected_fields - 1:
            row.append("Uncategorized")

        # If fields are missing, do not guess their contents.
        if len(row) < expected_fields:
            errors.append(
                f"Line {line_number}: expected "
                f"{expected_fields} fields, found {len(original)}."
            )
            continue

        # Repair extra fields by merging them into explanation.
        if len(row) > expected_fields:
            explanation_end = (
                len(row)
                - (expected_fields - explanation_index - 1)
            )

            row = (
                row[:explanation_index]
                + [
                    ",".join(
                        row[explanation_index:explanation_end]
                    )
                ]
                + row[explanation_end:]
            )

            if len(row) == expected_fields:
                recovered_lines.append(line_number)

        if len(row) != expected_fields:
            errors.append(
                f"Line {line_number}: could not repair "
                "the CSV record safely."
            )
            continue

        valid_rows.append(row)

    if errors:
        raise ValueError(
            "CSV structure validation failed:\n\n"
            + "\n".join(errors[:12])
            + "\n\nFix the affected rows and upload the CSV again."
        )

    if not valid_rows:
        raise ValueError("The CSV contains no valid data rows.")

    df = pd.DataFrame(valid_rows, columns=headers)

    for column in df.columns:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    df["category"] = df["category"].replace(
        "",
        "Uncategorized",
    )

    for column in ("latin", "answer", "options"):
        empty = df[column].eq("")

        if empty.any():
            lines = [
                str(index + 2)
                for index in df.index[empty][:10]
            ]

            raise ValueError(
                f"Required field '{column}' is empty "
                f"on CSV row(s): {', '.join(lines)}."
            )

    df = df.drop_duplicates().reset_index(drop=True)

    if recovered_lines:
        st.sidebar.warning(
            f"Recovered {len(recovered_lines)} CSV row(s) "
            "by merging extra fields into explanations."
        )

    return df


def split_options(value: str) -> list[str]:
    """Split the options field into answer choices."""

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def validate_questions(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, list[str]]:
    """Validate quiz questions and return diagnostics."""

    valid = []
    warnings = []

    for index, row in df.iterrows():
        latin = row["latin"].strip()
        answer = row["answer"].strip()
        options = split_options(row["options"])

        # Remove duplicate choices while preserving order.
        unique_options = list(dict.fromkeys(options))

        if len(unique_options) < 2:
            warnings.append(
                f"Row {index + 2} ({latin}): "
                "fewer than two distinct choices."
            )
            continue

        matching = [
            option for option in unique_options
            if option.casefold() == answer.casefold()
        ]

        if not matching:
            warnings.append(
                f"Row {index + 2} ({latin}): "
                "the answer does not match any option."
            )
            continue

        item = row.to_dict()

        item["answer"] = matching[0]
        item["options_list"] = unique_options

        for column in (
            "category",
            "plant",
            "plant_name",
            "explanation",
        ):
            item[column] = str(item.get(column, "")).strip()

        if not item["category"]:
            item["category"] = "Uncategorized"

        valid.append(item)

    if not valid:
        raise ValueError(
            "No valid questions remain. Check the CSV answers "
            "and options."
        )

    return pd.DataFrame(valid).reset_index(drop=True), warnings


# ============================================================
# DATA SOURCE
# ============================================================

st.sidebar.header("📂 Question Database")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"],
    help="Upload botanical_terms.csv.",
)

try:
    if uploaded_file is not None:
        raw_bytes = uploaded_file.getvalue()

        if not raw_bytes:
            raise ValueError("The uploaded CSV file is empty.")

        source_df = parse_csv_text(decode_csv(raw_bytes))

    else:
        if not DEFAULT_CSV.exists():
            st.error(
                "botanical_terms.csv was not found. "
                "Upload your CSV using the sidebar."
            )

            st.stop()

        source_df = parse_csv_text(
            decode_csv(DEFAULT_CSV.read_bytes())
        )

    df, validation_warnings = validate_questions(source_df)

except (ValueError, OSError) as exc:
    st.error(f"Could not load the question database: {exc}")

    st.info(
        "Check the CSV column names, quotation marks, answers, "
        "and answer choices. You can upload a corrected CSV "
        "using the sidebar."
    )

    st.stop()

except Exception as exc:
    st.error("An unexpected error occurred while loading the CSV.")
    st.caption(f"Details: {type(exc).__name__}: {exc}")
    st.stop()


if validation_warnings:
    with st.expander(
        f"⚠️ {len(validation_warnings)} invalid question(s)"
    ):
        for warning in validation_warnings:
            st.warning(warning)


# ============================================================
# QUIZ SETTINGS
# ============================================================

st.sidebar.divider()
st.sidebar.header("🎯 Quiz Settings")

categories = sorted(
    df["category"].unique().tolist(),
    key=str.casefold,
)

selected_categories = st.sidebar.multiselect(
    "Choose categories",
    options=categories,
    default=categories,
)

available_df = df[
    df["category"].isin(selected_categories)
].copy()

max_questions = len(available_df)

if max_questions:
    number_of_questions = st.sidebar.number_input(
        "Number of questions",
        min_value=1,
        max_value=max_questions,
        value=min(10, max_questions),
        step=1,
    )
else:
    number_of_questions = 0
    st.sidebar.warning("Select a category containing valid questions.")

shuffle_questions = st.sidebar.checkbox(
    "Shuffle questions",
    value=True,
)

shuffle_options = st.sidebar.checkbox(
    "Shuffle answer choices",
    value=True,
)

show_progress = st.sidebar.checkbox(
    "Show progress bar",
    value=True,
)

start_clicked = st.sidebar.button(
    "🚀 Start / Restart Quiz",
    type="primary",
    use_container_width=True,
    disabled=number_of_questions == 0,
)


# ============================================================
# START OR RESTART
# ============================================================

if start_clicked:
    pool = available_df.to_dict("records")

    if shuffle_questions:
        random.shuffle(pool)

    questions = pool[:int(number_of_questions)]

    for question in questions:
        choices = list(question["options_list"])

        if shuffle_options:
            random.shuffle(choices)

        question["display_options"] = choices

    reset_quiz()

    st.session_state.quiz_questions = questions
    st.session_state.quiz_started = True
    st.session_state.quiz_config = {
        "categories": list(selected_categories),
        "number_of_questions": int(number_of_questions),
    }

    st.rerun()


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.quiz_started:
    st.subheader("Welcome to the Botanical Latin Quiz! 🌱")

    st.write(
        "Learn botanical Latin through questions about plant "
        "morphology, colours, surface characteristics, and "
        "scientific plant names."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Valid questions", len(df))
    col2.metric("Categories", df["category"].nunique())
    col3.metric("Available questions", max_questions)

    st.markdown("### How to play")

    st.markdown(
        """
        1. Choose categories in the sidebar.
        2. Select the number of questions.
        3. Click **Start / Restart Quiz**.
        4. Select an answer and submit it.
        5. Read the explanation.
        6. Review your final score.
        """
    )

    st.markdown("### Available categories")

    for category in categories:
        count = int((df["category"] == category).sum())
        st.write(f"- **{category}**: {count} questions")

    st.stop()


# ============================================================
# ACTIVE QUIZ
# ============================================================

questions = st.session_state.quiz_questions
total_questions = len(questions)

if total_questions == 0:
    st.error("No questions are available.")

    if st.button("Return to setup"):
        reset_quiz()
        st.rerun()

    st.stop()


# ============================================================
# FINAL RESULTS
# ============================================================

if st.session_state.quiz_finished:
    score = st.session_state.score

    percentage = round(
        score / total_questions * 100,
        1,
    )

    st.balloons()
    st.success("🎉 Quiz completed!")

    st.subheader("Your Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Correct answers", f"{score}/{total_questions}")
    col2.metric("Accuracy", f"{percentage}%")
    col3.metric("Incorrect answers", total_questions - score)

    if percentage == 100:
        st.markdown("### 🌟 Perfect score!")
    elif percentage >= 80:
        st.markdown("### 🌿 Excellent work!")
    elif percentage >= 60:
        st.markdown("### 🌱 Good progress!")
    else:
        st.markdown("### 📚 Keep practicing!")

    st.divider()
    st.subheader("📋 Answer Review")

    for index, result in enumerate(
        st.session_state.question_results,
        start=1,
    ):
        icon = "✅" if result["is_correct"] else "❌"

        with st.expander(
            f"{icon} Question {index}: {result['latin']}"
        ):
            st.write(f"**Category:** {result['category']}")
            st.write(
                f"**Your answer:** "
                f"{result['selected_answer'] or 'No answer'}"
            )
            st.write(f"**Correct answer:** {result['answer']}")

            if result["plant"]:
                st.write(f"**Scientific name:** {result['plant']}")

            if result["plant_name"]:
                st.write(f"**Common name:** {result['plant_name']}")

            if result["explanation"]:
                st.info(result["explanation"])

    # Download the user's results.
    results_csv = pd.DataFrame(
        st.session_state.question_results
    ).to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "⬇️ Download Results",
        data=results_csv,
        file_name="botanical_latin_results.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if st.button(
        "🔄 Play Again",
        type="primary",
        use_container_width=True,
    ):
        reset_quiz()
        st.rerun()

    st.stop()


# ============================================================
# CURRENT QUESTION
# ============================================================

question_index = st.session_state.current_question
question = questions[question_index]

st.divider()

st.subheader(
    f"Question {question_index + 1} of {total_questions}"
)

if show_progress:
    st.progress(
        (question_index + 1) / total_questions,
        text=f"Question {question_index + 1} of {total_questions}",
    )

col1, col2 = st.columns(2)

col1.metric("Current score", st.session_state.score)
col2.caption(f"Category: {question['category']}")

st.markdown("### What does this botanical Latin term mean?")
st.markdown(f"# 🌿 {question['latin']}")

if question["plant"]:
    st.caption(f"Example plant: {question['plant']}")


# ============================================================
# ANSWER FORM
# ============================================================

if not st.session_state.answered:
    with st.form(
        key=f"answer_form_{question_index}",
        clear_on_submit=False,
    ):
        selected_answer = st.radio(
            "Choose the correct meaning:",
            options=question["display_options"],
            index=None,
            key=f"answer_{question_index}",
        )

        submitted = st.form_submit_button(
            "✅ Submit Answer",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if selected_answer is None:
            st.warning("Please select an answer.")
        else:
            is_correct = (
                selected_answer.casefold()
                == question["answer"].casefold()
            )

            st.session_state.selected_answer = selected_answer
            st.session_state.answered = True

            if is_correct:
                st.session_state.score += 1

            st.session_state.question_results.append(
                {
                    "latin": question["latin"],
                    "category": question["category"],
                    "selected_answer": selected_answer,
                    "answer": question["answer"],
                    "is_correct": is_correct,
                    "plant": question["plant"],
                    "plant_name": question["plant_name"],
                    "explanation": question["explanation"],
                }
            )

            st.rerun()


# ============================================================
# FEEDBACK AND NAVIGATION
# ============================================================

else:
    selected_answer = st.session_state.selected_answer

    is_correct = (
        selected_answer.casefold()
        == question["answer"].casefold()
    )

    if is_correct:
        st.success(
            f"✅ Correct! The answer is: {question['answer']}"
        )
    else:
        st.error(
            f"❌ Incorrect. The correct answer is: "
            f"{question['answer']}"
        )

    st.markdown("### 📖 Explanation")

    if question["explanation"]:
        st.info(question["explanation"])
    else:
        st.caption("No explanation is available.")

    if question["plant"]:
        st.markdown("### 🌱 Example Plant")
        st.write(f"**Scientific name:** {question['plant']}")

        if question["plant_name"]:
            st.write(f"**Common name:** {question['plant_name']}")

    st.divider()

    if question_index + 1 < total_questions:
        if st.button(
            "➡️ Next Question",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.current_question += 1
            st.session_state.answered = False
            st.session_state.selected_answer = None
            st.rerun()
    else:
        if st.button(
            "🏁 Finish Quiz",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.quiz_finished = True
            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌿 Botanical Latin Quiz | "
    "Learn botanical terminology one question at a time."
)
