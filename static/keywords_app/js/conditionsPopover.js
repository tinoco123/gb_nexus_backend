const informationIcons = document.querySelectorAll(".conditions");
informationIcons.forEach(icon => {
    icon.addEventListener("click", event => {
        console.log("Condiciones");
    })
});