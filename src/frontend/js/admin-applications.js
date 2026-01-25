document.addEventListener('DOMContentLoaded', async function () {
    requireAdmin();

    const logoutBtn = document.getElementById('logoutBtn');
    const applicationsContainer = document.getElementById('applications-container');
    const statusFilter = document.getElementById('statusFilter');

    let allApplications = [];

    // Logout functionality
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function (e) {
            e.preventDefault();
            api.logout();
        });
    }

    // Load applications
    try {
        const result = await api.getAllApplications();

        if (result.ok) {
            allApplications = result.data;
            renderApplications(allApplications);
        } else {
            applicationsContainer.innerHTML = '<div class="p-6 text-center text-red-600 bg-red-50 rounded-xl">Failed to load applications.</div>';
        }
    } catch (error) {
        console.error('Error loading applications:', error);
        applicationsContainer.innerHTML = '<div class="p-6 text-center text-red-600 bg-red-50 rounded-xl">Error loading applications.</div>';
    }

    // Filter functionality
    statusFilter.addEventListener('change', function () {
        const status = this.value;
        if (status) {
            const filtered = allApplications.filter(app => app.status === status);
            renderApplications(filtered);
        } else {
            renderApplications(allApplications);
        }
    });

    function renderApplications(applications) {
        if (!applications || applications.length === 0) {
            applicationsContainer.innerHTML = `
                <div class="text-center py-16 bg-white rounded-2xl border border-dashed border-slate-300">
                    <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 mb-4">
                        <span class="text-3xl">📭</span>
                    </div>
                    <h4 class="text-xl font-bold text-slate-800">No applications found</h4>
                    <p class="text-slate-500 mt-2">Try changing your filter or check back later.</p>
                </div>
            `;
            return;
        }

        applicationsContainer.innerHTML = applications.map(app => {
            let statusBadgeStyles = 'bg-slate-100 text-slate-800';
            if (app.status === 'Approved') statusBadgeStyles = 'bg-green-100 text-green-800';
            if (app.status === 'Rejected') statusBadgeStyles = 'bg-red-100 text-red-800';
            if (app.status === 'Pending') statusBadgeStyles = 'bg-yellow-100 text-yellow-800';

            const showActions = app.status === 'Pending';

            return `
                <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-md transition-shadow application-card" data-id="${app.id}">
                    <div class="p-6">
                        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
                            <div class="flex-grow">
                                <div class="flex items-center gap-3 mb-2">
                                    <h3 class="text-lg font-bold text-slate-900">${app.student_name}</h3>
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusBadgeStyles}">
                                        ${app.status}
                                    </span>
                                </div>
                                <h4 class="text-primary-600 font-semibold mb-2">${app.title}</h4>
                                <p class="text-slate-500 text-sm mb-4 font-medium uppercase tracking-wider">${app.company}</p>
                                
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-2 text-sm text-slate-600 mb-6">
                                    <div class="flex items-center gap-2">
                                        <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                                        ${app.student_email}
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                                        ${app.course} (Year ${app.year})
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                                        Applied: ${new Date(app.applied_at).toLocaleDateString()}
                                    </div>
                                    ${app.cv_file ? `
                                    <div class="flex items-center gap-2">
                                        <svg class="w-4 h-4 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.414a4 4 0 00-5.656-5.656l-6.415 6.414a6 6 0 108.486 8.486L20.5 13"></path></svg>
                                        <span class="text-primary-600 font-medium cursor-pointer hover:underline">Download CV</span>
                                    </div>
                                    ` : ''}
                                </div>
                                
                                <div class="bg-slate-50 p-4 rounded-xl border border-slate-100">
                                    <span class="block text-slate-400 text-xs uppercase tracking-wide font-semibold mb-2">Cover Letter</span>
                                    <p class="text-slate-600 text-sm italic">"${app.cover_letter || 'No cover letter submitted.'}"</p>
                                </div>
                            </div>
                            
                            <div class="flex-shrink-0 lg:w-48 xl:w-64 lg:pl-6 lg:border-l lg:border-slate-100 flex flex-col gap-3">
                                ${showActions ? `
                                    <button class="w-full inline-flex justify-center items-center px-4 py-2.5 border border-transparent text-sm font-semibold rounded-lg text-white bg-green-600 hover:bg-green-700 transition-all shadow-sm action-btn" onclick="updateStatus(${app.id}, 'approve')">
                                        Approve
                                    </button>
                                    <button class="w-full inline-flex justify-center items-center px-4 py-2.5 border border-slate-200 text-sm font-semibold rounded-lg text-slate-700 bg-white hover:bg-slate-50 transition-all shadow-sm action-btn" onclick="updateStatus(${app.id}, 'reject')">
                                        Reject
                                    </button>
                                ` : `
                                    <div class="text-center p-3 rounded-xl border border-slate-100 bg-slate-50">
                                        <span class="text-sm font-bold text-slate-400 uppercase tracking-widest">Processed</span>
                                        <p class="text-slate-600 font-medium text-sm mt-1">${app.status}</p>
                                    </div>
                                `}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    // Expose function to window for onclick handlers
    window.updateStatus = async function (id, action) {
        if (!confirm(`Are you sure you want to ${action} this application?`)) return;

        const card = document.querySelector(`.application-card[data-id="${id}"]`);
        const btns = card.querySelectorAll('.action-btn');
        btns.forEach(btn => btn.disabled = true);

        try {
            let result;
            if (action === 'approve') {
                result = await api.approveApplication(id);
            } else {
                result = await api.rejectApplication(id);
            }

            if (result.ok) {
                // Update local state and re-render
                const appIndex = allApplications.findIndex(a => a.id === id);
                if (appIndex !== -1) {
                    allApplications[appIndex].status = action === 'approve' ? 'Approved' : 'Rejected';

                    const currentFilter = statusFilter.value;
                    if (currentFilter) {
                        const filtered = allApplications.filter(a => a.status === currentFilter);
                        renderApplications(filtered);
                    } else {
                        renderApplications(allApplications);
                    }
                }
            } else {
                alert('Failed to update status: ' + (result.error || 'Unknown error'));
                btns.forEach(btn => btn.disabled = false);
            }
        } catch (error) {
            console.error('Error updating status:', error);
            alert('Connection error');
            btns.forEach(btn => btn.disabled = false);
        }
    };
});
