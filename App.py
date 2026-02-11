import streamlit as st
import joblib
import pandas as pd
import numpy as np
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="WAF Shield | Anomaly Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
if 'bytes_in' not in st.session_state: st.session_state['bytes_in'] = 500
if 'bytes_out' not in st.session_state: st.session_state['bytes_out'] = 2500
if 'dst_port' not in st.session_state: st.session_state['dst_port'] = 80
if 'time_taken' not in st.session_state: st.session_state['time_taken'] = 45
if 'scan_done' not in st.session_state: st.session_state['scan_done'] = False
if 'result' not in st.session_state: st.session_state['result'] = None

# --- Helper Functions ---
def clear_dashboard():
    st.session_state['bytes_in'] = 500
    st.session_state['bytes_out'] = 2500
    st.session_state['dst_port'] = 80
    st.session_state['time_taken'] = 45
    st.session_state['scan_done'] = False
    st.session_state['result'] = None

# --- Custom CSS Styling ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #00ffcc; }
    
    .stNumberInput > div > div > input { 
        background-color: #1a1d24; 
        color: #00ffcc; 
        border: 1px solid #00ffcc; 
        text-align: center; 
        font-size: 16px;
    }
    
    .main-header {
        color: #00ffcc;
        font-family: 'Segoe UI', sans-serif;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        white-space: nowrap;
        margin-bottom: 5px;
    }
    
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 16px;
        margin-bottom: 20px;
    }
    
    .cyber-container { 
        background-color: #131720; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #00ffcc; 
        border-right: 5px solid #00ffcc; 
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.1); 
        margin-bottom: 20px; 
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .stButton > button {
        height: 50px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
    }

    .stButton button[kind="primary"] {
        background: linear-gradient(90deg, #008f7a, #00ffcc) !important;
        color: #000000 !important;
        border: none !important;
    }
     .stButton button[kind="primary"]:hover {
         box-shadow: 0 0 20px rgba(0, 255, 204, 0.6) !important;
         transform: scale(1.02);
     }

    .stButton button[kind="secondary"] {
        background-color: transparent;
        border: 1px solid #00ffcc;
        color: #00ffcc;
    }
    
    .success-box { padding: 20px; background-color: rgba(0, 255, 127, 0.1); border: 1px solid #00ff7f; border-radius: 10px; color: #00ff7f; text-align: center; }
    .error-box { padding: 20px; background-color: rgba(255, 69, 58, 0.1); border: 1px solid #ff453a; border-radius: 10px; color: #ff453a; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- Load Model & Artifacts ---
@st.cache_resource
def load_artifacts():
    try:
        model = joblib.load('waf_rf_classifier.pkl')
        cols = joblib.load('model_feature_columns.pkl')
        return model, cols
    except FileNotFoundError:
        return None, None

model, model_columns = load_artifacts()

# --- Sidebar ---
with st.sidebar:
    # Center alignment layout
    c_left, c_center, c_right = st.columns([1, 2, 1])
    with c_center:
        st.image("https://cdn-icons-png.flaticon.com/512/2716/2716612.png", width=120)
    
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>WAF Shield v1.0</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center;'>
        <b>System Status:</b><br>
        Engine: <b>Hybrid (AI+Heuristic)</b><br>
        Status: 🟢 <b>Online</b><br>
        Threshold: 🎯 <b>50%</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # TIP BOX (Blue)
    st.markdown("""
    <div style="text-align: center; padding: 10px; border-radius: 5px; background-color: rgba(33, 150, 243, 0.2); border-left: 5px solid #2196F3; color: white;">
        ℹ️ <b>Tip:</b> Use 'Reset' To Clear All Fields.
    </div>
    """, unsafe_allow_html=True)

# --- Main Layout ---
st.markdown('<div class="main-header">🛡️ Network Traffic Analysis Console</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-time Anomaly Detection System (WAF Engine)</div>', unsafe_allow_html=True)

# --- Input Section ---
st.markdown('<div class="cyber-container">', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### 📥 Inbound Traffic")
    st.number_input("Bytes Received", min_value=0, key='bytes_in')

with c2:
    st.markdown("#### 📤 Outbound Traffic")
    st.number_input("Bytes Sent", min_value=0, key='bytes_out')

st.markdown("<br>", unsafe_allow_html=True) 

c3, c4 = st.columns(2)
with c3:
    st.markdown("#### 🌐 Target Port")
    st.number_input("Destination Port", min_value=0, step=1, key='dst_port')

with c4:
    st.markdown("#### ⏱️ Latency")
    st.number_input("Response Time (ms)", min_value=0, key='time_taken')

st.markdown('</div>', unsafe_allow_html=True)

# --- Control Buttons ---
col_spacer_left, col_scan, col_reset, col_spacer_right = st.columns([2.5, 2, 1, 2.5])

with col_scan:
    scan_clicked = st.button("🚀 INITIATE SCAN", type="primary", use_container_width=True)

with col_reset:
    clear_clicked = st.button("🔄 RESET", on_click=clear_dashboard, type="secondary", use_container_width=True)

# --- Execution Logic ---
if scan_clicked:
    if model and model_columns:
        with st.spinner('Scanning traffic signatures...'):
            time.sleep(0.8)
            
            try:
                input_df = pd.DataFrame(columns=model_columns)
                input_df.loc[0] = 0
                
                if 'bytes_in' in input_df: input_df['bytes_in'] = st.session_state['bytes_in']
                if 'bytes_out' in input_df: input_df['bytes_out'] = st.session_state['bytes_out']
                if 'dst_port' in input_df: input_df['dst_port'] = st.session_state['dst_port']
                if 'time' in input_df: input_df['time'] = st.session_state['time_taken']
                
                pred = model.predict(input_df)[0]
                proba = model.predict_proba(input_df)[0]
                suspicious_conf = proba[1]
                
                # Hybrid Rule: Force alert on high volume
                is_rule_triggered = False
                if st.session_state['bytes_in'] > 10000 or st.session_state['bytes_out'] > 10000:
                    pred = 1
                    suspicious_conf = 0.99
                    is_rule_triggered = True
                
                st.session_state['scan_done'] = True
                st.session_state['result'] = {
                    'pred': pred,
                    'conf': suspicious_conf,
                    'rule': is_rule_triggered
                }
                
            except Exception as e:
                st.error(f"Error: {e}")

# --- Output Display ---
if st.session_state['scan_done'] and st.session_state['result']:
    res = st.session_state['result']
    st.markdown("---")
    
    col_res_space1, col_res_main, col_res_space2 = st.columns([1, 4, 1])
    
    with col_res_main:
        # Determine Source Message
        source_msg = "Heuristic Rule Engine (Abnormal Data Volume)" if res['rule'] else "ML Anomaly Model"

        if res['pred'] == 1:
            # SUSPICIOUS
            st.markdown(f"""
                <div class="error-box">
                    <h2>🚨 THREAT DETECTED</h2>
                    <p style="font-size: 18px;">Suspicious Activity Flagged in Network Request.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # --- UPDATED DETECTION SOURCE BOX (CENTERED & VISIBLE) ---
            st.markdown(f"""
            <div style="
                text-align: center; 
                padding: 12px; 
                border-radius: 8px; 
                background-color: rgba(33, 150, 243, 0.3); 
                border: 1px solid #2196F3; 
                color: #ffffff; 
                font-size: 16px; 
                margin-top: 15px; 
                margin-bottom: 15px;">
                ℹ️ <b>Detection Source:</b> {source_msg}
            </div>
            """, unsafe_allow_html=True)
            
            cr1, cr2 = st.columns([3, 1])
            cr1.progress(float(res['conf']), text=f"Threat Confidence: {res['conf']*100:.2f}%")
            cr2.metric("Risk Level", "CRITICAL", delta="High Risk", delta_color="inverse")
            
            with st.expander("🔻 View Recommended Actions (High Priority)", expanded=True):
                st.markdown("""
                Based On Analysis Indicating High Data Volume Anomalies:
                1.  **Immediate Block:** Block The Source IP Address.
                2.  **Check for Data Exfiltration:** Investigate Outbound Transfers.
                3.  **Apply Rate Limiting:** Mitigate Potential DDoS Attacks.
                4.  **Notify SOC:** Elevate Incident To Security Operations Center.
                """)
                
        else:
            # NORMAL
            normal_conf = 1 - res['conf']
            st.markdown(f"""
                <div class="success-box">
                    <h2>✅ TRAFFIC IS SAFE</h2>
                    <p style="font-size: 18px;">No Anomalies Detected. Request Authorized.</p>
                </div>
                """, unsafe_allow_html=True)
                
            # --- UPDATED DETECTION SOURCE BOX (CENTERED & VISIBLE) ---
            st.markdown(f"""
            <div style="
                text-align: center; 
                padding: 12px; 
                border-radius: 8px; 
                background-color: rgba(33, 150, 243, 0.3); 
                border: 1px solid #2196F3; 
                color: #ffffff; 
                font-size: 16px; 
                margin-top: 15px; 
                margin-bottom: 15px;">
                ℹ️ <b>Detection Source:</b> {source_msg}
            </div>
            """, unsafe_allow_html=True)
            
            cr1, cr2 = st.columns([3, 1])
            cr1.progress(float(normal_conf), text=f"Safety Confidence: {normal_conf*100:.2f}%")
            cr2.metric("Risk Level", "LOW", delta="Safe")
            
            with st.expander("🔹 View System Actions (Safe Traffic)", expanded=True):
                 st.markdown("""
                 **Standard Protocols:**
                 1.  **Allow Traffic:** Permit Packet To Proceed.
                 2.  **Log Event:** Record Transaction For Auditing.
                 3.  **No Action Required:** Continue Routine Monitoring.
                 """)