const generatePDFButton = document.getElementById("generate-pdf")
generatePDFButton.addEventListener("click", () => {
    const selectedData = table.getSelectedData();
    const ids = selectedData.map(item => item._id);
    const data = {
        selected_ids: ids,
        keyword: getKeyword()
    }

    fetch("/search-results/generate-pdf/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                response.json()
                    .then(error => {
                        showNotifications(response.status, error.error);
                    })
            } else {
                return response.blob();
            }
        })
        .then(pdf => {
            const pdfURL = URL.createObjectURL(pdf)
            const a = document.createElement('a')
            a.download = "Reporte.pdf"
            a.href = pdfURL
            a.target = '_self'
            a.click()
            URL.revokeObjectURL(pdfURL)
            a.remove()
        })
        .catch(error => {
            console.error(error);
        });








})

