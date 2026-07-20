# Customer Support Ticketing CRM System

A modern, full-stack Customer Support Ticketing CRM built for the Datastraw AI + Tech Intern assessment. It features a premium iOS-style "liquid glassmorphism" user interface and an intelligent backend powered by Large Language Models.

## 🌐 Live Demo
web app (Render.com): *https://customer-support-ticketing-crm-system-5fhm.onrender.com/** <br>
loom video: **https://www.loom.com/share/6df1470bc7bf4b81a617369c30f4a346**

## ✨ Key Features
* **AI Auto-Triage:** Automatically reads new support tickets and instantly categorizes their priority (High, Medium, Low) using Groq API (with an OpenRouter fallback).
* **Ticket Management:** Seamlessly create, view, and update customer support tickets.
* **Advanced Sorting & Filtering:** Filter tickets by status (Open, In Progress, Closed) and smartly sort by AI-assigned Priority or Date.
* **Premium UI:** A fully responsive, custom translucent interface built natively with Tailwind CSS and Vanilla JavaScript.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI
* **Database:** SQLite, SQLAlchemy (ORM)
* **Frontend:** HTML5, Vanilla JS, Tailwind CSS
* **AI Integrations:** Groq API, OpenRouter API

## 🚀 Local Setup Instructions

### 1. Clone the repository:
```bash
git clone <your-github-repo-url>
cd Customer-Support-Ticketing-CRM-System
```

### 2. Set up the virtual environment:
This project uses `uv` for dependency management.

```bash
uv venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables:
Create a `.env` file in the root directory based on the provided `.env.example` file and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 5. Run the server:
```bash
uvicorn main:app --reload
```

Navigate to `http://127.0.0.1:8000/` in your browser to access the CRM Dashboard.
