SKILLS_DB = [
    "python", "java", "sql", "pandas",
    "machine learning", "react", "node",
    "data analysis", "excel", "power bi",
    "html", "css", "javascript"
]

def extract_skills(text):
    text_lower = text.lower()
    found = []

    for skill in SKILLS_DB:
        if skill in text_lower:
            found.append(skill)

    return found