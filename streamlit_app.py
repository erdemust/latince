import random
import ast
import csv
import io
from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Botanical Latin Quiz",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CONSTANTS
# --------------------------------------------------

DATA_FILE = Path(__file__).parent / "botanical_terms.csv"

REQUIRED_COLUMNS = [
    "category",
    "latin",
    "answer",
    "options",
    "plant",
    "plant_name",
    "explanation",
]


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f8f4;
    }

    .main-title {
        text-align: center;
        color: #245c3a;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #647568;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .term-card {
        background-color: white;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #dce8dc;
        margin: 15px 0;
    }

    .latin-term {
        color: #245c3a;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
    }

    .plant-name {
        color: #68786a;
        text-align: center;
        font-style: italic;
        margin-bottom: 15px;
    }

    .result-card {
        background-color: white;
        border-radius: 14px;
        padding: 22px;
        border: 1px solid #dce8dc;
        text-align: center;
    }

    div.stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 42px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

@st.cache_data
def load_data(uploaded_bytes=None, file_mtime=None):
    """
    Load the botanical CSV.

    The uploaded_bytes argument also allows users to upload
    their own dataset through the sidebar.
    """

    if uploaded_bytes is not None:
        source = io.BytesIO(uploaded_bytes)
    else:
        if not DATA_FILE.exists():
            return pd.DataFrame(columns=REQUIRED_COLUMNS)

        source = DATA_FILE

    try:
        df = pd.read_csv( source,    encoding="utf-8-sig",        dtype=str,    keep_default_na=False,    quoting=csv.QUOTE_MINIMAL,    skipinitialspace=True,
    engine="python",)

    except (UnicodeDecodeError, pd.errors.ParserError) as exc:
        raise ValueError(
            f"Could not read the CSV file: {exc}"
        ) from exc

    df.columns = df.columns.str.strip().str.lower()

    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(
            "Missing required CSV columns: "
            + ", ".join(sorted(missing))
        )

    for column in REQUIRED_COLUMNS:
        df[column] = df[column].astype(str).str.strip()

    # Remove incomplete questions.
    df = df[
        (df["category"] != "")
        & (df["latin"] != "")
        & (df["answer"] != "")
        & (df["options"] != "")
    ].copy()

    # Parse and validate the answer choices.
    valid_rows = []

    for index, row in df.iterrows():
        options = parse_options(row["options"])

        if len(options) < 2:
            continue

        if row["answer"] not in options:
            continue

        df.at[index, "options"] = options
        valid_rows.append(index)

    df = df.loc[valid_rows].reset_index(drop=True)

    return df


def parse_options(value):
    """
    Supports standard CSV options such as:
    "Red, Green, Blue, Yellow"

    Also supports Python-style lists such as:
    ['Red', 'Green', 'Blue', 'Yellow']
    """

    if isinstance(value, list):
        return [
            str(option).strip()
            for option in value
            if str(option).strip()
        ]

    value = str(value).strip()

    if not value:
        return []

    # Support a list stored as a string.
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)

            if isinstance(parsed, list):
                return list(
                    dict.fromkeys(
                        str(option).strip()
                        for option in parsed
                        if str(option).strip()
                    )
                )
        except (ValueError, SyntaxError):
            pass

    # Standard options are comma-separated.
    return list(
        dict.fromkeys(
            option.strip()
            for option in value.split(",")
            if option.strip()
        )
    )


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

