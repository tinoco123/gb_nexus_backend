const pageSpan = document.getElementById("id-page")
const urlSpan = document.getElementById("id-url")
const stateSpan = document.getElementById("id-state")
const sinopsysSpan = document.getElementById("id-sinopsys")
const dateSpan = document.getElementById("id-date")
const zoneSpan = document.getElementById("id-zone")

const modalVerResultadosBusqueda = document.getElementById("modalVerResultadosBusqueda")

modalVerResultadosBusqueda.addEventListener('show.bs.modal', event => {
    setTimeout(() => {
        pageSpan.innerHTML = rowSelected.getData().title
        urlSpan.innerHTML = rowSelected.getData().urlPage
        urlSpan.setAttribute("href", rowSelected.getData().urlPage)
        stateSpan.innerHTML = rowSelected.getData().state
        dateSpan.innerHTML = rowSelected.getData().date
        zoneSpan.innerHTML = rowSelected.getData().federalEstatal
        getSinopsys()
            .then(data => {
                if (data) {
                    sinopsysSpan.innerHTML = data.sinopsys
                }
            });
    }, 1)
})

async function getSinopsys() {
    try {
        const searchResultId = rowSelected.getData()._id;
        const response = await fetch("/search-results/data/get/" + searchResultId, {
            method: "GET"
        });
        if (!response.ok) {
            throw new Error('Error en la petición al servidor');
        }
        const jsonData = await response.json();
        return jsonData
    } catch (error) {
        console.error('Error:', error);
    }
}