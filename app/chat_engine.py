"""
Smart AI Chat Engine – GPT-like conversational intelligence
Uses intent detection, fuzzy matching, interest-based course recommendation,
and full website knowledge to answer ANY question intelligently.
"""
import re
import logging
import random
from difflib import SequenceMatcher
from app.config import settings
from app.knowledge_base import COMPANY_INFO, SERVICES, COURSES, FAQS

logger = logging.getLogger(__name__)

# ============================================================
# INTENT DETECTION
# ============================================================
INTENTS = {
    "greeting": {
        "patterns": ["hi", "hello", "hey", "good morning", "good evening", "good afternoon", "namaste", "hii", "hiii", "sup", "yo", "howdy", "greetings", "what's up", "whats up"],
        "handler": "_handle_greeting"
    },
    "farewell": {
        "patterns": ["bye", "goodbye", "see you", "take care", "later", "good night", "night", "cya"],
        "handler": "_handle_farewell"
    },
    "thanks": {
        "patterns": ["thank", "thanks", "thankyou", "thank you", "appreciate", "grateful", "thx"],
        "handler": "_handle_thanks"
    },
    "course_list": {
        "patterns": ["what courses", "all courses", "courses available", "list courses", "show courses", "course list", "what do you teach", "what can i learn", "training programs", "programs offered", "courses offered", "available courses", "tell me courses"],
        "handler": "_handle_course_list"
    },
    "course_recommend": {
        "patterns": ["which course", "recommend", "suggest", "best course", "right course", "what should i learn", "confused", "help me choose", "career guidance", "what to study", "i want to learn", "i am interested", "interested in", "good for me", "suitable", "beginner", "fresher", "which one", "best for", "career in"],
        "handler": "_handle_course_recommend"
    },
    "fee_pricing": {
        "patterns": ["fee", "fees", "price", "pricing", "cost", "charge", "how much", "payment", "emi", "installment", "afford", "expensive", "cheap", "budget", "money", "pay", "scholarship"],
        "handler": "_handle_fees"
    },
    "discount_offer": {
        "patterns": ["discount", "offer", "deal", "promo", "promotion", "coupon", "free", "scholarship", "waiver", "concession", "off"],
        "handler": "_handle_offers"
    },
    "admission": {
        "patterns": ["admission", "admissions", "enroll", "enrollment", "register", "registration", "join", "apply", "application", "signup", "sign up", "start", "begin", "how to join", "how to enroll", "admission process", "procedure"],
        "handler": "_handle_admission"
    },
    "placement": {
        "patterns": ["placement", "job", "career", "intern", "internship", "employment", "hire", "hiring", "recruit", "salary", "package", "opportunity", "opportunities"],
        "handler": "_handle_placement"
    },
    "certificate": {
        "patterns": ["certificate", "certification", "credential", "certified", "diploma", "degree"],
        "handler": "_handle_certificate"
    },
    "schedule": {
        "patterns": ["schedule", "timing", "batch", "when", "duration", "how long", "time", "weekend", "evening", "morning", "flexible", "start date", "next batch"],
        "handler": "_handle_schedule"
    },
    "mode": {
        "patterns": ["online", "offline", "classroom", "virtual", "remote", "in person", "hybrid", "live class"],
        "handler": "_handle_mode"
    },
    "prerequisite": {
        "patterns": ["prerequisite", "requirement", "eligibility", "required", "need to know", "background", "prior", "experience needed", "qualification", "who can join", "eligible"],
        "handler": "_handle_prerequisite"
    },
    "about_company": {
        "patterns": ["about", "company", "who are you", "tell me about", "what is ushnik", "ushnik", "about ushnik", "your company", "organization", "founded", "history"],
        "handler": "_handle_about"
    },
    "services": {
        "patterns": ["service", "services", "what do you do", "what you offer", "offerings", "solutions", "provide", "capabilities"],
        "handler": "_handle_services"
    },
    "contact": {
        "patterns": ["contact", "phone", "call", "email", "address", "location", "where", "reach", "directions", "map", "visit", "office", "hours", "opening"],
        "handler": "_handle_contact"
    },
    "demo": {
        "patterns": ["demo", "trial", "try", "sample", "free class", "demo class", "test"],
        "handler": "_handle_demo"
    },
    "trainer": {
        "patterns": ["trainer", "teacher", "instructor", "faculty", "mentor", "who teaches", "experience of trainer"],
        "handler": "_handle_trainer"
    },
    "material": {
        "patterns": ["material", "study material", "notes", "resource", "recorded", "video", "recording", "pdf", "book"],
        "handler": "_handle_material"
    },
    "curriculum": {
        "patterns": ["curriculum", "syllabus", "topics", "what will i learn", "modules", "subjects", "content covered", "course content"],
        "handler": "_handle_curriculum"
    },
    "career_path": {
        "patterns": ["career path", "job role", "job roles", "what job", "career options", "scope", "future", "demand", "trending"],
        "handler": "_handle_career"
    }
}

