# from fastapi import FastAPI
# import uvicorn

# app = FastAPI()

# @app.get("/")
# def demo():
#     return {"message":"Hello I am demo, i just made a change"}

# if __name__ == "__main__":
#     uvicorn.run(app=app,port=5000,host="0.0.0.0")

import sys
import os
import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ── Fix: ensure project root is on sys.path so `src` is importable ───────────
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Churn ML Platform",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Global Reset & Base */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
.stApp {
    background: #0f172a !important; /* Tailwind Slate 900 */
    font-family: 'Inter', sans-serif;
    color: #f8fafc;
}

/* Hide defaults */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stMainBlockContainer"],
section.main > div { background: transparent !important; }

/* ── Hero Banner ── */
.hero {
    background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
    border: 1px solid #312e81;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}
.hero-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.02em;
    margin-bottom: 0.2rem;
}
.hero-title span {
    background: linear-gradient(to right, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 500;
    letter-spacing: 0.05em;
}
.hero-badge {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    color: #818cf8;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #1e293b;
    padding: 0;
    gap: 2rem;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: none !important;
    padding: 1rem 0 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #c084fc !important;
    border-bottom: 2px solid #c084fc !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display: none !important; }

/* ── Section labels ── */
.sec-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94a3b8;
    margin-bottom: 1rem;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 0.4rem;
}

/* ── Step cards (pipeline) ── */
.step-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: all 0.2s ease;
}
.step-card.running { border-color: #818cf8; box-shadow: 0 0 15px rgba(129, 140, 248, 0.15); }
.step-card.done { border-color: #10b981; }
.step-card.error { border-color: #ef4444; }

.step-icon { 
    font-size: 1.4rem; 
    width: 36px; 
    height: 36px; 
    background: #0f172a; 
    border-radius: 8px; 
    display: flex; 
    align-items: center; 
    justify-content: center;
}
.step-name { font-weight: 600; font-size: 0.9rem; color: #cbd5e1; flex: 1; }
.step-name.active { color: #f8fafc; }

.step-badge {
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
}
.b-wait    { background: #0f172a; color: #64748b; }
.b-running { background: rgba(129, 140, 248, 0.15); color: #818cf8; }
.b-done    { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.b-error   { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

/* ── Log box ── */
.log-box {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.25rem;
    font-size: 0.8rem;
    line-height: 1.6;
    color: #94a3b8;
    min-height: 250px;
    max-height: 380px;
    overflow-y: auto;
    font-family: 'JetBrains Mono', monospace;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
}
.log-box .ts   { color: #475569; margin-right: 0.5rem; }
.log-box .info { color: #818cf8; }
.log-box .ok   { color: #10b981; }
.log-box .err  { color: #ef4444; }
.log-box .dim  { color: #475569; }

/* ── Metric boxes ── */
.metric-row { display: flex; gap: 1rem; margin-top: 1.5rem; }
.metric-box {
    flex: 1;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-val {
    font-size: 1.75rem;
    font-weight: 700;
    color: #c084fc;
}
.metric-lbl {
    font-size: 0.7rem;
    color: #94a3b8;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.25rem;
}

/* ── Result cards ── */
.result-churn {
    background: linear-gradient(180deg, rgba(127, 29, 29, 0.2) 0%, #0f172a 100%);
    border: 1px solid #7f1d1d;
    border-top: 4px solid #ef4444;
    border-radius: 16px;
    padding: 2.5rem 1.5rem;
    text-align: center;
}
.result-loyal {
    background: linear-gradient(180deg, rgba(20, 83, 45, 0.2) 0%, #0f172a 100%);
    border: 1px solid #14532d;
    border-top: 4px solid #10b981;
    border-radius: 16px;
    padding: 2.5rem 1.5rem;
    text-align: center;
}
.result-idle {
    background: #1e293b;
    border: 1px dashed #475569;
    border-radius: 16px;
    padding: 2.5rem 1.5rem;
    text-align: center;
}
.result-icon  { font-size: 3rem; margin-bottom: 0.5rem; }
.result-label { font-size: 1.5rem; font-weight: 700; color: #f8fafc; }
.result-sub   { font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem; }

/* ── Widgets & Inputs ── */
[data-testid="stSelectbox"] > div > div,
[data-baseweb="select"] > div,
[data-baseweb="input"] > div,
[data-testid="stNumberInput"] input {
    background: #0f172a !important;
    border: 1px solid #334155 !important;
    color: #f8fafc !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
}
[data-testid="stSelectbox"] > div > div:focus-within,
[data-baseweb="input"] > div:focus-within {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 1px #818cf8 !important;
}
label, [data-testid="stWidgetLabel"] p {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #cbd5e1 !important;
}

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(to right, #6366f1, #8b5cf6);
    color: white;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.1s;
}
div[data-testid="stButton"] > button:hover { opacity: 0.9; transform: translateY(-1px); }
div[data-testid="stButton"] > button:disabled {
    background: #334155; color: #94a3b8; transform: none; cursor: not-allowed;
}
hr { border-color: #334155 !important; margin: 2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div>
        <div class="hero-title">Churn <span>ML</span> Platform</div>
        <div class="hero-sub">End-to-End Training Pipeline & Inference Engine</div>
    </div>
    <div class="hero-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
        System Ready
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_pipeline, tab_predict = st.tabs(["⚙️ Pipeline Operations", "🔮 Predict Churn"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
with tab_pipeline:

    STEPS = [
        {"key": "ingest",   "icon": "📥", "label": "Data Ingestion",   "desc": "Fetch source data from GitHub"},
        {"key": "process",  "icon": "🔧", "label": "Data Processing",  "desc": "Clean and engineer features"},
        {"key": "train",    "icon": "🧠", "label": "Model Training",   "desc": "Fit the machine learning model"},
        {"key": "evaluate", "icon": "📊", "label": "Model Evaluation", "desc": "Calculate core metrics"},
    ]

    if "step_states" not in st.session_state:
        st.session_state.step_states = {s["key"]: "waiting" for s in STEPS}
    if "logs" not in st.session_state:
        st.session_state.logs = []
    if "pipe_running" not in st.session_state:
        st.session_state.pipe_running = False
    if "elapsed" not in st.session_state:
        st.session_state.elapsed = 0

    def pipe_reset():
        st.session_state.step_states = {s["key"]: "waiting" for s in STEPS}
        st.session_state.logs = []
        st.session_state.pipe_running = False
        st.session_state.elapsed = 0

    def ts():
        return datetime.now().strftime("%H:%M:%S")

    def add_log(msg, kind="dim"):
        st.session_state.logs.append(
            f'<span class="ts">[{ts()}]</span> <span class="{kind}">{msg}</span>'
        )

    pcol1, pcol2 = st.columns([1, 1.4], gap="large")

    with pcol1:
        st.markdown('<div class="sec-label">Execution Flow</div>', unsafe_allow_html=True)
        steps_ph = st.empty()

        def render_steps():
            html = ""
            for s in STEPS:
                state = st.session_state.step_states[s["key"]]
                card_cls = f"step-card {state if state != 'waiting' else ''}"
                name_cls = "step-name active" if state in ("running", "done", "error") else "step-name"
                badge_map = {
                    "waiting": '<span class="step-badge b-wait">Pending</span>',
                    "running": '<span class="step-badge b-running">Processing...</span>',
                    "done":    '<span class="step-badge b-done">Completed</span>',
                    "error":   '<span class="step-badge b-error">Failed</span>',
                }
                html += f"""
                <div class="{card_cls}">
                    <div class="step-icon">{s['icon']}</div>
                    <div class="{name_cls}">{s['label']}<br>
                        <span style="font-size:0.7rem;color:#64748b;font-weight:400;">{s['desc']}</span>
                    </div>
                    {badge_map[state]}
                </div>"""
            steps_ph.markdown(html, unsafe_allow_html=True)

        render_steps()

        metrics_ph = st.empty()

        def render_metrics():
            done_n = sum(1 for v in st.session_state.step_states.values() if v == "done")
            pct    = int(done_n / len(STEPS) * 100)
            metrics_ph.markdown(f"""
            <div class="metric-row">
                <div class="metric-box"><div class="metric-val">{done_n}/{len(STEPS)}</div><div class="metric-lbl">Steps Done</div></div>
                <div class="metric-box"><div class="metric-val">{pct}%</div><div class="metric-lbl">Progress</div></div>
                <div class="metric-box"><div class="metric-val">{st.session_state.elapsed}s</div><div class="metric-lbl">Elapsed</div></div>
            </div>""", unsafe_allow_html=True)

        render_metrics()
        st.markdown("<hr>", unsafe_allow_html=True)

        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            run_pipe_btn = st.button("▶ Run Pipeline", disabled=st.session_state.pipe_running, key="run_pipe")
        with btn_c2:
            if st.button("↺ Reset State", key="reset_pipe", disabled=st.session_state.pipe_running):
                pipe_reset()
                st.rerun()

    with pcol2:
        st.markdown('<div class="sec-label">System Logs</div>', unsafe_allow_html=True)
        log_ph = st.empty()

        def render_logs():
            content = "\n".join(st.session_state.logs) if st.session_state.logs \
                else '<span class="dim">Waiting for execution to begin...</span>'
            log_ph.markdown(f'<div class="log-box">{content}</div>', unsafe_allow_html=True)

        render_logs()

    # ── Pipeline execution ────────────────────────────────────────────────────
    def run_step(key, label):
        st.session_state.step_states[key] = "running"
        render_steps()
        add_log(f"Initializing {label}...", "info")
        render_logs()
        try:
            if key == "ingest":
                from src.data.ingest import DataIngestion
                DataIngestion().ingest_saved_data_github()
            elif key == "process":
                from src.data.preprocess import DataProcessing
                DataProcessing().FeatureEngineering()
            elif key == "train":
                from src.models.train import ModelTraining
                ModelTraining().train_model()
            elif key == "evaluate":
                from src.models.evaluate import ModelEvaluation
                ModelEvaluation().evaluate_model()
            
            st.session_state.step_states[key] = "done"
            add_log(f"Successfully completed {label}", "ok")
            return True
        except Exception as e:
            st.session_state.step_states[key] = "error"
            add_log(f"Execution failed in {label}: {e}", "err")
            return False

    if run_pipe_btn:
        pipe_reset()
        st.session_state.pipe_running = True
        t0 = time.time()
        add_log("----------------------------------------", "dim")
        add_log("Pipeline Execution Started", "info")
        add_log("----------------------------------------", "dim")
        render_logs()

        step_fns = [
            ("ingest",   "DataIngestion.ingest_saved_data_github()"),
            ("process",  "DataProcessing.FeatureEngineering()"),
            ("train",    "ModelTraining.train_model()"),
            ("evaluate", "ModelEvaluation.evaluate_model()"),
        ]

        success = True
        for key, lbl in step_fns:
            st.session_state.elapsed = int(time.time() - t0)
            render_metrics()
            ok = run_step(key, lbl)
            st.session_state.elapsed = int(time.time() - t0)
            render_steps()
            render_metrics()
            render_logs()
            if not ok:
                success = False
                break

        st.session_state.pipe_running = False
        add_log("----------------------------------------", "dim")
        add_log(
            f"Pipeline terminated. Total time: {st.session_state.elapsed}s" if success
            else "Pipeline aborted due to critical error.",
            "ok" if success else "err"
        )
        add_log("----------------------------------------", "dim")
        render_logs()
        render_steps()
        render_metrics()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PREDICT
# ══════════════════════════════════════════════════════════════════════════════
with tab_predict:

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown('<div class="sec-label">Demographics & Plan</div>', unsafe_allow_html=True)
        gender     = st.selectbox("Gender", ["Male", "Female"])
        senior     = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner    = st.selectbox("Has Partner", ["Yes", "No"])
        dependents = st.selectbox("Has Dependents", ["Yes", "No"])
        tenure     = st.slider("Tenure (months)", 0, 72, 12)

        st.markdown('<div class="sec-label" style="margin-top:1.5rem;">Billing Information</div>', unsafe_allow_html=True)
        contract  = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment   = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)"
        ])
        monthly = st.number_input("Monthly Charges ($)", 0.0, 200.0, 65.0, 0.5)
        total   = st.number_input("Total Charges ($)",   0.0, 10000.0, 780.0, 10.0)

    with col2:
        st.markdown('<div class="sec-label">Services Configuration</div>', unsafe_allow_html=True)
        phone      = st.selectbox("Phone Service",   ["Yes", "No"])
        multilines = st.selectbox("Multiple Lines",  ["No", "Yes", "No phone service"])
        
        st.markdown('<br>', unsafe_allow_html=True)
        internet    = st.selectbox("Internet Service",  ["DSL", "Fiber optic", "No"])
        online_sec  = st.selectbox("Online Security",   ["No", "Yes", "No internet service"])
        online_bk   = st.selectbox("Online Backup",     ["Yes", "No", "No internet service"])
        device_prot = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        tech_sup    = st.selectbox("Tech Support",      ["No", "Yes", "No internet service"])
        streaming_tv= st.selectbox("Streaming TV",      ["No", "Yes", "No internet service"])
        streaming_mv= st.selectbox("Streaming Movies",  ["No", "Yes", "No internet service"])

    with col3:
        st.markdown('<div class="sec-label">Inference Engine</div>', unsafe_allow_html=True)
        result_box = st.empty()
        result_box.markdown(
            '<div class="result-idle">'
            '<div class="result-icon">🎯</div>'
            '<div class="result-label" style="color:#94a3b8;font-size:1.2rem;">Ready for Input</div>'
            '<div class="result-sub">Adjust parameters and run inference</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("Run Prediction Model", key="predict_btn")

    if predict_btn:
        input_data = {
            'gender':           gender,
            'SeniorCitizen':    1 if senior == "Yes" else 0,
            'Partner':          partner,
            'Dependents':       dependents,
            'tenure':           tenure,
            'PhoneService':     phone,
            'MultipleLines':    multilines,
            'InternetService':  internet,
            'OnlineSecurity':   online_sec,
            'OnlineBackup':     online_bk,
            'DeviceProtection': device_prot,
            'TechSupport':      tech_sup,
            'StreamingTV':      streaming_tv,
            'StreamingMovies':  streaming_mv,
            'Contract':         contract,
            'PaperlessBilling': paperless,
            'PaymentMethod':    payment,
            'MonthlyCharges':   monthly,
            'TotalCharges':     total,
        }
        df_input = pd.DataFrame([input_data])

        with st.spinner("Executing model..."):
            try:
                from src.models.predict import Prediction
                predictor = Prediction()
                processed = predictor.preprocessing(df_input.copy())
                yp = predictor.model.predict(processed)[0]

                if yp == 1:
                    result_box.markdown("""
                    <div class="result-churn">
                        <div class="result-icon">⚠️</div>
                        <div class="result-label">High Risk</div>
                        <div class="result-sub">Customer is likely to churn</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    result_box.markdown("""
                    <div class="result-loyal">
                        <div class="result-icon">✅</div>
                        <div class="result-label">Low Risk</div>
                        <div class="result-sub">Customer is likely to remain</div>
                    </div>""", unsafe_allow_html=True)

            except Exception as e:
                result_box.error(f"Prediction execution failed: {e}")

        display_df = df_input.astype(str).T.rename(columns={0: "Value"})