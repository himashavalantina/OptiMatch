document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('matchForm');
    const dropZone = document.getElementById('dropZone');
    const cvInput = document.getElementById('cvInput');
    const fileNameDisplay = document.getElementById('fileName');
    const submitBtn = document.getElementById('submitBtn');
    
    // Drag & Drop Functionality
    dropZone.addEventListener('click', () => cvInput.click());
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-active');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-active');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-active');
        
        if (e.dataTransfer.files.length) {
            cvInput.files = e.dataTransfer.files;
            updateFileName();
        }
    });
    
    cvInput.addEventListener('change', updateFileName);
    
    function updateFileName() {
        if (cvInput.files.length) {
            fileNameDisplay.textContent = cvInput.files[0].name;
            fileNameDisplay.innerHTML = `<i class="fa-solid fa-check-circle"></i> ` + cvInput.files[0].name;
        }
    }
    
    // Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!cvInput.files.length) {
            alert('Please upload your CV first!');
            return;
        }
        
        const formData = new FormData(form);
        
        // UI State changes
        document.getElementById('loader').classList.remove('hidden');
        document.getElementById('resultsSection').classList.add('hidden');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Analyzing...</span> <i class="fa-solid fa-spinner fa-spin"></i>';
        
        try {
            const response = await fetch('/api/match', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                renderResults(data);
            } else {
                alert('Error: ' + (data.error || 'Something went wrong processing your request.'));
            }
        } catch (error) {
            alert('Network error. Is the backend running?');
            console.error(error);
        } finally {
            document.getElementById('loader').classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span>Find My Matches</span> <i class="fa-solid fa-wand-magic-sparkles"></i>';
        }
    });
    
    function renderResults(data) {
        const resultsSection = document.getElementById('resultsSection');
        const jobsColumn = document.getElementById('jobsColumn');
        const coursesColumn = document.getElementById('coursesColumn');
        const jobsList = document.getElementById('jobsList');
        const coursesList = document.getElementById('coursesList');
        
        // Reset
        jobsList.innerHTML = '';
        coursesList.innerHTML = '';
        jobsColumn.classList.add('hidden');
        coursesColumn.classList.add('hidden');
        
        resultsSection.classList.remove('hidden');
        
        if (data.jobs && data.jobs.length > 0) {
            jobsColumn.classList.remove('hidden');
            data.jobs.forEach((job, index) => {
                jobsList.innerHTML += `
                    <a href="${job.url}" target="_blank" class="result-card" style="--delay: ${index}">
                        <div class="match-badge">${job.score}% Match</div>
                        <h3 class="card-title">${job.title}</h3>
                        <div class="card-meta">
                            <i class="fa-regular fa-building"></i> ${job.company} 
                            ${job.location ? `| <i class="fa-solid fa-location-dot"></i> ${job.location}` : ''}
                        </div>
                    </a>
                `;
            });
        }
        
        if (data.courses && data.courses.length > 0) {
            coursesColumn.classList.remove('hidden');
            data.courses.forEach((course, index) => {
                coursesList.innerHTML += `
                    <a href="${course.url}" target="_blank" class="result-card" style="--delay: ${index}">
                        <div class="match-badge">${course.score}% Match</div>
                        <h3 class="card-title">${course.title}</h3>
                        <div class="card-meta">
                            <i class="fa-solid fa-laptop-code"></i> ${course.platform || 'Online Platform'}
                        </div>
                    </a>
                `;
            });
        }
        
        if (!data.jobs?.length && !data.courses?.length) {
            jobsColumn.classList.remove('hidden');
            jobsList.innerHTML = '<p style="color: var(--text-muted)">No matches found based on your criteria.</p>';
        }
        
        // Smooth scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
});
