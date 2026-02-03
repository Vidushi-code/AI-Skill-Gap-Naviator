# Requirements Document: AI Skill Gap Navigator

## Introduction

The AI Skill Gap Navigator addresses a critical challenge in the Indian education and employment ecosystem: the significant gap between academic learning and industry requirements, particularly affecting students from Tier-2 and Tier-3 colleges. These students often lack access to quality career guidance, industry mentorship, and awareness of current market demands, leading to lower employability rates despite technical competence.

This AI-powered web application analyzes students' resumes and GitHub profiles to provide personalized, actionable employability roadmaps. By leveraging artificial intelligence for skill gap analysis and roadmap generation, the system delivers insights that would be impossible through rule-based approaches, considering the dynamic nature of technology roles and the complexity of skill interdependencies.

The system is designed to be practical and easy to implement, using AI in a meaningful way to create real-world impact for underserved student communities.

## Glossary

- **System**: The AI Skill Gap Navigator web application
- **Student**: Primary user - undergraduate or recent graduate seeking employment guidance
- **Resume_Analyzer**: AI component that extracts and analyzes skills from resume documents
- **GitHub_Analyzer**: AI component that evaluates coding skills from GitHub repositories
- **Skill_Gap_Engine**: AI component that identifies missing skills for target roles
- **Roadmap_Generator**: AI component that creates personalized learning paths
- **Target_Role**: Specific job position the student aims to achieve (e.g., Frontend Developer, Data Scientist)
- **Skill_Gap**: Difference between student's current skills and role requirements
- **Employability_Roadmap**: Personalized action plan with learning resources and timeline
- **LLM_Service**: Large Language Model service (OpenAI API or Gemini API)

## Requirements

### Requirement 1: Resume Analysis and Skill Extraction

**User Story:** As a student from a Tier-2/Tier-3 college, I want to upload my resume and have it analyzed for skills, so that I can understand my current technical competencies.

#### Acceptance Criteria

1. WHEN a student uploads a resume file (PDF or DOCX), THE Resume_Analyzer SHALL extract text content and identify technical skills
2. WHEN the resume contains programming languages, frameworks, or tools, THE Resume_Analyzer SHALL categorize them by skill type (programming, frameworks, databases, tools)
3. WHEN skill extraction is complete, THE System SHALL display identified skills with AI-estimated relevance indicators
4. WHEN the uploaded file is not a valid resume format, THE System SHALL return a descriptive error message
5. WHEN resume analysis fails, THE System SHALL provide fallback options for manual skill input

### Requirement 2: GitHub Profile Integration and Code Analysis

**User Story:** As a student with coding projects, I want my GitHub profile analyzed, so that I can get insights into my practical programming skills beyond what's listed on my resume.

#### Acceptance Criteria

1. WHEN a student provides a GitHub username, THE GitHub_Analyzer SHALL fetch public repositories using GitHub REST API
2. WHEN repositories are retrieved, THE GitHub_Analyzer SHALL analyze code languages, commit patterns, and project complexity
3. WHEN analyzing repositories, THE System SHALL identify practical skills demonstrated through actual code implementation
4. WHEN the GitHub profile is private or inaccessible, THE System SHALL continue with resume-only analysis
5. WHEN GitHub API rate limits are exceeded, THE System SHALL display appropriate error messages and suggest manual retry

### Requirement 3: Role-Specific Skill Gap Identification

**User Story:** As a student targeting a specific career path, I want to select my desired role and understand what skills I'm missing, so that I can focus my learning efforts effectively.

#### Acceptance Criteria

1. WHEN a student selects a Target_Role from predefined options, THE Skill_Gap_Engine SHALL compare current skills against role requirements
2. WHEN skill comparison is complete, THE System SHALL identify missing skills categorized by importance (critical, important, nice-to-have)
3. WHEN generating skill gaps, THE System SHALL consider technical skills and lightly infer soft skills from resume language and keywords without deep behavioral analysis
4. WHEN multiple skill sources exist (resume + GitHub), THE System SHALL intelligently merge and prioritize skill evidence
5. WHEN role requirements are updated, THE System SHALL reflect changes in future gap analyses

### Requirement 4: AI-Powered Personalized Roadmap Generation

**User Story:** As a student with identified skill gaps, I want a personalized learning roadmap, so that I can systematically improve my employability with clear, actionable steps.

#### Acceptance Criteria

1. WHEN skill gaps are identified, THE Roadmap_Generator SHALL create a time-sequenced learning plan with specific milestones
2. WHEN generating roadmaps, THE System SHALL recommend free and affordable learning resources suitable for Indian students
3. WHEN creating timelines, THE System SHALL consider student's current skill level and typical learning curves
4. WHEN roadmap includes practical projects, THE System SHALL suggest GitHub-worthy implementations to build portfolio
5. WHEN multiple learning paths exist, THE System SHALL prioritize based on job market demand and student's existing strengths

### Requirement 5: Resume Enhancement Recommendations

