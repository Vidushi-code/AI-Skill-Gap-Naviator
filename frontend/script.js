
// ===========================
// Input Page (index.html)
// ===========================

if (document.getElementById('analysisForm')) {
    const form = document.getElementById('analysisForm');
    const fileInput = document.getElementById('resumeUpload');
    const fileLabel = fileInput.nextElementSibling;
    const fileText = document.getElementById('fileText');

    // File input handling
    fileInput.addEventListener('change', function(e) {
        if (this.files && this.files.length > 0) {
            const fileName = this.files[0].name;
            fileText.textContent = fileName;
            fileLabel.classList.add('has-file');
        } else {
            fileText.textContent = 'Choose your resume';
            fileLabel.classList.remove('has-file');
        }
    });

    // Form submission handling
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate form
        const resume = fileInput.files[0];
        const github = document.getElementById('githubUsername').value.trim();
        const jobDescription = document.getElementById('jobDescription').value.trim();

        if (!resume) {
            alert('Please upload your resume');
            return;
        }

        if (!github) {
            alert('Please enter your GitHub username');
            return;
        }

        if (!jobDescription) {
            alert('Please paste a job description');
            return;
        }

        try {
            const submitBtn = form.querySelector("button[type='submit']");
            submitBtn.innerText = "Analyzing...";
            submitBtn.disabled = true;

            const formData = new FormData();
            formData.append("resume", resume);
            formData.append("github_username", github);
            formData.append("job_description", jobDescription);

            const response = await fetch("https://ai-skill-gap-naviator.onrender.com/analyze", {
                method: "POST",
                body: formData
            });

            console.log("=== BACKEND RESPONSE ===");
            console.log("Status:", response.status);
            console.log("OK:", response.ok);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || "Server error");
            }

            const data = await response.json();
            
            // Debug: Log backend response
            console.log("=== RECEIVED DATA ===");
            console.log(JSON.stringify(data, null, 2));

            // Store real analysis result
            sessionStorage.setItem("analysisResult", JSON.stringify(data));

            // Redirect to results page
            window.location.href = "result.html";

        } catch (error) {
            alert("Error: " + error.message);
            const submitBtn = form.querySelector("button[type='submit']");
            submitBtn.innerText = "Analyze Profile";
            submitBtn.disabled = false;
        }
    });
}

// ===========================
// Result Page (result.html)
// ===========================

if (document.getElementById('skillGapSummary')) {
    // Get data from sessionStorage
    const analysisData = JSON.parse(sessionStorage.getItem("analysisResult"));
    
    // Debug: Log the full analysis data
    console.log("=== FULL ANALYSIS DATA ===");
    console.log(JSON.stringify(analysisData, null, 2));
    
    if (!analysisData || !analysisData.ai_analysis) {
        alert("No analysis data found. Please go back and submit the form.");
        window.location.href = "index.html";
    } else {
        const aiAnalysis = analysisData.ai_analysis;
        
        // Debug: Log AI analysis details
        console.log("=== AI ANALYSIS ===");
        console.log("Match Percentage:", aiAnalysis.match_percentage);
        console.log("Required Skills:", aiAnalysis.required_skills);
        console.log("Existing Skills:", aiAnalysis.existing_skills);
        console.log("Missing Skills:", aiAnalysis.missing_skills);
        
        // Render Match Percentage
        const matchPercentage = aiAnalysis.match_percentage || 0;
        const matchElement = document.getElementById('matchPercentage');
        const progressFill = document.getElementById('progressFill');
        
        matchElement.textContent = `${matchPercentage}%`;
        progressFill.style.width = `${matchPercentage}%`;
        
        // Add color coding based on percentage
        if (matchPercentage >= 75) {
            progressFill.classList.add('high-match');
        } else if (matchPercentage >= 50) {
            progressFill.classList.add('medium-match');
        } else {
            progressFill.classList.add('low-match');
        }
        
        // Render Required Skills
        const requiredSkillsContainer = document.getElementById('requiredSkills');
        if (aiAnalysis.required_skills && Array.isArray(aiAnalysis.required_skills)) {
            aiAnalysis.required_skills.forEach(skill => {
                const tag = document.createElement('span');
                tag.className = 'skill-tag required';
                tag.textContent = skill;
                requiredSkillsContainer.appendChild(tag);
            });
        }
        
        // Render Existing Skills
        const existingSkillsContainer = document.getElementById('existingSkills');
        if (aiAnalysis.existing_skills && Array.isArray(aiAnalysis.existing_skills)) {
            if (aiAnalysis.existing_skills.length > 0) {
                aiAnalysis.existing_skills.forEach(skill => {
                    const tag = document.createElement('span');
                    tag.className = 'skill-tag existing';
                    tag.textContent = skill;
                    existingSkillsContainer.appendChild(tag);
                });
            } else {
                existingSkillsContainer.innerHTML = '<p class="empty-state">None found in your resume</p>';
            }
        }
        
        // Render Missing Skills
        const missingSkillsContainer = document.getElementById('missingSkills');
        if (aiAnalysis.missing_skills && Array.isArray(aiAnalysis.missing_skills)) {
            if (aiAnalysis.missing_skills.length > 0) {
                aiAnalysis.missing_skills.forEach(skill => {
                    const tag = document.createElement('span');
                    tag.className = 'skill-tag missing';
                    tag.textContent = skill;
                    missingSkillsContainer.appendChild(tag);
                });
            } else {
                missingSkillsContainer.innerHTML = '<p class="empty-state">🎉 You have all required skills!</p>';
            }
        }
        
        // Render Skill Gap Summary
        const summaryElement = document.getElementById('skillGapSummary');
        summaryElement.textContent = aiAnalysis.skill_gap_summary || "No summary available";

        // Render Resume Improvements
        const improvementsList = document.getElementById('resumeImprovements');
        if (aiAnalysis.resume_improvements && Array.isArray(aiAnalysis.resume_improvements)) {
            aiAnalysis.resume_improvements.forEach(improvement => {
                const li = document.createElement('li');
                li.innerHTML = `<span class="check-icon">✓</span> ${improvement}`;
                improvementsList.appendChild(li);
            });
        }

        // Render Roadmap
        const roadmapGrid = document.getElementById('roadmapGrid');
        if (aiAnalysis.roadmap && typeof aiAnalysis.roadmap === 'object') {
            Object.entries(aiAnalysis.roadmap).forEach(([week, description]) => {
                const card = document.createElement('div');
                card.className = 'roadmap-card';
                
                const heading = document.createElement('h4');
                heading.textContent = week.charAt(0).toUpperCase() + week.slice(1);
                
                const paragraph = document.createElement('p');
                paragraph.textContent = description;
                
                card.appendChild(heading);
                card.appendChild(paragraph);
                roadmapGrid.appendChild(card);
            });
        }
    }
}

// ===========================
// Utility Functions
// ===========================

// Smooth scroll behavior for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});


function handlePerfectMatchRoadmap(matchScore) {
    if (parseInt(matchScore) === 100) {
        const roadmap = {
            week1: "Review core concepts related to the target role and revisit previous projects to improve code quality.",
            week2: "Optimize GitHub repositories by improving documentation, README files, and project descriptions.",
            week3: "Refine your resume and highlight role-relevant projects with measurable achievements.",
            week4: "Prepare for technical interviews by revising key concepts and practicing project explanations."
        };

        return roadmap;
    }

    return null; // return null if match is not 100
}


if (!response.ok) {
    throw new Error("API request failed");
}