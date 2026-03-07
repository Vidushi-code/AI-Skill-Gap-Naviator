# ARCHITECTURE DIAGRAM - AI Skill Gap Navigator

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (Not Modified)                         │
│                                                                              │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐        │
│  │  index.html  │────────▶│  script.js   │────────▶│ result.html  │        │
│  │ (Input Form) │         │  (Logic)     │         │ (Display)    │        │
│  └──────────────┘         └──────────────┘         └──────────────┘        │
│         │                         │                         ▲               │
│         │    File Upload +        │                         │               │
│         │    GitHub Username +    │                         │               │
│         │    Target Role          │                         │               │
│         ▼                         ▼                         │               │
└─────────────────────────────────────────────────────────────────────────────┘
          │                                                   │
          │ HTTP POST /analyze                                │ JSON Response
          │                                                   │
┌─────────▼───────────────────────────────────────────────────┴────────────────┐
│                            BACKEND (FastAPI)                                 │
│                         backend/main.py ✨ REFACTORED                        │
│                                                                              │
│  ╔══════════════════════════════════════════════════════════════════╗       │
│  ║  @app.post("/analyze")                                            ║       │
│  ║                                                                   ║       │
│  ║  1. Validate File ──────────────────────────────────┐            ║       │
│  ║                                                      │            ║       │
│  ║  2. Parse Resume (PDF/DOC/DOCX) ──────┐             ▼            ║       │
│  ║                                        │    ┌───────────────┐    ║       │
│  ║  3. Extract Skills ────────────────────┼───▶│   Services    │    ║       │
│  ║                                        │    │   Layer       │    ║       │
│  ║  4. Fetch GitHub Profile ──────────────┤    └───────────────┘    ║       │
│  ║                                        │             │            ║       │
│  ║  5. Match Role Skills ─────────────────┤             ▼            ║       │
│  ║                                        │    ┌───────────────┐    ║       │
│  ║  6. Build AI Input ────────────────────┤    │     Data      │    ║       │
│  ║                                        │    │    Layer      │    ║       │
│  ║  7. Generate AI Analysis ──────────────┤    └───────────────┘    ║       │
│  ║                                        │             │            ║       │
│  ║  8. Return JSON Response ◀─────────────┘             ▼            ║       │
│  ║                                              ┌───────────────┐    ║       │
│  ╚══════════════════════════════════════════════│    Config     │════╝       │
│                                                 │    Layer      │            │
│                                                 └───────────────┘            │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                            SERVICES LAYER ✨ NEW                              │
│                                                                              │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐ │
│  │  resume_parser.py   │  │ skill_extractor.py  │  │  role_matcher.py    │ │
│  │  ✨ NEW              │  │ ✅ KEPT              │  │  ✨ NEW              │ │
│  ├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤ │
│  │ - parse_resume()    │  │ - extract_skills()  │  │ - match_role_skills()│ │
│  │ - _parse_pdf()      │  │   from resume text  │  │ - Calculate match % │ │
│  │ - _parse_docx()     │  │                     │  │ - Find missing      │ │
│  │ - validate_file()   │  │ Uses skill_vocab    │  │   skills            │ │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘ │
│                                                                              │
│  ┌─────────────────────┐                                                    │
│  │   ai_agent.py       │                                                    │
│  │   ✅ UPDATED         │           ┌──────────────────────────┐            │
│  ├─────────────────────┤           │   External: Cerebras     │            │
│  │ - generate_analysis()├──────────▶│   AI API (gpt-oss-120b) │            │
│  │ - Builds prompt     │           │                          │            │
│  │ - Calls Cerebras    │◀──────────│   Returns JSON analysis  │            │
│  │ - Parses response   │           └──────────────────────────┘            │
│  └─────────────────────┘                                                    │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER ✅ REORGANIZED                        │
│                                                                              │
│  ┌─────────────────────┐                    ┌─────────────────────┐         │
│  │  role_skills.py     │                    │  skill_vocab.py     │         │
│  │  ✅ MOVED             │                    │  ✅ KEPT             │         │
│  ├─────────────────────┤                    ├─────────────────────┤         │
│  │ ROLE_SKILLS = {     │                    │ SKILL_VOCAB = {     │         │
│  │   "data analyst": [ │                    │   "Python": [...]   │         │
│  │     "python",       │                    │   "Java": [...]     │         │
│  │     "sql",          │                    │   "SQL": [...]      │         │
│  │     "pandas",       │                    │   ...               │         │
│  │     ...             │                    │ }                   │         │
│  │   ],                │                    │                     │         │
│  │   "sde": [...]      │                    │ Canonical skills    │         │
│  │   ...               │                    │ with aliases        │         │
│  │ }                   │                    │                     │         │
│  └─────────────────────┘                    └─────────────────────┘         │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                             CONFIG LAYER ✨ NEW                               │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────┐         │
│  │                      config/settings.py                         │         │
│  │                      ✨ NEW                                      │         │
│  ├────────────────────────────────────────────────────────────────┤         │
│  │  class Settings:                                                │         │
│  │    - CEREBRAS_API_KEY (from .env)                              │         │
│  │    - AI_MODEL = "gpt-oss-120b"                                 │         │
│  │    - AI_TEMPERATURE = 0.3                                      │         │
│  │    - MAX_FILE_SIZE = 10MB                                      │         │
│  │    - ALLOWED_EXTENSIONS = {.pdf, .doc, .docx, .txt}            │         │
│  │    - CORS_ORIGINS = [...]                                      │         │
│  │                                                                 │         │
│  │  ● Single source of truth for all configuration                │         │
│  │  ● Loaded once at application startup                          │         │
│  │  ● Used by all modules                                         │         │
│  └────────────────────────────────────────────────────────────────┘         │
│                                   ▲                                          │
│                                   │                                          │
│                         Reads from .env file                                │
│                                   │                                          │
│                      ┌────────────┴────────────┐                            │
│                      │  .env (root directory)  │                            │
│                      │  CEREBRAS_API_KEY=xxx   │                            │
│                      └─────────────────────────┘                            │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                             UTILITIES                                        │
│                                                                              │
│  ┌─────────────────────┐                                                    │
│  │  json_cleaner.py    │                                                    │
│  │  ✅ KEPT             │                                                    │
│  ├─────────────────────┤                                                    │
│  │ - clean_and_parse_  │  Used by ai_agent.py to parse                     │
│  │   json()            │  AI response (removes ```json markers)            │
│  └─────────────────────┘                                                    │
└──────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                              DATA FLOW EXAMPLE
═══════════════════════════════════════════════════════════════════════════════

User Action: Upload resume.pdf + GitHub: "johndoe" + Role: "SDE"
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Step 1: Validate & Parse Resume                                             │
│   resume_parser.py                                                           │
│   ├─ validate_resume_file(resume.pdf, 2MB) → ✓ Valid                        │
│   └─ parse_resume(resume.pdf) → "Experienced in Python, Java, OOPS..."      │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Step 2: Extract Skills                                                       │
│   skill_extractor.py                                                         │
│   └─ extract_skills_from_resume(text) → ["Python", "Java", "OOPS"]          │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Step 3: Fetch GitHub Data                                                    │
│   main.py (fetch_github_summary)                                             │
│   └─ GET https://api.github.com/users/johndoe                                │
│      → { repos: 15, languages: ["Python", "JavaScript"], stars: 45 }         │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Step 4: Match Role Skills                                                    │
│   role_matcher.py                                                            │
│   └─ match_role_skills("SDE", ["Python", "Java", "OOPS"])                   │
│      → Required: ["Python", "Java", "C++", "Data Structures", "Algorithms"] │
│      → Present: ["Python", "Java", "OOPS"]                                   │
│      → Missing: ["Data Structures", "Algorithms"]                            │
│      → Match: 60%                                                            │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Step 5: Build AI Input                                                       │
│   main.py                                                                    │
│   {                                                                          │
│     "resume_text": "Experienced in Python...",                               │
│     "github_summary": { repos: 15, ... },                                    │
│     "target_role": "SDE",                                                    │
│     "required_skills": [...],                                                │
│     "present_skills": [...],                                                 │
│     "missing_skills": [...]                                                  │
│   }                                                                          │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Step 6: AI Analysis                                                          │
│   ai_agent.py → Cerebras API                                                 │
│   → Returns:                                                                 │
│   {                                                                          │
│     "skill_gap_summary": "You need to focus on DSA...",                      │
│     "resume_improvements": [                                                 │
│       "Add quantifiable achievements...",                                    │
│       "Highlight collaborative work..."                                      │
│     ],                                                                       │
│     "roadmap": {                                                             │
│       "Week 1": "Master Arrays and Linked Lists...",                         │
│       "Week 2": "Deep dive into Trees and Graphs...",                        │
│       ...                                                                    │
│     }                                                                        │
│   }                                                                          │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Step 7: Build Final Response                                                 │
│   main.py                                                                    │
│   {                                                                          │
│     "status": "success",                                                     │
│     "user_info": { ... },                                                    │
│     "skill_analysis": {                                                      │
│       "present_skills": [...],                                               │
│       "missing_skills": [...],                                               │
│       "match_percentage": 60                                                 │
│     },                                                                       │
│     "github_summary": { ... },                                               │
│     "ai_analysis": { ... }  ← From Step 6                                    │
│   }                                                                          │
└──────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                        Return to Frontend (result.html)


═══════════════════════════════════════════════════════════════════════════════
                              KEY BENEFITS
═══════════════════════════════════════════════════════════════════════════════

✅ Clean Separation: Each layer has one responsibility
✅ Modular: Easy to test, modify, or replace components
✅ Scalable: Can add new services without affecting existing code
✅ Maintainable: Clear structure, easy to understand
✅ Production-Ready: Proper error handling, validation, logging-ready
✅ Config-Driven: Change behavior without modifying code
✅ Type-Safe: Type hints throughout (where applicable)

```
