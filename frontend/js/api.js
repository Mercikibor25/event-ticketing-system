const API_BASE = 'https://event-ticketing-system-production.up.railway.app/api';

// Token helpers
const getToken = () => localStorage.getItem('access_token');
const getUser  = () => JSON.parse(localStorage.getItem('user') || '{}');
const isLoggedIn = () => !!getToken();

// Auth headers
const authHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${getToken()}`
});

// Update navbar based on login state
function updateNav() {
    const loggedIn = isLoggedIn();
    const user = getUser();

    const navAuth = document.getElementById('nav-auth');
    const navUser = document.getElementById('nav-user');

    if (!navAuth || !navUser) return;

    if (loggedIn) {
        navAuth.style.display = 'none';
        navUser.style.display = 'flex';
        const navUsername = document.getElementById('nav-username');
        if (navUsername) navUsername.textContent = user.username || 'Account';
    } else {
        navAuth.style.display = 'flex';
        navUser.style.display = 'none';
    }
}

// Logout
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// Show alert message
function showAlert(containerId, message, type = 'error') {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => container.innerHTML = '', 4000);
}

// API calls
const api = {
    // Auth
    register: (data) => fetch(`${API_BASE}/accounts/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }),

    login: (data) => fetch(`${API_BASE}/accounts/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }),

    getProfile: () => fetch(`${API_BASE}/accounts/profile/`, {
        headers: authHeaders()
    }),

    // Events
    getEvents: () => fetch(`${API_BASE}/events/`),

    getEvent: (id) => fetch(`${API_BASE}/events/${id}/`),

    createEvent: (data) => fetch(`${API_BASE}/events/create/`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify(data)
    }),

    // Tickets
    bookTicket: (eventId) => fetch(`${API_BASE}/tickets/book/`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ event_id: eventId })
    }),

    getMyTickets: () => fetch(`${API_BASE}/tickets/my-tickets/`, {
        headers: authHeaders()
    }),

    // Payments
    initiatePayment: (data) => fetch(`${API_BASE}/payments/initiate/`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify(data)
    }),

    // Notifications
    sendEventUpdate: (data) => fetch(`${API_BASE}/notifications/send-update/`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify(data)
    }),
};