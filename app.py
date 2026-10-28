import os
import sys
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
from knowledge_base import KNOWLEDGE_BASE, get_knowledge_base_context_for_prompt

# Load environment variables from .env if present
load_dotenv()

# Configure minimal, clean logging (never log API keys or chat content)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("daywell")

app = Flask(__name__)

# Avoid repeatedly calling Gemini after this server process receives a quota error.
GEMINI_QUOTA_BLOCKED = False

# Security configuration
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1MB max request size

SYSTEM_INSTRUCTION = f"""
You are the DayWell Wellness Guide, a gentle, welcoming, and strictly educational health and wellness assistant.

CRITICAL BOUNDARIES & HACKATHON RULES:
1. NO DIAGNOSIS: You must NEVER diagnose symptoms or identify illnesses from user descriptions. If a user describes physical or psychological symptoms (e.g., "My chest hurts", "I have a fever and rash", "Could this be diabetes?"), explicitly decline to diagnose. State: "I am an educational wellness guide and cannot diagnose conditions or interpret symptoms."
2. NO MEDICINES OR MEDICAL TREATMENTS: Never recommend medicines, pharmaceuticals, dosages, off-label treatments, or medical interventions.
3. NO PERSONALIZED CARE OR DIET PLANS: Never calculate or prescribe personalized macronutrient, calorie, or medical meal plans. Only share general, evidence-based public health principles (e.g., WHO guidelines on eating 400g of fruit and vegetables daily).
4. PERSONAL MEDICAL QUESTIONS & TRIAGE: For personal medical questions, gently explain that you provide general educational wellness information only, and recommend consulting a qualified healthcare professional.
5. URGENT OR LIFE-THREATENING CONCERNS: For red-flag or emergency symptoms (such as chest pain, severe shortness of breath, severe pain, sudden weakness/numbness, or thoughts of self-harm), urgently advise the user to contact local emergency services immediately (such as 112 in India/Europe, 911 in North America, 988/Tele-MANAS for mental health crises, or their nearest emergency hospital).
6. STRICT SOURCE GROUNDING: Ground your educational answers in the provided WHO and FSSAI knowledge base below.
7. CITATIONS & UNCERTAINTY: Always attribute facts to their source (WHO or FSSAI) and include clickable markdown links [Source Title](URL) using ONLY the authentic URLs provided below. If a user asks a question where reliable information is not in the knowledge base or is uncertain/unproven, explicitly state that reliable information is unavailable or uncertain rather than inventing facts or sources.

{get_knowledge_base_context_for_prompt()}

TONE & STYLE:
- Warm, compassionate, accessible, and easy to understand for everyday people.
- Use clear formatting with bullet points when explaining health concepts.
- Keep answers focused, informative, and reassuring without medical jargon.
"""

def get_gemini_api_key():
    """Retrieve GEMINI_API_KEY from environment or .env file, reloading dynamically."""
    if not app.config.get("TESTING"):
        load_dotenv(override=True)
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    return key if key else None


