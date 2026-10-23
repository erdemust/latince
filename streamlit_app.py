import html
import random
import time
import uuid

import pandas as pd
import streamlit as st


# ============================================================
# 1. SAYFA AYARLARI
# ============================================================

st.set_page_config(
    page_title="Botanica Akademi | Latince Botanik",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. TASARIM SİSTEMİ
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --botanica-green: #3ddc97;
        --botanica-deep: #123c2d;
        --botanica-soft: #e5f7ed;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at top left,
                rgba(61, 220, 151, 0.09),
                transparent 40%
            );
    }

    .block-container {
        max-width: 900px;
        padding: 2rem 1.2rem 4rem;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    .hero {
        padding: 2.2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(61, 220, 151, .25);
        border-radius: 26px;
        background:
            linear-gradient(
                135deg,
                rgba(18, 60, 45, .98),
                rgba(23, 83, 60, .94)
            );
        color: #f4fff8;
        box-shadow: 0 18px 45px rgba(0, 0, 0, .10);
    }

    .eyebrow {
        color: #7df0b8;
        font-size: .76rem;
        font-weight: 850;
        letter-spacing: .16em;
        text-transform: uppercase;
        margin-bottom: .7rem;
    }

    .hero h1 {
        color: #ffffff;
        font-size: clamp(2rem, 6vw, 3.3rem);
        font-weight: 900;
        letter-spacing: -.055em;
        line-height: 1.1;
        margin: .2rem 0 1rem;
    }

    .hero h2 {
        color: #ffffff;
    }

    .hero p {
        color: #d9f5e5;
        line-height: 1.8;
        font-size: 1rem;
    }

    .hero-badges {
        display: flex;
        flex-wrap: wrap;
        gap: .5rem;
        margin-top: 1.3rem;
    }

    .badge {
        display: inline-block;
        padding: .45rem .75rem;
        border: 1px solid rgba(255, 255, 255, .20);
        border-radius: 999px;
        background: rgba(255, 255, 255, .08);
        color: #eafff2;
        font-size: .8rem;
        font-weight: 650;
    }

    .panel {
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--default-border-color);
        border-radius: 22px;
        background: var(--secondary-background-color);
    }

    .latin {
        font-size: clamp(2.3rem, 8vw, 4rem);
        font-weight: 900;
        font-style: italic;
        letter-spacing: -.055em;
        overflow-wrap: anywhere;
        line-height: 1.1;
        margin: .6rem 0 1rem;
    }

    .metric-card {
        padding: 1rem;
        min-height: 105px;
        border: 1px solid var(--default-border-color);
        border-radius: 18px;
        background: var(--secondary-background-color);
    }

    .metric-label {
        font-size: .78rem;
        opacity: .7;
        margin-bottom: .45rem;
    }

    .metric-value {
        font-size: clamp(1.35rem, 4vw, 2rem);
        font-weight: 900;
        letter-spacing: -.04em;
        overflow-wrap: anywhere;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        min-height: 48px;
        width: 100%;
        border-radius: 13px;
        font-weight: 750;
    }

    @media (max-width: 600px) {
        .hero {
            padding: 1.4rem;
            border-radius: 20px;
        }

        .panel {
            padding: 1rem;
        }

        .block-container {
            padding: 1rem .8rem 3rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. SORU HAVUZU
# ============================================================
#
# BURAYA ÖNCEKİ KODUNDAKİ RAW_QUESTIONS LİSTESİNİN
# TAMAMINI, BAŞLANGIÇ VE BİTİŞ KÖŞELİ PARANTEZLERİYLE
# BİRLİKTE AKTAR.
#
# Her soru şu yapıda olmalıdır:
#
# (
#     "Glaber",
#     "Tüysüz veya pürüzsüz",
#     ["Tüylü", "Tüysüz veya pürüzsüz", "Dikenli", "Benekli"],
#     "Acer glabrum",
#     "Pürüzsüz akçaağaç",
#     "Botanik açıklaması."
# )
#
# Aşağıdaki örnekler, uygulamanın hemen çalışabilmesi
# için eklenmiştir. Tam soru havuzunu kullanacaksan
# bunları kendi RAW_QUESTIONS listenle değiştir.
# ============================================================

RAW_QUESTIONS = [
    (
        "Glaber",
        "Tüysüz veya pürüzsüz",
        ["Tüylü", "Tüysüz veya pürüzsüz", "Dikenli", "Benekli"],
        "Acer glabrum",
        "Pürüzsüz akçaağaç",
        "'Glaber' tüysüz veya pürüzsüz anlamına gelir. "
        "Botanikte bitki yüzeyinde tüy bulunmamasını ifade eder."
    ),
    (
        "Hirsutus",
        "Uzun veya sert tüylü",
        ["Pürüzsüz", "Parlak", "Uzun veya sert tüylü", "Tüysüz"],
        "Rosa hirsuta",
        "Tüylü gül",
        "'Hirsutus' uzun veya sert tüylerle kaplı anlamına gelir."
    ),
    (
        "Albus",
        "Beyaz",
        ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "Nymphaea alba",
        "Beyaz nilüfer",
        "'Albus' beyaz anlamına gelir. 'Alba', sıfatın dişil biçimidir."
    ),
    (
        "Niger",
        "Siyah",
        ["Yeşil", "Mavi", "Siyah", "Pembe"],
        "Sambucus nigra",
        "Kara mürver",
        "'Niger' siyah veya çok koyu renkli anlamına gelir."
    ),
    (
        "Ruber",
        "Kırmızı",
        ["Kırmızı", "Mor", "Gri", "Beyaz"],
        "Quercus rubra",
        "Kırmızı meşe",
        "'Ruber' kırmızı anlamına gelir. 'Rubra', sıfatın dişil biçimidir."
    ),
    (
        "Roseus",
        "Gül pembesi",
        ["Turuncu", "Kahverengi", "Sarı", "Gül pembesi"],
        "Catharanthus roseus",
        "Madagaskar cezayir menekşesi",
        "'Roseus' gül renginde veya gül pembesi anlamına gelir."
    ),
    (
        "Purpureus",
        "Mor veya erguvan",
        ["Mavi", "Mor veya erguvan", "Yeşil", "Gümüş"],
        "Echinacea purpurea",
        "Mor ekinezya",
        "'Purpureus' mor veya erguvan tonlarını ifade eder."
    ),
    (
        "Flavus",
        "Sarı",
        ["Yeşil", "Mor", "Pembe", "Sarı"],
        "Glaucium flavum",
        "Sarı boynuzlu haşhaş",
        "'Flavus' sarı anlamına gelir."
    ),
    (
        "Viridis",
        "Yeşil",
        ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "Helleborus viridis",
        "Yeşil çöpleme",
        "'Viridis' yeşil anlamına gelir."
    ),
    (
        "Glaucus",
        "Mavimsi yeşil veya grimsi mavi",
        [
            "Parlak sarı",
            "Koyu kırmızı",
            "Saf beyaz",
            "Mavimsi yeşil veya grimsi mavi",
        ],
        "Rosa glauca",
        "Mavimsi yapraklı gül",
        "'Glaucus' mavimsi yeşil veya grimsi mavi tonları ifade eder."
    ),
    (
        "Dentatus",
        "Dişli kenarlı",
        ["Düz kenarlı", "Dişli kenarlı", "Yuvarlak", "Tüysüz"],
        "Urtica dioica",
        "Büyük ısırgan",
        "'Dentatus' dişli anlamına gelir ve yaprak kenarlarını tanımlar."
    ),
    (
        "Spinosus",
        "Dikenli",
        ["Düz yüzeyli", "Dikenli", "Tüysüz", "Yumuşak"],
        "Ruscus aculeatus",
        "Tavşanmemesi",
        "'Spinosus' dikenli anlamına gelir."
    ),
]


# ============================================================
# 4. SORU HAVUZUNU DOĞRULAMA
# ============================================================

def build_question_pool():
    result = []
    seen = set()

    for item in RAW_QUESTIONS:
        if not isinstance(item, (tuple, list)) or len(item) != 6:
            continue

        latin, answer, options, plant, plant_name, explanation = item

        if not all(
            isinstance(value, str) and value.strip()
            for value in (
                latin,
                answer,
                plant,
                plant_name,
                explanation,
            )
        ):
            continue

        latin = latin.strip()
        answer = answer.strip()

        key = latin.casefold()

        if key in seen:
            continue

        if not isinstance(options, (list, tuple)):
            continue

        clean_options = []

        for option in options:
            if not isinstance(option, str):
                continue

            option = option.strip()

            if option and option not in clean_options:
                clean_options.append(option)

        if answer not in clean_options:
            clean_options.append(answer)

        if len(clean_options) < 4:
            continue

        seen.add(key)

        result.append(
            {
                "latin": latin,
                "question": (
                    f"'{latin}' hangi rengi veya "
                    "özelliği ifade eder?"
                ),
                "answer": answer,
                "options": clean_options,
                "plant": plant.strip(),
                "plant_name": plant_name.strip(),
                "explanation": explanation.strip(),
            }
        )

    return result


QUESTIONS = build_question_pool()


# ============================================================
# 5. OTURUM DURUMU
# ============================================================

DEFAULTS = {
    "stage": "register",
    "name": "",
    "score": 0,
    "start_time": None,
    "elapsed_time": 0.0,
    "quiz_questions": [],
    "current_question": 0,
    "answers": [],
    "leaderboard": [],
    "run_id": None,
    "submitted_run_id": None,
    "quiz_length": 10,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = (
            value.copy()
            if isinstance(value, (dict, list))
            else value
        )


# ============================================================
# 6. YARDIMCI FONKSİYONLAR
# ============================================================

def safe_text(value):
    return html.escape(str(value))


def format_seconds(seconds):
    try:
        seconds = max(0, int(seconds))
    except (TypeError, ValueError, OverflowError):
        seconds = 0

    minutes, remaining = divmod(seconds, 60)

    if minutes:
        return f"{minutes} dk {remaining} sn"

    return f"{remaining} sn"


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{safe_text(label)}</div>
            <div class="metric-value">{safe_text(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 7. SORU OLUŞTURMA
# ============================================================

def make_balanced_questions(count):
    if not QUESTIONS:
        raise ValueError("Soru havuzu boş.")

    try:
        count = int(count)
    except (TypeError, ValueError):
        raise ValueError("Soru sayısı geçersiz.")

    if count < 1 or count > len(QUESTIONS):
        raise ValueError(
            f"Soru sayısı 1 ile {len(QUESTIONS)} arasında olmalıdır."
        )

    source = QUESTIONS.copy()
    random.shuffle(source)

    selected = source[:count]

    positions = [i % 4 for i in range(count)]
    random.shuffle(positions)

    prepared = []

    for question, correct_position in zip(selected, positions):
        correct_answer = question["answer"]

        distractors = [
            option
            for option in question["options"]
            if option != correct_answer
        ]

        random.shuffle(distractors)

        if len(distractors) < 3:
            for other_question in QUESTIONS:
                for option in other_question["options"]:
                    if (
                        option != correct_answer
                        and option not in distractors
                    ):
                        distractors.append(option)

                    if len(distractors) >= 3:
                        break

                if len(distractors) >= 3:
                    break

        if len(distractors) < 3:
            raise ValueError(
                f"{question['latin']} sorusu için "
                "yeterli cevap seçeneği bulunamadı."
            )

        options = distractors[:3]
        options.insert(correct_position, correct_answer)

        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(
                f"{question['latin']} sorusunun seçenekleri geçersiz."
            )

        item = question.copy()
        item["options"] = options

        prepared.append(item)

    if len(prepared) != count:
        raise ValueError("Soru listesi hazırlanamadı.")

    return prepared


# ============================================================
# 8. TEST YÖNETİMİ
# ============================================================

def start_quiz(name, count):
    name = str(name).strip()

    if not name:
        raise ValueError("Lütfen bir ad veya takma ad gir.")

    if len(name) > 50:
        raise ValueError("Ad en fazla 50 karakter olabilir.")

    questions = make_balanced_questions(count)

    st.session_state.update(
        {
            "stage": "quiz",
            "name": name,
            "score": 0,
            "start_time": time.time(),
            "elapsed_time": 0.0,
            "quiz_questions": questions,
            "current_question": 0,
            "answers": [],
            "run_id": str(uuid.uuid4()),
            "submitted_run_id": None,
            "quiz_length": len(questions),
        }
    )


def save_result():
    run_id = st.session_state.run_id

    if not run_id:
        return

    if st.session_state.submitted_run_id == run_id:
        return

    questions = st.session_state.quiz_questions
    answers = st.session_state.answers

    if not questions or len(answers) != len(questions):
        return

    score = sum(
        1
        for answer in answers
        if answer.get("is_correct") is True
    )

    start_time = st.session_state.start_time

    elapsed = (
        max(0.0, time.time() - start_time)
        if start_time is not None
        else 0.0
    )

    st.session_state.score = score
    st.session_state.elapsed_time = round(elapsed, 2)

    st.session_state.leaderboard.append(
        {
            "İsim": st.session_state.name,
            "Doğru Sayısı": score,
            "Toplam Soru": len(questions),
            "Başarı (%)": round(score / len(questions) * 100, 1),
            "Süre (sn)": round(elapsed, 2),
        }
    )

    st.session_state.submitted_run_id = run_id


def reset_quiz(clear_name=False):
    st.session_state.update(
        {
            "stage": "register",
            "score": 0,
            "start_time": None,
            "elapsed_time": 0.0,
            "quiz_questions": [],
            "current_question": 0,
            "answers": [],
            "run_id": None,
            "submitted_run_id": None,
        }
    )

    if clear_name:
        st.session_state.name = ""


# ============================================================
# 9. LİDERLİK TABLOSU
# ============================================================

def render_leaderboard():
    records = st.session_state.leaderboard

    if not records:
        st.info(
            "🌱 Henüz sonuç kaydedilmedi. "
            "İlk testi tamamlayarak liderlik tablosunu oluşturabilirsin."
        )
        return

    df = pd.DataFrame(records)

    df = df.sort_values(
        by=["Başarı (%)", "Doğru Sayısı", "Süre (sn)"],
        ascending=[False, False, True],
    ).reset_index(drop=True)

    df.index = df.index + 1
    df.index.name = "Sıra"

    st.dataframe(
        df[
            [
                "İsim",
                "Doğru Sayısı",
                "Toplam Soru",
                "Başarı (%)",
                "Süre (sn)",
            ]
        ],
        use_container_width=True,
    )


# ============================================================
# 10. BAŞLIK
# ============================================================

def render_header():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">🌿 BOTANICA AKADEMİ</div>
            <h1>Doğanın Dilini Keşfet.</h1>
            <p>
                Latince botanik terimlerini öğren,
                renklerin ardındaki anlamları keşfet
                ve bilgini test et.
            </p>
            <div class="hero-badges">
                <span class="badge">🌱 Botanik</span>
                <span class="badge">📚 Latince</span>
                <span class="badge">🎯 Bilgi Yarışması</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 11. KAYIT EKRANI
# ============================================================

def render_register():
    render_header()

    st.subheader("🌱 Yeni Bir Keşfe Başla")

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Soru havuzu", len(QUESTIONS))

    with col2:
        metric_card("Cevap seçeneği", "4")

    with col3:
        metric_card("Kategori", "Botanik")

    if not QUESTIONS:
        st.error("Soru havuzu boş veya geçersiz.")
        return

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    with st.form("register_form"):
        name = st.text_input(
            "Adın veya takma adın",
            value=st.session_state.name,
            placeholder="Örn. Botanica",
            max_chars=50,
        )

        maximum = len(QUESTIONS)

        count_options = sorted(
            set(
                n
                for n in [5, 10, 15, 20, 30, 40, 50, 60, maximum]
                if 1 <= n <= maximum
            )
        )

        default_count = min(10, maximum)

        selected_count = st.selectbox(
            "Test uzunluğu",
            count_options,
            index=count_options.index(default_count),
            format_func=lambda n: f"{n} soru",
        )

        submitted = st.form_submit_button(
            "Keşfe Başla 🚀",
            use_container_width=True,
            type="primary",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not name.strip():
            st.warning("Lütfen adını veya bir takma ad gir.")
        else:
            try:
                start_quiz(name, selected_count)
                st.rerun()
            except (ValueError, TypeError, KeyError) as exc:
                st.error(f"Test başlatılamadı: {exc}")

    st.divider()

    st.subheader("🏆 Liderlik Tablosu")
    render_leaderboard()

    with st.expander("📖 Nasıl oynanır?"):
        st.markdown(
            """
            1. Adını yaz ve test uzunluğunu seç.
            2. Latince terimin anlamını dört seçenek arasından bul.
            3. Cevabının doğruluğunu kontrol et.
            4. Açıklamaları okuyarak botanik bilgini geliştir.
            5. Test sonunda puanını ve süreni incele.
            """
        )


# ============================================================
# 12. SORU EKRANI
# ============================================================

def render_quiz():
    questions = st.session_state.quiz_questions
    index = st.session_state.current_question

    if not questions:
        st.error("Soru bulunamadı. Yeni bir test başlatın.")

        if st.button("Ana Sayfaya Dön"):
            reset_quiz()
            st.rerun()

        return

    if index < 0 or index >= len(questions):
        st.session_state.stage = "result"
        st.rerun()
        return

    q = questions[index]

    st.progress((index + 1) / len(questions))

    col1, col2 = st.columns(2)

    with col1:
        st.caption(f"Soru {index + 1} / {len(questions)}")

    with col2:
        st.caption(f"Puan: {st.session_state.score}")

    st.markdown(
        f"""
        <div class="panel">
            <div class="eyebrow">Botanik Terim</div>
            <div class="latin">{safe_text(q['latin'])}</div>
            <p>{safe_text(q['question'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    options = q["options"]

    form_key = (
        f"quiz_form_"
        f"{st.session_state.run_id}_"
        f"{index}"
    )

    with st.form(form_key):
        selected = st.radio(
            "Cevabını seç:",
            options,
            index=None,
            key=f"answer_{st.session_state.run_id}_{index}",
        )

        submitted = st.form_submit_button(
            "Cevabı Kontrol Et ✨",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        if selected is None:
            st.warning("Lütfen bir cevap seçin.")
            return

        if len(st.session_state.answers) != index:
            st.warning(
                "Cevap durumu beklenmedik biçimde değişti. "
                "Lütfen sayfayı kontrol edin."
            )
            return

        if selected not in options:
            st.error("Geçersiz cevap seçeneği.")
            return

        is_correct = selected == q["answer"]

        st.session_state.answers.append(
            {
                "latin": q["latin"],
                "question": q["question"],
                "selected": selected,
                "correct": q["answer"],
                "is_correct": is_correct,
                "plant": q["plant"],
                "plant_name": q["plant_name"],
                "explanation": q["explanation"],
            }
        )

        if is_correct:
            st.session_state.score += 1

        st.session_state.stage = "feedback"
        st.rerun()


# ============================================================
# 13. GERİ BİLDİRİM EKRANI
# ============================================================

def render_feedback():
    answers = st.session_state.answers

    if not answers:
        st.session_state.stage = "quiz"
        st.rerun()
        return

    answer = answers[-1]

    if answer["is_correct"]:
        st.success("🎉 Harika! Doğru cevap.")
    else:
        st.error(
            f"Yanlış cevap. Doğru cevap: "
            f"**{safe_text(answer['correct'])}**"
        )

    st.markdown(
        f"""
        <div class="panel">
            <div class="eyebrow">Botanik Bilgisi</div>
            <div style="
                font-size: 1.2rem;
                font-weight: 800;
                font-style: italic;
            ">
                🌿 {safe_text(answer['plant'])}
            </div>
            <p style="opacity: 0.75; margin-top: 0.3rem;">
                {safe_text(answer['plant_name'])}
            </p>
            <p style="margin-top: 0.8rem;">
                {safe_text(answer['explanation'])}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current = st.session_state.current_question
    total = len(st.session_state.quiz_questions)

    label = (
        "Sonuçları Gör 🏆"
        if current + 1 >= total
        else "Sonraki Soru ➡️"
    )

    if st.button(
        label,
        use_container_width=True,
        type="primary",
    ):
        if current + 1 >= total:
            save_result()
            st.session_state.stage = "result"
        else:
            st.session_state.current_question += 1
            st.session_state.stage = "quiz"

        st.rerun()


# ============================================================
# 14. SONUÇ EKRANI
# ============================================================

def render_result():
    questions = st.session_state.quiz_questions
    total = len(questions)
    score = st.session_state.score

    if total == 0:
        st.warning("Gösterilecek test sonucu bulunamadı.")

        if st.button("Ana Sayfaya Dön"):
            reset_quiz()
            st.rerun()

        return

    percentage = score / total * 100

    if score == total:
        st.balloons()

    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">Quiz Tamamlandı 🌿</div>
            <div style="
                font-size: 3.5rem;
                font-weight: 900;
                margin: 0.5rem 0;
            ">
                {score} / {total}
            </div>
            <h2>Başarı oranı: %{percentage:.0f}</h2>
            <p style="margin-top: 0.5rem;">
                Tamamlanma süresi:
                <strong>
                    {safe_text(format_seconds(
                        st.session_state.elapsed_time
                    ))}
                </strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if percentage >= 80:
        st.success(
            "Mükemmel! Botanik renk bilgine hâkim görünüyorsun."
        )
    elif percentage >= 50:
        st.info(
            "Güzel iş! Birkaç tekrar ile daha da ilerleyebilirsin."
        )
    else:
        st.warning(
            "Yeni bir turla bilgilerini geliştirebilirsin."
        )

    st.subheader("🏆 Liderlik Tablosu")
    render_leaderboard()

    st.divider()

    with st.expander("📝 Cevaplarını İncele"):
        for i, answer in enumerate(
            st.session_state.answers,
            start=1,
        ):
            status = (
                "✅ Doğru"
                if answer["is_correct"]
                else "❌ Yanlış"
            )

            st.markdown(
                f"**{i}. {safe_text(answer['latin'])} — {status}**"
            )

            st.write(
                f"Verdiğin cevap: {answer['selected']}"
            )

            st.write(
                f"Doğru cevap: {answer['correct']}"
            )

            st.caption(
                f"{answer['plant']} — {answer['plant_name']}"
            )

            st.write(answer["explanation"])
            st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Tekrar Oyna 🔄",
            use_container_width=True,
        ):
            reset_quiz()
            st.rerun()

    with col2:
        if st.button(
            "Ana Sayfaya Dön 🏠",
            use_container_width=True,
        ):
            reset_quiz(clear_name=True)
            st.rerun()


# ============================================================
# 15. ANA YÖNLENDİRME
# ============================================================

if not QUESTIONS:
    st.error(
        "Soru havuzu yüklenemedi. "
        "RAW_QUESTIONS listesini kontrol edin."
    )

elif st.session_state.stage == "register":
    render_register()

elif st.session_state.stage == "quiz":
    render_quiz()

elif st.session_state.stage == "feedback":
    render_feedback()

elif st.session_state.stage == "result":
    render_result()

else:
    st.session_state.stage = "register"
    st.rerun()
