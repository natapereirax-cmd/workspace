const form = document.getElementById('sign_up_form');

const emailInput = document.getElementById('email');
const errorSpan = document.getElementById('email_error');

emailInput.addEventListener('blur', async function (){
        const email = this.value;
        if (!email) return;

        const response_email = await fetch('/check_email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })  
        });

        const data_email = await response_email.json();

        if (data_email.exists) {
        errorSpan.textContent = "Email already registered!";
        } else {
        errorSpan.textContent = "";
        }

    });

form.addEventListener('submit', async function(e) {
    e.preventDefault();

    const firstname = document.getElementById('firstname').value;
    const lastname = document.getElementById('lastname').value;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;


    const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{4,}$/;

    if (
        firstname ==="" ||
        lastname === "" ||
        email === "" ||
        password === "" ||
        username === ""
    ) {
        alert("Fill all fields!");
        return;
    }

    if (!regex.test(password)) {
        alert("The password needs to have:\n- 1 capital letter\n- 1 number\n- 1 symbol\n- at least 4 characters")
        return;
    }

    const data = {
        firstname,
        lastname,
        username,
        email,
        password
    };

    const response = await fetch("/sign_up", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        alert("Registration Complete!");
        form.reset();
        window.location.href = "/sign_up";
    }
});