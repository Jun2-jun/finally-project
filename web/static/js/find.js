let map;
let markers = [];
let infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });


function initMap(lat, lng) {
  map = new kakao.maps.Map(document.getElementById('map'), {
    center: new kakao.maps.LatLng(lat, lng),
    level: 5
  });
}

function searchPlaces() {
  const keyword = document.getElementById('keyword').value.trim();
  if (!keyword) {
    alert('검색어를 입력해주세요.');
    return;
  }
  const ps = new kakao.maps.services.Places();
  ps.keywordSearch(keyword, placesSearchCB, { location: map.getCenter() });
}

function placesSearchCB(data, status, pagination) {
  if (status === kakao.maps.services.Status.OK) {
    displayPlaces(data);
    displayPagination(pagination);
  } else {
    alert('검색 결과가 없습니다.');
  }
}

function displayPlaces(places) {
  const listEl = document.getElementById('placesList');
  listEl.innerHTML = '';
  removeMarkers();

  const bounds = new kakao.maps.LatLngBounds();

  places.forEach((place) => {
    const position = new kakao.maps.LatLng(place.y, place.x);
    const marker = new kakao.maps.Marker({ position, map });

    kakao.maps.event.addListener(marker, 'click', () => {
      infowindow.setContent(`<div style="padding:5px;"><a href="${place.place_url}" target="_blank">${place.place_name}</a></div>`);
      infowindow.open(map, marker);
    });

    markers.push(marker);
    bounds.extend(position);

    const itemEl = document.createElement('li');
    itemEl.innerHTML = `
      <strong>${place.place_name}</strong><br>
      <span>${place.road_address_name || place.address_name}</span><br>
      <span style="color:green">${place.phone}</span><br>
      <button class="reserve-btn">예약</button>
    `;

    itemEl.onclick = () => {
      map.setCenter(position);
      infowindow.setContent(`<div style="padding:5px;"><a href="${place.place_url}" target="_blank">${place.place_name}</a></div>`);
      infowindow.open(map, marker);
    };

    const reserveBtn = itemEl.querySelector('.reserve-btn');
    reserveBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = '/reserve';

      const nameInput = document.createElement('input');
      nameInput.type = 'hidden';
      nameInput.name = 'hospital_name';
      nameInput.value = place.place_name;

      const addressInput = document.createElement('input');
      addressInput.type = 'hidden';
      addressInput.name = 'hospital_address';
      addressInput.value = place.road_address_name || place.address_name;

      form.appendChild(nameInput);
      form.appendChild(addressInput);
      document.body.appendChild(form);
      form.submit();
    });

    listEl.appendChild(itemEl);
  });

  map.setBounds(bounds);
  map.setLevel(map.getLevel() - 1);
}

function removeMarkers() {
  markers.forEach(marker => marker.setMap(null));
  markers = [];
}

function displayPagination(pagination) {
  const paginationEl = document.getElementById('pagination');
  paginationEl.innerHTML = '';
  for (let i = 1; i <= pagination.last; i++) {
    const a = document.createElement('a');
    a.href = '#';
    a.innerText = i;
    if (i === pagination.current) a.className = 'on';
    else a.onclick = () => pagination.gotoPage(i);
    paginationEl.appendChild(a);
  }
}

navigator.geolocation.getCurrentPosition(
  (pos) => {
    initMap(pos.coords.latitude, pos.coords.longitude);
    searchPlaces();
  },
  () => {
    initMap(37.5665, 126.9780); // 서울 좌표
    searchPlaces();
  }
);

