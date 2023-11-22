table.on("dataLoaded", function(){
    setTimeout(() => {
        var redirectButtons = document.getElementsByClassName("redirect")
        var count = redirectButtons.length
        if (count >= 1){
            for (let i = 0; i < count; i++) {
                const redirectBtn = redirectButtons[i];
                redirectBtn.addEventListener("click", () => {
                    setTimeout(() => {
                        var page = getPageToShowInSearchResults()

                        var radioSelected = getRadioSelected()
                        
                        window.location.href = `/search-results?keyword=${idActualizado}&keyword_type=${radioSelected}&page=${page}`;
                    }, 1)
                })
            }
        }
    }, 1) 
});
