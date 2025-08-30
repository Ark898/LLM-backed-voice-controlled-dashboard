# # app.py
# import re
# import streamlit as st
# import pandas as pd
# import plotly.express as px


# # ------------------------
# # Sample data
# # ------------------------
# df = px.data.gapminder()
# METRICS = {"gdpPercap": "GDP per Capita", "lifeExp": "Life Expectancy", "pop": "Population"}
# REVERSE_METRICS = {v.lower(): k for k, v in METRICS.items()}
# YEARS = sorted(df["year"].unique())
# REGIONS = sorted(df["continent"].unique())

# # ------------------------
# # Initialize session state
# # ------------------------
# def init_state():
#     defaults = {
#         "metric": "gdpPercap",
#         "year": None,
#         "region": None,
#         "chart_type": "bar",
#         "chart_visible": True,
#         "last_cmd": None
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v
#         if "user_text" not in st.session_state:
#             st.session_state["user_text"] = ""

# init_state()

# # ------------------------
# # Mock parser for text commands
# # ------------------------
# def mock_parse(user_text: str) -> dict:
#     u = user_text.lower()
#     cmd = {"action": "update", "target": "chart1", "property": None, "value": None}

#     # year
#     y = re.search(r"\b(19[5-9]\d|200[0-7])\b", u)
#     if y:
#         cmd["property"] = "year"
#         cmd["value"] = int(y.group(0))
#         return cmd

#     # metric
#     for disp, key in [(v.lower(), k) for k,v in METRICS.items()]:
#         if disp in u or key.lower() in u:
#             cmd["property"] = "metric"
#             cmd["value"] = key
#             return cmd

#     # region
#     for r in REGIONS:
#         if r.lower() in u:
#             cmd["property"] = "region"
#             cmd["value"] = r
#             return cmd

#     # chart type
#     if "line" in u:
#         cmd["property"] = "chart_type"; cmd["value"] = "line"; return cmd
#     if "bar" in u:
#         cmd["property"] = "chart_type"; cmd["value"] = "bar"; return cmd

#     # hide/show
#     if any(w in u for w in ["hide", "remove", "close"]):
#         cmd["property"] = "chart_visible"; cmd["value"] = False; return cmd
#     if any(w in u for w in ["show", "display", "open"]):
#         cmd["property"] = "chart_visible"; cmd["value"] = True; return cmd

#     # fallback
#     return {"action": "none"}

# # ------------------------
# # Apply command to session state
# # ------------------------
# def apply_command(cmd: dict):
#     if not cmd or cmd.get("action") in (None, "none"):
#         st.warning("Command could not be parsed or is empty.")
#         return

#     prop = cmd.get("property")
#     val = cmd.get("value")

#     if prop == "metric" and val in METRICS:
#         st.session_state["metric"] = val
#     elif prop == "year":
#         if val in YEARS:
#             st.session_state["year"] = val
#     elif prop == "region":
#         if val in REGIONS:
#             st.session_state["region"] = val
#     elif prop == "chart_type" and val in ["bar","line"]:
#         st.session_state["chart_type"] = val
#     elif prop == "chart_visible":
#         st.session_state["chart_visible"] = bool(val)
#     else:
#         st.info(f"No action for property: {prop}")

#     st.session_state["last_cmd"] = cmd
#     # No rerun needed; Streamlit automatically refreshes

# # ------------------------
# # UI
# # ------------------------
# st.title("📝 Text-Controlled Dashboard Prototype")
# st.markdown("Type commands like: 'Switch metric to life expectancy', 'Set year to 1997', 'Hide the chart'.")

# # Command input
# st.text_input("Enter your command:", key="user_text")
# if st.button("Run command"):
#     parsed_cmd = mock_parse(st.session_state["user_text"].strip())
#     st.subheader("Parsed command")
#     st.json(parsed_cmd)
#     apply_command(parsed_cmd)

# # Dashboard display
# display_metric = st.session_state["metric"]
# display_year = st.session_state["year"]
# display_region = st.session_state["region"]

# filtered = df.copy()
# if display_region:
#     filtered = filtered[filtered["continent"] == display_region]
# if display_year:
#     filtered = filtered[filtered["year"] == display_year]

# plot_df = filtered.sort_values(display_metric, ascending=False).copy()

