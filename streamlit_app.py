/* Genel görünüm */
.stApp {
    background-color: #0E1117;
    color: #FAFAFA;
}

.main .block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Başlıklar */
h1, h2, h3 {
    color: #7DD3FC !important;
    font-weight: 700 !important;
}

/* Normal metinler */
p, label {
    color: #E5E7EB !important;
}

/* Detaylı açıklama kartı */
.detail-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-left: 4px solid #38BDF8;
    border-radius: 10px;
    padding: 22px;
    margin: 15px 0;
}

/* Kart başlığı */
.detail-card h3 {
    color: #7DD3FC !important;
    margin-top: 0;
}

/* Açıklama metni */
.detail-card p {
    color: #F1F5F9 !important;
    font-size: 16px;
    line-height: 1.8;
}

/* Bitki adı */
.plant-name {
    color: #86EFAC !important;
    font-weight: bold;
}

/* Arama kutusu */
.stTextInput input {
    background-color: #1E293B !important;
    color: #FFFFFF !important;
    border: 1px solid #475569 !important;
    border-radius: 8px;
}

/* Seçim kutusu */
[data-baseweb="select"] > div {
    background-color: #1E293B !important;
    color: #FFFFFF !important;
    border-color: #475569 !important;
}

/* Buton */
.stButton button {
    background-color: #0284C7 !important;
    color: #FFFFFF !important;
    border: none;
    border-radius: 8px;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #0369A1 !important;
}

/* Mobil görünüm */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem;
    }

    .detail-card {
        padding: 16px;
    }
}
