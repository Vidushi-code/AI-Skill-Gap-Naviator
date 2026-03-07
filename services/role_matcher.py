from data.role_skills import ROLE_SKILLS
import logging

# Configure logging
logger = logging.getLogger(__name__)

def match_role_skills(target_role: str, user_skills: list) -> dict:
    """
    Match user skills against required skills for a target role.
    
    Args:
        target_role: The target job role (e.g., "data analyst", "sde")
        user_skills: List of skills extracted from user's resume
        
    Returns:
        dict with required_skills, present_skills, missing_skills, role_found, and match_percentage
    """
    try:
        logger.info(f"Matching skills for role: '{target_role}'")
        logger.debug(f"User has {len(user_skills)} skills: {user_skills}")
        
        # Normalize target role to lowercase
        role_key = target_role.lower().replace("-", " ").replace("_", " ").strip()
        
        # Handle common role aliases
        role_aliases = {
            "sde": "software developer",
            "software development engineer": "software developer",
            "full-stack": "full stack developer",
            "fullstack": "full stack developer",
            "ai/ml engineer": "machine learning engineer",
            "ai engineer": "machine learning engineer",
            "ml engineer": "machine learning engineer",
        }
        
        role_key = role_aliases.get(role_key, role_key)
    
        # Get required skills for the role
        required_skills = ROLE_SKILLS.get(role_key, [])
        
        if not required_skills:
            logger.warning(f"Role '{role_key}' not found in ROLE_SKILLS dictionary")
            # Return empty result if role not found
            return {
                "required_skills": [],
                "present_skills": [],
                "missing_skills": [],
                "role_found": False,
                "match_percentage": 0
            }
    
        # Normalize user skills to lowercase for comparison
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        # Find present and missing skills
        present_skills = []
        missing_skills = []
        
        for required_skill in required_skills:
            if required_skill.lower() in user_skills_lower:
                present_skills.append(required_skill)
            else:
                missing_skills.append(required_skill)
        
        match_percentage = round((len(present_skills) / len(required_skills)) * 100, 2) if required_skills else 0
        
        logger.info(f"Match result: {len(present_skills)}/{len(required_skills)} skills ({match_percentage}%)")
        logger.debug(f"Present: {present_skills}")
        logger.debug(f"Missing: {missing_skills}")
        
        return {
            "required_skills": required_skills,
            "present_skills": present_skills,
            "missing_skills": missing_skills,
            "role_found": True,
            "match_percentage": match_percentage
        }
    
    except Exception as e:
        logger.error(f"Role matching failed: {str(e)}", exc_info=True)
        return {
            "required_skills": [],
            "present_skills": [],
            "missing_skills": [],
            "role_found": False,
            "match_percentage": 0,
            "error": str(e)
        }
