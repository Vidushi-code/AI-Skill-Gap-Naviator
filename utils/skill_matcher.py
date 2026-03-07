"""
Skill matching utilities for normalizing and comparing skill names
"""

def normalize_skill_name(skill: str) -> str:
    """
    Normalize a skill name for comparison.
    Handles common variations like:
    - Case differences: "React" vs "react"
    - Punctuation: "Node.js" vs "Node" vs "NodeJS"
    - Plurals: "API" vs "APIs"
    
    Args:
        skill: Skill name to normalize
        
    Returns:
        Normalized skill name
    """
    # Convert to lowercase
    skill = skill.lower().strip()
    
    # Remove common suffixes
    skill = skill.replace('.js', '')
    skill = skill.replace('js', '')
    
    # Handle plurals
    if skill.endswith('s') and len(skill) > 3:
        skill_singular = skill[:-1]
        # Only remove 's' if it makes sense (APIs -> API, but CSS stays CSS)
        if skill != 'css' and skill != 'sass':
            skill = skill_singular
    
    # Remove spaces and punctuation for core comparison
    skill = skill.replace(' ', '').replace('-', '').replace('_', '').replace('.', '')
    
    return skill


def skills_match(skill1: str, skill2: str) -> bool:
    """
    Check if two skill names represent the same skill.
    
    Args:
        skill1: First skill name
        skill2: Second skill name
        
    Returns:
        True if skills match, False otherwise
    """
    # Exact match (case-insensitive)
    if skill1.lower().strip() == skill2.lower().strip():
        return True
    
    # Normalized match
    if normalize_skill_name(skill1) == normalize_skill_name(skill2):
        return True
    
    # Common aliases
    aliases = {
        'node': ['nodejs', 'node.js', 'node js'],
        'express': ['expressjs', 'express.js', 'express js'],
        'react': ['reactjs', 'react.js', 'react js'],
        'vue': ['vuejs', 'vue.js', 'vue js'],
        'angular': ['angularjs', 'angular.js', 'angular js'],
        'next': ['nextjs', 'next.js', 'next js'],
        'api': ['apis', 'rest api', 'rest apis', 'restful api', 'restful apis'],
    }
    
    skill1_norm = skill1.lower().strip()
    skill2_norm = skill2.lower().strip()
    
    for canonical, variations in aliases.items():
        if skill1_norm in variations or skill1_norm == canonical:
            if skill2_norm in variations or skill2_norm == canonical:
                return True
    
    return False


def find_matching_skill(skill: str, skill_list: list) -> str:
    """
    Find a matching skill from a list, accounting for variations.
    
    Args:
        skill: Skill to find
        skill_list: List of skills to search in
        
    Returns:
        Matching skill from the list, or None if not found
    """
    for list_skill in skill_list:
        if skills_match(skill, list_skill):
            return list_skill
    return None


def match_skill_lists(required_skills: list, user_skills: list) -> dict:
    """
    Match required skills against user skills with fuzzy matching.
    
    Args:
        required_skills: List of required skills
        user_skills: List of user's skills
        
    Returns:
        dict with matched_skills and missing_skills
    """
    matched = []
    missing = []
    
    for req_skill in required_skills:
        match = find_matching_skill(req_skill, user_skills)
        if match:
            matched.append(req_skill)  # Keep the original required skill name
        else:
            missing.append(req_skill)
    
    return {
        'matched_skills': matched,
        'missing_skills': missing,
        'match_count': len(matched),
        'total_required': len(required_skills),
        'match_percentage': round((len(matched) / len(required_skills)) * 100, 1) if required_skills else 0
    }
