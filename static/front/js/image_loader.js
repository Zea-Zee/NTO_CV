Nn = 'Город на Волге, основанный Великим князем Георгием Всеволодовичем в 1221 году. Богат историей и культурным наследием, включая Кремль и архитектуру.'
Yarosl = 'Жемчужина Золотого кольца, основана Ярославом Мудрым в 1010 году. Соборы, монастыри и старинные улицы переносят в сказочное прошлое.'
Ekat = 'Город на Урале, сочетающий историю и современность. Привлекает музеями, парками и культурной сценой.'
Vladimir = 'Жемчужина Золотого кольца, основана Владимиром Мономахом в 1108 году. Привлекает красивой архитектурой и историческими памятниками.'

document.addEventListener("DOMContentLoaded", function() {
    let cityBlock = document.querySelector('.city-block');
	cityBlock.style.backgroundImage = "url('../../static/front/images/Nizhniy Novgorod.jpg')";
});

let citySelect = document.getElementById('citySelect');
citySelect.addEventListener('change', function() {
    let selectedCity = citySelect.value;
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

	console.log(imagePath);
	let cityBlock = document.querySelector('.city-block');
	cityBlock.style.backgroundImage = "url('" + imagePath + "')";
	document.querySelector('#city-name').innerText = selectedCity;
	document.querySelector('#city-description').innerText = description;
});