def initialize_state():
    defaults = {
        "quiz_started": False,
        "quiz_finished": False,
        "questions": [],
        "current_question": 0,
        "score": 0,
        "answers": [],
        "submitted": False,
        "selected_answer": None,
        "quiz_config": {},
        "question_count": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz():
    st.session_state.quiz_started = False
    st.session_state.quiz_finished = False
    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.submitted = False
    st.session_state.selected_answer = None
    st.session_state.quiz_config = {}
    st.session_state.question_count = 0


initialize_state()


# --------------------------------------------------
# QUIZ CREATION
# --------------------------------------------------

def start_quiz(df, selected_categories, number_of_questions,
               shuffle_questions, shuffle_options):

    filtered = df[
        df["category"].isin(selected_categories)
    ].copy()

    if filtered.empty:
        st.error("No questions found for the selected categories.")
        return

    if shuffle_questions:
        filtered = filtered.sample(
            frac=1,
            random_state=None,
        ).reset_index(drop=True)

    filtered = filtered.head(number_of_questions)

    questions = []

    for _, row in filtered.iterrows():
        options = list(row["options"])

        if shuffle_options:
            random.shuffle(options)

        questions.append(
            {
                "category": row["category"],
                "latin": row["latin"],
                "answer": row["answer"],
                "options": options,
                "plant": row["plant"],
                "plant_name": row["plant_name"],
                "explanation": row["explanation"],
            }
        )

    st.session_state.questions = questions
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.submitted = False
    st.session_state.selected_answer = None
    st.session_state.quiz_started = True
    st.session_state.quiz_finished = False
    st.session_state.question_count = len(questions)

    st.session_state.quiz_config = {
        "categories": selected_categories,
        "shuffle_questions": shuffle_questions,
        "shuffle_options": shuffle_options,
    }


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🌿 Quiz Settings")

uploaded_file = st.sidebar.file_uploader(
    "Upload your own CSV dataset",
    type=["csv"],
    help="Your CSV must contain all seven required columns.",
)

try:
    if uploaded_file is not None:
        df = load_data(uploaded_file.getvalue())
    else:
        mtime = (
            DATA_FILE.stat().st_mtime
            if DATA_FILE.exists()
            else None
        )
        df = load_data(file_mtime=mtime)

except ValueError as exc:
    st.error(str(exc))
    st.stop()

if df.empty:
    st.warning(
        "No valid questions were found. Add botanical_terms.csv "
        "to the project folder or upload a CSV dataset."
    )
    st.stop()

categories = sorted(df["category"].unique().tolist())

st.sidebar.caption(
    f"{len(df)} questions available across "
    f"{len(categories)} categories."
)

selected_categories = st.sidebar.multiselect(
    "Choose categories",
    options=categories,
    default=categories,
    help="Select one or more categories for your quiz.",
)

available_questions = len(
    df[df["category"].isin(selected_categories)]
)

st.sidebar.metric(
    "Available questions",
    available_questions,
)

if available_questions > 0:
    number_of_questions = st.sidebar.selectbox(
        "Number of questions",
        options=sorted(
            set(
                [5, 10, 20, available_questions]
            )
        ),
        index=0,
    )

    number_of_questions = min(
        number_of_questions,
        available_questions,
    )
else:
    number_of_questions = 0

st.sidebar.divider()

shuffle_questions = st.sidebar.checkbox(
    "Shuffle questions",
    value=True,
)

shuffle_options = st.sidebar.checkbox(
    "Shuffle answer options",
    value=True,
)

show_botanical_details = st.sidebar.checkbox(
    "Show plant names during quiz",
    value=True,
)

st.sidebar.divider()

if st.sidebar.button(
    "🔄 Start a new quiz",
    use_container_width=True,
):
    reset_quiz()

    if selected_categories and number_of_questions > 0:
        start_quiz(
            df,
            selected_categories,
            number_of_questions,
            shuffle_questions,
            shuffle_options,
        )
        st.rerun()

if st.sidebar.button(
    "🏠 Back to quiz setup",
    use_container_width=True,
):
    reset_quiz()
    st.rerun()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🌿 Botanical Latin Quiz</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Explore botanical vocabulary, plant morphology, colors, "
    "and scientific terminology."
    "</div>",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HOME / SETUP SCREEN
# --------------------------------------------------

if not st.session_state.quiz_started:

    st.subheader("Welcome to the Botanical Quiz!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total questions", len(df))

    with col2:
        st.metric("Categories", len(categories))

    with col3:
        st.metric("Plant examples", df["plant"].nunique())

    st.markdown("---")

    st.subheader("Available categories")

    category_columns = st.columns(2)

    for index, category in enumerate(categories):
        category_df = df[df["category"] == category]

        with category_columns[index % 2]:
            with st.container(border=True):
                st.markdown(f"### 🌱 {category}")
                st.write(
                    f"**{len(category_df)} questions**"
                )

                examples = category_df["latin"].head(3).tolist()

                st.caption(
                    "Examples: " + ", ".join(examples)
                )

    st.markdown("---")

    if not selected_categories:
        st.info("Choose at least one category in the sidebar.")

    elif available_questions == 0:
        st.warning("No questions are available for this selection.")

    else:
        if st.button(
            "🚀 Start Quiz",
            type="primary",
            use_container_width=True,
        ):
            start_quiz(
                df,
                selected_categories,
                number_of_questions,
                shuffle_questions,
                shuffle_options,
            )
            st.rerun()


# --------------------------------------------------
# QUIZ SCREEN
# --------------------------------------------------

elif (
    st.session_state.quiz_started
    and not st.session_state.quiz_finished
):

    questions = st.session_state.questions
    index = st.session_state.current_question
    total = len(questions)

    if index >= total:
        st.session_state.quiz_finished = True
        st.rerun()

    question = questions[index]

    st.progress(
        (index + 1) / total,
        text=f"Question {index + 1} of {total}",
    )

    correct_so_far = st.session_state.score

    col1, col2, col3 = st.columns(3)

    col1.metric("Question", f"{index + 1}/{total}")
    col2.metric("Correct answers", correct_so_far)
    col3.metric(
        "Current accuracy",
        f"{(correct_so_far / max(index, 1)) * 100:.0f}%"
        if index > 0
        else "—",
    )

    st.markdown("---")

    st.caption(f"Category: {question['category']}")

    st.markdown(
        f'<div class="term-card">'
        f'<div class="latin-term">{question["latin"]}</div>'
        f'<div class="plant-name">'
        f'{question["plant_name"] if show_botanical_details else "Identify the botanical term"}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if show_botanical_details and question["plant"]:
        st.caption(
            f"Scientific name: {question['plant']}"
        )

    st.subheader("What does this term mean?")

    # Use a stable key for each question.
    answer_key = f"answer_{index}"

    if not st.session_state.submitted:

        selected_answer = st.radio(
            "Choose the correct answer:",
            options=question["options"],
            index=None,
            key=answer_key,
        )

        if st.button(
            "Submit Answer",
            type="primary",
            use_container_width=True,
            disabled=selected_answer is None,
        ):
            st.session_state.selected_answer = selected_answer
            st.session_state.submitted = True

            is_correct = (
                selected_answer == question["answer"]
            )

            if is_correct:
                st.session_state.score += 1

            st.session_state.answers.append(
                {
                    "latin": question["latin"],
                    "category": question["category"],
                    "selected": selected_answer,
                    "correct": question["answer"],
                    "is_correct": is_correct,
                    "explanation": question["explanation"],
                    "plant": question["plant"],
                }
            )

            st.rerun()

    else:

        selected_answer = st.session_state.selected_answer
        is_correct = selected_answer == question["answer"]

        if is_correct:
            st.success("✅ Correct answer!")
        else:
            st.error("❌ Incorrect answer.")

            st.markdown(
                f"**Correct answer:** {question['answer']}"
            )

        with st.container(border=True):
            st.markdown("### Explanation")
            st.write(question["explanation"])

            if question["plant"]:
                st.caption(
                    f"Plant example: {question['plant']}"
                )

        button_label = (
            "🏁 View Results"
            if index == total - 1
            else "➡️ Next Question"
        )

        if st.button(
            button_label,
            type="primary",
            use_container_width=True,
        ):
            st.session_state.current_question += 1
            st.session_state.submitted = False
            st.session_state.selected_answer = None
            st.rerun()


# --------------------------------------------------
# RESULTS SCREEN
# --------------------------------------------------

elif st.session_state.quiz_finished:

    answers = st.session_state.answers
    total = len(answers)
    score = st.session_state.score

    percentage = (
        (score / total) * 100
        if total
        else 0
    )

    st.balloons()

    st.subheader("🎉 Quiz Completed!")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Final Score",
            f"{score}/{total}",
        )

    with col2:
        st.metric(
            "Accuracy",
            f"{percentage:.1f}%",
        )

    with col3:
        st.metric(
            "Incorrect Answers",
            total - score,
        )

    if percentage >= 90:
        st.success(
            "Outstanding! You have an excellent understanding "
            "of these botanical terms."
        )
    elif percentage >= 70:
        st.success(
            "Great work! Review the missed questions to improve further."
        )
    elif percentage >= 50:
        st.info(
            "Good effort! More practice will help reinforce your knowledge."
        )
    else:
        st.warning(
            "Keep practicing! Review the explanations and try again."
        )

    st.markdown("---")

    st.subheader("📚 Review Your Answers")

    filter_mode = st.selectbox(
        "Filter questions",
        options=[
            "All questions",
            "Incorrect answers only",
            "Correct answers only",
        ],
    )

    for number, answer in enumerate(answers, start=1):

        if (
            filter_mode == "Incorrect answers only"
            and answer["is_correct"]
        ):
            continue

        if (
            filter_mode == "Correct answers only"
            and not answer["is_correct"]
        ):
            continue

        icon = "✅" if answer["is_correct"] else "❌"

        with st.expander(
            f"{icon} {number}. {answer['latin']} "
            f"— {answer['category']}"
        ):
            st.write(
                f"**Your answer:** {answer['selected']}"
            )

            st.write(
                f"**Correct answer:** {answer['correct']}"
            )

            st.write(
                f"**Explanation:** {answer['explanation']}"
            )

            if answer["plant"]:
                st.caption(
                    f"Scientific plant name: {answer['plant']}"
                )

    st.markdown("---")

    # Download the user's results.
    results_df = pd.DataFrame(answers)

    csv_data = results_df.to_csv(
        index=False,
        encoding="utf-8-sig",
    )

    st.download_button(
        label="⬇️ Download Results as CSV",
        data=csv_data,
        file_name="botanical_quiz_results.csv",
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
