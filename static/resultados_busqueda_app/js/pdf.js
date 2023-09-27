const generatePDFButton = document.getElementById("generate-pdf")
generatePDFButton.addEventListener("click", () => {
    const selectedData = table.getSelectedData(); 
    const ids = selectedData.map(item => item._id);
    const data = {
        selectedIds: ids
    }

    fetch("/search-results/generate-pdf/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then((response) => {
            if (response.ok) {
                
            }
            else if (response.status >= 400 || response.status < 500) {
                response.json()
                    .then(() => {
                        showNotifications(response.status, "No se pudo generar el PDF con los resultados de búsqueda seleccionados")
                    })
                    .catch((error) => {
                        showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
                        console.error(error)
                    })
            }
        })
        .catch((error) => {
            showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
            console.error(error)
        })
})