# ============================================================
# DYNAMIC UTILITIES
# ============================================================

def _pick(choices):
    return random.choice(choices)

def _get_greeting():
    return _pick([
        "Hi! Welcome to **Ushnik Technologies**. 😊",
        "Hello! Great to have you here. 👋",
        "Hey there! How can I help you today? ✨",
        "Namaste! Welcome to our interactive AI portal. 🙏",
        "Hi! I'm your Ushnik AI assistant. Ready to help! 🚀"
    ])

def _get_transition():
    return _pick([
        "Also,", "Additionally,", "In addition to that,", "Furthermore,", "You'll be glad to know that",
        "It's also worth noting that", "Moreover,"
    ])

def _get_cta():
    return _pick([
        "Would you like to explore our batches? 🎓",
        "Shall I share the curriculum for any of these? 📋",
        "Want to know about our placement records? 💼",
        "Would you like to schedule a free demo class? 🖥️",
        "Feel free to share your contact details to get a personalized counselor call! 📞"
    ])

def _get_admission_reminder():
    return _pick([
        "🔥 **Flash Offer:** Admissions are **OPEN** with **50% OFF** on your first course!",
        "✨ **Limited Time:** Get **50% OFF** if you enroll this week! Admissions Open.",
        "🚀 **Admissions Open!** Grab a **50% discount** on your first training program.",
        "💡 **Quick Tip:** We are currently offering **50% OFF** for new students. Don't miss out!"
    ])

# ============================================================
# CORE ENGINE
# ============================================================

def get_chat_response(user_message: str, conversation_history: list = None) -> str:
    if conversation_history is None:
        conversation_history = []
    # 1. Try OpenAI first (True GPT behavior)
    ai_resp = _try_openai(user_message, conversation_history)
    if ai_resp:
        return ai_resp
    # 2. Smart Dynamic Fallback
    return _dynamic_response(user_message, conversation_history)

def _try_openai(msg: str, history: list):
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-your"):
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        ctx = _build_full_context()
        messages = [{"role": "system", "content": ctx}]
        for h in history[-10:]:
            messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
        messages.append({"role": "user", "content": msg})
        resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=700, temperature=0.7)
        return resp.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return None

def _build_full_context() -> str:
    c = COMPANY_INFO
    ctx = f"""You are the AI assistant for {c['name']}. Tagline: "{c['tagline']}".
{c['description']} {c['about']}
STATS: {c['stats']['happy_clients']} happy clients, {c['stats']['projects_completed']} projects completed.
INDUSTRIES: {', '.join(c['industries'])}
VALUES: {', '.join(c['values'])}
LOCATION: {c['address']} | Phone: {c['phone']} | Email: {c['email']}
SERVICES:
"""
    for name, svc in SERVICES.items():
        ctx += f"- {name}: {svc['summary']}\n"
        ctx += f"  Capabilities: {', '.join(svc.get('expertise', svc.get('offerings', svc.get('services_list', []))))}\n"
    ctx += "\nCOURSES:\n"
    for course in COURSES:
        ctx += f"- {course['Course']}: {course['Duration']}, Fee: {course['Fee']}, Discount: {course['Discount']}\n"
        ctx += f"  Curriculum: {', '.join(course.get('curriculum', []))}\n"
        ctx += f"  Careers: {', '.join(course.get('career', []))}\n"
    ctx += """
INSTRUCTIONS:
1. Be extremely conversational and personal. Act like a helpful friend.
2. Use information from the knowledge base to answer.
3. If user mentions a specific interest, pitch a course.
4. Always prioritize user enrollment.
5. Mention 50% OFF and Admissions are OPEN frequently but naturally.
"""
    return ctx

