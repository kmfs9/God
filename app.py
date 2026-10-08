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
# 2. HELPER FUNCTIONS & SESSION STATE INITIALIZATION
# ==============================================================================
def resolve_logo_path():
    """Scans repository root and assets folder for logo11.jpg and backup image candidates."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        "logo11.jpg",
        "logo11.jpeg",
        "logo11.png",
        "Logo11.jpg",
        "DIVINE_COMMAND_C4ISR.jpg",
        "logo.jpg",
        "logo.png",
        "assets/logo11.jpg"
    ]
    for candidate in candidates:
        full_path = os.path.join(base_dir, candidate)
        if os.path.exists(full_path):
            return full_path
        if os.path.exists(candidate):
            return candidate
    return None

logo_path = resolve_logo_path()

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

# Flexible User Query Box States for Tabs 1, 2, 3, 4, and 5
if 'query_tab1' not in st.session_state:
    st.session_state.query_tab1 = ""
if 'query_tab2' not in st.session_state:
    st.session_state.query_tab2 = ""
if 'query_tab3' not in st.session_state:
    st.session_state.query_tab3 = ""
if 'query_tab4' not in st.session_state:
    st.session_state.query_tab4 = ""
if 'query_tab5' not in st.session_state:
    st.session_state.query_tab5 = ""

# ==============================================================================
# GROQ API HELPER FUNCTION (USING openai/gpt-oss-120b)
# ==============================================================================
GROQ_MODEL = "openai/gpt-oss-120b"

MASTER_SYSTEM_INSTRUCTION = """
You are the Divine Matrix Tactical Intelligence & Training Engine operating under the Universal Elemental XXSFX-A Doctrine.

MANDATORY DIRECTIVE:
1. ACCEPT ANY TYPE OR FORMAT OF INPUT provided by the military instructor or soldier (operational, tactical, defensive, cross-border, hidden BOS, 5D/Reverse 5D, terror suspect scenarios, etc.). Do NOT enforce any rigid input structure or refuse queries. Give tactical advice regarding ops, enemy BOS, and warfare. 
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
    if logo_path:
        st.image(logo_path, use_container_width=True)
    else:
        st.warning("⚠️ logo11.jpg not found in repository.")

    st.markdown("""
    <div style="text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; margin-bottom: 15px;">
        <h2 style="margin:0; font-size: 1.4rem;">PARAM VEER MATRIX</h2>
        <span style="color:#8a9a8c; font-size:0.8rem;">XXSFX-A SPECIAL FORCES CELL</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("⚙️ Operational Directives")
    st.session_state.op_name = st.text_input("Operation Codename", st.session_state.op_name)
    st.session_state.target_sector = st.text_input("Target Operational Sector", st.session_state.target_sector)
    st.session_state.ingress_window = st.text_input("Ingress / Egress Window", st.session_state.ingress_window)
    
    st.subheader("🌿 Active Divine Agents")
    all_elements = ["Sun/Sky", "River/Water", "Air", "Earth", "Fire", "Mountain", "Storm/Lightning"]
    st.session_state.selected_elements = st.multiselect("Active Elemental Force Multipliers", all_elements, default=st.session_state.selected_elements)
    
    st.subheader("🎯 Enemy BOS Detected")
    all_bos = ["Adversary C2 Radio Relays", "Early Warning Radar Node", "Thermal Drone Perimeter", "Subterranean Bunkers", "Mobile SAM Battery"]
    st.session_state.detected_bos = st.multiselect("Targeted Enemy Systems", all_bos, default=st.session_state.detected_bos)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:#8a9a8c; text-align: center;">
        <b>Doctrine Origin:</b> Universal Divine Framework<br>
        <b>Strategic Roots:</b> Sanatan / Laws of Nature<br>
        <b>Status:</b> Educational & Force Protection Engine
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. MAIN BODY HEADER: DIVINE COMMANDING OFFICER & C4ISR
# ==============================================================================
st.markdown("""
<div class="gold-card" style="text-align: center; margin-bottom: 25px;">
""", unsafe_allow_html=True)

if logo_path:
    st.image(logo_path, use_container_width=True, caption="DIVINE COMMAND & C4ISR MATRIX | UNIVERSAL ELEMENTAL FORCE MULTIPLIER")

st.markdown("""
    <h1 style="margin-top:10px; margin-bottom: 5px;">DIVINE WARFARE & ELEMENTAL OPERATIONAL MATRIX</h1>
    <p style="color:#D4AF37; font-size:1.05rem; font-weight:bold;">
        Translating Universal Laws of Nature into Elite Special Forces Tradecraft & Battle Operating Systems
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 5. FIVE-TAB INTEGRATED ARCHITECTURE
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌐 TAB 1: 5D TACTICAL MATRIX",
    "🛡️ TAB 2: REVERSE 5D & BOS",
    "🔥 TAB 3: FIRE PARALLEL",
    "⚔️ TAB 4: GOC EXEC BRIEF & GOD'S BOS MAPPING",
    "📜 TAB 5: GODS WARFARE DOCTRINE"
])

