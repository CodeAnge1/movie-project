const MIN_RATING = 0.0;
const MAX_RATING = 10.0;
const MIN_YEAR = 1890;
const MAX_YEAR = new Date().getFullYear() + 1;

const RATING_REGEX = /^[0-9]*\.?[0-9]*$/;
const YEAR_REGEX = /^\d+$/;

const MOVIE_API_URL = '/api/films';

const validateInput = (event, regex) => {
    const value = event.target.value;
    if (!regex.test(value)) {
        event.target.value = value.slice(0, -1);
    }
};

const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

const addInputValidation = (input, regex, onBlur) => {
    input.addEventListener('input', e => validateInput(e, regex));
    input.addEventListener('blur', onBlur);
};

document.querySelectorAll('.filter-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
        const target = document.getElementById(btn.dataset.target);
        if (!target) return;
        target.classList.toggle('open');
        btn.querySelector('.arrow')?.classList.toggle('rotate');
    });
});

document.addEventListener('DOMContentLoaded', () => {
    initFilters();
    initRatingFilter();
    initYearFilter();
    loadFilteredFilms();

    const applyBtn = document.querySelector('.apply-filters-btn');
    applyBtn.addEventListener('click', () => {
        loadFilteredFilms();
    });

    document.querySelector('.search-wrapper input')
        .addEventListener('input', debounce(() => loadFilteredFilms(), 500));

    document.querySelector('.sort-select')
        .addEventListener('change', () => loadFilteredFilms());
});

const initFilters = () => {
    fetchAndRenderFilter('/api/genres', 'genre-options');
    fetchAndRenderFilter('/api/countries', 'country-options');
};

const fetchAndRenderFilter = (url, targetId) => {
    fetch(url)
        .then(res => res.ok ? res.json() : null)
        .then(data => renderFilterOptions(data, targetId));
};

const renderFilterOptions = (data, containerId) => {
    if (!data?.data) return;
    const container = document.getElementById(containerId);
    if (!container) return;

    data.data.forEach(({ id, name }) => {
        container.appendChild(createFilterOption(containerId, name, name));
    });
};

const createFilterOption = (name, value, text) => {
    const label = document.createElement('label');
    label.className = 'filter-option';

    const checkbox = Object.assign(document.createElement('input'), {
        type: 'checkbox',
        name,
        value
    });

    const span = document.createElement('span');
    span.textContent = text;

    label.append(checkbox, span);
    return label;
};

const initRatingFilter = () => {
    const minInput = document.getElementById('rating-min-input');
    const maxInput = document.getElementById('rating-max-input');
    const minSlider = document.getElementById('rating-min');
    const maxSlider = document.getElementById('rating-max');

    const validate = value => clamp(value, MIN_RATING, MAX_RATING);

    const syncFromInput = () => {
        let min = parseFloat(minInput.value) || MIN_RATING;
        let max = parseFloat(maxInput.value) || MAX_RATING;
        min = validate(min);
        max = validate(max);

        minSlider.value = min;
        maxSlider.value = max;

        minInput.value = min.toFixed(1);
        maxInput.value = max.toFixed(1);
    };

    const syncFromSlider = () => {
        let min = validate(parseFloat(minSlider.value));
        let max = validate(parseFloat(maxSlider.value));

        minInput.value = min.toFixed(1);
        maxInput.value = max.toFixed(1);
    };

    minInput.value = MIN_RATING.toFixed(1);
    maxInput.value = MAX_RATING.toFixed(1);

    [minSlider, maxSlider].forEach(slider => {
        slider.min = MIN_RATING;
        slider.max = MAX_RATING;
    });

    minSlider.value = MIN_RATING;
    maxSlider.value = MAX_RATING;

    addInputValidation(minInput, RATING_REGEX, syncFromInput);
    addInputValidation(maxInput, RATING_REGEX, syncFromInput);

    minSlider.addEventListener('input', syncFromSlider);
    maxSlider.addEventListener('input', syncFromSlider);
};

const initYearFilter = () => {
    const minInput = document.getElementById('year-min-input');
    const maxInput = document.getElementById('year-max-input');
    const minSlider = document.getElementById('year-min');
    const maxSlider = document.getElementById('year-max');

    const validate = value => clamp(value, MIN_YEAR, MAX_YEAR);

    const syncFromInput = () => {
        let min = parseInt(minInput.value) || MIN_YEAR;
        let max = parseInt(maxInput.value) || MAX_YEAR;
        min = validate(min);
        max = validate(max);

        minSlider.value = min;
        maxSlider.value = max;

        minInput.value = min;
        maxInput.value = max;
    };

    const syncFromSlider = () => {
        let min = validate(parseInt(minSlider.value));
        let max = validate(parseInt(maxSlider.value));

        minInput.value = min;
        maxInput.value = max;
    };

    [minInput, maxInput, minSlider, maxSlider].forEach(el => {
        el.min = MIN_YEAR;
        el.max = MAX_YEAR;
    });

    minInput.value = MIN_YEAR;
    maxInput.value = MAX_YEAR;
    minSlider.value = MIN_YEAR;
    maxSlider.value = MAX_YEAR;

    addInputValidation(minInput, YEAR_REGEX, syncFromInput);
    addInputValidation(maxInput, YEAR_REGEX, syncFromInput);

    minSlider.addEventListener('input', syncFromSlider);
    maxSlider.addEventListener('input', syncFromSlider);
};

