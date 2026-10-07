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

# Custom Military / Tactical Styling with Embossed Gold Accents & Overt Gold Tabs
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

    /* Sub-cards and badges */
    .element-badge {
        background-color: #243326;
        color: #f0e68c;
        border: 1px solid #D4AF37;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: bold;
    }

    /* Overt Gold Tabs Styling (Fully Visible Without Hover or Touch) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #161e17;
        border: 2px solid #D4AF37;
        border-radius: 6px 6px 0px 0px;
        padding: 8px;
        overflow-x: auto;
    }

    .stTabs [data-baseweb="tab"] {
        height: 52px;
        background-color: #1c281e !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 4px 4px 0px 0px;
        color: #D4AF37 !important;
        font-weight: bold !important;
        font-size: 0.95rem !important;
        padding: 0 16px;
        opacity: 1 !important;
    }

    .stTabs [data-baseweb="tab"] p {
        color: #D4AF37 !important;
        font-weight: bold !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #3a4d3c 0%, #243326 100%) !important;
        border: 2px solid #D4AF37 !important;
        border-bottom: 3px solid #0b0e0c !important;
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.9);
        box-shadow: 0 -2px 10px rgba(212, 175, 55, 0.4);
    }

    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }

    /* Input Controls Customization */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #161e17 !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(180deg, #3a4d3c 0%, #1c281e 100%);
        color: #D4AF37;
        border: 2px solid #D4AF37;
        font-weight: bold;
        text-shadow: 1px 1px 2px #000;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #D4AF37;
        color: #0b0e0c;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SESSION STATE INITIALIZATION FOR COMMANDER'S BRIEF SYNTHESIS
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
# 4. MAIN BODY HEADER: DIVINE COMMANDING OFFICER & C4ISR (IMAGE REFLECTED)
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

