function scrollCarousel(direction) {
    const carousel = document.getElementById('actor-carousel');
    const cardWidth = carousel.querySelector('.actor-card').offsetWidth + 16;
    carousel.scrollBy({
        left: direction * cardWidth * 2,
        behavior: 'smooth'
    });
}

document.addEventListener("DOMContentLoaded", async () => {
    const movieId = extractIdFromURL();
    if (movieId) {
        const data = await fetchFilmData(movieId);
        if (!data) throw new Error("Пустые данные");

        setFilmInfo(data);
    }
});

function extractIdFromURL() {
    const parts = window.location.pathname.split("/");
    const id = parts.pop() || parts.pop();
    return id || null;
}

async function fetchFilmData(id) {
    const res = await fetch(`/api/films/${id}`);
    const json = await res.json();
    return json.data;
}

function setText(selector, text) {
    const el = document.querySelector(selector);
    if (el) el.textContent = text;
}

function capitalize(word) {
    return typeof word === "string" && word.length > 0
        ? word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
        : "";
}

function setFilmInfo(data) {
    setText("h1", data.title || "Без названия");
    setText("#rating-value", formatRating(data.rating));
    setText("#duration", formatDuration(data.duration));
    setText("#year", data.year || "");
    setText("#country", formatCountries(data.countries));
    setText("#genres", formatGenres(data.genres));
    setText("#movie-description", data.description || "");

    setTrailerButton(data.trailers);
    setPosterImage(data.media);
    renderActors(data.film_people);
}

function formatRating(rating) {
    const parsed = parseFloat(rating);
    return !isNaN(parsed) ? parsed.toFixed(1) : "—";
}

function formatDuration(duration) {
    if (!duration || typeof duration !== "number") return "";

    const hours = Math.floor(duration / 60);
    const minutes = duration % 60;

    const hoursStr = hours > 0 ? `${hours} ч` : "";
    const minutesStr = minutes > 0 ? `${minutes} м` : "";

    return [hoursStr, minutesStr].filter(Boolean).join(" ");
}

function formatCountries(countries) {
    return Array.isArray(countries)
        ? countries.map(c => c.name).join(", ")
        : "";
}

function formatGenres(genres) {
    return Array.isArray(genres)
        ? genres
              .map(g => capitalize(g.name))
              .join(", ")
        : "";
}

function setTrailerButton(trailers = []) {
    const button = document.querySelector(".show-trailer-btn");
    if (!button || !Array.isArray(trailers)) return;

    const uniqueTrailers = [];
    const seenUrls = new Set();

    for (const trailer of trailers) {
        if (trailer.full_url && !seenUrls.has(trailer.full_url)) {
            seenUrls.add(trailer.full_url);
            uniqueTrailers.push(trailer);
        }
    }

    const trailerUrl = uniqueTrailers[0]?.full_url;

    if (trailerUrl) {
        button.addEventListener("click", () => {
            window.open(trailerUrl, "_blank");
        });
        button.disabled = false;
    } else {
        button.disabled = true;
    }
}

function setPosterImage(media) {
    if (Array.isArray(media)) {
        const poster = media.find(item => item.type === 'poster' && item.full_url);
        if (!poster) return;

        const asideImg = document.querySelector("aside img");
        if (asideImg) {
            asideImg.src = `${poster.full_url}/400x600`; // или без суффикса, если не нужен
            asideImg.alt = "Постер фильма";
        }
    }
}

function renderActors(filmPeople = []) {
    const carousel = document.getElementById("actor-carousel");
    const template = document.querySelector("template");

    if (!carousel || !template) return;

    filmPeople.forEach(actor => {
        const person = actor.person;
        if (
            !person ||
            !person.first_name?.trim() ||
            !person.last_name?.trim() ||
            !person.full_url?.trim()
        ) {
            return; // пропускаем, если данных недостаточно
        }

        const clone = template.content.cloneNode(true);
        const img = clone.querySelector("img");
        const name = clone.querySelector("h3");
        const role = clone.querySelector("p");

        img.src = person.full_url;
        img.alt = `${person.first_name} ${person.last_name}`;
        name.textContent = `${person.first_name} ${person.last_name}`;
        role.textContent = actor.character_name || "";

        carousel.appendChild(clone);
    });
}
