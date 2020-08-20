const track = document.querySelector(".carouselTrack");
const slides = Array.from(track.children);
const prevButton = document.querySelector(".carouselButtonLeft");
const nextButton = document.querySelector(".carouselButtonRight");
const dotsNav = document.querySelector(".carouselNav");
const dots = Array.from(dotsNav.children);

var slideWidth = slides[0].getBoundingClientRect().width;

// Arrange the slides next to one another
slides[0].style.left = 0;
slides[1].style.left = slideWidth;

const setSlidePosition = (slide, index) =>
{
    slide.style.left = slideWidth * index + "px";
}
slides.forEach(setSlidePosition);

// Change slide width when user resize the window.
function setSlide()
{
    slideWidth = slides[0].getBoundingClientRect().width;
    slides.forEach(setSlidePosition);
}
window.addEventListener("resize", setSlide);

const moveToSlide = (track, currentSlide, targetSlide) =>
{
    track.style.transform = "translateX(-" + targetSlide.style.left + ")";
    currentSlide.classList.remove("currentSlide");
    targetSlide.classList.add("currentSlide");
}

const updateDots = (currentDot, targetDot) =>
{
    currentDot.classList.remove("currentSlide");
    targetDot.classList.add("currentSlide");
}

// Auto change photo every 3 seconds.
window.setInterval(autoNext, 5000);
function autoNext()
{
    const currentSlide = track.querySelector(".currentSlide");
    const nextSlide = currentSlide.nextElementSibling;
    const currentDot = dotsNav.querySelector(".currentSlide");
    const nextDot = currentDot.nextElementSibling;

    if (nextSlide)
    {
        moveToSlide(track, currentSlide, nextSlide);
        updateDots(currentDot, nextDot);
    }
    else // If currentSlide is the last one, target is the first one.
    {
        moveToSlide(track, currentSlide, slides[0]);
        updateDots(currentDot, dots[0]);
    }
}

// Click left, move slides to the left
prevButton.addEventListener("click", e => 
{
    const currentSlide = track.querySelector(".currentSlide");
    const prevSlide = currentSlide.previousElementSibling;
    const currentDot = dotsNav.querySelector(".currentSlide");
    const prevDot = currentDot.previousElementSibling;

    if (prevSlide)
    {
        moveToSlide(track, currentSlide, prevSlide);
        updateDots(currentDot, prevDot);
    }
    else // If currentSlide is the first one, target is the last one.
    {
        const targetIndex = slides.length -1;
        moveToSlide(track, currentSlide, slides[targetIndex]);
        updateDots(currentDot, dots[targetIndex]);
    }
})


// Click rught, move slides to the right
nextButton.addEventListener("click", e =>
{
    const currentSlide = track.querySelector(".currentSlide");
    const nextSlide = currentSlide.nextElementSibling;
    const currentDot = dotsNav.querySelector(".currentSlide");
    const nextDot = currentDot.nextElementSibling;

    if (nextSlide)
    {
        moveToSlide(track, currentSlide, nextSlide);
        updateDots(currentDot, nextDot);
    }
    else // If currentSlide is the last one, target is the first one.
    {
        moveToSlide(track, currentSlide, slides[0]);
        updateDots(currentDot, dots[0]);
    }
})


// Click the nav indicators, move to that img

dotsNav.addEventListener("click", e =>
{
    // Which indicator was clicked?
    const targetDot = e.target.closest("button");

    if (!targetDot) return;

    const currentSlide = track.querySelector(".currentSlide");
    const currentDot = dotsNav.querySelector(".currentSlide");
    const targetIndex = dots.findIndex(dot => dot === targetDot);
    const targetSlide = slides[targetIndex];

    moveToSlide(track, currentSlide, targetSlide);
    updateDots(currentDot, targetDot);
})