# 🗣️ Speechably

**Creating confidence through user-driven feedback.**  
Optimized to deliver professional speech advice — at no cost.  
Perfect for public speaking, everyday conversation, or confidence-building exercises.

---

## 🔍 Overview

**Speechably** is an AI-powered accessibility tool that analyzes videos of users giving speeches or speaking naturally. It evaluates both **speech emotion** and **body language**, then generates personalized feedback using a large language model (LLM). The goal: help users overcome social anxiety, improve delivery, and speak with confidence.

---

## 🎯 Key Features

- 🎥 **Video Upload** – Users upload a short video of themselves speaking.
- 🔊 **Speech Emotion Recognition** – Detects tone, mood, and speaking style using pre-trained models.
- 💃 **Body Language Analysis** – Uses pose estimation to assess posture, gestures, and confidence cues.
- 🧠 **AI-Powered Feedback** – LLM-generated insights and tips to improve delivery and presence.
- 🌐 **Streamlit Interface** – Clean, minimal UI for easy interaction and visualization.

---

## 🗂️ Project Structure
```bash
speechably/
├── app/                     # Frontend logic (Streamlit)
│   ├── main.py              # Entry point for your web app
│   └── components/          # Reusable UI components if needed
│
├── backend/                 # Core processing logic
│   ├── video_processor.py   # Extract frames, audio
│   ├── emotion_model.py     # Run speech emotion recognition
│   ├── pose_estimator.py    # Use MediaPipe or OpenPose
│   ├── feedback_engine.py   # Feedback generation via LLM or rule-based
│   └── utils.py             # Shared utilities (e.g., file handling)
│
├── models/                  # Store downloaded/pretrained models
│   ├── emotion/             
│   └── body_language/
│
├── data/                    # Sample videos and test inputs
│   ├── test_video.mp4       
│   └── extracted_audio.wav
│
├── output/                  # Processed outputs and logs
│   ├── feedback.json        
│   ├── plots/               # Emotion timeline plots
│   └── debug_logs.txt
│
├── requirements.txt         # Python deps
├── .env                     # API keys (Gemini)
└── README.md                # Project overview
```


---

## ⚙️ Tech Stack

- **Python**
- **Streamlit** – Frontend
- **MoviePy** – Video + audio extraction
- **Kaggle / Hugging Face** – Pre-trained Speech Emotion Models
- **MediaPipe** – Pose & gesture analysis
- **Hugging Face** – LLM Integration
- **Plotly** – Optional feedback visualization

---

## 🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/speechably.git
   cd speechably

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a .env file in the root directory and add your API key**
   ```bash
   GEMINI_API_KEY=your_key_here
   ```

4. **Run the program**
   ```bash
   cd app
   streamlit run main.py
   ```

