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

function showNotifications(statusCode, message) {

  if (statusCode >= 500) {
    appendAlert(message, "danger")
  } else if (statusCode >= 400) {
    appendAlert(message, "warning")
  } else if (statusCode >= 200) {
    appendAlert(message, "info")
  }
}

function setErrorsInForm(formErrors, prefixErrorId="error_") {
  if (formErrors.success === false) {
    json_errors = JSON.parse(formErrors.errors)
    for (var error in json_errors) {
      if (json_errors.hasOwnProperty(error)) {
        errorName = error
        var listaErrores = json_errors[error];
        listaErrores.forEach(function (error) {
          id = prefixErrorId + errorName
          errorSpan = document.getElementById(id)
          errorSpan.innerHTML = error.message
        });
      }
    }
  }
}
