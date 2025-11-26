# SpreadLove Web App

**SpreadLove** is a Streamlit-based web application that detects hate speeches and generates kind, contextual replies. It’s designed for educational and demo purposes only.

This project is inspired by **Halle Bailey**’s X account and uses a fictional “love & kindness” theme to demonstrate AI moderation of toxic content.

Visit the Web:
https://spreadlove.streamlit.app/

---

## ⚡ Features

* Detect hate speeches in text input (insults, racism, etc.)
* Generate contextual, friendly replies based on detected keywords
* Simple chat interface with avatars and “post-style” layout similar to X GUI
* Lightweight SVM model for toxicity detection

---

## 🚀 Demo / Web Deployment

The current deployment is a **preview only**, showcasing how the AI moderation works.
It is **not an official app** from Halle Bailey.

---

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/spreadlove.git
cd spreadlove
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the environment:

* **Windows:** `venv\Scripts\activate`
* **Mac/Linux:** `source venv/bin/activate`

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run locally:

```bash
streamlit run spreadlove.py
```

---

## 📂 Project Structure

```
assets/           # Avatars and CSV data
spreadlove.py     # Main Streamlit app
requirements.txt  # Python dependencies
README.md         # Project documentation
```

---

## ⚠️ Notes

* This app uses a **basic SVM model** and keyword-based replies.
* It is meant for **demonstration and learning purposes only**.
