var actionIcons = function (cell, formatterParams) {
    var actionHTML = "<button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#userModal'><i class='bi bi-pen fs-5'></i></button> <button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#eliminarUsuario'><i class='bi bi-trash fs-5'></i></button>"
    return actionHTML;
};

var table = new Tabulator("#userTable", {
    layout: "fitDataFill",
    data: usuarios,
    pagination: true,
    paginationSize: 10,
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
        { title: "Nombre", field: "first_name" },
        { title: "Apellidos", field: "last_name" },
        { title: "Empresa", field: "company" },
        { title: "Fecha de registro", field: "date_joined"},
        { title: "Acciones", formatter: actionIcons, hozAlign: "center", headerHozAlign: "center", headerSort: false, width:102 },
    ],
});