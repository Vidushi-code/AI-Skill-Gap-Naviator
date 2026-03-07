from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to Python path for imports to work
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.ai_agent import generate_analysis
from services.skill_extractor import extract_skills_from_resume
from services.role_matcher import match_role_skills
from services.resume_parser import parse_resume, validate_resume_file
from config.settings import settings
from utils.skill_matcher import match_skill_lists

# Initialize FastAPI app
app = FastAPI(
    title="AI Skill Gap Navigator",
    description="Analyze resumes and GitHub profiles to identify skill gaps and generate personalized roadmaps",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "message": "AI Skill Gap Navigator API",
        "status": "active",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        settings.validate()
        return {"status": "healthy", "api_configured": True}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.post("/analyze")
async def analyze_profile(
    resume: UploadFile = File(..., description="Resume file (PDF, DOC, DOCX, or TXT)"),
    github_username: str = Form(..., description="GitHub username"),
    analysis_mode: str = Form("job_description", description="Mode: 'predefined_role' or 'job_description'"),
    target_role: str = Form(None, description="Target role for predefined mode (e.g., 'data analyst', 'software developer')"),
    job_description: str = Form(None, description="Full job description text for job_description mode")
):
    """
    Main endpoint to analyze user profile and generate skill gap analysis.
    
    Supports two modes:
    1. predefined_role: Match against predefined role skills from ROLE_SKILLS
    2. job_description: Match against custom job description
    
    Args:
        resume: Resume file
        github_username: GitHub username
        analysis_mode: 'predefined_role' or 'job_description'
        target_role: Required for predefined_role mode
        job_description: Required for job_description mode
    
    Returns:
        Complete analysis with skill gaps, resume improvements, and roadmap
    """
    try:
        # Log incoming request
        logger.info(f"=== NEW ANALYSIS REQUEST ===")
        logger.info(f"GitHub Username: {github_username}")
        logger.info(f"Resume Filename: {resume.filename}")
        logger.info(f"Analysis Mode: {analysis_mode}")
        
        # Validate mode and required parameters
        if analysis_mode not in ["predefined_role", "job_description"]:
            raise HTTPException(
                status_code=400, 
                detail="Invalid analysis_mode. Must be 'predefined_role' or 'job_description'"
            )
        
        if analysis_mode == "predefined_role" and not target_role:
            raise HTTPException(
                status_code=400,
                detail="target_role is required when using predefined_role mode"
            )
        
        if analysis_mode == "job_description" and not job_description:
            raise HTTPException(
                status_code=400,
                detail="job_description is required when using job_description mode"
            )
        
        if analysis_mode == "predefined_role":
            logger.info(f"Target Role: {target_role}")
        else:
            logger.info(f"Job Description Length: {len(job_description)} chars")
            logger.info(f"Job Description Preview: {job_description[:200]}")
        
        # Validate resume file
        file_size = 0
        resume.file.seek(0, 2)  # Seek to end
        file_size = resume.file.tell()
        resume.file.seek(0)  # Reset to beginning
        
        is_valid, error_msg = validate_resume_file(resume.filename, file_size, settings.MAX_FILE_SIZE)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Step 1: Parse resume
        try:
            file_bytes = await resume.read()
            resume_text = parse_resume(file_bytes, resume.filename)
            if not resume_text or len(resume_text.strip()) < 10:
                raise HTTPException(status_code=400, detail="Resume appears to be empty or too short")
            logger.info(f"✓ Resume parsed: {len(resume_text)} characters")
        except Exception as e:
            logger.error(f"✗ Resume parsing failed: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to parse resume: {str(e)}")
        
        # Step 2: Extract skills from resume
        try:
            user_skills = extract_skills_from_resume(resume_text)
            logger.info(f"✓ Extracted {len(user_skills)} skills from resume: {user_skills}")
        except Exception as e:
            logger.error(f"✗ Skill extraction failed: {str(e)}")
            user_skills = []  # Continue with empty skills
        
        # Step 3: Fetch GitHub summary
        try:
            github_summary = fetch_github_summary(github_username)
            logger.info(f"✓ GitHub summary fetched: {github_summary.get('found', False)}, repos: {github_summary.get('public_repos', 0)}")
        except Exception as e:
            logger.error(f"✗ GitHub fetch failed: {str(e)}")
            github_summary = {
                "username": github_username,
                "found": False,
                "error": str(e),
                "public_repos": 0
            }
        
        # Step 4: Build AI input based on mode
        if analysis_mode == "predefined_role":
            # Predefined role mode: match against ROLE_SKILLS
            try:
                match_result = match_role_skills(target_role, user_skills)
                
                if not match_result.get("role_found"):
                    logger.warning(f"Role '{target_role}' not found in ROLE_SKILLS")
                    raise HTTPException(
                        status_code=404,
                        detail=f"Role '{target_role}' not found. Available roles: data analyst, frontend developer, backend developer, software developer, full stack developer, data scientist, machine learning engineer, devops engineer"
                    )
                
                logger.info(f"✓ Role match: {match_result['match_percentage']}% ({len(match_result['present_skills'])}/{len(match_result['required_skills'])})")
                
                ai_input = {
                    "mode": "predefined_role",
                    "resume_text": resume_text[:2000],
                    "github_summary": github_summary,
                    "target_role": target_role,
                    "required_skills": match_result["required_skills"],
                    "present_skills": match_result["present_skills"],
                    "missing_skills": match_result["missing_skills"]
                }
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"✗ Role matching failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Role matching failed: {str(e)}")
        else:
            # Job description mode
            ai_input = {
                "mode": "job_description",
                "resume_text": resume_text[:2000],
                "github_summary": github_summary,
                "job_description": job_description,
                "user_skills": user_skills
            }
        
        logger.info(f"✓ AI input prepared with mode: {analysis_mode}")
        
        # Step 5: Generate AI analysis
        try:
            analysis_result = generate_analysis(ai_input)
            
            # Check for errors in AI response
            if "error" in analysis_result and not all(key in analysis_result for key in ["required_skills", "missing_skills"]):
                logger.error(f"✗ AI analysis failed: {analysis_result['error']}")
                raise HTTPException(status_code=500, detail=f"AI analysis failed: {analysis_result['error']}")
            
            logger.info(f"✓ AI analysis completed")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"✗ AI generation error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"AI analysis error: {str(e)}")
        
        # Step 6: For job description mode, verify and correct skill matching using fuzzy matching
        if analysis_mode == "job_description":
            required_skills = analysis_result.get("required_skills", [])
            if required_skills and user_skills:
                try:
                    # Re-validate the match using our skill matching utility
                    match_result = match_skill_lists(required_skills, user_skills)
                    
                    logger.info(f"✓ Fuzzy match: {match_result['match_count']}/{match_result['total_required']} = {match_result['match_percentage']}%")
                    
                    # Update the analysis with corrected matching
                    analysis_result["existing_skills"] = match_result["matched_skills"]
                    analysis_result["missing_skills"] = match_result["missing_skills"]
                    analysis_result["match_percentage"] = match_result["match_percentage"]
                    
                    logger.info(f"✓ Corrected match percentage: {match_result['match_percentage']}%")
                except Exception as e:
                    logger.warning(f"Fuzzy matching failed, using AI results: {str(e)}")
        
        # Step 7: Build final response
        final_response = {
            "status": "success",
            "mode": analysis_mode,
            "user_info": {
                "github_username": github_username,
                "analysis_type": "Predefined Role Analysis" if analysis_mode == "predefined_role" else "Job Description Based Analysis",
                "resume_parsed": True,
                "target_role": target_role if analysis_mode == "predefined_role" else None
            },
            "github_summary": github_summary,
            "ai_analysis": {
                "required_skills": analysis_result.get("required_skills", []),
                "existing_skills": analysis_result.get("existing_skills", []),
                "missing_skills": analysis_result.get("missing_skills", []),
                "match_percentage": analysis_result.get("match_percentage", 0),
                "skill_gap_summary": analysis_result.get("skill_gap_summary", ""),
                "resume_improvements": analysis_result.get("resume_improvements", []),
                "roadmap": analysis_result.get("roadmap", {})
            }
        }
        
        logger.info(f"✓ Analysis complete - Match: {final_response['ai_analysis']['match_percentage']}%")
        
        return JSONResponse(content=final_response, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Internal server error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def fetch_github_summary(username: str) -> dict:
    """
    Fetch GitHub profile summary using GitHub API.
    
    Args:
        username: GitHub username
        
    Returns:
        dict with user stats and repository information
    """
    try:
        # Fetch user profile
        user_url = f"https://api.github.com/users/{username}"
        user_response = requests.get(user_url, timeout=10)
        
        if user_response.status_code == 404:
            return {
                "username": username,
                "found": False,
                "message": "GitHub user not found"
            }
        
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Fetch repositories
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
        repos_response = requests.get(repos_url, timeout=10)
        repos_response.raise_for_status()
        repos_data = repos_response.json()
        
        # Extract languages
        languages = set()
        total_stars = 0
        
        for repo in repos_data:
            if repo.get("language"):
                languages.add(repo["language"])
            total_stars += repo.get("stargazers_count", 0)
        
        return {
            "username": username,
            "found": True,
            "profile_url": user_data.get("html_url"),
            "public_repos": user_data.get("public_repos", 0),
            "followers": user_data.get("followers", 0),
            "following": user_data.get("following", 0),
            "languages": list(languages),
            "total_stars": total_stars,
            "bio": user_data.get("bio", "")
        }
        
    except requests.exceptions.RequestException as e:
        # Return minimal info if GitHub API fails
        return {
            "username": username,
            "found": False,
            "error": f"Failed to fetch GitHub data: {str(e)}",
            "languages": [],
            "public_repos": 0
        }
    except Exception as e:
        return {
            "username": username,
            "found": False,
            "error": str(e),
            "languages": [],
            "public_repos": 0
        }


if __name__ == "__main__":
    import uvicorn
    import sys
    from pathlib import Path
    
    # Add parent directory to Python path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
