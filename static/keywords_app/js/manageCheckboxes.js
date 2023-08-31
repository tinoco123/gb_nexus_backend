create_estatal_checkbox = document.getElementById("selectAllEstatal")
create_congreso_checkbox = document.getElementById("selectAllCongreso")
create_federal_checkbox = document.getElementById("selectAllFederal")

edit_estatal_checkbox = document.getElementById("selectAllEditEstatal")
edit_congreso_checkbox = document.getElementById("selectAllEditCongreso")
edit_federal_checkbox = document.getElementById("selectAllEditFederal")

checkboxes_estatales = document.getElementsByClassName("create-estatal-checkboxes")
checkboxes_congreso = document.getElementsByClassName("create-congreso-checkboxes")
checkboxes_federal = document.getElementsByClassName("create-federal-checkboxes")

edit_checkboxes_estatales = document.getElementsByClassName("edit-estatal-checkboxes")
edit_checkboxes_congreso = document.getElementsByClassName("edit-congreso-checkboxes")
edit_checkboxes_federal = document.getElementsByClassName("edit-federal-checkboxes")

var checkboxesToSelectAll = [
    { "selectAll": create_estatal_checkbox, "checkboxes": checkboxes_estatales }, 
    { "selectAll": create_congreso_checkbox, "checkboxes": checkboxes_congreso },
    { "selectAll": create_federal_checkbox, "checkboxes": checkboxes_federal },
    { "selectAll": edit_estatal_checkbox, "checkboxes": edit_checkboxes_estatales },
    { "selectAll": edit_congreso_checkbox, "checkboxes": edit_checkboxes_congreso },
    { "selectAll": edit_federal_checkbox, "checkboxes": edit_checkboxes_federal }
]

checkboxesToSelectAll.forEach(keywordType => {
    keywordType.selectAll.addEventListener("change", () => {
        var isChecked = keywordType.selectAll.checked;
        for (var i = 0; i < keywordType.checkboxes.length; i++) {
            keywordType.checkboxes[i].checked = isChecked;
        }
    })
    for (const i of keywordType.checkboxes) {
        i.addEventListener("change", () => {
            var allChecked = true
            for (const j of keywordType.checkboxes) {
                if (!j.checked) {
                    allChecked = false
                    break
                }
            }
            keywordType.selectAll.checked = allChecked
        })
    }
})




