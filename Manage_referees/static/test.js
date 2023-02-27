function CreateQuestionsTable() {
    let table = document.createElement('table')
    let tr = document.createElement('tr')
    let th = document.createElement('th')
    let th2 = document.createElement('th')
    let th3 = document.createElement('th')
    table.id = "new-question-table"
    th.classList = "col-8"
    th.innerText = "Pytanie"
    th2.innerText = "Dla klasy"
    th3.innerText = "Akcja"
    table.appendChild(th)
    table.appendChild(th2)
    table.appendChild(th3)
    return table
    }

function AddDiv(testslug) {
   let div = document.createElement("div")
    div.id = "new-div"
    div.style.margin = "20px 20px 20px 20px"
   div.style.height = '500px'
   div.style.overflow = "scroll"
    let button = document.querySelector('#add_quesiton')
    button.parentElement.insertBefore(div, button)
    button.remove()
    document.querySelector('#new-div').appendChild(CreateQuestionsTable())
    fillDiv(testslug)
}

function fillDiv(parameter) {
//     trzeba uzupelnic div danymi z all questions, ale tylko ktore nie sa uzyte w tescie

    fetch(`/questions_not_in_test/${parameter}`).then(resp => {
        if (!resp.ok) {
            alert("Błąd")
        }
        return resp.json();
    }).then(
        function (resp) {
            if (resp.counter>0) {
                resp.data.forEach(function (el) {
                    let newtable = document.querySelector("#new-question-table")
                    let newtr = document.createElement('tr')
                    let newtd = document.createElement('td')
                    let newtd2 = document.createElement('td')
                    let newtd3 = document.createElement('td')
                    newtr.classList = "new-question-row"
                    newtd.innerText = el.question
                    newtd2.innerText = el.league
                    let link = document.createElement('button')
                    link.className = "tn btn-primary btn-sm button-to-add"
                    link.setAttribute("id", el.url)
                    link.setAttribute("data-testslug", parameter)
                    link.innerText = "Dodaj do testu"
                    newtd3.appendChild(link)
                    newtr.appendChild(newtd)
                    newtr.appendChild(newtd2)
                    newtr.appendChild(newtd3)
                    newtable.appendChild(newtr)
                })
            }
            else {
                let newtable = document.querySelector("#new-question-table")
                let newtr = document.createElement('tr')
                let newtd = document.createElement('td')
                newtd.innerText = "Brak pytań do dodania"
                newtr.appendChild(newtd)
                newtable.appendChild(newtr)
            }


        let tdelement = document.querySelectorAll('td');
        tdelement.forEach(function (element){
            element.setAttribute("style", "border-width: 2px")});
        let thelement = document.querySelectorAll('th');
        thelement.forEach(function (element){
        element.setAttribute("style", "border-width: 2px")});
        buttonsAction()
        }
    )
}

function buildTable(testslug) {
    let questionTable = document.getElementById("questions-table")
    fetch(`/test_details3/${testslug}`).then(resp => {
        if (!resp.ok) {
            alert("Błąd")
        }
        return resp.json();
    })
        .then(
            function (resp) {

                resp.test.forEach(function (el, index) {
                    let hiddenrow = document.querySelector('.hidden-row')
                    let newrow = hiddenrow.cloneNode(true);
                    newrow.classList = "rowclass"
                    newrow.style.display = "table-row"
                    newrow.cells[0].innerText = index + 1
                    newrow.cells[1].innerText = el.question
                    newrow.cells[2].innerText = el.possible_answers;
                    newrow.cells[3].innerText = el.correct_answer;
                    let link = document.createElement('a')
                    link.setAttribute("href", el.url)
                    link.innerText = "Usuń"
                    newrow.cells[4].appendChild(link)
                    newrow.cells[2].style.wordWrap = "break-word"
                    questionTable.appendChild(newrow)
                    document.querySelector('#question-counter').innerText = index+1


                })

            }
        )
}

function clearTables() {
    document.querySelectorAll("#questions-table .rowclass").forEach(function (e){e.remove()})
    document.querySelectorAll(".new-question-row").forEach(function (e){e.remove()})
}


function addToTest(linktoadd, testslug) {
    clearTables()
    fetch(`${linktoadd}`)
    buildTable(testslug)
    fillDiv(testslug)


}

function buttonsAction() {
    let allAddButtons = document.querySelectorAll('.button-to-add')
    allAddButtons.forEach(function (el) {
        el.addEventListener('click', function () {
            addToTest(el.id, el.dataset.testslug)

        })
    })
}