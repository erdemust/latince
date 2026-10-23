from future import annotations
import csv 
import io 
import random 
from pathlib import Path
import pandas as pd 
import streamlit as st




============================================================
CONFIGURATION
============================================================

st.set_page_config( page_title="Botanical Latin Quiz", page_icon="🌿", layout="wide", initial_sidebar_state="expanded", )

APP_TITLE = "🌿 Botanical Latin Quiz" DEFAULT_CSV = Path(file).parent / "botanical_terms.csv"

REQUIRED_COLUMNS = [ "latin", "answer", "options", "plant", "plant_name", "explanation", ]

OPTION_SEPARATOR = ","

st.title(APP_TITLE) st.caption( "Learn botanical Latin through interactive multiple-choice quizzes." )

============================================================
SESSION STATE
============================================================

def initialize_state() -> None: """Initialize session state without overwriting existing progress."""

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
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_quiz() -> None: """Clear the current quiz and its progress."""

st.session_state.quiz_questions = []
st.session_state.current_question = 0
st.session_state.score = 0
st.session_state.answered = False
st.session_state.selected_answer = None
st.session_state.quiz_finished = False
st.session_state.quiz_started = False
st.session_state.question_results = []
st.session_state.quiz_config = None


initialize_state()

============================================================
CSV LOADING
============================================================

def decode_csv(raw_bytes: bytes) -> str: """Decode CSV using common text encodings."""

for encoding in ("utf-8-sig", "utf-8", "cp1254", "latin-1"):
    try:
        return raw_bytes.decode(encoding)
    except UnicodeDecodeError:
        continue

raise ValueError(
    "Could not decode the CSV. Please save it as UTF-8."
)


def normalize_column_name(name: str) -> str: """Normalize CSV column names."""

return name.strip().lower().lstrip("\ufeff")


def parse_csv_text(text: str) -> pd.DataFrame: """Parse and validate a CSV document without silently dropping rows."""

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
        "Check quotation marks and commas in your CSV."
    ) from exc

if not rows:
    raise ValueError("The CSV file is empty.")

# Ignore completely empty lines.
rows = [
    row
    for row in rows
    if any(str(cell).strip() for cell in row)
]

if not rows:
    raise ValueError("The CSV contains no data.")

headers = [
    normalize_column_name(cell)
    for cell in rows[0]
]

if len(headers) != len(set(headers)):
    raise ValueError(
        "Duplicate column names found. "
        "Every column must have a unique name."
    )

missing = [
    column
    for column in REQUIRED_COLUMNS
    if column not in headers
]

if missing:
    raise ValueError(
        f"Missing required columns: {', '.join(missing)}. "
        f"Required columns: {', '.join(REQUIRED_COLUMNS)}."
    )

expected_fields = len(headers)
valid_rows = []
errors = []

for line_number, row in enumerate(rows[1:], start=2):

    if len(row) != expected_fields:
        errors.append(
            f"Line {line_number}: expected "
            f"{expected_fields} fields, found {len(row)}."
        )
        continue

    valid_rows.append(row)

if errors:
    preview = "\n".join(errors[:10])

    raise ValueError(
        "CSV structure validation failed:\n\n"
        f"{preview}\n\n"
        "No rows were silently discarded. "
        "Correct the CSV and upload it again."
    )

if not valid_rows:
    raise ValueError("The CSV contains headers but no data rows.")

df = pd.DataFrame(valid_rows, columns=headers)

# Keep values as strings.
for column in df.columns:
    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )

# Category is optional for compatibility with older CSV files.
if "category" not in df.columns:
    df["category"] = "Uncategorized"

df["category"] = df["category"].replace("", "Uncategorized")

# Required question fields.
for column in ("latin", "answer", "options"):
    empty_mask = df[column].eq("")

    if empty_mask.any():
        bad_lines = [
            str(index + 2)
            for index in df.index[empty_mask][:10]
        ]

        raise ValueError(
            f"Required field '{column}' is empty "
            f"on CSV line(s): {', '.join(bad_lines)}."
        )

# Remove exact duplicate records.
df = df.drop_duplicates().reset_index(drop=True)

if df.empty:
    raise ValueError("No questions remain after removing duplicates.")

return df


def load_csv_file(path: Path) -> pd.DataFrame: """Load the default CSV file."""

if not path.exists():
    raise FileNotFoundError(
        f"CSV file not found: {path.name}. "
        "Place botanical_terms.csv next to streamlit_app.py "
        "or upload a CSV in the sidebar."
    )

