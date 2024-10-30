let stage = 'ask_occasion';
let occasion = null;
let intensity = null;
let eventLocation = null;
let eventDate = null;  
let eventSeason = null;
let eventWeather = null;
let gender = null;

document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM fully loaded and parsed");
    displayRecentReviews();

    displayMessage("Welcome to FragranceFitter. What is the event you are planning to attend?", "bot");
    displayOccasionButtons();  
    
    document.getElementById("send-btn").addEventListener("click", function() {
        if (stage === "ask_location_date") {
            getLocationAndDate();  
        } else {
            sendMessage();  
        }
    });
});

function displayOccasionButtons() {
    const occasions = ["Party", "Professional Event", "Casual Event", "Formal Event", "Sports Event", "Romantic", "Outdoor Event", "Religious Event"];
    createButtons(occasions, selectOccasion);
}

function displayIntensityButtons() {
    const intensities = ["Light", "Moderate", "Intense"];
    createButtons(intensities, selectIntensity);
}

function displayGenderButtons() {
    const genders = ["Male", "Female", "Unisex"];
    createButtons(genders, selectGender);
}

function createButtons(options, callback) {
    const messagesDiv = document.getElementById("messages");
    const buttonsDiv = document.createElement("div");

    buttonsDiv.classList.add("selection-buttons", "d-flex", "flex-wrap", "align-items-end", "mt-3");
    buttonsDiv.style.flexDirection = "row-reverse"; 
    buttonsDiv.style.maxWidth = "600px"; 
    buttonsDiv.style.justifyContent = "flex-end"; 

    options.forEach((option) => {
        const button = document.createElement("button");
        button.classList.add("btn", "btn-primary", "mb-2");
        button.style.fontSize = "12px";
        button.style.padding = "8px 14px";
        button.style.marginRight = "12px"; 
        button.textContent = option;
        button.onclick = () => callback(option);

        buttonsDiv.appendChild(button);
    });

    messagesDiv.appendChild(buttonsDiv);
}

function selectOccasion(selectedOccasion) {
    occasion = selectedOccasion;
    displayMessage(selectedOccasion, "user");
    displayMessage("Please select the perfume intensity.", "bot");
    displayIntensityButtons();  

    stage = "ask_intensity";  
}

function selectIntensity(selectedIntensity) {
    intensity = selectedIntensity;
    displayMessage(selectedIntensity, "user");
    displayMessage("Please provide the gender", "bot");
    displayGenderButtons();

    stage = "ask_gender";  
}

function selectGender(selectedGender) {
    gender = selectedGender;
    displayMessage(selectedGender, "user");
    displayMessage("Please provide the location and date of the event.", "bot");

    stage = "ask_location_date";  
    sendMessage();
}

function getLocationAndDate() {
    const input = document.getElementById("userInput").value.trim();
    displayMessage(input, "user");
    
    sendMessage(); 
    
    document.getElementById("userInput").value = "";    
}

function sendMessage() {
    const userMessage = document.getElementById("userInput").value;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            message: userMessage,  
            stage: stage,
            occasion: occasion,
            intensity: intensity,
            location: eventLocation, 
            date: eventDate,         
            season: eventSeason,
            weather: eventWeather,
            gender: gender
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("Received response:", data);
        if (data.recommended_perfume) {
            displayMessage(data.bot_message, "bot", data.recommended_perfume);
        } else {
            displayMessage(data.bot_message, "bot");
        }
    })
    
    .catch((error) => {
        console.error("Error:", error);
    });

    document.getElementById("userInput").value = ""; // Clear input after sending
}


