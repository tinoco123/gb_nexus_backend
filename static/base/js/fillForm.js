function fillFormWithData(data, form) {
    for (let i = 0; i < form.elements.length; i++) {
        const field = form[i];
        if (field.getAttribute("name") === "password") {
            continue
        }
        if (field.getAttribute("type") === 'text' || field.tagName === "TEXTAREA" || field.tagName === "date") {
            if (field.id) {
                fieldName = field.getAttribute("name")
                field.value = data[fieldName]
            }
        }
        if (field.getAttribute("name") == "congreso_search") {
            data["congreso_search"].forEach(idState => {
                if (idState == field.value) field.checked = true;
            })
        }
    }
}