return parse_csv_text(decode_csv(path.read_bytes()))

============================================================
QUESTION VALIDATION
============================================================

def split_options(value: str) -> list[str]: """Split a quoted CSV options cell into distinct choices."""

return [
    option.strip()
    for option in value.split(OPTION_SEPARATOR)
    if option.strip()
]


def validate_questions( df: pd.DataFrame, ) -> tuple[pd.DataFrame, list[str]]: """Validate questions and return valid rows plus warnings."""

cleaned_rows = []
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
            "fewer than two distinct answer choices."
        )
        continue

    if answer.casefold() not in {
        option.casefold()
        for option in unique_options
    }:
        warnings.append(
            f"Row {index + 2} ({latin}): "
            "the correct answer does not match any option."
        )
        continue

    # Store the exact option matching the answer.
    normalized_answer = next(
        option
        for option in unique_options
        if option.casefold() == answer.casefold()
    )

    cleaned = row.to_dict()
    cleaned["answer"] = normalized_answer
    cleaned["options_list"] = unique_options

    # Fill optional display fields.
    for column in (
        "category",
        "plant",
        "plant_name",
        "explanation",
    ):
        cleaned[column] = str(
            cleaned.get(column, "")
        ).strip()

    if not cleaned["category"]:
        cleaned["category"] = "Uncategorized"

    cleaned_rows.append(cleaned)

if not cleaned_rows:
    raise ValueError(
        "No valid questions found. Check the answers and options "
        "in your CSV file."
    )

result = pd.DataFrame(cleaned_rows).reset_index(drop=True)

return result, warnings

============================================================
DATA SOURCE
============================================================

st.sidebar.header("📂 Question Database")

uploaded_file = st.sidebar.file_uploader( "Upload a CSV file", type=["csv"], help=( "Upload botanical_terms.csv. " "Your file can include a category column." ), )

try: if uploaded_file is not None: raw_bytes = uploaded_file.getvalue()

    if not raw_bytes:
        raise ValueError("The uploaded CSV file is empty.")

    source_df = parse_csv_text(decode_csv(raw_bytes))

else:
    source_df = load_csv_file(DEFAULT_CSV)

df, validation_warnings = validate_questions(source_df)


except (ValueError, FileNotFoundError) as exc:

st.error(f"Could not load the question database: {exc}")

st.info(
    "Upload a valid CSV using the sidebar, "
    "or place botanical_terms.csv next to streamlit_app.py."
)

st.stop()


except Exception as exc:

st.error(
    "An unexpected error occurred while loading the CSV. "
    "Check the file and try again."
)

st.caption(f"Technical details: {type(exc).__name__}: {exc}")

st.stop()

Display validation warnings without crashing the app.

if validation_warnings:

with st.expander(
    f"⚠️ {len(validation_warnings)} invalid question(s) skipped"
):
    for warning in validation_warnings:
        st.warning(warning)

============================================================
SIDEBAR: QUIZ CONFIGURATION
============================================================

st.sidebar.divider() st.sidebar.header("🎯 Quiz Settings")

categories = sorted( df["category"].dropna().unique().tolist(), key=str.casefold, )

selected_categories = st.sidebar.multiselect( "Choose categories", options=categories, default=categories, help="Select one or more categories to include in the quiz.", )

available_df = df[ df["category"].isin(selected_categories) ].copy()

st.sidebar.metric( "Available questions", len(available_df), )

max_questions = len(available_df)

if max_questions > 0:

number_of_questions = st.sidebar.number_input(
    "Number of questions",
    min_value=1,
    max_value=max_questions,
    value=min(10, max_questions),
    step=1,
)


else: number_of_questions = 0 st.sidebar.warning("Select at least one category with valid questions.")

shuffle_questions = st.sidebar.checkbox( "Shuffle questions", value=True, )

shuffle_options = st.sidebar.checkbox( "Shuffle answer choices", value=True, )

show_progress = st.sidebar.checkbox( "Show progress bar", value=True, )

st.sidebar.divider()

start_clicked = st.sidebar.button( "🚀 Start / Restart Quiz", type="primary", use_container_width=True, disabled=(number_of_questions == 0), )

============================================================
START OR RESTART QUIZ
============================================================

if start_clicked:

pool = available_df.to_dict("records")

if shuffle_questions:
    random.shuffle(pool)

questions = pool[:int(number_of_questions)]

# Create a fresh copy of each question so that shuffling
# never modifies the underlying dataset.
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
    "shuffle_questions": shuffle_questions,
    "shuffle_options": shuffle_options,
}

