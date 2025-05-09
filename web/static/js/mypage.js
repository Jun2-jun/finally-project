document.addEventListener('DOMContentLoaded', () => {
  // DOM 요소 참조
  const reservationTbody = document.querySelector('#reservation-check tbody');
  const userInfoForm = document.getElementById('mypage-form');
  const healthForm = document.querySelector('#health-form');
  const editBtn = document.getElementById('edit-btn');
  const editables = document.querySelectorAll('.editable');
  const serverIP = document.body.dataset.serverIp;
  let isEmailVerified = false;

  // 로딩 상태 표시
  if (reservationTbody) {
    reservationTbody.innerHTML = '<tr><td colspan="4" class="text-center">불러오는 중...</td></tr>';
  }
  
  // 1. 사용자 정보 가져오기
  fetch(`http://${serverIP}:5002/api/current-user`, {
    method: 'GET',
    credentials: 'include'
  })
  .then(res => res.json())
  .then(userData => {
    if (userData.status === 'success' && userData.user) {
      const user = userData.user;
      const userId = user.id;

      if (!userId) throw new Error('user.id 없음');

      // 내정보 채우기
      if (userInfoForm) {
        userInfoForm.userid.value = user.username || '';
        userInfoForm.email.value = user.email || '';
        userInfoForm.birthdate.value = user.birthdate || '';
        userInfoForm.phone.value = user.phone || '';
        userInfoForm.address.value = user.address || '';
        userInfoForm.detail_address.value = user.address_detail || '';
      }

      // 2. 예약정보 가져오기
      return fetch(`http://${serverIP}:5002/api/reservations/user/${userId}`, {
        method: 'GET',
        credentials: 'include'
      });
    } else {
      throw new Error('userData 실패');
    }
  })
  .then(res => res.json())
  .then(reservationData => {
    if (!reservationTbody) return; // 예약 섹션이 없으면 처리 중단
    
    reservationTbody.innerHTML = '';

    if (reservationData.status === 'success' && reservationData.data.length > 0) {
      let hasActiveReservations = false;
      
      reservationData.data.forEach((r, i) => {
        const reservationTimeStr = r.reservation_time || `${r.date} ${r.time}`;
        const reservationTime = new Date(reservationTimeStr);
        const now = new Date();

        if (reservationTime < now) {
          // 과거 예약 자동 삭제
          fetch(`http://${serverIP}:5002/api/mypage/reservation/${r.id}`, {
            method: 'DELETE',
            credentials: 'include'
          })
          .then(res => {
            if (!res.ok) console.warn(`예약 ID ${r.id} 삭제 실패`);
          })
          .catch(err => {
            console.error(`예약 ID ${r.id} 삭제 요청 중 오류 발생`, err);
          });
        } else {
          // 미래 예약만 출력
          hasActiveReservations = true;
          reservationTbody.insertAdjacentHTML('beforeend', `
            <tr data-id="${r.id}">
              <td class="px-4 py-2">${i + 1}</td>
              <td class="px-4 py-2">${r.hospital}</td>
              <td class="px-4 py-2">${reservationTimeStr}</td>
              <td class="px-4 py-2">
                <button type="button" class="cancel-btn text-red-500 hover:text-red-700 text-xl">❌</button>
              </td>
            </tr>
          `);
        }
      });

      if (!hasActiveReservations) {
        reservationTbody.innerHTML = '<tr><td colspan="4" class="text-center px-4 py-4 text-gray-500">예약된 병원이 없습니다.</td></tr>';
      }
    } else {
      reservationTbody.innerHTML = '<tr><td colspan="4" class="text-center px-4 py-4 text-gray-500">예약된 병원이 없습니다.</td></tr>';
    }

    // 취소 버튼 이벤트 연결
    document.querySelectorAll(".cancel-btn").forEach(button => {
      button.addEventListener("click", event => {
        const row = event.target.closest("tr");
        const reservationId = row.getAttribute("data-id");

        if (confirm("정말 이 예약을 취소하시겠습니까?")) {
          fetch(`http://${serverIP}:5002/api/mypage/reservation/${reservationId}`, {
            method: "DELETE",
            credentials: "include"
          })
          .then(res => {
            if (res.ok) {
              alert("예약이 취소되었습니다.");
              row.remove();
              
              // 남은 예약이 없으면 메시지 표시
              if (reservationTbody.querySelectorAll('tr').length === 0) {
                reservationTbody.innerHTML = '<tr><td colspan="4" class="text-center px-4 py-4 text-gray-500">예약된 병원이 없습니다.</td></tr>';
              }
            } else {
              alert("예약 취소 실패");
            }
          });
        }
      });
    });
  })
  .catch(err => {
    console.error('[mypage.js] 예약 정보 오류:', err);
    if (reservationTbody) {
      reservationTbody.innerHTML = '<tr><td colspan="4" class="text-center text-red-500 px-4 py-4">예약 정보를 불러오는 데 실패했습니다.</td></tr>';
    }
  });

  // 3. 민감정보 조회
  if (healthForm) {
    fetch(`http://${serverIP}:5002/api/patient/info`, {
      method: 'GET',
      credentials: 'include'
    })
    .then(res => res.json())
    .then(result => {
      if (result.status === 'success' && result.data) {
        const info = result.data;
    
        const bt = healthForm.querySelector(`input[name="blood_type"][value="${info.blood_type}"]`);
        if (bt) bt.checked = true;
    
        healthForm.height.value = info.height_cm || '';
        healthForm.weight.value = info.weight_kg || '';
        healthForm.allergy.value = info.allergy_info || '';
        healthForm.past_diseases.value = info.past_illnesses || '';
        healthForm.chronic_diseases.value = info.chronic_diseases || '';
    
        // 약물
        if (healthForm.medications) {
          healthForm.medications.value = info.medications || '';
        }
    
        // 흡연 여부 라디오 버튼 체크
        const smokingRadio = healthForm.querySelector(`input[name="smoking"][value="${info.smoking}"]`);
        if (smokingRadio) smokingRadio.checked = true;
      } else {
        console.log('[mypage.js] 민감정보 없음 → 입력 가능 상태 유지');
      }
    })      
    .catch(err => {
      console.warn('[mypage.js] 민감정보 조회 실패 (비정상 응답이거나 정보 없음)', err);
    });

    // 4. 건강 정보 저장 이벤트
    healthForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const payload = {
        blood_type: healthForm.querySelector('input[name="blood_type"]:checked')?.value || '',
        height_cm: healthForm.height.value.trim(),
        weight_kg: healthForm.weight.value.trim(),
        allergy_info: healthForm.allergy.value.trim(),
        past_illnesses: healthForm.past_diseases.value.trim(),
        chronic_diseases: healthForm.chronic_diseases.value.trim(),
        medications: healthForm.medications?.value.trim() || '',
        smoking: healthForm.querySelector('input[name="smoking"]:checked')?.value || ''
      };
      
      console.log('[payload]', payload);
      
      fetch(`http://${serverIP}:5002/api/patient/info`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(res => res.json())
      .then(result => {
        if (result.status === 'success') {
          alert('건강 정보 저장 완료!');
        } else {
          alert('실패: ' + result.message);
        }
      })
      .catch(err => {
        console.error('[mypage.js] 건강 정보 저장 실패:', err);
        alert('저장 중 오류 발생');
      });
    });
  }

  // 5. 사용자 정보 수정 기능
if (editBtn) {
  editBtn.addEventListener('click', async (e) => {
    e.preventDefault(); // 이벤트 기본 동작 및 중복 요청 방지
    
    try {
      // 바로 정보 업데이트 요청 전송
      const payload = {
        email: userInfoForm.querySelector('[name="email"]').value,
        birthdate: userInfoForm.querySelector('[name="birthdate"]').value,
        phone: userInfoForm.querySelector('[name="phone"]').value,
        address: userInfoForm.querySelector('[name="address"]').value,
        address_detail: userInfoForm.querySelector('[name="detail_address"]').value
      };
      
      console.log('전송할 데이터:', payload);
      
      const response = await fetch(`http://${serverIP}:5002/api/users/update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      });
      
      const result = await response.json();
      
      if (result.status === 'success') {
        alert('정보가 성공적으로 수정되었습니다.');
      } else {
        alert(`수정 실패: ${result.message}`);
      }
    } catch (err) {
      console.error('수정 요청 중 예외 발생:', err);
      alert('서버 요청 중 오류가 발생했습니다.');
    }
  });
}
});

// 6. 회원탈퇴 요청 (비밀번호 확인 후 탈퇴)
function submitWithdraw() {
  const password = document.getElementById('withdrawPassword').value;
  const errorMsg = document.getElementById('withdrawError');
  const serverIP = document.body.dataset.serverIp;

  if (!password) {
    errorMsg.textContent = '비밀번호를 입력해주세요.';
    errorMsg.classList.remove('hidden');
    return;
  }

  // 1단계: 비밀번호 확인
  fetch(`http://${serverIP}:5002/api/users/check-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ password: password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      errorMsg.classList.add('hidden');

      // 2단계: 실제 탈퇴 처리
      fetch(`http://${serverIP}:5002/api/users/withdraw`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ password: password })
      })
      .then(res => res.json())
      .then(result => {
        if (result.success) {
          alert('회원 탈퇴가 완료되었습니다.');
          window.location.href = '/';
        } else {
          errorMsg.textContent = result.message || '탈퇴 처리 중 오류가 발생했습니다.';
          errorMsg.classList.remove('hidden');
        }
      });
    } else {
      errorMsg.textContent = data.message || '비밀번호가 일치하지 않습니다.';
      errorMsg.classList.remove('hidden');
    }
  })
  .catch(err => {
    console.error('에러:', err);
    errorMsg.textContent = '서버 오류가 발생했습니다.';
    errorMsg.classList.remove('hidden');
  });
}

