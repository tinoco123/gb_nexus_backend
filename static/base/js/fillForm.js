function fillFormWithData(data, form) {
    for (let i = 0; i < form.elements.length; i++) {
        const field = form[i];
        if (field.tagName === 'INPUT' || field.tagName === "TEXTAREA" || field.tagName === "date") {
            if (field.id) {
                fieldName = field.getAttribute("name")
                field.value = data[fieldName]
            }
        }
    }
}