function displayMessage(message, sender, perfume = null) {
    const messagesDiv = document.getElementById("messages");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender, "d-flex", "align-items-center", "mb-3");

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("content", "p-3", "rounded");

    contentDiv.textContent = message;

    messageDiv.appendChild(contentDiv);
    messagesDiv.appendChild(messageDiv);

    if (perfume) {
        const perfumeDiv = document.createElement("div");
        perfumeDiv.classList.add("perfume", "mt-3", "p-3", "border", "rounded", "d-flex", "flex-column");
    
        const perfumeName = document.createElement("h5");
        perfumeName.classList.add("mb-3");
        perfumeName.textContent = perfume.name;
        perfumeName.style.color = "#333";
    
        const divInner1 = document.createElement("div");
        divInner1.classList.add("d-flex", "align-items-center");
    
        const divInner2 = document.createElement("div");
        divInner2.classList.add("ms-3");
    
        const perfumeImage = document.createElement("img");
        perfumeImage.src = perfume.image_url;
        perfumeImage.alt = perfume.name;
        perfumeImage.classList.add("img-fluid", "rounded");
        perfumeImage.style.width = "150px";
        perfumeImage.style.height = "200px";
    
        const perfumeBrand = document.createElement("p");
        perfumeBrand.classList.add("mb-1");
        perfumeBrand.textContent = "Brand: " + perfume.brand;
        perfumeBrand.style.color = "#333";
    
        const perfumeDescription = document.createElement("p");
        perfumeDescription.classList.add("mb-4");
        perfumeDescription.textContent = perfume.description;
        perfumeDescription.style.color = "#333";

        const showReviewButton = document.createElement("button");
        showReviewButton.classList.add("btn", "btn-primary");
        showReviewButton.textContent = "Show Reviews";
        showReviewButton.onclick = () => showReviewsPane(perfume.name);

        divInner2.appendChild(perfumeBrand);
        divInner2.appendChild(perfumeDescription);
        divInner2.appendChild(showReviewButton);
    
        divInner1.appendChild(perfumeImage);
        divInner1.appendChild(divInner2);
    
        perfumeDiv.appendChild(perfumeName);
        perfumeDiv.appendChild(divInner1);
    
        messagesDiv.appendChild(perfumeDiv);
    }

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}






