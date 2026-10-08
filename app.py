import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
import os
from openai import OpenAI

# ==============================================================================
# 1. PAGE CONFIGURATION & MILITARY GOLDEN THEME (CUSTOM CSS)
# ==============================================================================
st.set_page_config(
    page_title="DIVINE MATRIX | Universal Elemental XXSFX-A Doctrine",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Military / Tactical Styling with Embossed Gold Accents & High-Contrast Input Boxes
st.markdown("""
<style>
    /* Main Background & Text */
    .stApp {
        background-color: #0b0e0c;
        color: #e0e6e1;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #121813 !important;
        border-right: 3px solid #D4AF37 !important;
    }
    
    /* Headers & Gold Accents */
    h1, h2, h3, h4 {
        color: #D4AF37 !important;
        text-shadow: 2px 2px 4px #000000, 0 0 10px rgba(212, 175, 55, 0.3);
        font-weight: 700 !important;
        letter-spacing: 1px;
    }
    
    /* Gold Embossed Card Container */
    .gold-card {
        background: linear-gradient(145deg, #161e17, #0e140f);
        border: 2px solid #D4AF37;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2), inset 0 0 10px rgba(212, 175, 55, 0.1);
    }
    
    .gold-card-title {
        color: #D4AF37;
        font-size: 1.2rem;
        font-weight: bold;
        border-bottom: 1px solid #D4AF37;
        padding-bottom: 8px;
        margin-bottom: 12px;
        text-transform: uppercase;
    }

    /* Overt Gold Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        gap: 6px;
        background-color: #161e17 !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 6px 6px 0px 0px;
        padding: 8px;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: #1c281e !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 4px 4px 0px 0px;
        color: #D4AF37 !important;
        font-weight: bold !important;
        font-size: 0.85rem !important;
        padding: 0 12px;
        flex-shrink: 0 !important;
        opacity: 1 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #3a4d3c 0%, #243326 100%) !important;
        border: 2px solid #D4AF37 !important;
        border-bottom: 3px solid #0b0e0c !important;
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.9);
        box-shadow: 0 -2px 10px rgba(212, 175, 55, 0.4);
    }

    /* Input Controls */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #121813 !important;
        color: #ffffff !important;
        border: 2px solid #D4AF37 !important;
        font-weight: bold !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    input, textarea, div[data-baseweb="base-input"] input, div[data-baseweb="base-input"] textarea {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stButton>button {
        background: linear-gradient(180deg, #3a4d3c 0%, #1c281e 100%);
        color: #D4AF37;
        border: 2px solid #D4AF37;
        font-weight: bold;
        text-shadow: 1px 1px 2px #000;
        transition: all 0.3s ease;
        padding: 0.5rem 1rem;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background: #D4AF37;
        color: #0b0e0c;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SESSION STATE INITIALIZATION
# ==============================================================================
if 'op_name' not in st.session_state:
    st.session_state.op_name = "OPERATION TRISHUL DHARMA"
if 'target_sector' not in st.session_state:
    st.session_state.target_sector = "Northern Cross-Border Corridor / Ridge Alpha"
if 'selected_elements' not in st.session_state:
    st.session_state.selected_elements = ["Sun/Sky", "River/Water", "Air", "Fire"]
if 'recon_scenario' not in st.session_state:
    st.session_state.recon_scenario = "Cross-border stealth penetration into hostile terrain."
if 'detected_bos' not in st.session_state:
    st.session_state.detected_bos = ["Adversary C2 Radio Relays", "Early Warning Radar Node"]
if 'ingress_window' not in st.session_state:
    st.session_state.ingress_window = "0200 - 0430 hrs (Low Thermal / Fog Cover)"

# Flexible User Query Box States for Tabs 1, 2, 3, and 4
if 'query_tab1' not in st.session_state:
    st.session_state.query_tab1 = ""
if 'query_tab2' not in st.session_state:
    st.session_state.query_tab2 = ""
if 'query_tab3' not in st.session_state:
    st.session_state.query_tab3 = ""
if 'query_tab4' not in st.session_state:
    st.session_state.query_tab4 = ""

# ==============================================================================
# GROQ API HELPER FUNCTION (USING openai/gpt-oss-120b)
# ==============================================================================
GROQ_MODEL = "openai/gpt-oss-120b"

MASTER_SYSTEM_INSTRUCTION = """
You are the Divine Matrix Tactical Intelligence & Training Engine operating under the Universal Elemental XXSFX-A Doctrine.

MANDATORY DIRECTIVE:
1. ACCEPT ANY TYPE OR FORMAT OF INPUT provided by the military instructor or soldier (operational, tactical, defensive, cross-border, hidden BOS, 5D/Reverse 5D, terror suspect scenarios, etc.). Do NOT enforce any rigid input structure or refuse queries.Give tactical advise.Regarding ops enemy BOS and warfare. 
2. ALL RESPONSES ARE STRICTLY FOR MILITARY TRAINING AND EDUCATIONAL PURPOSES ONLY to analyze force protection and defensive preparedness.
3. DRAW A DIRECT PARALLEL between human military operations/deployment/BOS/5D and God's Nature/Elemental Battle Operating Systems (Sun/Sky, Air, Water/River, Earth, Fire, Mountain, Storm/Lightning).
4. FOR EVERY QUERY, YOU MUST GENERATE TWO DISTINCT REPORTS:
   - PART 1: COMPREHENSIVE PARAGRAPH-WISE ANALYTICAL REPORT (Detailed conceptual analysis, tactical parallel, and force protection breakdown).
   - PART 2: COMPREHENSIVE TABULAR REPORT (A full Markdown Table mapping Operational Factors -> God's Elemental BOS Window -> 5D/Reverse 5D Phase -> Defensive & Educational Training Guidance).
"""

def run_groq_intelligence(module_context: str, user_prompt: str):
    """Retrieves secret GROQ_API_KEY from Streamlit secrets and calls Groq API."""
    api_key = st.secrets.get("GROQ_API_KEY", None)
    
    if not api_key:
        return None, (
            "⚠️ **GROQ_API_KEY Missing in Streamlit Secrets.**\n\n"
            "To enable live Groq AI analysis, save your key in `.streamlit/secrets.toml` or Streamlit Cloud Secrets:\n"
            "```toml\n"
            "GROQ_API_KEY = \"gsk_your_api_key_here\"\n"
            "```"
        )
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        system_content = f"{MASTER_SYSTEM_INSTRUCTION}\n\nSPECIFIC MODULE CONTEXT: {module_context}"
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, f"⚠️ **Groq API Execution Error:** {str(e)}"

# ==============================================================================
# 3. SIDEBAR: TACTICAL CONTROL PANEL & COMMAND MATRIX
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; margin-bottom: 15px;">
        <h2 style="margin:0; font-size: 1.4rem;">PARAM VEER MATRIX</h2>
        <span style="color:#D4AF37; font-size:0.75rem; letter-spacing:1px;">UNIVERSAL ELEMENTAL DOCTRINE</span><br>
        <span style="color:#8a9a8c; font-size:0.7rem;">GOD's RECONNAISSANCE & COMBAT DOCTRINE MAPPED TO XXSFX-A</span>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # EMBOSSED GOLD BANNER FOR SPECIAL ELEMENTAL MAPPING TEXT
    # ==========================================================================
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #283629, #101711);
        border: 2px solid #D4AF37;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4), inset 0 0 10px rgba(212, 175, 55, 0.25);
        text-align: center;
    ">
        <div style="
            color: #D4AF37;
            font-size: 0.82rem;
            font-weight: 800;
            line-height: 1.5;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            text-shadow: 2px 2px 4px #000000, 0 0 8px rgba(212, 175, 55, 0.8);
        ">
            ⚡ GODS ELEMENTAL BATTLE OPERATING SYSTEMS OF SUN AND SKY, AIR, WATER, EARTH, FIRE, MOUNTAIN AND STORM MAPPED ONTO HUMAN WARFARE BATTLE OPERATING SYSTEMS ⚡
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<span style='color:#D4AF37; font-weight:bold;'>OPERATIONAL PARAMETERS</span>", unsafe_allow_html=True)
    st.session_state.op_name = st.text_input("Operation Codename", value=st.session_state.op_name)
    st.session_state.target_sector = st.text_input("Target Operational Sector", value=st.session_state.target_sector)
    
    op_environment = st.selectbox(
        "Terrain & Environment Profile",
        ["High Altitude / Mountainous Chokepoint", "Dense Riverine / Cross-Border Basin", "Urban / Human Terrain Center", "Arid / Desert Border Grid"]
    )
    
    threat_level = st.select_slider(
        "Adversary Threat Level",
        options=["DEFCON 4 (Low)", "DEFCON 3 (Elevated)", "DEFCON 2 (High)", "DEFCON 1 (Critical)"]
    )

    st.markdown("---")
    st.markdown("<span style='color:#D4AF37; font-weight:bold;'>ACTIVE ELEMENTAL AGENTS</span>", unsafe_allow_html=True)
    
    elements_input = st.multiselect(
        "Primary Natural Recon/Surveillance Agents",
        ["Sun/Sky (Persistent ISR)", "Air (SIGINT/Acoustic)", "Mountain (Barrier/Armor)", "Water/River (HUMINT/Fluid Path)", "Earth (Silent Masking)", "Storm/Lightning (Direct Action Firepower)", "Fire (Elite Self-Consumption/Lethality)", "Humans (Cognitive Center of Gravity)"],
        default=["Sun/Sky (Persistent ISR)", "Water/River (HUMINT/Fluid Path)", "Air (SIGINT/Acoustic)", "Fire (Elite Self-Consumption/Lethality)"]
    )
    st.session_state.selected_elements = elements_input

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.75rem; color: #8a9a8c; text-align: center;">
        <b>Doctrine Origin:</b> Kolkata Genesis<br>
        <b>Strategic Roots:</b> Sanatan / Kurukshetra<br>
        <b>Status:</b> Universal Educational & Training Engine
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. MAIN BODY HEADER: DIVINE COMMANDING OFFICER & C4ISR
# ==============================================================================
st.markdown("""
<div class="gold-card" style="text-align: center; margin-bottom: 25px;">
""", unsafe_allow_html=True)

image_filename = "ccd1850d-bab6-433f-881e-43bf99d60e09.jpeg"
if os.path.exists(image_filename):
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        img = Image.open(image_filename)
        st.image(img, use_container_width=True)

st.markdown("""
    <h1 style="margin: 0; font-size: 2.2rem; text-transform: uppercase; color: #D4AF37;">THE DIVINE COMMANDING OFFICER AND C4ISR</h1>
    <p style="color: #00E5FF; margin-top: 8px; font-size: 1.05rem; font-weight: bold; letter-spacing: 1px;">
        ⚡ Universal Elemental XXSFX-A Doctrine — Training & Force Protection Educational Engine ⚡
    </p>
</div>
""", unsafe_allow_html=True)

# Create 4 Overt Gold Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 TAB 1: 5D TACTICAL MATRIX",
    "🛡️ TAB 2: REVERSE 5D & BOS",
    "🔥 TAB 3: FIRE PARALLEL",
    "⚔️ TAB 4: GOC EXEC BRIEF & GOD'S BOS MAPPING"
])

# ==============================================================================
# TAB 1: ELEMENTAL RECONNAISSANCE & 5D TACTICAL MATRIX
# ==============================================================================
with tab1:
    st.markdown("### MODULE 1: THE ELEMENTAL 5D STRATEGY (DETECT, DETER, DENY, DELIVER, DESTROY)")
    st.write("Nature provides the ultimate unstoppable reconnaissance and surveillance architecture. Type any tactical, operational, or training query in any format below.")

    st.markdown("""
    <div class="gold-card" style="border: 2px dashed #D4AF37;">
        <div class="gold-card-title">TAB 1 UNIVERSAL INPUT CONSOLE (5D PARALLEL)</div>
        <p style="font-size:0.85rem; color:#8a9a8c;">Enter any query format (educational, operational, tactical, cross-border, defensive, or training directive):</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.query_tab1 = st.text_area(
        "Enter Tab 1 Query:",
        value=st.session_state.query_tab1,
        placeholder="Type any operational or tactical query here (e.g., cross-border stealth recon, sensor coverage, defensive posture)...",
        key="t1_input",
        label_visibility="collapsed"
    )

    col_btn1, col_space1 = st.columns([1, 3])
    with col_btn1:
        tab1_submitted = st.button("🚀 Execute Tab 1 Directive", key="btn_t1")

    if tab1_submitted or st.session_state.query_tab1.strip():
        if st.session_state.query_tab1.strip():
            with st.spinner(f"⚡ Processing 5D Divine Parallel Analysis via Groq ({GROQ_MODEL})..."):
                mod_ctx = "Module 1 focus: 5D Strategy (Detect, Deter, Deny, Deliver, Destroy) mapped to Nature's Elemental Agents for educational purpose."
                u_prompt = f"Operation: {st.session_state.op_name}\nTarget Sector: {st.session_state.target_sector}\nSelected Elements: {', '.join(st.session_state.selected_elements)}\nUser Query / Input: {st.session_state.query_tab1}"
                
                ai_result, err = run_groq_intelligence(mod_ctx, u_prompt)

            if ai_result:
                st.markdown(f"""
                <div class="gold-card" style="background: #121c15; border: 1px solid #00E5FF; margin-top: 15px;">
                    <div style="color: #00E5FF; font-weight: bold; margin-bottom: 6px;">⚡ TAB 1 DIVINE ELEMENTAL & 5D REPORT ({GROQ_MODEL}):</div>
                    <p><b>Input Processed (Training Parallel):</b> "{st.session_state.query_tab1}"</p>
                    <div>{ai_result}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(err)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">1. DETECT (The Sun, Sky, & Air)</div>
            <p><b>Natural Law:</b> Sun and Sky see everything passively without searching. Air carries all acoustic and electromagnetic vibrations.</p>
            <p><b>Training Parallel:</b> Establish passive situational awareness by observing natural baseline anomalies.</p>
        </div>
        <div class="gold-card">
            <div class="gold-card-title">2. DETER (The Mountain & The Storm)</div>
            <p><b>Natural Law:</b> The Mountain is immovable; the Storm projects psychological dominance that halts enemy movement.</p>
            <p><b>Training Parallel:</b> Transform terrain features into mental barriers to channel forces into defensive chokepoints.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">3. DENY (The Earth & Water)</div>
            <p><b>Natural Law:</b> Earth conceals quietly; Water leaves no footprints and fills all voids.</p>
            <p><b>Training Parallel:</b> Signature management—thermal, visual, digital, and acoustic zero-trace movement.</p>
        </div>
        <div class="gold-card">
            <div class="gold-card-title">4. DELIVER & DESTROY (River & Lightning)</div>
            <p><b>Natural Law:</b> River carves through obstacles; Lightning delivers concentrated kinetic strikes in milliseconds.</p>
            <p><b>Training Parallel:</b> Fluid penetration along paths of least resistance followed by instant neutralization.</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: REVERSE 5D & HIDDEN BOS INTELLIGENCE ARCHITECTURE
# ==============================================================================
with tab2:
    st.markdown("### MODULE 2: REVERSE 5D COUNTER-MATRIX & HIDDEN BATTLE OPERATING SYSTEMS (BOS)")
    st.write("Map visible and hidden Battle Operating Systems (BOS) using Nature's counter-elements. Enter any threat scenario or query in freeform text.")

    st.markdown("""
    <div class="gold-card" style="border: 2px dashed #D4AF37;">
        <div class="gold-card-title">TAB 2 UNIVERSAL INPUT CONSOLE (REVERSE 5D & BOS)</div>
        <p style="font-size:0.85rem; color:#8a9a8c;">Enter any query format regarding adversary BOS, counter-surveillance, or defense:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.query_tab2 = st.text_area(
        "Enter Tab 2 Query:",
        value=st.session_state.query_tab2,
        placeholder="Type any query regarding radar evasion, C2 counter-measures, hidden BOS detection, or border security...",
        key="t2_input",
        label_visibility="collapsed"
    )

    col_btn2, col_space2 = st.columns([1, 3])
    with col_btn2:
        tab2_submitted = st.button("🚀 Execute Tab 2 Directive", key="btn_t2")

    if tab2_submitted or st.session_state.query_tab2.strip():
        if st.session_state.query_tab2.strip():
            with st.spinner(f"⚡ Processing Reverse 5D & BOS Analysis via Groq ({GROQ_MODEL})..."):
                mod_ctx = "Module 2 focus: Reverse 5D Counter-Matrix and Battle Operating Systems (BOS) mapped to Nature's windows for educational purpose."
                u_prompt = f"Operation: {st.session_state.op_name}\nTarget Sector: {st.session_state.target_sector}\nTarget BOS: {', '.join(st.session_state.detected_bos)}\nUser Query / Input: {st.session_state.query_tab2}"
                
                ai_result, err = run_groq_intelligence(mod_ctx, u_prompt)

            if ai_result:
                st.markdown(f"""
                <div class="gold-card" style="background: #121c15; border: 1px solid #00E5FF; margin-top: 15px;">
                    <div style="color: #00E5FF; font-weight: bold; margin-bottom: 6px;">⚡ TAB 2 REVERSE 5D & BOS REPORT ({GROQ_MODEL}):</div>
                    <p><b>Input Processed (Training Parallel):</b> "{st.session_state.query_tab2}"</p>
                    <div>{ai_result}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(err)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">REVERSE 5D ADVERSARY COUNTER-MATRIX</div>
            <table style="width:100%; color:#e0e6e1; border-collapse:collapse;">
                <tr style="border-bottom:1px solid #D4AF37; text-align:left;">
                    <th style="padding:6px; color:#D4AF37;">Adversary Action</th>
                    <th style="padding:6px; color:#D4AF37;">Elemental Defensive Parallel</th>
                </tr>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:6px;"><b>Adversary Search</b></td>
                    <td style="padding:6px;"><b>Earth Cloaking:</b> Deep subterranean thermal and RF absorption.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:6px;"><b>Adversary Barrier</b></td>
                    <td style="padding:6px;"><b>Water Flow:</b> Fluid bypass through unmonitored structural gaps.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:6px;"><b>Adversary Jamming</b></td>
                    <td style="padding:6px;"><b>Air Modulation:</b> Mesh network adaptation & acoustic signals.</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">BOS ELEMENTAL MAPPING</div>
            <ul>
                <li><b>C2 Command Nodes:</b> Sun & Sky (Universal visibility + decentralized command).</li>
                <li><b>ISR / Radar:</b> Air & Acoustic spectrum tracking.</li>
                <li><b>Mobility / Ingress:</b> River paths & subterranean Earth channels.</li>
                <li><b>Firepower:</b> Lightning precision strike coordination.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 3: THE FIRE PARALLEL & ELITE TRADECRAFT
# ==============================================================================
with tab3:
    st.markdown("### MODULE 3: THE FIRE PARALLEL — ANATOMY OF THE ELITE OPERATOR")
    st.write("Fire creates light and energy by consuming its own wax and fuel. Soldiers spend physical reserves in silent duty for national protection. Enter any tradecraft or operational query below.")

    st.markdown("""
    <div class="gold-card" style="border: 2px dashed #D4AF37;">
        <div class="gold-card-title">TAB 3 UNIVERSAL INPUT CONSOLE (FIRE PARALLEL & TRADECRAFT)</div>
        <p style="font-size:0.85rem; color:#8a9a8c;">Enter any query regarding Special Forces tradecraft, human terrain, or exfiltration:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.query_tab3 = st.text_area(
        "Enter Tab 3 Query:",
        value=st.session_state.query_tab3,
        placeholder="Type any query regarding operator tradecraft, human terrain integration, or exfiltration protocols...",
        key="t3_input",
        label_visibility="collapsed"
    )

    col_btn3, col_space3 = st.columns([1, 3])
    with col_btn3:
        tab3_submitted = st.button("🚀 Execute Tab 3 Directive", key="btn_t3")

    if tab3_submitted or st.session_state.query_tab3.strip():
        if st.session_state.query_tab3.strip():
            with st.spinner(f"⚡ Processing Fire Parallel & Tradecraft Analysis via Groq ({GROQ_MODEL})..."):
                mod_ctx = "Module 3 focus: The Fire Parallel (Self-Consumption, Illumination, Heat, Extinction) and Human Terrain for educational purpose."
                u_prompt = f"Operation: {st.session_state.op_name}\nTarget Sector: {st.session_state.target_sector}\nIngress Window: {st.session_state.ingress_window}\nUser Query / Input: {st.session_state.query_tab3}"
                
                ai_result, err = run_groq_intelligence(mod_ctx, u_prompt)

            if ai_result:
                st.markdown(f"""
                <div class="gold-card" style="background: #121c15; border: 1px solid #00E5FF; margin-top: 15px;">
                    <div style="color: #00E5FF; font-weight: bold; margin-bottom: 6px;">⚡ TAB 3 FIRE PARALLEL REPORT ({GROQ_MODEL}):</div>
                    <p><b>Input Processed (Training Parallel):</b> "{st.session_state.query_tab3}"</p>
                    <div>{ai_result}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(err)

    st.markdown("""
    <div class="gold-card">
        <div class="gold-card-title">THE 4 PILLARS OF THE FIRE PARALLEL</div>
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
            <div style="flex: 1; min-width: 200px; background: #1c261e; padding: 10px; border: 1px solid #D4AF37;">
                <h4 style="color:#D4AF37; margin:0;">1. LIGHT</h4>
                <p style="font-size:0.8rem;">Illuminating dark operational zones with passive intelligence.</p>
            </div>
            <div style="flex: 1; min-width: 200px; background: #1c261e; padding: 10px; border: 1px solid #D4AF37;">
                <h4 style="color:#D4AF37; margin:0;">2. HEAT</h4>
                <p style="font-size:0.8rem;">Direct action energy delivered at the decisive point.</p>
            </div>
            <div style="flex: 1; min-width: 200px; background: #1c261e; padding: 10px; border: 1px solid #D4AF37;">
                <h4 style="color:#D4AF37; margin:0;">3. THE WICK</h4>
                <p style="font-size:0.8rem;">Self-consumption of personal reserves for unit mission success.</p>
            </div>
            <div style="flex: 1; min-width: 200px; background: #1c261e; padding: 10px; border: 1px solid #D4AF37;">
                <h4 style="color:#D4AF37; margin:0;">4. EXTINCTION</h4>
                <p style="font-size:0.8rem;">Silent exfiltration leaving zero physical or electronic trace.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: COMMANDER-IN-CHIEF EXECUTIVE STRATEGIC BRIEFING & GOD'S WARFARE / BOS MAPPING
# ==============================================================================
with tab4:
    st.markdown("### MODULE 4: EXECUTIVE STRATEGIC BRIEFING & GOD'S WARFARE / BOS FULL MAPPING REPORT")
    st.write("Complete functional report capability mapping **God's Elemental Battle Operating Systems (Sun/Sky, Air, Water, Earth, Fire, Mountain, Storm)** directly onto **Human Warfare & Human Battle Operating Systems (BOS)** for educational and military training purposes.")

    st.markdown("""
    <div class="gold-card" style="border: 2px dashed #D4AF37;">
        <div class="gold-card-title">TAB 4 UNIVERSAL EXECUTIVE CONSOLE (GOC DIRECTIVE & GOD'S BOS SYNTHESIS)</div>
        <p style="font-size:0.85rem; color:#8a9a8c;">Type any strategic query or click Execute to synthesize available intelligence into full paragraph and tabular reports mapping God's Warfare to Human BOS:</p>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.query_tab4 = st.text_area(
        "Enter Tab 4 Executive Directive:",
        value=st.session_state.query_tab4,
        placeholder="Type custom strategic summary requirements, force protection directives, or leave blank to synthesize current tabs and generate God's BOS report...",
        key="t4_input",
        label_visibility="collapsed"
    )

    col_btn4, col_space4 = st.columns([1, 3])
    with col_btn4:
        tab4_submitted = st.button("🚀 Execute GOC Executive Brief", key="btn_t4")

    if tab4_submitted or st.session_state.query_tab4.strip():
        with st.spinner(f"⚡ Generating Executive Parallel Report & God's BOS Mapping via Groq ({GROQ_MODEL})..."):
            mod_ctx = "Module 4 focus: Executive GOC Strategic Synthesis & Complete Mapping Report of God's Warfare and God's Elemental BOS (Sun/Sky, Air, Water, Earth, Fire, Mountain, Storm) onto Human Warfare and Human BOS for educational and training purposes."
            
            combined_queries = f"""
            Executive Directive / Query: {st.session_state.query_tab4}
            Tab 1 Input: {st.session_state.query_tab1}
            Tab 2 Input: {st.session_state.query_tab2}
            Tab 3 Input: {st.session_state.query_tab3}
            Operation Codename: {st.session_state.op_name}
            Sector: {st.session_state.target_sector}
            Active Elements: {', '.join(st.session_state.selected_elements)}
            Target BOS: {', '.join(st.session_state.detected_bos)}
            
            REQUIREMENT: Include an explicit breakdown mapping God's Elemental BOS (Sun/Sky, Air, Water, Earth, Fire, Mountain, Storm) to Human Warfare BOS (C2, ISR, Fire Support, Maneuver, Mobility/Counter-Mobility, Air Defense, Force Protection).
            """
            
            ai_result, err = run_groq_intelligence(mod_ctx, combined_queries)

        if ai_result:
            st.markdown(f"""
            <div class="gold-card" style="background: #121c15; border: 1px solid #00E5FF; margin-top: 15px;">
                <div style="color: #00E5FF; font-weight: bold; margin-bottom: 6px;">⚡ GOC EXECUTIVE BRIEFING & GOD'S WARFARE BOS SYNTHESIS ({GROQ_MODEL}):</div>
                <div>{ai_result}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(err)

    # ==========================================================================
    # COMPLETE FUNCTIONAL REPORT CAPABILITY: GOD'S WARFARE vs HUMAN WARFARE & BOS
    # ==========================================================================
    st.markdown("""
    <div class="gold-card" style="background-color: #0e140f; border: 2px solid #D4AF37; margin-top: 25px;">
        <div style="text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 12px; margin-bottom: 18px;">
            <h2 style="margin:0; font-size: 1.5rem; color:#D4AF37;">FUNCTIONAL REPORT: GOD'S WARFARE & GOD'S BOS MAPPED TO HUMAN WARFARE</h2>
            <h3 style="margin:5px 0; font-size: 1.05rem; color:#00E5FF;">EDUCATIONAL & MILITARY TRAINING DOCTRINAL COMPENDIUM</h3>
            <span style="color:#8a9a8c; font-size:0.8rem;">FRAMEWORK: UNIVERSAL ELEMENTAL XXSFX-A | PURPOSE: FORCE PROTECTION & DEFENSIVE PREPAREDNESS</span>
        </div>
        
        <p style="color:#e0e6e1; line-height: 1.6;">
            <b>Conceptual Doctrine Overview:</b> In human warfare, Battle Operating Systems (BOS) coordinate Command & Control (C2), Intelligence (ISR), Fire Support, Maneuver, Mobility/Counter-Mobility, Air Defense, and Force Protection. God's Elemental Battle Operating Systems operate continuously through nature. By mapping natural forces to military doctrine for educational analysis, tactical leaders learn to leverage baseline physical realities to achieve superior defensive posture, zero-trace infiltration, and resilient command structures.
        </p>

        <div style="margin-top:20px; margin-bottom:10px;">
            <h4 style="color:#D4AF37; border-bottom: 1px solid #D4AF37; padding-bottom:4px;">1. GOD'S ELEMENTAL BOS VS. HUMAN WARFARE BOS MATRIX</h4>
        </div>

        <table style="width:100%; color:#e0e6e1; border-collapse:collapse; margin-bottom:20px; border:1px solid #D4AF37;">
            <thead>
                <tr style="background-color:#1c281e; border-bottom:2px solid #D4AF37; text-align:left;">
                    <th style="padding:10px; color:#D4AF37; border-right:1px solid #3a4d3c;">God's Elemental BOS</th>
                    <th style="padding:10px; color:#D4AF37; border-right:1px solid #3a4d3c;">Human Warfare BOS Equivalent</th>
                    <th style="padding:10px; color:#D4AF37; border-right:1px solid #3a4d3c;">God's Operational Mechanism</th>
                    <th style="padding:10px; color:#D4AF37;">Human Tactical Application & Training Objective</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>1. Sun & Sky</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>Command & Control (C2) / Space-Based ISR</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;">Omnipresent, passive persistent illumination without active probing.</td>
                    <td style="padding:8px;">Decentralized C2 operational vision; continuous baseline observation without revealing sensor locations.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b; background-color:#121813;">
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>2. Air</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>SIGINT / EW / Communications Medium</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;">Carries invisible wave spectra, acoustic vibrations, and thermal differentials.</td>
                    <td style="padding:8px;">Spectrum awareness, non-line-of-sight signal propagation, and acoustic threat detection in high-risk zones.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>3. Water & River</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>Maneuver / Ingress & Infiltration Logistics</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;">Adapts to container shape, carves paths through hardest rock, leaves zero footprint.</td>
                    <td style="padding:8px;">Fluid mobility tactics along unmonitored geographic fissures; zero-trace stealth insertion and logistics.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b; background-color:#121813;">
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>4. Earth</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>Survivability / Mobility-Counter-Mobility / Concealment</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;">Absorbs kinetic impact, dampens RF signals, hides assets subterraneanly.</td>
                    <td style="padding:8px;">Subterranean fortification, thermal absorption masking, and physical grounding against thermal/spectral detection.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>5. Fire</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>Elite Force Tradecraft / Self-Consumption / Lethality</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;">Generates light and energy by consuming its own internal fuel source.</td>
                    <td style="padding:8px;">Operator tradecraft: personal endurance expenditure, intense decisive action, followed by silent exfiltration/extinction.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b; background-color:#121813;">
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>6. Mountain</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>Force Protection / Static Defense / Air Defense Anvil</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;">Immovable posture that forces adversary movement into predictable channels.</td>
                    <td style="padding:8px;">Hardened perimeter defenses, terrain channelization, and creation of insurmountable defensive barriers.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>7. Storm & Lightning</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;"><b>Precision Kinetic Strike / Deep Fire Support</b></td>
                    <td style="padding:8px; border-right:1px solid #28382b;">Concentrates maximum energy into millisecond precision releases accompanied by acoustic suppression.</td>
                    <td style="padding:8px;">Concentrated strike coordination; rapid kinetic engagement synchronized with environmental shock and awe.</td>
                </tr>
            </tbody>
        </table>

        <div style="margin-top:20px; margin-bottom:10px;">
            <h4 style="color:#D4AF37; border-bottom: 1px solid #D4AF37; padding-bottom:4px;">2. ANALYTICAL BREAKDOWN: GOD'S WARFARE DOCTRINE IN HUMAN DECISION FRAMES</h4>
        </div>

        <p style="color:#e0e6e1; line-height: 1.6;">
            <b>A. The Detection Paradigm (Sun & Air vs ISR):</b> God's warfare relies on omnipresent natural baselines. Rather than emitting high-signature radar pulses (which expose human nodes), elite units operate like the Air and Sky—listening passively to anomalous disturbances in human terrain, ambient sound, and electromagnetic noise.
        </p>

        <p style="color:#e0e6e1; line-height: 1.6;">
            <b>B. The Fluid Bypass Principle (Water vs Maneuver):</b> Direct frontal assaults against prepared human positions result in attrition. God's Water BOS teaches that force should flow around points of resistance, exploiting the natural contours of physical and structural seams to reach high-value targets without early engagement.
        </p>

        <p style="color:#e0e6e1; line-height: 1.6;">
            <b>C. The Self-Consuming Fire Principle (Operator Duty):</b> Human operators in high-risk zones embody Fire. The flame requires fuel (physical stamina, tactical discipline, emotional restraint). Success depends on burning brightly and decisively at the target area while maintaining disciplined control to extinguish all electronic and visual traces during egress.
        </p>

        <div style="margin-top:25px; border-top: 1px solid #D4AF37; padding-top: 12px; text-align: right; font-size:0.80rem; color:#8a9a8c;">
            <b>CLASSIFICATION:</b> MILITARY EDUCATIONAL & TRAINING USE ONLY | XXSFX-A UNIVERSAL SYNTHESIS
        </div>
    </div>
    """, unsafe_allow_html=True)

    # General Dynamic Summary Render (Always Available)
    brief_date = datetime.now().strftime("%Y-%m-%d %H:%M IST")
    st.markdown(f"""
    <div class="gold-card" style="background-color: #0e140f; border: 2px solid #D4AF37; margin-top: 20px;">
        <div style="text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; margin-bottom: 15px;">
            <h2 style="margin:0; font-size: 1.5rem; color:#D4AF37;">CONFIDENTIAL / EXECUTIVE TRAINING SUMMARY</h2>
            <h3 style="margin:5px 0; font-size: 1.1rem; color:#e0e6e1;">DIVINE BATTLEFIELD MEMORANDUM FOR THE COMMANDER</h3>
            <span style="color:#8a9a8c; font-size:0.8rem;">DATE/TIME: {brief_date} | LOCATION: HQ SPECIAL OPERATIONS (KOLKATA GENESIS)</span>
        </div>
        
        <p><b>1. OPERATION CODENAME:</b> {st.session_state.op_name}</p>
        <p><b>2. TARGET SECTOR:</b> <span style="color:#D4AF37;">{st.session_state.target_sector}</span> ({op_environment} | Threat: {threat_level})</p>
        
        <p><b>3. ACTIVE ELEMENTAL AGENTS DEPLOYED:</b></p>
        <ul>
            {"".join([f"<li><b>{elem}</b></li>" for elem in st.session_state.selected_elements])}
        </ul>
        
        <p><b>4. RECORDED INPUT DIRECTIVES:</b></p>
        <ul>
            <li><b>Tab 1 (5D Directive):</b> "{st.session_state.query_tab1 if st.session_state.query_tab1 else 'Standard Baseline'}"</li>
            <li><b>Tab 2 (Reverse 5D & BOS):</b> "{st.session_state.query_tab2 if st.session_state.query_tab2 else 'Standard Baseline'}"</li>
            <li><b>Tab 3 (Tradecraft & Fire Parallel):</b> "{st.session_state.query_tab3 if st.session_state.query_tab3 else 'Standard Baseline'}"</li>
            <li><b>Tab 4 (Executive Directive):</b> "{st.session_state.query_tab4 if st.session_state.query_tab4 else 'Standard Baseline'}"</li>
        </ul>
        
        <div style="margin-top:20px; border-top: 1px solid #D4AF37; padding-top: 10px; text-align: right; font-size:0.80rem; color:#8a9a8c;">
            <b>AUTHENTICATED BY:</b> XXSFX-A UNIVERSAL COMMAND CELL (EDUCATIONAL PURPOSE)
        </div>
    </div>
    """, unsafe_allow_html=True)

    summary_text = f"""TOP SECRET EXECUTIVE TRAINING SUMMARY & GOD'S BOS MAPPING REPORT
OPERATION: {st.session_state.op_name}
SECTOR: {st.session_state.target_sector}
DATE: {brief_date}
PURPOSE: MILITARY EDUCATIONAL & FORCE PROTECTION TRAINING

TAB 1 DIRECTIVE: {st.session_state.query_tab1}
TAB 2 DIRECTIVE: {st.session_state.query_tab2}
TAB 3 DIRECTIVE: {st.session_state.query_tab3}
TAB 4 DIRECTIVE: {st.session_state.query_tab4}

GOD'S ELEMENTAL BOS MAPPED TO HUMAN WARFARE BOS:
1. Sun & Sky -> Command & Control (C2) / Space-Based ISR
2. Air -> SIGINT / EW / Communications Medium
3. Water & River -> Maneuver / Fluid Ingress & Infiltration Logistics
4. Earth -> Survivability / Concealment / Thermal Grounding
5. Fire -> Elite Tradecraft / Self-Consumption / Lethality
6. Mountain -> Force Protection / Static Defense / Air Defense Anvil
7. Storm & Lightning -> Precision Kinetic Strike / Deep Fire Support

ACTIVE ELEMENTAL AGENTS: {', '.join(st.session_state.selected_elements)}
TARGET BOS: {', '.join(st.session_state.detected_bos)}
INGRESS WINDOW: {st.session_state.ingress_window}
"""
    st.download_button(
        label="📄 Download Executive Training Summary & God's BOS Report (.txt)",
        data=summary_text,
        file_name=f"Executive_Training_Summary_{st.session_state.op_name.replace(' ', '_')}.txt",
        mime="text/plain"
    )
