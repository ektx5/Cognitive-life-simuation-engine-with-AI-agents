# Cognitive Life Simulation Engine (with AI Agents)

This project is a multi-agent social simulation environment where multiple AI personas interact dynamically in a group chat setting. Using the Google Gemini API, agents with distinct personalities converse, interpret messages, and continuously update their internal cognitive states (such as stress levels and emotions).

## 🚀 Features

- **Multi-Agent Architecture:** Five unique agents (Serious, Lazy, Extrovert, Logical, Anxious) interacting autonomously.
- **Dynamic Cognitive States:** Agents track and adjust their `emotion` and `stress` dynamically based on the ongoing conversation context.
- **Robust API Handling:** Intelligent request handling using `gemini-2.5-flash-lite`, including automated fallback logic for rate limits. 
- **Web Interface:** Built on Flask, providing a clean, browser-based UI to Start, Step, and Stop the simulation while monitoring agents' states.

## 🛠️ Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ektx5/Cognitive-life-simuation-engine-with-AI-agents.git
   cd Cognitive-life-simuation-engine-with-AI-agents
   ```

2. **Setup Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate # On Windows
   ```

3. **Install Dependencies:**
   Ensure you have Flask and the OpenAI Python client installed.
   ```bash
   pip install flask openai
   ```

4. **Run the Simulation Engine:**
   ```bash
   python app.py
   ```

5. **Access the Interface:**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## 🧠 How It Works
- The engine initiates a group conversation.
- At each step, an agent is randomly selected (excluding the previous speaker) to generate a contextual reply based on their personality and current state.
- Bystander agents analyze the new message and adjust their internal stress and emotional states accordingly.
- The Flask backend passes these conversation logs and cognitive updates to the UI.