def find_offline_guidance(query: str):
    """
    Find relevant educational material from the trusted WHO/FSSAI knowledge base.
    Used for graceful source-based responses when Gemini API key is not yet configured.
    """
    q = (query or "").lower()

    # Safety: check for symptoms/diagnosis attempts even in offline reference mode
    symptom_triggers = ["diagnose", "diagnosis", "headache", "chest pain", "fever", "rash", "symptom", "medicine", "pill", "cure", "prescription", "antibiotic", "disease do i have"]
    if any(trigger in q for trigger in symptom_triggers):
        return {
            "type": "safety",
            "text": (
                "🛡️ **Hackathon Safety Rule: No Diagnosis or Medical Prescriptions**\n\n"
                "DayWell is strictly an educational wellness guide. We cannot diagnose conditions, evaluate personal symptoms, or recommend medications.\n\n"
                "• **For personal medical evaluation:** Please consult a qualified doctor or healthcare specialist.\n"
                "• **For medical emergencies:** Please contact emergency services immediately (112 in India/Europe, 911 in North America, or 988/Tele-MANAS at 14416 for mental health emergencies)."
            )
        }

    # Keyword mapping to trusted knowledge base items
    category_map = [
        (["move", "walk", "exercise", "physical activity", "sedentary", "step", "posture"], "physical_activity"),
        (["diet", "eat", "food", "nutrition", "sugar", "salt", "sodium", "fruit", "vegetable", "fssai", "eat right"], "nutrition_balanced_diet"),
        (["sleep", "insomnia", "bed", "rest", "circadian", "wake", "night"], "sleep_circadian"),
        (["stress", "anxiety", "grounding", "calm", "relax", "mindful", "tele-manas", "mental"], "stress_management"),
        (["wash", "hand", "hygiene", "soap", "clean", "safer food", "contamination"], "hygiene_food_safety"),
        (["ncd", "diabetes", "cardiovascular", "heart", "blood pressure", "hypertension", "chronic"], "ncds_prevention")
    ]

    matched_item = None
    for keywords, item_id in category_map:
        if any(kw in q for kw in keywords):
            for item in KNOWLEDGE_BASE:
                if item["id"] == item_id:
                    matched_item = item
                    break
            if matched_item:
                break

    if matched_item:
        lines = [
            f"ℹ️ **Source-Based Reference Mode** *(Gemini API Key is not configured)*\n",
            f"### {matched_item['title']} ({matched_item['organization']})",
            f"{matched_item['summary']}\n",
            "**Key Guidelines from Public Health Literature:**"
        ]
        for pt in matched_item["key_points"]:
            lines.append(f"- {pt}")
        lines.append("\n**Verified Sources:**")
        for src in matched_item["sources"]:
            lines.append(f"- [{src['title']}]({src['url']}) ({src['organization']})")
        lines.append("\n---\n💡 *Want interactive conversational AI? Add your free Google Gemini API key using the **'⚙️ Set API Key'** button above!*")
        return {"type": "match", "text": "\n".join(lines)}

    return {
        "type": "fallback",
        "text": (
            "ℹ️ **Source-Based Reference Mode** *(Gemini API Key is not configured)*\n\n"
            "DayWell is currently running in local reference mode. Here are the core topics available in our verified public health library:\n\n"
            "- **Balanced Nutrition & Diet:** WHO & FSSAI guidelines on fruits, vegetables, and limiting salt (<5g/day) and sugar (<10%).\n"
            "- **Physical Activity:** WHO recommendation of 150-300 mins of moderate aerobic movement weekly.\n"
            "- **Sleep Hygiene:** Consistent circadian schedules and evening digital wind-down.\n"
            "- **Stress Management:** Grounding exercises and the WHO 'Doing What Matters in Times of Stress' framework.\n"
            "- **Food Safety & Hygiene:** WHO 5 Keys to Safer Food and thorough 20-30s handwashing.\n\n"
            "Browse full details with official links in the **Trusted Sources** tab, or click **'⚙️ Set API Key'** to enable live Gemini AI chat!"
        )
    }


@app.route("/")
def index():
    """Serve the DayWell single page application."""
    return render_template("index.html")


@app.route("/api/config-status", methods=["GET"])
def config_status():
    """
    Check if the Gemini API key is configured.
    Never exposes the key or any part of it.
    """
    key = get_gemini_api_key()
    return jsonify({
        "configured": bool(key),
        "service": "Google Gemini API",
        "notice": "Chat messages are sent to Google Gemini API for real-time educational responses. No identifying or sensitive medical data is saved on our server."
    })


@app.route("/api/knowledge-base", methods=["GET"])
def get_knowledge_base():
    """Return the curated WHO and FSSAI knowledge base items."""
    return jsonify({
        "status": "success",
        "data": KNOWLEDGE_BASE
    })


