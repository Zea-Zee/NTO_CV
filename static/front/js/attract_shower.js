async function fetchDataFromUrl(url) {
    try {
      const response = await fetch(`/fetch_otp?url=${encodeURIComponent(url)}`);
        if (!response.ok) {
            throw new Error('Ошибка HTTP: ' + response.status);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Произошла ошибка:', error);
        return null;
    }
}

document.getElementById('fetchDataForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение отправки формы
    const url = document.getElementById('urlInput').value;
    const data = await fetchDataFromUrl(url);
    if (data) {
        console.log('Описание:', data.description);
        console.log('URL изображения:', data.image_url);
    } else {
        console.log('Не удалось получить данные.');
    }
});