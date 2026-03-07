"""
Test script to debug skill extraction and matching flow
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from services.skill_extractor import extract_skills_from_resume
from data.skill_vocab import SKILL_VOCAB

# Sample resume text with common skills
sample_resume = """
John Doe
Software Developer

Skills:
- React.js and Node.js development
- PHP backend programming
- MongoDB database management
- Express.js framework
- Bootstrap and HTML/CSS
- JavaScript programming
- RESTful APIs design

Experience:
Built web applications using MERN stack (MongoDB, Express, React, Node.js).
Proficient in frontend technologies like HTML5, CSS3, and Bootstrap.
"""

print("=" * 60)
print("SKILL EXTRACTION TEST")
print("=" * 60)

print("\n📄 Sample Resume:")
print(sample_resume)

print("\n" + "=" * 60)
print("EXTRACTING SKILLS...")
print("=" * 60)

extracted_skills = extract_skills_from_resume(sample_resume)

print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)
print(f"Total skills found: {len(extracted_skills)}")
print(f"Skills: {extracted_skills}")

print("\n" + "=" * 60)
print("CHECKING REQUIRED SKILLS FOR JOB")
print("=" * 60)

required_skills = ["React", "PHP", "Node.js", "MongoDB", "Express.js", "Bootstrap", "JavaScript", "HTML", "CSS", "APIs"]
print(f"Required: {required_skills}")

# Check which skills match
matching = [skill for skill in required_skills if skill in extracted_skills or skill.lower() in [s.lower() for s in extracted_skills]]
missing = [skill for skill in required_skills if skill not in matching]

print(f"\n✓ Matching skills: {matching}")
print(f"✗ Missing skills: {missing}")
print(f"📊 Match percentage: {(len(matching) / len(required_skills)) * 100:.1f}%")

print("\n" + "=" * 60)
print("SKILL VOCABULARY CHECK")
print("=" * 60)
print(f"Total canonical skills in vocab: {len(SKILL_VOCAB)}")
print("\nSample entries:")
for i, (canonical, aliases) in enumerate(list(SKILL_VOCAB.items())[:10]):
    print(f"  {canonical}: {aliases[:3]}..." if len(aliases) > 3 else f"  {canonical}: {aliases}")
