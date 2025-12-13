
document.getElementById("contactForm").addEventListener("submit", function (e) {
    e.preventDefault();
    console.log("📨 Contact form submitted");

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log("🔐 CSRF Token:", csrftoken);

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        company: document.getElementById("company").value,
        contact_number: document.getElementById("contact_number").value,
        service_type: document.getElementById("service_type").value,
        message: document.getElementById("message").value
    };

    console.log("📦 Form Data:", data);

    fetch("/email/send-otp/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            console.log("📡 Raw Response:", response);
            return response.json();
        })
        .then(result => {
            console.log("✅ Server Response JSON:", result);
            alert(result.message);

            if (result.status === "success") {
                console.log("🔄 Form reset");
                document.getElementById("contactForm").reset();
            }
        })
        .catch(error => {
            console.error("❌ Fetch Error:", error);
        });
});

