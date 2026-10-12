import streamlit as st
from research_agent import generate_brief, save_brief

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="✦",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #10213f;
        --muted: #65728b;
        --blue: #3568f5;
        --blue-dark: #1e43b7;
        --line: #e6ebf5;
        --surface: #ffffff;
    }

    .stApp {
        background:
            radial-gradient(circle at 4% 0%, rgba(72, 130, 255, .16), transparent 26rem),
            radial-gradient(circle at 96% 9%, rgba(152, 92, 255, .12), transparent 24rem),
            #f7f9fd;
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    .block-container {
        max-width: 1180px;
        padding: 2.8rem 2rem 5rem;
    }

    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { visibility: hidden; }

    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        padding: 2.5rem 2.7rem 2.35rem;
        color: white;
        background: linear-gradient(116deg, #102653 0%, #1d47ad 58%, #447ff7 100%);
        box-shadow: 0 20px 50px rgba(35, 70, 150, .2);
        animation: rise-in .65s ease-out both;
    }

    .hero:before, .hero:after {
        content: "";
        position: absolute;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,.16);
        pointer-events: none;
    }
    .hero:before { width: 320px; height: 320px; right: -80px; top: -170px; }
    .hero:after { width: 260px; height: 260px; right: 80px; bottom: -205px; }
    .hero-content { position: relative; z-index: 1; }
    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: .5rem;
        color: #cfe0ff;
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .13em;
        text-transform: uppercase;
    }
    .pulse {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #8dffcc;
        box-shadow: 0 0 0 0 rgba(141,255,204,.7);
        animation: pulse 2s infinite;
    }
    .hero h1 {
        margin: .75rem 0 .55rem;
        color: #fff;
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(2rem, 5vw, 3.25rem);
        letter-spacing: -.055em;
        line-height: 1.04;
    }
    .hero p { max-width: 570px; margin: 0; color: #d9e5ff; font-size: 1.04rem; }

    .section-label {
        margin: 2.25rem 0 .8rem;
        color: var(--ink);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
    }
    .section-label span { color: var(--blue); }
    .notice {
        display: flex;
        gap: .8rem;
        align-items: flex-start;
        margin: 1.25rem 0 1.7rem;
        padding: 1rem 1.1rem;
        border: 1px solid #dce8ff;
        border-radius: 15px;
        color: #405170;
        background: rgba(238,245,255,.85);
        font-size: .9rem;
        line-height: 1.5;
    }
    .notice-icon { color: var(--blue); font-size: 1.1rem; line-height: 1.2; }

    [data-testid="stTextInput"] label {
        color: var(--ink);
        font-weight: 700;
    }
    [data-testid="stFileUploader"] label {
        color: var(--ink);
        font-weight: 700;
    }
    [data-testid="stFileUploaderDropzone"] {
        min-height: 108px;
        border: 1px dashed #b8c8e9;
        border-radius: 12px;
        background: rgba(255,255,255,.75);
    }
    [data-testid="stFileUploaderDropzone"] button {
        color: var(--blue) !important;
        background: #edf2ff !important;
        border: 1px solid #c5d5fb !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    [data-testid="stFileUploaderDropzone"] button:hover {
        background: #dce8ff !important;
        border-color: var(--blue) !important;
    }
    [data-testid="stTextInput"] input {
        height: 3.25rem;
        border: 1px solid #d9e1f0;
        border-radius: 12px;
        color: var(--ink);
        background: var(--surface);
        box-shadow: 0 4px 15px rgba(30, 54, 103, .04);
        transition: border-color .2s ease, box-shadow .2s ease, transform .2s ease;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #5a83f8;
        box-shadow: 0 0 0 4px rgba(53,104,245,.12);
        transform: translateY(-1px);
    }
    .stButton > button, .stDownloadButton > button {
        min-height: 3.25rem;
        border-radius: 12px;
        font-weight: 700;
        transition: transform .2s ease, box-shadow .2s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(46, 88, 196, .18);
    }
    .stButton > button[kind="primary"] {
        border: 0;
        background: linear-gradient(135deg, #3568f5, #264bc8);
    }
    .result-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-top: 2.4rem;
        padding: 1.2rem 1.4rem;
        border: 1px solid var(--line);
        border-bottom: 0;
        border-radius: 18px 18px 0 0;
        background: var(--surface);
    }
    .result-heading h2 {
        margin: 0;
        color: var(--ink);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
    }
    .ticker-badge {
        padding: .4rem .7rem;
        border-radius: 999px;
        color: #2854ce;
        background: #edf2ff;
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .08em;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--line);
        border-radius: 0 0 18px 18px;
        background: var(--surface);
        box-shadow: 0 12px 30px rgba(38, 59, 107, .06);
        animation: rise-in .55s ease-out both;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 1.8rem 2rem;
    }
    .report-card h1, .report-card h2, .report-card h3 { color: var(--ink); font-family: 'Space Grotesk', sans-serif; }
    .report-card a { color: var(--blue); }
    .footer-note { margin-top: 2rem; color: #8a95a8; font-size: .78rem; text-align: center; }

    @keyframes rise-in { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(141,255,204,.7); } 70% { box-shadow: 0 0 0 8px rgba(141,255,204,0); } 100% { box-shadow: 0 0 0 0 rgba(141,255,204,0); } }
    @media (max-width: 640px) {
        .block-container { padding: 1.2rem 1rem 3rem; }
        .hero { padding: 1.8rem 1.4rem; border-radius: 20px; }
        .report-card { padding: 1.2rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <div class="hero-content">
            <div class="eyebrow"><span class="pulse"></span> Evidence-led intelligence</div>
            <h1>AI Research Agent</h1>
            <p>Turn your research pack into a clear, source-backed company brief in seconds.</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="notice"><span class="notice-icon">ⓘ</span><span>'
    "This agent analyzes only the documents you provide. "
    "It does not independently verify company information."
    "</span></div>",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">Start a <span>new brief</span></div>', unsafe_allow_html=True)
input_col, documents_col = st.columns([1, 1], vertical_alignment="bottom")
with input_col:
    ticker = (
        st.text_input(
            "Company ticker",
            value="SRVCABLE",
            help="Enter the ticker you want the agent to analyze.",
            placeholder="e.g. SRVCABLE",
        )
        .strip()
        .upper()
    )
with documents_col:
    uploaded_files = st.file_uploader(
        "Company documents",
        type=["md", "txt", "pdf"],
        accept_multiple_files=True,
        help="Upload one or more source documents. Uploaded files replace the local research pack for this brief.",
    )

if uploaded_files:
    st.caption(
        f"✦ {len(uploaded_files)} document(s) ready: "
        + ", ".join(file.name for file in uploaded_files)
    )
else:
    st.caption("Using documents from the local research_pack folder.")

generate = st.button("✦  Generate brief", type="primary", use_container_width=True)

if generate:
    if not ticker:
        st.warning("Please enter a company ticker.")
    else:
        try:
            with st.spinner("✦  Reading documents and generating your brief..."):
                uploaded_content = (
                    [(file.name, file.getvalue()) for file in uploaded_files]
                    if uploaded_files
                    else None
                )
                report = generate_brief(ticker, uploaded_content)

            if report.strip():
                saved_path = save_brief(ticker, report)
                st.session_state["report"] = report
                st.session_state["ticker"] = ticker
                st.session_state["saved_path"] = str(saved_path)
            else:
                st.error("The model returned an empty response.")

        except Exception as exc:
            st.error(f"Request failed: {exc}")

if st.session_state.get("report"):
    report = st.session_state["report"]
    report_ticker = st.session_state.get("ticker", ticker)

    st.markdown(
        f"""
        <div class="result-heading">
            <h2>Research brief</h2>
            <span class="ticker-badge">{report_ticker}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown(report)

    download_col, _ = st.columns([1, 3])
    with download_col:
        st.download_button(
            label="↓  Download report",
            data=report,
            file_name=f"{report_ticker.lower()}_research_brief.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.caption(f"Exact response saved to `{st.session_state.get('saved_path', 'generated_briefs')}`")
    st.text_area(
        "Exact generated brief (copy this unchanged for submission)",
        value=report,
        height=420,
        disabled=True,
    )

    st.markdown(
        '<div class="footer-note">Built for thoughtful research, grounded in your evidence.</div>',
        unsafe_allow_html=True,
    )
