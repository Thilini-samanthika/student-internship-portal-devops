// Login page functionality
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');

    // If already logged in, redirect to appropriate dashboard
    if (api.isLoggedIn()) {
        const role = api.getRole();
        if (role === 'admin') {
            window.location.href = 'admin-dashboard.html';
        } else {
            window.location.href = 'student-dashboard.html';
        }
        return;
    }

    loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const alertPlaceholder = document.getElementById('alertPlaceholder');

        // Hide any previous error
        alertPlaceholder.innerHTML = '';

        try {
            const result = await api.login(email, password);

            if (result.ok && result.access_token) {
                // Store token and role
                api.setToken(result.access_token);
                api.setRole(result.role);

                // Show success message
                alertPlaceholder.innerHTML = `
                    <div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg relative mb-4" role="alert">
                        <span class="block sm:inline">Login successful! Redirecting...</span>
                    </div>
                `;

                // Redirect based on role
                setTimeout(() => {
                    if (result.role === 'admin') {
                        window.location.href = 'admin-dashboard.html';
                    } else {
                        window.location.href = 'student-dashboard.html';
                    }
                }, 1000);
            } else {
                // Show error message
                alertPlaceholder.innerHTML = `
                    <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg relative mb-4" role="alert">
                        <strong class="font-bold">Error!</strong>
                        <span class="block sm:inline">${result.error || 'Login failed'}.</span>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Login error:', error);
            alertPlaceholder.innerHTML = `
                <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg relative mb-4" role="alert">
                    <span class="block sm:inline">Connection error. Please make sure the server is running.</span>
                </div>
            `;
        }
    });
});
