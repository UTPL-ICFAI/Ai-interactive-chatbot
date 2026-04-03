// ============================================================
// USHNIK TECHNOLOGIES – PROFESSIONAL UI HANDLER
// ============================================================

const LEAD_PROMPT_AFTER = 3;
let messageCount = 0;
let leadSubmitted = false;
let conversationHistory = [];

const LOGO_URL = "https://ushnik.in/ushnik-logo.png";

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    addBotMsg("Namaste! Welcome to **Ushnik Technologies**. 🚀\n\nI'm your AI guide for today. I can tell you all about our industry-leading programs in **AI/ML**, **Cybersecurity**, and **Web Development**.\n\nHow can I help you take the next step in your career?");
});

function getMessagesArea() {
    return document.getElementById('messages-area');
}

function scrollToBottom() {
    const area = getMessagesArea();
    area.scrollTop = area.scrollHeight;
}

// Utility
function getTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function escHtml(text) {
    const d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
}

function formatMd(text) {
    let html = escHtml(text);
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
    html = html.replace(/\n/g, '<br>');
    return html;
}

// ============================================================
// MESSAGE RENDERING
// ============================================================

function addBotMsg(text) {
    const area = getMessagesArea();
    const el = document.createElement('div');
    el.className = 'message bot';
    el.innerHTML = `
        <div class="avatar-small">
            <img src="${LOGO_URL}" alt="U">
        </div>
        <div class="msg-container">
            <div class="bubble">${formatMd(text)}</div>
        </div>
    `;
    area.appendChild(el);
    scrollToBottom();
}

function addUserMsg(text) {
    const area = getMessagesArea();
    const el = document.createElement('div');
    el.className = 'message user';
    el.innerHTML = `
        <div class="msg-container">
            <div class="bubble">${escHtml(text)}</div>
        </div>
    `;
    area.appendChild(el);
    scrollToBottom();
}

function showTyping() {
    const area = getMessagesArea();
    const el = document.createElement('div');
    el.className = 'message bot';
    el.id = 'typing';
    el.innerHTML = `
        <div class="avatar-small">
            <img src="${LOGO_URL}" alt="U">
        </div>
        <div class="bubble" style="display: flex; gap: 4px; padding: 12px;">
            <div class="typing-dot" style="width: 6px; height: 6px; background: #94a3b8; border-radius: 50%; animation: bounce 1.4s infinite;"></div>
            <div class="typing-dot" style="width: 6px; height: 6px; background: #94a3b8; border-radius: 50%; animation: bounce 1.4s infinite 0.2s;"></div>
            <div class="typing-dot" style="width: 6px; height: 6px; background: #94a3b8; border-radius: 50%; animation: bounce 1.4s infinite 0.4s;"></div>
        </div>
    `;
    area.appendChild(el);
    scrollToBottom();
}

function hideTyping() {
    const t = document.getElementById('typing');
    if (t) t.remove();
}

// Show course cards
function showCourseCards(courses) {
    const area = getMessagesArea();
    const wrapper = document.createElement('div');
    wrapper.className = 'course-cards-container';

    courses.forEach(c => {
        const card = document.createElement('div');
        card.className = 'course-card-pro';
        card.innerHTML = `
            <div class="card-badge">${c.Discount || '50% OFF'}</div>
            <div class="card-title">${c.Course}</div>
            <div class="card-info">
                <span>📅 ${c.Duration}</span>
                <span>💰 ${c.Fee}</span>
            </div>
            <p style="font-size: 0.8rem; color: #64748b;">${c.Mode || 'Expert Training • Lab Access'}</p>
        `;
        card.onclick = () => sendQuick(`Tell me more about ${c.Course}`);
        wrapper.appendChild(card);
    });

    area.appendChild(wrapper);
    scrollToBottom();

    if (!leadSubmitted) {
        setTimeout(() => promptLeadForm(), 1500);
    }
}

// ============================================================
// SEND LOGIC
// ============================================================

async function sendMsg() {
    const input = document.getElementById('msg-input');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    addUserMsg(text);
    messageCount++;
    conversationHistory.push({ role: 'user', content: text });

    showTyping();

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, conversation_history: conversationHistory })
        });

        const data = await res.json();
        hideTyping();

        if (data.status === 'success') {
            if (data.courses && data.courses.length > 0) {
                addBotMsg(data.response);
                showCourseCards(data.courses);
            } else {
                addBotMsg(data.response);
            }
            conversationHistory.push({ role: 'assistant', content: data.response });
        } else {
            addBotMsg("Pardon me, I encountered a hiccup. Could you try that again? 🙏");
        }
    } catch (err) {
        hideTyping();
        addBotMsg("⚠️ System connectivity issue. Please check your network.");
    }

    if (messageCount >= LEAD_PROMPT_AFTER && !leadSubmitted) {
        setTimeout(() => promptLeadForm(), 1200);
    }
}

function sendQuick(text) {
    document.getElementById('msg-input').value = text;
    sendMsg();
}

// ============================================================
// LEAD HANDLING
// ============================================================

function promptLeadForm() {
    if (leadSubmitted) return;
    document.getElementById('inline-lead-form').style.display = 'flex';
}

function skipLeadForm() {
    document.getElementById('inline-lead-form').style.display = 'none';
    addBotMsg("Understood. I'm still here if you have any questions! What's on your mind?");
}

async function submitLead() {
    const name = document.getElementById('lead-name').value.trim();
    const email = document.getElementById('lead-email').value.trim();
    const phone = document.getElementById('lead-phone').value.trim();
    const course = document.getElementById('lead-course').value;

    if (!name || name.length < 2) { shakeField('lead-name'); return; }
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { shakeField('lead-email'); return; }
    if (!phone || phone.replace(/\D/g, '').length < 10) { shakeField('lead-phone'); return; }
    if (!course) { shakeField('lead-course'); return; }

    const btn = document.getElementById('submit-lead-btn');
    btn.textContent = 'Processing...';
    btn.disabled = true;

    try {
        const res = await fetch('/api/lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone, course, source: 'pro_chat' })
        });

        const data = await res.json();
        if (data.status === 'success') {
            leadSubmitted = true;
            document.getElementById('inline-lead-form').style.display = 'none';
            addBotMsg(`Thank you, **${name}**! Your interest in **${course}** has been noted.\n\nCheck your inbox for the discount details. Our team will reach out shortly to discuss your goals! 🎉`);

            if (data.popup) {
                setTimeout(() => showPopup(data.popup.title, data.popup.message, data.popup.discount), 1000);
            }
        }
    } catch (err) {
        btn.textContent = 'Claim 50% Discount';
        btn.disabled = false;
        alert("Submission failed. Please try again.");
    }
}

function shakeField(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.add('shake-error');
    el.focus();
    setTimeout(() => el.classList.remove('shake-error'), 500);
}

// Popup
function showPopup(title, message, discount) {
    document.getElementById('popup-title').textContent = title;
    document.getElementById('popup-message').textContent = message;
    document.getElementById('popup-discount').textContent = discount;
    document.getElementById('popup-overlay').style.display = 'flex';
}

function closePopup() {
    document.getElementById('popup-overlay').style.display = 'none';
}
