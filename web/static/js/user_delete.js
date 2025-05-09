async function submitWithdraw() {
    const password = document.getElementById("withdrawPassword").value;
    const errorMsg = document.getElementById("withdrawError");
    const modal = document.getElementById("withdrawModal");
    const serverIP = document.body.dataset.serverIp;
    try {
        const response = await fetch(`http://${serverIP}:5002/api/users/withdraw`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({ password: password })
        });

        const result = await response.json();

        if (result.success) {
            // ✅ alert 띄우고 → /index 페이지 이동
            alert("탈퇴가 완료되었습니다.");
            window.location.href = "/";
        } else {
            errorMsg.style.display = "block";
            errorMsg.innerText = result.message || "비밀번호가 일치하지 않습니다.";
        }
    } catch (err) {
        console.error("회원 탈퇴 중 오류 발생:", err);
        errorMsg.style.display = "block";
        errorMsg.innerText = "서버 오류가 발생했습니다.";
    }
}
