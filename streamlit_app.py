from pathlib import Path
import csv
import io
import random

import pandas as pd
import streamlit as st


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Botanical Latin Quiz",
    page_icon="🌿",
    layout="wide",
)

APP_DIR = Path(__file__).resolve().parent
CSV_PATH = APP_DIR / "botanical_terms.csv"

REQUIRED_COLUMNS = [
    "latin",
    "answer",
    "options",
    "plant",
    "plant_name",
    "explanation",
]


# --------------------------------------------------
# CSV LOADING
# --------------------------------------------------

def read_csv_safely(file_bytes):
    """
    Read a CSV file while preserving quoted commas
    and reporting malformed rows.
    """

    try:
        text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ValueError(
            "The CSV file must use UTF-8 encoding."
        )

    try:
        reader = csv.reader(
            io.StringIO(text, newline=""),
            strict=True,
        )

        rows = list(reader)

    except csv.Error as exc:
        raise ValueError(
            f"CSV parsing failed: {exc}"
        )

    if not rows:
        raise ValueError("The CSV file is empty.")

    header = [
        value.strip().lower()
        for value in rows[0]
    ]

    if len(header) != len(set(header)):
        raise ValueError(
            "The CSV contains duplicate column names."
        )

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in header
    ]

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing)
        )

    expected_fields = len(header)
    valid_rows = []
    errors = []

    for line_number, row in enumerate(
        rows[1:],
        start=2,
    ):
        # Ignore completely empty lines.
        if not row or all(
            not value.strip() for value in row
        ):
            continue

        if len(row) != expected_fields:
            errors.append(
                f"CSV line {line_number}: "
                f"expected {expected_fields} fields "
                f"but found {len(row)}."
            )
            continue

        valid_rows.append(row)

    if errors:
        raise ValueError(
            "Malformed CSV rows were found:\n\n"
            + "\n".join(errors)
            + "\n\nCheck commas and quotation marks."
        )

    dataframe = pd.DataFrame(
        valid_rows,
        columns=header,
    )

    # Normalize text fields.
    for column in REQUIRED_COLUMNS:
        dataframe[column] = (
            dataframe[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    return dataframe


# --------------------------------------------------
# QUESTION VALIDATION
# --------------------------------------------------

def parse_options(options_text):
    """
    Prefer pipe-separated choices.

    Legacy comma-separated choices are supported
    as a fallback for existing datasets.
    """

    if "|" in options_text:
        options = options_text.split("|")
    else:
        options = options_text.split(",")

    return [
        option.strip()
        for option in options
        if option.strip()
    ]


def validate_questions(dataframe):
    valid_questions = []
    errors = []

    for index, row in dataframe.iterrows():
        question_number = index + 2
        latin = row["latin"]
        answer = row["answer"]

        missing_fields = [
            column
            for column in REQUIRED_COLUMNS
            if not row[column]
        ]

        if missing_fields:
            errors.append(
                f"Row {question_number} ({latin}): "
                "missing fields: "
                + ", ".join(missing_fields)
            )
            continue

        options = parse_options(row["options"])

        # Remove duplicate choices without silently
        # accepting an invalid question.
        unique_options = list(dict.fromkeys(options))

        if len(unique_options) < 2:
            errors.append(
                f"Row {question_number} ({latin}): "
                "fewer than two distinct choices."
            )
            continue

        if answer not in unique_options:
            errors.append(
                f"Row {question_number} ({latin}): "
                "the correct answer does not exactly "
                "match any answer choice."
            )
            continue

        question = row.to_dict()
        question["options_list"] = unique_options

        valid_questions.append(question)

    return valid_questions, errors


# --------------------------------------------------
# USER INTERFACE
# --------------------------------------------------

st.title("🌿 Botanical Latin Quiz")

st.write(
    "Learn botanical Latin terms, plant descriptions, "
    "and scientific names."
)

st.sidebar.header("Question Database")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"],
)

st.sidebar.caption(
    "Required columns: latin, answer, options, "
    "plant, plant_name, explanation"
)

# Prefer an uploaded file when available.
if uploaded_file is not None:
    source_bytes = uploaded_file.getvalue()
    source_name = uploaded_file.name

elif CSV_PATH.exists():
    source_bytes = CSV_PATH.read_bytes()
    source_name = CSV_PATH.name

else:
    st.error(
        "Question database not found. Upload a CSV "
        "using the sidebar or place botanical_terms.csv "
        "next to streamlit_app.py."
    )
    st.stop()


# --------------------------------------------------
# LOAD AND VALIDATE DATABASE
# --------------------------------------------------

try:
    dataframe = read_csv_safely(source_bytes)

except ValueError as exc:
    st.error("Could not load the question database.")
    st.code(str(exc))
    st.stop()

questions, validation_errors = validate_questions(
    dataframe
)

if validation_errors:
    st.warning(
        f"{len(validation_errors)} invalid question(s) "
        "were found."
    )

    with st.expander("View validation errors"):
        for error in validation_errors:
            st.error(error)

if not questions:
    st.error(
        "There are no valid questions available. "
        "Correct the CSV and upload it again."
    )
    st.stop()

st.sidebar.success(
    f"{len(questions)} valid questions loaded."
)

st.caption(f"Database: {source_name}")


# --------------------------------------------------
# QUIZ SETTINGS
# --------------------------------------------------

st.sidebar.header("Quiz Settings")

shuffle_questions = st.sidebar.checkbox(
    "Shuffle questions",
    value=False,
)

shuffle_options = st.sidebar.checkbox(
    "Shuffle answer choices",
    value=True,
)

show_explanation = st.sidebar.checkbox(
    "Show explanations after answering",
    value=True,
)

if shuffle_questions:
    quiz_questions = questions.copy()
    random.Random(42).shuffle(quiz_questions)
else:
    quiz_questions = questions.copy()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_source" not in st.session_state:
    st.session_state.quiz_source = None

current_source = (
    source_name,
    len(questions),
    tuple(q["latin"] for q in questions),
)

if st.session_state.quiz_source != current_source:
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.quiz_source = current_source


# --------------------------------------------------
# QUIZ FORM
# --------------------------------------------------

st.subheader("Choose the correct meaning")

with st.form("botanical_quiz"):
    for number, question in enumerate(
        quiz_questions,
        start=1,
    ):
        latin = question["latin"]

        st.markdown(
            f"### {number}. {latin}"
        )

        st.write(
            f"**Plant:** {question['plant']}"
        )

        st.write(
            f"**Common name:** {question['plant_name']}"
        )

        options = question["options_list"].copy()

        if shuffle_options:
            random.Random(
                f"{latin}-options"
            ).shuffle(options)

        previous_answer = (
            st.session_state.quiz_answers.get(latin)
        )

        selected_index = 0

        if previous_answer in options:
            selected_index = options.index(
                previous_answer
            )

        selected = st.radio(
            "Select the meaning:",
            options,
            index=selected_index,
            key=f"question_{latin}",
        )

        st.session_state.quiz_answers[latin] = selected

        st.divider()

    submitted = st.form_submit_button(
        "Check Answers",
        type="primary",
        use_container_width=True,
    )

    if submitted:
        st.session_state.quiz_submitted = True


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

if st.session_state.quiz_submitted:
    correct_count = 0

    st.subheader("Quiz Results")

    for number, question in enumerate(
        quiz_questions,
        start=1,
    ):
        latin = question["latin"]
        correct_answer = question["answer"]

        user_answer = (
            st.session_state.quiz_answers.get(latin)
        )

        is_correct = user_answer == correct_answer

        if is_correct:
            correct_count += 1

            st.success(
                f"{number}. {latin}: Correct!"
            )
        else:
            st.error(
                f"{number}. {latin}: Incorrect. "
                f"Correct answer: {correct_answer}"
            )

        if show_explanation:
            st.write(question["explanation"])

        st.caption(
            f"Scientific name: {question['plant']}"
        )

    total = len(quiz_questions)
    percentage = round(
        correct_count / total * 100,
        1,
    )

    st.metric(
        "Final Score",
        f"{correct_count}/{total}",
        f"{percentage}%",
    )

    st.progress(correct_count / total)

    if percentage == 100:
        st.balloons()
        st.success("Perfect score! Excellent work.")

    elif percentage >= 70:
        st.success("Good work! Keep learning.")

    else:
        st.info(
            "Review the explanations and try again."
        )

    if st.button("Restart Quiz"):
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.rerun()
