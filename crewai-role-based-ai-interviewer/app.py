
import os
import random
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── API key detection ─────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
LIVE_MODE = bool(OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your_"))

# ── Role config ───────────────────────────────────────────────────────────────
ROLES = {
    "Data Scientist": {
        "icon": "🧠",
        "color": "#6C63FF",
        "tag": "ML · Statistics · Modelling",
        "questions": [
            "What is overfitting in machine learning, and how do you prevent it?",
            "Explain the difference between regression and classification with examples.",
            "What is the purpose of cross-validation, and how does k-fold work?",
            "How would you handle a highly imbalanced dataset?",
            "Explain the bias-variance tradeoff in simple terms.",
            "What is the difference between supervised and unsupervised learning?",
        ],
    },
    "Web Developer": {
        "icon": "💻",
        "color": "#00B4D8",
        "tag": "APIs · Frontend · HTTP",
        "questions": [
            "Explain the difference between REST and GraphQL APIs.",
            "What is the virtual DOM in React and why does it matter?",
            "How does CSS specificity work? Give an example.",
            "What are HTTP status codes? Name a few important ones.",
            "Explain the concept of responsive design and how you implement it.",
            "What is CORS and how do you handle it in a web application?",
        ],
    },
    "Product Manager": {
        "icon": "📋",
        "color": "#F77F00",
        "tag": "Strategy · Metrics · Roadmap",
        "questions": [
            "How do you prioritize features when you have limited engineering resources?",
            "Describe a time you used data to make a product decision.",
            "What frameworks do you use for writing user stories?",
            "How do you measure the success of a product feature after launch?",
            "Explain the difference between output metrics and outcome metrics.",
            "How would you handle a situation where engineering and design disagree on a solution?",
        ],
    },
    "UI/UX Designer": {
        "icon": "🎨",
        "color": "#E63946",
        "tag": "Design · Research · Accessibility",
        "questions": [
            "Walk me through your design process from research to final delivery.",
            "What is the difference between UX and UI design?",
            "How do you conduct user research, and what methods do you prefer?",
            "Explain the concept of information architecture.",
            "How do you ensure your designs are accessible to users with disabilities?",
            "Describe a time when user feedback significantly changed your design direction.",
        ],
    },
}

# ── Demo feedback ─────────────────────────────────────────────────────────────
DEMO_FEEDBACK = [
    "Good explanation! You covered the core concept clearly. Try to include a real-world example next time to make your answer even stronger.",
    "That's a solid answer. You demonstrated a good understanding of the topic. Consider elaborating on edge cases or trade-offs to show deeper knowledge.",
    "Nice start! The key idea is there. Adding more specific details or a concrete example would make this answer stand out.",
    "You're on the right track. Try to structure your answer with a brief definition first, then an example, then the practical implication.",
    "Good effort! You touched on the important points. A bit more depth on the 'why' behind your answer would really impress an interviewer.",
    "That's correct, but can you provide an example? Grounding your answer in a real scenario shows practical experience.",
]


def get_demo_feedback(answer: str) -> str:
    words = len(answer.strip().split())
    if words < 10:
        return "Your answer is quite brief. Try to expand on the concept and include at least one example to demonstrate your understanding."
    if words > 120:
        return "Great detail! You clearly know this topic well. In a real interview, aim for 60–90 words and let the interviewer ask follow-ups."
    return random.choice(DEMO_FEEDBACK)


def get_live_feedback(question: str, answer: str) -> str:
    from crewai import Agent, Task, Crew
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=OPENAI_API_KEY)
    agent = Agent(
        role="Interview Feedback Coach",
        goal="Provide concise, constructive feedback on interview answers",
        backstory=(
            "You are an experienced hiring manager and interview coach. "
            "You give short, honest, and encouraging feedback. Keep it to 2-3 sentences."
        ),
        llm=llm,
        verbose=False,
    )
    task = Task(
        description=(
            f"Candidate was asked: '{question}'\nTheir answer: '{answer}'\n\n"
            "Give 2-3 sentence constructive feedback. Start positive, then suggest one improvement."
        ),
        expected_output="2-3 sentence feedback on the candidate's answer.",
        agent=agent,
    )
    return str(Crew(agents=[agent], tasks=[task], verbose=False).kickoff())


