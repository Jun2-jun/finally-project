// 비밀번호 일치 실시간 확인
document.addEventListener("DOMContentLoaded", () => {
    const pw = document.getElementById("password");
    const confirmPw = document.getElementById("confirm_password");
    const msg = document.getElementById("pwCheckMsg");
  
    function checkPasswordMatch() {
      if (pw.value && confirmPw.value) {
        if (pw.value === confirmPw.value) {
          msg.textContent = "비밀번호가 일치합니다.";
          msg.className = "check-message match";
        } else {
          msg.textContent = "비밀번호가 일치하지 않습니다.";
          msg.className = "check-message no-match";
        }
      } else {
        msg.textContent = "";
      }
    }
  
    pw.addEventListener("input", checkPasswordMatch);
    confirmPw.addEventListener("input", checkPasswordMatch);
  
    // 회원가입 폼 제출 처리
    const registerForm = document.getElementById("registerForm");
    registerForm.addEventListener("submit", function (event) {
      event.preventDefault();
  
      const password = pw.value;
      const confirmPassword = confirmPw.value;
  
      if (password !== confirmPassword) {
        document.getElementById("errorMessage").textContent = "비밀번호가 일치하지 않습니다.";
        document.getElementById("errorMessage").style.display = "block";
        return;
      }
  
      const formData = {
        username: document.getElementById("username").value,
        password: password,
        email: document.getElementById("email").value,
        birthdate: document.getElementById("birthdate").value,
        phone: document.getElementById("phone").value,
        address: document.getElementById("address").value,
        address_detail: document.getElementById("address_detail").value
      };
  
      // ✅ API 주소 자동 설정 (현재 호스트에 맞춰서)
      const apiHost = window.location.hostname;
      const apiBaseUrl = 'http://192.168.219.200:5002';
  
      fetch('http://192.168.219.200:5002/api/users/register', {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData),
        mode: "cors",
        credentials: "include"
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          document.getElementById("successMessage").textContent = "회원가입이 완료되었습니다! 로그인 페이지로 이동합니다.";
          document.getElementById("successMessage").style.display = "block";
          document.getElementById("errorMessage").style.display = "none";
          registerForm.reset();
          setTimeout(() => {
            window.location.href = "/login";
          }, 1500);
        } else {
          document.getElementById("errorMessage").textContent = data.message || "회원가입에 실패했습니다.";
          document.getElementById("errorMessage").style.display = "block";
          document.getElementById("successMessage").style.display = "none";
        }
      })
      .catch(error => {
        document.getElementById("errorMessage").textContent = "서버 오류가 발생했습니다.";
        document.getElementById("errorMessage").style.display = "block";
        document.getElementById("successMessage").style.display = "none";
        console.error("에러 발생:", error);
      });
    });
  });
  
  // 주소 검색 (카카오 우편번호 서비스)
  function execDaumPostcode() {
    new daum.Postcode({
      oncomplete: function(data) {
        document.getElementById("address").value = data.address;
      }
    }).open();
  }
  