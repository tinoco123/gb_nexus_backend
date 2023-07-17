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

document.getElementById('user-form').addEventListener('submit', function (event) {

  event.preventDefault();
  var formData = new FormData(event.target);

  fetch('/users/create/', {
    method: 'POST',
    body: formData
  })
    .then(function (response) {
      if (!response.ok) {
        response.json()
          .then(function (formErrors) {
            setErrorsInForm(formErrors)
          });
      } else {
        window.location.href = "/users/"
      }
    })
    .catch(function (error) {
      console.error('Error:', error);
    });
});