# if st.session_state["chart_visible"] and not plot_df.empty:
#     if st.session_state["chart_type"] == "bar":
#         fig = px.bar(plot_df, x="country", y=display_metric,
#                      title=f"{METRICS[display_metric]} - {display_region or 'All'} {display_year or ''}")
#     else:
#         fig = px.line(plot_df, x="country", y=display_metric,
#                       title=f"{METRICS[display_metric]} - {display_region or 'All'} {display_year or ''}")
#     st.plotly_chart(fig, use_container_width=True)
# else:
#     st.info("Chart hidden or no data available for selected filters.")

# st.subheader("Data Table")
# st.dataframe(plot_df[["country","continent","year",display_metric]].reset_index(drop=True))

# st.markdown("---")
# st.write("Last applied command:")
# st.json(st.session_state.get("last_cmd"))

# # CSV export
# csv = plot_df[["country","continent","year",display_metric]].to_csv(index=False).encode("utf-8")
# st.download_button("Export current view as CSV", csv, file_name="dashboard_view.csv")

# app.py
# import os
# import re
# import tempfile
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import sounddevice as sd
# from scipy.io.wavfile import write
# import openai
# from dotenv import load_dotenv

# # ------------------------
# # Load API key
# # ------------------------
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # ------------------------
# # Sample data
# # ------------------------
# df = px.data.gapminder()
# METRICS = {"gdpPercap": "GDP per Capita", "lifeExp": "Life Expectancy", "pop": "Population"}
# REVERSE_METRICS = {v.lower(): k for k, v in METRICS.items()}
# YEARS = sorted(df["year"].unique())
# REGIONS = sorted(df["continent"].unique())

# # ------------------------
# # Initialize session state
# # ------------------------
# def init_state():
#     defaults = {
#         "metric": "gdpPercap",
#         "year": None,
#         "region": None,
#         "chart_type": "bar",
#         "chart_visible": True,
#         "last_cmd": None,
#         "user_text": ""
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# init_state()

# # ------------------------
# # Record from microphone
# # ------------------------
# def record_audio(duration=5, fs=44100):
#     st.info("🎙 Recording... Speak now!")
#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
#     sd.wait()  # wait until recording is finished
#     temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
#     write(temp_file.name, fs, recording)  # Save as WAV
#     return temp_file.name

# # ------------------------
# # Transcribe with Whisper
# # ------------------------
# def transcribe_audio(file_path):
#     with open(file_path, "rb") as f:
#         transcript = openai.audio.transcriptions.create(
#             model="whisper-1",
#             file=f
#         )
#     return transcript.text

# # ------------------------
# # Mock parser for text commands
# # ------------------------
# def mock_parse(user_text: str) -> dict:
#     u = user_text.lower()
#     cmd = {"action": "update", "target": "chart1", "property": None, "value": None}

#     # year
#     y = re.search(r"\b(19[5-9]\d|200[0-7])\b", u)
#     if y:
#         cmd["property"] = "year"
#         cmd["value"] = int(y.group(0))
#         return cmd

#     # metric
#     for disp, key in [(v.lower(), k) for k,v in METRICS.items()]:
#         if disp in u or key.lower() in u:
#             cmd["property"] = "metric"
#             cmd["value"] = key
#             return cmd

#     # region
#     for r in REGIONS:
#         if r.lower() in u:
#             cmd["property"] = "region"
#             cmd["value"] = r
#             return cmd

#     # chart type
#     if "line" in u:
#         cmd["property"] = "chart_type"; cmd["value"] = "line"; return cmd
#     if "bar" in u:
#         cmd["property"] = "chart_type"; cmd["value"] = "bar"; return cmd

#     # hide/show
#     if any(w in u for w in ["hide", "remove", "close"]):
#         cmd["property"] = "chart_visible"; cmd["value"] = False; return cmd
#     if any(w in u for w in ["show", "display", "open"]):
#         cmd["property"] = "chart_visible"; cmd["value"] = True; return cmd

#     # fallback
#     return {"action": "none"}

# # ------------------------
# # Apply command to session state
# # ------------------------
# def apply_command(cmd: dict):
#     if not cmd or cmd.get("action") in (None, "none"):
#         st.warning("Command could not be parsed or is empty.")
#         return

