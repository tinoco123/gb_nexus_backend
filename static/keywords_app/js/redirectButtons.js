table.on("dataLoaded", function(){
    setTimeout(() => {
        var redirectButtons = document.getElementsByClassName("redirect")
        var count = redirectButtons.length
        if (count >= 1){
            for (let i = 0; i < count; i++) {
                const redirectBtn = redirectButtons[i];
                redirectBtn.addEventListener("click", () => {
                    setTimeout(() => {
                        var maxPageElements = table.getPageSize()
                        var currentPage = table.getPage()
                        var rowPosition = table.getRowPosition(rowSelected)

                        var lowerLimit = maxPageElements * (currentPage - 1)
                        var position = lowerLimit + rowPosition

                        var page = 0

                        if (position % 10 != 0){
                            page = Math.trunc(position / 10) + 1
                        } else {
                            page = Math.trunc(position / 10)
                        }

                        var radioSelected = getRadioSelected()
                        
                        window.location.href = `/search-results?keyword=${idActualizado}&keyword_type=${radioSelected}&page=${page}`;
                    }, 1)
                })
            }
        }
    }, 1) 
});
