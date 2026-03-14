"""
GramCare AI — Healthcare Chatbot v2.0
Enhanced rule-based + keyword NLP chatbot for rural health guidance.
Supports multi-symptom understanding, structured responses, follow-ups,
and bilingual (English + Hindi/Punjabi) interaction.
Works offline with no external API dependencies.
"""
import re
import os
import json
import random
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


class HealthcareChatbot:
    def __init__(self):
        self.disease_info = {}
        self.conversation_context = {}
        self._load_knowledge()
        self._build_intents()
        self._build_symptom_combos()

    def _follow_up_for_intent(self, intent_tag):
        followups = {
            "fever": "Follow-up Question: Since when do you have fever, and what is the highest recorded temperature?",
            "cold_cough": "Follow-up Question: Is your cough dry or with mucus, and do you have any breathing difficulty?",
            "stomach": "Follow-up Question: Are you having loose motions, vomiting, or abdominal pain right now?",
            "headache": "Follow-up Question: Is the headache one-sided, with nausea, or worsened by light/noise?",
            "diabetes": "Follow-up Question: Do you have a recent fasting/post-meal sugar reading?",
            "blood_pressure": "Follow-up Question: Do you have a recent BP reading and any dizziness or chest discomfort?",
            "pregnancy": "Follow-up Question: Which month of pregnancy are you in, and are there any warning symptoms?",
            "symptom_check": "Follow-up Question: Please list your top 3 symptoms and how long you have had them.",
            "multi_symptom": "Follow-up Question: Please share duration of symptoms and whether fever or breathing issues are worsening.",
        }
        return followups.get(intent_tag, "Follow-up Question: Would you like me to guide you with next steps or help you connect with a doctor?")

    def _add_care_tone(self, text, intent_tag):
        prefix = "I understand your concern. "
        suffix = "\n\nPlease remember: this is general guidance and not a final diagnosis."
        followup = self._follow_up_for_intent(intent_tag)
        return f"{prefix}{text}\n\n{followup}{suffix}"

    def _load_knowledge(self):
        info_path = os.path.join(MODEL_DIR, "disease_info.json")
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                self.disease_info = json.load(f)

    def _build_symptom_combos(self):
        """Map common symptom combinations to structured advice."""
        self.symptom_combos = [
            {
                "symptoms": ["fever", "cough", "cold", "sore throat"],
                "min_match": 2,
                "condition": "Common Cold / Flu",
                "response": {
                    "possible_cause": "Common Cold or Influenza (Flu)",
                    "what_to_do": [
                        "Rest and stay hydrated — drink warm water, soups",
                        "Take Paracetamol (Dolo 650 / Crocin) for fever",
                        "Steam inhalation 2-3 times daily",
                        "Gargle with warm salt water for sore throat",
                        "Honey + tulsi + ginger tea helps naturally",
                    ],
                    "when_to_see_doctor": "If fever persists beyond 3 days, difficulty breathing, or symptoms worsen",
                },
            },
            {
                "symptoms": ["headache", "fever", "body ache", "fatigue"],
                "min_match": 2,
                "condition": "Viral Fever",
                "response": {
                    "possible_cause": "Viral Fever / Dengue-like illness",
                    "what_to_do": [
                        "Complete bed rest for 2-3 days",
                        "Drink plenty of fluids and ORS",
                        "Take Paracetamol — avoid Aspirin/Ibuprofen",
                        "Sponge with lukewarm water if temp > 102°F",
                        "Eat light, nutritious food",
                    ],
                    "when_to_see_doctor": "If high fever (>103°F), rash, severe body pain, or bleeding from gums/nose",
                },
            },
            {
                "symptoms": ["stomach", "diarrhea", "vomit", "nausea", "loose motion"],
                "min_match": 2,
                "condition": "Gastroenteritis",
                "response": {
                    "possible_cause": "Stomach Infection (Gastroenteritis)",
                    "what_to_do": [
                        "Drink ORS after every loose motion",
                        "Eat BRAT diet (Banana, Rice, Apple, Toast)",
                        "Avoid spicy, oily, and heavy food",
                        "Take Zinc supplements if available",
                        "Wash hands frequently with soap",
                    ],
                    "when_to_see_doctor": "If blood in stool, severe dehydration, or symptoms last >24 hours",
                },
            },
            {
                "symptoms": ["chest pain", "breathless", "sweating", "arm pain"],
                "min_match": 2,
                "condition": "Possible Cardiac Emergency",
                "response": {
                    "possible_cause": "Possible Heart Attack — SEEK IMMEDIATE HELP",
                    "what_to_do": [
                        "🚨 Call 108 (Ambulance) IMMEDIATELY",
                        "Sit or lie down in a comfortable position",
                        "Chew an Aspirin tablet if available (300mg)",
                        "Loosen tight clothing",
                        "Do NOT exert yourself",
                    ],
                    "when_to_see_doctor": "THIS IS AN EMERGENCY — go to hospital NOW",
                },
            },
        ]

    def _check_symptom_combos(self, message):
        """Check if message mentions multiple symptoms from known combos."""
        msg_lower = message.lower()
        for combo in self.symptom_combos:
            matches = sum(1 for s in combo["symptoms"] if s in msg_lower)
            if matches >= combo["min_match"]:
                r = combo["response"]
                lines = [f"Based on your symptoms, this could be **{r['possible_cause']}**\n"]
                lines.append("**What to do:**")
                for step in r["what_to_do"]:
                    lines.append(f"• {step}")
                lines.append(f"\n⚠️ **See a doctor if:** {r['when_to_see_doctor']}")
                return {
                    "reply": "\n".join(lines),
                    "action": "symptom_check",
                    "intent": "multi_symptom",
                    "condition": combo["condition"],
                }
        return None

    def _build_intents(self):
        """Define intent patterns and responses."""
        self.intents = [
            {
                "tag": "greeting",
                "patterns": [
                    r"\b(hi|hello|hey|namaste|sat sri akal|namaskar|good morning|good evening)\b",
                ],
                "responses": [
                    "Namaste! 🙏 I'm the GramCare AI health assistant. How can I help you today?\n\nYou can ask me about:\n• Symptoms & health concerns\n• Medicine information\n• Doctor appointments\n• Health tips",
                    "Hello! Welcome to GramCare AI. 😊 Tell me what's bothering you, or choose from the quick options below.",
                    "Hi there! I'm here to help with your health questions. What would you like to know?",
                ],
            },
            {
                "tag": "symptom_check",
                "patterns": [
                    r"\b(symptom|symptoms|feeling sick|not well|biimar|bimaar|tabiyat|taklif|check my)\b",
                ],
                "responses": [
                    "I can help check your symptoms! 🩺\n\n**How to use the Symptom Checker:**\n1. Go to the **Symptom Checker** page\n2. Search and select your symptoms\n3. Our AI will analyze and predict possible conditions\n\nOr simply tell me what symptoms you're experiencing right here!",
                ],
                "action": "symptom_check",
            },
            {
                "tag": "fever",
                "patterns": [
                    r"\b(fever|bukhar|temperature|high temp|badan garam)\b",
                ],
                "responses": [
                    "**Possible cause:** Viral infection, common cold, or flu\n\n**What to do:**\n• Rest and drink plenty of fluids (water, ORS, nimbu pani)\n• Take Paracetamol (Crocin/Dolo 650) if temp > 100°F\n• Apply cool damp cloth on forehead\n• Wear light clothing\n• Monitor temperature every 4 hours\n\n⚠️ **See a doctor if:** Fever persists beyond 3 days, temp > 103°F, or accompanied by rash/stiff neck",
                ],
            },
            {
                "tag": "cold_cough",
                "patterns": [
                    r"\b(cold|cough|khansi|nazla|zukaam|sardi|sneez|runny nose|gala kharab|sore throat)\b",
                ],
                "responses": [
                    "**Possible cause:** Common cold, viral upper respiratory infection\n\n**What to do:**\n• Drink warm water with honey and tulsi\n• Steam inhalation 2-3 times a day\n• Gargle with warm salt water for sore throat\n• Avoid cold food and drinks\n• Rest well and stay hydrated\n\n⚠️ **See a doctor if:** Symptoms last more than 7 days, difficulty breathing, or high fever develops",
                ],
            },
            {
                "tag": "stomach",
                "patterns": [
                    r"\b(stomach|pet|diarrh|dast|ulti|vomit|nausea|acidity|gas|constipat|kabz|indigestion)\b",
                ],
                "responses": [
                    "**Possible cause:** Indigestion, food poisoning, or gastritis\n\n**What to do:**\n• Stay hydrated — drink ORS (oral rehydration solution)\n• Eat light, bland food (khichdi, rice water, bananas)\n• Avoid spicy, oily, heavy food, tea/coffee on empty stomach\n• Take small, frequent meals\n• Jeera (cumin) water can help with gas/bloating\n\n⚠️ **See a doctor if:** Vomiting/diarrhea continues > 24 hours, blood in stool, or severe abdominal pain",
                ],
            },
            {
                "tag": "headache",
                "patterns": [
                    r"\b(headache|sir dard|head pain|migraine|sir mein dard)\b",
                ],
                "responses": [
                    "**Possible cause:** Tension headache, dehydration, or eye strain\n\n**What to do:**\n• Rest in a quiet, dark room\n• Drink water — dehydration is a common cause\n• Take Paracetamol if needed\n• Apply cold compress on forehead\n• Avoid screens and bright lights\n• Gentle neck/shoulder stretches may help\n\n⚠️ **See a doctor if:** Headaches are frequent, very severe, or with vision changes/vomiting",
                ],
            },
            {
                "tag": "emergency",
                "patterns": [
                    r"\b(emergency|urgent|heart attack|bleeding|unconscious|accident|seizure|stroke|saans|breathless|chest pain)\b",
                ],
                "responses": [
                    "🚨 **EMERGENCY — CALL FOR HELP IMMEDIATELY** 🚨\n\n📞 **Ambulance**: 108\n📞 **Emergency**: 112\n📞 **Women Helpline**: 1091\n🏥 **Nearest Hospital**: Nabha Civil Hospital\n\n**While waiting for help:**\n• Keep the person calm and still\n• Do not give food/water if unconscious\n• If bleeding, apply firm pressure with clean cloth\n• If not breathing, start CPR if trained\n• Note the time symptoms started\n\n⚡ Every minute matters — please seek help NOW!",
                ],
            },
            {
                "tag": "medicine_search",
                "patterns": [
                    r"\b(medicine|dawai|dawa|tablet|capsule|syrup|pharmacy|medical store|price|available)\b",
                ],
                "responses": [
                    "I can help you find medicines! 💊\n\nGo to **Medicine Search** to:\n• Search by medicine name or disease\n• Check prices at nearby pharmacies\n• Find generic (cheaper) alternatives\n• See composition and side effects\n\nYou can also ask me about any specific medicine!",
                ],
                "action": "medicine_search",
            },
            {
                "tag": "find_doctor",
                "patterns": [
                    r"\b(doctor|daktar|specialist|appointment|book|milna|consult)\b",
                ],
                "responses": [
                    "You can see a doctor right from home! 👨‍⚕️\n\nGramCare AI offers:\n• **Video Call** — best for detailed consultation\n• **Audio Call** — when internet is slow\n• **Chat** — works even on 2G networks\n\nGo to **See Doctor** on the dashboard to book your appointment.\nConsultation fee starts at just ₹50!",
                ],
                "action": "find_doctor",
            },
            {
                "tag": "health_tips",
                "patterns": [
                    r"\b(health tips|advice|prevent|healthy|diet|exercise|fit|wellness)\b",
                ],
                "responses": [
                    "**Daily Health Tips for a Better Life:** 🌟\n\n🥗 Eat seasonal vegetables and fruits daily\n💧 Drink 8-10 glasses of water\n🚶 Walk for at least 30 minutes every day\n😴 Sleep 7-8 hours at night\n🧂 Reduce salt and sugar intake\n🚭 Avoid tobacco and alcohol\n🧘 Practice deep breathing or yoga\n🧴 Wash hands before meals and after toilet\n☀️ Get 15 minutes of morning sunlight (Vitamin D)\n\nVisit our **Health Tips** page for detailed guides!",
                ],
            },
            {
                "tag": "diabetes",
                "patterns": [
                    r"\b(diabetes|sugar|madhumeh|sugar ki bimari|blood sugar|insulin)\b",
                ],
                "responses": [
                    "**Managing Diabetes (Sugar):** 🩸\n\n**What to do:**\n• Check blood sugar regularly (fasting + post-meal)\n• Eat whole grains (roti, brown rice) instead of maida\n• Avoid sweets, cold drinks, processed food, and white rice\n• Walk 30-45 minutes daily — morning walk is best\n• Take medicines as prescribed — NEVER skip\n• Keep feet clean and dry, check for wounds daily\n\n⚠️ **See a doctor if:** Sugar > 300 mg/dL, blurred vision, frequent infections, or non-healing wounds\n\n📅 Get check-ups every 3 months (HbA1c test)",
                ],
            },
            {
                "tag": "blood_pressure",
                "patterns": [
                    r"\b(bp|blood pressure|hypertension|uchcha raktchap)\b",
                ],
                "responses": [
                    "**Managing Blood Pressure:** ❤️\n\n**What to do:**\n• Reduce salt (namak) intake — less than 1 teaspoon/day\n• Eat potassium-rich foods (bananas, potatoes, spinach)\n• Walk or exercise 30 minutes daily\n• Maintain healthy weight\n• Avoid stress — practice deep breathing\n• Take BP medicines regularly\n• Limit tea/coffee to 2 cups/day\n\n**Normal BP:** 120/80 mmHg\n⚠️ **See a doctor if:** BP > 180/120, severe headache, chest pain, or vision problems",
                ],
            },
            {
                "tag": "pregnancy",
                "patterns": [
                    r"\b(pregnan|garbhvati|baby|delivery|antenatal|prenatal)\b",
                ],
                "responses": [
                    "**Pregnancy Care Tips:** 🤰\n\n• Visit doctor/ANM regularly (at least 4 checkups)\n• Take Iron + Folic Acid tablets daily\n• Eat nutritious food — dal, green vegetables, milk, fruits\n• Drink extra water (10+ glasses)\n• Get TT (Tetanus) vaccination\n• Rest well but stay active with light walks\n• Avoid heavy lifting and stress\n\n⚠️ **Go to hospital immediately if:** Heavy bleeding, severe pain, no baby movement, swelling in face/hands, or fever",
                ],
            },
            {
                "tag": "records",
                "patterns": [
                    r"\b(record|records|history|report|prescription|past visits)\b",
                ],
                "responses": [
                    "Your health records are saved securely in GramCare AI. 📋\n\nGo to **My Records** to view:\n• Past consultations & prescriptions\n• Lab reports & test results\n• Vitals history (BP, sugar, temp)\n• Vaccination records\n\nAll data is encrypted and accessible offline!",
                ],
            },
            {
                "tag": "help",
                "patterns": [
                    r"\b(help|how to use|kaise use|guide|tutorial|kya kar sakte)\b",
                ],
                "responses": [
                    "**How to use GramCare AI:** 📱\n\n1️⃣ **Symptom Checker** — Select symptoms, AI predicts conditions\n2️⃣ **AI Chatbot** — That's me! Ask anything about health\n3️⃣ **Medicine Search** — Check prices & find generics\n4️⃣ **See Doctor** — Video/Audio/Chat consultation\n5️⃣ **My Records** — View your health history\n6️⃣ **Health Tips** — Daily wellness advice\n7️⃣ **Emergency Guide** — First aid & helpline numbers\n\nEverything works on 2G/3G networks! 🌐",
                ],
            },
            {
                "tag": "thanks",
                "patterns": [
                    r"\b(thank|thanks|dhanyavaad|shukriya|meherbani)\b",
                ],
                "responses": [
                    "You're welcome! Stay healthy 🌟 Feel free to ask if you need anything else.",
                    "Glad I could help! 😊 Take care of your health. GramCare AI is always here for you.",
                ],
            },
            {
                "tag": "bye",
                "patterns": [
                    r"\b(bye|goodbye|alvida|chalo|ok bye)\b",
                ],
                "responses": [
                    "Take care! 🙏 Remember, GramCare AI is always here when you need health help. Stay healthy!",
                    "Goodbye! Stay healthy and come back anytime. 😊\n\n💡 Tip: Drink a glass of water right now!",
                ],
            },
        ]

    def _classify_intent(self, message):
        """Match message to the best intent using regex patterns."""
        message_lower = message.lower().strip()
        for intent in self.intents:
            for pattern in intent["patterns"]:
                if re.search(pattern, message_lower):
                    return intent
        return None

    def _get_disease_response(self, message):
        """Check if the message mentions a known disease and return structured info."""
        message_lower = message.lower().strip()
        for disease, info in self.disease_info.items():
            if disease.lower() in message_lower:
                desc = info.get("description", "")
                precs = info.get("precautions", [])
                response = f"**{disease}**\n\n{desc}"
                if precs:
                    response += "\n\n**Precautions:**\n"
                    response += "\n".join(f"• {p}" for p in precs)
                response += "\n\n⚠️ _This is general information. Please consult a doctor for proper diagnosis._"
                return response
        return None

    def get_response(self, message):
        """
        Process user message and return chatbot response.
        Returns: {"reply": str, "action": str|None, "intent": str}
        """
        # 1. Check multi-symptom combinations first
        combo_response = self._check_symptom_combos(message)
        if combo_response:
            combo_response["reply"] = self._add_care_tone(combo_response["reply"], "multi_symptom")
            combo_response["reply"] += "\n\n⚠️ This is AI-generated advice. Please consult a doctor for accurate diagnosis."
            self.conversation_context["last_intent"] = combo_response.get("intent", "multi_symptom")
            self.conversation_context["last_message_time"] = time.time()
            return combo_response

        # 2. Try intent classification
        intent = self._classify_intent(message)
        if intent:
            reply = random.choice(intent["responses"])
            reply = self._add_care_tone(reply, intent["tag"])
            self.conversation_context["last_intent"] = intent["tag"]
            self.conversation_context["last_message_time"] = time.time()
            return {
                "reply": reply,
                "action": intent.get("action"),
                "intent": intent["tag"],
            }

        # 3. Try disease info lookup
        disease_response = self._get_disease_response(message)
        if disease_response:
            disease_response = self._add_care_tone(disease_response, "disease_info")
            self.conversation_context["last_intent"] = "disease_info"
            self.conversation_context["last_message_time"] = time.time()
            return {
                "reply": disease_response,
                "action": "symptom_check",
                "intent": "disease_info",
            }

        # 4. Default fallback with helpful suggestions
        fallback_reply = (
            "I'm not sure I understand that. Here's what I can help with:\n\n"
            "- Tell me your symptoms (example: fever with cough for 2 days)\n"
            "- Ask about medicines (example: paracetamol uses)\n"
            "- Request health tips for a condition\n"
            "- Ask about diabetes, BP, pregnancy care\n"
            "- Type emergency for urgent help numbers\n\n"
            "Try the AI Symptom Checker for detailed analysis."
        )
        fallback_reply = self._add_care_tone(fallback_reply, "fallback")
        self.conversation_context["last_intent"] = "fallback"
        self.conversation_context["last_message_time"] = time.time()
        return {
            "reply": fallback_reply,
            "action": None,
            "intent": "fallback",
        }
