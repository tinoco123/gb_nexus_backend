const mailModal = document.getElementById("send-mail-modal")
const sendMailBtn = document.getElementById("send-mail-btn")
const sendMailForm = document.getElementById("send-mail-form")
const sendToMany = document.getElementById("send-to-more-people")
const sendToMyself = document.getElementById("send-mail-myself")
const recipientList = document.getElementById("recipient-list")
const closeMailsModalBtn = document.getElementById("close-mails-modal")


sendMailBtn.addEventListener("click", async () => {
    if (validateRadioOptionIsSelected()) {
        var response
        var ids = getDocumentsIds()
        if (sendToMyself.checked == true) {
            response = await sendRequestToBack(ids)
            if (response.status === 200) {
                closeMailsModalBtn.click()
                showNotifications(response.status, "Email enviado correctamente")
            } else if (response.status === 400) {
                var error = await response.json()
                showNotifications(response.status, error.error)
            }
        }
        else if (sendToMany.checked == true && recipientList.value != "") {
            var mails = getMailsFromInput()
            response = await sendRequestToBack(ids, mails)
            if (response.status === 200) {
                closeMailsModalBtn.click()
                showNotifications(response.status, "Email enviado correctamente")
            } else if (response.status === 400) {
                var error = await response.json()
                showNotifications(response.status, error.error)
            }
        }
        else {
            showNotifications(400, "Ingresa al menos un mail")
        }
    } else {
        showNotifications(400, "Selecciona una de las 2 opciones")
    }
})

function validateRadioOptionIsSelected() {

    if (sendToMyself.checked == false && sendToMany.checked == false) {
        return false
    }
    return true
}

function getMailsFromInput() {
    var rawMails = recipientList.value
    var mails = rawMails.split(",")
    return mails
}

function getDocumentsIds() {
    var selectedData = table.getSelectedData();
    var ids = selectedData.map(item => item._id);
    return ids
}

async function sendRequestToBack(documentIds, recipientList = null) {
    try {
        var data = {
            selected_ids: documentIds,
            keyword: getKeyword()
        }
        if (recipientList != null) {
            data = {
                selected_ids: documentIds,
                recipient_list: recipientList,
                keyword: getKeyword()
            }
        }

        var response = await fetch("/search-results/send-mail/", { method: "POST", headers: { "Content-Type": 'application/json', 'X-CSRFToken': getCSRFToken() }, body: JSON.stringify(data) })

        return response

    } catch (error) {
        console.log(error);
        showNotifications(500, "Error inesperado, intentelo más tarde")
    }
}