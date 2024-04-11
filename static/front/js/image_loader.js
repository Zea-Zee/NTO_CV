let Nn = 'Город на Волге, основанный Великим князем Георгием Всеволодовичем в 1221 году. Богат историей и культурным наследием, включая Кремль и архитектуру.';
let Yarosl = 'Жемчужина Золотого кольца, основана Ярославом Мудрым в 1010 году. Соборы, монастыри и старинные улицы переносят в сказочное прошлое.';
let Ekat = 'Город на Урале, сочетающий историю и современность. Привлекает музеями, парками и культурной сценой.';
let Vladimir = 'Жемчужина Золотого кольца, основана Владимиром Мономахом в 1108 году. Привлекает красивой архитектурой и историческими памятниками.';
let selectedCity = 'Нижний Новгород';
let myMap;
let selectedColor;
let placesToVisit = [];


function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
	const predictWrapper = document.querySelector('.predict-wrapper');
	let mapDiv;
	let routeButton = document.getElementById('routeButton');
	routeButton.addEventListener('click', buildRouteFromCurrentLocation);
	let colorButtonsContainer = document.getElementById('colorButtons');
	let placesList = document.querySelector('#placesList')
	let cityBlock = document.querySelector('.city-block');
	cityBlock.style.backgroundImage = "url('../../static/front/images/Nizhniy Novgorod.jpg')";

	let citySelect = document.getElementById('citySelect');
	let fetchDataForm = document.querySelector('.put-info-container');
	let imageForm = document.querySelector('#imageForm')
	let descriptionForm = document.querySelector('#descriptionForm')

	let getSpots = document.getElementById('getSpots');

	let imageInput = document.getElementById('image');
	let descriptionInput = document.getElementById('text');

	function checkInputs() {
		if (imageInput.files.length > 0) {
			descriptionInput.disabled = true;
		} else {
			descriptionInput.disabled = false;
		}
		if (descriptionInput.value.trim() !== '') {
			imageInput.disabled = true;
		} else {
			imageInput.disabled = false;
		}
	}

	imageInput.addEventListener('input', checkInputs);
	descriptionInput.addEventListener('input', checkInputs);

	citySelect.addEventListener('change', function () {
		selectedCity = citySelect.value;
		let description = '';
		let imagePath = '';
		switch (selectedCity) {
			case 'Нижний Новгород':
				imagePath = '../../static/front/images/Nizhniy Novgorod.jpg';
				description = Nn;
				break;
			case 'Ярославль':
				imagePath = '../../static/front/images/Yaroslavl.png';
				description = Yarosl;
				break;
			case 'Екатеринбург':
				imagePath = '../../static/front/images/Ekaterinburg.jpeg';
				description = Ekat;
				break;
			case 'Владимир':
				imagePath = '../../static/front/images/Vladimir.jpg';
				description = Vladimir;
				break;
		}

		let cityBlock = document.querySelector('.city-block');
		cityBlock.style.backgroundImage = "url('" + imagePath + "')";
		document.querySelector('#city-name').innerText = selectedCity;
		document.querySelector('#city-description').innerText = description;
	});

	getSpots.addEventListener('click', function (event) {
		event.preventDefault();
		let formData = new FormData();
		let imageInput = document.getElementById('image');
		let descriptionInput = document.getElementById('text');

		if (imageInput.files && imageInput.files.length > 0) {
			formData.append('photo', imageInput.files[0]);
		} else {
			formData.append('text', descriptionInput.value);
		}
		formData.append('city', selectedCity);

		sendData(formData);
		imageInput.value = '';
		descriptionInput.value = '';
		imageInput.disabled = false;
		descriptionInput.disabled = false;
	});


	function sendData(formData) {
		const csrftoken = getCookie('csrftoken');
		fetch('/predict_front', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken
			},
			body: formData
		})
			.then(response => {
				if (!response.ok) {
					throw new Error('Network response was not ok');
				}
				return response.json();
			})
			.then(data => {
				console.log(data);
				if (data.image) {
					addPredictedImage(data.image);
				} else {
					console.log(`No data available ${data}`);
				}


				ymaps.ready(function () {
					console.log('creating map');
					if (myMap) {
						myMap.geoObjects.removeAll();

						mapDiv = document.createElement('div');
						mapDiv.id = 'map';
						mapDiv.style.width = '600px';
						mapDiv.style.height = '400px';
						predictWrapper.appendChild(mapDiv);
					}
					ymaps.geolocation.get({
						provider: 'browser'
					}).then(function (result) {
						myMap = new ymaps.Map("map", {
							center: result.geoObjects.get(0).geometry.getCoordinates(),
							zoom: 7
						});
						myMap.geoObjects.add(result.geoObjects);

						let magentaSpot = new ymaps.Placemark([data.spots[0].Lat, data.spots[0].Lon], {
							iconContent: data.spots[0].prob,
							balloonContent: data.spots[0].text_from_div
						}, {
							preset: 'islands#violetStretchyIcon'
						});
						magentaSpot.events.add('click', function (e) {
							console.log(data.spots[0]);
						});
						myMap.geoObjects.add(magentaSpot)


						let blueSpot = new ymaps.Placemark([data.spots[1].Lat, data.spots[1].Lon], {
							// iconContent: data.spots[1].prob
							iconContent: data.spots[1].prob
							,
							balloonContent: data.spots[1].text_from_div
						}, {
							preset: 'islands#blueStretchyIcon'
						});
						myMap.geoObjects.add(blueSpot)

						let greenSpot = new ymaps.Placemark([data.spots[2].Lat, data.spots[2].Lon], {
							iconContent: data.spots[2].prob,
							balloonContent: data.spots[2].text_from_div
						}, {
							preset: 'islands#greenStretchyIcon'
						});
						myMap.geoObjects.add(greenSpot)

						let yellowSpot = new ymaps.Placemark([data.spots[3].Lat, data.spots[3].Lon], {
							iconContent: data.spots[3].prob,
							balloonContent: data.spots[3].text_from_div
						}, {
							preset: 'islands#yellowStretchyIcon'
						});
						myMap.geoObjects.add(yellowSpot)

						let orangeSpot = new ymaps.Placemark([data.spots[4].Lat, data.spots[4].Lon], {
							iconContent: data.spots[4].prob,
							balloonContent: data.spots[4].text_from_div
						}, {
							preset: 'islands#orangeStretchyIcon'
						});
						myMap.geoObjects.add(orangeSpot)

					}).catch(function (err) {
						console.log('Ошибка: ' + err);
						createMap({
							center: [55.751574, 37.573856],
							zoom: 2
						});
					});

					function createMap(state) {
						myMap = new ymaps.Map('map', state);
					}
				});

				colorButtonsContainer.style.display = 'block';
				let colorButtons = document.querySelectorAll('.colorButton');
				document.getElementById('map').style.display = 'block';

				colorButtons.forEach(function (button, i) {

					let spotName = data.spots[i]['Name'];
					spotName = spotName.substring(0, 10);
					let spotNameElement = document.createElement('span');
					spotNameElement.innerText = spotName;
					button.appendChild(spotNameElement);
					button.style.backgroundColor = button.getAttribute('data-color');

					button.addEventListener('click', function () {
						selectedColor = this.getAttribute('data-color');
						let spot = data.spots[i];
						placesToVisit.push(spot);
						colorButtonsContainer.style.display = 'none';
						document.getElementById('map').style.display = 'none';
						let bars = document.querySelector('.prediction-container');
						if (bars) bars.remove()
						placesList.style.display = 'flex'
						const listItem = document.createElement('div');
						listItem.innerHTML = `
            <p>${spot.Name} ${spot.Lon} ${spot.Lat}</p>
        `;
						var mapElement = document.getElementById('map');

						// Проверяем, существует ли элемент
						if (mapElement) {
							// Если элемент существует, удаляем его
							mapElement.parentNode.removeChild(mapElement);
						} else {
							// Если элемент не найден, выводим сообщение об ошибке
							console.log('Элемент с id "map" не найден.');
						}
						placesList.appendChild(listItem);

						routeButton.style.display = 'block'
					});
				});


			})
			.catch(error => {
				console.error('There was an error!', error);
			});
	}


	function base64ToImage(base64Data) {
		const img = new Image();
		img.src = 'data:image/png;base64,' + base64Data;
		return img;
	}

	function addPredictedImage(imageData) {
		const imgElement = base64ToImage(imageData);
		const predictWrapper = document.querySelector('.predict-wrapper');
		const existingPrediction = predictWrapper.querySelector('img');
		imgElement.classList.add('prediction-container')
		if (existingPrediction) {
			existingPrediction.remove();
		}
		predictWrapper.appendChild(imgElement);
	}


	function buildRouteFromCurrentLocation() {
		fetchDataForm.style.display = 'none';
		getSpots.style.display = 'none';

		ymaps.geolocation.get({
			provider: 'auto',
			autoReverseGeocode: true
		}).then(function (result) {
			// Получение координат текущего местоположения
			var userCoords = result.geoObjects.get(0).geometry.getCoordinates();
			console.log('Координаты текущего местоположения:', userCoords);

			// Создание копии списка placesToVisit
			var placesCopy = JSON.parse(JSON.stringify(placesToVisit));
			// Массив для хранения новых мест
			var newPlaces = [];

			// Добавляем текущее местоположение пользователя в список newPlaces
			newPlaces.push({
				'Lat': userCoords[0],
				'Lon': userCoords[1],
				'Name': 'Моё местоположение'
			});

			// Построение маршрутов от текущего местоположения пользователя
			// до каждой точки из списка placesToVisit
			buildRoute(newPlaces[0], placesCopy, newPlaces);
			drawRoute(newPlaces);
		}).catch(function (error) {
			console.error('Ошибка при получении местоположения:', error);
		});
	}

	// Функция для построения маршрутов от одной точки до всех остальных
	function buildRoute(startPlace, placesToVisit, newPlaces) {
		if (placesToVisit.length === 0) {
			console.log('Маршрут построен');
			return;
		}

		var closestPlace = findClosestPlace(startPlace, placesToVisit);
		console.log('Ближайшее место:', closestPlace);

		placesToVisit = placesToVisit.filter(function (place) {
			return place !== closestPlace;
		});
		console.log(`new free placelist ${JSON.stringify(placesToVisit)}`);
		newPlaces.push(closestPlace);
		console.log(`new route placelist ${JSON.stringify(newPlaces)}`);
		buildRoute(closestPlace, placesToVisit, newPlaces);
	}

	// Функция для нахождения ближайшего места к данным координатам
	function findClosestPlace(startPlace, placesToVisit) {
		var closestDistance = Infinity;
		var closestPlace = null;

		placesToVisit.forEach(function (place) {
			var distance = calculateDistance([startPlace.Lon, startPlace.Lat], [place.Lon, place.Lat]);

			console.log(`distance: ${distance}  ${closestDistance}`);
			if (distance < closestDistance) {
				closestDistance = distance;
				closestPlace = place;
			}
		});

		return closestPlace;
	}

	// Функция для вычисления расстояния между двумя точками на карте (гипотенуза)
	function calculateDistance(coords1, coords2) {
		console.log(`start coords: ${coords1}
		end coords: ${coords2}
		`);
		var dx = coords2[0] - coords1[0];
		var dy = coords2[1] - coords1[1];
		return Math.sqrt(dx * dx + dy * dy);
	}


	function drawRoute(places) {
		let map2 = document.querySelector('#map2')
		map2.style.display = 'block'
		ymaps.ready(function () {
			var myMap = new ymaps.Map('map2', {
				center: [places[0].Lat, places[0].Lon],
				zoom: 9,
				controls: []
			});

			let coords = places.map(function (place) {
				return [place.Lat, place.Lon];
			})
			console.log(`dots for route are: ${coords}`);
			var multiRoute = new ymaps.multiRouter.MultiRoute({
				referencePoints: coords
			}, {
				// Автоматически устанавливать границы карты так,
				// чтобы маршрут был виден целиком.
				boundsAutoApply: true
			});

			// Добавление маршрута на карту.
			myMap.geoObjects.add(multiRoute);
		})
	}
})