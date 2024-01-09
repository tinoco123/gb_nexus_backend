var actionIcons = function (cell, formatterParams) {
    var actionHTML = "<button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#edit-user-modal'><i class='bi bi-pen fs-5'></i></button> <button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#delete-user-modal'><i class='bi bi-trash fs-5'></i></button>"
    return actionHTML;
};

var table = new Tabulator("#userTable", {
    layout: "fitDataFill",
    pagination: true,
    paginationMode: "remote",
    ajaxURL: "/users/data/",
    paginationSize: 20,
    paginationSizeSelector: [20, 30, 40, 50],
    paginationCounter: "rows",
    height: 1000,
    placeholder: "Sin datos que mostrar",
    columns: [
        {
            formatter: "rowSelection", titleFormatter: "rowSelection", hozAlign: "center", headerHozAlign: "center", resizable: false, headerSort: false, cellClick: function (e, cell) {
                cell.getRow().toggleSelect();
            }
        },
        { title: "ID", field: "id", sorter: "number" },
        { title: "Nombre", field: "first_name" },
        { title: "Apellidos", field: "last_name" },
        { title: "Mail", field: "email" },
        { title: "Empresa", field: "company" },
        {
            title: "Último acceso", field: "last_login", sorter: "date", sorterParams: {
                format: "yyyy-MM-dd",
                alignEmptyValues: "top",
            }
        },
        {
            title: "Fecha de registro", field: "date_joined", sorter: "date", sorterParams: {
                format: "yyyy-MM-dd",
                alignEmptyValues: "top",
            }
        },
        { title: "Acciones", formatter: actionIcons, hozAlign: "center", headerHozAlign: "center", headerSort: false, width: 102, frozen: true },
    ],
});

var idActualizado = 0
var rowIndex = 0

table.on("rowClick", function (e, row) {
    idActualizado = row.getData().id
    rowIndex = row.getIndex()
});