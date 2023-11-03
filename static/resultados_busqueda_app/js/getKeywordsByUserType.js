
const myKeywords = document.getElementById("my-keywords")
const usuarioKeywords = document.getElementById("usuario-keywords")
const clienteKeywords = document.getElementById("cliente-keywords")
var radios = [myKeywords, usuarioKeywords, clienteKeywords]
var radioSelected = "my-keywords"

let page = 1;
const btnAnterior = document.getElementById('btnAnterior');
const btnSiguiente = document.getElementById('btnSiguiente');
var last_page = page

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

function getKeywords() {
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
}

getKeywords()

async function keywordsAJAX() {
    try {

        var response = await fetch(`/keywords/data/?page=${page}&size=10&keyword_type=${getRadioSelected()}`)
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

keywordsAJAX()

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
                </a>
            `
        })
        assignLinksToEachKeyword()
        autoClickKeyword()
    }
}

function autoClickKeyword() {
    const url = new URL(window.location.href)
    const keyword_id = url.searchParams.get("keyword").toString()
    var keyword = document.getElementById(keyword_id)
    if (keyword) {
        keyword.click()
    }
}