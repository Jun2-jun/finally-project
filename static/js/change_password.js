document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById("password-form");

    form.addEventListener("submit", async function(e) {
        e.preventDefault(); // 기본 제출 막기

        const currentPassword = document.getElementById("current_password").value;
        const newPassword = document.getElementById("new_password").value;
        const confirmPassword = document.getElementById("confirm_password").value;

        if (newPassword !== confirmPassword) {
            alert("새 비밀번호가 일치하지 않습니다.");
            return;
        }

        try {
            const response = await fetch("http://192.168.219.200:5002/api/users/change-password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",  // 세션 쿠키 전송
                body: JSON.stringify({
                    current_password: currentPassword,
                    new_password: newPassword
                })
            });

            const result = await response.json();

            if (result.status === "success") {
                alert("비밀번호가 성공적으로 변경되었습니다.");
                form.reset();
            } else {
                alert("변경 실패: " + result.message);
            }

        } catch (err) {
            console.error("비밀번호 변경 중 오류 발생:", err);
            alert("서버 오류가 발생했습니다.");
        }
    });
});
