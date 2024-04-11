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
					var myMap;
					ymaps.geolocation.get({
						provider: 'yandex'
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
							createAndCenterContainer(data.spots[0]['modal-dialog'])
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
            <p>${spot.Name.substring(0, 10)} ${spot.Lon} ${spot.Lat}</p>
        `;
						placesList.appendChild(listItem);
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


	function createAndCenterContainer(containerText) {
		// Создаем временный div элемент
		var tempDiv = document.createElement('div');

		// Задаем текст контейнера для временного div
		tempDiv.innerHTML = containerText;

		// Получаем размеры окна браузера
		var windowWidth = window.innerWidth;
		var windowHeight = window.innerHeight;

		// Получаем размеры контейнера
		var containerWidth = tempDiv.offsetWidth;
		var containerHeight = tempDiv.offsetHeight;

		// Рассчитываем координаты для размещения контейнера по центру
		var leftPosition = (windowWidth - containerWidth) / 2;
		var topPosition = (windowHeight - containerHeight) / 2;

		// Устанавливаем позицию абсолютно по центру
		tempDiv.style.position = 'absolute';
		tempDiv.style.left = leftPosition + 'px';
		tempDiv.style.top = topPosition + 'px';

		// Добавляем временный div в самый верхний уровень DOM (поверх всего)
		document.body.appendChild(tempDiv);
	}
});
