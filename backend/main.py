from fastapi import FastAPI, UploadFile, File
from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.github_analyzer import get_github_summary
from utils.roadmap_generator import generate_roadmap
from data.roles import ROLE_SKILLS

app = FastAPI(title="AI Skill Gap Navigator")


@app.get("/")
def health():
    return {"status": "Backend running"}


@app.post("/analyze-profile/")
async def analyze_profile(
    role: str,
    github_username: str,
    file: UploadFile = File(...)
):
    # 1. Resume text
    text = extract_text_from_pdf(file.file)

    # 2. Skills from resume
    user_skills = extract_skills(text)

    # 3. Required skills for role
    required_skills = ROLE_SKILLS.get(role.lower(), [])

    # 4. Find missing skills
    missing = [s for s in required_skills if s not in user_skills]

    # 5. GitHub analysis
    github_data = get_github_summary(github_username)

    # 6. Generate roadmap
    roadmap = generate_roadmap(missing)

    return {
        "role": role,
        "your_skills": user_skills,
        "missing_skills": missing,
        "github": github_data,
        "roadmap": roadmap
    }