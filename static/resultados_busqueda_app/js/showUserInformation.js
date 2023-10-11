function showUserInformation(userData, event) {
    if (UserInfoContainerExists()) {
        document.getElementById("container-user-information").remove()
    }
    userData.first_name += ` ${userData.last_name}`
    delete userData.last_name

    var containerUserInformation = document.createElement("div")
    containerUserInformation.className = "user-information"
    containerUserInformation.id = "container-user-information"

    var btnClose = document.createElement("button")
    btnClose.setAttribute('type', 'button')
    btnClose.setAttribute('aria-label', 'Close')
    btnClose.className = "btn-close"
    btnClose.id = "btnClose"

    btnClose.addEventListener("click", () => {
        containerUserInformation.remove()
    })
    containerUserInformation.appendChild(btnClose)

    const keys = Object.keys(userData)
    const labels = ["Nombre: ", "Email: ", "Organización: ", "Último acceso: "]

    for (let i = 0; i < 4; i++) {
        var userInfo = document.createElement("p")
        var spanLabel = document.createElement("span")
        spanLabel.className = "spanLabelUserInfo"
        var spanText = document.createElement("span")

        spanLabel.textContent = labels[i]
        spanText.textContent = userData[keys[i]]

        userInfo.appendChild(spanLabel)
        userInfo.appendChild(spanText)
        containerUserInformation.appendChild(userInfo)
    }

    containerUserInformation.style.left = (event.clientX - 190) + "px"
    containerUserInformation.style.top = (event.clientY + 20) + "px"

    document.body.appendChild(containerUserInformation)


}

function UserInfoContainerExists() {
    const container = document.getElementById("container-user-information")
    if (container) {
        return container
    } else {
        false
    }
}