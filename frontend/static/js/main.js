const POSTERS_COUNT = 5;
const MAX_PAGE = 100;

document.addEventListener("DOMContentLoaded", () => {
    const page = getRandomPage(MAX_PAGE);
    const url = buildApiUrl(page);

    fetchFilmsPosters(url).then(renderPosters);
});

function getRandomPage(max) {
    return Math.floor(Math.random() * max) + 1;
}

function buildApiUrl(page) {
    const apiUrl = window.location.protocol + '//' +
        window.location.host + '/' +
        'api' + '/' + 'films';
    const params = new URLSearchParams({
        count: POSTERS_COUNT,
        page: page.toString()
    });

    return `${apiUrl}?${params.toString()}`;
}

function buildPosterUrl(baseUrl) {
    return `${baseUrl}/300x450`;
}

async function fetchFilmsPosters(url) {
    const response = await fetch(url);
    const posterUrls = [];

    if (response.ok) {
        const json = await response.json();
        const movies = json.data;

        movies.forEach(movie => {
            const poster = movie.media?.find(m => m.type === 'poster');
            if (poster?.full_url) {
                posterUrls.push(buildPosterUrl(poster.full_url));
            }
        });

        return posterUrls;
    }
}

function renderPosters(posterUrls) {
    const container = document.querySelector('.poster-stack');

    container.innerHTML = '';

    posterUrls.forEach(url => {
        const img = document.createElement('img');
        img.className = 'poster';
        img.src = url;

        container.appendChild(img);
    });
}