def _dynamic_response(msg: str, history: list) -> str:
    msg_lower = msg.lower().strip()
    msg_words = set(re.findall(r'\b\w+\b', msg_lower))
    
    intents = _detect_intents(msg_lower, msg_words)
    matched_course = _match_course(msg_lower)
    faq_match = _match_faq_dynamic(msg_lower, msg_words)
    knowledge_bits = _search_knowledge(msg_lower, msg_words)
    interests = _extract_interests(msg_lower, msg_words, history)
    
    response_parts = []

    # -- Part 1: Greeting (Inclusive) --
    if "greeting" in intents or any(x in msg_lower for x in ["hello", "hi", "hey"]):
        response_parts.append(_get_greeting())

    # -- Part 2: High-Priority Direct Channel --
    # If we have a specific FAQ or matched course, we prioritize that and limit other "unrelated" noise
    specific_answer_found = False
    
    if faq_match:
        response_parts.append(faq_match)
        specific_answer_found = True
    elif matched_course:
        response_parts.append(_handle_course_specific(matched_course, msg_lower))
        specific_answer_found = True
    
    # -- Part 3: Intent Handlers (Only if specific answer not found, or if multiple intents detected) --
    processed_intents = set()
    for intent in intents:
        if intent == "greeting": continue
        if specific_answer_found and intent in ["course_list", "about_company"]: continue
        if intent in processed_intents: continue
        
        handler_fn = globals().get(INTENTS[intent]["handler"])
        if handler_fn:
            if intent == "course_recommend":
                response_parts.append(handler_fn(msg_lower, interests))
                specific_answer_found = True
            else:
                intent_resp = handler_fn(msg_lower)
                # If we already have a course response, we don't want the full course list or general company info
                if specific_answer_found and len(intent_resp) > 200: 
                    continue 
                response_parts.append(intent_resp)
                specific_answer_found = True
            processed_intents.add(intent)

    # -- Part 4: Knowledge Expanders (Only as fallback or if message is short) --
    if knowledge_bits and (not specific_answer_found or len(msg_words) > 5):
        filtered_bits = []
        for bit in knowledge_bits:
            # Don't add a bit if it's already in the response
            if not any(bit[:20] in p for p in response_parts):
                filtered_bits.append(bit)
        
        if not response_parts and filtered_bits:
            response_parts.append("I have some relevant information for you:")
        
        response_parts.extend(filtered_bits[:1]) # Limit to 1 punchy bit

    # -- Part 5: Personalization / Recommendation --
    if interests and not specific_answer_found:
        top_course = interests[0][0]
        response_parts.append(f"{_get_transition()} if you're exploring this field, our **{top_course['Course']}** course is highly recommended! 🚀")

    # -- Fallback if nothing matched --
    if not response_parts:
        return _handle_general(msg_lower, msg_words)

    # Join and limit length to prevent "unrelated template dumping"
    final_resp = "\n\n".join(response_parts)
    
    # Filter out redundant knowledge bits if the main answer is already very detailed
    if len(final_resp) > 300:
        # If response is already long, remove small knowledge fragments that repeat course names
        cleaned_parts = []
        for p in response_parts:
            # If a part is just a short snippet about a course we already described, skip it
            is_redundant = False
            if matched_course and matched_course['Course'] in p and len(p) < 150:
                is_redundant = True
            if not is_redundant:
                cleaned_parts.append(p)
        final_resp = "\n\n".join(cleaned_parts)

    # Add contextually relevant closing
    if "50% OFF" not in final_resp:
        final_resp += f"\n\n{_get_admission_reminder()}"
    
    if "?" not in response_parts[-1]:
        final_resp += f"\n\n{_get_cta()}"

    return final_resp

def _search_knowledge(msg: str, words: set) -> list:
    bits = []
    for ind in COMPANY_INFO["industries"]:
        if ind.lower() in msg:
            bits.append(f"🏢 We serve the **{ind}** industry with tailored solutions.")
    for svc_name, svc_data in SERVICES.items():
        if svc_name.lower() in msg or any(k in msg for k in svc_data.get("keywords", [])):
            bits.append(f"⚙️ **{svc_name}:** {svc_data['summary']}")
    return bits

def _match_faq_dynamic(msg: str, words: set):
    res = _match_faq(msg)
    if res: return res.split("\n\n🔥")[0].replace("💡 ", "")
    return None

