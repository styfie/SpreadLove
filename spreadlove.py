import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from pathlib import Path
import base64
import io
import re
import string

import streamlit as st
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from PIL import Image, ImageDraw

# -------------------------
# Configuration / Assets
# -------------------------
ASSETS = Path("assets")
HATER_AVATAR = ASSETS / "person.png"
USER_AVATAR = ASSETS / "halle.png"
BOT_AVATAR = ASSETS / "spreadlove.png"
CSV_FILE = ASSETS / "labeled_data.csv"

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="SpreadLove", page_icon="💙", layout="wide")

# -------------------------
# CSS
# -------------------------
st.markdown("""
<style>
:root{
  --bg:#ffffff;
  --muted:#6b6b6b;
  --accent:#1DA1F2;
}
.post-card{
  background: var(--bg);
  padding:18px;
  border-radius:10px;
  border:1px solid #eee;
  box-shadow: 0 2px 6px rgba(15,15,15,0.03);
  margin-bottom:12px;
}
.name { font-weight:700; font-size:15px; margin-bottom:2px; }
.handle { color:var(--muted); font-size:13px; }
.post-text { font-size:15px; margin-top:8px; white-space:pre-wrap; }
.timestamp { color:var(--muted); font-size:12px; margin-top:8px; }
.reply { display:flex; gap:10px; margin-bottom:12px; }
.bubble { background:#f7f9fb; padding:10px 12px; border-radius:12px; max-width:78%; }
.input-area { position: sticky; bottom:0; padding:12px; background:white; border-top:1px solid #eee; }
.system-note { color:#444; font-size:13px; margin:4px 0; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Avatar Helper
# -------------------------
def make_circle_data_uri(path: Path, size: int = 64):
    try:
        im = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        im.putalpha(mask)
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        encoded = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{encoded}"
    except:
        return ""

user_avatar_uri = make_circle_data_uri(USER_AVATAR)
bot_avatar_uri = make_circle_data_uri(BOT_AVATAR)
hater_avatar_uri = make_circle_data_uri(HATER_AVATAR)

# -------------------------
# NLP Clean Function
# -------------------------
nltk.download("stopwords", quiet=True)
STOP_WORDS = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return " ".join([w for w in text.split() if w not in STOP_WORDS])

# -------------------------
# Load SVM Model
# -------------------------
@st.cache_resource
def load_svm(csv_path):
    df = pd.read_csv(csv_path)
    df["clean"] = df["tweet"].astype(str).apply(clean_text)
    df["label"] = df["class"].replace({0: 0, 1: 0, 2: 1})

    vec = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vec.fit_transform(df["clean"])

    model = LinearSVC(max_iter=2000)
    model.fit(X, df["label"])
    return model, vec

svm_model, vectorizer = load_svm(CSV_FILE)

# -------------------------
# Generate Contextual Kind Reply
# -------------------------
def gen_reply(text):
    text_lower = text.lower()

    # Anger / aggression
    if any(word in text_lower for word in ["hate", "kill", "destroy", "attack"]):
        return "I understand you're upset 😔, let's stay calm and kind ❤️"

    # Insults / personal attacks
    elif any(word in text_lower for word in ["stupid", "dumb", "idiot", "loser", "fool"]):
        return "We can express disagreement without being mean 😊"

    # Appearance / body shaming
    elif any(word in text_lower for word in ["ugly", "fat", "skinny", "short"]):
        return "Everyone deserves kindness 💙, let's be respectful"

    # Racism / ethnic slurs
    elif any(word in text_lower for word in ["nigger", "chink", "kike", "racist", "white man", "black man", "asian"]):
        return "Racism and discrimination are hurtful. Let's respond with respect ✨"

    # Religion / belief attacks
    elif any(word in text_lower for word in ["muslim", "christian", "jew", "atheist", "islam", "christianity", "buddhist"]):
        return "Everyone has the right to their beliefs. Let's be kind 💛"

    # Region / nationality insults
    elif any(word in text_lower for word in ["american", "chinese", "indian", "filipino", "immigrant"]):
        return "Nationality or origin doesn't define someone's value 🌍 Let's stay positive"

    # Sexual harassment / inappropriate
    elif any(word in text_lower for word in ["slut", "whore", "bitch", "dick", "sex"]):
        return "Please be respectful, this is not appropriate 😇"

    # Generic fallback
    else:
        return "Let's keep things kind and respectful ❤️"

# -------------------------
# Session Messages
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"who": "SpreadLove", "text": "Hi! Paste a message and I'll check toxicity ❤️", "avatar": bot_avatar_uri, "type": "bot"},
    ]

# -------------------------
# UI Layout
# -------------------------
left, center, right = st.columns([1, 2, 1])
with center:

    # Fake post
    st.markdown("<div class='post-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 9])
    with c1:
        st.markdown(f"<img src='{user_avatar_uri}' style='width:64px;border-radius:999px;'>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='name'>Halle</div>", unsafe_allow_html=True)
        st.markdown("<div class='handle'>@HalleBailey</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='post-text'>love? or something like it’ — my debut album. ❤️</div>",
            unsafe_allow_html=True
        )
        st.markdown("<div class='timestamp'>1:12 AM · Oct 9 · 2.4M Views</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat Area
    st.markdown("<div class='post-card' style='max-height:480px;overflow:auto;'>", unsafe_allow_html=True)
    for m in st.session_state.messages:
        if m["type"] == "system":
            st.markdown(f"<div class='system-note'>{m['text']}</div>", unsafe_allow_html=True)
            continue

        c1, c2 = st.columns([0.7, 9.3])
        with c1:
            st.markdown(f"<img src='{m['avatar']}' style='width:48px;border-radius:999px;'>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='name-small'>{m['who']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bubble'>{m['text']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Input
    st.markdown("<div class='input-area'>", unsafe_allow_html=True)
    text = st.text_input("Message", placeholder="Paste a message...", label_visibility="collapsed")
    send = st.button("Send")
    st.markdown("</div>", unsafe_allow_html=True)

    # Logic
    if send and text.strip():
        # add user
        st.session_state.messages.append(
            {"who": "User", "text": text, "avatar": hater_avatar_uri, "type": "user"}
        )

        clean = clean_text(text)
        pred = svm_model.predict(vectorizer.transform([clean]))[0]

        if pred == 0:
            st.session_state.messages.append({"who": "System", "text": "Detected: Toxic ⚠️", "type": "system"})
            reply = gen_reply(text)
            st.session_state.messages.append({"who": "SpreadLove", "text": reply, "avatar": bot_avatar_uri, "type": "bot"})
        else:
            st.session_state.messages.append({"who": "System", "text": "Detected: Clean ✔️", "type": "system"})

        st.rerun()
