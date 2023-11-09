table.on("dataLoaded", function(data){
    setTimeout(() => {
        var redirectButtons = document.getElementsByClassName("redirect")
        var count = redirectButtons.length
        if (count >= 1){
            for (let i = 0; i < count; i++) {
                const redirectBtn = redirectButtons[i];
                redirectBtn.addEventListener("click", () => {
                    setTimeout(() => {
                        window.location.href = `/search-results?keyword=${idActualizado}`;
                    }, 1)
                })
            }
        }
    }, 1) 
});
