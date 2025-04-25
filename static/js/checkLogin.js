// checkLogin.js
document.addEventListener('DOMContentLoaded', () => {
    fetch("http://192.168.219.189:5002/api/users/check-login", {
      method: "GET",
      credentials: "include"
    })
    .then(res => {
      if (res.status === 401) {
        alert("로그인해야 됩니다.");
        window.location.href = "/index";
      }
    })
    .catch(err => {
      console.error("로그인 체크 중 오류 발생:", err);
    });
  });
  