// Array of slideshow data
const slides = [
    {
        image: "{% static 'images/background1.svg' %}",
        backgroundColor: "#009b9d",
        title: "Welcome to Assur'Aimant"
    },
    {
        image: "{% static 'images/background2.svg' %}",
        backgroundColor: "#007b7d",
        title: "Your Health, Our Priority"
    },
    {
        image: "{% static 'images/background3.svg' %}",
        backgroundColor: "#005b5d",
        title: "Tailored Plans for Everyone"
    },
    {
        image: "{% static 'images/background4.svg' %}",
        backgroundColor: "#003b3d",
        title: "Secure Your Future Today"
    },
    {
        image: "{% static 'images/background5.svg' %}",
        backgroundColor: "#001b1d",
        title: "Assur'Aimant: Always With You"
    }
];

let currentSlideIndex = 0;

// Function to update the slideshow
function updateSlideshow() {
    const blurElement = document.getElementById("slideshow-blur");
    const imageElement = document.getElementById("slideshow-image");
    const textElement = document.getElementById("slideshow-text");

    // Get the current slide
    const currentSlide = slides[currentSlideIndex];

    // Update the background image and text
    blurElement.style.backgroundImage = `url('${currentSlide.image}')`;
    imageElement.style.backgroundImage = `url('${currentSlide.image}')`;
    textElement.textContent = currentSlide.title;

    // Update the index for the next slide
    currentSlideIndex = (currentSlideIndex + 1) % slides.length;
}

// Start the slideshow
setInterval(updateSlideshow, 5000); // Change slide every 5 seconds

// Initialize the first slide
updateSlideshow();