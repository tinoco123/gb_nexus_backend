function fillFormWithData(data, form) {
    if (data.search_terms) {
        search_terms_length = data.search_terms.length
        if (search_terms_length >= 1) {
            for (let index = 0; index < search_terms_length; index++) {
                form.elements[`id_search_term_${index + 1}`].value = data.search_terms[index].name
                form.elements[`filter_${index + 1}`].selectedIndex = data.search_terms[index].is_required ? 0 : 1

            }
        }
    }

    for (let i = 0; i < form.elements.length; i++) {
        const field = form[i];
        if (field.id.startsWith('id_search_term_') || field.getAttribute("type") === 'SELECT' || field.getAttribute("name") === "password") {
            continue
        }

        if (field.getAttribute("type") === 'text' || field.tagName === "TEXTAREA" || field.getAttribute("type") === "date" || field.getAttribute("type") === 'email') {
            if (field.id) {
                fieldName = field.getAttribute("name")
                field.value = data[fieldName]
            }
        }
        if (field.getAttribute("name") == "congreso_search" || field.getAttribute("name") == "estatal_search" || field.getAttribute("name") == "federal_search") {
            data[field.getAttribute("name")].forEach(idState => {
                if (idState == field.value) field.checked = true;
            })
        }
    }
}
