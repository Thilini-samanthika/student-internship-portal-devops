// API Configuration
const API_BASE_URL = '/api';

// API Helper Functions
const api = {
    // Get the JWT token from localStorage
    getToken() {
        return localStorage.getItem('access_token');
    },

    // Set the JWT token in localStorage
    setToken(token) {
        localStorage.setItem('access_token', token);
    },

    // Remove the JWT token from localStorage
    removeToken() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_role');
    },

    // Get user role
    getRole() {
        return localStorage.getItem('user_role');
    },

    // Set user role
    setRole(role) {
        localStorage.setItem('user_role', role);
    },

    // Get headers with authorization
    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (includeAuth && this.getToken()) {
            headers['Authorization'] = `Bearer ${this.getToken()}`;
        }
        return headers;
    },

    // Centralized request handler
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;

        try {
            const response = await fetch(url, options);

            // Handle invalid token errors automatically
            if (response.status === 401 || response.status === 422) {
                console.warn('Session expired or invalid. Logging out...');
                this.removeToken();
                // Only redirect if not already on public pages
                if (!window.location.pathname.endsWith('login.html') &&
                    !window.location.pathname.endsWith('register.html') &&
                    !window.location.pathname.endsWith('index.html')) {
                    window.location.href = 'login.html';
                }
                // Return a clear error
                return { error: 'Session expired', ok: false };
            }

            const data = await response.json().catch(() => ({}));
            return { ...data, ok: response.ok, data: Array.isArray(data) ? data : data.data };
        } catch (error) {
            console.error('API Request Error:', error);
            return { error: 'Connection error', ok: false };
        }
    },

    // Login
    async login(email, password) {
        return this.request('/login', {
            method: 'POST',
            headers: this.getHeaders(false),
            body: JSON.stringify({ email, password })
        });
    },

    // Register student
    async registerStudent(data) {
        return this.request('/register/student', {
            method: 'POST',
            headers: this.getHeaders(false),
            body: JSON.stringify(data)
        });
    },

    // Register admin
    async registerAdmin(data) {
        return this.request('/register/admin', {
            method: 'POST',
            headers: this.getHeaders(false),
            body: JSON.stringify(data)
        });
    },

    // Get current user
    async getCurrentUser() {
        return this.request('/me', {
            method: 'GET',
            headers: this.getHeaders()
        });
    },

    // Get all internships
    async getInternships() {
        return this.request('/internships', {
            method: 'GET',
            headers: this.getHeaders(false) // Public endpoint
        });
    },

    // Apply for internship
    async applyForInternship(formData) {
        return this.request('/apply', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.getToken()}`
                // Content-Type is set automatically by fetch for FormData
            },
            body: formData
        });
    },

    // Get application status (student)
    async getApplicationStatus() {
        return this.request('/status', {
            method: 'GET',
            headers: this.getHeaders()
        });
    },

    // Get all applications (admin)
    async getAllApplications() {
        const result = await this.request('/applications', {
            method: 'GET',
            headers: this.getHeaders()
        });
        // normalize response structure if needed
        return { data: result, ok: result.ok };
    },

    // Approve application (admin)
    async approveApplication(applicationId) {
        return this.request(`/applications/${applicationId}/approve`, {
            method: 'POST',
            headers: this.getHeaders()
        });
    },

    // Reject application (admin)
    async rejectApplication(applicationId) {
        return this.request(`/applications/${applicationId}/reject`, {
            method: 'POST',
            headers: this.getHeaders()
        });
    },

    // Get statistics (admin)
    async getStats() {
        return this.request('/stats', {
            method: 'GET',
            headers: this.getHeaders()
        });
    },

    // Check if user is logged in
    isLoggedIn() {
        return !!this.getToken();
    },

    // Logout
    logout() {
        this.removeToken();
        window.location.href = 'login.html';
    }
};

// Redirect if not logged in (for protected pages)
function requireAuth() {
    if (!api.isLoggedIn()) {
        window.location.href = 'login.html';
    }
}

// Redirect if not admin
function requireAdmin() {
    if (!api.isLoggedIn() || api.getRole() !== 'admin') {
        window.location.href = 'login.html';
    }
}

// Redirect if not student
function requireStudent() {
    if (!api.isLoggedIn() || api.getRole() !== 'student') {
        window.location.href = 'login.html';
    }
}
