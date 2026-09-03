document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");

    forms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            const inputs = form.querySelectorAll("input[required], select[required]");
            let valid = true;

            inputs.forEach((input) => {
                if (!input.value.trim()) {
                    valid = false;
                    input.style.borderColor = "red";
                } else {
                    input.style.borderColor = "#cccccc";
                }
            });

            if (!valid) {
                event.preventDefault();
                alert("Please fill in all required fields before submitting.");
            }
        });
    });
});