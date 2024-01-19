const sendMailButon = document.getElementById("send-mail")

sendMailButon.addEventListener("click", async () => {
    try {
        const selectedData = table.getSelectedData();
        const ids = selectedData.map(item => item._id);
        const data = {
            selectedIds: ids,
            keyword: getKeyword()
        }
        var response = await fetch("/search-results/send-mail/", {method: "POST", headers: {"Content-Type": 'application/json', 'X-CSRFToken': getCSRFToken()}, body: JSON.stringify(data)})

        if (response.status === 200){
            showNotifications(response.status, "Email enviado correctamente")
        } else if (response.status === 400){
            var error = await response.json()
            showNotifications(response.status, error.error)
        }

    } catch (error) {
        console.log(error);
        showNotifications(500, "Error inesperado, intentelo más tarde")
    }


})