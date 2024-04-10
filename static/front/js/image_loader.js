document.addEventListener("DOMContentLoaded", function() {
    document.getElementsByClassName('city-block').backgroundImage = "url('" + imagePath + "')";
});

let citySelect = document.getElementById('citySelect');
citySelect.addEventListener('change', function() {
    let selectedCity = citySelect.value;
	let imagePath = '../../static/front/images/Nizhniy Novgorod.jpg';
	switch(selectedCity){
		case 'Нижний Новгород':
			imagePath = '../../static/front/images/Nizhniy Novgorod.jpg';
			break;
		case 'Ярославль':
			imagePath = '../../static/front/images/Yaroslavl.png';
			break;
		case 'Екатеринбург':
			imagePath = '../../static/front/images/Ekaterinburg.jpeg';
			break;
		case 'Владимир':
			imagePath = '../../static/front/images/Vladimir.jpg';
			break;
	}

	console.log(imagePath);
	document.getElementsByClassName('city-block').backgroundImage = "url('" + imagePath + "')";
});
