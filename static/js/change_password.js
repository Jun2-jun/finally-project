document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById("password-form");

    form.addEventListener("submit", async function (e) {
      e.preventDefault();
  
      const currentPassword = document.getElementById("current_password").value;
      const newPassword = document.getElementById("new_password").value;
      const confirmPassword = document.getElementById("confirm_password").value;
  
      if (newPassword !== confirmPassword) {
        alert("새 비밀번호가 일치하지 않습니다.");
        return;
      }
  
      try {
        const response = await fetch("http://192.168.219.193:5002/api/users/change-password", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          credentials: "include", // 세션 쿠키 포함
          body: JSON.stringify({
            current_password: currentPassword,
            new_password: newPassword
          })
        });
  
        const result = await response.json();
  
        if (result.status === "success") {
          alert("비밀번호가 성공적으로 변경되었습니다.");
          form.reset();
          window.location.href = "http://192.168.219.193:5000/dashboard";  // 이동
        } else {
          alert("변경 실패: " + result.message);
        }
      } catch (err) {
        console.error("비밀번호 변경 중 오류 발생:", err);
        alert("서버 오류가 발생했습니다.");
      }
    });
  
    // 인증번호 발송
    document.getElementById('sendCodeBtn').addEventListener('click', () => {
      const email = document.getElementById('email').value;
      if (!email) return alert("이메일을 입력하세요.");
  
      fetch('http://192.168.219.193:5002/api/users/send_verification_code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        credentials: 'include',
        body: new URLSearchParams({ email })
      })
        .then(res => res.json())
        .then(data => {
          alert(data.message);
        })
        .catch(err => {
          console.error('인증번호 전송 오류:', err);
          alert("인증번호 전송에 실패했습니다.");
        });
    });
  
    // 인증번호 확인
    document.getElementById('verifyCodeBtn').addEventListener('click', () => {
      const code = document.getElementById('verification_code').value;
  
      fetch('http://192.168.219.193:5002/api/users/verify_code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        credentials: 'include',
        body: new URLSearchParams({ code })
      })
        .then(res => res.json())
        .then(data => {
          const msg = document.getElementById('emailVerificationMessage');
          if (data.success) {
            msg.textContent = data.message;
            msg.style.color = 'green';
          } else {
            msg.textContent = data.message;
            msg.style.color = 'red';
          }
        })
        .catch(err => {
          console.error('인증번호 확인 오류:', err);
          alert("인증번호 확인에 실패했습니다.");
        });
    });
  });
  
