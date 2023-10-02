var radioSelected = "my-keywords"
myKeywords = document.getElementById("my-keywords")
usuarioKeywords = document.getElementById("usuario-keywords")
clienteKeywords = document.getElementById("cliente-keywords")
var radios = [myKeywords, usuarioKeywords, clienteKeywords]

radios.forEach(radio => {
    if (radio) {
        radio.addEventListener("change", (event) => {
            if (radio.checked) {
                setRadioSelected(radio.id)
                event.preventDefault()
                table.setData("/keywords/data/", { keyword_type: getRadioSelected() })
                    .then(() => {
                        console.log(getRadioSelected());
                    })
                event.stopPropagation()
            }
        })
    }
})


function getRadioSelected() {
    return radioSelected
}

function setRadioSelected(valor) {
    radioSelected = valor
}