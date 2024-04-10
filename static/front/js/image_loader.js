let Nn = 'Город на Волге, основанный Великим князем Георгием Всеволодовичем в 1221 году. Богат историей и культурным наследием, включая Кремль и архитектуру.';
let Yarosl = 'Жемчужина Золотого кольца, основана Ярославом Мудрым в 1010 году. Соборы, монастыри и старинные улицы переносят в сказочное прошлое.';
let Ekat = 'Город на Урале, сочетающий историю и современность. Привлекает музеями, парками и культурной сценой.';
let Vladimir = 'Жемчужина Золотого кольца, основана Владимиром Мономахом в 1108 году. Привлекает красивой архитектурой и историческими памятниками.';
let selectedCity = 'Нижний Новгород';
let myMap;


function initMap() {
    ymaps.geolocation.get({
        provider: 'yandex'
    }).then(function (result) {
        myMap = new ymaps.Map("map", {
            center: result.geoObjects.get(0).geometry.getCoordinates(),
            zoom: 7
        });
        myMap.geoObjects.add(result.geoObjects);
    }).catch(function (err) {
        console.log('Ошибка: ' + err);
        createMap({
            center: [55.751574, 37.573856],
            zoom: 2
        });
    });
}


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
	let cityBlock = document.querySelector('.city-block');
	cityBlock.style.backgroundImage = "url('../../static/front/images/Nizhniy Novgorod.jpg')";

	let citySelect = document.getElementById('citySelect');
	let fetchDataForm = document.querySelector('.put-info-container');
	let imageForm = document.querySelector('#imageForm')
	let descriptionForm = document.querySelector('#descriptionForm')

	let getSpots = document.getElementById('getSpots');
	let imageInput = document.getElementById('image');
	let descriptionInput = document.getElementById('text');


	ymaps.ready(initMap);


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
					console.log(data);
				}
				addMarkers(data.spots);
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
	function addMarkers(spots) {
		// Добавление меток на карту
		for (let i = 0; i < spots.length; i++) {
			let spot = spots[i];
			let marker = new ymaps.Placemark([spot.Lat, spot.Lon], {
				balloonContent: spot.prob
			}, {
				preset: 'islands#violetIcon'
			});
			myMap.geoObjects.add(marker);
		}
	}
});
