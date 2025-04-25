async function submitWithdraw() {
    const password = document.getElementById("withdrawPassword").value;
    const errorMsg = document.getElementById("withdrawError");
    const modal = document.getElementById("withdrawModal");
    const successBox = document.getElementById("withdrawSuccess");

    try {
        const response = await fetch("http://192.168.219.189:5002/api/users/withdraw", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({ password: password })
        });

        const result = await response.json();

        if (result.success) {
            modal.style.display = "none";
            successBox.style.display = "block";
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
