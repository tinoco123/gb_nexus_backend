var actionIcons = function (cell, formatterParams) {
    var actionHTML = "<button class='btn p-2' data-bs-toggle='modal' data-bs-target='#editarUsuario'><i class='bi bi-pen fs-5'></i></button> <button class='btn p-2' data-bs-toggle='modal' data-bs-target='#eliminarUsuario'><i class='bi bi-trash fs-5'></i></button>"
    return actionHTML;
};

var tableData = []

var table = new Tabulator("#userTable", {
    layout: "fitDataStretch",
    data: tableData,
    pagination: true,
    paginationSize: 5,
    paginationSizeSelector: [10, 20, 30, 40, 50, true],
    paginationCounter: "rows",
    placeholder:"Sin datos que mostrar",
    columns: [
        {
            formatter: "rowSelection", titleFormatter: "rowSelection", hozAlign: "center", headerHozAlign: "center", resizable: false, headerSort: false, cellClick: function (e, cell) {
                cell.getRow().toggleSelect();
            }
        },
        { title: "ID", field: "id", sorter: "number" },
        { title: "Nombre", field: "name" },
        { title: "Apellidos", field: "lastname" },
        { title: "Empresa", field: "empresa" },
        { title: "Fecha de registro", field: "date"},
        { title: "Acciones", formatter: actionIcons, width: 107, hozAlign: "center", headerHozAlign: "center", headerSort: false },
    ],
});