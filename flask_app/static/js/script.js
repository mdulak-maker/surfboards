const WEATHER_API_KEY = '72e9e59e3dd345f2763583c3ea554c63';

var windContainer = document.getElementById("wind-info");
var adviceContainer = document.getElementById("board-recommendation");

async function getWeather(lat, lon) {
    var response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=imperial&appid=${WEATHER_API_KEY}`);
    var data = await response.json();
    console.log(data);
    var windSpeed = data.wind.speed;
    windContainer.innerHTML = `The curren wind speed in San Francisco is: ${windSpeed} mph`;
    pageAdvice(windSpeed);
}

function pageAdvice(windSpeed) {
    if (windSpeed > 10) {
        adviceContainer.innerHTML = `At these speeds you can expect rough conditions for surfing. 
        Whether the wind is onshore or offshore, you may find it difficult to paddle into waves.
        For less than ideal conditions like these, we'd recommend a large board. For reference, if you're a novice 
        surfer who weighs around 160 lbs, please select a board with at least 40 liters of volume.`;
    } else {
        adviceContainer.innerHTML = `Wind speed is mild enough that any board should do today.`;
    }
}

getWeather(37.7749, -122.4194);
