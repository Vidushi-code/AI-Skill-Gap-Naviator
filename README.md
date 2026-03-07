# 🚀 AI Skill Gap Navigator

🚀 Built for **AWS AI for Bharat Hackathon**

An intelligent web-based platform that leverages AI to analyze resumes, GitHub profiles, and job descriptions to identify skill gaps and generate personalized learning roadmaps for career advancement.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Team](#-team)
- [License](#license)

---

## 📖 Overview

The **AI Skill Gap Navigator** helps students and professionals understand their skill gaps relative to target job roles. By analyzing resume content, GitHub activity, and job descriptions, it provides:

- **Skill Gap Analysis**: Identifies missing skills for your target role
- **Resume Improvement Suggestions**: Actionable tips to enhance your resume
- **Personalized Learning Roadmap**: Week-by-week plan to acquire missing skills
- **Two Analysis Modes**:
  - Predefined roles (Data Analyst, Software Developer, etc.)
  - Custom job descriptions from any source

---

## ✨ Features

- 🔍 **Smart Skill Extraction**: Automatically detects skills from resumes using NLP and skill vocabulary matching
- 🎯 **Role Matching**: Compare your skills against 8+ predefined tech roles
- 📄 **Multiple File Formats**: Supports PDF, DOC, DOCX, and TXT files
- 🤖 **AI-Powered Insights**: Uses Cerebras AI for intelligent analysis and recommendations
- 📊 **GitHub Integration**: Analyzes your GitHub profile for additional skills detection
- 🗺️ **Learning Roadmaps**: 4-week actionable plans customized to your skill gaps
- 💼 **Job Description Mode**: Paste any job posting for custom skill comparison
- ⚡ **Fast & Accurate**: Sub-second skill extraction with high precision matching

---

## 🛠️ Tech Stack

### Backend

- **Framework**: FastAPI (Python 3.8+)
- **AI Engine**: Cerebras Cloud SDK (gpt-oss-120b model)
- **File Parsing**: PyPDF2, python-docx
- **API Integration**: GitHub API, REST APIs

### Frontend

- **Languages**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: Responsive, mobile-friendly UI

### Data & Configuration

- **Environment Management**: python-dotenv
- **Validation**: Pydantic
- **Logging**: Python logging module

---

## 🏗️ Project Architecture

```
skill_gap_new/
│
├── backend/
│   ├── __init__.py
│   └── main.py                 # FastAPI app & endpoints
│
├── services/
│   ├── __init__.py
│   ├── ai_agent.py             # Cerebras AI integration
│   ├── skill_extractor.py      # Skill detection from text
│   ├── role_matcher.py         # Role-skill comparison logic
│   └── resume_parser.py        # Multi-format file parser
│
├── data/
│   ├── __init__.py
│   ├── role_skills.py          # Predefined role definitions
│   └── skill_vocab.py          # Skill vocabulary (180+ skills)
│
├── config/
│   ├── __init__.py
│   └── settings.py             # App configuration & env vars
│
├── utils/
│   ├── __init__.py
│   ├── json_cleaner.py         # AI response parser
│   └── skill_matcher.py        # Fuzzy skill matching
│
├── frontend/
│   ├── index.html              # Main input interface
│   ├── result.html             # Analysis results page
│   ├── script.js               # Frontend logic
│   └── styles.css              # Styling
│
├── tests/                      # Test files
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── run_backend.py              # Backend startup script
├── start.bat                   # Windows startup script
└── README.md                   # This file
```

## 🌩️ Cloud Architecture (Planned AWS Deployment)

The current prototype runs locally using FastAPI and a browser-based frontend.  
For scalable production deployment, the system is designed to integrate with AWS cloud services.

User Browser
│
▼
CloudFront (Frontend Hosting)
│
▼
Amazon S3
│
▼
API Gateway
│
▼
FastAPI Backend (AWS Lambda / EC2)
│
├ Resume Upload → Amazon S3
├ Skill Extraction Service
├ Role Matching Engine
│
▼
AI Analysis Layer (Cerebras / Amazon Bedrock)
│
▼
Amazon DynamoDB (Store Analysis Results)

---

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Cerebras API key ([Get one here](https://cerebras.ai/))

### Step-by-Step Setup

1. **Clone the Repository**

```bash
git clone https://github.com/Vidushi-code/AI-Skill-Gap-Naviator.git
cd AI-Skill-Gap-Naviator
```

2. **Create Virtual Environment**

```bash
python -m venv venv
```

3. **Activate Virtual Environment**

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

4. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
CEREBRAS_API_KEY=your_cerebras_api_key_here
```

### Optional Configuration

Edit `config/settings.py` to customize:

- `AI_MODEL`: AI model name (default: "gpt-oss-120b")
- `AI_TEMPERATURE`: Response creativity (default: 0.7)
- `MAX_FILE_SIZE`: Max upload size (default: 10MB)
- `CORS_ORIGINS`: Allowed frontend origins

---

## 🚀 Usage

### Start the Backend Server

**Option 1: Using the startup script (Recommended)**

```bash
python run_backend.py
```

**Option 2: Using uvicorn directly**

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Windows batch file**

```bash
start.bat
```

### Access the Application

- **Frontend**: Open `frontend/index.html` in your browser
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Using the Web Interface

1. Open `frontend/index.html` in your browser
2. Upload your resume (PDF, DOCX, DOC, or TXT)
3. Enter your GitHub username
4. Choose analysis mode:
   - **Predefined Role**: Select from dropdown (e.g., "Software Developer")
   - **Job Description**: Paste a job posting
5. Click "Analyze"
6. View your skill gap analysis and roadmap

---

## 📡 API Documentation

### Main Endpoint

**POST** `/analyze`

Analyzes resume and generates skill gap report.

**Parameters:**

| Name              | Type   | Required    | Description                            |
| ----------------- | ------ | ----------- | -------------------------------------- |
| `resume`          | File   | Yes         | Resume file (PDF/DOC/DOCX/TXT)         |
| `github_username` | String | Yes         | GitHub username                        |
| `analysis_mode`   | String | Yes         | "predefined_role" or "job_description" |
| `target_role`     | String | Conditional | Required for predefined_role mode      |
| `job_description` | String | Conditional | Required for job_description mode      |

**Response:**

```json
{
  "status": "success",
  "mode": "predefined_role",
  "user_info": {
    "github_username": "john_doe",
    "analysis_type": "Predefined Role Analysis",
    "target_role": "Software Developer"
  },
  "github_summary": {
    "username": "john_doe",
    "found": true,
    "public_repos": 25,
    "languages": ["Python", "JavaScript", "Go"]
  },
  "ai_analysis": {
    "required_skills": ["Python", "Java", "C++", "Git"],
    "existing_skills": ["Python", "Git"],
    "missing_skills": ["Java", "C++"],
    "match_percentage": 50,
    "skill_gap_summary": "You have 2 out of 4 required skills...",
    "resume_improvements": [
      "Add projects demonstrating OOP concepts",
      "Include algorithmic problem-solving experience"
    ],
    "roadmap": {
      "week1": "Learn Java basics. Complete 10 coding challenges.",
      "week2": "Build a CLI application using Java.",
      "week3": "Learn C++ fundamentals. Focus on pointers.",
      "week4": "Create a portfolio project combining all skills."
    }
  }
}
```

### Additional Endpoints

- **GET** `/` - API status
- **GET** `/health` - Health check

---

## 📂 Project Structure

### Key Modules

#### `services/skill_extractor.py`

Extracts skills from resume text using:

- 180+ skill vocabulary with aliases
- Case-insensitive matching
- Word boundary detection
- Handles variations (e.g., "React", "ReactJS", "React.js")

#### `services/role_matcher.py`

Compares user skills against predefined role requirements:

- 8 predefined roles
- Calculates match percentage
- Identifies missing skills

#### `services/ai_agent.py`

Generates intelligent analysis using Cerebras AI:

- Skill gap summaries
- Resume improvement tips
- Week-by-week learning roadmaps

#### `utils/skill_matcher.py`

Advanced fuzzy matching for skills:

- Handles common aliases
- Normalizes skill names
- Improves accuracy in job description mode

---

## 🧪 Testing

Run the test suite:

```bash
# Test skill extraction
python tests/test_extraction.py

# Test role matching
python tests/test_matching_logic.py

# Test skill matching utilities
python tests/test_skill_matching.py
```

---

## 👥 Team

Built by **Team NULL_POINTERS** for the **AI for Bharat Hackathon**.

| Name            | Role                                |
| --------------- | ----------------------------------- |
| Vidushi Agarwal | AI Agent Development, System Design |
| Sameep Madan    | Backend Development                 |
| Somya Gupta     | Data Processing & Skill Matching    |

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Cerebras AI** for providing the powerful AI model
- **FastAPI** for the excellent web framework
- **GitHub API** for profile integration

---

## 📞 Contact & Support

For questions, issues, or suggestions:

- Email: agarwalvidushi0805@gmail.com

---

**Made with ❤️ by Vidushi Agarwal**
