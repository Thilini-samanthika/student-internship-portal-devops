document.addEventListener('DOMContentLoaded', async function () {
    const internshipsContainer = document.getElementById('internships-container');
    const desktopNav = document.getElementById('desktop-nav');
    const mobileNav = document.getElementById('mobile-nav');

    // Check login state and update nav
    if (api.isLoggedIn()) {
        const role = api.getRole();
        const dashboardLink = role === 'admin' ? 'admin-dashboard.html' : 'student-dashboard.html';

        // Desktop Nav Update
        desktopNav.innerHTML = `
            <a href="${dashboardLink}" class="text-sm font-medium text-slate-600 hover:text-primary-600 transition-colors">Dashboard</a>
            <a href="#" id="logoutBtn" class="text-sm font-medium px-4 py-2 bg-white border border-slate-200 text-slate-700 rounded-full hover:bg-slate-50 transition-all shadow-sm">Logout</a>
        `;

        // Mobile Nav Update
        mobileNav.innerHTML = `
            <a href="${dashboardLink}" class="block py-3 px-4 text-sm hover:bg-slate-50 text-slate-600">Dashboard</a>
            <a href="#" id="mobileLogoutBtn" class="block py-3 px-4 text-sm hover:bg-slate-50 text-slate-600">Logout</a>
        `;

        const handleLogout = (e) => {
            e.preventDefault();
            api.logout();
        };

        const logoutBtn = document.getElementById('logoutBtn');
        const mobileLogoutBtn = document.getElementById('mobileLogoutBtn');
        
        if(logoutBtn) logoutBtn.addEventListener('click', handleLogout);
        if(mobileLogoutBtn) mobileLogoutBtn.addEventListener('click', handleLogout);
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
        internshipsContainer.innerHTML = '<div class="col-span-full text-center p-4 bg-red-50 text-red-600 rounded-lg">Error loading internships.</div>';
    }

    function renderInternships(internships) {
        if (!internships || internships.length === 0) {
            internshipsContainer.innerHTML = `
                <div class="col-span-full text-center p-12 bg-slate-50 rounded-2xl border border-dashed border-slate-300">
                    <h4 class="text-lg font-medium text-slate-600">No internships available at the moment</h4>
                    <p class="text-slate-500 mt-2">Check back later for new opportunities.</p>
                </div>
            `;
            return;
        }

        // Show only first 3 internships on home page
        const recentInternships = internships.slice(0, 3);

        internshipsContainer.innerHTML = recentInternships.map(internship => `
            <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col h-full group">
                <div class="p-6 flex-grow">
                    <div class="flex justify-between items-start mb-4">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700">
                            ${internship.slots} Slots
                        </span>
                        <span class="text-slate-400 text-sm">${new Date(internship.date_posted).toLocaleDateString()}</span>
                    </div>
                    <h5 class="text-xl font-bold text-slate-900 mb-2 group-hover:text-primary-600 transition-colors">${internship.title}</h5>
                    <h6 class="text-sm font-semibold text-slate-500 mb-4 uppercase tracking-wider">${internship.company}</h6>
                    <p class="text-slate-600 text-sm leading-relaxed mb-4 line-clamp-3">
                        ${internship.description}
                    </p>
                </div>
                <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 mt-auto">
                    <a href="${api.isLoggedIn() ? 'internships.html' : 'login.html'}" class="block w-full text-center text-sm font-semibold text-primary-600 hover:text-primary-700 transition-colors">
                        View Details →
                    </a>
                </div>
            </div>
        `).join('');

        if (internships.length > 3) {
            const btnDiv = document.createElement('div');
            btnDiv.className = "col-span-full text-center mt-8";
            btnDiv.innerHTML = `
                <a href="${api.isLoggedIn() ? 'internships.html' : 'login.html'}" class="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-full text-primary-600 bg-primary-50 hover:bg-primary-100 transition-colors">
                    View All Internships
                </a>
            `;
            internshipsContainer.appendChild(btnDiv);
        }
    }
});
