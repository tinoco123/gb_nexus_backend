const myKeywords = document.getElementById("my-keywords")
const usuarioKeywords = document.getElementById("usuario-keywords")
const clienteKeywords = document.getElementById("cliente-keywords")
var radios = [myKeywords, usuarioKeywords, clienteKeywords]
var radioSelected = ""

let page = 1;
const btnAnterior = document.getElementById('btnAnterior');
const btnSiguiente = document.getElementById('btnSiguiente');
var last_page = page

radios.forEach(radio => {
    if (radio) {
        radio.addEventListener("change", async () => {
            if (radio.checked) {
                page = 1
                setRadioSelected(radio.id)
                await keywordsAJAX()
            }
        })
    }
})

btnSiguiente.addEventListener('click', () => {
    var userInfoContainerExists = UserInfoContainerExists()
    if (userInfoContainerExists) {
        userInfoContainerExists.remove()
    }
    if (page + 1 > last_page) {
        showNotifications(400, "No existen más keywords")
    } else {
        page += 1;
        keywordsAJAX()
    }
});

btnAnterior.addEventListener('click', () => {
    var userInfoContainerExists = UserInfoContainerExists()
    if (userInfoContainerExists) {
        userInfoContainerExists.remove()
    }
    if (page > 1) {
        page -= 1;
        keywordsAJAX()
    }
});

const url = new URL(window.location.href)
var keyword_id = url.searchParams.get("keyword")
var where = url.searchParams.get("keyword_type")
if (parseInt(url.searchParams.get("page"))) {
    page = parseInt(url.searchParams.get("page"))
}
var radioToSelect = document.getElementById(where)
if (radioToSelect != null) {
    if (keyword_id && page) {
        getKeywords(radioToSelect)
    }
} else if (where == "my-keywords" && keyword_id && page) {
    setRadioSelected("my-keywords")
    keywordsAJAX()
} else if (!keyword_id && !where && page) {
    setRadioSelected("my-keywords")
    keywordsAJAX()
}

function getKeywords(radio) {
    if (radio) {
        if (radio.checked == false) {
            radio.checked = true
            setRadioSelected(radio.id)
            keywordsAJAX()
        } else {
            radio.checked = true
            setRadioSelected(radio.id)
            keywordsAJAX()
        }
    }
}

async function keywordsAJAX() {
    try {
        var response = await fetch(`/keywords/data/?page=${page}&size=10&keyword_type=${getRadioSelected()}&search=`)
        var data = await response.json()
        if (response.status === 200) {
            last_page = data.last_page
            showKeywordsInList(data)
        } else if (response.status === 400) {
            showNotifications(response.status, data.error)
        } else if (response.status === 405) {
            showNotifications(response.status, "Metodo HTTP no válido")
        } else {
            showNotifications(response.status, "Intentalo más tarde")
        }
    } catch (error) {
        console.log(error)
    }
}

function getRadioSelected() {
    return radioSelected
}

function setRadioSelected(valor) {
    radioSelected = valor
}


function showKeywordsInList(data) {
    const keywordsContainer = document.getElementById("keywords-container")
    if (data.data.length == 0) {
        keywordsContainer.innerHTML = `
            <li
                class="d-flex align-items-center bg-warning-subtle p-2 mx-2 keyword-li border border-warning rounded-2"
            >
                <p class="d-flex m-0">
                    <span>Sin keywords</span>
                </p>
            </li>
    `
    } else {
        keywordsContainer.innerHTML = ``
        data.data.forEach(keyword => {
            keywordsContainer.innerHTML += `
                <a href="" class="text-black keyword-link" id="${keyword.id}">
                    <li
                        class="d-flex align-items-center bg-light p-2 m-1 keyword-li"
                    >
                        <p class="d-flex m-0">
                            <span>
                                ${keyword.title} 
                            </span>
                        </p>
                    </li>
                </a>            `
        })
        assignLinksToEachKeyword()
        var keyword = document.getElementById(keyword_id)
        if (keyword) {
            keyword.click()
            keyword_id = 0
        }
    }
}
