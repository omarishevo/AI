"""
Nova AI Chatbot — Powered by Groq (Free API)
Fast, free, no credit card required.
Get your free API key at: console.groq.com
"""

import streamlit as st
from groq import Groq
import json
Nova AI Chatbot — Powered by Groq (Free API)
Fast, free, no credit card required.
Get your free API key at: console.groq.com
"""

import streamlit as st
from groq import Groq
import json
from datetime import datetime

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nova · AI Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0A0A0F;
    color: #E8E8F0;
  }
  .stApp { background: #0A0A0F; }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
    background: #111118 !important;
    border-right: 1px solid #1E1E2E !important;
  }
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] div.stMarkdown {
    color: #C8C8D8 !important;
  }
  section[data-testid="stSidebar"] input {
    background: #1A1A28 !important;
    border: 1px solid #2E2E4E !important;
    color: #E8E8F0 !important;
    border-radius: 8px !important;
  }
  section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #1A1A28 !important;
    border: 1px solid #2E2E4E !important;
    color: #E8E8F0 !important;
  }
  button[data-testid="collapsedControl"],
  [data-testid="stSidebarCollapseButton"],
  [data-testid="stSidebarOpenButton"] {
    color: #A78BFA !important;
    background: #1A1A28 !important;
    border: 1px solid #2E2E4E !important;
    border-radius: 8px !important;
    opacity: 1 !important;
    visibility: visible !important;
  }
  [data-testid="collapsedControl"] svg,
  [data-testid="stSidebarCollapseButton"] svg,
  [data-testid="stSidebarOpenButton"] svg {
    fill: #A78BFA !important;
  }
  header[data-testid="stHeader"] { background: transparent !important; border-bottom: none !important; }
  footer { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* ── Chat wrapper ── */
  .chat-wrapper { max-width: 820px; margin: 0 auto; padding: 2rem 1.5rem 6rem; }

  /* ── Header ── */
  .chat-header {
    text-align: center; padding: 2.5rem 0 1.8rem;
    border-bottom: 1px solid #1E1E2E; margin-bottom: 2rem;
  }
  .chat-header .logo {
    font-family: 'Syne', sans-serif; font-size: 2.8rem; font-weight: 800;
    background: linear-gradient(135deg, #A78BFA, #60A5FA, #34D399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -0.03em; line-height: 1;
  }
  .chat-header .tagline {
    font-size: 0.85rem; color: #6B6B8A; font-weight: 300;
    letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.4rem;
  }
  .free-badge {
    display: inline-block; background: linear-gradient(135deg, #34D39922, #60A5FA22);
    border: 1px solid #34D39944; border-radius: 20px;
    padding: 4px 14px; font-size: 0.75rem; color: #34D399;
    margin-top: 0.6rem; letter-spacing: 0.05em;
  }

  /* ── Empty state ── */
  .empty-state { text-align: center; padding: 3rem 2rem; }
  .empty-state .spark { font-size: 3.2rem; margin-bottom: 1rem; }
  .empty-state h3 {
    font-family: 'Syne', sans-serif; font-size: 1.4rem;
    font-weight: 700; color: #C8C8E8; margin-bottom: 0.4rem;
  }
  .empty-state p { font-size: 0.88rem; color: #55556A; max-width: 380px; margin: 0 auto 1.5rem; }

  /* ── Suggestion chips ── */
  .chips-wrap { display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-top:1rem; }
  .chip {
    background: #14141F; border: 1px solid #2E2E4E; border-radius: 20px;
    padding: 6px 14px; font-size: 0.82rem; color: #9898B8; cursor: pointer;
  }

  /* ── Chat messages ── */
  .stChatMessage { background: transparent !important; }
  [data-testid="stChatMessageContent"] {
    background: #14141F !important;
    border: 1px solid #1E1E2E !important;
    border-radius: 4px 18px 18px 18px !important;
    color: #DDE0F0 !important;
    font-size: 0.95rem !important;
    line-height: 1.65 !important;
    padding: 0.85rem 1.2rem !important;
  }
  [data-testid="stChatMessage"][data-testid*="user"] [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    border: none !important;
    border-radius: 18px 4px 18px 18px !important;
    color: white !important;
  }

  /* ── Sidebar brand ── */
  .sidebar-brand {
    font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 800;
    background: linear-gradient(135deg, #A78BFA, #60A5FA);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .sidebar-sub {
    font-size: 0.7rem; color: #44445A !important;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1rem;
  }

  /* ── Persona cards ── */
  .persona-card {
    background: #1A1A28; border: 1px solid #2E2E4E; border-radius: 10px;
    padding: 0.6rem 0.85rem; margin-bottom: 0.4rem;
  }
  .persona-card.active { border-color: #A78BFA; background: #A78BFA11; }
  .persona-card .pname { font-weight: 600; font-size: 0.86rem; color: #C8C8E8 !important; }
  .persona-card .pdesc { font-size: 0.74rem; color: #55556A !important; margin-top: 1px; }

  /* ── Model badge ── */
  .model-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #1A1A28; border: 1px solid #2E2E4E; border-radius: 8px;
    padding: 4px 10px; font-size: 0.76rem; color: #9898B8 !important; margin: 2px;
  }
  .model-dot { width: 7px; height: 7px; border-radius: 50%; background: #34D399; flex-shrink:0; }

  /* ── Buttons ── */
  .stButton > button {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
    padding: 0.45rem 1rem !important; transition: opacity 0.2s !important;
  }
  .stButton > button:hover { opacity: 0.82 !important; }

  /* ── API key success indicator ── */
  .key-ok {
    display: flex; align-items: center; gap: 6px;
    background: #34D39911; border: 1px solid #34D39933;
    border-radius: 8px; padding: 6px 10px;
    font-size: 0.78rem; color: #34D399 !important;
    margin-top: 4px;
  }
  .key-missing {
    display: flex; align-items: center; gap: 6px;
    background: #F8717111; border: 1px solid #F8717133;
    border-radius: 8px; padding: 6px 10px;
    font-size: 0.78rem; color: #F87171 !important;
    margin-top: 4px;
  }

  /* ── Stat pills ── */
  .stat-row { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 4px; }
  .stat-pill {
    background: #1A1A28; border: 1px solid #2E2E4E; border-radius: 8px;
    padding: 3px 10px; font-size: 0.74rem; color: #9898B8 !important;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: #0A0A0F; }
  ::-webkit-scrollbar-thumb { background: #2E2E4E; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Groq Models ────────────────────────────────────────────────────────────────
GROQ_MODELS = {
    "⚡ Llama 3.3 70B (Best quality)":     "llama-3.3-70b-versatile",
    "🚀 Llama 3.1 8B (Fastest)":           "llama-3.1-8b-instant",
    "🧠 Mixtral 8x7B (Great reasoning)":   "mixtral-8x7b-32768",
    "💎 Gemma 2 9B (Balanced)":            "gemma2-9b-it",
}

# ── Personas ───────────────────────────────────────────────────────────────────
PERSONAS = {
    "✦ Nova (General)": {
        "icon": "✦", "desc": "Helpful all-rounder",
        "system": "You are Nova, a sharp, friendly, and knowledgeable AI assistant. Give clear, concise, accurate answers. Be warm but professional. Format code with markdown. Use bullet points for lists. When uncertain, say so."
    },
    "💻 Code Expert": {
        "icon": "💻", "desc": "Senior software engineer",
        "system": "You are an expert software engineer. Write clean, efficient, well-commented code. Explain technical concepts clearly. Always provide working examples. Prefer modern best practices."
    },
    "📊 Data Analyst": {
        "icon": "📊", "desc": "Data science & analytics",
        "system": "You are a seasoned data scientist. Excel at interpreting data, suggesting statistical approaches, writing Python/R code, and explaining insights to both technical and non-technical audiences."
    },
    "✍️ Writing Coach": {
        "icon": "✍️", "desc": "Creative & professional writing",
        "system": "You are an expert writing coach and editor. Help improve clarity, tone, structure, and style. Write, edit, rewrite, or give detailed feedback on any piece of writing."
    },
    "🧠 Research Assistant": {
        "icon": "🧠", "desc": "Deep research & analysis",
        "system": "You are a meticulous research assistant with broad academic knowledge. Synthesize information thoroughly, cite reasoning clearly, provide balanced perspectives, and flag areas of uncertainty."
    },
    "🩺 Health Advisor": {
        "icon": "🩺", "desc": "Health & wellness info",
        "system": "You are a knowledgeable health information assistant. Provide clear, evidence-based health information while always reminding users to consult qualified healthcare professionals for personal medical advice."
    },
}

SUGGESTIONS = [
    "Explain how neural networks work",
    "Write Python code to read a CSV file",
    "What are REST API best practices?",
    "Help me write a professional email",
    "What causes seasonal malaria outbreaks?",
    "Give me tips for better data visualizations",
]

# ── Session State ──────────────────────────────────────────────────────────────
defaults = {
    "messages":       [],
    "persona":        "✦ Nova (General)",
    "total_tokens":   0,
    "total_messages": 0,
    "pending_input":  "",
    "groq_api_key":   "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<div class='sidebar-brand'>✦ Nova</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-sub'>Free AI · Powered by Groq</div>", unsafe_allow_html=True)

    # ── API Key ──
    st.markdown("**🔑 Groq API Key**")
    st.markdown(
        "<div style='font-size:0.75rem;color:#55556A;margin-bottom:6px;'>"
        "Free key at <b style='color:#A78BFA;'>console.groq.com</b> — no credit card needed"
        "</div>", unsafe_allow_html=True
    )
    key_input = st.text_input(
        "groq_key", label_visibility="collapsed",
        value=st.session_state.groq_api_key,
        type="password", placeholder="gsk_..."
    )
    if key_input:
        st.session_state.groq_api_key = key_input

    if st.session_state.groq_api_key:
        st.markdown("<div class='key-ok'>✅ API key entered</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='key-missing'>⚠️ No API key — enter above</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Model selector ──
    st.markdown("**🤖 Model**")
    model_label = st.selectbox("model_sel", list(GROQ_MODELS.keys()),
                               label_visibility="collapsed", index=0)
    model_id = GROQ_MODELS[model_label]
    st.markdown(
        f"<div class='model-badge'><div class='model-dot'></div>{model_id}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ── Persona selector ──
    st.markdown("**🎭 Persona**")
    for pname, pdata in PERSONAS.items():
        is_active = st.session_state.persona == pname
        st.markdown(
            f"<div class='persona-card {'active' if is_active else ''}'>"
            f"<div class='pname'>{pname}</div>"
            f"<div class='pdesc'>{pdata['desc']}</div>"
            f"</div>", unsafe_allow_html=True
        )
        if st.button("Select", key=f"p_{pname}", use_container_width=True):
            st.session_state.persona = pname
            st.rerun()

    st.markdown("---")

    # ── Settings ──
    st.markdown("**⚙️ Settings**")
    max_tokens   = st.slider("Max Tokens",   256, 4096, 1024, 128)
    temperature  = st.slider("Temperature",  0.0, 1.0,  0.7,  0.05,
                             help="Higher = more creative · Lower = more precise")
    system_extra = st.text_area("Extra system instructions (optional)", height=68,
                                placeholder="e.g. Always respond in bullet points…")

    st.markdown("---")

    # ── Stats ──
    st.markdown("**📈 Session**")
    st.markdown(
        f"<div class='stat-row'>"
        f"<div class='stat-pill'>💬 {st.session_state.total_messages} msgs</div>"
        f"<div class='stat-pill'>🔤 {st.session_state.total_tokens:,} tokens</div>"
        f"</div>", unsafe_allow_html=True
    )

    st.markdown("")

    # ── Export ──
    if st.session_state.messages:
        export = json.dumps([
            {"role": m["role"], "content": m["content"], "time": m.get("time","")}
            for m in st.session_state.messages
        ], indent=2)
        st.download_button(
            "⬇️ Export Chat", data=export,
            file_name=f"nova_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json", use_container_width=True
        )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages       = []
        st.session_state.total_tokens   = 0
        st.session_state.total_messages = 0
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.7rem;color:#2A2A3A;text-align:center;'>"
        "Nova v2.1 · Groq Edition · Streamlit"
        "</div>", unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='chat-header'>
  <div class='logo'>Nova</div>
  <div class='tagline'>Intelligent Assistant · Free · Fast · No Credit Card</div>
  <div class='free-badge'>⚡ Powered by Groq — 100% Free API</div>
</div>
""", unsafe_allow_html=True)

