document.addEventListener("click", function (e) {
    if (e.target !== containerUserInformation) {
        document.body.removeChild(containerUserInformation);
    }
})



function showUserInformation(userData, event) {
    
    var containerUserInformation = document.createElement("div")
    containerUserInformation.className = "user-information"
    containerUserInformation.id = "container-user-information"
    containerUserInformation.innerHTML += `
        
    `

    containerUserInformation.style.left = event.clientX + "px"
    containerUserInformation.style.top = event.clientY + "px"

    document.body.appendChild(containerUserInformation)

    
}