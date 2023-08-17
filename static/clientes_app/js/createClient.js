const createClientForm = document.getElementById("create-client-form")
createClientForm.addEventListener("submit", (event) => {
    event.preventDefault()
    var formData = new FormData(event.target)
    fetch("/clients/create/", {
        method: "POST",
        body: formData
    })
    .then((response) => {
        if (response.ok){
            window.location.href = "/clients";
        }
        else if (response.status >= 400 || response.status < 500 ){
            response.json()
            .then((errors) => {
                console.log("error: " + errors);
            })
        }
    })
    .catch((error) => {
        console.log("Error en el servidor: " + error);
    })
})