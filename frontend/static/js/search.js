const MIN_RATING = 0.0;
const MAX_RATING = 10.0;

const MIN_YEAR = 1980;
const MAX_YEAR = (new Date().getFullYear()) + 1;

const RATING_REGEX = /^[0-9]*\.?[0-9]*$/;
const YEAR_REGEX = /^\d+$/;

document.querySelectorAll('.filter-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-target');
        const target = document.getElementById(targetId);

        if (target) {
            target.classList.toggle('open');
            const arrow = btn.querySelector('.arrow');
            if (arrow) {
                arrow.classList.toggle('rotate');
            }
        }
    });
});

function validateInput(event, regex) {
    const value = event.target.value;

    if (!regex.test(value)) {
        event.target.value = value.slice(0, -1);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const ratingMinInput = document.getElementById('rating-min-input');
    const ratingMaxInput = document.getElementById('rating-max-input');
    const ratingMinSlider = document.getElementById('rating-min');
    const ratingMaxSlider = document.getElementById('rating-max');

    initRatingFilter()

    function validateRating(value) {
        return Math.min(Math.max(value, MIN_RATING), MAX_RATING);
    }

    function initRatingFilter() {
        ratingMinInput.value = MIN_RATING.toFixed(1);
        ratingMaxInput.value = MAX_RATING.toFixed(1);

        ratingMinSlider.min = MIN_RATING;
        ratingMinSlider.max = MAX_RATING;
        ratingMinSlider.value = MIN_RATING;

        ratingMaxSlider.min = MIN_RATING;
        ratingMaxSlider.max = MAX_RATING;
        ratingMaxSlider.value = MAX_RATING;
    }

    function updateRatingFromInput() {
        let minRating = parseFloat(ratingMinInput.value.trim()) || MIN_RATING;
        let maxRating = parseFloat(ratingMaxInput.value.trim()) || MAX_RATING;

        minRating = validateRating(minRating);
        maxRating = validateRating(maxRating);

        ratingMinSlider.value = minRating;
        ratingMaxSlider.value = maxRating;

        ratingMinInput.value = minRating.toFixed(1);
        ratingMaxInput.value = maxRating.toFixed(1);
    }

    function updateRatingFromSlider() {
        let minRating = parseFloat(ratingMinSlider.value) || MIN_RATING;
        let maxRating = parseFloat(ratingMaxSlider.value) || MAX_RATING;

        minRating = validateRating(minRating);
        maxRating = validateRating(maxRating);

        ratingMinInput.value = minRating.toFixed(1);
        ratingMaxInput.value = maxRating.toFixed(1);
    }

    ratingMinInput.addEventListener('input', function (event) {
        validateInput(event, RATING_REGEX);
    });
    ratingMaxInput.addEventListener('input', function (event) {
        validateInput(event, RATING_REGEX);
    });
    ratingMinInput.addEventListener('blur', function () {
        updateRatingFromInput();
    })
    ratingMaxInput.addEventListener('blur', function () {
        updateRatingFromInput();
    })
    ratingMinSlider.addEventListener('input', updateRatingFromSlider);
    ratingMaxSlider.addEventListener('input', updateRatingFromSlider);


    const yearMinInput = document.getElementById('year-min-input');
    const yearMaxInput = document.getElementById('year-max-input');
    const yearMinSlider = document.getElementById('year-min');
    const yearMaxSlider = document.getElementById('year-max');

    initYearFilter()

    function initYearFilter() {
        yearMinInput.min = MIN_YEAR;
        yearMinInput.max = MAX_YEAR;
        yearMinInput.value = MIN_YEAR;

        yearMaxInput.min = MIN_YEAR;
        yearMaxInput.max = MAX_YEAR;
        yearMaxInput.value = MAX_YEAR;

        yearMinSlider.min = MIN_YEAR;
        yearMinSlider.max = MAX_YEAR;
        yearMinSlider.value = MIN_YEAR;

        yearMaxSlider.min = MIN_YEAR;
        yearMaxSlider.max = MAX_YEAR;
        yearMaxSlider.value = MAX_YEAR;
    }

    function validateYear(value) {
        return Math.min(Math.max(value, MIN_YEAR), MAX_YEAR);
    }

    function updateYearFromInput() {
        let minYear = parseInt(yearMinInput.value.trim()) || MIN_YEAR;
        let maxYear = parseInt(yearMaxInput.value.trim()) || MAX_YEAR;

        minYear = validateYear(minYear);
        maxYear = validateYear(maxYear);

        yearMinSlider.value = minYear;
        yearMaxSlider.value = maxYear;

        yearMinInput.value = minYear;
        yearMaxInput.value = maxYear;
    }

    function updateYearFromSlider() {
        let minYear = parseInt(yearMinSlider.value);
        let maxYear = parseInt(yearMaxSlider.value);

        minYear = validateYear(minYear);
        maxYear = validateYear(maxYear);

        yearMinInput.value = minYear;
        yearMaxInput.value = maxYear;
    }

    yearMinInput.addEventListener('input', function (event) {
        validateInput(event, YEAR_REGEX);
    });
    yearMaxInput.addEventListener('input', function (event) {
        validateInput(event, YEAR_REGEX);
    });
    yearMinInput.addEventListener('blur', function () {
        updateYearFromInput();
    })
    yearMaxInput.addEventListener('blur', function () {
        updateYearFromInput();
    })
    yearMinSlider.addEventListener('input', updateYearFromSlider);
    yearMaxSlider.addEventListener('input', updateYearFromSlider);
});
