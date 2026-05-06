import streamlit as st
import time
import os
from dotenv import load_dotenv

from analyzer import analyze_repo
from components.health_gauge import render_health_gauge
from components.architecture import render_architecture
from components.file_tree import render_file_tree
from components.quick_wins import render_quick_wins
from components.sprint_plan import render_sprint_plan
from components.report import render_report

load_dotenv()

# Page config
st.set_page_config(
    page_title="FDE Codebase Scout",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS — Aristotle-inspired warm dark aesthetic
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet">
<style>
    /* === GLOBAL — Warm dark palette inspired by Aristotle's earthy warmth === */
    .stApp {
        background-color: #111110;
        font-family: 'DM Sans', -apple-system, sans-serif;
    }

    .stApp * {
        font-family: 'DM Sans', -apple-system, sans-serif;
    }

    /* Dotted grid background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: radial-gradient(circle, #2A2A28 1px, transparent 1px);
        background-size: 24px 24px;
        pointer-events: none;
        z-index: -1;
        opacity: 0.4;
    }

    /* Sidebar — warm charcoal */
    section[data-testid="stSidebar"] {
        background-color: #161615;
        border-right: 1px solid rgba(207, 173, 153, 0.08);
    }

    section[data-testid="stSidebar"] .stMarkdown {
        font-family: 'DM Sans', sans-serif;
    }

    /* === TYPOGRAPHY — Warm, readable hierarchy === */
    .stApp h1 {
        color: #F5F0EB !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.03em !important;
    }

    .stApp h2 {
        color: #E8E0D8 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1.15rem !important;
        letter-spacing: -0.01em !important;
        margin-top: 1.5rem !important;
    }

    .stApp h3 {
        color: #E8E0D8 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }

    .stApp p, .stApp label, .stApp span {
        color: #9C9488 !important;
        font-family: 'DM Sans', sans-serif;
    }

    /* === TABS — Warm underline style === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: transparent;
        border-bottom: 1px solid rgba(207, 173, 153, 0.1);
        padding: 0;
        border-radius: 0;
    }

    .stTabs [data-baseweb="tab"] {
        color: #6B6560;
        border-radius: 0;
        padding: 14px 24px;
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        font-weight: 500;
        border-bottom: 2px solid transparent;
        background: transparent !important;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #E8A87C;
    }

    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #F5F0EB !important;
        border-bottom: 2px solid #E8A87C !important;
    }

    /* === BUTTONS — Warm cream accent === */
    .stButton > button {
        background: #CFAD99;
        color: #111110;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        padding: 11px 22px;
        letter-spacing: 0.01em;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton > button:hover {
        background: #D7BCA4;
        color: #111110;
        transform: translateY(-1px);
        box-shadow: 0 8px 24px rgba(207, 173, 153, 0.2);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(207, 173, 153, 0.15);
    }

    /* Download button */
    .stDownloadButton > button {
        background: rgba(207, 173, 153, 0.08);
        color: #CFAD99;
        border: 1px solid rgba(207, 173, 153, 0.2);
        border-radius: 8px;
        font-weight: 500;
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        transition: all 0.2s ease;
    }

    .stDownloadButton > button:hover {
        background: rgba(207, 173, 153, 0.12);
        border-color: rgba(207, 173, 153, 0.4);
        box-shadow: 0 4px 16px rgba(207, 173, 153, 0.1);
    }

    /* === INPUTS — Subtle warm borders === */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #1A1A18;
        border: 1px solid rgba(207, 173, 153, 0.12);
        color: #F5F0EB;
        border-radius: 8px;
        font-family: 'DM Mono', monospace;
        font-size: 13px;
        padding: 12px 14px;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: rgba(207, 173, 153, 0.4);
        box-shadow: 0 0 0 3px rgba(207, 173, 153, 0.06);
    }

    .stTextInput label, .stTextArea label {
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important;
        font-weight: 400 !important;
        color: #6B6560 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* === EXPANDER — Glass card effect === */
    .streamlit-expanderHeader {
        background-color: rgba(207, 173, 153, 0.03);
        border: 1px solid rgba(207, 173, 153, 0.08);
        border-radius: 10px;
        color: #E8E0D8 !important;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.2s ease;
    }

    .streamlit-expanderHeader:hover {
        background-color: rgba(207, 173, 153, 0.06);
        border-color: rgba(207, 173, 153, 0.15);
    }

    .streamlit-expanderContent {
        border: 1px solid rgba(207, 173, 153, 0.08);
        border-top: none;
        border-radius: 0 0 10px 10px;
        background: rgba(207, 173, 153, 0.02);
    }

    /* === STATUS === */
    .stStatus {
        background-color: #161615;
        border: 1px solid rgba(207, 173, 153, 0.08);
        border-radius: 10px;
    }

    /* === SCROLLBAR — Thin, warm === */
    ::-webkit-scrollbar {
        width: 5px;
        height: 5px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(207, 173, 153, 0.15);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(207, 173, 153, 0.3);
    }

    /* === HIDE DEFAULTS === */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hide BaseWeb keyboard navigation hints and input method labels */
    [data-baseweb="select"] li[aria-label="Keyboard"],
    [data-baseweb="popover"] li[role="option"][aria-label="Keyboard"],
    [role="listbox"] li:has(> div:only-child):last-child,
    div[data-baseweb="popover"] div[role="listbox"] li[aria-label="Keyboard"],
    ul[role="listbox"] li[aria-label="Keyboard"] {
        display: none !important;
    }

    /* Ensure sidebar is always visible */
    section[data-testid="stSidebar"] {
        display: block !important;
        opacity: 1 !important;
        visibility: visible !important;
        width: 320px !important;
        min-width: 320px !important;
    }

    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Hide sidebar collapse/expand arrow button */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarNavCollapseButton"],
    button[kind="headerNoPadding"],
    section[data-testid="stSidebar"] button[aria-label*="Collapse"],
    section[data-testid="stSidebar"] button[aria-label*="Close"],
    [data-testid="stSidebar"] > div > div > div > button {
        display: none !important;
    }

    /* Nuclear: hide ALL material icon ligature text everywhere */
    [data-testid="stExpanderToggleIcon"] svg,
    [data-testid="stExpanderToggleIcon"] span {
        display: none !important;
    }

    .stExpander span[class*="emotion-cache"],
    .stStatus span[class*="emotion-cache"] {
        font-family: 'Material Symbols Rounded' !important;
    }

    /* Global fix: any span rendering icon ligatures */
    span {
        font-variant-ligatures: none !important;
    }

    /* Target the exact Streamlit icon pattern */
    [data-testid="stExpanderToggleIcon"] {
        font-size: 0 !important;
        width: 18px !important;
        height: 18px !important;
        overflow: hidden !important;
        position: relative !important;
    }

    [data-testid="stExpanderToggleIcon"]::after {
        content: '▸' !important;
        font-size: 14px !important;
        font-family: 'DM Sans', sans-serif !important;
        color: #6B6560 !important;
        position: absolute !important;
        top: 0; left: 0;
    }

    details[open] > summary [data-testid="stExpanderToggleIcon"]::after {
        content: '▾' !important;
    }

    /* Hide keyboard text in status widget */
    [data-testid="stStatusWidget"] span:not([data-testid]) {
        font-size: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
    }

    /* === DIVIDERS === */
    hr {
        border-color: rgba(207, 173, 153, 0.08) !important;
    }

    /* === ANIMATIONS — Staggered reveals inspired by Uncommon Studio === */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(207, 173, 153, 0); }
        50% { box-shadow: 0 0 20px 2px rgba(207, 173, 153, 0.08); }
    }

    .stTabs {
        animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Staggered card animations */
    [data-testid="column"]:nth-child(1) { animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.05s both; }
    [data-testid="column"]:nth-child(2) { animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.12s both; }
    [data-testid="column"]:nth-child(3) { animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.19s both; }
    [data-testid="column"]:nth-child(4) { animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.26s both; }

    /* Hover micro-interactions — Unseen Studio style */
    .stApp [data-testid="column"] > div > div > div > div {
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease;
    }

    .stApp [data-testid="column"] > div > div > div > div:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(207, 173, 153, 0.08);
    }

    /* Expander hover lift */
    .streamlit-expanderHeader {
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .streamlit-expanderHeader:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(207, 173, 153, 0.06);
    }

    /* Plotly chart container subtle glow */
    [data-testid="stPlotlyChart"] {
        animation: pulseGlow 4s ease-in-out infinite;
        border-radius: 12px;
    }

    /* Tab content fade in */
    .stTabs [data-baseweb="tab-panel"] {
        animation: fadeIn 0.4s ease forwards;
    }
</style>
""", unsafe_allow_html=True)

# Sample repos
SAMPLE_REPOS = {
    "acme-fitness-app": {
        "description": """Repository: acme-fitness-app
Tech Stack: TypeScript, React 17 (with some class components), Node.js/Express backend, PostgreSQL, Redis for caching, Custom JWT authentication, Docker + AWS ECS deployment
Size: 142 files, ~18,000 lines of code
Description: A fitness SaaS platform with user management, workout tracking, and subscription billing. Built by a small team over 2 years. Has some legacy patterns, minimal test coverage (~30%), and inconsistent API documentation. Uses a monorepo structure with shared packages.""",
    },
    "retool-crm-internal": {
        "description": """Repository: retool-crm-internal
Tech Stack: Python 3.9, FastAPI, PostgreSQL with SQLAlchemy ORM, Alembic migrations, Basic API key auth, Deployed on Heroku with GitHub Actions CI
Size: 87 files, ~9,500 lines of code
Description: An internal CRM tool built for a sales team of 25. Handles contact management, deal tracking, and email integration. Built in 6 months by a single developer who left the company. No tests, hardcoded config values, some SQL injection risks in raw queries. Needs security audit and proper auth.""",
    },
    "greenfield-ecommerce": {
        "description": """Repository: greenfield-ecommerce
Tech Stack: Next.js 14 (App Router), Prisma ORM, PostgreSQL, Stripe for payments, NextAuth.js, Tailwind CSS, Vercel deployment, Turborepo monorepo
Size: 203 files, ~24,000 lines of code
Description: A modern e-commerce platform 3 months into development. Well-structured with good TypeScript coverage, but missing critical features: no rate limiting, no error monitoring, incomplete webhook handling, no load testing done. Team of 3 developers, good PR practices, 60% test coverage on API routes.""",
    },
}

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="padding: 28px 0 20px;">
        <div style="display: flex; align-items: center; gap: 12px; justify-content: center;">
            <div style="width: 36px; height: 36px; background: linear-gradient(145deg, #CFAD99, #A68B76); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(207, 173, 153, 0.2);">
                <span style="font-size: 18px; line-height: 1;">&#9889;</span>
            </div>
            <div>
                <div style="color: #F5F0EB; font-family: 'DM Sans', sans-serif; font-size: 17px; font-weight: 600; letter-spacing: -0.02em;">Codebase Scout</div>
                <div style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.06em; text-transform: uppercase;">FDE Tools</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    github_url = st.text_input("GITHUB URL", placeholder="https://github.com/org/repo")

    repo_description = st.text_area(
        "DESCRIBE THE CODEBASE",
        placeholder="Tech stack, size, what it does, known issues...",
        height=140,
    )

    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
    analyze_clicked = st.button("Run Analysis", use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <span style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;">Sample Repos</span>
    </div>
    """, unsafe_allow_html=True)

    # Sample repo buttons styled with dark text via markdown + buttons
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] [data-testid="baseButton-secondary"] {
            background: #D7BCA4 !important;
            color: #000000 !important;
            border: none !important;
            font-family: 'DM Mono', monospace !important;
            font-size: 12px !important;
            font-weight: 600 !important;
        }
        section[data-testid="stSidebar"] [data-testid="baseButton-secondary"]:hover {
            background: #E8CCBA !important;
            color: #000000 !important;
            box-shadow: 0 4px 12px rgba(207, 173, 153, 0.25) !important;
        }
        section[data-testid="stSidebar"] [data-testid="baseButton-secondary"] p,
        section[data-testid="stSidebar"] [data-testid="baseButton-secondary"] span {
            color: #000000 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    sample_clicked = None
    if st.button("acme-fitness-app", key="sample1", use_container_width=True, type="secondary"):
        sample_clicked = "acme-fitness-app"
    if st.button("retool-crm-internal", key="sample2", use_container_width=True, type="secondary"):
        sample_clicked = "retool-crm-internal"
    if st.button("greenfield-ecommerce", key="sample3", use_container_width=True, type="secondary"):
        sample_clicked = "greenfield-ecommerce"

    # Footer
    st.markdown("<div style='flex: 1; min-height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 8px 0;">
        <p style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 10px; margin: 0;">
            built by <a href="https://github.com/isha-madhurendra" style="color: #CFAD99; text-decoration: none; font-weight: 500;">isha madhurendra</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Handle sample selection
if sample_clicked:
    st.session_state["repo_description"] = SAMPLE_REPOS[sample_clicked]["description"]
    st.session_state["trigger_analysis"] = True
    st.rerun()

# Check if we should auto-analyze from sample selection
should_analyze = analyze_clicked
if st.session_state.get("trigger_analysis"):
    should_analyze = True
    st.session_state["trigger_analysis"] = False

# Get effective description
effective_description = st.session_state.get("repo_description", repo_description)
if not effective_description:
    effective_description = repo_description
if github_url and not effective_description:
    effective_description = f"GitHub Repository: {github_url}\nPlease analyze this repository structure and provide recommendations."

# Run analysis
if should_analyze and effective_description:
    if not os.getenv("ANTHROPIC_API_KEY"):
        st.error("Missing ANTHROPIC_API_KEY. Please add it to your .env file.")
    else:
        with st.status("Analyzing codebase...", expanded=True) as status:
            st.write("Scanning repo structure...")
            time.sleep(1)
            st.write("Analyzing dependencies...")
            time.sleep(1)
            st.write("Mapping API endpoints...")
            time.sleep(1)
            st.write("Detecting tech debt...")
            time.sleep(1)
            st.write("Identifying quick wins...")
            time.sleep(1)
            st.write("Generating onboarding plan...")

            try:
                result = analyze_repo(effective_description)
                st.session_state["analysis"] = result
                status.update(label="Analysis complete!", state="complete")
            except Exception as e:
                status.update(label="Analysis failed", state="error")
                st.toast(f"Error: {str(e)}", icon="")

# Display results
if "analysis" in st.session_state:
    analysis = st.session_state["analysis"]

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Architecture", "Quick Wins", "Sprint Plan", "Report"])

    with tab1:
        col_gauge, col_summary = st.columns([1, 2])
        with col_gauge:
            render_health_gauge(analysis.get("health_score", 0))
        with col_summary:
            st.markdown(f"""
            <div style="background: rgba(207, 173, 153, 0.03); border: 1px solid rgba(207, 173, 153, 0.1); border-radius: 12px; padding: 28px; margin-top: 10px;">
                <div style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 14px;">Executive Summary</div>
                <p style="color: #D4CBC2; font-family: 'DM Sans', sans-serif; font-size: 14px; line-height: 1.8; margin: 0;">{analysis.get('summary', '')}</p>
            </div>
            """, unsafe_allow_html=True)

        # Stat cards
        st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        quick_wins_count = len(analysis.get("quick_wins", []))
        total_sp = sum(w.get("story_points", 0) for w in analysis.get("onboarding_plan", []))
        critical_count = sum(1 for w in analysis.get("quick_wins", []) if w.get("impact") == "Critical")

        with c1:
            st.markdown(f"""
            <div style="background: rgba(207, 173, 153, 0.03); border: 1px solid rgba(207, 173, 153, 0.1); border-radius: 12px; padding: 24px; text-align: center;">
                <div style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px;">Quick Wins</div>
                <div style="color: #FF8C42; font-size: 32px; font-weight: 700; font-family: 'DM Mono', monospace;">{quick_wins_count}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background: rgba(207, 173, 153, 0.03); border: 1px solid rgba(207, 173, 153, 0.1); border-radius: 12px; padding: 24px; text-align: center;">
                <div style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px;">Story Points</div>
                <div style="color: #FFB020; font-size: 32px; font-weight: 700; font-family: 'DM Mono', monospace;">{total_sp}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div style="background: rgba(207, 173, 153, 0.03); border: 1px solid rgba(207, 173, 153, 0.1); border-radius: 12px; padding: 24px; text-align: center;">
                <div style="color: #6B6560; font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px;">Critical</div>
                <div style="color: #FF4D4D; font-size: 32px; font-weight: 700; font-family: 'DM Mono', monospace;">{critical_count}</div>
            </div>
            """, unsafe_allow_html=True)

        # File tree in overview
        st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
        render_file_tree(analysis.get("file_tree", {}))

    with tab2:
        render_architecture(
            analysis.get("architecture", []),
            analysis.get("mermaid_diagram", ""),
        )

    with tab3:
        render_quick_wins(analysis.get("quick_wins", []))

    with tab4:
        render_sprint_plan(analysis.get("onboarding_plan", []))

    with tab5:
        render_report(analysis)

else:
    # Welcome state
    st.markdown("""
    <div style="text-align: center; padding: 110px 20px 60px;">
        <div style="margin-bottom: 28px;">
            <div style="width: 64px; height: 64px; background: linear-gradient(145deg, #CFAD99, #A68B76); border-radius: 18px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 24px; box-shadow: 0 8px 32px rgba(207, 173, 153, 0.2), 0 0 60px rgba(207, 173, 153, 0.08); animation: pulseGlow 3s ease-in-out infinite;">
                <span style="font-size: 30px;">&#9889;</span>
            </div>
        </div>
        <h1 style="font-family: 'DM Sans', sans-serif; font-size: 48px; font-weight: 700; letter-spacing: -0.04em; margin-bottom: 16px; background: linear-gradient(135deg, #F5F0EB 0%, #CFAD99 50%, #FF8C42 100%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: shimmer 4s linear infinite;">Codebase Scout</h1>
        <p style="color: #7A7168; font-family: 'DM Sans', sans-serif; font-size: 17px; max-width: 440px; margin: 0 auto 60px; line-height: 1.6; font-weight: 400;">
            AI-powered codebase analysis for<br>Forward Deployed Engineers.
        </p>
        <div style="display: flex; justify-content: center; gap: 18px; flex-wrap: wrap; max-width: 740px; margin: 0 auto;">
            <div class="feature-card" style="background: rgba(207, 173, 153, 0.04); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(207, 173, 153, 0.12); border-radius: 16px; padding: 32px 26px; width: 210px; text-align: left; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both; cursor: default;">
                <div style="width: 36px; height: 36px; background: rgba(255, 140, 66, 0.12); border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; border: 1px solid rgba(255, 140, 66, 0.2);">
                    <span style="color: #FF8C42; font-size: 16px;">&#9776;</span>
                </div>
                <div style="color: #FF8C42; font-family: 'DM Mono', monospace; font-size: 10px; font-weight: 600; letter-spacing: 0.06em; margin-bottom: 12px;">01 &mdash; ASSESS</div>
                <div style="color: #F5F0EB; font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 15px; margin-bottom: 8px;">Health Score</div>
                <div style="color: #7A7168; font-family: 'DM Sans', sans-serif; font-size: 12px; line-height: 1.6;">Codebase quality gauge with detailed breakdown</div>
            </div>
            <div class="feature-card" style="background: rgba(207, 173, 153, 0.04); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(207, 173, 153, 0.12); border-radius: 16px; padding: 32px 26px; width: 210px; text-align: left; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.35s both; cursor: default;">
                <div style="width: 36px; height: 36px; background: rgba(255, 176, 32, 0.12); border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; border: 1px solid rgba(255, 176, 32, 0.2);">
                    <span style="color: #FFB020; font-size: 16px;">&#9881;</span>
                </div>
                <div style="color: #FFB020; font-family: 'DM Mono', monospace; font-size: 10px; font-weight: 600; letter-spacing: 0.06em; margin-bottom: 12px;">02 &mdash; MAP</div>
                <div style="color: #F5F0EB; font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 15px; margin-bottom: 8px;">Architecture</div>
                <div style="color: #7A7168; font-family: 'DM Sans', sans-serif; font-size: 12px; line-height: 1.6;">Visual system diagram with layer connections</div>
            </div>
            <div class="feature-card" style="background: rgba(207, 173, 153, 0.04); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(207, 173, 153, 0.12); border-radius: 16px; padding: 32px 26px; width: 210px; text-align: left; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.5s both; cursor: default;">
                <div style="width: 36px; height: 36px; background: rgba(74, 222, 128, 0.12); border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; border: 1px solid rgba(74, 222, 128, 0.2);">
                    <span style="color: #4ADE80; font-size: 16px;">&#9650;</span>
                </div>
                <div style="color: #4ADE80; font-family: 'DM Mono', monospace; font-size: 10px; font-weight: 600; letter-spacing: 0.06em; margin-bottom: 12px;">03 &mdash; PLAN</div>
                <div style="color: #F5F0EB; font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 15px; margin-bottom: 8px;">Sprint Plan</div>
                <div style="color: #7A7168; font-family: 'DM Sans', sans-serif; font-size: 12px; line-height: 1.6;">4-week onboarding with velocity tracking</div>
            </div>
        </div>
        <style>
            .feature-card:hover {
                transform: translateY(-4px) !important;
                border-color: rgba(207, 173, 153, 0.25) !important;
                box-shadow: 0 12px 40px rgba(207, 173, 153, 0.1) !important;
            }
        </style>
        <div style="margin-top: 64px;">
            <p style="color: #3D3833; font-family: 'DM Mono', monospace; font-size: 11px; letter-spacing: 0.02em;">Select a sample repo or paste a URL to begin</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