// Search for perfumes
function searchPerfume() {
    const searchInput = document.getElementById("searchInput");
    const searchQuery = searchInput.value.trim();
    if (searchQuery === "") {
        clearDropdown();
        return;
    }

    console.log("Searching for perfume:", searchQuery);
    fetch("/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ perfume_name: searchQuery }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("Search results:", data);
        displayDropdownResults(data.results);
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}

function displayDropdownResults(results) {
    const dropdown = document.getElementById("dropdown");
    dropdown.innerHTML = ""; // Clear previous results

    if (results.length === 0) {
        dropdown.style.display = "none";
        return;
    }

    results.forEach((result) => {
        const resultDiv = document.createElement("div");
        resultDiv.classList.add("dropdown-item");
        resultDiv.textContent = result.name;
        resultDiv.onclick = () => selectPerfume(result);

        dropdown.appendChild(resultDiv);
    });

    dropdown.style.display = "block";
}

function selectPerfume(perfume) {
    const searchInput = document.getElementById("searchInput");
    searchInput.value = perfume.name;
    clearDropdown();
    displaySearchResults([perfume]);
}

function clearDropdown() {
    const dropdown = document.getElementById("dropdown");
    dropdown.innerHTML = "";
    dropdown.style.display = "none";
}

function displaySearchResults(results) {
    const searchResultsDiv = document.getElementById("searchResults");
    searchResultsDiv.innerHTML = ""; // Clear previous results

    if (results.length === 0) {
        searchResultsDiv.textContent = "No results found.";
        return;
    }

    results.forEach((result) => {
        const resultDiv = document.createElement("div");
        resultDiv.classList.add("search-result", "p-3", "mb-3", "d-flex", "align-items-center");

        const perfumeImage = document.createElement("img");
        perfumeImage.src = result.image_url;
        perfumeImage.alt = result.name;
        perfumeImage.classList.add("me-3");

        const resultDivInner = document.createElement("div");

        const perfumeName = document.createElement("h5");
        perfumeName.textContent = result.name;

        const perfumeBrand = document.createElement("p");
        perfumeBrand.textContent = "Brand: " + result.brand;

        const addReviewButton = document.createElement("button");
        addReviewButton.classList.add("btn");
        addReviewButton.textContent = "Add Review";
        addReviewButton.classList.add("btn", "btn-primary");
        addReviewButton.setAttribute("data-bs-toggle", "modal");
        addReviewButton.setAttribute("data-bs-target", "#reviewModal");
        addReviewButton.onclick = () => showReviewModal(result.name);

        resultDivInner.appendChild(perfumeName);
        resultDivInner.appendChild(perfumeBrand);
        resultDivInner.appendChild(addReviewButton);

        resultDiv.appendChild(perfumeImage);
        resultDiv.appendChild(resultDivInner);

        searchResultsDiv.appendChild(resultDiv);
    });
}

function showReviewModal(perfumeName) {
    const perfumeNameInput = document.getElementById('perfumeName');
    perfumeNameInput.value = perfumeName;
}

function saveReview() {
    const perfumeName = document.getElementById("perfumeName").value.trim();
    const userName = document.getElementById("user-name").value.trim();
    const reviewText = document.getElementById("review_text").value.trim(); 

    console.log("Saving review:", { perfumeName, userName, reviewText });
    fetch("/add_review", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ perfume_name: perfumeName, user_name: userName, review: reviewText }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("Review saved:", data);
        displayThankYouMessage();
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}


function displayRecentReviews() {
    fetch("/recent_reviews")
    .then((response) => response.json())
    .then((data) => {
        console.log("Recent reviews:", data);
        const recentReviewsDiv = document.getElementById("recentReviewsContent");
        recentReviewsDiv.innerHTML = ""; 

        data.reviews.forEach((review) => {
            // Create main review container
            const reviewDiv = document.createElement("div");
            reviewDiv.classList.add("review", "mb-3", "p-3", "gray-400-bg");

            // const hrDiv = document.createElement("hr");

            // Create container for user and date details
            const userDetailDiv = document.createElement("div");
            userDetailDiv.classList.add("d-flex", "justify-content-between", "mb-2");

            const reviewUser = document.createElement("p");
            reviewUser.textContent = "By: " + review.user_name;
            reviewUser.classList.add("fw-bold");

            const reviewAddedDate = document.createElement("p");
            reviewAddedDate.textContent = review.date_posted;
            reviewAddedDate.classList.add("text-muted", "fs-6");

            userDetailDiv.appendChild(reviewUser);
            userDetailDiv.appendChild(reviewAddedDate);

            // Create container for perfume name and image
            const perfumeDetailDiv = document.createElement("div");
            perfumeDetailDiv.classList.add("d-flex", "align-items-start", "mb-2");

            const perfumeImage = document.createElement("img");
            perfumeImage.src = review.image_url;
            perfumeImage.alt = review.perfume_name;
            perfumeImage.classList.add("me-3", "rounded");
            perfumeImage.style.width = "80px";
            perfumeImage.style.height = "80px";

            const perfumeName = document.createElement("h5");
            perfumeName.textContent = review.perfume_name;
            perfumeName.classList.add("mb-0", "text-dark");

            perfumeDetailDiv.appendChild(perfumeImage);
            perfumeDetailDiv.appendChild(perfumeName);

            // Create container for review text
            const reviewTextDiv = document.createElement("div");
            reviewTextDiv.classList.add("mt-2");

            const reviewText = document.createElement("p");
            reviewText.textContent = review.review;
            reviewText.classList.add("text-secondary", "mb-1");

            reviewTextDiv.appendChild(reviewText);

            // Assemble all parts into the main review div
            reviewDiv.appendChild(userDetailDiv);
            reviewDiv.appendChild(perfumeDetailDiv);
            reviewDiv.appendChild(reviewTextDiv);
            // reviewDiv.appendChild(hrDiv);

            // Add the complete reviewDiv to the main container
            recentReviewsDiv.appendChild(reviewDiv);
        });
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}



function displayThankYouMessage() {
    const modalBody = document.querySelector("#reviewModal .modal-content");
    modalBody.innerHTML = `
        <div class="thank-you-message">
            <h5>Thank you for sharing your experience!</h5>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button>
        </div>
    `;
}

document.getElementById('reviewForm').addEventListener('submit', function(event) {
    event.preventDefault();
    saveReview();
});






function showReviewsPane(perfumeName) {
    // Fetch reviews for the selected perfume
    fetch(`/show_reviews?perfume_name=${encodeURIComponent(perfumeName)}`)
    .then(response => response.json())
    .then(data => {
        const reviewsPane = document.getElementById('reviewsPane');
        const reviewsContent = document.getElementById('reviewsContent');
        reviewsContent.innerHTML = ''; // Clear previous reviews

        if (data.reviews.length === 0) {
            reviewsContent.innerHTML = '<p>No reviews available.</p>';
        } else {
            data.reviews.forEach(review => {
                const reviewDiv = document.createElement('div');
                reviewDiv.classList.add('review', 'mb-3');
                reviewDiv.innerHTML = `
                    <h6>${review.user_name}</h6>
                    <p>${review.review}</p>
                `;
                reviewsContent.appendChild(reviewDiv);
            });
        }

        reviewsPane.classList.add('active');
    })
    .catch(error => {
        console.error('Error fetching reviews:', error);
    });
}

function closeReviewsPane() {
    const reviewsPane = document.getElementById('reviewsPane');
    reviewsPane.classList.remove('active');
}