const loadFilteredFilms = async (page = 1) => {
    const genreNames = Array.from(document.querySelectorAll('#genre-options input:checked'))
        .map(el => el.nextSibling.textContent.trim());

    const countryNames = Array.from(document.querySelectorAll('#country-options input:checked'))
        .map(el => el.nextSibling.textContent.trim());

    const year_from = document.getElementById('year-min-input').value || MIN_YEAR;
    const year_to = document.getElementById('year-max-input').value || MAX_YEAR;

    const rating_from = document.getElementById('rating-min-input').value || MIN_RATING;
    const rating_to = document.getElementById('rating-max-input').value || MAX_RATING;

    const title = document.querySelector('.search-wrapper input').value.trim();
    const sort = document.querySelector('.sort-select')?.value || '';

    const params = new URLSearchParams({
        page,
        title,
        year_from,
        year_to,
        rating_from,
        rating_to
    });

    if (genreNames.length) params.append('genres', genreNames.join(','));
    if (countryNames.length) params.append('countries', countryNames.join(','));
    if (sort) params.append('sort', sort);

    const response = await fetch(`${MOVIE_API_URL}?${params.toString()}`);
    if (response.ok) {
        const result = await response.json();

        if (sort === 'rating') {
            result.data.sort((a, b) => (b.rating || 0) - (a.rating || 0));
        } else if (sort === 'year') {
            result.data.sort((a, b) => (b.year || 0) - (a.year || 0));
        }

        renderFilms(result.data, result.meta?.records);
        renderPagination(result.meta.pages, page);
    }
};

function buildPosterUrl(baseUrl) {
    return `${baseUrl}/300x450`;
}

function getPoster(movie) {
    const poster = movie.media?.find(m => m.type === 'poster');
    return poster?.full_url ? buildPosterUrl(poster.full_url) : '';
}

const getTitle = (movie) => movie.title || 'Без названия';
const getYear = (movie) => `Год: ${movie.year || '—'}`;
const getRating = (movie) => {
    const rating = Number(movie.rating);
    return `★ ${!isNaN(rating) ? rating.toFixed(1) : '—'}`;
};

const getShortDescription = (movie, maxLength = 150) => {
    const text = movie.description || '';
    return text.length > maxLength ? text.slice(0, maxLength) + '...' : text;
};

const renderFilms = (movies, totalRecords = movies.length) => {
    const container = document.querySelector('.movie-grid');
    const countDisplay = document.getElementById('movie-count-number');
    const template = document.getElementById('movie-card-template');

    container.innerHTML = '';
    countDisplay.textContent = totalRecords;

    movies.forEach(movie => {
        const clone = template.content.cloneNode(true);
        const link = clone.querySelector('.movie-link');
        const card = clone.querySelector('.movie-card');

        link.href = `/film/${movie.id}`;
        card.querySelector('img').src = getPoster(movie);
        card.querySelector('img').alt = getTitle(movie);
        card.querySelector('h3').textContent = getTitle(movie);
        card.querySelector('.year').textContent = getYear(movie);
        card.querySelector('.rating').textContent = getRating(movie);
        card.querySelector('p').textContent = getShortDescription(movie);

        container.appendChild(clone);
    });
};

const renderPagination = (totalPages, currentPage) => {
    const pagination = document.querySelector('.pagination');
    pagination.innerHTML = '';

    const createBtn = (label, page, isActive = false) => {
        const btn = document.createElement('button');
        btn.className = 'pagination-btn';
        if (isActive) btn.classList.add('active');
        btn.textContent = label;
        btn.addEventListener('click', () => loadFilteredFilms(page));
        return btn;
    };

    if (currentPage > 1) {
        pagination.appendChild(createBtn('‹', currentPage - 1));
    }

    for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
        pagination.appendChild(createBtn(i, i, i === currentPage));
    }

    if (currentPage < totalPages) {
        pagination.appendChild(createBtn('›', currentPage + 1));
    }
};

const debounce = (fn, delay = 300) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
    };
};
