table.on("dataLoaded", function(){
    setTimeout(() => {
        var redirectButtons = document.getElementsByClassName("redirect")
        var count = redirectButtons.length
        if (count >= 1){
            for (let i = 0; i < count; i++) {
                const redirectBtn = redirectButtons[i];
                redirectBtn.addEventListener("click", () => {
                    setTimeout(() => {
                        var searchInput = document.getElementById("search-keyword")
                        var radioSelected = getRadioSelected()
                        if (searchInput.value != "") {
                            window.location.href = `/search-results?keyword=${idActualizado}&keyword_type=${radioSelected}&page=1&includeKeywordInTop=true&keyword_title=${keyword_title}`;
                        } else {
                            var page = getPageToShowInSearchResults()
                                                        
                            window.location.href = `/search-results?keyword=${idActualizado}&keyword_type=${radioSelected}&page=${page}`;
                        }                        
                        
                    }, 1)
                })
            }
        }
    }, 1) 
});
