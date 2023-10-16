const informationIcons = document.querySelectorAll(".icon-condition");
informationIcons.forEach(icon => {
    icon.addEventListener("click", event => {
        if (removeContainerIfExists()){
            return true
        }
        var container = document.createElement("div")
        container.className = "box-conditions"

        var btnClose = document.createElement("button")
        btnClose.setAttribute('type', 'button')
        btnClose.setAttribute('aria-label', 'Close')
        btnClose.className = "btn-close"
        btnClose.id = "btnClose"

        btnClose.addEventListener("click", () => {
            container.remove()
        })

        container.appendChild(btnClose)

        var obligatorio = document.createElement("p")

        var tituloObligatorio = document.createElement("b")
        tituloObligatorio.textContent = "Obligatorio: "

        var descripcionObligatorio = document.createElement("span")
        descripcionObligatorio.textContent = "Keyword obligatoriamente incluida en el documento"

        obligatorio.appendChild(tituloObligatorio)
        obligatorio.appendChild(descripcionObligatorio)

        container.appendChild(obligatorio)

        var noObligatorio = document.createElement("p")

        var tituloNoObligatorio = document.createElement("b")
        tituloNoObligatorio.textContent = "No Obligatorio: "

        var descripcionNoObligatorio = document.createElement("span")
        descripcionNoObligatorio.textContent = "Keyword no incluida obligatoriamente en el documento. Se anexan resultados encontrados"

        noObligatorio.appendChild(tituloNoObligatorio)
        noObligatorio.appendChild(descripcionNoObligatorio)

        container.appendChild(noObligatorio)

        container.style.left = (event.clientX - 100) + "px"
        container.style.top = (event.clientY + 16) + "px"

        document.body.appendChild(container)
    })
})

function removeContainerIfExists() {
    const informationIcons = document.getElementsByClassName("box-conditions");
    if (informationIcons.length >= 1) {
        informationIcons[0].remove()
        return true
    } else {
        false
    }
}
