document.addEventListener('DOMContentLoaded', async function () {
    requireAdmin();

    const logoutBtn = document.getElementById('logoutBtn');
    const internshipsContainer = document.getElementById('internships-container');
    const createForm = document.getElementById('createInternshipForm');

    // Modal Elements
    const modal = document.getElementById('createInternshipModal');
    const modalBackdrop = document.getElementById('modalBackdrop');
    const modalPanel = document.getElementById('modalPanel');
    const openCreateModalBtn = document.getElementById('openCreateModal');
    const cancelModalBtn = document.getElementById('cancelModal');
    const submitBtn = document.getElementById('submitInternship');
    const createError = document.getElementById('create-error');

    // Logout functionality
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function (e) {
            e.preventDefault();
            api.logout();
        });
    }

    // Modal Functions
    function showModal() {
        modal.classList.remove('hidden');
        void modal.offsetWidth; // trigger reflow
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
        }, 300);
    }

    if (openCreateModalBtn) openCreateModalBtn.addEventListener('click', () => {
        createError.classList.add('hidden');
        createForm.reset();
        showModal();
    });

    if (cancelModalBtn) cancelModalBtn.addEventListener('click', hideModal);

    // Load internships
    loadInternships();

    async function loadInternships() {
        try {
            const result = await api.getInternships();

            if (result.ok) {
                renderInternships(result.data);
            } else {
                internshipsContainer.innerHTML = '<div class="col-span-full py-12 text-center text-red-600 bg-red-50 rounded-xl">Failed to load internships.</div>';
            }
        } catch (error) {
            console.error('Error loading internships:', error);
            internshipsContainer.innerHTML = '<div class="col-span-full py-12 text-center text-red-600 bg-red-50 rounded-xl">Error loading internships.</div>';
        }
    }

    function renderInternships(internships) {
        if (!internships || internships.length === 0) {
            internshipsContainer.innerHTML = `
                <div class="col-span-full text-center py-20 bg-white rounded-2xl border border-dashed border-slate-300">
                    <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 mb-4">
                        <span class="text-3xl">📁</span>
                    </div>
                    <h4 class="text-xl font-bold text-slate-800">No internships created yet</h4>
                    <p class="text-slate-500 mt-2">Click the "Create New Internship" button to add one.</p>
                </div>
            `;
            return;
        }

        internshipsContainer.innerHTML = internships.map(internship => `
            <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-lg transition-all duration-300 flex flex-col h-full group">
                <div class="p-6 flex-grow">
                    <div class="flex justify-between items-start mb-4">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700">
                            ${internship.slots} Slots
                        </span>
                        <span class="text-slate-400 text-xs font-medium">${new Date(internship.date_posted).toLocaleDateString()}</span>
                    </div>
                    <h5 class="text-lg font-bold text-slate-900 mb-1 group-hover:text-primary-600 transition-colors">${internship.title}</h5>
                    <h6 class="text-sm font-semibold text-slate-500 mb-4 uppercase tracking-wider">${internship.company}</h6>
                    <div class="flex items-center gap-2 mb-4">
                         <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-50 text-indigo-700">
                            ${internship.duration}
                        </span>
                    </div>
                    <p class="text-slate-600 text-sm leading-relaxed line-clamp-3">${internship.description}</p>
                </div>
                <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 mt-auto flex justify-end">
                    <!-- Future: Edit/Delete buttons -->
                    <span class="text-xs text-slate-400 italic">Managed by Admin</span>
                </div>
            </div>
        `).join('');
    }

    // Handle form submission
    submitBtn.addEventListener('click', async function () {
        if (!createForm.checkValidity()) {
            createForm.reportValidity();
            return;
        }

        const internshipData = {
            title: document.getElementById('title').value,
            company: document.getElementById('company').value,
            description: document.getElementById('description').value,
            duration: document.getElementById('duration').value,
            slots: parseInt(document.getElementById('slots').value)
        };

        submitBtn.disabled = true;
        submitBtn.textContent = 'Creating...';
        createError.classList.add('hidden');

        try {
            // Using API base URL for fetching if api helper doesn't have create helper
            // Note: API_BASE_URL should be available if api.js defines it globally or we can use relative
            const response = await fetch('/api/internships', {
                method: 'POST',
                headers: api.getHeaders(),
                body: JSON.stringify(internshipData)
            });

            const result = await response.json();

            if (response.ok) {
                hideModal();
                createForm.reset();
                loadInternships(); // Reload list
                alert('Internship created successfully!');
            } else {
                createError.textContent = result.error || 'Failed to create internship';
                createError.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error creating internship:', error);
            createError.textContent = 'Connection error. Please try again.';
            createError.classList.remove('hidden');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Internship';
        }
    });
});