def _handle_general(msg: str, words: set) -> str:
    return _pick([
        "That's interesting! 🧐 Could you tell me more about your requirements?",
        "I'm here to help! Are you looking for a course or a business solution? 😊",
        f"I'm your Ushnik assistant. How about we explore our AI or Cyber courses? 🚀",
        "I'd love to assist. Tell me more about your goals! 💬"
    ])

def _detect_intents(msg: str, words: set) -> list:
    matches = []
    for intent_name, intent_data in INTENTS.items():
        score = 0
        for pattern in intent_data["patterns"]:
            if pattern in msg:
                score = max(score, len(pattern.split()) * 2 + 1)
            else:
                p_words = set(pattern.split())
                overlap = len(p_words & words)
                if overlap >= len(p_words) * 0.7:
                    score = max(score, overlap)
        
        if score >= 1:
            matches.append((intent_name, score))
    
    # Sort by score and return names
    matches.sort(key=lambda x: x[1], reverse=True)
    return [m[0] for m in matches]

def _match_course(msg: str):
    course_keywords = {
        "AI & Machine Learning": ["ai", "ml", "machine learning", "artificial intelligence", "deep learning"],
        "Cybersecurity": ["cybersecurity", "cyber security", "hacking", "ethical hacking", "pen testing"],
        "Full Stack Web Development": ["web development", "web dev", "full stack", "react", "node"],
        "Digital Marketing": ["digital marketing", "seo", "social media marketing"],
        "Data Science & Analytics": ["data science", "data analytics", "data analysis"],
        "SAP Modules": ["sap", "erp", "sap fico", "sap mm"]
    }
    for c_name, keywords in course_keywords.items():
        for kw in keywords:
            if kw in msg: return next((c for c in COURSES if c["Course"] == c_name), None)
    return None

def _match_faq(msg: str):
    best_score, best_answer = 0, None
    msg_words = set(re.findall(r'\b\w+\b', msg.lower()))
    for faq in FAQS:
        q_words = set(re.findall(r'\b\w+\b', faq["q"].lower()))
        overlap = len(msg_words & (q_words - {"what", "is", "the", "do", "you", "how"}))
        if overlap >= len(q_words) * 0.5 and overlap > best_score:
            best_score, best_answer = overlap, faq["a"]
    return f"💡 {best_answer}" if best_answer else None

def _extract_interests(msg: str, words: set, history: list) -> list:
    all_text = msg + " " + " ".join(h.get("content", "") for h in history[-3:])
    all_words = set(re.findall(r'\b\w+\b', all_text.lower()))
    interests = []
    for course in COURSES:
        match_count = sum(1 for tag in course.get("interest_tags", []) if tag in all_words)
        if match_count >= 1: interests.append((course, match_count))
    interests.sort(key=lambda x: x[1], reverse=True)
    return interests

# ============================================================
# DYNAMIC HANDLERS
# ============================================================

def _handle_greeting(msg: str) -> str:
    intro = _get_greeting()
    return f"{intro}\n\nI'm here to help you with expert guidance on our industry-ready career programs and powerful IT services. 🛠️\n\nTell me, are you looking to **upskill yourself** for a new career, or does your **business need** a technological edge? 🎯"

def _handle_farewell(msg: str) -> str:
    return "It was great chatting with you! 👋 Take care.\n\nBefore you go, keep in mind that our **50% OFF Admission** offer is for a limited time only. ⏳"

def _handle_thanks(msg: str) -> str:
    return _pick(["You're very welcome! 😊", "Glad I could help! ✨", "Anytime! 🚀"]) + "\n\nAnything else about our programs?"

def _handle_course_list(msg: str) -> str:
    lines = [f"🎓 **{c['Course']}** ({c['Duration']})" for c in COURSES]
    return "We've designed **6 industry-focused programs** to bridge the skill gap: 🚀\n\n" + "\n".join(lines) + "\n\nEvery course features **50% OFF** and 100% placement support! Which one interests you? 📚"

def _handle_course_specific(course: dict, msg: str) -> str:
    # Concise, high-impact course summary
    return (
        f"🌟 **{course['Course']}** | _{course['Duration']} Program_\n\n"
        f"💰 **Investment:** ~~{course['Fee']}~~ **{course.get('Discounted_Fee', course['Fee'])}** (Applied 50% OFF!)\n\n"
        f"🎯 **Highlight:** {course['Description'][:150]}...\n\n"
        f"💼 **Careers:** Become a {', '.join(course.get('career', [])[:2])}."
    )