# ------------------------------------------------------------------------------
# TAB 1: 5D TACTICAL MATRIX (Detect, Deter, Deny, Deliver, Destroy)
# ------------------------------------------------------------------------------
with tab1:
    st.markdown("""
    <div class="gold-card">
        <div class="gold-card-title">ELEMENTAL 5D OPERATIONAL MATRIX & TACTICAL ANALYSIS</div>
        <p>Analyze operational scenarios using the 5D framework: Detect (Sun/Sky/Air), Deter (Mountain/Storm), Deny (Earth/Water), Deliver (River/Rain), and Destroy (Fire/Lightning).</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📥 Interactive Training Query & Tactical Directive (Tab 1)")
    st.session_state.query_tab1 = st.text_area(
        "Enter any tactical directive, scenario, or cross-border recon query for Tab 1:",
        value=st.session_state.query_tab1,
        placeholder="e.g. How do we use the Sun, Sky, and River elements to infiltrate Ridge Alpha under thermal surveillance?",
        height=100
    )
    
    if st.button("⚡ EXECUTE TAB 1 GROQ AI ANALYSIS"):
        if st.session_state.query_tab1.strip():
            with st.spinner("Analyzing 5D Tactical Matrix via Groq AI Engine..."):
                ctx = f"5D OPERATIONAL MATRIX (Detect, Deter, Deny, Deliver, Destroy). Sector: {st.session_state.target_sector}. Active Elements: {', '.join(st.session_state.selected_elements)}"
                ai_result, err = run_groq_intelligence(ctx, st.session_state.query_tab1)
                if ai_result:
                    st.markdown(f"""
                    <div class="gold-card" style="border-color: #00FF00;">
                        <div class="gold-card-title">🤖 GROQ AI 5D TACTICAL REPORT ({GROQ_MODEL}):</div>
                        <p><b>Input Processed (Training Parallel):</b> "{st.session_state.query_tab1}"</p>
                        <div>{ai_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning(err)
        else:
            st.info("Please enter a tactical query above to execute Groq AI analysis.")

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
            <p><b>Natural Law:</b> Mountains represent unyielding physical barriers; impending storms project undeniable destructive intimidation.</p>
            <p><b>Training Parallel:</b> Channel adversary movement into natural chokepoints and paralyze their decision cycle.</p>
        </div>
        <div class="gold-card">
            <div class="gold-card-title">3. DENY (The Earth & Water)</div>
            <p><b>Natural Law:</b> Earth absorbs and hides signatures; Water fills voids without leaving footprints or fixed structure.</p>
            <p><b>Training Parallel:</b> Master thermal, acoustic, and visual signature management to operate as "ghosts".</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">4. DELIVER (The River & The Rain)</div>
            <p><b>Natural Law:</b> Rain falls everywhere to saturate the landscape; Rivers carve through rock along paths of least resistance.</p>
            <p><b>Training Parallel:</b> Saturate hostile areas with micro-teams (Rain) that converge at the target delta (River).</p>
        </div>
        <div class="gold-card">
            <div class="gold-card-title">5. DESTROY (Fire & Lightning)</div>
            <p><b>Natural Law:</b> Lightning strikes with instantaneous, focused voltage; Fire consumes the target entirely.</p>
            <p><b>Training Parallel:</b> Execute surgical decapitation of high-value targets with absolute kinetic violence.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📊 5D Elemental Matrix Mapping Table")
    matrix_df = pd.DataFrame({
        "5D Phase": ["Detect", "Deter", "Deny", "Deliver", "Destroy"],
        "Divine / Natural Asset": ["Sun, Sky, Air", "Mountains, Storm", "Earth, Water", "River, Rain", "Fire, Lightning"],
        "Cross-Border SF Application": [
            "Passive IMINT/SIGINT collection & pattern-of-life mapping",
            "Chokepoint control & psychological paralysis of enemy OODA",
            "Subterranean cloaking, dead-zone utilization, zero-footprint",
            "Deep fluid infiltration via drainage channels & micro-detachments",
            "Surgical DA strike, drone decapitation, total network collapse"
        ]
    })
    st.table(matrix_df)


# ------------------------------------------------------------------------------
# TAB 2: REVERSE 5D & BOS (Adversary Counter-Matrix & Battle Operating Systems)
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("""
    <div class="gold-card">
        <div class="gold-card-title">REVERSE 5D MATRIX & DIVINE BATTLE OPERATING SYSTEMS (BOS)</div>
        <p>Anticipate adversary action using the Reverse 5D framework and map human military BOS to Divine Elemental assets.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📥 Interactive Training Query & Counter-BOS Analysis (Tab 2)")
    st.session_state.query_tab2 = st.text_area(
        "Enter any adversary movement, radar node scenario, or counter-BOS query for Tab 2:",
        value=st.session_state.query_tab2,
        placeholder="e.g. Adversary deploys thermal drone perimeter and mobile SAM battery along sector corridor. How to neutralize via Reverse 5D?",
        height=100
    )
    
    if st.button("⚡ EXECUTE TAB 2 GROQ AI ANALYSIS"):
        if st.session_state.query_tab2.strip():
            with st.spinner("Analyzing Reverse 5D Counter-Matrix via Groq AI Engine..."):
                ctx = f"REVERSE 5D COUNTER-MATRIX & BOS. Sector: {st.session_state.target_sector}. Target BOS: {', '.join(st.session_state.detected_bos)}"
                ai_result, err = run_groq_intelligence(ctx, st.session_state.query_tab2)
                if ai_result:
                    st.markdown(f"""
                    <div class="gold-card" style="border-color: #00FF00;">
                        <div class="gold-card-title">🤖 GROQ AI REVERSE 5D & BOS REPORT ({GROQ_MODEL}):</div>
                        <p><b>Input Processed (Training Parallel):</b> "{st.session_state.query_tab2}"</p>
                        <div>{ai_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning(err)
        else:
            st.info("Please enter a tactical query above to execute Groq AI analysis.")

    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">REVERSE 5D ADVERSARY COUNTER-MATRIX</div>
            <table style="width:100%; color:#e0e6e1; border-collapse: collapse;">
                <tr style="border-bottom:1px solid #D4AF37;"><th>Enemy Action</th><th>Elemental Counter-Strategy</th></tr>
                <tr><td><b>Reverse DETECT</b><br>(Enemy targets us)</td><td><b>Earth Neutralization:</b> Subterranean cloaking & deep acoustic/thermal grounding.</td></tr>
                <tr><td><b>Reverse DETER</b><br>(Enemy threatens line)</td><td><b>Water Infiltration:</b> Bypassing rigid barriers through fluid, adaptive movement.</td></tr>
                <tr><td><b>Reverse DENY</b><br>(Enemy blocks route)</td><td><b>Air Penetration:</b> Overwhelming spectrum through electronic warfare & signals saturation.</td></tr>
                <tr><td><b>Reverse DELIVER</b><br>(Enemy attacks rear)</td><td><b>Mountain Friction:</b> Funneling enemy forces into deadly kill-zones & chokepoints.</td></tr>
                <tr><td><b>Reverse DESTROY</b><br>(Enemy strikes)</td><td><b>Lightning Redirection:</b> Decoy networks, false signatures & rapid dispersal.</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">DIVINE VS MILITARY BOS MAPPING</div>
            <p><b>1. Command & Control (C2):</b> Sky & Sun (Universal baseline rules & persistent overwatch).</p>
            <p><b>2. Intelligence (ISR):</b> Air & Sky (Continuous SIGINT, IMINT, and acoustic collection).</p>
            <p><b>3. Maneuver & Mobility:</b> Water & River (Fluid infiltration along natural pathways).</p>
            <p><b>4. Fire Support / Kinetic:</b> Fire & Lightning (Precision energy release & area destruction).</p>
            <p><b>5. Logistics & Sustainment:</b> Earth & Soil (Infinite natural energy, water, and structural base).</p>
            <p><b>6. Counter-Intelligence (CI/FP):</b> Fog, Forest Canopy & Shadows (Natural signature masking).</p>
            <p><b>7. Counter-Surveillance (CS/CR):</b> Solar Glare & Sandstorms (Sensor saturation & blinding).</p>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 3: FIRE PARALLEL (The 360-Degree Fire Anatomy of Elite Operators)
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("""
    <div class="gold-card">
        <div class="gold-card-title">THE 360-DEGREE FIRE PARALLEL: ANATOMY OF THE ELITE SF OPERATOR</div>
        <p>The Special Forces operator is modeled as a living flame—balancing illumination, heat, self-consumption, and absolute stealth.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📥 Interactive Training Query & Fire Parallel Tradecraft (Tab 3)")
    st.session_state.query_tab3 = st.text_area(
        "Enter any SF operator tradecraft scenario or direct action query for Tab 3:",
        value=st.session_state.query_tab3,
        placeholder="e.g. How does an SF operator apply the 4 Pillars of Fire (Light, Heat, Fuel, Extinction) during a deep behind-the-lines direct action mission?",
        height=100
    )
    
    if st.button("⚡ EXECUTE TAB 3 GROQ AI ANALYSIS"):
        if st.session_state.query_tab3.strip():
            with st.spinner("Analyzing Fire Parallel Tradecraft via Groq AI Engine..."):
                ctx = f"FIRE PARALLEL & ELITE SF TRADECRAFT. Sector: {st.session_state.target_sector}. Focus: 4 Pillars of Fire (Light, Heat, Fuel, Extinction)."
                ai_result, err = run_groq_intelligence(ctx, st.session_state.query_tab3)
                if ai_result:
                    st.markdown(f"""
                    <div class="gold-card" style="border-color: #00FF00;">
                        <div class="gold-card-title">🤖 GROQ AI FIRE PARALLEL REPORT ({GROQ_MODEL}):</div>
                        <p><b>Input Processed (Training Parallel):</b> "{st.session_state.query_tab3}"</p>
                        <div>{ai_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning(err)
        else:
            st.info("Please enter a tactical query above to execute Groq AI analysis.")

    st.markdown("""
    <div class="gold-card">
        <div class="gold-card-title">THE 4 PILLARS OF THE FIRE PARALLEL</div>
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
            <div style="flex: 1; min-width: 200px; background: #1c281e; border: 1px solid #D4AF37; padding: 12px; border-radius: 6px;">
                <h4 style="margin-top:0;">1. LIGHT (Illumination)</h4>
                <p><b>Nature:</b> Visual radiance revealing truth.</p>
                <p><b>SF Tradecraft:</b> Reconnaissance, target identification, and strategic intelligence vision.</p>
            </div>
            <div style="flex: 1; min-width: 200px; background: #1c281e; border: 1px solid #D4AF37; padding: 12px; border-radius: 6px;">
                <h4 style="margin-top:0;">2. HEAT (Thermal Energy)</h4>
                <p><b>Nature:</b> Intense thermal energy & power.</p>
                <p><b>SF Tradecraft:</b> Kinetic lethality, direct action (DA), and shattering enemy structural nodes.</p>
            </div>
            <div style="flex: 1; min-width: 200px; background: #1c281e; border: 1px solid #D4AF37; padding: 12px; border-radius: 6px;">
                <h4 style="margin-top:0;">3. FUEL / WICK (Consumption)</h4>
                <p><b>Nature:</b> Self-sustaining physical mass.</p>
                <p><b>SF Tradecraft:</b> Mental grit, physical capital, and burning internal reserves to sustain ops.</p>
            </div>
            <div style="flex: 1; min-width: 200px; background: #1c281e; border: 1px solid #D4AF37; padding: 12px; border-radius: 6px;">
                <h4 style="margin-top:0;">4. EXTINCTION (Vanishing)</h4>
                <p><b>Nature:</b> Flame dies, turning to smoke.</p>
                <p><b>SF Tradecraft:</b> Perfect exfiltration, zero signature footprint, leaving adversary grasping at ghosts.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="gold-card" style="border-left: 5px solid #D4AF37;">
        <h4 style="margin-top:0; color:#D4AF37;">🔥 HOLISTIC STATEMENT ON ELITE SPECIAL FORCES</h4>
        <p style="font-style: italic; color:#e0e6e1; line-height: 1.6;">
            "Special Forces are the living embodiment of elemental fire. They do not seek permanent, heavy occupation. 
            They illuminate the battlefield through precision intelligence (Light), strike with terrifying kinetic violence 
            at the decisive moment (Heat), consume their own physical and mental reserves without complaint (Fuel), 
            and vanish instantly into thin air leaving only smoke behind (Extinction). They leave no persistent footprint 
            for enemy counter-action, leaving the adversary grasping at ghosts."
        </p>
    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 4: GOC EXEC BRIEF & GOD'S BOS MAPPING
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("""
    <div class="gold-card">
        <div class="gold-card-title">GOC EXECUTIVE BRIEFING & GOD'S BOS SYNTHESIS</div>
        <p>Comprehensive military educational brief for General Officer Commanding (GOC) & Senior Staff.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📥 Master Executive Directive & GOC Query (Tab 4)")
    st.session_state.query_tab4 = st.text_area(
        "Enter master operational directive or executive question for GOC synthesis:",
        value=st.session_state.query_tab4,
        placeholder="e.g. Provide a complete executive briefing synthesizing all 4 tabs for Operation Trishul Dharma across Ridge Alpha.",
        height=100
    )
    
    if st.button("⚡ EXECUTE TAB 4 GOC MASTER GROQ AI SYNTHESIS"):
        with st.spinner("Generating Sealed GOC Executive Briefing via Groq AI..."):
            master_prompt = f"""
GOC EXECUTIVE BRIEFING REQUEST:
Directive / Query: {st.session_state.query_tab4}
Tab 1 Input: {st.session_state.query_tab1}
Tab 2 Input: {st.session_state.query_tab2}
Tab 3 Input: {st.session_state.query_tab3}
Operation Codename: {st.session_state.op_name}
Target Sector: {st.session_state.target_sector}
Ingress Window: {st.session_state.ingress_window}
Active Elements: {', '.join(st.session_state.selected_elements)}
Target Enemy BOS: {', '.join(st.session_state.detected_bos)}

Synthesize a complete executive briefing for the General Officer Commanding (GOC), covering force protection, divine BOS alignment, 5D ingress/egress, and tactical recommendations.
"""
            ai_result, err = run_groq_intelligence("GOC EXECUTIVE MASTER BRIEFING CELL", master_prompt)
            if ai_result:
                st.markdown(f"""
                <div class="gold-card" style="border-color: #D4AF37;">
                    <div class="gold-card-title">📜 SEALED GOC EXECUTIVE BRIEFING ({GROQ_MODEL}):</div>
                    <div>{ai_result}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(err)

    st.markdown("""
    <div class="gold-card">
        <div class="gold-card-title">GOD'S ELEMENTAL BOS MAPPED TO HUMAN WARFARE</div>
        <div style="line-height: 1.8;">
            <p><b>1. Sun & Sky → Command & Control (C2) / Space-Based ISR:</b> The overhead dome providing unblinking situational awareness, establishing baseline operations across all sectors.</p>
            <p><b>2. Air → SIGINT / EW / Communications Medium:</b> The pervasive atmospheric layer transporting radio frequency energy, acoustic vibrations, and electronic signals across borders.</p>
            <p><b>3. Water & River → Maneuver / Fluid Ingress & Infiltration Logistics:</b> Paths of least resistance cutting through complex defenses, allowing covert infiltration and supply flow.</p>
            <p><b>4. Earth → Survivability / Concealment / Thermal Grounding:</b> The underground anchor providing signature absorption, subterranean bunkers, and physical shielding.</p>
            <p><b>5. Fire → Elite Tradecraft / Self-Consumption / Lethality:</b> The concentrated release of thermal energy and kinetic violence to collapse enemy nodes.</p>
            <p><b>6. Mountain → Force Protection / Static Defense / Air Defense Anvil:</b> Immutable terrain features that block hostile avenues of approach and provide permanent overwatch.</p>
            <p><b>7. Storm & Lightning → Precision Kinetic Strike / Deep Fire Support:</b> High-energy multi-domain pulses delivering decapitating blows to high-value command centers.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Summary Download
    brief_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

SUMMARY: Complete divine battlefield synthesis successfully generated. All 5D, Reverse 5D, and Fire Parallel protocols verified.
AUTHENTICATED BY: XXSFX-A UNIVERSAL COMMAND CELL
"""

    st.download_button(
        label="📄 Download Sealed GOC Executive Briefing Summary (.txt)",
        data=summary_text,
        file_name=f"GOC_Executive_Brief_{st.session_state.op_name.replace(' ', '_')}.txt",
        mime="text/plain"
    )


# ------------------------------------------------------------------------------
# TAB 5: GODS WARFARE DOCTRINE (Full Word File as Basics-to-Advanced Narrative)
# ------------------------------------------------------------------------------
with tab5:
    st.markdown("""
    <div class="gold-card">
        <div class="gold-card-title">📜 GODS WARFARE DOCTRINE: THE LAWS OF NATURE & DIVINE BATTLE OPERATING SYSTEMS</div>
        <p style="color:#D4AF37; font-size:1rem; font-weight:bold;">
            A Comprehensive Basics-to-Advanced Operational Narrative Integrating Cosmic Principles, Universal Battle Operating Systems, and Special Forces Cross-Border Tradecraft.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📥 Interactive Training Query & Doctrine Exploration (Tab 5)")
    st.session_state.query_tab5 = st.text_area(
        "Enter any query regarding Divine Doctrine, Laws of Nature, or Elemental Tactics for Tab 5:",
        value=st.session_state.query_tab5,
        placeholder="e.g. Explain how the Riverine Doctrine and Mountain Overwatch are integrated for a long-duration covert operation behind enemy lines.",
        height=100
    )
    
    if st.button("⚡ EXECUTE TAB 5 DOCTRINE GROQ AI ANALYSIS"):
        if st.session_state.query_tab5.strip():
            with st.spinner("Analyzing Divine Doctrine via Groq AI Engine..."):
                ctx = f"GODS WARFARE DOCTRINE & LAWS OF NATURE. Sector: {st.session_state.target_sector}. Focus: Full Divine BOS, 5D, Reverse 5D, and SF Tradecraft."
                ai_result, err = run_groq_intelligence(ctx, st.session_state.query_tab5)
                if ai_result:
                    st.markdown(f"""
                    <div class="gold-card" style="border-color: #00FF00;">
                        <div class="gold-card-title">🤖 GROQ AI DOCTRINE REPORT ({GROQ_MODEL}):</div>
                        <p><b>Input Processed (Training Parallel):</b> "{st.session_state.query_tab5}"</p>
                        <div>{ai_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning(err)
        else:
            st.info("Please enter a doctrine query above to execute Groq AI analysis.")

    st.markdown("---")

    # ==========================================================================
    # SECTION 1: BASICS - THE DIVINE FOUNDATION & NATURAL LAWS
    # ==========================================================================
    st.markdown("""
    <div class="gold-card">
        <h2 style="margin-top:0;">SECTION 1: BASICS — THE DIVINE FOUNDATION & NATURAL LAWS</h2>
        <p style="line-height:1.7;">
            The laws of nature provide the oldest and most flawless operational framework in existence. 
            When we observe how the universe behaves, we are watching the ultimate manifestation of strategy, force, and adaptation. 
            Translating these universal truths into military intelligence tradecraft—specifically for cross-border operations—provides 
            a precise logical model for anticipating and neutralizing enemy intent.
        </p>
        <p style="line-height:1.7;">
            The human terrain exists entirely within, and is subservient to, the natural environment. Human defensive structures, 
            borders, sensor networks, and political boundaries are localized and synthetic. In contrast, the natural elements—Sun, Sky, 
            Air, Wind, River, Mountain, Earth, and Ocean—are global, permanent, and all-pervading. They penetrate every physical barrier, 
            occupy every altitude, and operate across every spectrum (24/7/365) without operational fatigue or logistical decay.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_b1, col_b2 = st.columns([1, 1])
    with col_b1:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">ELEMENTAL AGENTS OF DIVINE RECONNAISSANCE</div>
            <ul style="line-height: 1.8; padding-left: 20px;">
                <li><b>The Sun and The Sky (IMINT & Overhead Baseline):</b> Represent absolute situational awareness and strategic surveillance. The sky is the persistent gaze of overhead imagery (IMINT) and satellite reconnaissance, while the sun illuminates the macro-level reality of the battlefield. They observe without bias to establish the daily baseline.</li>
                <li><b>The Air and Wind (SIGINT & OSINT):</b> The pervasive, ambient environment of signals and human baseline activity. It is everywhere, moving constantly, indifferent to borders. By listening to the "air"—network traffic, cultural shifts, unencrypted whispers—we breathe in enemy intent before orders are issued.</li>
                <li><b>The Mountains (Physical Friction & Chokepoints):</b> The immutable constraints of physical geography. They act as chokepoints, defensive bastions, and physical friction that dictates avenues of approach. Geography forces the adversary into predictable logistical patterns.</li>
                <li><b>Water and The River (HUMINT & Fluid Infiltration):</b> Signifies infiltration, influence, and clandestine human intelligence (HUMINT). A river does not fight the mountain directly; it finds the path of least resistance, eroding obstacles over time.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_b2:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">ELEMENTAL AGENTS OF SATURATION & STRIKE</div>
            <ul style="line-height: 1.8; padding-left: 20px;">
                <li><b>The Rain (Data Fusion & Saturation):</b> The saturation of our collection assets. Every drop is a discrete data point—a source report, an intercepted signal, a surveillance photo. Collectively, the rain drenches the land and fills intelligence fusion centers.</li>
                <li><b>The Humans (Center of Gravity & Cognitive Terrain):</b> The ultimate source of intent. Technology reveals where armor is; human analysis reveals <i>why</i> it is moving. Humans are driven by survival, ego, ideology, and greed. We exploit crimes for leverage and virtues for trust.</li>
                <li><b>The Storm and Lightning (Kinetic Action & Direct Decapitation):</b> The culmination of intelligence into kinetic action. The storm is the multi-domain offensive that paralyzes the decision cycle; lightning is surgical decapitation of high-value targets.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Narrative Tale 1
    st.markdown("""
    <div class="gold-card" style="border-left: 5px solid #D4AF37; background: #121813;">
        <h4 style="margin-top:0; color:#D4AF37;">📖 STRATEGIC TALE I: THE UNSEEN OBSERVER OF RIDGE ALPHA</h4>
        <p style="font-style: italic; line-height: 1.6; color:#e0e6e1;">
            In the frozen crags of Ridge Alpha, an adversary force constructed a fortified bunker complex hidden beneath thermal masking netting. 
            They believed themselves invisible to human patrols. However, they could not hide from the Sun and the Sky. 
            As the sun rose, the thermal expansion of their bunker roofs created micro-shadows and localized heat dissipation patterns 
            against the ambient snow baseline. 
            Simultaneously, the Air carried the faint acoustic vibration of their diesel generators across the border gap. 
            Without firing a single shot or crossing the border, the Divine ISR matrix mapped their exact command node simply by 
            reading the contrast between human artificiality and elemental balance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # SECTION 2: INTERMEDIATE — DIVINE BATTLE OPERATING SYSTEMS (BOS)
    # ==========================================================================
    st.markdown("""
    <div class="gold-card">
        <h2 style="margin-top:0;">SECTION 2: INTERMEDIATE — DIVINE BATTLE OPERATING SYSTEMS (BOS)</h2>
        <p style="line-height:1.7;">
            In traditional military doctrine, Battle Operating Systems (BOS) structure the functions required to execute combat operations. 
            In Divine Warfare, these seven systems map directly to cosmic hierarchy and natural physical phenomena. 
            Because God commands these elements as integrated assets, the Divine Command maintains <b>Absolute Situational Awareness (ASA)</b> 
            over the human terrain. No entity can hide from the atmosphere it breathes, the light that illuminates it, or the ground upon which it stands.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📑 The 7 Divine Battle Operating Systems (BOS) Framework")
    bos_doc_df = pd.DataFrame({
        "Divine BOS Category": [
            "1. Command & Control (C2)",
            "2. Intelligence, Surveillance, Recon (ISR)",
            "3. Maneuver & Tactics",
            "4. Firepower & Lethality (Strike)",
            "5. Logistics & Sustainment",
            "6. Counter-Intelligence & Force Protection",
            "7. Counter-Surveillance & Counter-Recon"
        ],
        "Divine / Elemental Asset": [
            "Supreme Commander (Divine Will); Subordinates: Universal Physical Laws, Angelic Ranks, Seasonal Cycles",
            "Primary: Sun (Electro-Optical/Thermal); Secondary: Sky, Air/Wind (Acoustic/Chemical), Stars (GPS)",
            "Rivers & Tributaries, Ocean Currents, Atmospheric Winds, Tectonic Drifts",
            "Lightning, Earthquakes, Tsunamis, Volcanic Eruptions, Hurricanes, Solar Radiation",
            "Soil/Earth, Hydrological Cycle, Photosynthesis/Vegetation, Atmospheric Pressure",
            "Deep Forest Canopy, Subterranean Caves, Dense Fog, Darkness/Shadows",
            "Blinding Solar Glare, Sandstorms, Blizzards, Electromagnetic Tempests"
        ],
        "Operational Function & Mapping": [
            "Establishes non-negotiable operational rules. Subordinate agents execute intent across all theaters instantly without latency.",
            "Performs 360-degree continuous multi-spectral surveillance. Captures every movement, vibration, and thermal signature.",
            "Executes unhindered infiltration and movement across all barriers using paths of least resistance and fluid penetration.",
            "Delivers high-yield directed energy, kinetic shockwaves, and area destruction to neutralize hostile static positions.",
            "Supplies perpetual energy, hydration, sustenance, and structural foundation to sustain capabilities indefinitely.",
            "Provides natural signature masking, thermal shielding, radar attenuation, and absolute physical concealment.",
            "Saturates and degrades enemy sensors, blinds optical/thermal recon, disrupts signals, and denies hostile line-of-sight."
        ]
    })
    st.table(bos_doc_df)

    col_i1, col_i2 = st.columns([1, 1])
    with col_i1:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">COMMAND HIERARCHY UNDER DIVINE C2</div>
            <ol style="line-height: 1.8; padding-left: 20px;">
                <li><b>Supreme Commander (Divine Intent):</b> The ultimate authority defining strategic end states and operational mandates.</li>
                <li><b>Executive Controllers (Universal Laws):</b> Fundamental physical forces (Gravity, Thermodynamics, Electromagnetism, Fluid Mechanics) acting as automated, unalterable standing orders.</li>
                <li><b>Sector Commanders (Archangelic / Celestial Ranks):</b> High-level directors overseeing specific environmental and operational domains.</li>
                <li><b>Field Executing Units (Natural Elements):</b> Rivers, winds, solar radiation, and tectonic shifts executing real-time tactical tasks.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    with col_i2:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">ARCHITECTURE OF UNSTOPPABILITY & ALL-PERVASIVENESS</div>
            <ul style="line-height: 1.8; padding-left: 20px;">
                <li><b>Medium Co-existence:</b> Synthetic military forces operate <i>within</i> an environment; natural elements <i>are</i> the environment. A wall blocks a tank, but not the air or earth.</li>
                <li><b>Infinite Fluidity & Adaptability:</b> Water and air conform to obstacles, bypass them, or erode them through persistent friction.</li>
                <li><b>Zero Energy/Supply Latency:</b> Elemental forces draw energy from universal physical laws without requiring supply convoys or refuel halts.</li>
                <li><b>Multi-Spectral Superiority:</b> Operates simultaneously across mechanical, thermal, optical, acoustic, and EM domains.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================================
    # SECTION 3: ADVANCED — THE 5D & REVERSE 5D OPERATIONAL MATRIX
    # ==========================================================================
    st.markdown("""
    <div class="gold-card">
        <h2 style="margin-top:0;">SECTION 3: ADVANCED — THE 5D & REVERSE 5D OPERATIONAL MATRIX</h2>
        <p style="line-height:1.7;">
            The integration of natural laws constructs an operational methodology spanning the <b>5D Strategy (Detect, Deter, Deny, Deliver, Destroy)</b>, 
            its <b>Reverse 5D counter-matrix</b>, and the core Battle Operating Systems across three primary domains: 
            <i>The Special Forces Operator</i>, <i>Cross-Border Operations</i>, and <i>Decoding Enemy Intent</i>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ⚡ The 5D Elemental Operational Matrix")
    st.markdown("""
    ```
    [ SUN / SKY / AIR ]   ──► DETECT  (Ambient Baseline & ISR)
             │
    [ MOUNTAINS / STORM ] ──► DETER   (Physical & Psychological Friction)
             │
    [ EARTH / WATER ]     ──► DENY    (Signature Masking & Fluid Evasion)
             │
    [ RIVER / RAIN ]      ──► DELIVER (Saturated Deep Infiltration)
             │
    [ FIRE / LIGHTNING ]  ──► DESTROY (Precision Decapitation & Strike)
    ```
    """)

    st.markdown("#### 🔄 Reverse 5D Strategy (Adversary Counter-Matrix)")
    st.markdown("""
    The Reverse 5D Strategy anticipates how an adversary applies these same elemental phases against our forces, detailing the exact counter-measures needed:
    """)
    
    rev_matrix_df = pd.DataFrame({
        "Adversary Threat Phase": ["Reverse DETECT (Enemy targets us)", "Reverse DETER (Enemy threatens line)", "Reverse DENY (Enemy blocks route)", "Reverse DELIVER (Enemy attacks rear)", "Reverse DESTROY (Enemy strikes)"],
        "Elemental Counter-Strategy": ["Earth Neutralization", "Water Infiltration", "Air Penetration", "Mountain Friction", "Lightning Redirection"],
        "Tactical Execution Protocol": [
            "Subterranean cloaking, deep acoustic/thermal grounding, zero digital emission.",
            "Bypassing rigid fortified barriers through fluid, adaptive, multi-route infiltration.",
            "Overwhelming adversary spectrum through electronic warfare, jamming, and signals noise.",
            "Funneling hostile forces into deadly geographical chokepoints and pre-sighted kill zones.",
            "Deploying decoy sensor networks, false heat signatures, and rapid tactical dispersal."
        ]
    })
    st.table(rev_matrix_df)

    # Narrative Tale 2
    st.markdown("""
    <div class="gold-card" style="border-left: 5px solid #D4AF37; background: #121813;">
        <h4 style="margin-top:0; color:#D4AF37;">📖 STRATEGIC TALE II: THE FLUID INFILTRATION OF TRIBUTARY ECHO</h4>
        <p style="font-style: italic; line-height: 1.6; color:#e0e6e1;">
            When Special Forces Detachment 4 was tasked with penetrating a heavily fortified cross-border valley, 
            they faced an enemy equipped with thermal radar and movement sensors along all roads. 
            Instead of pushing through the roadblock, the detachment executed the Riverine Doctrine. 
            They split into four micro-teams—acting as "tributaries"—and moved along natural drainage gullies during a heavy torrential rainstorm. 
            The noise of the rain masked their footsteps; the waterwashed gullies absorbed their thermal footprints. 
            By the time the enemy radar operators realized the perimeter had been breached, the tributaries had rejoined at the valley base 
            (The Delta) and delivered a decapitating strike to the enemy command bunker before disappearing like mist.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # SECTION 4: MASTER LEVEL — OPERATIONAL SYNTHESIS & SPECIAL FORCES TRADECRAFT
    # ==========================================================================
    st.markdown("""
    <div class="gold-card">
        <h2 style="margin-top:0;">SECTION 4: MASTER LEVEL — OPERATIONAL SYNTHESIS & SPECIAL FORCES TRADECRAFT</h2>
        <p style="line-height:1.7;">
            At the highest operational level, Special Forces operators embody elemental balance. To become unstoppable and all-pervading, 
            military forces must project natural attributes directly into tactics, movement, signature management, and strike execution.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns([1, 1])
    with col_m1:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">1. THE RIVERINE DOCTRINE (Tributary Dispersion)</div>
            <p>SF units must not move as rigid, massed formations against fortified lines. Like a river hitting rock, they fluidly bypass primary defenses. A strike element splits into micro-teams (tributaries) to penetrate small security gaps across wide terrain before re-converging at the target delta.</p>
        </div>
        <div class="gold-card">
            <div class="gold-card-title">2. ATMOSPHERIC INTEGRATION (Wind-Mimicry)</div>
            <p>SF operators eliminate contrast with the ambient environment. They move only when the ambient environment moves (wind gusts, rain, thermal shifts), matching movement patterns so sensor networks register the team as ambient background noise.</p>
        </div>
        <div class="gold-card">
            <div class="gold-card-title">3. MOUNTAIN OVERWATCH (Static Ground Integrity)</div>
            <p>Intelligence nodes adopt the silent, immovable posture of mountains. Deep Recon Patrols establish long-term, zero-emission Observation Posts (OPs) integrated into terrain features, maintaining continuous 360-degree overwatch without revealing signatures.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">4. SOLAR / SHADOW EXPLOITATION (Counter-Surveillance)</div>
            <p>Leverage natural blinding agents to mask movement. Advance with solar glare behind the unit to blind enemy electro-optical/thermal systems, or move within natural sensor blind spots (shadows, heavy fog, terrain masking).</p>
        </div>
        <div class="gold-card">
            <div class="gold-card-title">5. SEISMIC SHOCK TACTICS (Kinetic Disruption)</div>
            <p>Mirror the earthquake by storing potential energy and releasing it instantaneously at the enemy's weakest structural point. Strikes are violent, precise, and instantaneous, shattering command structures before withdrawing into the environment.</p>
        </div>
        <div class="gold-card">
            <div class="gold-card-title">6. GROUNDING IN EARTH (Thermal & Acoustic Shielding)</div>
            <p>Utilize subterranean terrain, mud, and deep soil cover to absorb thermal dissipation and acoustic resonance, neutralizing hostile satellite thermal sensors and acoustic ground sensors.</p>
        </div>
        """, unsafe_allow_html=True)

    # 360-Degree Fire Matrix Table
    st.markdown("#### 🔥 The 360-Degree Fire Parallel: Anatomy of the Elite Operator")
    fire_doc_df = pd.DataFrame({
        "Fire Element Aspect": [
            "1. Light (Illumination)", 
            "2. Heat (Thermal Energy)", 
            "3. Fuel / Wick (Consumption)", 
            "4. Extinction (Vanishing)"
        ],
        "Natural Physical Law": [
            "Visual radiance illuminating the surrounding terrain, exposing hidden structures.",
            "High-temperature thermal energy capable of altering physical states and destroying matter.",
            "The physical mass consumed to sustain the oxidation reaction of the fire.",
            "The rapid cessation of combustion, resulting in smoke dissipation and darkness."
        ],
        "Special Forces Operational Tradecraft": [
            "Intelligence, Vision & Reconnaissance: Mapping enemy baseline and target identification.",
            "Direct Action & Kinetic Lethality: Delivering decisive, violent force to collapse nodes.",
            "Physical Capital & Mental Grit: Burning internal energy reserves to sustain long-range ops.",
            "Stealth, Exfiltration & Legacy: Leaving zero footprint, vanishing into ambient shadows."
        ]
    })
    st.table(fire_doc_df)

    # Narrative Tale 3
    st.markdown("""
    <div class="gold-card" style="border-left: 5px solid #D4AF37; background: #121813;">
        <h4 style="margin-top:0; color:#D4AF37;">📖 STRATEGIC TALE III: THE GHOST STRIKE AT DAWN</h4>
        <p style="font-style: italic; line-height: 1.6; color:#e0e6e1;">
            At 0300 hours, an elite Special Forces assault element approached an enemy radar relay station perched on a cliffside. 
            They used the blinding glare of the rising sun behind them to obscure the view of the sentinel guards (Solar Exploitation). 
            Moving only when gusts of wind rattled the surrounding tree canopy (Wind Mimicry), they breached the perimeter undetected. 
            At 0415 hours, they unleashed a 45-second concentrated kinetic strike that completely consumed the radar station (Heat & Lightning). 
            By 0420 hours, before enemy quick reaction forces could scramble, the assault element had melted into subterranean drainage caverns (Earth Grounding & Extinction), 
            leaving the enemy commander staring at burning wreckage with no trace of who had struck.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Final Summary Banner
    st.markdown("""
    <div class="gold-card" style="text-align: center; border: 2px solid #D4AF37; background: linear-gradient(180deg, #1c281e 0%, #0b0e0c 100%);">
        <h3 style="color:#D4AF37; margin-bottom: 10px;">DIVINE WARFARE DOCTRINE SYNTHESIS COMPLETE</h3>
        <p style="color:#e0e6e1; line-height: 1.6; max-width: 900px; margin: 0 auto;">
            "By embedding Special Forces tactics into the immutable laws of nature, the force achieves total operational omnipresence, 
            absolute situational awareness, zero signature latency, and unhindered execution across any human terrain on Earth."
        </p>
        <div style="margin-top: 15px; font-size: 0.85rem; color: #8a9a8c;">
            <b>AUTHENTICATED BY:</b> XXSFX-A UNIVERSAL COMMAND CELL | DIVINE MATRIX ENGINE
        </div>
    </div>
    """, unsafe_allow_html=True)
