import sys
sys.path.insert(0, '.')
from services.skill_extractor import extract_skills_from_resume
from services.role_matcher import match_role_skills

sample_resume = '''
Skills:
React.js
Node.js
HTML5
CSS3
Express.js
MongoDB
JavaScript
GitHub
REST APIs
'''

print('Testing full pipeline...')
print('=' * 50)
extracted_skills = extract_skills_from_resume(sample_resume)
print('=' * 50)
print('\nTesting role matching for Full Stack Developer...')
result = match_role_skills('full stack developer', extracted_skills)
print(f'\nRole Found: {result["role_found"]}')
print(f'Match Percentage: {result["match_percentage"]}%')
print(f'Required Skills: {result["required_skills"]}')
print(f'Present Skills: {result["present_skills"]}')
print(f'Missing Skills: {result["missing_skills"]}')
