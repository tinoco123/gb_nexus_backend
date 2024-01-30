var customFrequencyRadio = document.getElementById("custom-frequency")
var dailyRadio = document.getElementById("daily")
var weeklyRadio = document.getElementById("weekly")
var customFrequencyContainer = document.getElementById("custom-frequency-container")
var customDayFrequency = document.getElementById("custom-day-frequency")

customFrequencyRadio.addEventListener("click", () => {
    customFrequencyContainer.classList.remove("d-none")
    customFrequencyContainer.classList.add("d-inline-flex")
    customDayFrequency.setAttribute("required", "required")
})

dailyRadio.addEventListener("click", () => {
    customFrequencyContainer.classList.remove("d-inline-flex")
    customFrequencyContainer.classList.add("d-none")
    customDayFrequency.removeAttribute("required")
})

weeklyRadio.addEventListener("click", () => {
    customFrequencyContainer.classList.remove("d-inline-flex")
    customFrequencyContainer.classList.add("d-none")
    customDayFrequency.removeAttribute("required")
})

setTimeout(function () {
    var messagesElement = document.getElementById('messages');
    if (messagesElement) {
        messagesElement.style.display = 'none';
    }
}, 3000);