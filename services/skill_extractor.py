from data.skill_vocab import SKILL_VOCAB
import re
import logging

# Configure logging
logger = logging.getLogger(__name__)

def normalize_text(text):
    """
    Normalize text by converting to lowercase and removing punctuation.
    This helps match variations like React.js, Node.js, HTML5, CSS3, etc.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove common punctuation characters
    # Replace punctuation with spaces to avoid merging words
    punctuation_chars = ['.', ',', '+', '#', '-', '(', ')', '!', '?', ':', ';', '"', "'", '/', '\\', '[', ']', '{', '}']
    for char in punctuation_chars:
        text = text.replace(char, ' ')
    
    # Replace multiple spaces with single space
    text = ' '.join(text.split())
    
    return text


def extract_skills_from_resume(resume_text):
    """
    Extract skills from resume text using flexible matching.
    
    Args:
        resume_text: Raw text extracted from resume
        
    Returns:
        List of canonical skill names (e.g., ["React", "Node.js", "Python"])
    """
    try:
        if not resume_text or not resume_text.strip():
            logger.warning("Empty resume text provided for skill extraction")
            return []
        
        found_skills = set()  # Use set to avoid duplicates
        
        # Normalize the resume text
        normalized_text = normalize_text(resume_text)
        
        # Log skill extraction start
        logger.info(f"Starting skill extraction from {len(resume_text)} character resume")
        logger.debug(f"Normalized text preview: {normalized_text[:300]}...")
        
        # Check each skill and its aliases
        for canonical_skill, aliases in SKILL_VOCAB.items():
            for alias in aliases:
                # Normalize the alias too
                normalized_alias = normalize_text(alias)
                
                # Use word boundary matching for better precision
                # This prevents matching "react" inside "preaction"
                pattern = r'\b' + re.escape(normalized_alias) + r'\b'

                if re.search(pattern, normalized_text):
                    found_skills.add(canonical_skill)
                    logger.debug(f"Matched skill: {canonical_skill} using alias '{alias}'")
                    break
        
        # Convert to sorted list for consistent output
        result = sorted(list(found_skills))
        
        logger.info(f"Skill extraction complete: {len(result)} skills detected")
        logger.info(f"Extracted skills: {result}")
        
        return result
    
    except Exception as e:
        logger.error(f"Skill extraction failed: {str(e)}", exc_info=True)
        return []  # Return empty list on error