#     prop = cmd.get("property")
#     val = cmd.get("value")

#     if prop == "metric" and val in METRICS:
#         st.session_state["metric"] = val
#     elif prop == "year":
#         if val in YEARS:
#             st.session_state["year"] = val
#     elif prop == "region":
#         if val in REGIONS:
#             st.session_state["region"] = val
#     elif prop == "chart_type" and val in ["bar","line"]:
#         st.session_state["chart_type"] = val
#     elif prop == "chart_visible":
#         st.session_state["chart_visible"] = bool(val)
#     else:
#         st.info(f"No action for property: {prop}")

#     st.session_state["last_cmd"] = cmd
#     # No rerun needed; Streamlit automatically refreshes

# # ------------------------
# # UI
# # ------------------------
# st.title("📝 Voice + Text Controlled Dashboard")
# st.markdown("Try commands like: 'Switch metric to life expectancy', 'Set year to 1997', 'Show Asia 2002', 'Hide chart'.")

# # ------------------------
# # Text command input
# # ------------------------
# st.text_input("Enter your command:", key="user_text")
# if st.button("Run command"):
#     parsed_cmd = mock_parse(st.session_state["user_text"].strip())
#     st.subheader("Parsed command (text)")
#     st.json(parsed_cmd)
#     apply_command(parsed_cmd)

# # ------------------------
# # Voice command input
# # ------------------------
# st.markdown("### 🎤 Or use your voice")
# if st.button("Record Voice Command"):
#     audio_file = record_audio(duration=5)  # Record 5 seconds
#     user_text = transcribe_audio(audio_file)
#     st.success(f"📝 Transcribed: {user_text}")

#     st.session_state["user_text"] = user_text
#     parsed_cmd = mock_parse(user_text)
#     st.subheader("Parsed command (voice)")
#     st.json(parsed_cmd)
#     apply_command(parsed_cmd)

# # ------------------------
# # Dashboard display
# # ------------------------
# display_metric = st.session_state["metric"]
# display_year = st.session_state["year"]
# display_region = st.session_state["region"]

# filtered = df.copy()
# if display_region:
#     filtered = filtered[filtered["continent"] == display_region]
# if display_year:
#     filtered = filtered[filtered["year"] == display_year]

# plot_df = filtered.sort_values(display_metric, ascending=False).copy()

# if st.session_state["chart_visible"] and not plot_df.empty:
#     if st.session_state["chart_type"] == "bar":
#         fig = px.bar(plot_df, x="country", y=display_metric,
#                      title=f"{METRICS[display_metric]} - {display_region or 'All'} {display_year or ''}")
#     else:
#         fig = px.line(plot_df, x="country", y=display_metric,
#                       title=f"{METRICS[display_metric]} - {display_region or 'All'} {display_year or ''}")
#     st.plotly_chart(fig, use_container_width=True)
# else:
#     st.info("Chart hidden or no data available for selected filters.")

# # ------------------------
# # Data table + export
# # ------------------------
# st.subheader("Data Table")
# st.dataframe(plot_df[["country","continent","year",display_metric]].reset_index(drop=True))

# st.markdown("---")
# st.write("Last applied command:")
# st.json(st.session_state.get("last_cmd"))

# csv = plot_df[["country","continent","year",display_metric]].to_csv(index=False).encode("utf-8")
# st.download_button("Export current view as CSV", csv, file_name="dashboard_view.csv")


import re
import streamlit as st
import pandas as pd
import plotly.express as px
import whisper
from streamlit_mic_recorder import mic_recorder
from ui import render_ui

# ------------------------
# Load Whisper model once
# ------------------------
@st.cache_resource
def load_model():
    return whisper.load_model("small")  # you can use "tiny", "small", "medium", "large"
model = load_model()

# ------------------------
# Sample data
# ------------------------
df = px.data.gapminder()
METRICS = {"gdpPercap": "GDP per Capita", "lifeExp": "Life Expectancy", "pop": "Population"}
YEARS = sorted(df["year"].unique())
REGIONS = sorted(df["continent"].unique())

