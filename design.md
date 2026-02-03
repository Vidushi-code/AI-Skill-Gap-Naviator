# Design Document: AI Skill Gap Navigator

## Overview

The AI Skill Gap Navigator is a web-based application that leverages artificial intelligence to analyze student resumes and GitHub profiles, identify skill gaps for target roles, and generate personalized employability roadmaps. The system is specifically designed for Tier-2 and Tier-3 college students in India, addressing the critical gap between academic learning and industry requirements.

The application follows a streamlined architecture optimized for hackathon development constraints while demonstrating meaningful AI integration. It processes unstructured data such as resumes and code repositories and converts it into actionable insights using AI-powered analysis, which would be impractical to achieve using purely rule-based approaches.
## Architecture Design

### High-Level Architecture

The system follows a three-tier architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (Web UI)      │◄──►│   (FastAPI)     │◄──►│   Services      │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │    │ • API Routes    │    │ • OpenAI/Gemini │
│ • File Upload   │    │ • AI Processing │    │ • GitHub API    │
│ • Results UI    │    │ • Data Models   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Database      │
                       │  (PostgreSQL)   │
                       │                 │
                       │ • User Sessions │
                       │ • Analysis Data │
                       │ • Role Profiles │
                       └─────────────────┘
```

### Layer Responsibilities

**Frontend Layer:**
- Responsive web interface for file uploads and result display
- Real-time feedback during processing
- Clean, accessible UI suitable for diverse user backgrounds

**Backend Layer:**
- RESTful API endpoints for all operations
- AI workflow orchestration
- Data validation and error handling
- Session management

**Data Layer:**
- Temporary storage for analysis sessions
- Role requirement templates
- Learning resource database

**External Integration Layer:**
- LLM API integration (OpenAI/Gemini)
- GitHub REST API integration
- Graceful handling of external service limitations

## Component Breakdown

### Frontend Components

**File Upload Interface:**
- Drag-and-drop resume upload (PDF/DOCX support)
- GitHub username input with validation
- Role selection dropdown with popular tech roles
- Progress indicators for long-running operations

**Results Dashboard:**
- Skill visualization with categorization
- Interactive skill gap analysis
- Personalized roadmap display with timeline
- Resume improvement suggestions
- Downloadable action plan

**Technology Choice:** Vanilla HTML/CSS/JavaScript or lightweight React for rapid development and minimal complexity.

### Backend (FastAPI) Components

**API Routes:**
- `POST /upload-resume` - Handle resume file processing
- `POST /analyze-github` - Process GitHub profile analysis
- `POST /generate-roadmap` - Create personalized learning path
- `GET /roles` - Retrieve available target roles
- `GET /analysis/{session_id}` - Fetch analysis results

**Core Services:**
- `ResumeProcessor` - Extract and parse resume content
- `GitHubAnalyzer` - Fetch and analyze repository data
- `SkillExtractor` - AI-powered skill identification
- `GapAnalyzer` - Compare skills against role requirements
- `RoadmapGenerator` - Create personalized learning paths

**Data Models:**
- `StudentProfile` - Aggregated skill and experience data
- `SkillGap` - Identified missing skills with priority levels
- `LearningRoadmap` - Structured action plan with resources
- `AnalysisSession` - Temporary session data management

### AI/LLM Layer

**Resume Analysis Pipeline:**
```
PDF/DOCX → Text Extraction → AI Skill Extraction → Skill Categorization
```

**GitHub Analysis Pipeline:**
```
Username → Repository Fetch → Code Analysis → Practical Skill Inference
```

**Skill Gap Analysis:**
```
Current Skills + Target Role → AI Comparison → Prioritized Gap List
```

**Roadmap Generation:**
```
Skill Gaps + Student Profile → AI Planning → Personalized Learning Path
```

### Database (PostgreSQL)

**Core Tables:**
- `analysis_sessions` - Temporary session storage
- `role_requirements` - Predefined skill requirements for target roles
- `learning_resources` - Curated educational content database
- `skill_categories` - Standardized skill taxonomy

**Data Retention Policy:**
- Session data automatically purged after 24 hours
- No permanent storage of personal information
- Anonymized usage analytics only

### External Integrations

**GitHub REST API:**
- Repository listing and metadata
- Language statistics and commit analysis
- Rate limiting handling with graceful degradation
- Public repository focus (no authentication required)

**LLM Service (OpenAI/Gemini):**
- Direct API integration without agent frameworks
- Structured prompts for consistent output
- Error handling and retry logic
- Cost optimization through efficient prompt design

## AI Workflow

### Resume Processing Pipeline

**Step 1: Text Extraction**
- Use `pdfplumber` for PDF processing and `python-docx` for DOCX files
- Clean and normalize extracted text
- Handle various resume formats and layouts

**Step 2: AI-Powered Skill Extraction**
```python
# Prompt Template Example
prompt = f"""
Analyze this resume text and extract technical skills:

{resume_text}

Return a JSON object with:
- programming_languages: []
- frameworks: []
- databases: []
- tools: []
- soft_skills: []

Focus on explicit mentions and reasonable inferences from project descriptions.
"""
```

**Step 3: Skill Validation and Categorization**
- Cross-reference extracted skills with industry taxonomy
- Assign relevance indicators based on context
- Handle skill variations and synonyms

### GitHub Repository Analysis

**Step 1: Repository Data Collection**
```python
# GitHub API Integration
repos = github_client.get_user_repos(username)
languages = github_client.get_repo_languages(repo_name)
commits = github_client.get_repo_commits(repo_name, limit=50)
```

**Step 2: Basic Repository Analysis**
```python
# AI Analysis Prompt
prompt = f"""
Analyze these GitHub repositories for programming skills:

Repository Data:
{repo_summary}

Provide lightweight AI-assisted inference for:
1. Programming language usage based on file counts and sizes
2. Framework identification from repository metadata
3. Basic project scope indicators
4. Repository structure analysis

Return structured assessment of demonstrated skills.
"""
```

**Step 3: Practical Skill Inference**
- Combine language statistics with metadata-based indicators
- Identify frameworks and libraries from repository structure
- Basic repository structure analysis for project scope
- Simple version control activity patterns

### Skill Gap Identification

**Step 1: Role Requirement Mapping**
- Load predefined skill requirements for target roles
- Include both technical and essential soft skills
- Consider Indian job market specifics

**Step 2: AI-Powered Gap Analysis**
```python
# Gap Analysis Prompt
prompt = f"""
Compare current skills against target role requirements:

Current Skills: {student_skills}
Target Role: {role_name}
Role Requirements: {role_requirements}

Identify skill gaps categorized as:
- Critical: Essential for role entry
- Important: Valuable for competitiveness  
- Nice-to-have: Beneficial for growth

Consider skill transferability and learning curves.
"""
```

**Step 3: Priority Assignment**
- Rank gaps by importance and achievability
- Consider student's existing foundation
- Factor in market demand and hiring trends

### Roadmap Generation Logic

**Step 1: Learning Path Planning**
```python
# Roadmap Generation Prompt
prompt = f"""
Create a personalized learning roadmap for:

Student Profile: {student_profile}
Skill Gaps: {prioritized_gaps}
Timeline: 6-12 months
Budget: Free/affordable resources preferred

Generate:
1. Phase-wise learning plan
2. Specific resource recommendations
3. Practical project suggestions
4. Milestone checkpoints

Focus on resources accessible to Indian students.
"""
```

**Step 2: Resource Curation**
- Prioritize free and affordable learning platforms
- Include hands-on project suggestions
- Recommend GitHub portfolio improvements
- Suggest relevant certifications

**Step 3: Timeline Optimization**
- Balance learning intensity with feasibility
- Sequence skills based on dependencies
- Include regular assessment checkpoints
- Adapt to student's current commitments

## Data Flow Diagram

### End-to-End Process Flow

```
1. Student uploads resume + provides GitHub username
   ↓
