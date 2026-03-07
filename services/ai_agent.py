from cerebras.cloud.sdk import Cerebras
from utils.json_cleaner import clean_and_parse_json
from config.settings import settings
import logging
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Cerebras(
    api_key=settings.CEREBRAS_API_KEY,
)

def generate_analysis(data):
    """
    Generate AI-powered career analysis.
    
    Supports two modes:
    1. Predefined Role Mode: Uses ROLE_SKILLS for comparison
    2. Job Description Mode: Analyzes custom job description to extract skills
    
    Args:
        data: Dictionary with mode and relevant information
        
    Returns:
        Dictionary with skill_gap_summary, resume_improvements, and roadmap
    """
    
    mode = data.get('mode', 'predefined_role')
    
    if mode == 'job_description':
        # MODE 2: Custom Job Description Analysis
        prompt = f"""
You are an AI career advisor specializing in skill gap analysis.

Your task is to analyze a job description and compare it with a candidate's resume.

**Candidate's Resume:**
{data['resume_text']}

**GitHub Summary:**
{data['github_summary']}

**Candidate's Extracted Skills (using standardized names):**
{data['user_skills']}

**Job Description (from LinkedIn/Internshala/Indeed):**
{data['job_description']}

**Your Task:**

Step 1: Carefully analyze the job description and extract ALL required skills, technologies, and qualifications mentioned.

Step 2: **IMPORTANT**: When listing required skills, use standardized names that match the candidate's extracted skills format:
   - Use "Node.js" not "Node" or "NodeJS"
   - Use "Express.js" not "Express" or "ExpressJS"
   - Use "APIs" not "API" or "RESTful API"
   - Use "React" not "ReactJS" or "React.js" (unless specifically differ)
   - When a skill has multiple names (e.g., "React", "React.js"), normalize to the most common form
   
Step 3: Compare the required skills from the job description with the candidate's extracted skills list above.

Step 4: Identify:
   - existing_skills: Skills the candidate HAS from their extracted skills that match the required skills
   - missing_skills: Skills from the required list that the candidate does NOT have
   - match_percentage: Calculate as (count of existing_skills / count of required_skills) * 100

Step 5: Generate a comprehensive analysis in the following JSON format:

{{
  "required_skills": ["React", "PHP", "Node.js", "MongoDB", "Express.js", "Bootstrap", "JavaScript", "HTML", "CSS", "APIs"],
  "existing_skills": ["React", "Node.js", "JavaScript", "HTML", "CSS"],
  "missing_skills": ["PHP", "MongoDB", "Express.js", "Bootstrap", "APIs"],
  "match_percentage": 50,
  "skill_gap_summary": "You have 5 out of 10 required skills. You know React, Node.js, JavaScript, HTML, and CSS. But you need to learn PHP, MongoDB, Express.js, Bootstrap, and APIs to fully qualify for this role.",
  "resume_improvements": [
    "Add a full-stack project using MERN stack",
    "Include PHP backend development experience",
    "Build and document RESTful APIs in your projects"
  ],
  "roadmap": {{
      "week1": "Learn PHP basics. Build a simple CRUD app. Use W3Schools tutorials.",
      "week2": "Learn MongoDB. Practice queries. Connect MongoDB to a Node.js app.",
      "week3": "Build Express.js APIs. Create 5 RESTful endpoints. Test with Postman.",
      "week4": "Complete MERN stack project. Use Bootstrap for UI. Deploy and add to resume."
  }}
}}

**CRITICAL WRITING RULES:**
- Use EXTREMELY SIMPLE English - write like you are talking to a college student
- NO long paragraphs - use SHORT sentences only
- Avoid technical jargon unless absolutely necessary
- The summary should be readable in under 10 seconds
- Be direct and actionable
- Focus on what to DO, not what is missing

**Output Requirements:**
- required_skills: List ALL skills from job description using STANDARDIZED names (Node.js not Node, APIs not API)
- existing_skills: ONLY skills the candidate already has (check against the extracted skills list above)
- missing_skills: Skills from required list that candidate does not have
- match_percentage: MUST be an integer. Calculate as (len(existing_skills) / len(required_skills)) * 100
- skill_gap_summary: 2-3 SHORT sentences in simple English, mention specific numbers
- resume_improvements: 3-5 specific actions, each under 15 words
- roadmap: week1 to week4, each under 25 words, very actionable

Return ONLY valid JSON. No explanation outside JSON.
"""
    else:
        # MODE 1: Predefined Role Analysis (existing logic)
        prompt = f"""
You are an AI career analyst.

Analyze the student profile below and return STRICT JSON only.

Student Resume:
{data['resume_text']}

GitHub Summary:
{data['github_summary']}

Target Role:
{data['target_role']}

Required Skills:
{data['required_skills']}

Present Skills:
{data['present_skills']}

Missing Skills:
{data['missing_skills']}

Return JSON in this format:

{{
  "required_skills": {data['required_skills']},
  "existing_skills": {data['present_skills']},
  "missing_skills": {data['missing_skills']},
  "match_percentage": 50,
  "skill_gap_summary": "You have X out of Y required skills. [Simple 2-3 sentence explanation]",
  "resume_improvements": [
    "Short actionable suggestion 1",
    "Short actionable suggestion 2",
    "Short actionable suggestion 3"
  ],
  "roadmap": {{
      "week1": "Learn [skill]. Practice daily. Use [resource].",
      "week2": "Build [project type]. Push to GitHub.",
      "week3": "Learn [another skill]. Focus on [specific topic].",
      "week4": "Build portfolio project. Add to resume."
  }}
}}

**CRITICAL WRITING RULES:**
- Use EXTREMELY SIMPLE English
- NO long paragraphs - SHORT sentences only
- Write like you are advising a college student
- Be direct and actionable
- Each improvement should be under 15 words
- Each roadmap week should be under 25 words

Return valid JSON only. No explanation outside JSON.
"""

    try:
        # Log request timestamp for debugging
        timestamp = datetime.datetime.now().isoformat()
        logger.info(f"AI Request at {timestamp}")
        logger.info(f"Mode: {mode}")
        logger.info(f"Prompt length: {len(prompt)} characters")
        
        # Create unique system message with timestamp to avoid caching
        system_message = f"You are a strict JSON generator and career analysis expert. Current analysis timestamp: {timestamp}"
        
        response = client.chat.completions.create(
            model=settings.AI_MODEL,   
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=settings.AI_TEMPERATURE
        )

        raw_output = response.choices[0].message.content
        logger.info(f"AI Response received: {len(raw_output)} characters")
        logger.info(f"First 300 chars of response: {raw_output[:300]}")

        parsed_result = clean_and_parse_json(raw_output)
        
        # Validate the parsed result has required fields
        if "error" in parsed_result:
            logger.error(f"JSON parsing returned error structure: {parsed_result.get('error')}")
            return parsed_result
        
        required_fields = ["required_skills", "existing_skills", "missing_skills", 
                          "match_percentage", "skill_gap_summary", "resume_improvements", "roadmap"]
        
        missing_fields = [field for field in required_fields if field not in parsed_result]
        if missing_fields:
            logger.warning(f"AI response missing fields: {missing_fields}")
            # Fill in missing fields with defaults
            if "required_skills" not in parsed_result:
                parsed_result["required_skills"] = []
            if "existing_skills" not in parsed_result:
                parsed_result["existing_skills"] = []
            if "missing_skills" not in parsed_result:
                parsed_result["missing_skills"] = []
            if "match_percentage" not in parsed_result:
                parsed_result["match_percentage"] = 0
            if "skill_gap_summary" not in parsed_result:
                parsed_result["skill_gap_summary"] = "Unable to generate summary."
            if "resume_improvements" not in parsed_result:
                parsed_result["resume_improvements"] = ["Add more relevant projects to your resume"]
            if "roadmap" not in parsed_result:
                parsed_result["roadmap"] = {
                    "week1": "Focus on learning missing skills",
                    "week2": "Build practice projects",
                    "week3": "Update resume with new projects",
                    "week4": "Apply for positions"
                }
        
        logger.info(f"Successfully parsed and validated JSON with {len(parsed_result.get('missing_skills', []))} missing skills")
        
        return parsed_result

    except Exception as e:
        logger.error(f"AI generation failed: {str(e)}", exc_info=True)
        
        # Return a safe fallback response
        return {
            "error": str(e),
            "required_skills": data.get('required_skills', []) if mode == 'predefined_role' else [],
            "existing_skills": data.get('present_skills', []) if mode == 'predefined_role' else [],
            "missing_skills": data.get('missing_skills', []) if mode == 'predefined_role' else [],
            "match_percentage": 0,
            "skill_gap_summary": f"An error occurred during AI analysis: {str(e)}. Please try again.",
            "resume_improvements": [
                "Unable to generate improvements due to an error",
                "Please ensure your resume is properly formatted",
                "Try uploading the resume again"
            ],
            "roadmap": {
                "week1": "Review the error and try again",
                "week2": "Ensure all inputs are correct",
                "week3": "Contact support if issue persists",
                "week4": "Continue skill development independently"
            }
        }