# Create 4 Overt Gold Tabs (Fully Visible and Legible Without Touching)
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

        # Interactive Reconnaissance Planner
        st.markdown("<div class=\"gold-card\">", unsafe_allow_html=True)
        st.markdown("<div class=\"gold-card-title\">INTERACTIVE RECON PATROL SIMULATOR</div>", unsafe_allow_html=True)
        st.session_state.recon_scenario = st.text_area("Formulate XXSFX-A Patrol Operational Scenario:", value=st.session_state.recon_scenario)
        
        if st.button("Generate Elemental Invincibility Analysis"):
            st.success("Elemental Mapping Generated:")
            st.markdown(f"""
            - 🌊 **River Pathing:** Infiltrate via drainage channels in sector **{st.session_state.target_sector}**.
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

    # Hidden BOS Mapping Workspace
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
        border_domain = st.radio("Location", ["Cross-Border Hostile Territory", "Internal Border Grid / Hidden Sleeper Cells"])
    
    with c3:
        st.markdown("<span style='color:#D4AF37; font-weight:bold;'>Calculated Ingress/Egress Window</span>", unsafe_allow_html=True)
        window = st.text_input("Optimal Time Window", value=st.session_state.ingress_window)
        st.session_state.ingress_window = window

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# TAB 3: THE FIRE PARALLEL & ELITE TRADECRAFT
# ==============================================================================
with tab3:
    st.markdown("### MODULE 3: THE FIRE PARALLEL — ANATOMY OF THE ELITE XXSFX-A OPERATOR")
    st.write("Fire creates immense light and heat through the deliberate, controlled consumption of its own body. An elite XXSFX-A operator burns their physical reserves, youth, and comfort to illuminate the dark and project force for the nation.")

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
# TAB 4: COMMANDER-IN-CHIEF EXECUTIVE STRATEGIC BRIEFING
# ==============================================================================
with tab4:
    st.markdown("### MODULE 4: EXECUTIVE STRATEGIC BRIEFING FOR GENERAL OFFICER COMMANDING (GOC)")
    st.write("This tab automatically aggregates inputs, selections, scenario analyses, and elemental mappings from Tabs 1, 2, and 3 into an executive military memorandum.")

    # Executive Brief Container
    brief_date = datetime.now().strftime("%Y-%m-%d %H:%M IST")
    
    st.markdown(f"""
    <div class="gold-card" style="background-color: #0e140f; border: 2px solid #D4AF37;">
        <div style="text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; margin-bottom: 15px;">
            <h2 style="margin:0; font-size: 1.5rem; color:#D4AF37;">CONFIDENTIAL / OPERATIONAL EYES ONLY</h2>
            <h3 style="margin:5px 0; font-size: 1.1rem; color:#e0e6e1;">TOP SECRET BRIEFING MEMORANDUM FOR THE GOC</h3>
            <span style="color:#8a9a8c; font-size:0.8rem;">DATE/TIME OF SYNTHESIS: {brief_date} | LOCATION: HQ SPECIAL OPERATIONS</span>
        </div>
        
        <p><b>1. SUBJECT:</b> Operational Application of Universal Elemental Doctrine to {st.session_state.op_name}.</p>
        
        <p><b>2. TARGET SECTOR:</b> <span style="color:#D4AF37;">{st.session_state.target_sector}</span> ({op_environment} | Threat: {threat_level})</p>
        
        <p><b>3. DEPLOYED NATURAL RECON & SURVEILLANCE AGENTS:</b></p>
        <ul>
            {"".join([f"<li><b>{elem}</b></li>" for elem in st.session_state.selected_elements])}
        </ul>
        
        <p><b>4. 5D & REVERSE 5D TACTICAL SYNTHESIS:</b></p>
        <ul>
            <li><b>Detect / Counter-Detect:</b> Employing Sun/Sky overhead baseline tracking paired with Earth-based subterranean thermal cloaking to maintain zero footprint.</li>
            <li><b>Deter / Counter-Deter:</b> Utilizing Mountain geographic bottlenecks to force adversary movement into predetermined engagement zones while bypassing enemy bastions as Water.</li>
            <li><b>Deny / Counter-Deny:</b> Exploiting Air acoustic/SIGINT channels while denying target acquisition to adversary counter-surveillance assets.</li>
            <li><b>Deliver & Destroy:</b> Infiltrating deep via River corridors during the optimal window (<b>{st.session_state.ingress_window}</b>) to deliver Fire/Lightning decapitation strikes on critical adversary BOS nodes.</li>
        </ul>
        
        <p><b>5. TARGETED ADVERSARY HIDDEN BATTLE OPERATING SYSTEMS (BOS):</b></p>
        <ul>
            {"".join([f"<li><b>Target BOS:</b> {bos}</li>" for bos in st.session_state.detected_bos])}
        </ul>
        
        <p><b>6. OPERATIONAL PATROL SCENARIO:</b></p>
        <p style="font-style: italic; color:#c0cac1; background: #161e17; padding: 10px; border-left: 3px solid #D4AF37;">
            "{st.session_state.recon_scenario}"
        </p>
        
        <p><b>7. COMMANDER'S CONCLUSION:</b></p>
        <p style="font-size: 0.9rem;">
            The XXSFX-A detachment operating under this doctrine acts with the invisibility of the Wind, the persistence of the Sun, the fluid stealth of the River, and the lethal precision of Lightning. By consuming their physical reserves (The Wick), operators illuminate the operational dark, uncover hidden adversary BOS, and execute cross-border missions with absolute invincibility and zero compromise.
        </p>
        
        <div style="margin-top:20px; border-top: 1px solid #D4AF37; padding-top: 10px; text-align: right; font-size:0.80rem; color:#8a9a8c;">
            <b>BY ORDER OF COMMAND:</b> XXSFX-A STRATEGIC CELL (KOLKATA GENESIS)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Download Button for Briefing Text
    brief_text = f"""TOP SECRET BRIEFING MEMORANDUM FOR THE GOC
SUBJECT: Universal Elemental Doctrine - {st.session_state.op_name}
DATE: {brief_date}
SECTOR: {st.session_state.target_sector}

1. DEPLOYED ELEMENTS: {', '.join(st.session_state.selected_elements)}
2. TARGET BOS: {', '.join(st.session_state.detected_bos)}
3. INGRESS/EGRESS WINDOW: {st.session_state.ingress_window}
4. SCENARIO: {st.session_state.recon_scenario}

EXECUTIVE SUMMARY:
XXSFX-A teams executing 5D & Reverse 5D framework map immutable natural laws to remain undetectable, undeniable, and undestructible across border corridors.
"""
    st.download_button(
        label="📄 Download GOC Executive Briefing (.txt)",
        data=brief_text,
        file_name=f"GOC_Briefing_{st.session_state.op_name.replace(' ', '_')}.txt",
        mime="text/plain"
    )