const passwordChangeBtn = document.getElementById('submit-password-change');

if (passwordChangeBtn) {
  passwordChangeBtn.addEventListener('click', () => {
    const currentPassword = document.querySelector('#password-modal input[placeholder="현재 비밀번호"]').value.trim();
    const newPassword = document.querySelector('#password-modal input[placeholder="새 비밀번호"]').value.trim();
    const confirmPassword = document.querySelector('#password-modal input[placeholder="비밀번호 확인"]').value.trim();
    const serverIP = document.body.dataset.serverIp;

    // ✅ 이메일 인증 체크
    if (!isEmailVerified) {
      alert('이메일 인증 후 비밀번호를 변경할 수 있습니다.');
      return;
    }

    if (!currentPassword || !newPassword || !confirmPassword) {
      alert('모든 필드를 입력해주세요.');
      return;
    }

    if (newPassword !== confirmPassword) {
      alert('새 비밀번호와 확인이 일치하지 않습니다.');
      return;
    }

    // 서버에 비밀번호 변경 요청
    fetch(`http://${serverIP}:5002/api/users/change-password`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword
      })
    })
    .then(res => res.json())
    .then(result => {
      if (result.status === 'success') {
        alert('비밀번호가 성공적으로 변경되었습니다.');
        document.getElementById('password-modal').classList.add('hidden');
        isEmailVerified = false;  // ✅ 이후 변경 시 재인증 요구
      } else {
        alert('비밀번호 변경 실패: ' + result.message);
      }
    })
    .catch(err => {
      console.error('[mypage.js] 비밀번호 변경 오류:', err);
      alert('비밀번호 변경 중 오류가 발생했습니다.');
    });
  });
}


