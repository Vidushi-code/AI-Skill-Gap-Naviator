def generate_roadmap(missing_skills):
    roadmap = []

    for i, skill in enumerate(missing_skills, start=1):
        roadmap.append(f"Step {i}: Learn {skill}")

    return roadmap