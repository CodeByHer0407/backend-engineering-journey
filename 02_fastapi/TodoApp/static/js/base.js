    // Add Todo JS
    const todoForm = document.getElementById('todoForm');
    if (todoForm) {
        todoForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            const payload = {
                title: data.title,
                description: data.description,
                priority: parseInt(data.priority),
                complete: false
            };

            try {
                const response = await fetch('/todos/todo', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${getCookie('access_token')}`
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {

    showToast(
        "Task Created",
        "Your new task has been added."
    );

    form.reset();

    setTimeout(() => {
        window.location.href = "/todos/todo-page";
    }, 800);

}   else {
                    // Handle error
                    const errorData = await response.json();

    showToast(
    "Failed to Create Task",
    errorData.detail,
    "error"
);
                }
            } catch (error) {
                console.error('Error:', error);
                showToast(
    "Unexpected Error",
    "Please try again.",
    "error"
);
            }
        });
    }

    // Edit Todo JS
    const editTodoForm = document.getElementById('editTodoForm');
    if (editTodoForm) {
        editTodoForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        var url = window.location.pathname;
        const todoId = url.substring(url.lastIndexOf('/') + 1);

        const payload = {
            title: data.title,
            description: data.description,
            priority: parseInt(data.priority),
            complete: data.complete === "on"
        };

        try {
            const token = getCookie('access_token');
            console.log(token)
            if (!token) {
                throw new Error('Authentication token not found');
            }

            console.log(`${todoId}`)

            const response = await fetch(`/todos/todo/${todoId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                showToast(
    "Task Updated",
    "Changes saved successfully."
);

setTimeout(() => {
    window.location.href = "/todos/todo-page";
}, 800);
            } else {
                // Handle error
                const errorData = await response.json();
                showToast(
    "Update Failed",
    errorData.detail,
    "error"
);
            }
        } catch (error) {
            console.error('Error:', error);
            showToast(
    "Unexpected Error",
    "Please try again.",
    "error"
);
        }
    });

        document.getElementById('deleteButton').addEventListener('click', async function () {
            var url = window.location.pathname;
            const todoId = url.substring(url.lastIndexOf('/') + 1);

            try {
                const token = getCookie('access_token');
                if (!token) {
                    throw new Error('Authentication token not found');
                }

                const response = await fetch(`/todos/todo/${todoId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    // Handle success
                    showToast(
    "Task Deleted",
    "The task has been removed."
);

setTimeout(() => {
    window.location.href = "/todos/todo-page";
}, 800); // Redirect to the todo page
                } else {
                    // Handle error
                    const errorData = await response.json();
                    showToast(
    "Delete Failed",
    errorData.detail,
    "error"
);
                }
            } catch (error) {
                console.error('Error:', error);
                showToast(
    "Unexpected Error",
    "Please try again.",
    "error"
);
            }
        });

        
    }

    // Login JS
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);

            const payload = new URLSearchParams();
            for (const [key, value] of formData.entries()) {
                payload.append(key, value);
            }

            try {
                const response = await fetch('/auth/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: payload.toString()
                });

                if (response.ok) {
                    // Handle success (e.g., redirect to dashboard)
                    const data = await response.json();
            
                    // Save token to cookie
                    document.cookie = `access_token=${data.access_token}; path=/`;
                    window.location.href = '/todos/todo-page'; // Change this to your desired redirect page
                } else {
                    // Handle error
                    const errorData = await response.json();
                    showToast("Login Failed",errorData.detail,"error");
                }
            } catch (error) {
                console.error('Error:', error);
                showToast("Unexpected Error","Please try again.","error");
            }
        });
    }

    // Register JS
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            if (data.password !== data.password2) {
                showToast("Passwords Don't Match","Please enter the same password twice.","error");
                return;
            }
            console.log("Form data:", data);
            const payload = {
                email: data.email,
                username: data.username,
                first_name: data.first_name,
                last_name: data.last_name,
                role: "user",
                phone_number: data.phone_number,
                password: data.password,
            };
            console.log("Payload:", payload);

            try {
                const response = await fetch('/auth', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {

                    showToast(
                        "Account Created",
                        "Welcome to TodoFlow!"
                    );

                    setTimeout(() => {
                        window.location.href = '/auth/login-page';
                    }, 1200);

} else {
                    // Handle error
                    const errorData = await response.json();

                    showToast(
    "Registration Failed",
    errorData.detail || "Unable to create account.",
    "error"
);
                }
            } catch (error) {
                console.error('Error:', error);
                showToast("Unexpected Error","Please try again.","error");
            }
        });
    }





    // Helper function to get a cookie by name
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    function logout() {
        // Get all cookies
        const cookies = document.cookie.split(";");
    
        // Iterate through all cookies and delete each one
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            // Set the cookie's expiry date to a past date to delete it
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
        }
    
        // Redirect to the login page
        window.location.href = '/auth/login-page';
    };

function showToast(title, message, type="success"){

    const container = document.getElementById("toast-container");

    const toast = document.createElement("div");

    toast.className=`custom-toast ${type}`;

    toast.innerHTML=`

        <div class="toast-icon">

            ${type==="success" ? "✅" : "❌"}

        </div>

        <div>

            <div class="toast-title">${title}</div>

            <div class="toast-message">${message}</div>

        </div>

    `;

    container.appendChild(toast);

    setTimeout(()=>{

        toast.classList.add("toast-hide");

        setTimeout(()=>{

            toast.remove();

        },350);

    },3000);

}

