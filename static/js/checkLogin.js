// checkLogin.js
document.addEventListener('DOMContentLoaded', () => {
    fetch("http://192.168.219.189:5002/api/users/check-login", {
      method: "GET",
      credentials: "include"
    })
    .then(res => {
      if (res.status === 401) {
        alert("로그인이 필요한 서비스입니다.");
        window.location.href = "/login";
      }
    })
    .catch(err => {
      console.error("로그인 체크 중 오류 발생:", err);
    });
  });
  
