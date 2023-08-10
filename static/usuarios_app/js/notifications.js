const notificationContainer = document.getElementById('notificationContainer');

const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  notificationContainer.append(wrapper)
  setTimeout(function () {
    wrapper.remove();
  }, 5000);
}

function mostrarNotificacion(statusCode) {

  if (statusCode >= 500) {
    appendAlert("Error en el servidor, el usuario no se pudo agregar", "danger")
  } else if (statusCode >= 400) {
    appendAlert("Error al procesar tu solicitud, el usuario no se pudo agregar", "danger")
  }
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
