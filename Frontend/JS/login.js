document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const data = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
    };

    try {
        // Send a POST request to the backend API for login
        const response = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            credentials: 'include', // Include cookies for session management
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message); // Optional success message
            window.location.href = './dashboard.html'; // Redirect to dashboard
        } else {
            document.getElementById("login-message").textContent = result.message || "Login failed!";
        }
    } catch (error) {
        console.error("Error during login:", error);
        document.getElementById("login-message").textContent = "An unexpected error occurred. Please try again.";
    }
});