**User Story:** As a student preparing for job applications, I want specific feedback on improving my resume, so that I can better showcase my skills to potential employers.

#### Acceptance Criteria

1. WHEN resume analysis is complete, THE System SHALL provide specific improvement suggestions for content and formatting
2. WHEN technical skills are underrepresented, THE System SHALL recommend ways to better highlight programming experience
3. WHEN resume lacks industry keywords, THE System SHALL suggest relevant terms for the target role
4. WHEN project descriptions are weak, THE System SHALL provide templates for better technical project presentation
5. WHEN resume format is suboptimal, THE System SHALL recommend ATS-friendly formatting improvements

### Requirement 6: Data Privacy and Security

**User Story:** As a student sharing personal information, I want my data to be secure and private, so that I can use the system without privacy concerns.

#### Acceptance Criteria

1. WHEN students upload resumes, THE System SHALL process documents without storing personal information permanently
2. WHEN GitHub data is accessed, THE System SHALL only use publicly available information and respect API terms
3. WHEN user sessions end, THE System SHALL clear temporary data and analysis results
4. WHEN data processing occurs, THE System SHALL use secure connections and encrypt sensitive information
5. WHEN users request data deletion, THE System SHALL remove all associated information within 24 hours

### Requirement 7: Performance and Scalability

**User Story:**As a hackathon participant, I want the system to perform reliably during demonstrations, so that the core functionality can be clearly showcased to judges.

### Acceptance Criteria

1.WHEN processing a resume, THE System SHALL complete analysis within a reasonable time suitable for live demo conditions
2.WHEN multiple users access the system concurrently, THE System SHALL remain responsive without crashing or blocking core workflows
3.WHEN GitHub analysis is performed, THE System SHALL handle API rate limits gracefully and inform the user if a retry is required
4.WHEN LLM API calls experience delays or failures, THE System SHALL implement timeout handling and controlled retries to ensure system stability
5.WHEN system resources are limited, THE System SHALL prioritize essential features over non-critical functionality to maintain demo reliability

### Requirement 8: AI Integration and Justification

**User Story:**As a hackathon judge, I want to clearly understand why artificial intelligence is essential to this solution, so that I can evaluate whether AI is being used meaningfully rather than superficially.

### Acceptance Criteria

1.WHEN analyzing resumes, THE System SHALL use AI-based language understanding to extract and interpret technical skills from varied resume formats, including skills that are not explicitly listed
2.WHEN processing GitHub repositories, THE System SHALL use AI-assisted analysis to infer project complexity and practical skill usage based on repository metadata, structure, and code context, rather than relying only on language counts
3.WHEN identifying skill gaps, THE System SHALL use AI to compare the student’s profile against role-specific expectations and highlight missing or weak areas in a contextual manner
4.WHEN generating learning roadmaps, THE System SHALL use AI to personalize recommendations based on the student’s current skills, target role, and commonly expected industry skill progressions
5.WHEN providing guidance and recommendations, THE System SHALL use AI to generate clear, contextual, and actionable suggestions tailored to the individual student profile

### Requirement 9: Hackathon Constraints and MVP Scope

**User Story:** As a project team, we want a clearly scoped MVP that demonstrates the core value of the solution, so that a stable and complete system can be delivered within limited development time.

#### Acceptance Criteria

1.WHEN implementing the system, THE System SHALL support a limited set of high-demand technical roles (e.g., Frontend, Backend, Full-Stack, Data Science, DevOps) to ensure depth over breadth
2.WHEN developing features, THE System SHALL prioritize the end-to-end core workflow over non-essential features such as user authentication or advanced analytics
3.WHEN integrating AI capabilities, THE System SHALL use direct API calls to a single LLM provider (OpenAI or Gemini) without introducing agent frameworks or orchestration layers
4.WHEN designing the system architecture, THE System SHALL adopt a monolithic structure optimized for rapid development, testing, and demo deployment
5.WHEN selecting technologies, THE System SHALL adhere to the predefined technology stack and avoid introducing additional frameworks unless required to support core functionality

### Requirement 10: Impact Measurement and Success Criteria (Post-MVP)

**User Story:** As a solution evaluator, I want clear and realistic indicators of impact and success, so that the practical value of the system can be assessed within a hackathon setting.

#### Acceptance Criteria

1.WHEN students complete the analysis, THE System SHALL demonstrate accurate skill extraction and gap identification through controlled demo scenarios
2.WHEN personalized roadmaps are generated, THE System SHALL present recommendations that are relevant, actionable, and appropriate for the intended student audience
3.WHEN learning resources are suggested, THE System SHALL prioritize freely available or low-cost options suitable for Indian students
4.WHEN system performance is evaluated during demonstration, THE System SHALL maintain stable and responsive behavior suitable for live presentation
5.WHEN overall impact is assessed, THE System SHALL clearly communicate its value proposition through concrete use-case walkthroughs, with advanced tracking and feedback mechanisms explicitly planned for post-hackathon development
