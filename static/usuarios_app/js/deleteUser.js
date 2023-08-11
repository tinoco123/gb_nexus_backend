// Popular modal eliminar usuario con información del usuario al abrir el modal
const spanNombreUsuario = document.getElementById("nombre-eliminar")
const spanMailUsuario = document.getElementById("mail-eliminar")
const eliminarUsuario = document.getElementById('eliminarUsuarioModal')
eliminarUsuario.addEventListener('shown.bs.modal', event => {
    var row = table.getRow(rowIndex)
    var nombreUsuario = row.getData().first_name
    spanNombreUsuario.innerHTML = nombreUsuario
})
