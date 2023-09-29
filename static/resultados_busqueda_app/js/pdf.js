const generatePDFButton = document.getElementById("generate-pdf")
generatePDFButton.addEventListener("click", () => {
    const selectedData = table.getSelectedData();
    const ids = selectedData.map(item => item._id);
    const data = {
        selectedIds: ids,
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
            const pdfURL = URL.createObjectURL(pdf);
            window.open(pdfURL, '_blank');
            URL.revokeObjectURL(pdfURL)
        })
        .catch(error => {
            console.error(error);
        });








})