2. System extracts text from resume (pdfplumber/python-docx)
   ↓
3. AI analyzes resume text for skills (OpenAI/Gemini API)
   ↓
4. System fetches GitHub repositories (GitHub REST API)
   ↓
5. AI analyzes code repositories for practical skills
   ↓
6. Student selects target role from predefined options
   ↓
7. AI compares current skills vs role requirements
   ↓
8. System identifies and prioritizes skill gaps
   ↓
9. AI generates personalized learning roadmap
   ↓
10. System presents comprehensive analysis and recommendations
```

### Data Processing Pipeline

**Input Processing:**
- Resume file → Text extraction → Skill identification
- GitHub username → Repository data → Code analysis
- Role selection → Requirement matching → Gap calculation

**AI Processing:**
- Structured prompts for consistent output
- JSON response parsing and validation
- Error handling for malformed responses
- Fallback strategies for API failures

**Output Generation:**
- Skill visualization with categories
- Gap analysis with priority levels
- Roadmap with timeline and resources
- Resume improvement suggestions

## Technology Stack Justification

### FastAPI (Backend Framework)
**Why chosen:** 
- Rapid development with automatic API documentation
- Built-in async support for external API calls
- Type hints for better code quality
- Excellent performance for hackathon demos

**Hackathon suitability:** Fast setup, clear documentation, handles file uploads efficiently

### PostgreSQL (Database)
**Why chosen:**
- Reliable relational database for structured data
- JSON support for flexible skill data storage
- ACID compliance for data integrity
- Easy deployment and management

**Hackathon suitability:** Quick setup, familiar SQL interface, robust for demo scenarios

### OpenAI/Gemini API (AI Processing)
**Why chosen:**
- Direct API access without complex frameworks
- Proven performance for text analysis tasks
- Structured output capabilities
- Cost-effective for hackathon scope

**Hackathon suitability:** Simple integration, reliable performance, clear pricing model

### HTML/CSS/JavaScript Frontend
**Why chosen:**
- Minimal setup and deployment complexity
- Universal browser compatibility
- Fast development iteration
- No build process required

**Hackathon suitability:** Immediate deployment, easy debugging, focus on functionality over complexity

### GitHub REST API (External Integration)
**Why chosen:**
- Comprehensive repository data access
- No authentication required for public repos
- Well-documented with Python libraries
- Rate limiting suitable for demo usage

**Hackathon suitability:** Free access, extensive documentation, reliable uptime

## Scalability & Future Enhancements

### Post-Hackathon Possibilities

**Performance Optimization:**
- Implement caching for role requirements and common analyses
- Optimize AI prompts for faster response times
- Implement database indexing for improved query performance

**Feature Expansion:**
- User account system with analysis history
- Advanced portfolio project recommendations
- Integration with job boards and company requirements
- Mobile application development

**AI Enhancement:**
- Fine-tuned models for Indian job market specifics
- Multi-language support for regional preferences

**Market Expansion Potential:**
- Adaptation for other emerging markets
- Educational partnerships with colleges
- Integration with placement systems

## Risks & Mitigations

### AI-Related Risks

**Risk: AI Hallucinations and Inaccurate Analysis**
- *Mitigation:* Implement structured prompts with clear constraints
- *Mitigation:* Add confidence indicators and manual review options
- *Mitigation:* Provide fallback manual input methods
- *Mitigation:* Include disclaimers about AI-generated recommendations

**Risk: Inconsistent Skill Extraction**
- *Mitigation:* Use standardized skill taxonomy and validation
- *Mitigation:* Implement multiple extraction approaches with consensus
- *Mitigation:* Allow user verification and correction of extracted skills
- *Mitigation:* Continuous prompt refinement based on feedback

### Technical Risks

**Risk: External API Limitations**
- *Mitigation:* Implement graceful degradation for API failures
- *Mitigation:* Add retry logic with exponential backoff
- *Mitigation:* Provide alternative analysis paths when APIs are unavailable
- *Mitigation:* Monitor API usage and implement rate limiting

**Risk: File Processing Failures**
- *Mitigation:* Support multiple file formats with fallback options
- *Mitigation:* Implement robust error handling and user feedback
- *Mitigation:* Provide manual text input as backup method
- *Mitigation:* Add file validation and sanitization

### Data and Privacy Risks

**Risk: Sensitive Information Exposure**
- *Mitigation:* Implement automatic data purging after session completion
- *Mitigation:* Process files in memory without permanent storage
- *Mitigation:* Use secure connections for all data transmission
- *Mitigation:* Provide clear privacy policy and data handling transparency

**Risk: GitHub Profile Privacy Concerns**
- *Mitigation:* Only access publicly available repository information
- *Mitigation:* Clearly communicate what data is being accessed
- *Mitigation:* Provide opt-out options for GitHub analysis
- *Mitigation:* Respect GitHub API terms of service and rate limits

### Business and Market Risks

**Risk: Limited Hackathon Scope Demonstration**
- *Mitigation:* Focus on core value proposition with clear demo scenarios
- *Mitigation:* Prepare compelling use cases with realistic student profiles
- *Mitigation:* Emphasize scalability potential and market opportunity
- *Mitigation:* Document clear roadmap for post-hackathon development

**Risk: Competition from Established Platforms**
- *Mitigation:* Focus on underserved Tier-2/Tier-3 student market
- *Mitigation:* Emphasize AI-powered personalization as key differentiator
- *Mitigation:* Build for Indian market specifics and cultural context
- *Mitigation:* Plan for rapid iteration and feature development post-hackathon

## Error Handling

### Input Validation and Sanitization
- **File Upload Validation**: Verify file types, sizes, and content before processing
- **GitHub Username Validation**: Check format and existence before API calls
- **Role Selection Validation**: Ensure selected roles exist in predefined options
- **Data Sanitization**: Clean and validate all user inputs to prevent injection attacks

### External Service Failures
- **LLM API Failures**: Implement retry logic with exponential backoff and fallback to cached responses
- **GitHub API Failures**: Graceful degradation to resume-only analysis when GitHub is unavailable
- **Database Connection Issues**: Temporary in-memory storage with periodic retry attempts
- **Network Timeouts**: Configurable timeout values with user notification of delays

### AI Processing Errors
- **Malformed AI Responses**: JSON parsing validation with fallback to manual processing
- **Skill Extraction Failures**: Alternative extraction methods using keyword matching
- **Roadmap Generation Issues**: Template-based fallback roadmaps for common scenarios
- **Confidence Threshold Management**: Minimum confidence requirements for AI-generated content

### User Experience Error Handling
- **Progress Indicators**: Real-time feedback during long-running operations
- **Error Recovery Options**: Clear paths for users to retry or modify inputs
- **Partial Results Display**: Show available results even when some components fail
- **Help and Support**: Contextual guidance for common error scenarios

## Testing Strategy

### Basic Testing Approach

The system requires focused testing suitable for hackathon development:

**Unit Tests** focus on:
- Core component functionality with mock external services
- File upload and processing workflows
- Basic API endpoint validation
- Error handling for common failure scenarios

**Manual Demo Validation:**
- End-to-end workflow testing with sample data
- User interface functionality verification
- External API integration with real services (limited scope)
- Performance validation under demo conditions

### Testing Implementation

**Component-Level Testing:**
- Resume text extraction with sample PDF/DOCX files
- GitHub API integration with mock responses
- AI prompt construction and response parsing
- Database operations and session management

**Demo Preparation:**
- Prepare diverse sample resumes for demonstration
- Test with known GitHub profiles for consistent results
- Validate AI outputs for reasonableness and relevance
- Ensure system handles demo scenarios reliably