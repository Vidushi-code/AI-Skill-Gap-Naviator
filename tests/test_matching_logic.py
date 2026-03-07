"""
Test the skill matching with the updated backend logic
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.skill_matcher import match_skill_lists

# Simulate the AI response with potential naming variations
ai_required_skills = ["React", "PHP", "Node.js", "MongoDB", "Express.js", "Bootstrap", "JavaScript", "HTML", "CSS", "APIs"]

# Simulate extracted user skills (from resume parsing)
user_skills = ["React", "Node.js", "JavaScript", "HTML", "CSS", "MongoDB", "Bootstrap", "APIs"]

print("=" * 60)
print("SKILL MATCHING TEST")
print("=" * 60)

print(f"\nRequired Skills (from job): {ai_required_skills}")
print(f"User Skills (from resume): {user_skills}")

# Test the matching
result = match_skill_lists(ai_required_skills, user_skills)

print(f"\n{'-' * 60}")
print("MATCH RESULTS:")
print(f"{'-' * 60}")
print(f"✓ Matched Skills: {result['matched_skills']}")
print(f"✗ Missing Skills: {result['missing_skills']}")
print(f"📊 Match: {result['match_count']}/{result['total_required']} = {result['match_percentage']}%")

# Test with variations
print("\n" + "=" * 60)
print("TESTING SKILL NAME VARIATIONS")
print("=" * 60)

test_cases = [
    (["Node.js"], ["Node", "nodejs", "NodeJS"]),
    (["APIs"], ["API", "api", "REST API"]),
    (["React"], ["ReactJS", "React.js", "react"]),
    (["Express.js"], ["Express", "ExpressJS", "express"]),
]

for required, variations in test_cases:
    print(f"\nRequired: {required[0]}")
    print(f"Testing against: {variations}")
    for var in variations:
        result = match_skill_lists(required, [var])
        status = "✓ MATCH" if result['match_count'] > 0 else "✗ NO MATCH"
        print(f"  {var:20s} -> {status}")
