/**
 * Weather & Regional News App Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    /* --- WEATHER PAGE LOGIC --- */
    const searchWeatherBtn = document.getElementById('search-weather-btn');
    const cityInput = document.getElementById('city-input');
    
    if (searchWeatherBtn && cityInput) {
        // Handle search button click
        searchWeatherBtn.addEventListener('click', () => {
            const city = cityInput.value.trim();
            if (city) {
                fetchWeather(city);
            }
        });

        // Handle Enter key press
        cityInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const city = cityInput.value.trim();
                if (city) {
                    fetchWeather(city);
                }
            }
        });
    }

    /* --- NEWS PAGE LOGIC --- */
    const searchNewsBtn = document.getElementById('search-news-btn');
    const countrySelect = document.getElementById('country-select');

    if (searchNewsBtn && countrySelect) {
        searchNewsBtn.addEventListener('click', () => {
            const country = countrySelect.value;
            fetchNews(country);
        });
    }
});

/**
 * Fetch weather data from backend API
 */
async function fetchWeather(city) {
    const loader = document.getElementById('weather-loader');
    const errorMsg = document.getElementById('weather-error');
    const resultCard = document.getElementById('weather-result');

    // Reset UI
    loader.classList.remove('hidden');
    errorMsg.classList.add('hidden');
    resultCard.classList.add('hidden');

    try {
        const response = await fetch(`/api/weather/${encodeURIComponent(city)}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch weather data.');
        }

        // Update UI with Data
        document.getElementById('w-city').textContent = data.city;
        document.getElementById('w-desc').textContent = data.description;
        document.getElementById('w-temp-val').textContent = data.temperature;
        document.getElementById('w-humidity').textContent = data.humidity + '%';
        document.getElementById('w-wind').textContent = data.wind_speed + ' m/s';
        
        // Construct icon URL
        document.getElementById('w-icon').src = `https://openweathermap.org/img/wn/${data.icon}@4x.png`;

        resultCard.classList.remove('hidden');

    } catch (error) {
        errorMsg.textContent = error.message;
        errorMsg.classList.remove('hidden');
    } finally {
        loader.classList.add('hidden');
    }
}

/**
 * Fetch news data from backend API
 */
async function fetchNews(countryCode) {
    const loader = document.getElementById('news-loader');
    const errorMsg = document.getElementById('news-error');
    const grid = document.getElementById('news-grid');

    // Reset UI
    loader.classList.remove('hidden');
    errorMsg.classList.add('hidden');
    grid.classList.add('hidden');
    grid.innerHTML = ''; // Clear previous news

    try {
        const response = await fetch(`/api/news/${encodeURIComponent(countryCode)}`);
        const articles = await response.json();

        if (!response.ok) {
            throw new Error(articles.error || 'Failed to fetch news data.');
        }

        if (!Array.isArray(articles) || articles.length === 0) {
            throw new Error('No news articles found for this region.');
        }

        // Populate grid
        articles.forEach((article, index) => {
            const card = document.createElement('div');
            card.className = 'news-card fade-in';
            card.style.animationDelay = `${index * 0.1}s`; // Staggered animation
            
            card.innerHTML = `
                <div class="news-image">
                    <img src="${article.image}" alt="News Image" onerror="this.src='https://via.placeholder.com/400x200?text=No+Image'">
                </div>
                <div class="news-content">
                    <span class="news-source">${article.source}</span>
                    <h3 class="news-title">${article.title}</h3>
                    <p class="news-desc">${article.description}</p>
                    <div style="margin-top: auto;">
                        <a href="${article.url}" target="_blank" rel="noopener noreferrer" class="read-more">
                            Read Full Story <i class="fa-solid fa-arrow-right"></i>
                        </a>
                    </div>
                </div>
            `;
            grid.appendChild(card);
        });

        grid.classList.remove('hidden');

    } catch (error) {
        errorMsg.textContent = error.message;
        errorMsg.classList.remove('hidden');
    } finally {
        loader.classList.add('hidden');
    }
}
