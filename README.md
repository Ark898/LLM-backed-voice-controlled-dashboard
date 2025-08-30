# ORIONAI 🎤📊

A **voice- and text-controlled data dashboard** powered by **LLM/NLP models** and **OpenAI Whisper**, built with **Streamlit** and **Plotly**. Visualize, filter, and analyze datasets using natural language commands—no coding required!

---

## 🚀 Features

- **Voice Commands**: Speak to control the dashboard.  
  Example:  
  - “Show life expectancy in Asia for 2007”  
  - “Hide the chart”  
  - “Switch metric to GDP per Capita”
- **Text Commands**: Manual input supported alongside voice.  
- **Dynamic Charts**: Bar or line charts rendered with Plotly.  
- **Data Table**: View filtered data in an interactive table.  
- **Quick Insights**: Dashboard summarizes key stats (countries, region, year).  
- **Export Data**: Download filtered view as CSV.  
- **Seamless UI**: Unified dashboard experience with collapsible sections.  

---

## 🗣 How It Works

1. **Voice / Text Input**  
   The user speaks a command using the microphone or types it manually in the input box.

2. **Parsing**  
   A custom parser interprets the command to identify:
   - Metric (e.g., GDP per Capita, Life Expectancy, Population)  
   - Year  
   - Region / Continent  
   - Chart type (bar or line)  
   - Chart visibility (show/hide)

3. **State Update**  
   Streamlit's session state is updated based on the parsed command.

4. **UI Update**  
   Charts, tables, and insights automatically refresh to reflect the updated state.

## 🚀 Future Enhancements

- **Multi-Metric Comparison Charts**  
  Allow users to visualize multiple metrics on the same chart for better insights.

- **Integrate OpenAI GPT**  
  Use GPT models for richer and more natural command understanding.

- **Real-Time Data Streaming Support**  
  Enable dynamic updates of charts and tables as new data comes in.

- **Custom Dashboards for Multiple Datasets**  
  Allow users to create and switch between dashboards for different datasets.


## 💻 Tech Stack

- **Frontend / UI**: Streamlit, Plotly  
- **Voice Recognition**: OpenAI Whisper + Streamlit Mic Recorder  
- **Data Processing**: Pandas  
- **Language Understanding**: Custom parser for natural language commands  
- **Optional LLM Integration**: OpenAI GPT for advanced command interpretation  

---
## ⚙️ Setup & Installation

```bash
git clone https://github.com/your-username/reponame.git
cd reponame
python -m venv .venv
# Activate the environment
# Linux / Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
# Set up OpenAI API key in .env file
OPENAI_API_KEY=your_openai_api_key_here
#Run the dashboard
streamlit run app.py