# ------------------------
# Initialize session state
# ------------------------
def init_state():
    defaults = {
        "metric": "gdpPercap",
        "year": None,
        "region": None,
        "chart_type": "bar",
        "chart_visible": True,
        "last_cmd": None,
        "user_text": ""
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_state()

# ------------------------
# Parser for voice/text commands
# ------------------------
def parse_command(user_text: str) -> dict:
    u = user_text.lower()
    cmd = {"action": "update", "target": "chart1", "property": None, "value": None}

    # year
    y = re.search(r"\b(19[5-9]\d|200[0-7])\b", u)
    if y:
        cmd["property"] = "year"
        cmd["value"] = int(y.group(0))
        return cmd

    # metric
    for key, disp in METRICS.items():
        if disp.lower() in u or key.lower() in u:
            cmd["property"] = "metric"
            cmd["value"] = key
            return cmd

    # region
    for r in REGIONS:
        if r.lower() in u:
            cmd["property"] = "region"
            cmd["value"] = r
            return cmd

    # chart type
    if "line" in u:
        return {"property": "chart_type", "value": "line", "action": "update", "target": "chart1"}
    if "bar" in u:
        return {"property": "chart_type", "value": "bar", "action": "update", "target": "chart1"}

    # hide/show
    if any(w in u for w in ["hide", "remove", "close"]):
        return {"property": "chart_visible", "value": False, "action": "update", "target": "chart1"}
    if any(w in u for w in ["show", "display", "open"]):
        return {"property": "chart_visible", "value": True, "action": "update", "target": "chart1"}

    return {"action": "none"}

# ------------------------
# Apply command
# ------------------------
def apply_command(cmd: dict):
    if not cmd or cmd.get("action") == "none":
        return
    prop, val = cmd.get("property"), cmd.get("value")
    if prop == "metric" and val in METRICS:
        st.session_state["metric"] = val
    elif prop == "year" and val in YEARS:
        st.session_state["year"] = val
    elif prop == "region" and val in REGIONS:
        st.session_state["region"] = val
    elif prop == "chart_type" and val in ["bar","line"]:
        st.session_state["chart_type"] = val
    elif prop == "chart_visible":
        st.session_state["chart_visible"] = bool(val)
    st.session_state["last_cmd"] = cmd

# ------------------------
# UI
# ------------------------
st.title("🎤 Voice-Controlled Dashboard")
st.markdown("Speak commands like: *'Show life expectancy in Asia for 2007'* or *'Hide the chart'*.")

# --- 🎙️ Mic Recorder ---
audio = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="⏹ Stop Recording", key="recorder")

if audio is not None:
    with open("temp.wav", "wb") as f:
        f.write(audio["bytes"])
    result = model.transcribe("temp.wav", fp16=False)
    user_text = result["text"]
    st.session_state["user_text"] = user_text
    st.success(f"Recognized: {user_text}")

    # Parse & apply
    cmd = parse_command(user_text)
    st.json(cmd)
    apply_command(cmd)

# Also allow manual text input
user_text_input = st.text_input("Or type your command:", value=st.session_state["user_text"])
if st.button("Run text command"):
    cmd = parse_command(user_text_input)
    st.json(cmd)
    apply_command(cmd)

# ------------------------
# Dashboard Display
# ------------------------
display_metric = st.session_state["metric"]
display_year = st.session_state["year"]
display_region = st.session_state["region"]

filtered = df.copy()
if display_region:
    filtered = filtered[filtered["continent"] == display_region]
if display_year:
    filtered = filtered[filtered["year"] == display_year]
plot_df = filtered.sort_values(display_metric, ascending=False)

# Initialize fig
fig = None

if st.session_state["chart_visible"] and not plot_df.empty:
    if st.session_state["chart_type"] == "bar":
        fig = px.bar(
            plot_df, x="country", y=display_metric,
            title=f"{METRICS[display_metric]} - {display_region or 'All'} {display_year or ''}"
        )
    else:
        fig = px.line(
            plot_df, x="country", y=display_metric,
            title=f"{METRICS[display_metric]} - {display_region or 'All'} {display_year or ''}"
        )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Chart hidden or no data available.")

st.subheader("Data Table")
st.dataframe(plot_df[["country","continent","year",display_metric]].reset_index(drop=True))

st.markdown("---")
st.write("Last applied command:")
st.json(st.session_state.get("last_cmd"))

# ✅ Safely call render_ui
render_ui(
    plot_df[["country", "continent", "year", display_metric]],
    fig
)
