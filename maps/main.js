async function fetchDataFromUrl(url) {
    try {
        const response = await fetch(url);
        console.log(response)
        if (!response.ok) { // Проверяем успешность запроса
            throw new Error('Ошибка HTTP: ' + response.status);
        }
        const html = await response.text(); // Получаем HTML-код страницы
        const parser = new DOMParser(); // Создаем парсер для HTML
        const doc = parser.parseFromString(html, 'text/html'); // Парсим HTML
        const description = doc.querySelector('meta[name="description"]').getAttribute('content'); // Извлекаем описание
        const imageUrl = doc.querySelector('meta[property="og:image"]').getAttribute('content'); // Извлекаем ссылку на изображение
        return { description, imageUrl }; // Возвращаем объект с данными
    } catch (error) {
        console.error('Произошла ошибка:', error);
        return null;
    }
}

// const exampleUrl = 'https://opentripmap.com/ru/card/R2906502';
// const exampleUrl = 'https://opentripmap.com/ru/card/R2906502#15/56.3280/44.0021';
const exampleUrl = 'google.com';
fetchDataFromUrl(exampleUrl)
    .then(data => {
        if (data) {
            console.log('Описание:', data.description);
            console.log('URL изображения:', data.imageUrl);
        } else {
            console.log('Не удалось получить данные.');
        }
    })
    .catch(err => console.error('Произошла ошибка:', err));
