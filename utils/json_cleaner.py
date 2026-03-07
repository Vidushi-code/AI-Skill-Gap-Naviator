import re
import json
import logging

logger = logging.getLogger(__name__)


def clean_and_parse_json(response_text):
    """
    Robustly extract and parse JSON from AI responses.
    
    Handles:
    - JSON wrapped in markdown code blocks
    - Extra text before/after JSON
    - Common JSON formatting issues
    
    Args:
        response_text: Raw text response from AI
        
    Returns:
        Parsed JSON dictionary
        
    Raises:
        ValueError: If no valid JSON found or parsing fails
    """
    try:
        # Remove markdown code blocks
        cleaned = re.sub(r'```json\s*', '', response_text)
        cleaned = re.sub(r'```\s*', '', cleaned)
        cleaned = cleaned.strip()
        
        # Try to find JSON object in the text
        # Look for content between outermost { and }
        json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(0)
            try:
                parsed = json.loads(json_str)
                logger.info("Successfully parsed JSON from AI response")
                return parsed
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error at position {e.pos}: {e.msg}")
                logger.debug(f"Failed JSON string: {json_str[:500]}...")
                raise ValueError(f"Invalid JSON format: {e.msg}")
        
        # If no JSON found, try parsing the whole cleaned text
        try:
            parsed = json.loads(cleaned)
            logger.info("Successfully parsed JSON (full text)")
            return parsed
        except json.JSONDecodeError:
            logger.error("No valid JSON found in AI response")
            logger.debug(f"Response text (first 500 chars): {response_text[:500]}...")
            raise ValueError("AI response did not contain valid JSON")
    
    except Exception as e:
        logger.error(f"JSON parsing failed: {str(e)}")
        logger.debug(f"Raw response: {response_text[:500]}...")
        
        # Return a default error structure
        return {
            "error": "Failed to parse AI response",
            "detail": str(e),
            "skill_gap_summary": "An error occurred while processing the analysis.",
            "required_skills": [],
            "existing_skills": [],
            "missing_skills": [],
            "match_percentage": 0,
            "resume_improvements": ["Unable to generate improvements due to parsing error"],
            "roadmap": {
                "week1": "Error occurred",
                "week2": "Error occurred",
                "week3": "Error occurred",
                "week4": "Error occurred"
            }
        }