let isEmailVerified = false;

// 📌 비밀번호 변경 버튼 클릭 시 이메일 인증 모달만 표시
const openBtn = document.getElementById('change-password-btn');
if (openBtn) {
  openBtn.addEventListener('click', () => {
    isEmailVerified = false;  // 초기화
    openEmailVerificationModal();
  });
}

// 📌 이메일 인증 모달 열기
function openEmailVerificationModal() {
  document.getElementById('email-verification-modal').classList.remove('hidden');
  document.getElementById('email-verification-modal').classList.add('flex');
}

// 📌 인증코드 전송
function sendVerificationCode() {
  const email = document.getElementById('verificationEmail').value.trim();
  const serverIP = document.body.dataset.serverIp;

  if (!email) {
    alert('이메일을 입력해주세요.');
    return;
  }

  fetch(`http://${serverIP}:5002/api/users/send_code`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ email })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      alert('인증코드가 전송되었습니다.');
    } else {
      alert('코드 전송 실패: ' + data.message);
    }
  })
  .catch(err => {
    console.error('[mypage.js] 인증코드 전송 실패:', err);
    alert('인증코드 전송 중 오류 발생');
  });
}

// 📌 인증 확인 → 성공 시 비밀번호 변경 모달 열기
function submitVerificationCode() {
  const code = document.getElementById('verificationCode').value.trim();
  const serverIP = document.body.dataset.serverIp;

  if (!code) {
    alert('인증번호를 입력해주세요.');
    return;
  }

  const formData = new FormData();
  formData.append('code', code);

  fetch(`http://${serverIP}:5002/api/users/verify_code`, {
    method: 'POST',
    credentials: 'include',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      alert('이메일 인증이 완료되었습니다.');
      isEmailVerified = true;

      // 이메일 인증 모달 닫기
      document.getElementById('email-verification-modal').classList.add('hidden');
      document.getElementById('email-verification-modal').classList.remove('flex');

      // 비밀번호 변경 모달 열기
      document.getElementById('password-modal').classList.remove('hidden');
    } else {
      alert('인증 실패: ' + data.message);
    }
  });
}


function submitVerificationCode() {
  const code = document.getElementById('verificationCode').value.trim();
  const serverIP = document.body.dataset.serverIp;

  if (!code) {
    alert('인증번호를 입력해주세요.');
    return;
  }

  const formData = new FormData();
  formData.append('code', code);

  fetch(`http://${serverIP}:5002/api/users/verify_code`, {
    method: 'POST',
    credentials: 'include',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      alert('이메일 인증이 완료되었습니다.');
      document.getElementById('email-verification-modal').classList.add('hidden');
      isEmailVerified = true;  // ✅ 프론트는 확인용만
    } else {
      alert('인증 실패: ' + data.message);
    }
  });
}
