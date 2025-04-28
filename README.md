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
- 📊 **Speaking Rate Analysis** – Measures words per second and provides visual feedback.
- 🧠 **AI-Powered Feedback** – LLM-generated insights and tips to improve delivery and presence.
- 💬 **AI Speech Coach** – Chat with an AI coach for personalized advice based on your speech patterns.
- 📈 **Interactive Visualizations** – View detailed timelines of your emotion patterns and speaking rate.

---

## ⚙️ Tech Stack

### Backend
- **Flask** – API backend
- **Python** – Core logic
- **Hugging Face Transformers** – Speech emotion recognition
- **Whisper** – Speech-to-text conversion
- **Google Gemini** – AI feedback generation
- **FFmpeg** – Audio extraction and processing

### Frontend
- **React** – User interface
- **React Router** – Client-side routing
- **Recharts** – Data visualization
- **CSS Modules** – Component styling

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- FFmpeg installed on your system

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/speechably.git
   cd speechably
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create a .env file in the backend directory with your API keys**
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   FFMPEG_PATH=/path/to/ffmpeg  # Only if FFmpeg is not in your PATH
   ```

4. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the Flask backend**
   ```bash
   cd backend
   python app.py
   ```

2. **Start the React frontend**
   ```bash
   cd frontend
   npm start
   ```

3. **Open your browser and go to http://localhost:3000**

---

## 📁 Project Structure

```
speechably/
├── backend/                   # Flask backend
│   ├── app.py                 # Main Flask application
│   ├── api/                   # API routes
│   ├── services/              # Core services
│   ├── utils/                 # Utilities
│   └── requirements.txt       # Backend dependencies
│
├── frontend/                  # React frontend
│   ├── public/                # Static files
│   ├── src/                   # Source code
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Application pages
│   │   ├── services/          # API client
│   │   └── styles/            # CSS files
│   └── package.json           # Frontend dependencies
│
├── .env                       # Environment variables
├── README.md                  # Project documentation
└── LICENSE                    # MIT License
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Special thanks to the open-source community for providing the tools and libraries that make this project possible.
- Inspired by the need for accessible speech coaching tools for everyone.