# ── API key gate ──
if not st.session_state.groq_api_key:
    st.markdown("""
    <div class='empty-state'>
      <div class='spark'>🔑</div>
      <h3>Free API Key Required</h3>
      <p>Get your <b>free</b> Groq API key in 30 seconds — no credit card needed.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("""
        **How to get your free key:**

        1. Go to 👉 **[console.groq.com](https://console.groq.com)**
        2. Sign up with Google or email (free)
        3. Click **API Keys → Create API Key**
        4. Copy the key (starts with `gsk_...`)
        5. Paste it in the **sidebar** ← on the left

        ✅ Takes less than 1 minute · No billing required
        """)
    st.stop()

# ── Chat history ──
if not st.session_state.messages:
    st.markdown(f"""
    <div class='empty-state'>
      <div class='spark'>✦</div>
      <h3>What can I help you with?</h3>
      <p>I'm running as <b>{st.session_state.persona}</b> — ask me anything below.</p>
    </div>
    <div class='chips-wrap'>
      {"".join(f"<div class='chip'>{s}</div>" for s in SUGGESTIONS)}
    </div>
    """, unsafe_allow_html=True)

    # Functional suggestion buttons
    cols = st.columns(3)
    for i, s in enumerate(SUGGESTIONS):
        if cols[i % 3].button(s, key=f"sug_{i}", use_container_width=True):
            st.session_state.pending_input = s
            st.rerun()
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"],
                             avatar="🧑" if msg["role"]=="user"
                             else PERSONAS[st.session_state.persona]["icon"]):
            st.markdown(msg["content"])

st.markdown("</div>", unsafe_allow_html=True)

# ── Chat input ──
prompt = st.chat_input(
    placeholder=f"Message {st.session_state.persona}...",
    key="main_chat_input"
)

# Pick up suggestion click
if st.session_state.pending_input and not prompt:
    prompt = st.session_state.pending_input
    st.session_state.pending_input = ""

# ═══════════════════════════════════════════════════════════════════════════════
# HANDLE MESSAGE
# ═══════════════════════════════════════════════════════════════════════════════
if prompt:
    ts = datetime.now().strftime("%H:%M")

    # Save & show user message
    st.session_state.messages.append({"role": "user", "content": prompt, "time": ts})
    st.session_state.total_messages += 1
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Build system prompt
    base_system = PERSONAS[st.session_state.persona]["system"]
    system_prompt = base_system + (f"\n\n{system_extra}" if system_extra.strip() else "")

    # Build message history for API
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    # Stream response
    persona_icon = PERSONAS[st.session_state.persona]["icon"]
    with st.chat_message("assistant", avatar=persona_icon):
        response_placeholder = st.empty()
        full_response = ""

        try:
            client = Groq(api_key=st.session_state.groq_api_key)

            stream = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "system", "content": system_prompt}] + api_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
            )

            # Stream tokens live
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    response_placeholder.markdown(full_response + "▌")

            # Final render without cursor
            response_placeholder.markdown(full_response)

            # Token usage (Groq returns this on last chunk)
            try:
                usage = chunk.x_groq.usage if hasattr(chunk, "x_groq") else None
                if usage:
                    st.session_state.total_tokens += (
                        usage.prompt_tokens + usage.completion_tokens
                    )
            except Exception:
                pass

        except Exception as e:
            err = str(e)
            if "invalid_api_key" in err.lower() or "401" in err:
                full_response = "❌ Invalid API key. Please check your Groq API key in the sidebar."
            elif "rate_limit" in err.lower() or "429" in err:
                full_response = "⚠️ Rate limit reached. Wait a few seconds and try again."
            elif "model_not_found" in err.lower():
                full_response = f"⚠️ Model `{model_id}` not available. Try a different model from the sidebar."
            else:
                full_response = f"❌ Error: {err}"
            response_placeholder.error(full_response)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "time": datetime.now().strftime("%H:%M")
    })
    st.session_state.total_messages += 1
from datetime import datetime

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nova · AI Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

  /* ── Global ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0A0A0F;
    color: #E8E8F0;
  }
  .stApp { background: #0A0A0F; }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
    background: #111118 !important;
    border-right: 1px solid #1E1E2E !important;
  }
  /* Sidebar text — only target text nodes, NOT the toggle button */
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] span:not([data-testid]),
  section[data-testid="stSidebar"] div.stMarkdown,
  section[data-testid="stSidebar"] .stSelectbox label,
  section[data-testid="stSidebar"] .stSlider label,
  section[data-testid="stSidebar"] .stTextInput label {
    color: #C8C8D8 !important;
  }
  /* Sidebar inputs */
  section[data-testid="stSidebar"] input {
    background: #1A1A28 !important;
    border: 1px solid #2E2E4E !important;
    color: #E8E8F0 !important;
    border-radius: 8px !important;
  }
  /* Sidebar selectbox */
  section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #1A1A28 !important;
    border: 1px solid #2E2E4E !important;
    color: #E8E8F0 !important;
  }
  /* Sidebar collapse/expand button — keep it visible */
  button[data-testid="collapsedControl"],
  button[kind="header"],
  [data-testid="stSidebarCollapseButton"],
  [data-testid="stSidebarOpenButton"] {
    color: #A78BFA !important;
    background: #1A1A28 !important;
    border: 1px solid #2E2E4E !important;
    border-radius: 8px !important;
    opacity: 1 !important;
    visibility: visible !important;
  }
  /* Make sure the sidebar toggle arrow is always visible */
  [data-testid="collapsedControl"] svg,
  [data-testid="stSidebarCollapseButton"] svg,
  [data-testid="stSidebarOpenButton"] svg {
    fill: #A78BFA !important;
    color: #A78BFA !important;
  }

  /* ── Keep Streamlit toolbar visible for sidebar toggle ── */
  header[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
  }
  /* Only hide footer */
  footer { visibility: hidden; }

  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* ── Chat container ── */
  .chat-wrapper {
    max-width: 820px;
    margin: 0 auto;
    padding: 2rem 1.5rem 10rem;
  }

  /* ── Header ── */
  .chat-header {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid #1E1E2E;
    margin-bottom: 2rem;
  }
  .chat-header .logo {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #A78BFA, #60A5FA, #34D399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.4rem;
  }
  .chat-header .tagline {
    font-size: 0.9rem;
    color: #6B6B8A;
    font-weight: 300;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* ── Messages ── */
  .msg-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 1.6rem;
    animation: fadeSlide 0.25s ease-out;
  }
  @keyframes fadeSlide {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .msg-row.user   { flex-direction: row-reverse; }
  .msg-row.user .bubble {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    color: #fff;
    border-radius: 18px 4px 18px 18px;
    margin-left: auto;
  }
  .msg-row.assistant .bubble {
    background: #14141F;
    border: 1px solid #1E1E2E;
    color: #DDE0F0;
    border-radius: 4px 18px 18px 18px;
  }
  .bubble {
    padding: 0.85rem 1.2rem;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.65;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
    margin-top: 2px;
  }
  .avatar.user-av {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    color: white;
    font-weight: 700;
    font-family: 'Syne', sans-serif;
  }
  .avatar.bot-av {
    background: linear-gradient(135deg, #A78BFA22, #60A5FA22);
    border: 1px solid #2E2E4E;
    color: #A78BFA;
  }
  .msg-time {
    font-size: 0.7rem;
    color: #44445A;
    margin-top: 4px;
    text-align: right;
  }
  .msg-row.user .msg-time { text-align: right; }

  /* ── Typing indicator ── */
  .typing-indicator {
    display: flex; align-items: center; gap: 5px;
    padding: 0.7rem 1rem;
    background: #14141F;
    border: 1px solid #1E1E2E;
    border-radius: 4px 18px 18px 18px;
    width: fit-content;
  }
  .typing-dot {
    width: 7px; height: 7px;
    background: #6B6B9A;
    border-radius: 50%;
    animation: typingBounce 1.2s infinite;
  }
  .typing-dot:nth-child(2) { animation-delay: 0.2s; }
  .typing-dot:nth-child(3) { animation-delay: 0.4s; }
  @keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-6px); opacity: 1; }
  }

  /* ── Empty state ── */
  .empty-state {
    text-align: center;
    padding: 4rem 2rem;
  }
  .empty-state .spark {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 20px #A78BFA44);
  }
  .empty-state h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #C8C8E8;
    margin-bottom: 0.5rem;
  }
  .empty-state p {
    font-size: 0.9rem;
    color: #55556A;
    max-width: 400px;
    margin: 0 auto 2rem;
  }

  /* ── Suggestion chips ── */
  .chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 1rem;
  }
  .chip {
    background: #14141F;
    border: 1px solid #2E2E4E;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.82rem;
    color: #9898B8;
    cursor: pointer;
    transition: all 0.2s;
  }
  .chip:hover {
    border-color: #A78BFA;
    color: #A78BFA;
    background: #A78BFA11;
  }

  /* ── Input area ── */
  .input-dock {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, #0A0A0F 70%, transparent);
    padding: 1rem 1.5rem 1.5rem;
    z-index: 100;
  }
  .input-inner {
    max-width: 820px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 10px;
    background: #14141F;
    border: 1px solid #2E2E4E;
    border-radius: 16px;
    padding: 0.6rem 0.6rem 0.6rem 1.2rem;
    box-shadow: 0 0 40px #A78BFA11;
  }
  .stTextInput > div > div > input {
    background: transparent !important;
    border: none !important;
    color: #E8E8F0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.4rem 0 !important;
    box-shadow: none !important;
  }
  .stTextInput > div > div > input::placeholder { color: #44445A !important; }
  .stTextInput > div { border: none !important; background: transparent !important; }

  /* ── Send button ── */
  .stButton > button {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.4rem !important;
    font-size: 0.9rem !important;
    transition: opacity 0.2s !important;
    white-space: nowrap;
  }
  .stButton > button:hover { opacity: 0.85 !important; }

  /* ── Sidebar elements ── */
  .sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #A78BFA, #60A5FA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
  }
  .sidebar-sub {
    font-size: 0.72rem;
    color: #44445A !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1.2rem;
  }
  .persona-card {
    background: #1A1A28;
    border: 1px solid #2E2E4E;
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: border-color 0.2s;
  }
  .persona-card.active { border-color: #A78BFA; background: #A78BFA11; }
  .persona-card .pname {
    font-weight: 600;
    font-size: 0.88rem;
    color: #C8C8E8 !important;
  }
  .persona-card .pdesc {
    font-size: 0.76rem;
    color: #55556A !important;
    margin-top: 2px;
  }
  .stat-pill {
    display: inline-flex; align-items: center; gap: 5px;
    background: #1A1A28; border: 1px solid #2E2E4E;
    border-radius: 8px; padding: 4px 10px;
    font-size: 0.76rem; color: #9898B8 !important;
    margin: 2px;
  }
  .stSelectbox > div, .stSlider, .stTextArea { color: #C8C8D8 !important; }

  /* ── Code blocks in chat ── */
  .bubble code {
    background: #0D0D1A;
    border: 1px solid #2E2E4E;
    border-radius: 4px;
    padding: 1px 5px;
    font-size: 0.85em;
    font-family: 'Courier New', monospace;
    color: #A78BFA;
  }
  .bubble pre {
    background: #0D0D1A;
    border: 1px solid #2E2E4E;
    border-radius: 8px;
    padding: 1rem;
    overflow-x: auto;
    margin: 0.5rem 0;
  }
  .bubble pre code {
    background: transparent;
    border: none;
    padding: 0;
    color: #A5D6A7;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: #0A0A0F; }
  ::-webkit-scrollbar-thumb { background: #2E2E4E; border-radius: 10px; }

  /* ── Divider ── */
  hr { border-color: #1E1E2E !important; }
</style>
""", unsafe_allow_html=True)


# ── Personas ───────────────────────────────────────────────────────────────────
PERSONAS = {
    "✦ Nova (General)": {
        "icon": "✦",
        "desc": "Helpful all-rounder",
        "system": (
            "You are Nova, a sharp, friendly, and knowledgeable AI assistant. "
            "You give clear, concise, and accurate answers. You are warm but professional. "
            "Format code blocks with proper markdown. Use bullet points for lists. "
            "When uncertain, say so clearly."
        )
    },
    "💻 Code Expert": {
        "icon": "💻",
        "desc": "Senior software engineer",
        "system": (
            "You are an expert software engineer with deep knowledge across all programming languages, "
            "frameworks, and best practices. You write clean, efficient, well-commented code. "
            "You explain technical concepts clearly. Always provide working code examples. "
            "Prefer best practices and modern approaches."
        )
    },
    "📊 Data Analyst": {
        "icon": "📊",
        "desc": "Data science & analytics",
        "system": (
            "You are a seasoned data scientist and analyst. You excel at interpreting data, "
            "suggesting statistical approaches, writing Python/R code for analysis, "
            "and explaining insights clearly to both technical and non-technical audiences. "
            "You recommend appropriate visualizations, models, and tools."
        )
    },
    "✍️ Writing Coach": {
        "icon": "✍️",
        "desc": "Creative & professional writing",
        "system": (
            "You are an expert writing coach and editor with experience in creative writing, "
            "technical documentation, and professional communication. "
            "You help improve clarity, tone, structure, and style. "
            "You can write, edit, rewrite, or give detailed feedback on any piece of writing."
        )
    },
    "🧠 Research Assistant": {
        "icon": "🧠",
        "desc": "Deep research & analysis",
        "system": (
            "You are a meticulous research assistant with broad academic knowledge. "
            "You synthesize information thoroughly, cite reasoning clearly, "
            "provide balanced perspectives, and flag areas of uncertainty. "
            "You structure your responses with clear headings and logical flow."
        )
    },
    "🩺 Health Advisor": {
        "icon": "🩺",
        "desc": "Health & wellness info",
        "system": (
            "You are a knowledgeable health information assistant. You provide clear, "
            "evidence-based health information while always reminding users to consult "
            "qualified healthcare professionals for personal medical advice. "
            "You are empathetic, clear, and thorough."
        )
    },
}

SUGGESTIONS = [
    "Explain how neural networks work",
    "Write a Python script to analyze CSV data",
    "What are the best practices for REST APIs?",
    "Help me write a professional email",
    "What causes malaria outbreaks?",
    "Summarize the latest trends in AI",
]

# ── Session State ──────────────────────────────────────────────────────────────
if "messages"        not in st.session_state: st.session_state.messages        = []
if "persona"         not in st.session_state: st.session_state.persona         = "✦ Nova (General)"
if "total_tokens"    not in st.session_state: st.session_state.total_tokens    = 0
if "total_messages"  not in st.session_state: st.session_state.total_messages  = 0
if "pending_input"   not in st.session_state: st.session_state.pending_input   = ""
if "api_key"         not in st.session_state: st.session_state.api_key         = ""


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-brand'>✦ Nova</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-sub'>AI Assistant · Powered by Claude</div>", unsafe_allow_html=True)

    # API Key input
    api_key_input = st.text_input(
        "🔑 Anthropic API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-api...",
        help="Get your API key from console.anthropic.com"
    )
    if api_key_input:
        st.session_state.api_key = api_key_input

    st.markdown("---")

    # Persona selector
    st.markdown("**🎭 Persona**")
    for persona_name, persona_data in PERSONAS.items():
        is_active = st.session_state.persona == persona_name
        card_class = "persona-card active" if is_active else "persona-card"
        st.markdown(f"""
        <div class='{card_class}'>
          <div class='pname'>{persona_name}</div>
          <div class='pdesc'>{persona_data['desc']}</div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"Select", key=f"p_{persona_name}", use_container_width=True):
            st.session_state.persona = persona_name
            st.rerun()

    st.markdown("---")

    # Model settings
    st.markdown("**⚙️ Settings**")
    model_choice = st.selectbox(
        "Model",
        ["claude-sonnet-4-5", "claude-opus-4-5", "claude-haiku-4-5-20251001"],
        index=0,
        help="Select the Claude model to use"
    )
    max_tokens = st.slider("Max Response Tokens", 256, 4096, 1024, 128)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05,
                            help="Higher = more creative, Lower = more precise")

    st.markdown("---")

    # Stats
    st.markdown("**📈 Session Stats**")
    col1, col2 = st.columns(2)
    col1.markdown(f"<div class='stat-pill'>💬 {st.session_state.total_messages}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='stat-pill'>🔤 {st.session_state.total_tokens:,}</div>", unsafe_allow_html=True)

    st.markdown("")

    # Export chat
    if st.session_state.messages:
        chat_export = json.dumps([
            {"role": m["role"], "content": m["content"], "time": m.get("time","")}
            for m in st.session_state.messages
        ], indent=2)
        st.download_button(
            "⬇️ Export Chat (JSON)",
            data=chat_export,
            file_name=f"nova_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages       = []
        st.session_state.total_tokens   = 0
        st.session_state.total_messages = 0
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;color:#33334A;text-align:center;'>"
        "Nova v2.0 · Built with Streamlit<br>Powered by Anthropic Claude"
        "</div>",
        unsafe_allow_html=True
    )


# ── Main Chat Area ─────────────────────────────────────────────────────────────
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='chat-header'>
  <div class='logo'>Nova</div>
  <div class='tagline'>Your intelligent companion · Ask anything</div>
</div>
""", unsafe_allow_html=True)

# API Key guard
if not st.session_state.api_key:
    st.markdown("""
    <div class='empty-state'>
      <div class='spark'>🔑</div>
      <h3>API Key Required</h3>
      <p>Enter your Anthropic API key in the sidebar to start chatting with Nova.</p>
      <p style='font-size:0.8rem;color:#33334A;'>
        Get your key at <b style='color:#A78BFA;'>console.anthropic.com</b>
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


def render_message(role, content, timestamp=""):
    """Render a single chat message with avatar and bubble."""
    avatar_html = (
        "<div class='avatar user-av'>You</div>"
        if role == "user"
        else f"<div class='avatar bot-av'>{PERSONAS[st.session_state.persona]['icon']}</div>"
    )
    time_html = f"<div class='msg-time'>{timestamp}</div>" if timestamp else ""

    # Escape content for safe HTML embedding
    import html as html_mod
    safe_content = html_mod.escape(content)
    # Restore markdown-style code blocks
    import re
    safe_content = re.sub(r"```(\w*)\n(.*?)```", lambda m:
        f"<pre><code>{m.group(2)}</code></pre>", safe_content, flags=re.DOTALL)
    safe_content = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe_content)

    if role == "user":
        st.markdown(f"""
        <div class='msg-row user'>
          {avatar_html}
          <div>
            <div class='bubble'>{safe_content}</div>
            {time_html}
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='msg-row assistant'>
          {avatar_html}
          <div>
            <div class='bubble'>{safe_content}</div>
            {time_html}
          </div>
        </div>""", unsafe_allow_html=True)


# ── Message History ────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown(f"""
    <div class='empty-state'>
      <div class='spark'>✦</div>
      <h3>How can I help you today?</h3>
      <p>I'm {st.session_state.persona} — ask me anything.</p>
    </div>
    <div class='chips-row'>
    {"".join(f"<div class='chip'>{s}</div>" for s in SUGGESTIONS)}
    </div>
    """, unsafe_allow_html=True)

    # Clickable suggestion buttons
    cols = st.columns(3)
    for i, suggestion in enumerate(SUGGESTIONS):
        if cols[i % 3].button(suggestion, key=f"sug_{i}", use_container_width=True):
            st.session_state.pending_input = suggestion
            st.rerun()
else:
    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"], msg.get("time", ""))

st.markdown("</div>", unsafe_allow_html=True)  # close chat-wrapper

# ── Chat Input (Streamlit native — triggers cleanly without full rerun) ────────
prompt = st.chat_input(
    placeholder=f"Message {st.session_state.persona}...",
    key="main_chat_input"
)

# Pick up suggestion clicks
if st.session_state.pending_input and not prompt:
    prompt = st.session_state.pending_input
    st.session_state.pending_input = ""

# ── Handle Submission ──────────────────────────────────────────────────────────
if prompt:
    ts = datetime.now().strftime("%H:%M")

    # Append & render user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt, "time": ts})
    st.session_state.total_messages += 1
    render_message("user", prompt, ts)

    # Build API message list
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]
    system_prompt = PERSONAS[st.session_state.persona]["system"]

    # Render assistant bubble that streams into it live
    with st.chat_message("assistant"):
        try:
            client = anthropic.Anthropic(api_key=st.session_state.api_key)

            full_response = ""
            response_placeholder = st.empty()

            with client.messages.stream(
                model=model_choice,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=api_messages,
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    # Update placeholder with accumulated text in real time
                    response_placeholder.markdown(full_response + "▌")

            # Final render without cursor
            response_placeholder.markdown(full_response)

            # Token accounting
            try:
                final_msg = stream.get_final_message()
                tokens_used = (
                    final_msg.usage.input_tokens + final_msg.usage.output_tokens
                )
                st.session_state.total_tokens += tokens_used
            except Exception:
                pass

        except anthropic.AuthenticationError:
            full_response = "❌ Invalid API key. Please check your Anthropic API key in the sidebar."
            st.error(full_response)

        except anthropic.RateLimitError:
            full_response = "⚠️ Rate limit reached. Please wait a moment and try again."
            st.warning(full_response)

        except anthropic.APIError as e:
            full_response = f"⚠️ API error: {str(e)}"
            st.error(full_response)

        except Exception as e:
            full_response = f"❌ Unexpected error: {str(e)}"
            st.error(full_response)

    # Save assistant response
    ts_resp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "time": ts_resp
    })
    st.session_state.total_messages += 1
