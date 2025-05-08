document.addEventListener('DOMContentLoaded', () => {
    const reservationTbody = document.querySelector('#reservation-check tbody');
    const userInfoForm = document.getElementById('mypage-form');
    const healthForm = document.querySelector('#health-form');
  
    reservationTbody.innerHTML = '<tr><td colspan="3" class="text-center">불러오는 중...</td></tr>';
  
    // 1. 현재 사용자 정보 가져오기
    fetch('http://192.168.219.72:5002/api/current-user', {
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
          return fetch(`http://192.168.219.72:5002/api/reservations/user/${userId}`, {
            method: 'GET',
            credentials: 'include'
          });
        } else {
          throw new Error('userData 실패');
        }
      })
      .then(res => res.json())
      .then(reservationData => {
        reservationTbody.innerHTML = '';
  
        if (reservationData.status === 'success' && reservationData.data.length > 0) {
          reservationData.data.forEach((r, i) => {
            const reservationTimeStr = r.reservation_time || `${r.date} ${r.time}`;
            const reservationTime = new Date(reservationTimeStr);
            const now = new Date();
  
            if (reservationTime < now) {
              // 과거 예약 삭제
              fetch(`http://192.168.219.72:5002/api/mypage/reservation/${r.id}`, {
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
              reservationTbody.insertAdjacentHTML('beforeend', `
                <tr data-id="${r.id}">
                  <td>        ${i + 1}</td>
                  <td>  ${r.hospital}</td>
                  <td>${reservationTimeStr}</td>
                  <td><button type="button" class="cancel-btn text-red-500 hover:text-red-700 text-xl">       ❌</button></td>
                </tr>
              `);
            }
          });
  
          if (!reservationTbody.querySelector('tr')) {
            reservationTbody.innerHTML = '<tr><td colspan="4" class="text-center">예약된 병원이 없습니다.</td></tr>';
          }
        } else {
          reservationTbody.innerHTML = '<tr><td colspan="4" class="text-center">예약된 병원이 없습니다.</td></tr>';
        }
  
        // 취소 버튼 이벤트 연결
        document.querySelectorAll(".cancel-btn").forEach(button => {
          button.addEventListener("click", event => {
            const row = event.target.closest("tr");
            const reservationId = row.getAttribute("data-id");
  
            if (confirm("정말 이 예약을 취소하시겠습니까?")) {
              fetch(`http://192.168.219.72:5002/api/mypage/reservation/${reservationId}`, {
                method: "DELETE",
                credentials: "include"
              })
                .then(res => {
                  if (res.ok) {
                    alert("예약이 취소되었습니다.");
                    row.remove();
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
        reservationTbody.innerHTML = '<tr><td colspan="4" class="text-center text-red-500">예약 정보를 불러오는 데 실패했습니다.</td></tr>';
      });
  
    // 3. 민감정보 조회
    fetch('http://192.168.219.72:5002/api/patient/info', {
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
      
          // ✅ 추가: 약물
          if (healthForm.medications) {
            healthForm.medications.value = info.medications || '';
          }
      
          // ✅ 추가: 흡연 여부 라디오 버튼 체크
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
    if (healthForm) {
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
          
  
        fetch('http://192.168.219.72:5002/api/patient/info', {
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
    // 수정 버튼 요소 가져오기
  const button = document.getElementById('edit-btn');
  if (!button) {
    console.error('❌ 수정 버튼(#edit-btn)을 찾을 수 없습니다.');
    return;
  }

  // 수정 버튼 클릭 처리
  button.addEventListener('click', async () => {
    console.log('수정하기 버튼 클릭됨');

    const payload = {
      email: document.querySelector('[name="email"]').value,
      birthdate: document.querySelector('[name="birthdate"]').value,
      phone: document.querySelector('[name="phone"]').value,
      address: document.querySelector('[name="address"]').value,
      address_detail: document.querySelector('[name="detail_address"]').value
    };
    console.log('전송할 데이터:', payload);

    try {
      const response = await fetch('http://192.168.219.72:5002/api/users/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      });
      const result = await response.json();
      console.log('수정 응답:', result);

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
  });
  
