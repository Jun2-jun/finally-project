function togglePassword(inputId, icon) {
    const input = document.getElementById(inputId);
    const isVisible = input.type === "text";
    input.type = isVisible ? "password" : "text";
    icon.classList.toggle("fa-eye");
    icon.classList.toggle("fa-eye-slash");
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("password-form");
    form.addEventListener("submit", function(e) {
        const newPassword = document.getElementById("new_password").value;
        const confirmPassword = document.getElementById("confirm_password").value;
        if (newPassword !== confirmPassword) {
            e.preventDefault();
            alert("새 비밀번호가 일치하지 않습니다.");
        }
    });
});
