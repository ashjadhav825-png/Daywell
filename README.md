# 🌱 DayWell | Personal Habit Tracker & Grounded Wellness Guide

DayWell is a gentle, privacy-first personal habit tracker and educational wellness assistant built with Python (Flask) and vanilla modern JavaScript. It is designed to foster sustainable everyday well-being while adhering strictly to public health literature and ethical boundaries.

---

## 📋 Table of Contents
1. [Key Features](#-key-features)
   - [Personal Habit Tracker](#1-personal-habit-tracker)
   - [Wellness Guide (AI Chat)](#2-wellness-guide-ai-chat)
   - [Trusted Knowledge Base](#3-trusted-knowledge-base)
2. [Data Privacy & Data Flow](#-data-privacy--data-flow)
3. [Safety & Hackathon Compliance (No-Diagnosis Rule)](#-safety--hackathon-compliance-no-diagnosis-rule)
4. [Trusted Sources & Attribution](#-trusted-sources--attribution)
5. [Limitations](#-limitations)
6. [Local Setup & Running Guide](#-local-setup--running-guide)
   - [Prerequisites](#prerequisites)
   - [Quick Start](#quick-start)
   - [Configuring the Gemini API Key](#configuring-the-gemini-api-key)
7. [How to Try DayWell](#-how-to-try-daywell)
8. [Automated Verification & Testing](#-automated-verification--testing)

---

## ✨ Key Features

### 1. Personal Habit Tracker
- **Evidence-Inspired Preset Habits**: Choose from gentle everyday practices such as taking movement breaks, maintaining a consistent sleep routine, practicing mindful grounding breaths, and staying hydrated.
- **Custom Habit Creation**: Define your own routines with custom titles, categories, icons, and gentle cues.
- **7-Day Interactive Weekly Progress**: View your active habits on a 7-day calendar grid. Check off today or previous days in the past 7 days, complete with visual progress rings and completion percentages.
- **Edit & Remove Habits**: Edit habit titles and cues or remove habits at any time with a single click.
- **Daily Reflection & Well-being Check**: Log today's energy/mood (e.g., Calm, Energized, Needing Rest) and an optional personal reflection note.
- **100% Local & Account-Free**: All habit records, streaks, and reflections are stored directly in your browser's `localStorage`. No user accounts, passwords, or server-side databases are required.

### 2. Wellness Guide (AI Chat)
- **AI-Powered via Flask Backend**: Driven by the official Google Gemini API (`gemini-2.5-flash` with fallback to `gemini-1.5-flash`) through a secure Flask proxy.
- **Zero API Key Leakage**: The `GEMINI_API_KEY` is read strictly from backend environment variables and is never sent to the browser or logged.
- **Transparent Setup Handling**: If the API key is not configured, the interface displays a clear setup message and instructions instead of pretending or fabricating AI output.
- **Stateless Server**: Conversation history is ephemeral on the client side; no chat messages or health queries are stored on the server.
- **Prompt Suggestion Chips**: Quick one-click educational queries to explore nutrition, physical activity, sleep hygiene, stress management, and safe food handling.

### 3. Trusted Knowledge Base
- A dedicated in-app browser presenting verified public health guidelines and official links from the **World Health Organization (WHO)** and the **Food Safety and Standards Authority of India (FSSAI)**.

---

## 🔒 Data Privacy & Data Flow

| Data Element | Storage Location | Server Retention | Third-Party Flow |
| :--- | :--- | :--- | :--- |
| **Habits & Completions** | Browser `localStorage` | **None (0%)** | None. Kept 100% on the user's device. |
| **Daily Reflections & Mood** | Browser `localStorage` | **None (0%)** | None. Kept 100% on the user's device. |
| **Chat Messages** | Browser RAM (ephemeral) | **None (0%)** | Sent in real-time via Flask backend to Google Gemini API for educational answers. |
| **API Keys** | Local `.env` file | Read at runtime | Never exposed to frontend or printed in logs. |

### Notice Displayed to Users:
> **Notice**: Chat messages are processed in real-time by Google Gemini AI for educational health guidance. Please do not enter identifying details (names, phone numbers) or sensitive personal medical records. DayWell does not retain chat transcripts on the server.

---

## 🛡️ Safety & Hackathon Compliance (No-Diagnosis Rule)

DayWell strictly enforces safety guardrails both in prompt engineering and application logic:

1. **NO DIAGNOSIS**: The guide will never identify illnesses, diagnose conditions, or analyze personal symptoms. If a user describes symptoms (e.g. *"I have chest pain and shortness of breath"*), the guide explicitly declines to diagnose.
2. **NO MEDICINE OR PHARMACEUTICAL RECOMMENDATIONS**: The assistant does not prescribe drugs, recommend pharmaceutical dosages, or suggest medicinal treatments.
3. **NO INDIVIDUALIZED DIET OR MEDICAL CARE PLANS**: The guide does not prescribe restrictive calorie targets or medical nutrition therapy. It only provides general public health recommendations (e.g., eating at least 400g of fruit and vegetables daily).
4. **PERSONAL MEDICAL QUESTIONS**: The assistant directs users to consult a licensed physician or healthcare professional.
5. **EMERGENCY ESCALATION**: For urgent or red-flag concerns, DayWell prominently displays emergency numbers and directs users to local emergency services:
   - **India**: 112 (National Emergency), 108 (Ambulance), Tele-MANAS 14416 / 1800-891-4416 (Mental Health).
   - **North America**: 911 (Emergency), 988 (Suicide & Crisis Lifeline).
   - **Europe / Global**: 112.

---

## 📚 Trusted Sources & Attribution

All educational content is grounded in published literature from:

1. **World Health Organization (WHO)**:
   - [WHO Healthy Diet Fact Sheet](https://www.who.int/news-room/fact-sheets/detail/healthy-diet)
   - [WHO Physical Activity Guidelines](https://www.who.int/news-room/fact-sheets/detail/physical-activity)
   - [WHO Mental Health & Stress Guidelines ("Doing What Matters in Times of Stress")](https://www.who.int/publications/i/item/9789240003927)
   - [WHO Hand Hygiene Guidelines](https://www.who.int/campaigns/world-hand-hygiene-day)
   - [WHO Five Keys to Safer Food](https://www.who.int/publications/m/item/five-keys-to-safer-food-manual)
   - [WHO Noncommunicable Diseases Fact Sheet](https://www.who.int/news-room/fact-sheets/detail/noncommunicable-diseases)
   - [WHO Salt Reduction Fact Sheet](https://www.who.int/news-room/fact-sheets/detail/salt-reduction)

2. **Food Safety and Standards Authority of India (FSSAI)**:
   - [FSSAI Eat Right India Initiative](https://eatrightindia.gov.in/)
   - [FSSAI Food Fortification (+F Logo)](https://ffrc.fssai.gov.in/)
   - [FSSAI Safe Food Guidance](https://www.fssai.gov.in/)

The AI assistant cites these exact sources in markdown links. If a user asks about unverified fads, speculative supplements, or ungrounded topics, the assistant explicitly states that reliable evidence is unavailable or uncertain.

---

## ⚠️ Limitations

- **Not a Medical Device**: DayWell is an educational well-being tool, not an Electronic Health Record (EHR) or clinical diagnostic system.
- **General Guidance Only**: Recommendations are population-level public health guidelines and may not apply to individuals with specific clinical conditions or dietary restrictions.
- **Offline Mode**: The Habit Tracker works completely offline. The Wellness Guide uses Gemini when configured and available. If the Gemini project quota is exhausted, DayWell stops further Gemini calls for the current server session and shows related guidance from the local WHO/FSSAI knowledge base. The Trusted Knowledge Base remains available.

---

## 🚀 Local Setup & Running Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- (Optional) `uv` or standard Python `venv`

### Quick Start

1. **Clone or navigate to the repository directory**:
   ```bash
   cd d:\DayWell
   ```

2. **Set up a virtual environment**:
   ```bash
   # Using uv:
   uv venv .venv
   .\.venv\Scripts\activate

   # Or using standard python:
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application**:
   ```bash
   python app.py
   ```
   The application will start on `http://127.0.0.1:5000`.

---

### Configuring the Gemini API Key

You can configure your key in either of two easy ways:

#### Option A: In-Browser Setup (Easiest)
1. Open DayWell at `http://127.0.0.1:5000`.
2. Click the **"🔑 Set API Key"** button in the header or in the Wellness Guide tab.
3. Paste your key from [Google AI Studio (free)](https://aistudio.google.com/app/apikey).
4. Click **"Save & Activate"**. The app verifies the key with Google and saves it directly to your local `.env` file without requiring a server restart!

#### Option B: Local `.env` File
1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
2. Open `.env` in an editor and insert your key:
   ```env
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   ```
3. The app dynamically reloads `.env` on every check—no server restart required!

> **Note**: If `GEMINI_API_KEY` is omitted, DayWell operates in verified **Source-Based Reference Mode**. The Habit Tracker and the Trusted Sources library function fully, while the chat window provides authentic WHO/FSSAI literature guidance and setup instructions.

---

## 🧪 How to Try DayWell

1. **Open the App**:
   Navigate to `http://127.0.0.1:5000` in your web browser.

2. **Try the Habit Tracker**:
   - Check off today's habits by clicking the checkmark buttons.
   - Watch the **Today's Progress** ring and **7-Day Completion Rate** update in real time.
   - Click **"Suggested Habits"** and pick an evidence-inspired routine (e.g. *"Eat a Balanced, Colorful Meal"* or *"Morning Natural Light"*).
   - Click **"+ Create Habit"** to add a custom routine (e.g. *"Evening 5-Minute Stretch"*).
   - Click the ✏️ pencil icon to edit a habit or the 🗑️ trash icon to delete one.
   - Select today's mood (e.g. *😌 Calm* or *⚡ Energized*) and write a reflection in the Daily Reflection box. Refresh the page to verify that all data persists!

3. **Try the Wellness Guide (Chat)**:
   - Click the **"Wellness Guide"** tab.
   - Observe the privacy notice reminding you not to input sensitive health data.
   - If the API key is set, click a suggestion chip such as **"🏃 WHO Physical Activity"** or **"🥗 FSSAI Eat Right"**.
   - **Test the No-Diagnosis Rule**: Type *"I have a severe headache, what illness do I have and what medicine should I take?"* Notice how the guide politely declines to diagnose, advises against taking self-prescribed medication, recommends seeing a physician, and provides emergency contacts.
   - If the API key is not configured, observe the informative setup banner and instructions.

4. **Explore the Trusted Sources**:
   - Click the **"Trusted Sources"** tab.
   - Filter by category (*Nutrition*, *Movement*, *Sleep*, *Stress*, *Hygiene*, *Prevention*).
   - Click any source link to open the authentic WHO or FSSAI documentation.

---

## 🔬 Automated Verification & Testing

DayWell includes an automated test suite verifying all API endpoints, data validation, privacy bounds, and no-diagnosis safety rules.

Run the test suite with:
```bash
.\.venv\Scripts\python.exe -m unittest test_app.py
```

Expected output:
```text
Ran 10 tests in 0.056s

OK
```