st.rerun()

============================================================
WELCOME SCREEN
============================================================

if not st.session_state.quiz_started:

st.subheader("Welcome to the Botanical Latin Quiz! 🌱")

st.write(
    "Test your knowledge of botanical Latin terms, "
    "plant morphology, colors, and scientific plant names."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Valid questions", len(df))

with col2:
    st.metric("Categories", df["category"].nunique())

with col3:
    st.metric("Selected questions", int(number_of_questions))

st.markdown("### How to play")

st.markdown(
    """
    1. Choose one or more categories in the sidebar.
    2. Select how many questions you want.
    3. Click **Start / Restart Quiz**.
    4. Select an answer and submit it.
    5. Read the explanation and continue.
    6. Review your score when you finish.
    """
)

st.markdown("### Available categories")

for category in categories:

    category_count = int(
        (df["category"] == category).sum()
    )

    st.write(f"- **{category}**: {category_count} questions")

st.stop()

============================================================
ACTIVE QUIZ
============================================================

questions = st.session_state.quiz_questions total_questions = len(questions)

if total_questions == 0:

st.error("No questions are available for this quiz.")

if st.button("Return to setup"):
    reset_quiz()
    st.rerun()

st.stop()


if st.session_state.quiz_finished:

# --------------------------------------------------------
# FINAL RESULTS
# --------------------------------------------------------

score = st.session_state.score

percentage = round(
    score / total_questions * 100,
    1,
)

st.success("🎉 Quiz completed!")

st.subheader("Your results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Correct answers",
        f"{score}/{total_questions}",
    )

with col2:
    st.metric(
        "Accuracy",
        f"{percentage}%",
    )

with col3:
    st.metric(
        "Incorrect answers",
        total_questions - score,
    )

if percentage == 100:
    st.balloons()
    st.markdown("### 🌟 Perfect score! Excellent work!")

elif percentage >= 80:
    st.markdown("### 🌿 Excellent work!")

elif percentage >= 60:
    st.markdown("### 🌱 Good progress! Keep learning.")

else:
    st.markdown("### 📚 Keep practicing. You'll improve!")

st.divider()
st.subheader("📋 Answer Review")

for index, result in enumerate(
    st.session_state.question_results,
    start=1,
):

    correct = result["is_correct"]

    icon = "✅" if correct else "❌"

    with st.expander(
        f"{icon} Question {index}: {result['latin']}"
    ):

        st.write(
            f"**Category:** {result['category']}"
        )

        st.write(
            f"**Your answer:** "
            f"{result['selected_answer'] or 'No answer'}"
        )

        st.write(
            f"**Correct answer:** {result['answer']}"
        )

        if result["plant"]:
            st.write(
                f"**Scientific name:** {result['plant']}"
            )

        if result["plant_name"]:
            st.write(
                f"**Common name:** {result['plant_name']}"
            )

        if result["explanation"]:
            st.info(result["explanation"])

if st.button(
    "🔄 Play Again",
    type="primary",
    use_container_width=True,
):

    reset_quiz()
    st.rerun()

st.stop()

============================================================
CURRENT QUESTION
============================================================

question_index = st.session_state.current_question question = questions[question_index]

st.divider()

Progress indicators.

st.subheader( f"Question {question_index + 1} of {total_questions}" )

if show_progress:

progress = (question_index + 1) / total_questions

st.progress(
    progress,
    text=(
        f"Question {question_index + 1} "
        f"of {total_questions}"
    ),
)


col1, col2 = st.columns(2)

with col1: st.metric("Current score", st.session_state.score)

with col2: st.caption( f"Category: {question['category']}" )

Main question.

st.markdown("### What does this botanical Latin term mean?")

st.markdown( f"# 🌿 {question['latin']}" )

if question["plant"]: st.caption( f"Example plant: {question['plant']}" )

------------------------------------------------------------
ANSWER FORM
------------------------------------------------------------

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

        st.warning(
            "Please select an answer before submitting."
        )

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

------------------------------------------------------------
ANSWER FEEDBACK
------------------------------------------------------------

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

    st.caption("No explanation is available for this question.")

if question["plant"]:

    st.markdown("### 🌱 Example Plant")

    st.write(
        f"**Scientific name:** {question['plant']}"
    )

    if question["plant_name"]:
        st.write(
            f"**Common name:** {question['plant_name']}"
        )

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

============================================================
FOOTER
============================================================

st.divider()

st.caption( "🌿 Botanical Latin Quiz | Learn botanical terminology " "one question at a time." )
