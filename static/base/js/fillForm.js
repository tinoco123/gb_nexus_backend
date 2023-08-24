function fillFormWithData(data, form) {
    for (let i = 0; i < form.elements.length; i++) {
        const field = form[i];
        if (field.getAttribute("name") === "password") {
            continue
        }
        if (field.tagName === 'INPUT' || field.tagName === "TEXTAREA" || field.tagName === "date") {
            if (field.id) {
                fieldName = field.getAttribute("name")
                field.value = data[fieldName]
            }
        }
        if (field.getAttribute("name") === "states_to_search") {
            var options = field.options
            for (var j = 0; j < options.length; j++) {
                if (data["states_to_search"].includes(options[j].text)) {
                    options[j].selected = true
                }
            }
        }
    }
}