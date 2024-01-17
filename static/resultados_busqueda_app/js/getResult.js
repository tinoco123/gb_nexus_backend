const pageSpan = document.getElementById("id-page")
const urlSpan = document.getElementById("id-url")
const stateSpan = document.getElementById("id-state")
const sinopsysSpan = document.getElementById("id-sinopsys")
const dateSpan = document.getElementById("id-date")
const zoneSpan = document.getElementById("id-zone")
const moreInformationContainer = document.getElementById("information-container")
const footerMoreInformation = document.getElementById("footer-more-information")
const modalVerResultadosBusqueda = document.getElementById("modalVerResultadosBusqueda")

modalVerResultadosBusqueda.addEventListener('show.bs.modal', event => {
    setTimeout(() => {
        getSinopsys()
            .then(data => {
                if (data.urlAttach.length == 1) {
                    urlSpan.innerHTML = data.urlAttach[0].urlAttach
                    urlSpan.setAttribute("href", data.urlAttach[0].urlAttach)
                    if (data.urlAttach[0].sinopsys == "") {
                        footerMoreInformation.hidden = true
                    }else{
                        footerMoreInformation.hidden = false
                    }
                }else{
                    urlSpan.innerHTML = rowSelected.getData().urlPage
                    urlSpan.setAttribute("href", rowSelected.getData().urlPage)
                    if(data.urlAttach.length == 0){
                        footerMoreInformation.hidden = true
                    }else {
                        footerMoreInformation.hidden = false
                    }                    
                }
                pageSpan.innerHTML = rowSelected.getData().title                                
                stateSpan.innerHTML = rowSelected.getData().state
                dateSpan.innerHTML = rowSelected.getData().date
                zoneSpan.innerHTML = rowSelected.getData().federalEstatal
                sinopsysSpan.innerHTML = data.sinopsys
                moreInformationContainer.innerHTML = ""
                moreInformation(data, moreInformationContainer)
            });

    }, 1)
})

async function getSinopsys() {
    try {
        const params = new URLSearchParams()
        params.append('keyword', getKeyword())
        const searchResultId = rowSelected.getData()._id;
        const response = await fetch("/search-results/data/get/" + searchResultId + "?" + params.toString(), {
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

function moreInformation(data, container) {
    for (let i = 0; i < data.urlAttach.length; i++) {
        var url = data.urlAttach[i].urlAttach
        var sinopsys = data.urlAttach[i].sinopsys
        container.innerHTML += `
        <tr>
            <th scope="row" class="titulo-ver-mas">
                <i class="bi bi-link-45deg me-3"></i>
                URL
            </th>
            <td>
                <a href="${url}" target="_blank">${url}</a>
            </td>
        </tr>
            
        <tr>
            <th scope="row">
                <i class="bi bi-book me-3"></i>
                    Sinopsis
            </th>
            <td>
                <p>${sinopsys}</p>
            </td>
            </tr>
        `
    }
}