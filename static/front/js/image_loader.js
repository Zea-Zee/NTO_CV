Nn = 'Город на Волге, основанный Великим князем Георгием Всеволодовичем в 1221 году. Богат историей и культурным наследием, включая Кремль и архитектуру.'
Yarosl = 'Жемчужина Золотого кольца, основана Ярославом Мудрым в 1010 году. Соборы, монастыри и старинные улицы переносят в сказочное прошлое.'
Ekat = 'Город на Урале, сочетающий историю и современность. Привлекает музеями, парками и культурной сценой.'
Vladimir = 'Жемчужина Золотого кольца, основана Владимиром Мономахом в 1108 году. Привлекает красивой архитектурой и историческими памятниками.'
let selectedCity = 'Нижний Новгород'


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Ищем куки с нужным именем
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



document.addEventListener("DOMContentLoaded", function() {
    let cityBlock = document.querySelector('.city-block');
	cityBlock.style.backgroundImage = "url('../../static/front/images/Nizhniy Novgorod.jpg')";

	let citySelect = document.getElementById('citySelect');
	let fetchDataForm = document.querySelector('.put-info-container');
	let imageForm = document.querySelector('#imageForm')
	let descriptionForm = document.querySelector('#descriptionForm')

    let getSpots = document.getElementById('getSpots');
    let selectedPlacesList = document.getElementById('selectedPlacesList');
    let selectedPlaces = [];

	let imageInput = document.getElementById('image');
	let descriptionInput = document.getElementById('text');


    function checkInputs() {
		console.log(fetchDataForm);
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


	citySelect.addEventListener('change', function() {
		selectedCity = citySelect.value;
		let description = 'Основанный в 1221 году Великим Князем Георгием Всеволодовичем, Нижний Новгород - один из старейших российских городов. Столица Поволжского княжества в XIV-XV веках, он был крупным торговым центром, играя важную роль в экономической и политической жизни страны. Здесь расположена Кремлевская площадь с Домом Рождества Богородицы и другими историческими памятниками.';
		let imagePath = '../../static/front/images/Nizhniy Novgorod.jpg';
		switch(selectedCity){
			case 'Нижний Новгород':
				imagePath = '../../static/front/images/Nizhniy Novgorod.jpg';
				description = Nn
				break;
			case 'Ярославль':
				imagePath = '../../static/front/images/Yaroslavl.png';
				description = Yarosl
				break;
			case 'Екатеринбург':
				imagePath = '../../static/front/images/Ekaterinburg.jpeg';
				description = Ekat
				break;
			case 'Владимир':
				imagePath = '../../static/front/images/Vladimir.jpg';
				description = Vladimir
				break;
		}

		let cityBlock = document.querySelector('.city-block');
		cityBlock.style.backgroundImage = "url('" + imagePath + "')";
		document.querySelector('#city-name').innerText = selectedCity;
		document.querySelector('#city-description').innerText = description;
	});


    getSpots.addEventListener('click', function(event) {
		console.log('getspot click');
        event.preventDefault();
        let selectedPlacesContainer = document.getElementById('selectedPlacesContainer');    
        if (!selectedPlacesContainer) {
            selectedPlacesContainer = document.createElement('div');
            selectedPlacesContainer.id = 'selectedPlacesContainer';
            selectedPlacesContainer.classList.add('selected-places-container');
            selectedPlacesContainer.innerHTML = `
                <p>Выбранные места:</p>
                <ul id="selectedPlacesList">
                </ul>
            `;
            fetchDataForm.insertAdjacentElement('afterend', selectedPlacesContainer);
        }

        let formData = new FormData();
		console.log(imageInput);
		console.log(descriptionInput);
        if (imageInput.files && imageInput.files.length > 0) {
            formData.append('photo', imageInput.files[0]);
        } else {
            formData.append('text', descriptionInput.value);
        }

		formData.append('city', selectedCity)
		console.log(formData);
        sendData(formData);
		imageInput.value = '';
		descriptionInput.value = '';
		imageForm.reset()
		descriptionForm.reset()
		imageInput.disabled = false;
		descriptionInput.disabled = false;
    });

    function sendData(formData) {
        const csrftoken = getCookie('csrftoken');
		fetch('/predict_front', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken // Добавляем токен CSRF в заголовок запроса
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
        })
        .catch(error => {
            console.error('There was an error!', error);
        });
    }
});