// Registration page functionality
document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');
    const alertPlaceholder = document.getElementById('alertPlaceholder');
    const btnStudent = document.getElementById('btnStudent');
    const btnAdmin = document.getElementById('btnAdmin');
    const roleInput = document.getElementById('role');
    const studentFields = document.getElementById('studentFields');

    // If already logged in, redirect to dashboard
    if (api.isLoggedIn()) {
        const role = api.getRole();
        if (role === 'admin') {
            window.location.href = 'admin-dashboard.html';
        } else {
            window.location.href = 'student-dashboard.html';
        }
        return;
    }

    // Role selection logic
    btnStudent.addEventListener('click', () => {
        roleInput.value = 'student';
        btnStudent.className = "px-6 py-2 text-sm font-medium rounded-full transition-all focus:outline-none bg-primary-600 text-white shadow-md";
        btnAdmin.className = "px-6 py-2 text-sm font-medium rounded-full transition-all focus:outline-none bg-slate-100 text-slate-600 hover:bg-slate-200";
        studentFields.classList.remove('hidden');
    });

    btnAdmin.addEventListener('click', () => {
        roleInput.value = 'admin';
        btnAdmin.className = "px-6 py-2 text-sm font-medium rounded-full transition-all focus:outline-none bg-primary-600 text-white shadow-md";
        btnStudent.className = "px-6 py-2 text-sm font-medium rounded-full transition-all focus:outline-none bg-slate-100 text-slate-600 hover:bg-slate-200";
        studentFields.classList.add('hidden');
    });

    registerForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const role = roleInput.value;
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Hide any previous messages
        alertPlaceholder.innerHTML = '';

        let data = { name, email, password };
        let registerPromise;

        if (role === 'student') {
            const course = document.getElementById('course').value;
            const year = document.getElementById('year').value;
            data.course = course;
            data.year = parseInt(year) || null;
            registerPromise = api.registerStudent(data);
        } else {
            registerPromise = api.registerAdmin(data);
        }

        try {
            const result = await registerPromise;

            if (result.ok) {
                // Show success message
                alertPlaceholder.innerHTML = `
                    <div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg relative mb-4" role="alert">
                        <span class="block sm:inline">Registration successful! Redirecting to login...</span>
                    </div>
                `;

                // Redirect to login after 1.5 seconds
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 1500);
            } else {
                // Show error message
                alertPlaceholder.innerHTML = `
                    <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg relative mb-4" role="alert">
                        <strong class="font-bold">Error!</strong>
                        <span class="block sm:inline">${result.error || 'Registration failed. Please try again.'}</span>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Registration error:', error);
            alertPlaceholder.innerHTML = `
                <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg relative mb-4" role="alert">
                    <span class="block sm:inline">Connection error. Please make sure the server is running.</span>
                </div>
            `;
        }
    });
});
