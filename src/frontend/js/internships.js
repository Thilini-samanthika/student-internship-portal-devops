document.addEventListener('DOMContentLoaded', async function () {
    // Check if user is logged in (optional for viewing, required for applying)
    const isLoggedIn = api.isLoggedIn();
    const logoutBtn = document.getElementById('logoutBtn');

    if (logoutBtn) {
        if (!isLoggedIn) {
            logoutBtn.textContent = 'Login';
            logoutBtn.href = 'login.html';
            logoutBtn.className = "text-sm font-medium px-4 py-2 bg-primary-600 text-white rounded-full hover:bg-primary-700 transition-all shadow-md hover:shadow-lg";
        } else {
            logoutBtn.addEventListener('click', function (e) {
                e.preventDefault();
                api.logout();
            });
        }
    }

    const internshipsContainer = document.getElementById('internships-container');
    const applicationForm = document.getElementById('applicationForm');

    // Modal Elements
    const modal = document.getElementById('applicationModal');
    const modalBackdrop = document.getElementById('modalBackdrop');
    const modalPanel = document.getElementById('modalPanel');
    const modalInternshipId = document.getElementById('modal-internship-id');
    const submitBtn = document.getElementById('submitApplication');
    const cancelModalBtn = document.getElementById('cancelModal');
    const applicationError = document.getElementById('application-error');

    // Modal Functions
    function showModal() {
        modal.classList.remove('hidden');
        // Trigger reflow
        void modal.offsetWidth;

        modalBackdrop.classList.remove('opacity-0');
        modalPanel.classList.remove('opacity-0', 'scale-95');
        modalPanel.classList.add('opacity-100', 'scale-100');
    }

    function hideModal() {
        modalBackdrop.classList.add('opacity-0');
        modalPanel.classList.add('opacity-0', 'scale-95');
        modalPanel.classList.remove('opacity-100', 'scale-100');

        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300); // Match transition duration
    }

    if (cancelModalBtn) {
        cancelModalBtn.addEventListener('click', hideModal);
    }

    // Close on backdrop click
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target === modalBackdrop) {
                hideModal();
            }
        });
    }

    // Load internships
    try {
        const result = await api.getInternships();

        if (result.ok) {
            renderInternships(result.data);
        } else {
            internshipsContainer.innerHTML = '<div class="col-span-full text-center p-4 bg-red-50 text-red-600 rounded-lg">Failed to load internships.</div>';
        }
    } catch (error) {
        console.error('Error loading internships:', error);
        internshipsContainer.innerHTML = '<div class="col-span-full text-center p-4 bg-red-50 text-red-600 rounded-lg">Error loading internships. Please try again later.</div>';
    }

    function renderInternships(internships) {
        if (!internships || internships.length === 0) {
            internshipsContainer.innerHTML = `
                <div class="col-span-full text-center p-12 bg-slate-50 rounded-2xl border border-dashed border-slate-300">
                    <h4 class="text-xl font-medium text-slate-800">No internships available</h4>
                    <p class="text-slate-500 mt-2">Please check back later for new opportunities.</p>
                </div>
            `;
            return;
        }

        internshipsContainer.innerHTML = internships.map(internship => `
            <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1 flex flex-col h-full group">
                <div class="p-6 flex-grow">
                    <div class="flex justify-between items-start mb-4">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700">
                            ${internship.duration || 'Flexible'}
                        </span>
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700">
                            ${internship.slots} Slots
                        </span>
                    </div>
                    <h5 class="text-xl font-bold text-slate-900 mb-2 group-hover:text-primary-600 transition-colors">${internship.title}</h5>
                    <h6 class="text-sm font-semibold text-slate-500 mb-4 uppercase tracking-wider">${internship.company}</h6>
                    <p class="text-slate-600 text-sm leading-relaxed mb-6 line-clamp-4">
                        ${internship.description}
                    </p>
                </div>
                <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 mt-auto">
                    <button class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm apply-btn"
                            data-id="${internship.id}" 
                            ${!isLoggedIn || api.getRole() !== 'student' ? 'disabled' : ''}>
                        ${!isLoggedIn ? 'Login to Apply' : (api.getRole() !== 'student' ? 'Student Only' : 'Apply Now')}
                    </button>
                    ${!isLoggedIn ? `<p class="text-xs text-center text-slate-400 mt-2">You must login as a student to apply</p>` : ''}
                </div>
            </div>
        `).join('');

        // Add event listeners to apply buttons
        if (isLoggedIn && api.getRole() === 'student') {
            document.querySelectorAll('.apply-btn').forEach(btn => {
                btn.addEventListener('click', function () {
                    const id = this.getAttribute('data-id');
                    modalInternshipId.value = id;
                    applicationError.style.display = 'none'; // Use class manipulation if possible, but style works for hidden/block legacy
                    applicationError.classList.add('hidden');
                    applicationError.textContent = '';

                    applicationForm.reset();
                    // Reset file name text
                    const fileName = document.getElementById('file-name');
                    if (fileName) fileName.textContent = '';

                    showModal();
                });
            });
        }
    }

    // Handle application submission
    submitBtn.addEventListener('click', async function () {
        if (!applicationForm.checkValidity()) {
            applicationForm.reportValidity();
            return;
        }

        const internshipId = modalInternshipId.value;
        const coverLetter = document.getElementById('cover-letter').value;
        const cvFile = document.getElementById('cv-file').files[0];

        if (!cvFile) {
            showError('Please upload your CV');
            return;
        }

        const formData = new FormData();
        formData.append('internship_id', internshipId);
        formData.append('cover_letter', coverLetter);
        formData.append('cv', cvFile);

        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';

        try {
            const result = await api.applyForInternship(formData);

            if (result.ok) {
                hideModal();
                // We'll use a simple alert for now, or could implement a toast notification
                alert('Application submitted successfully!');
                // Optional: redirect to dashboard to see it
                window.location.href = 'student-dashboard.html';
            } else {
                showError(result.error || 'Failed to submit application');
            }
        } catch (error) {
            console.error('Error applying:', error);
            showError('Connection error. Please try again.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Application';
        }
    });

    function showError(msg) {
        applicationError.textContent = msg;
        applicationError.classList.remove('hidden');
        // applicationError.style.display = 'block'; // Legacy fallback
    }
});
