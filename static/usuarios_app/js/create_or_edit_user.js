document.getElementById('user-form').addEventListener('submit', function (event) {
  event.preventDefault();
  var formData = new FormData(event.target);

  if (modalMode == "agregar") {
    agregarUsuario(formData)
  } else if (modalMode == "editar") {
    console.log("Sin implementar");
  }

});

function agregarUsuario(formData) {
  fetch(urlAgregarUsuario, {
    method: 'POST',
    body: formData
  })
    .then(function (response) {
      if (!response.ok) {
        if (response.status >= 500) {
          mostrarNotificacion(response.status)
        } else if (response.status >= 400) {
          mostrarNotificacion(response.status)
        } else {
          response.json()
            .then(function (formErrors) {
              setErrorsInForm(formErrors)
            });
        }
      } else {
        window.location.href = urlUsers;
        mostrarNotificacion(response.status);
      }
    })
    .catch(function (error) {
      console.error('Error:', error);
    });
}

function setErrorsInForm(formErrors) {
  if (formErrors.success === false) {
    json_errors = JSON.parse(formErrors.errors)
    for (var error in json_errors) {
      if (json_errors.hasOwnProperty(error)) {
        errorName = error
        var listaErrores = json_errors[error];
        listaErrores.forEach(function (error) {
          id = "error_" + errorName
          errorSpan = document.getElementById(id)
          errorSpan.innerHTML = error.message
        });
      }
    }
  }
}