def get_feedback(question: str, answer: str) -> str:
    return get_live_feedback(question, answer) if LIVE_MODE else get_demo_feedback(answer)


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Mock Interviewer",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base & fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── App background ── */
.stApp { background: #0f1117; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #161b27;
    border-right: 1px solid #1e2535;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }

/* ── Role card grid ── */
.role-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin: 24px 0; }
.role-card {
    background: #161b27;
    border: 2px solid #1e2535;
    border-radius: 14px;
    padding: 22px 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}
.role-card:hover { border-color: #6C63FF; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(108,99,255,0.15); }
.role-card.selected { border-color: var(--role-color); box-shadow: 0 0 0 3px color-mix(in srgb, var(--role-color) 25%, transparent); }
.role-icon { font-size: 2.4rem; margin-bottom: 8px; }
.role-name { font-size: 1rem; font-weight: 600; color: #e6edf3; margin-bottom: 4px; }
.role-tag { font-size: 0.72rem; color: #8b949e; letter-spacing: 0.04em; }

/* ── Question card ── */
.q-card {
    background: #161b27;
    border-left: 4px solid #6C63FF;
    border-radius: 0 12px 12px 0;
    padding: 20px 24px;
    margin: 20px 0 16px;
}
.q-label { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em; color: #8b949e; text-transform: uppercase; margin-bottom: 8px; }
.q-text { font-size: 1.1rem; font-weight: 500; color: #e6edf3; line-height: 1.6; }

/* ── Feedback card ── */
.fb-card {
    background: linear-gradient(135deg, #0d2137 0%, #0a1628 100%);
    border: 1px solid #1e4a6e;
    border-radius: 12px;
    padding: 18px 22px;
    margin-top: 12px;
}
.fb-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em; color: #58a6ff; text-transform: uppercase; margin-bottom: 8px; }
.fb-text { font-size: 0.95rem; color: #c9d1d9; line-height: 1.65; }

/* ── History item ── */
.hist-card {
    background: #161b27;
    border: 1px solid #1e2535;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.hist-q { font-size: 0.82rem; font-weight: 600; color: #8b949e; margin-bottom: 6px; }
.hist-a { font-size: 0.88rem; color: #c9d1d9; margin-bottom: 8px; }
.hist-fb { font-size: 0.85rem; color: #58a6ff; font-style: italic; }

/* ── Stat pill ── */
.stat-pill {
    background: #1e2535;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.stat-icon { font-size: 1.3rem; }
.stat-label { font-size: 0.75rem; color: #8b949e; }
.stat-value { font-size: 1rem; font-weight: 600; color: #e6edf3; }

/* ── Mode badge ── */
.mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 4px;
}
.mode-live { background: #0d2b1a; color: #3fb950; border: 1px solid #238636; }
.mode-demo { background: #2b1d0a; color: #d29922; border: 1px solid #9e6a03; }

/* ── Hero ── */
.hero { text-align: center; padding: 40px 0 20px; }
.hero-title { font-size: 2.4rem; font-weight: 700; color: #e6edf3; margin-bottom: 8px; }
.hero-sub { font-size: 1rem; color: #8b949e; }

/* ── Summary header ── */
.summary-header {
    background: linear-gradient(135deg, #0d2b1a, #0a1628);
    border: 1px solid #238636;
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    margin-bottom: 24px;
}
.summary-title { font-size: 1.6rem; font-weight: 700; color: #3fb950; margin-bottom: 4px; }
.summary-sub { font-size: 0.9rem; color: #8b949e; }

/* ── Streamlit widget overrides ── */
.stTextArea textarea {
    background: #161b27 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    color: #e6edf3 !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.2) !important;
}
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6C63FF, #5a52e0) !important;
    border: none !important;
    color: white !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(108,99,255,0.35) !important;
}
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #6C63FF, #00B4D8) !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key, default in [
    ("started", False),
    ("q_index", 0),
    ("history", []),
    ("current_role", None),
    ("selected_role", "Data Scientist"),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def start_interview():
    st.session_state.started = True
    st.session_state.q_index = 0
    st.session_state.history = []
    st.session_state.current_role = st.session_state.selected_role


def restart():
    for k in ["started", "q_index", "history", "current_role"]:
        del st.session_state[k]


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎙️ AI Interviewer")
    st.divider()

    # Mode badge
    if LIVE_MODE:
        st.markdown('<div class="mode-badge mode-live">🟢 Live Mode — GPT-4o-mini</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="mode-badge mode-demo">🟡 Demo Mode — No API key</div>', unsafe_allow_html=True)
        st.caption("Add `OPENAI_API_KEY` to `.env` for live AI feedback.")

    st.divider()

    # Stats during interview
    if st.session_state.started:
        role = st.session_state.current_role
        cfg = ROLES[role]
        total = len(cfg["questions"])
        done = st.session_state.q_index

        st.markdown("**Session Stats**")
        st.markdown(f"""
        <div class="stat-pill">
            <span class="stat-icon">{cfg['icon']}</span>
            <div><div class="stat-label">Role</div><div class="stat-value">{role}</div></div>
        </div>
        <div class="stat-pill">
            <span class="stat-icon">✅</span>
            <div><div class="stat-label">Answered</div><div class="stat-value">{done} / {total}</div></div>
        </div>
        <div class="stat-pill">
            <span class="stat-icon">📊</span>
            <div><div class="stat-label">Progress</div><div class="stat-value">{int((done/total)*100)}%</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        if st.button("🔄 Restart", use_container_width=True):
            restart()
            st.rerun()
    else:
        st.markdown("**How it works**")
        st.markdown("""
        1. Pick a job role
        2. Answer 6 questions
        3. Get instant feedback
        4. Review your summary
        """)
        st.divider()
        st.markdown("**Roles available**")
        for name, cfg in ROLES.items():
            st.markdown(f"{cfg['icon']} {name}")


# ── Landing page ──────────────────────────────────────────────────────────────
if not st.session_state.started:
    st.markdown("""
    <div class="hero">
        <div class="hero-title">🎙️ AI Mock Interviewer</div>
        <div class="hero-sub">Role-based interview practice powered by CrewAI</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Choose your interview role")

    # Role cards — 2 per row using columns
    role_names = list(ROLES.keys())
    for row in range(0, len(role_names), 2):
        cols = st.columns(2, gap="medium")
        for col_i, col in enumerate(cols):
            idx = row + col_i
            if idx >= len(role_names):
                break
            name = role_names[idx]
            cfg = ROLES[name]
            is_selected = st.session_state.selected_role == name
            border = f"2px solid {cfg['color']}" if is_selected else "2px solid #1e2535"
            glow = f"box-shadow: 0 0 0 3px {cfg['color']}33;" if is_selected else ""
            with col:
                st.markdown(f"""
                <div class="role-card" style="border: {border}; {glow}">
                    <div class="role-icon">{cfg['icon']}</div>
                    <div class="role-name">{name}</div>
                    <div class="role-tag">{cfg['tag']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(
                    f"{'✓ Selected' if is_selected else 'Select'} — {name}",
                    key=f"select_{name}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary",
                ):
                    st.session_state.selected_role = name
                    st.rerun()

    st.divider()

    sel = st.session_state.selected_role
    sel_cfg = ROLES[sel]
    st.markdown(f"**Selected:** {sel_cfg['icon']} {sel} &nbsp;·&nbsp; {sel_cfg['tag']}")
    st.markdown(f"You'll answer **{len(sel_cfg['questions'])} questions** and receive feedback after each one.")

    st.button("Start Interview ▶", on_click=start_interview, type="primary", use_container_width=False)


# ── Interview screen ──────────────────────────────────────────────────────────
elif st.session_state.q_index < len(ROLES[st.session_state.current_role]["questions"]):
    role = st.session_state.current_role
    cfg = ROLES[role]
    questions = cfg["questions"]
    total = len(questions)
    idx = st.session_state.q_index

    # Header row
    col_title, col_badge = st.columns([3, 1])
    with col_title:
        st.markdown(f"## {cfg['icon']} {role} Interview")
    with col_badge:
        st.markdown(f"<br>", unsafe_allow_html=True)

    # Progress
    st.progress(idx / total, text=f"Question {idx + 1} of {total}")
    st.markdown("")

    # Completed history (collapsed)
    if st.session_state.history:
        with st.expander(f"📖 Previous answers ({len(st.session_state.history)} completed)", expanded=False):
            for item in st.session_state.history:
                st.markdown(f"""
                <div class="hist-card">
                    <div class="hist-q">Q{item['num']} — {item['question']}</div>
                    <div class="hist-a">💬 {item['answer']}</div>
                    <div class="hist-fb">💡 {item['feedback']}</div>
                </div>
                """, unsafe_allow_html=True)

    # Current question card
    st.markdown(f"""
    <div class="q-card" style="border-left-color: {cfg['color']};">
        <div class="q-label">Question {idx + 1} of {total}</div>
        <div class="q-text">{questions[idx]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Answer input
    answer = st.text_area(
        "Your answer",
        key=f"answer_{idx}",
        height=160,
        placeholder="Type your answer here... Be specific and use examples where possible.",
        label_visibility="collapsed",
    )

    # Word count hint
    word_count = len(answer.strip().split()) if answer.strip() else 0
    wc_color = "#3fb950" if 30 <= word_count <= 120 else "#d29922" if word_count > 0 else "#8b949e"
    st.markdown(
        f'<p style="font-size:0.78rem; color:{wc_color}; margin-top:-8px;">'
        f'{"✓" if 30 <= word_count <= 120 else "ℹ"} {word_count} words'
        f'{"  ·  Aim for 30–120 words" if word_count < 30 and word_count > 0 else ""}'
        f'</p>',
        unsafe_allow_html=True,
    )

    col_btn, col_tip = st.columns([1, 3])
    with col_btn:
        submit = st.button("Submit Answer ➜", type="primary", use_container_width=True)

    if submit:
        if answer.strip():
            with st.spinner("Analysing your answer..."):
                feedback = get_feedback(questions[idx], answer)
            st.session_state.history.append({
                "num": idx + 1,
                "question": questions[idx],
                "answer": answer,
                "feedback": feedback,
            })
            st.session_state.q_index += 1
            st.rerun()
        else:
            st.warning("Please enter an answer before submitting.")


# ── Summary screen ────────────────────────────────────────────────────────────
else:
    role = st.session_state.current_role
    cfg = ROLES[role]
    total = len(cfg["questions"])

    st.markdown(f"""
    <div class="summary-header">
        <div class="summary-title">🎉 Interview Complete!</div>
        <div class="summary-sub">{cfg['icon']} {role} &nbsp;·&nbsp; {total} questions answered</div>
    </div>
    """, unsafe_allow_html=True)

    # Score strip
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Questions", total)
    with c2:
        avg_words = int(sum(len(i["answer"].split()) for i in st.session_state.history) / total)
        st.metric("Avg. Answer Length", f"{avg_words} words")
    with c3:
        st.metric("Role", cfg["icon"] + " " + role)

    st.divider()
    st.markdown("### 📝 Full Session Review")

    for item in st.session_state.history:
        with st.expander(f"Q{item['num']}  ·  {item['question']}", expanded=True):
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <span style="font-size:0.72rem;font-weight:600;letter-spacing:.08em;color:#8b949e;text-transform:uppercase;">Your Answer</span>
                <p style="color:#e6edf3;margin-top:4px;font-size:0.95rem;line-height:1.6;">{item['answer']}</p>
            </div>
            <div class="fb-card">
                <div class="fb-label">💡 AI Feedback</div>
                <div class="fb-text">{item['feedback']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    col_r, col_s = st.columns([1, 3])
    with col_r:
        if st.button("🔄 Try Another Role", type="primary", use_container_width=True):
            restart()
            st.rerun()
