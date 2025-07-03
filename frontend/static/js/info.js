function scrollCarousel(direction) {
    const carousel = document.getElementById('actor-carousel');
    const cardWidth = carousel.querySelector('.actor-card').offsetWidth + 16;
    carousel.scrollBy({
        left: direction * cardWidth * 2,
        behavior: 'smooth'
    });
}