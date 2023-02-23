function AddDiv() {
   let div = document.createElement("div")
    div.id = "new-div"
   div.style.height = '500px'
   div.style.overflow = "scroll"
    let button = document.querySelector('#add_quesiton')
    button.parentElement.insertBefore(div, button)
    button.remove()
    fillDiv(div)
}

function fillDiv(parameter) {
//     trzeba uzupelnic div danymi z all questions, ale tylko ktore nie sa uzyte w tescie

}

function buildTable() {
    let questionTable = document.getElementById("questions-table")
    let rowsInTable = questionTable.rows
    fetch("/test_details3/testowy-test-1676896069").then(resp => {
        if (!resp.ok) {
            alert("Błąd")
        }
        return resp.json();
    })
        .then(
            function (resp) {
                document.querySelectorAll("#questions-table .rowclass").forEach(function (e){e.remove()})
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


                })

            }
        )
}


