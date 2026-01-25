document.addEventListener('DOMContentLoaded', async function () {
    requireStudent();

    const studentNameElement = document.getElementById('student-name');
    const applicationsContainer = document.getElementById('applications-container');
    const logoutBtn = document.getElementById('logoutBtn');

    // Logout functionality
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function (e) {
            e.preventDefault();
            api.logout();
        });
    }

    try {
        // Load user info
        const user = await api.getCurrentUser();
        studentNameElement.textContent = user.name || 'Student';

        // Load applications
        const result = await api.getApplicationStatus();

        if (result.ok) {
            renderApplications(result.data);
        } else {
            applicationsContainer.innerHTML = '<div class="p-6 text-center text-red-600 bg-red-50 rounded-lg">Failed to load applications.</div>';
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        applicationsContainer.innerHTML = '<div class="p-6 text-center text-red-600 bg-red-50 rounded-lg">Error loading dashboard. Please try again later.</div>';
    }

    function renderApplications(applications) {
        if (!applications || applications.length === 0) {
            applicationsContainer.innerHTML = `
                <div class="p-12 text-center">
                    <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 mb-4">
                        <span class="text-3xl">📝</span>
                    </div>
                    <h4 class="text-lg font-medium text-slate-900 mb-2">No applications yet</h4>
                    <p class="text-slate-500 mb-6">Browse internships and apply to get started!</p>
                    <a href="internships.html" class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-full text-white bg-primary-600 hover:bg-primary-700 transition-colors shadow-sm">
                        Browse Internships
                    </a>
                </div>
            `;
            return;
        }

        // Using grid layout container is handled in HTML/CSS usually, but here we replace the inner HTML structure
        // The container #applications-container has 'divide-y divide-gray-100' class in HTML

        let html = '';

        applications.forEach(app => {
            let statusStyles = 'bg-slate-100 text-slate-800'; // Default/Pending
            if (app.status === 'Approved') statusStyles = 'bg-green-100 text-green-800';
            if (app.status === 'Rejected') statusStyles = 'bg-red-100 text-red-800';
            if (app.status === 'Pending') statusStyles = 'bg-yellow-100 text-yellow-800';

            html += `
                <div class="p-6 hover:bg-slate-50/50 transition-colors">
                    <div class="md:flex md:justify-between md:items-start">
                        <div class="flex-grow">
                            <div class="flex items-center gap-3 mb-2">
                                <h3 class="text-lg font-bold text-slate-900">${app.title || app.internship_title || 'Internship'}</h3>
                                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusStyles}">
                                    ${app.status}
                                </span>
                            </div>
                            <p class="text-slate-500 font-medium mb-4">${app.company || app.company_name || 'Company'}</p>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                                <div>
                                    <span class="block text-slate-400 text-xs uppercase tracking-wide font-semibold mb-1">Applied On</span>
                                    <span class="text-slate-700 font-mono">${new Date(app.applied_at).toLocaleDateString()}</span>
                                </div>
                                ${app.cv_file ? `
                                <div>
                                    <span class="block text-slate-400 text-xs uppercase tracking-wide font-semibold mb-1">Documents</span>
                                    <span class="text-primary-600 flex items-center gap-1">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                                        CV Submitted
                                    </span>
                                </div>
                                ` : ''}
                            </div>
                            
                            ${app.cover_letter ? `
                                <div class="mt-4 bg-slate-50 p-4 rounded-lg border border-slate-100">
                                    <span class="block text-slate-400 text-xs uppercase tracking-wide font-semibold mb-2">Cover Letter</span>
                                    <p class="text-slate-600 text-sm italic">"${app.cover_letter}"</p>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
            `;
        });

        applicationsContainer.innerHTML = html;
    }
});
