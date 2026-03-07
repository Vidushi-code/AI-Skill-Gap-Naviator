# Quick Start Guide - Job Description Feature

## What's New?

Your AI Skill Gap Navigator now supports **two modes**:

### Mode 1: Predefined Role (Original)
- Select a role from dropdown (SDE, Data Scientist, etc.)
- System compares against pre-defined skill requirements

### Mode 2: Custom Job Description (NEW!)
- Paste any job description from LinkedIn, Internshala, Indeed, or company websites
- AI extracts required skills directly from the job posting
- Get personalized analysis based on actual job requirements

## How to Use

### Option A: Using Predefined Role
1. Open `frontend/index.html` in browser
2. Upload your resume
3. Enter GitHub username
4. **Select a role from dropdown**
5. **Leave job description textarea empty**
6. Click "Analyze Profile"

### Option B: Using Custom Job Description (NEW!)
1. Open `frontend/index.html` in browser
2. Upload your resume
3. Enter GitHub username
4. **Leave role dropdown unselected**
5. **Paste full job description in textarea**
   - Example: Copy entire job posting from LinkedIn
6. Click "Analyze Profile"

## Important Notes

⚠️ **You must choose ONE mode:**
- Either select a role OR paste job description
- NOT both at the same time

✅ **Job Description Format:**
- Paste the complete job description
- Include skills, requirements, responsibilities
- The more details, the better the analysis

## Example Job Description

```
Full Stack Developer - TechCorp Inc.

We are seeking an experienced Full Stack Developer to join our team.

Required Skills:
- 3+ years experience with React and Node.js
- Strong knowledge of JavaScript/TypeScript
- Experience with MongoDB and PostgreSQL
- Familiarity with Docker and Kubernetes
- AWS or Azure cloud services
- RESTful API development

Preferred:
- Experience with microservices architecture
- Knowledge of CI/CD pipelines
- Strong problem-solving skills
```

## What You'll Get

Both modes provide:
- ✅ Skill gap analysis
- ✅ Resume improvement suggestions  
- ✅ 4-week personalized learning roadmap
- ✅ GitHub profile integration

**Mode 2 advantage**: Analysis based on real job requirements from actual companies!

## Starting the Application

### Start Backend:
```bash
python run_backend.py
```

Or use the batch file:
```bash
start.bat
```

### Open Frontend:
Simply open `frontend/index.html` in your web browser.

The backend will run on: `http://localhost:8000`

## Testing

To verify both modes work:

1. **Test Mode 1**: Use existing predefined role functionality
2. **Test Mode 2**: Paste a real job description from LinkedIn

Both should generate comprehensive analysis with skills, improvements, and roadmap.

## Troubleshooting

**Problem**: "Please either select a role OR paste a job description"
- **Solution**: Make sure you fill only ONE field, not both

**Problem**: Analysis not generating
- **Solution**: Ensure backend is running on port 8000
- Check that your AI API key is configured in `.env` file

**Problem**: Job description not being analyzed
- **Solution**: Make sure you left the role dropdown unselected
- Paste the complete job description (minimum 50 characters)

## Benefits of Job Description Mode

1. **Real Job Matching**: Match against actual job postings
2. **Up-to-date Skills**: Get current industry requirements
3. **Specific Companies**: Target specific companies you're interested in
4. **Multiple Roles**: Analyze different positions easily
5. **Practical Insights**: Based on real-world requirements

Enjoy your enhanced AI Skill Gap Navigator! 🚀
