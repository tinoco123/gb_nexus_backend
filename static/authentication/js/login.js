document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('btn-recuperar-contrasena').addEventListener('click', function (e) {
        e.preventDefault()
        var email = document.getElementById("email-recuperar-contrasena").value;
        if (validateEmail(email)) {
            document.getElementById('form-recuperar-contrasena').submit()
        }
    })
})

function validateEmail(email) {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
        return (true)
    }
    alert("Escribiste un email inválido")
    return (false)
}