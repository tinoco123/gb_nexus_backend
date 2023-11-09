document.addEventListener("DOMContentLoaded", () => {
    const statesDivs = document.querySelectorAll(".states")
    for (let i = 0; i < statesDivs.length; i++) {
        var statesDiv = statesDivs[i]
        var states = Array.from(statesDiv.children)
        var parte1 = states.slice(0, 5)
        var parte2 = states.slice(5, 10)
        var parte3 = states.slice(10, 15)
        var parte4 = states.slice(15, 20)
        var parte5 = states.slice(20, 25)
        var parte6 = states.slice(25, 30)
        var parte7 = states.slice(30)
        statesDiv.appendChild(createDivWithStates(parte1))
        statesDiv.appendChild(createDivWithStates(parte2))
        statesDiv.appendChild(createDivWithStates(parte3))
        statesDiv.appendChild(createDivWithStates(parte4))
        statesDiv.appendChild(createDivWithStates(parte5))
        statesDiv.appendChild(createDivWithStates(parte6))
        statesDiv.appendChild(createDivWithStates(parte7))
    }

    setTimeout(() => {
        var redirectButtons = document.getElementsByClassName("redirect")
        for (let i = 0; i < redirectButtons.length; i++) {
            const redirectButton = redirectButtons[i];
            redirectButton.addEventListener("click", () => {
                window.location.href = `/search-results?keyword=${idActualizado}`
            })
        }
    }, 1)
})


function createDivWithStates(states) {
    var newContainer = document.createElement("div")
    newContainer.className = "d-flex flex-column"
    states.forEach(state => {
        newContainer.appendChild(state)
    })
    return newContainer
}