document.getElementById('user-form').addEventListener('submit', function (event) {
  event.preventDefault();
  var formData = new FormData(event.target);

  if (modalMode == "agregar") {
    agregarUsuario(formData)
  } else if (modalMode == "editar") {
    editarUsuario(formData, idActualizado)
  }

});

function editarUsuario(formData, user_id) {
  fetch("/users/edit/" + user_id, {
    method: 'POST',
    body: formData
  })
    .then(function (response) {
      if (!response.ok) {
        if (response.status >= 500) {
          showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
          console.error(error)
        } else if (response.status >= 400) {
          response.json()
            .then(function (formErrors) {
              setErrorsInForm(formErrors)
              showNotifications(response.status, "Error de usuario: Existen errores en tu formulario")
            });
        }
      } else {
        window.location.href = urlUsers;
      }
    })
    .catch(function (error) {
      showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
      console.error(error)
    });
}

function agregarUsuario(formData) {
  fetch(urlAgregarUsuario, {
    method: 'POST',
    body: formData
  })
    .then(function (response) {
      if (!response.ok) {
        if (response.status >= 500) {
          showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
          console.error(error)
        } else if (response.status >= 400) {
          response.json()
            .then(function (formErrors) {
              setErrorsInForm(formErrors)
              showNotifications(response.status, "Error de usuario: Existen errores en tu formulario")
            });
        }
      } else {
        window.location.href = urlUsers;
      }
    })
    .catch(function (error) {
      showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
      console.error(error)
    });
}