@app.route("/api/save-key", methods=["POST"])
def save_key():
    """
    Securely saves or updates the GEMINI_API_KEY in the local .env file.
    Tests the key against Gemini API before saving to verify authorization.
    """
    data = request.get_json(silent=True) or {}
    api_key = (data.get("api_key") or "").strip()

    if not api_key:
        return jsonify({"success": False, "error": "API key cannot be empty."}), 400

    # Basic length check to avoid malformed inputs
    if len(api_key) < 20 or len(api_key) > 120:
        return jsonify({"success": False, "error": "Invalid API key format. A valid Gemini API key is typically ~39 characters."}), 400

    # Test key against Gemini API to verify validity
    test_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

    try:
        test_resp = requests.get(test_url, timeout=10)
        if test_resp.status_code in (400, 403):
            # Key was explicitly rejected by Google
            error_data = test_resp.json() if test_resp.headers.get("content-type", "").startswith("application/json") else {}
            err_msg = error_data.get("error", {}).get("message", "API key not recognized or not authorized by Google AI Studio.")
            return jsonify({
                "success": False,
                "error": f"Google API authentication failed: {err_msg}"
            }), 400
    except requests.exceptions.RequestException as e:
        logger.warning("Could not reach Google to verify key during save: %s", str(e))
        # If offline / network error, continue to save so user is not blocked offline

    # Write key to .env file
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    try:
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        key_written = False
        new_lines = []
        for line in lines:
            if line.strip().startswith("GEMINI_API_KEY="):
                new_lines.append(f"GEMINI_API_KEY={api_key}\n")
                key_written = True
            else:
                new_lines.append(line)

        if not key_written:
            new_lines.append(f"GEMINI_API_KEY={api_key}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        # Update running environment immediately
        os.environ["GEMINI_API_KEY"] = api_key
        load_dotenv(override=True)

        return jsonify({
            "success": True,
            "message": "Gemini API key successfully verified and saved to .env!"
        })
    except Exception as e:
        logger.error("Failed to write .env file: %s", str(e))
        return jsonify({"success": False, "error": f"Failed to write to .env file: {str(e)}"}), 500


@app.route("/api/remove-key", methods=["POST"])
def remove_key():
    """Removes the GEMINI_API_KEY from the local .env file and environment."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    try:
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = [l for l in lines if not l.strip().startswith("GEMINI_API_KEY=")]
            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
        load_dotenv(override=True)

        return jsonify({"success": True, "message": "Gemini API key removed."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    AI-powered Wellness Guide chat endpoint.
    Stateless: does not store chat history or user messages on the server.
    """
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    if len(user_message) > 1500:
        return jsonify({"error": "Message exceeds maximum allowed length of 1500 characters"}), 400

    global GEMINI_QUOTA_BLOCKED
    gemini_key = get_gemini_api_key()
    if not gemini_key:
        offline_result = find_offline_guidance(user_message)
        return jsonify({
            "status": "unconfigured",
            "message": "Gemini API key is not configured.",
            "instructions": "1. Click '⚙️ Configure API Key' in the header or chat tab\n2. Or add GEMINI_API_KEY to your .env file",
            "reply": offline_result["text"]
        }), 200

    # A quota error is project-level, so trying other models or sending every
    # subsequent chat message again will not help. Keep this server session on
    # the trusted local reference fallback instead.
    if GEMINI_QUOTA_BLOCKED:
        offline_result = find_offline_guidance(user_message)
        return jsonify({
            "status": "quota_exceeded",
            "reply": (
                "⏳ **Gemini quota reached.** DayWell has paused further AI requests "
                "for this server session. Check Google AI Studio for the reset time. "
                "Your habit tracker and Trusted Knowledge Base are still available.\n\n"
                "Here is related source-based guidance:\n\n" + offline_result["text"]
            )
        }), 200

    # Build conversation contents from client-supplied history (ephemeral, not stored on server)
    client_history = data.get("history", [])
    contents = []

    # Format previous turns (safely capped to last 6 turns to keep context tidy)
    if isinstance(client_history, list):
        recent_history = client_history[-6:]
        for turn in recent_history:
            if isinstance(turn, dict) and "role" in turn and "content" in turn:
                role = "user" if turn["role"] == "user" else "model"
                text_content = str(turn["content"]).strip()
                if text_content:
                    contents.append({
                        "role": role,
                        "parts": [{"text": text_content[:2000]}]
                    })

    # Append current message
    contents.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    # Prepare Gemini API request payload
    payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.8,
            "maxOutputTokens": 1024
        }
    }

    # Models to try in order — list based on what this API key actually supports.
    # Discovered via /v1beta/models: older gemini-2.x/1.5 names are removed for this account.
    models_to_try = [
        "gemini-3.5-flash",       # confirmed working ✓
        "gemini-3.7-flash",       # next stable
        "gemini-3.6-flash",       # fallback
        "gemini-3.1-flash-lite",  # lighter fallback
        "gemini-2.5-flash",       # API-reported as available
    ]
    last_error = None

    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
        try:
            resp = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=18
            )

            if resp.status_code == 200:
                result_json = resp.json()
                candidates = result_json.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    bot_text = "".join(part.get("text", "") for part in parts).strip()
                    if bot_text:
                        return jsonify({
                            "status": "success",
                            "model": model,
                            "reply": bot_text
                        })
                # If candidate was empty or blocked by safety filter
                return jsonify({
                    "status": "safety_notice",
                    "reply": "I am here to share general, educational wellness information from WHO and FSSAI. For personal medical concerns, symptoms, or prescriptions, please consult a qualified doctor or emergency service."
                })

            elif resp.status_code == 400:
                logger.warning("Gemini model %s returned 400: %s", model, resp.text[:200])
                last_error = "Invalid request format or model compatibility issue."
                continue
            elif resp.status_code == 404:
                logger.warning("Gemini model %s returned 404, falling back", model)
                last_error = f"Model {model} returned 404."
                continue
            elif resp.status_code == 503:
                logger.warning("Gemini model %s returned 503 (high load), falling back", model)
                last_error = f"Model {model} is experiencing temporary high demand."
                continue
            elif resp.status_code == 403:
                return jsonify({
                    "status": "error",
                    "reply": "⚠️ **Authentication Error**: The configured GEMINI_API_KEY was rejected by Google Gemini API (HTTP 403). Please verify that your API key is valid and has Generative Language API access enabled in Google AI Studio."
                }), 200
            elif resp.status_code == 429:
                GEMINI_QUOTA_BLOCKED = True
                offline_result = find_offline_guidance(user_message)
                return jsonify({
                    "status": "quota_exceeded",
                    "reply": (
                        "⏳ **Gemini quota reached.** DayWell has paused further AI "
                        "requests for this server session. Check Google AI Studio for "
                        "the reset time. Your habit tracker and Trusted Knowledge "
                        "Base are still available.\n\n"
                        "Here is related source-based guidance:\n\n" + offline_result["text"]
                    )
                }), 200
            else:
                last_error = f"Gemini API returned status code {resp.status_code}."
                logger.error("Gemini API error status %s: %s", resp.status_code, resp.text[:200])

        except requests.exceptions.Timeout:
            last_error = "The request to the AI service timed out. Please try again."
            logger.warning("Gemini API request timed out for model %s", model)
        except requests.exceptions.RequestException as e:
            last_error = "Unable to connect to the AI service. Please check your network connection."
            logger.error("Gemini API network exception: %s", str(e))

    # Graceful fallback: return offline guidance so user is never left without an answer
    fallback_result = find_offline_guidance(user_message)
    return jsonify({
        "status": "partial_offline",
        "reply": f"⚠️ *Note: The live Gemini AI service is temporarily experiencing high latency or connection limits ({last_error or 'Network issue'}). Here is verified educational guidance from WHO & FSSAI:*\n\n" + fallback_result["text"]
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting DayWell server on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
