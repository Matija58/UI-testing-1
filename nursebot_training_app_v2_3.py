import time
from datetime import timedelta
import streamlit as st

st.set_page_config(
    page_title="NurseBot Training",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# VISUAL STYLE — mirrors the desktop NurseBot layout
# --------------------------------------------------
st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            background: #f3f3f3 !important;
            color: #111111 !important;
        }

        .block-container {
            padding-top: 0.7rem;
            padding-bottom: 1rem;
            max-width: 1500px;
            color: #111111 !important;
        }

        .stMarkdown, .stText, label, p, span, div {
            color: inherit;
        }

        div[data-testid="stTabs"] {
            color: #111111 !important;
        }

        div[data-testid="stTabs"] button {
            color: #111111 !important;
        }

        div[data-testid="stSelectbox"] label,
        div[data-testid="stNumberInput"] label,
        div[data-testid="stTextInput"] label,
        div[data-testid="stCheckbox"] label {
            color: #111111 !important;
        }

        .nb-header {
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding:10px 14px 8px 14px;
        }

        .nb-title {
            font-family: Arial, sans-serif;
            font-size: 27px;
            font-weight: 700;
        }

        .nb-header-right {
            font-family: Arial, sans-serif;
            font-size: 14px;
            font-weight: 700;
        }

        .groupbox {
            border:1px solid #b8b8b8;
            border-radius:4px;
            padding:12px 10px 10px 10px;
            margin:5px 0 9px 0;
            position:relative;
            background:#ffffff;
            color:#111111 !important;
        }

        .legend {
            position:absolute;
            top:-10px;
            left:10px;
            background:#ffffff;
            color:#111111 !important;
            padding:0 5px;
            font-family:Arial, sans-serif;
            font-size:14px;
            font-weight:600;
        }

        .compact {
            padding-top:9px;
            padding-bottom:7px;
        }

        .caption-status {
            font-size:12px;
            font-style:italic;
            color:#444 !important;
            margin-bottom:5px;
        }

        .caption-text {
            font-size:18px;
            font-style:italic;
            color:#333 !important;
            min-height:28px;
        }

        .cue-category {
            font-size:15px;
            font-weight:700;
            color:#1d6b36;
        }

        .cue-category-urgent {
            font-size:15px;
            font-weight:700;
            color:#9c1c1c;
        }

        .cue-quote {
            color:#444 !important;
            font-style:italic;
            margin:4px 0 7px 0;
        }

        .response-box {
            border:1px solid #c8c8c8;
            border-radius:4px;
            padding:9px;
            min-height:86px;
            background:white;
        }

        .response-title {
            font-size:13px;
            font-weight:700;
            margin-bottom:7px;
        }

        .transcript {
            border:1px solid #ababab;
            min-height:430px;
            max-height:520px;
            overflow-y:auto;
            padding:10px 12px;
            background:#ffffff;
            color:#111111 !important;
            font-family:Arial, sans-serif;
            font-size:15px;
            line-height:1.42;
        }

        .line {
            margin-bottom:5px;
        }

        .confidence-red { color:#b00020; font-weight:700; }
        .confidence-orange { color:#d26900; font-weight:700; }
        .confidence-yellow { color:#a57c00; font-weight:700; }
        .confidence-green { color:#137333; font-weight:700; }
        .identity-uncertain { color:#555; font-weight:700; }

        .status-running { color:#137333; font-weight:700; }
        .status-paused { color:#a05a00; font-weight:700; }
        .status-stopped { color:#8c1d1d; font-weight:700; }

        .training-note {
            font-size:12px;
            color:#5f6368 !important;
        }

        div[data-testid="stTabs"] button {
            font-size:15px;
        }

        div[data-testid="stButton"] > button {
            min-height:38px;
            background:#ffffff !important;
            color:#111111 !important;
            border:1px solid #8f8f8f !important;
            border-radius:8px !important;
            font-weight:600 !important;
            box-shadow:none !important;
        }

        div[data-testid="stButton"] > button:hover {
            background:#eaf2f8 !important;
            color:#111111 !important;
            border:1px solid #2b6f9f !important;
        }

        div[data-testid="stButton"] > button:focus,
        div[data-testid="stButton"] > button:focus-visible {
            color:#111111 !important;
            border:2px solid #2b6f9f !important;
            outline:none !important;
            box-shadow:none !important;
        }

        div[data-testid="stButton"] > button p,
        div[data-testid="stButton"] > button span,
        div[data-testid="stButton"] > button div {
            color:#111111 !important;
        }

        div[data-testid="stButton"] > button:disabled,
        div[data-testid="stButton"] > button[disabled] {
            background:#ececec !important;
            color:#666666 !important;
            border:1px solid #bcbcbc !important;
            opacity:1 !important;
        }

        .disabled-row {
            color:#6c6c6c;
            font-size:13px;
        }
    
        .groupbox, .groupbox * {
            color:#111111;
        }

        .response-box, .response-box * {
            color:#111111 !important;
        }

        .transcript, .transcript .line {
            color:#111111 !important;
        }

        .confidence-red { color:#b00020 !important; font-weight:700; }
        .confidence-orange { color:#d26900 !important; font-weight:700; }
        .confidence-yellow { color:#a57c00 !important; font-weight:700; }
        .confidence-green { color:#137333 !important; font-weight:700; }
        .identity-uncertain { color:#555555 !important; font-weight:700; }

        div[data-testid="stExpander"] {
            background:#ffffff !important;
            color:#111111 !important;
            border-color:#b8b8b8 !important;
        }

        div[data-testid="stExpander"] summary,
        div[data-testid="stExpander"] summary * {
            color:#111111 !important;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SCRIPTED TRAINING SCENARIOS
# Times are seconds after Start.
# --------------------------------------------------
SCENARIOS = {
    "Perfect Recognition Demo": {
        "patient": "John Carter",
        "caregiver": "None",
        "reason": "Headache and dizziness",
        "baseline_ao": 4,
        "current_ao": 4,
        "cue_at": 18,
        "cue_category": "Possible Fall / Mobility Risk",
        "cue_level": "Review",
        "cue_quote": "I've been having a headache and I've also felt dizzy a few times today.",
        "nursebot_response": (
            "Please stay seated for now. I am going to let your nurse know "
            "that you feel dizzy or unsteady."
        ),
        "nurse_next_step": (
            "Prevent unsupported standing or walking until a nurse assesses "
            "dizziness, balance, orthostatic symptoms, and fall risk."
        ),
        "lines": [
            (4,  "Nurse 1", 98, "Good morning, my name is Sarah and I'll be one of your nurses today."),
            (8,  "Nurse 1", 97, "Can you tell me your full name and what brought you in?"),
            (11, "Patient", 96, "Good morning."),
            (13, "Patient", 98, "My name is John."),
            (18, "Patient", 97, "I've been having a headache and I've also felt dizzy a few times today."),
            (23, "Nurse 2", 98, "I'm Michael, the other nurse helping with your care."),
            (27, "Nurse 2", 97, "When did the headache and dizziness start?"),
            (33, "Patient", 96, "The headache started this morning. The dizziness came on later, especially when I stood up."),
            (39, "Nurse 1", 98, "On a scale of zero to ten, how bad is your headache?"),
            (43, "Patient", 97, "I would say it's about a five out of ten."),
            (49, "Nurse 2", 98, "Have you had nausea, blurred vision, chest pain, trouble breathing, or weakness?"),
            (54, "Patient", 97, "I haven't had chest pain or trouble breathing."),
            (58, "Patient", 96, "I felt a little nauseous, but my vision seems normal."),
            (63, "Nurse 1", 99, "Thank you for telling us. Please stay seated while I check your vital signs."),
            (68, "Patient", 98, "Okay, I'll stay here."),
            (73, "Nurse 2", 98, "Since you felt dizzy when standing, please don't get up or walk by yourself for now."),
            (78, "Patient", 97, "I understand. I was worried I might lose my balance."),
            (83, "Nurse 1", 98, "We'll help you if you need to stand."),
            (88, "Nurse 1", 97, "Have you had anything to eat or drink today?"),
            (93, "Patient", 96, "I had a small breakfast, but I haven't had much water."),
            (99, "Nurse 2", 98, "Thanks for letting us know. We'll share that with the health care provider."),
            (106,"Nurse 1", 99, "Is there anything else you need right now?"),
            (111,"Patient", 98, "No thank you. I feel better knowing you're checking on me."),
            (116,"Nurse 1", 99, "You're welcome, John. Please use the call button if you need us."),
        ],
    },

    "Dizziness / Fall Risk": {
        "patient": "John Carter",
        "caregiver": "None",
        "reason": "Headache and dizziness",
        "baseline_ao": 4,
        "current_ao": 4,
        "cue_at": 18,
        "cue_category": "Possible Fall / Mobility Risk",
        "cue_level": "Review",
        "cue_quote": "I've been having a headache and I've also felt dizzy a few times today.",
        "nursebot_response": (
            "Please stay seated for now. I am going to let your nurse know "
            "that you feel dizzy or unsteady."
        ),
        "nurse_next_step": (
            "Prevent unsupported standing or walking until a nurse assesses "
            "dizziness, balance, orthostatic symptoms, and fall risk."
        ),
        "lines": [
            (4,  "Nurse 1", 92, "Good morning, my name is Sarah and I'll be one of your nurses today."),
            (8,  "Nurse 1", 89, "Can you tell me your full name and what brought you in?"),
            (11, "Speaker 3", None, "Good morning."),
            (13, "Speaker 3", None, "My name is John."),
            (18, "Patient", 78, "I've been having a headache and I've also felt dizzy a few times today."),
            (23, "Nurse 2", 86, "I'm Michael, the other nurse helping with your care."),
            (27, "Nurse 2", 82, "When did the headache and dizziness start?"),
            (33, "Patient", 80, "The headache started this morning. The dizziness came on later, especially when I stood up."),
            (39, "Nurse 1", 88, "On a scale of zero to ten, how bad is your headache?"),
            (43, "Patient", 84, "I would say it's about a five out of ten."),
            (49, "Nurse 2", 80, "Have you had nausea, blurred vision, chest pain, trouble breathing, or weakness?"),
            (54, "Patient", 88, "I haven't had chest pain or trouble breathing."),
            (58, "Patient", 83, "I felt a little nauseous, but my vision seems normal."),
            (63, "Nurse 1", 91, "Thank you for telling us. Please stay seated while I check your vital signs."),
            (68, "Patient", 82, "Okay, I'll stay here."),
            (73, "Nurse 2", 85, "Since you felt dizzy when standing, please don't get up or walk by yourself for now."),
            (78, "Patient", 90, "I understand. I was worried I might lose my balance."),
            (83, "Nurse 1", 88, "We'll help you if you need to stand."),
            (88, "Nurse 1", 86, "Have you had anything to eat or drink today?"),
            (93, "Patient", 81, "I had a small breakfast, but I haven't had much water."),
            (99, "Nurse 2", 84, "Thanks for letting us know. We'll share that with the health care provider."),
            (106,"Nurse 1", 87, "Is there anything else you need right now?"),
            (111,"Patient", 85, "No thank you. I feel better knowing you're checking on me."),
            (116,"Nurse 1", 90, "You're welcome, John. Please use the call button if you need us."),
        ],
    },

    "Medication Safety": {
        "patient": "Maria Lopez",
        "caregiver": "None",
        "reason": "Medication review",
        "baseline_ao": 4,
        "current_ao": 4,
        "cue_at": 22,
        "cue_category": "Medication Safety",
        "cue_level": "Review",
        "cue_quote": "I don't know which pill I'm supposed to take in the afternoon.",
        "nursebot_response": (
            "Thank you for telling me. We can review your medication list "
            "with you one medication at a time."
        ),
        "nurse_next_step": (
            "Review the medication list, timing, dose, and recent adherence. "
            "Escalate possible duplicate or missed dosing according to clinical procedure."
        ),
        "lines": [
            (4, "Nurse 1", 93, "Good afternoon. We're going to review your medications together."),
            (9, "Patient", 82, "I'm worried because there are several new pills."),
            (14,"Nurse 2", 86, "Can you tell us what has been difficult?"),
            (22,"Patient", 90, "I don't know which pill I'm supposed to take in the afternoon."),
            (29,"Nurse 1", 92, "Thank you for telling us. We'll go through them one at a time."),
            (35,"Patient", 85, "I also think I may have missed one yesterday."),
            (42,"Nurse 2", 88, "We'll review your medication list and timing with you."),
        ],
    },

    "Disorientation / Confusion": {
        "patient": "Eleanor Brown",
        "caregiver": "Daughter",
        "reason": "Post-discharge follow-up",
        "baseline_ao": 4,
        "current_ao": 2,
        "cue_at": 20,
        "cue_category": "Disorientation / Confusion",
        "cue_level": "Review",
        "cue_quote": "I don't know where I am. What day is it?",
        "nursebot_response": (
            "You are safe. We can take this one step at a time. "
            "Can you tell me your name and where you are right now?"
        ),
        "nurse_next_step": (
            "Reorient the patient to person, place, time, and situation, "
            "then assess orientation with simple follow-up questions."
        ),
        "lines": [
            (4, "Nurse 1", 94, "Good morning. Can you tell me your name?"),
            (9, "Patient", 79, "My name is Eleanor."),
            (14,"Nurse 1", 89, "Do you know where we are right now?"),
            (20,"Patient", 77, "I don't know where I am. What day is it?"),
            (27,"Nurse 2", 88, "That's okay. We can go through it together."),
            (34,"Patient", 73, "I thought I was at home."),
        ],
    },

    "Urgent Self-Harm Statement": {
        "patient": "Test Patient",
        "caregiver": "None",
        "reason": "Behavioral health screening",
        "baseline_ao": 4,
        "current_ao": 4,
        "cue_at": 24,
        "cue_category": "Suicide / Self-Harm Risk Language",
        "cue_level": "Urgent Review",
        "cue_quote": "I don't want to live anymore.",
        "nursebot_response": (
            "Thank you for telling me. I am going to get a nurse to stay "
            "with you and talk with you right away."
        ),
        "nurse_next_step": (
            "URGENT: Keep the patient under appropriate observation and follow "
            "the approved suicide-risk assessment and escalation procedure."
        ),
        "lines": [
            (4, "Nurse 1", 93, "You've seemed quieter today. Can you tell me how you're feeling?"),
            (11,"Patient", 79, "I feel like nothing is going to get better."),
            (17,"Nurse 1", 91, "Can you tell me more about what you mean?"),
            (24,"Patient", 92, "I don't want to live anymore."),
            (30,"Nurse 1", 95, "Thank you for telling me. I'm going to stay with you and get additional help right away."),
        ],
    },
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
DEFAULTS = {
    "training_scenario": "Perfect Recognition Demo",
    "study_mode": "Mode 2 - Scripted Responses",
    "session_state": "Ready",
    "started_at": None,
    "paused_at": None,
    "total_paused": 0.0,
    "stopped_elapsed": 0.0,
    "cue_feedback": [],
    "cue_dismissed": False,
    "cue_acknowledged": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

MODES = [
    "Mode 1 - Observe Only",
    "Mode 2 - Scripted Responses",
    "Mode 3 - Caregiver-Led",
    "Mode 4 - Robot Detects, Caregiver Responds",
]

def current_elapsed():
    if st.session_state.started_at is None:
        return 0.0

    if st.session_state.session_state == "Paused":
        end = st.session_state.paused_at or time.time()
    elif st.session_state.session_state in ("Stopped", "Completed"):
        return float(st.session_state.stopped_elapsed)
    else:
        end = time.time()

    return max(
        0.0,
        end - st.session_state.started_at - st.session_state.total_paused
    )

def start_session():
    st.session_state.session_state = "Running"
    st.session_state.started_at = time.time()
    st.session_state.paused_at = None
    st.session_state.total_paused = 0.0
    st.session_state.stopped_elapsed = 0.0
    st.session_state.cue_feedback = []
    st.session_state.cue_dismissed = False
    st.session_state.cue_acknowledged = False

def pause_session():
    if st.session_state.session_state == "Running":
        st.session_state.session_state = "Paused"
        st.session_state.paused_at = time.time()

def resume_session():
    if st.session_state.session_state == "Paused":
        now = time.time()
        if st.session_state.paused_at is not None:
            st.session_state.total_paused += now - st.session_state.paused_at
        st.session_state.paused_at = None
        st.session_state.session_state = "Running"

def stop_session():
    if st.session_state.started_at is not None:
        st.session_state.stopped_elapsed = current_elapsed()
    st.session_state.session_state = "Stopped"
    st.session_state.paused_at = None

def confidence_class(conf):
    if conf is None:
        return "identity-uncertain"
    if conf < 50:
        return "confidence-red"
    if conf < 70:
        return "confidence-orange"
    if conf < 85:
        return "confidence-yellow"
    return "confidence-green"

def format_elapsed(seconds):
    seconds = max(0, int(seconds))
    return str(timedelta(seconds=seconds))

# --------------------------------------------------
# HEADER — same desktop labels
# --------------------------------------------------
header_left, header_right = st.columns([1, 1])
with header_left:
    st.markdown('<div class="nb-title">NurseBot Test</div>', unsafe_allow_html=True)
with header_right:
    st.markdown(
        '<div style="text-align:right" class="nb-header-right">'
        'Models: Training Simulation &nbsp;&nbsp;&nbsp; '
        '<span style="color:#137333">Microphone: Simulated</span>'
        '</div>',
        unsafe_allow_html=True,
    )

# Scenario is a training setup item, not a live session control.
with st.expander("Training Setup", expanded=False):
    selected = st.selectbox(
        "Scripted training scenario",
        list(SCENARIOS.keys()),
        index=list(SCENARIOS.keys()).index(st.session_state.training_scenario),
        disabled=st.session_state.session_state in ("Running", "Paused"),
    )
    if selected != st.session_state.training_scenario:
        st.session_state.training_scenario = selected
        st.session_state.session_state = "Ready"
        st.session_state.started_at = None
        st.session_state.stopped_elapsed = 0.0
        st.session_state.cue_dismissed = False
        st.session_state.cue_acknowledged = False

scenario = SCENARIOS[st.session_state.training_scenario]

session_tab, patient_tab, alerts_tab, video_tab = st.tabs(
    ["Session", "Patient & Readings", "Alerts / Events", "Video"]
)

# --------------------------------------------------
# SESSION TAB
# --------------------------------------------------
with session_tab:
    st.markdown(
        '<div class="groupbox compact"><div class="legend">Session Controls</div>',
        unsafe_allow_html=True
    )

    c_mode, c_start, c_pause, c_resume, c_stop, c_status, c_processing = st.columns(
        [2.4, .7, .7, .8, .7, 1.7, 1.3]
    )

    with c_mode:
        mode = st.selectbox(
            "Study Mode:",
            MODES,
            index=MODES.index(st.session_state.study_mode),
            label_visibility="visible",
        )
        st.session_state.study_mode = mode

    with c_start:
        st.write("")
        if st.button(
            "Start",
            use_container_width=True,
            disabled=st.session_state.session_state in ("Running", "Paused"),
        ):
            start_session()
            st.rerun()

    with c_pause:
        st.write("")
        if st.button(
            "Pause",
            use_container_width=True,
            disabled=st.session_state.session_state != "Running",
        ):
            pause_session()
            st.rerun()

    with c_resume:
        st.write("")
        if st.button(
            "Resume",
            use_container_width=True,
            disabled=st.session_state.session_state != "Paused",
        ):
            resume_session()
            st.rerun()

    with c_stop:
        st.write("")
        if st.button(
            "Stop",
            use_container_width=True,
            disabled=st.session_state.session_state not in ("Running", "Paused"),
        ):
            stop_session()
            st.rerun()

    with c_status:
        st.caption("Status:")
        status = st.session_state.session_state
        status_class = (
            "status-running" if status == "Running"
            else "status-paused" if status == "Paused"
            else "status-stopped" if status in ("Stopped", "Completed")
            else ""
        )
        st.markdown(
            f'<span class="{status_class}">{status}</span> &nbsp; • &nbsp; '
            f'<span id="elapsed">{format_elapsed(current_elapsed())}</span>',
            unsafe_allow_html=True,
        )

    with c_processing:
        st.selectbox(
            "Processing:",
            ["Fast Live"],
            index=0,
            disabled=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Visible because it exists in the real NurseBot UI, but disabled for training.
    st.markdown(
        '<div class="groupbox compact"><div class="legend">Nurse Voice Enrollment</div>',
        unsafe_allow_html=True
    )
    e1, e2, e3, e4, e5 = st.columns([1.3, 1.1, 1.2, 1.1, 2.5])
    with e1:
        st.selectbox("Enrollment:", ["30 sec"], disabled=True)
    with e2:
        st.button("Enroll Nurse 1", disabled=True, use_container_width=True)
    with e3:
        st.caption("Nurse 1: training voice")
    with e4:
        st.button("Enroll Nurse 2", disabled=True, use_container_width=True)
    with e5:
        st.caption("Voice enrollment is simulated in the training application.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="groupbox"><div class="legend">Live Captions + Finalized Transcript</div>',
        unsafe_allow_html=True
    )

    @st.fragment(run_every=1.0)
    def live_simulation():
        elapsed = current_elapsed()
        state = st.session_state.session_state
        lines = scenario["lines"]

        if state == "Running" and lines and elapsed >= lines[-1][0] + 3:
            st.session_state.stopped_elapsed = elapsed
            st.session_state.session_state = "Completed"
            state = "Completed"

        visible_lines = [line for line in lines if line[0] <= elapsed]

        if visible_lines:
            current_line = visible_lines[-1]
            partial_status = (
                "Fast Live — simulated committed sentence"
                if state == "Running"
                else f"Simulation {state.lower()}"
            )
            partial_caption = current_line[3]
        else:
            partial_status = (
                "Fast Live — waiting for scripted conversation..."
                if state in ("Ready", "Running")
                else f"Simulation {state.lower()}"
            )
            partial_caption = "Listening..." if state == "Running" else ""

        st.markdown(
            '<div class="groupbox compact"><div class="legend">Live Caption (temporary)</div>'
            f'<div class="caption-status">{partial_status}</div>'
            f'<div class="caption-text">{partial_caption}</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        cue_visible = (
            elapsed >= scenario["cue_at"]
            and not st.session_state.cue_dismissed
        )

        st.markdown(
            '<div class="groupbox"><div class="legend">'
            'Patient Cue — NurseBot Response / Nurse Next Step</div>',
            unsafe_allow_html=True,
        )

        if cue_visible:
            urgent = scenario["cue_level"] == "Urgent Review"
            cue_class = "cue-category-urgent" if urgent else "cue-category"
            h1, h2 = st.columns([4, 1])
            with h1:
                st.markdown(
                    f'<div class="{cue_class}">{scenario["cue_category"]}</div>',
                    unsafe_allow_html=True,
                )
            with h2:
                st.markdown(
                    f'<div style="text-align:right;font-weight:700">{scenario["cue_level"]}</div>',
                    unsafe_allow_html=True,
                )

            st.markdown(
                f'<div class="cue-quote">Detected Patient cue: '
                f'“{scenario["cue_quote"]}”</div>',
                unsafe_allow_html=True,
            )

            r1, r2 = st.columns(2)
            with r1:
                st.markdown(
                    '<div class="response-box"><div class="response-title">'
                    'NurseBot May Say</div>'
                    f'{scenario["nursebot_response"]}</div>',
                    unsafe_allow_html=True,
                )
            with r2:
                st.markdown(
                    '<div class="response-box"><div class="response-title">'
                    'Nurse Next Step</div>'
                    f'{scenario["nurse_next_step"]}</div>',
                    unsafe_allow_html=True,
                )

            a1, a2, a3, a4, a5 = st.columns([1.2, 1.1, 1.1, 1.6, 3.0])
            with a1:
                if st.button("Speak Response", use_container_width=True):
                    st.session_state.cue_feedback.append(
                        (st.session_state.training_scenario, "Speak Response")
                    )
                    st.toast("Training action recorded: Speak Response")
            with a2:
                if st.button("Cue Correct", use_container_width=True):
                    st.session_state.cue_feedback.append(
                        (st.session_state.training_scenario, "Cue Correct")
                    )
                    st.toast("Feedback saved")
            with a3:
                if st.button("Cue Incorrect", use_container_width=True):
                    st.session_state.cue_feedback.append(
                        (st.session_state.training_scenario, "Cue Incorrect")
                    )
                    st.toast("Feedback saved")
            with a4:
                if st.button("Response Appropriate", use_container_width=True):
                    st.session_state.cue_feedback.append(
                        (st.session_state.training_scenario, "Response Appropriate")
                    )
                    st.toast("Feedback saved")
            with a5:
                if st.button("Dismiss", use_container_width=False):
                    st.session_state.cue_dismissed = True
                    st.session_state.cue_feedback.append(
                        (st.session_state.training_scenario, "Dismissed")
                    )
                    st.rerun(scope="fragment")
        else:
            st.markdown(
                '<div class="training-note">'
                'A suggested nurse response will appear here when a Patient cue is recognized.'
                '</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="groupbox"><div class="legend">Finalized / Committed Transcript</div>',
            unsafe_allow_html=True,
        )

        html = '<div class="transcript">'
        if not visible_lines:
            if state == "Ready":
                html += '<span class="training-note">Press Start to begin the scripted NurseBot simulation.</span>'
            elif state == "Running":
                html += '<span class="training-note">Listening...</span>'

        for sec, speaker, conf, text in visible_lines:
            stamp = f"00:{sec//60:02d}:{sec%60:02d}"
            if conf is None:
                label = f'{speaker} (identity uncertain)'
                css = "identity-uncertain"
            else:
                label = f'{speaker} ({conf}% confidence)'
                css = confidence_class(conf)

            html += (
                f'<div class="line">[{stamp}] '
                f'<span class="{css}">{label}</span>: {text}</div>'
            )

        if state == "Completed":
            html += '<br><b>=== SIMULATED SESSION COMPLETE ===</b>'

        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if state in ("Running", "Paused"):
            st.caption(
                f"Status: {state}  •  Elapsed: {format_elapsed(elapsed)}  •  "
                "Training transcript is scripted."
            )

    live_simulation()

    bottom1, bottom2 = st.columns([4, 1])
    with bottom1:
        st.checkbox("Retain raw audio after session", value=False, disabled=True)
    with bottom2:
        st.button("Export TXT + CSV", disabled=True, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# PATIENT & READINGS TAB
# --------------------------------------------------
with patient_tab:
    st.markdown(
        '<div class="groupbox"><div class="legend">Patient Information</div>',
        unsafe_allow_html=True
    )
    p1, p2, p3, p4 = st.columns(4)
    p1.text_input("Patient", scenario["patient"], disabled=True)
    p2.number_input("Baseline A&O", 0, 4, scenario["baseline_ao"], disabled=True)
    p3.number_input("Current A&O", 0, 4, scenario["current_ao"], disabled=True)
    p4.text_input("Caregiver", scenario["caregiver"], disabled=True)
    st.text_input("Reason for visit", scenario["reason"], disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="groupbox"><div class="legend">Readings</div>',
        unsafe_allow_html=True
    )
    r1, r2, r3, r4 = st.columns(4)
    r1.number_input("Systolic BP", value=118, disabled=True)
    r2.number_input("Heart Rate", value=76, disabled=True)
    r3.number_input("Glucose", value=105, disabled=True)
    r4.number_input("Weight", value=155, disabled=True)
    st.caption("Training simulation only — readings are fictional.")
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# ALERTS / EVENTS TAB
# --------------------------------------------------
with alerts_tab:
    elapsed = current_elapsed()
    rows = []

    if elapsed >= scenario["cue_at"]:
        rows.append({
            "Type": "Cue-Driven Patient Review",
            "Level": scenario["cue_level"],
            "Status": "Dismissed" if st.session_state.cue_dismissed else "New",
            "Detail": scenario["cue_category"],
        })

    for scen, feedback in st.session_state.cue_feedback:
        rows.append({
            "Type": "Nurse Cue Feedback",
            "Level": "Log Only",
            "Status": feedback,
            "Detail": scen,
        })

    st.markdown(
        '<div class="groupbox"><div class="legend">Alerts / Events</div>',
        unsafe_allow_html=True
    )
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No alerts or events have been recorded in this training session.")
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# VIDEO TAB
# --------------------------------------------------
with video_tab:
    st.markdown(
        '<div class="groupbox"><div class="legend">Video</div>',
        unsafe_allow_html=True
    )
    st.info(
        "Video is not active in the NurseBot training simulation. "
        "This tab is included so students see the same navigation as the local NurseBot interface."
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(
    "NurseBot Training Simulation — fictional patient scenarios only. "
    "For orientation/usability testing; not for clinical care."
)
