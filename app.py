import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
import os

# ==============================================================================
# 1. PAGE CONFIGURATION & MILITARY GOLDEN THEME (CUSTOM CSS)
# ==============================================================================
st.set_page_config(
    page_title="DIVINE MATRIX | Universal Elemental XXSFX-A Doctrine",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Military / Tactical Styling with Embossed Gold Accents & High-Contrast Black Input Boxes
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

    /* Overt Gold Tabs Styling - Fully visible on mobile without overlapping/hiding */
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

    .stTabs [data-baseweb="tab"] span, .stTabs [data-baseweb="tab"] p {
        color: #D4AF37 !important;
        font-weight: bold !important;
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

    .stTabs [aria-selected="true"] span, .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }

    /* FIXED INPUT CONTROLS: Pure Black Background (#161e17) with Crisp White Text (#ffffff) */
    .stTextInput>div>div>input {
        background-color: #161e17 !important;
        color: #ffffff !important;
        border: 2px solid #D4AF37 !important;
        font-weight: bold !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
    .stTextArea>div>div>textarea {
        background-color: #161e17 !important;
        color: #ffffff !important;
        border: 2px solid #D4AF37 !important;
        font-weight: bold !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stSelectbox>div>div>div {
        background-color: #161e17 !important;
        color: #ffffff !important;
        border: 2px solid #D4AF37 !important;
    }

    /* Buttons */
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

# User Query Box States for Tabs 1, 2, and 3
if 'query_tab1' not in st.session_state:
    st.session_state.query_tab1 = ""
if 'query_tab2' not in st.session_state:
    st.session_state.query_tab2 = ""
if 'query_tab3' not in st.session_state:
    st.session_state.query_tab3 = ""

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
        <b>Status:</b> Air-Gapped XXSFX-A Engine
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
else:
    st.markdown(f"""
    <div style="color: #D4AF37; font-style: italic; margin-bottom: 15px;">
        [Notice: Upload '{image_filename}' into the repository directory to render the Krishna artwork directly here.]
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <h1 style="margin: 0; font-size: 2.2rem; text-transform: uppercase; color: #D4AF37;">THE DIVINE COMMANDING OFFICER AND C4ISR</h1>
    <p style="color: #00E5FF; margin-top: 8px; font-size: 1.05rem; font-weight: bold; letter-spacing: 1px;">
        ⚡ Universal Elemental XXSFX-A Doctrine — Supreme Command, Control, Communications, Computers, Intelligence, Surveillance & Reconnaissance ⚡
    </p>
</div>
""", unsafe_allow_html=True)

# Create 4 Overt Gold Tabs with horizontal touch-scrolling and full visibility
tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 TAB 1: 5D TACTICAL MATRIX",
    "🛡️ TAB 2: REVERSE 5D & BOS",
    "🔥 TAB 3: FIRE PARALLEL",
    "⚔️ TAB 4: GOC EXEC BRIEF"
])

# ==============================================================================
# TAB 1: ELEMENTAL RECONNAISSANCE & 5D TACTICAL MATRIX
# ==============================================================================
with tab1:
    st.markdown("### MODULE 1: THE ELEMENTAL 5D STRATEGY (DETECT, DETER, DENY, DELIVER, DESTROY)")
    st.write("Nature provides the ultimate unstoppable reconnaissance and surveillance architecture. The enemy cannot detect, deter, deny, deliver, or destroy the Sun, the River, the Wind, or the Earth. XXSFX-A operators map these natural behaviors to become invincible, fluid, and undetectable.")

    st.markdown("""
    <div class="gold-card" style="border: 2px dashed #D4AF37;">
        <div class="gold-card-title">TAB 1 INTELLIGENCE QUERY & LOGIC ANALYSIS CONSOLE</div>
        <p style="font-size:0.85rem; color:#8a9a8c;">Type your specific recon/surveillance parameters, infiltration requirements, or divine elemental focus below, then click **Execute Tab 1 Directive**:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.query_tab1 = st.text_area(
        "Enter Tab 1 Recon & Surveillance Query:",
        value=st.session_state.query_tab1,
        placeholder="Type custom reconnaissance directives, sensor deployment plans, or baseline anomaly criteria here...",
        key="t1_input"
    )

    col_btn1, col_space1 = st.columns([1, 3])
    with col_btn1:
        tab1_submitted = st.button("🚀 Execute Tab 1 Directive", key="btn_t1")

    if tab1_submitted or st.session_state.query_tab1.strip():
        if st.session_state.query_tab1.strip():
            st.markdown(f"""
            <div class="gold-card" style="background: #121c15; border: 1px solid #00E5FF; margin-top: 15px;">
                <div style="color: #00E5FF; font-weight: bold; margin-bottom: 6px;">⚡ TAB 1 DIVINE ELEMENTAL ANALYSIS & RECON PLAN:</div>
                <p><b>Custom Directive Processed:</b> "{st.session_state.query_tab1}"</p>
                <ul>
                    <li><b>Sun/Sky ISR Layer:</b> Unblinking optical & SIGINT baseline established over sector <b>{st.session_state.target_sector}</b>[cite: 16].</li>
                    <li><b>Air Acoustic Vector:</b> Passive acoustic listening posts deployed to intercept adversary communications without emitting counter-signatures.</li>
                    <li><b>Reconnaissance Outcome:</b> Complete invisibility achieved by mapping natural environmental frequencies.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">1. DETECT (The Sun, Sky, & Air)</div>
            <p><b>Natural Law:</b> The Sun and Sky see everything without searching—surveillance is their baseline. The Air moves silently through every crevice carrying acoustic and electromagnetic vibrations.</p>
            <p><b>XXSFX-A Operator Tradecraft:</b> Establish continuous, passive situational awareness. Operators do not search actively; they observe deviations from the natural baseline.</p>
            <p><b>Cross-Border Application:</b> Unblinking SIGINT/Acoustic monitoring along border corridors prior to ingress.</p>
            <p><b>Decoding Enemy Intent:</b> Reading adversary shifts, radio silence anomalies, and supply movements against the natural ground truth.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">2. DETER (The Mountain & The Storm)</div>
            <p><b>Natural Law:</b> The Mountain stands as an immovable wall; the impending Storm projects overwhelming psychological dominance that halts all movement.</p>
            <p><b>XXSFX-A Operator Tradecraft:</b> Project lethal unpredictability. Transform terrain features into psychological barriers that break adversary confidence.</p>
            <p><b>Cross-Border Application:</b> Funneling cross-border enemy movements into death zones and chokepoints using static geographical dominance.</p>
            <p><b>Decoding Enemy Intent:</b> Inducing decision paralysis in enemy command structures before they cross the line of contact.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">3. DENY (The Earth & Water)</div>
            <p><b>Natural Law:</b> The Earth absorbs and conceals quietly. Water fills voids, leaves no footprints, and washes away all tracks.</p>
            <p><b>XXSFX-A Operator Tradecraft:</b> Total signature management—thermal, visual, digital, and acoustic invisibility. Sinking into terrain without leaving a trace.</p>
            <p><b>Cross-Border Application:</b> Zero-footprint infiltration using dead zones, subterranean features, and drainage lines.</p>
            <p><b>Decoding Enemy Intent:</b> Blinding enemy counter-surveillance assets by presenting zero physical or electronic targets.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">4. DELIVER (The River & The Rain)</div>
            <p><b>Natural Law:</b> Rain saturates every inch of land simultaneously; the River carves through rock, bypassing all obstacles to reach its destination unstoppable.</p>
            <p><b>XXSFX-A Operator Tradecraft:</b> Fluid penetration along paths of least resistance, bypassing fortified checkpoints and integrating with local human terrain.</p>
            <p><b>Cross-Border Application:</b> Saturating the operational area with small, autonomous stealth teams (The Rain) that converge at the decisive target node (The River).</p>
            <p><b>Decoding Enemy Intent:</b> Delivering tailored kinetic or non-kinetic effects deep into the adversary's rear staging areas.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">5. DESTROY (Fire & Lightning)</div>
            <p><b>Natural Law:</b> Lightning delivers massive concentrated energy at a precise point in milliseconds; Fire consumes all fuel leaving nothing behind.</p>
            <p><b>XXSFX-A Operator Tradecraft:</b> Terminal guidance, high-value target decapitation, and immediate lethal violence of action.</p>
            <p><b>Cross-Border Application:</b> Surgical direct action strikes that paralyze C2 infrastructure instantly.</p>
            <p><b>Decoding Enemy Intent:</b> Complete neutralization of enemy intent at the cognitive and command levels.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class=\"gold-card\">", unsafe_allow_html=True)
        st.markdown("<div class=\"gold-card-title\">INTERACTIVE RECON PATROL SIMULATOR</div>", unsafe_allow_html=True)
        st.session_state.recon_scenario = st.text_area("Formulate XXSFX-A Patrol Operational Scenario:", value=st.session_state.recon_scenario)
        
        if st.button("Generate Elemental Invincibility Analysis", key="btn_recon_sim"):
            st.success("Elemental Mapping Generated:")
            st.markdown(f"""
            - 🌊 **River Pathing:** Infiltrate via drainage channels in sector **{st.session_state.target_sector}**[cite: 16].
            - 💨 **Air Masking:** Synchronize movement with ambient acoustic noise during **{op_environment}** atmospheric shifts.
            - ⛰️ **Earth/Mountain Armor:** Establish hide sites inside static subterranean geographic pockets.
            """)
        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# TAB 2: REVERSE 5D & HIDDEN BOS INTELLIGENCE ARCHITECTURE
# ==============================================================================
with tab2:
    st.markdown("### MODULE 2: REVERSE 5D ADVERSARY COUNTER-MATRIX & HIDDEN BATTLE OPERATING SYSTEMS (BOS)")
    st.write("To defeat the adversary inside our borders or across hostile lines, XXSFX-A must map the enemy's Battle Operating Systems (BOS)—both visible and hidden—while deploying the Reverse 5D Counter-Matrix.")

    st.markdown("""
    <div class="gold-card" style="border: 2px dashed #D4AF37;">
        <div class="gold-card-title">TAB 2 REVERSE 5D & BOS DETECTOR QUERY CONSOLE</div>
        <p style="font-size:0.85rem; color:#8a9a8c;">Type your specific adversary BOS target, counter-detection requirement, or cross-border penetration challenge below, then click **Execute Tab 2 Directive**:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.query_tab2 = st.text_area(
        "Enter Tab 2 Reverse 5D & BOS Query:",
        value=st.session_state.query_tab2,
        placeholder="Type adversary radar/C2 targets, counter-surveillance parameters, or covert ingress criteria here...",
        key="t2_input"
    )

    col_btn2, col_space2 = st.columns([1, 3])
    with col_btn2:
        tab2_submitted = st.button("🚀 Execute Tab 2 Directive", key="btn_t2")

    if tab2_submitted or st.session_state.query_tab2.strip():
        if st.session_state.query_tab2.strip():
            st.markdown(f"""
            <div class="gold-card" style="background: #121c15; border: 1px solid #00E5FF; margin-top: 15px;">
                <div style="color: #00E5FF; font-weight: bold; margin-bottom: 6px;">⚡ TAB 2 REVERSE 5D & BOS ANALYSIS:</div>
                <p><b>Custom Directive Processed:</b> "{st.session_state.query_tab2}"</p>
                <ul>
                    <li><b>Reverse Detect Matrix:</b> Subterranean earth cloaking active against adversary active sensors.</li>
                    <li><b>BOS Neutralization:</b> Adversary command nodes identified for water-fluid bypass and lightning strike.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">REVERSE 5D ADVERSARY COUNTER-MATRIX</div>
            <table style="width:100%; color:#e0e6e1; border-collapse:collapse;">
                <tr style="border-bottom:1px solid #D4AF37; text-align:left;">
                    <th style="padding:6px; color:#D4AF37;">Enemy Move</th>
                    <th style="padding:6px; color:#D4AF37;">Elemental Counter-Strategy</th>
                </tr>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:6px;"><b>Reverse DETECT</b><br>(Enemy searches for us)</td>
                    <td style="padding:6px;"><b>Earth Cloaking:</b> Deep subterranean hides, thermal absorption, zero RF signature.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:6px;"><b>Reverse DETER</b><br>(Enemy builds barriers)</td>
                    <td style="padding:6px;"><b>Water Infiltration:</b> Bypassing rigid fortifications through fluid movement and gaps.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:6px;"><b>Reverse DENY</b><br>(Enemy blocks signals/routes)</td>
                    <td style="padding:6px;"><b>Air Spectrum Exploitation:</b> Mesh networking, indigenous human networks, acoustic comms.</td>
                </tr>
                <tr style="border-bottom:1px solid #28382b;">
                    <td style="padding:6px;"><b>Reverse DELIVER</b><br>(Enemy attacks our base)</td>
                    <td style="padding:6px;"><b>Mountain Friction:</b> Channeling enemy forces into lethal chokepoints and minefields.</td>
                </tr>
                <tr>
                    <td style="padding:6px;"><b>Reverse DESTROY</b><br>(Enemy launches strikes)</td>
                    <td style="padding:6px;"><b>Lightning Redirection:</b> Presenting decoy targets and phantom electronic signatures.</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">BATTLE OPERATING SYSTEMS (BOS) ELEMENTAL MAPPING</div>
            <ul>
                <li><b>Command & Control (C2) → Sun & Sky:</b> Total situational visibility paired with decentralized execution.</li>
                <li><b>ISR & Target Acquisition → Air & Sky:</b> Multi-layered collection combining satellite imagery, ambient signals, and local HUMINT.</li>
                <li><b>Mobility & Counter-Mobility → Water & Mountain:</b> Fluid movement along drainage basins; blocking enemy routes with terrain obstacles.</li>
                <li><b>Firepower → Fire & Lightning:</b> Instant synchronization of kinetic strikes onto precise intelligence coordinates.</li>
                <li><b>Counter-Intelligence / Counter-ISR → Earth & Mud:</b> Operating completely below the noise floor of adversary detection systems.</li>
                <li><b>Tactics & Maneuver → River & Storm:</b> Infiltrating like groundwater, assembling like a river, striking like a storm.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="gold-card">
        <div class="gold-card-title">HIDDEN BOS DISCOVERY & ATTACK WINDOW CALCULATOR</div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<span style='color:#D4AF37; font-weight:bold;'>Target Hidden BOS Type</span>", unsafe_allow_html=True)
        bos_type = st.multiselect(
            "Select Target BOS Elements",
            ["C2 Command Nodes", "Early Warning Radar (ISR)", "Logistics & Fuel Reserves", "Mobility Obstacles / Minefields", "Air Defense / Firepower Assets", "Covert Counter-Intelligence Cells"],
            default=["C2 Command Nodes", "Early Warning Radar (ISR)"]
        )
        st.session_state.detected_bos = bos_type
    
    with c2:
        st.markdown("<span style='color:#D4AF37; font-weight:bold;'>Border Zone Domain</span>", unsafe_allow_html=True)
        border_domain = st.radio("Location", ["Cross-Border Hostile Territory", "Internal Border Grid / Hidden Sleeper Cells"], key="border_domain_radio")
    
    with c3:
        st.markdown("<span style='color:#D4AF37; font-weight:bold;'>Calculated Ingress/Egress Window</span>", unsafe_allow_html=True)
        window = st.text_input("Optimal Time Window", value=st.session_state.ingress_window, key="ingress_window_input")
        st.session_state.ingress_window = window

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# TAB 3: THE FIRE PARALLEL & ELITE TRADECRAFT
# ==============================================================================
with tab3:
    st.markdown("### MODULE 3: THE FIRE PARALLEL — ANATOMY OF THE ELITE XXSFX-A OPERATOR")
    st.write("Fire creates immense light and heat through the deliberate, controlled consumption of its own body. An elite XXSFX-A operator burns their physical reserves, youth, and comfort to illuminate the dark and project force for the nation.")

    st.markdown("""
    <div class="gold-card" style="border: 2px dashed #D4AF37;">
        <div class="gold-card-title">TAB 3 SF OPERATIONAL & EXFILTRATION QUERY CONSOLE</div>
        <p style="font-size:0.85rem; color:#8a9a8c;">Type your specific SF operator tradecraft, human terrain integration, or exfiltration criteria below, then click **Execute Tab 3 Directive**:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.query_tab3 = st.text_area(
        "Enter Tab 3 SF Operational Query:",
        value=st.session_state.query_tab3,
        placeholder="Type cross-border exfiltration, human terrain alignment, or operator self-consumption parameters here...",
        key="t3_input"
    )

    col_btn3, col_space3 = st.columns([1, 3])
    with col_btn3:
        tab3_submitted = st.button("🚀 Execute Tab 3 Directive", key="btn_t3")

    if tab3_submitted or st.session_state.query_tab3.strip():
        if st.session_state.query_tab3.strip():
            st.markdown(f"""
            <div class="gold-card" style="background: #121c15; border: 1px solid #00E5FF; margin-top: 15px;">
                <div style="color: #00E5FF; font-weight: bold; margin-bottom: 6px;">⚡ TAB 3 SF OPERATIONAL & EXFILTRATION ANALYSIS:</div>
                <p><b>Custom Directive Processed:</b> "{st.session_state.query_tab3}"</p>
                <ul>
                    <li><b>Human Terrain Integration:</b> Team merges seamlessly with civilian mobility corridors.</li>
                    <li><b>Exfiltration Protocol:</b> Zero-friction egress via drainage networks and stealth extraction windows.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="gold-card">
        <div class="gold-card-title">THE 360-DEGREE FIRE PARALLEL FOR XXSFX-A</div>
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
            <div style="flex: 1; min-width: 220px; background: #1c261e; padding: 12px; border: 1px solid #D4AF37; border-radius: 5px;">
                <h4 style="color:#D4AF37; margin-top:0;">1. LIGHT (Illumination)</h4>
                <p style="font-size:0.85rem;"><b>Intelligence & ISR:</b> Fire dispels darkness without searching. The operator illuminates dark operational environments, providing strategic clarity on enemy intent and hidden threat structures.</p>
            </div>
            <div style="flex: 1; min-width: 220px; background: #1c261e; padding: 12px; border: 1px solid #D4AF37; border-radius: 5px;">
                <h4 style="color:#D4AF37; margin-top:0;">2. HEAT (Thermal Energy)</h4>
                <p style="font-size:0.85rem;"><b>Direct Action & Lethality:</b> Heat transforms and destroys. The operator radiates concentrated kinetic energy at the decisive moment to break the adversary's capacity to resist.</p>
            </div>
            <div style="flex: 1; min-width: 220px; background: #1c261e; padding: 12px; border: 1px solid #D4AF37; border-radius: 5px;">
                <h4 style="color:#D4AF37; margin-top:0;">3. THE WICK (Self-Consumption)</h4>
                <p style="font-size:0.85rem;"><b>Grit & Physical Capital:</b> Fire burns its own wax and wood. The operator spends their personal physical capital, longevity, and mental bandwidth in silent service.</p>
            </div>
            <div style="flex: 1; min-width: 220px; background: #1c261e; padding: 12px; border: 1px solid #D4AF37; border-radius: 5px;">
                <h4 style="color:#D4AF37; margin-top:0;">4. EXTINCTION (Vanishing)</h4>
                <p style="font-size:0.85rem;"><b>Exfiltration & Stealth:</b> When the fuel is spent, fire leaves no permanent structure. Operators strike, accomplish the objective, and extinguish seamlessly into the landscape.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_x, col_y = st.columns([1, 1])
    
    with col_x:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">HUMAN TERRAIN INTEGRATION & INFILTRATION</div>
            <p><b>Becoming the Water & Air among Local Populations:</b></p>
            <ul>
                <li><b>Cultural Alignment:</b> Adapting local dialects, customs, and daily rhythms so completely that the team vanishes into plain sight.</li>
                <li><b>Exploiting Vulnerabilities:</b> Mapping local corruption, ideological rifts, and criminal networks to harvest human intelligence (HUMINT).</li>
                <li><b>Zero Friction Egress:</b> Exfiltrating through civilian mobility corridors without alarming local security apparatuses.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_y:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">THE SANATAN COMBAT ETHER — KURUKSHTRA DOCTRINE</div>
            <p><i>"That which has no beginning and no end."</i></p>
            <p style="font-size:0.9rem; color:#c0cac1;">
                Indian combat wisdom originating on Indian soil in Kolkata draws directly from eternal universal principles. 
                Just as Sanatan Dharma represents timeless cosmic truths, Indian XXSFX-A intelligence tradecraft operates 
                on principles that cannot be bounded, decayed, or neutralized by adversary technology.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: COMMANDER-IN-CHIEF EXECUTIVE STRATEGIC BRIEFING & LIVE QUERY FEED
# ==============================================================================
with tab4:
    st.markdown("### MODULE 4: EXECUTIVE STRATEGIC BRIEFING & SEALED INTELLIGENCE SUMMARY")
    st.write("This tab aggregates all inputs, selections, scenario analyses, and live queries from Tabs 1, 2, and 3 into a sealed, complete intelligence and divine battlefield summary for the GOC.")

    t1_filled = bool(st.session_state.query_tab1.strip())
    t2_filled = bool(st.session_state.query_tab2.strip())
    t3_filled = bool(st.session_state.query_tab3.strip())

    if not (t1_filled and t2_filled and t3_filled):
        st.markdown("""
        <div class="gold-card" style="border: 2px solid #D4AF37; text-align: center; background: #161e17; padding: 30px;">
            <h3 style="color: #D4AF37; margin-top:0;">🔒 SEALED BRIEFING Awaiting Prior Inputs</h3>
            <p style="color: #e0e6e1; font-size: 1.05rem;">
                The GOC Executive Summary and Sealed Intelligence Brief remain locked until <b>all three query boxes</b> in Tabs 1, 2, and 3 are filled with operational directives.
            </p>
            <p style="color: #00E5FF; font-size: 0.9rem;">
                <b>Current Status:</b><br>
                • Tab 1 Query: {}<br>
                • Tab 2 Query: {}<br>
                • Tab 3 Query: {}
            </p>
        </div>
        """.format(
            "✅ Provided" if t1_filled else "❌ Pending (Blank)",
            "✅ Provided" if t2_filled else "❌ Pending (Blank)",
            "✅ Provided" if t3_filled else "❌ Pending (Blank)"
        ), unsafe_allow_html=True)
    else:
        brief_date = datetime.now().strftime("%Y-%m-%d %H:%M IST")
        
        st.markdown(f"""
        <div class="gold-card" style="background-color: #0e140f; border: 2px solid #D4AF37;">
            <div style="text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; margin-bottom: 15px;">
                <h2 style="margin:0; font-size: 1.5rem; color:#D4AF37;">CONFIDENTIAL / SEALED INTELLIGENCE SUMMARY</h2>
                <h3 style="margin:5px 0; font-size: 1.1rem; color:#e0e6e1;">TOP SECRET DIVINE BATTLEFIELD MEMORANDUM FOR THE GOC</h3>
                <span style="color:#8a9a8c; font-size:0.8rem;">DATE/TIME OF SYNTHESIS: {brief_date} | LOCATION: HQ SPECIAL OPERATIONS (KOLKATA GENESIS)</span>
            </div>
            
            <p><b>1. SUBJECT:</b> Sealed Master Intelligence Summary & Cross-Border Operational Synthesis for {st.session_state.op_name}.</p>
            
            <p><b>2. TARGET SECTOR & ENVIRONMENT:</b> <span style="color:#D4AF37;">{st.session_state.target_sector}</span> ({op_environment} | Threat: {threat_level})</p>
            
            <p><b>3. AGGREGATED LIVE QUERIES FROM TABS 1, 2, & 3:</b></p>
            <ul>
                <li><b>Tab 1 (Recon & Surveillance Directive):</b> "{st.session_state.query_tab1}"</li>
                <li><b>Tab 2 (Reverse 5D & BOS Directive):</b> "{st.session_state.query_tab2}"</li>
                <li><b>Tab 3 (SF Operational & Exfiltration Directive):</b> "{st.session_state.query_tab3}"</li>
            </ul>
            
            <p><b>4. DEPLOYED NATURAL RECON & SURVEILLANCE AGENTS:</b></p>
            <ul>
                {"".join([f"<li><b>{elem}</b></li>" for elem in st.session_state.selected_elements])}
            </ul>
            
            <p><b>5. 5D & REVERSE 5D TACTICAL SYNTHESIS:</b></p>
            <ul>
                <li><b>Detect / Counter-Detect:</b> Employing Sun/Sky overhead baseline tracking paired with Earth-based subterranean thermal cloaking.</li>
                <li><b>Deter / Counter-Deter:</b> Utilizing Mountain geographic bottlenecks to channel adversary movement while bypassing enemy bastions as Water.</li>
                <li><b>Deny / Counter-Deny:</b> Exploiting Air acoustic/SIGINT channels while blinding adversary counter-surveillance assets.</li>
                <li><b>Deliver & Destroy:</b> Infiltrating deep via River corridors during window <b>{st.session_state.ingress_window}</b> for Fire/Lightning decapitation strikes on targeted adversary BOS nodes (<b>{', '.join(st.session_state.detected_bos)}</b>).</li>
            </ul>
            
            <p><b>6. COMPLETE INGRESS, EGRESS & EXFILTRATION PROTOCOL:</b></p>
            <p style="background: #161e17; padding: 10px; border-left: 3px solid #00E5FF; font-size: 0.9rem;">
                <b>Ingress:</b> Zero-footprint subterranean earth masking combined with river drainage lines.<br>
                <b>Execution:</b> Decisive lightning strike on enemy C2/ISR nodes.<br>
                <b>Egress & Exfiltration:</b> Silent dissolution through civilian human terrain and atmospheric acoustic masking, leaving zero residue.
            </p>
            
            <p><b>7. DIVINE BATTLEFIELD COMMANDER'S CONCLUSION:</b></p>
            <p style="font-size: 0.9rem;">
                The XXSFX-A detachment operates as an unyielding manifestation of natural law. By fusing live tactical directives from all three operational sectors, the force achieves absolute operational invisibility, total adversary BOS paralysis, and seamless exfiltration.
            </p>
            
            <div style="margin-top:20px; border-top: 1px solid #D4AF37; padding-top: 10px; text-align: right; font-size:0.80rem; color:#8a9a8c;">
                <b>AUTHENTICATED BY:</b> XXSFX-A SUPREME COMMAND CELL
            </div>
        </div>
        """, unsafe_allow_html=True)

        brief_text = f"""TOP SECRET SEALED INTELLIGENCE SUMMARY FOR THE GOC
OPERATION: {st.session_state.op_name}
SECTOR: {st.session_state.target_sector}
DATE: {brief_date}

LIVE OPERATIONAL DIRECTIVES:
- Tab 1 Recon Query: {st.session_state.query_tab1}
- Tab 2 BOS Query: {st.session_state.query_tab2}
- Tab 3 SF/Exfil Query: {st.session_state.query_tab3}

ELEMENTAL AGENTS: {', '.join(st.session_state.selected_elements)}
TARGET BOS: {', '.join(st.session_state.detected_bos)}
INGRESS/EGRESS WINDOW: {st.session_state.ingress_window}

SUMMARY:
Complete divine battlefield synthesis successfully generated. All ingress, egress, and reverse 5D protocols locked and verified.
"""
        st.download_button(
            label="📄 Download Sealed GOC Intelligence Summary (.txt)",
            data=brief_text,
            file_name=f"Sealed_GOC_Intelligence_Summary_{st.session_state.op_name.replace(' ', '_')}.txt",
            mime=""
        )