def _handle_course_recommend(msg: str, interests: list) -> str:
    if interests: return _recommend_from_interests(interests)
    return "I'd love to recommend the perfect course! 🎯 Tell me, what excites you more: **Hacking**, **AI**, **Coding**, or **Business**? 🧠"

def _recommend_from_interests(interests: list) -> str:
    top = interests[0][0]
    return (
        f"🎯 **Top Pick for You:** {top['Course']}\n"
        f"Since you are exploring {', '.join(top['interest_tags'][:3])}, this program is the perfect fast-track to a career as a **{top['career'][0]}**. 🚀"
    )

def _handle_fees(msg: str) -> str:
    return "💰 **Pricing Update:** We're currently offering **50% OFF** on all first-course enrollments! 🎁\n\n• AI/ML: **₹20,000**\n• Cybersecurity: **₹24,500**\n• Web Dev: **₹27,000**\n\nEMI options available! Need a specific quote? 💳"

def _handle_offers(msg: str) -> str:
    return "🎁 **Current Offers:**\n\n🔥 **Flat 50% OFF** on first enrollment.\n🎓 **FREE Demo Class** included.\n🤝 **Placement Support** to help you get hired.\n\nReady to reserve your spot? 🚀"

def _handle_admission(msg: str) -> str:
    return "🎉 **Admissions are OPEN!**\n\n1️⃣ Share your details here.\n2️⃣ Get expert counseling call.\n3️⃣ Start your batch! 📋\n\nWe have Morning, Evening, and Weekend batches. Ready? 🚀"

def _handle_placement(msg: str) -> str:
    return "💼 **Career Support:** We provide Resume Building, Mock Interviews, and direct referrals to hit 50+ partners! 🌍\n\nWant to know average salaries for a course? 💰"

def _handle_certificate(msg: str) -> str:
    return "📜 **Certification:** We provide industry-recognized certificates with unique IDs and official seal. Valued globally by top firms! 🎓"

def _handle_schedule(msg: str) -> str:
    return "📅 **Schedule:** Morning (10-12), Afternoon (2-4), Evening (6-8), and Weekend batches. New batches start every 2 weeks! 🕒"

def _handle_mode(msg: str) -> str:
    return "🖥️ **Modes:**\n🟢 **Online:** Live interactive classes + recordings.\n🏢 **Offline:** Classroom training at Gachibowli, Hyderabad.\n\nWhich do you prefer? 🔍"

def _handle_about(msg: str) -> str:
    c = COMPANY_INFO
    return f"🏢 **About {c['name']}:** {c['description']} {c['about']}\n\nWe've completed {c['stats']['projects_completed']} projects across {len(c['industries'])} industries! 🌍"

def _handle_services(msg: str) -> str:
    svcs = ", ".join(SERVICES.keys())
    return f"🛠️ **Our Expertise:** We provide high-end solutions in **{svcs}**.\n\nDoes your business need an AI edge or a security shield? 🛡️"

def _handle_trainer(msg: str) -> str:
    return "👨‍🏫 **Our Mentors:** Industry veterans with 5-15 years experience from top tech giants. They teach you real-world practicals, not just theory! 🧠"

def _handle_material(msg: str) -> str:
    return "📖 **Study Resources:** You get full access to recorded sessions, code repositories, and project notes. Life-long revision support! 📚"

def _handle_career(msg: str) -> str:
    return "🚀 **Career Scope:** AI, Security, and Cloud are the highest paying jobs today. Our programs are built to get you there fast! 💰"

def _handle_curriculum(msg: str) -> str:
    return "📚 **Curriculum:** Each course has 10+ modules covering absolute basics to master-level. Want to see the list? 📋"

def _handle_contact(msg: str) -> str:
    c = COMPANY_INFO
    return f"📞 **Reach Us:**\n📍 {c['address']}\n📱 {c['phone']}\n📧 {c['email']}\n⏰ {c['hours']}\n\nShall I send these details to your phone? 🗺️"

def _handle_demo(msg: str) -> str:
    return "🖥️ **Free Demo Class:** Highly recommended! Experience our teaching style before you decide. Share your phone number to schedule! 🕒"
