
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
                    let tr = document.createElement("tr")
                    let td = document.createElement("td")
                    let td1 = document.createElement("td")
                    let td2 = document.createElement("td")
                    let td3 = document.createElement("td")
                    let td4 = document.createElement("td")
                    tr.className = "rowclass"
                    td.setAttribute("style", "border-width: 2px");
                    td1.setAttribute("style", "border-width: 2px");
                    td2.setAttribute("style", "border-width: 2px");
                    td2.style.wordWrap = "break-word"
                    td3.setAttribute("style", "border-width: 2px");
                    td4.setAttribute("style", "border-width: 2px");

                    td.innerText = index + 1;
                    td1.innerText = el.question;
                    td2.innerText = el.possible_answers;
                    td3.innerText = el.correct_answer;
                    tr.appendChild(td)
                    tr.appendChild(td1)
                    tr.appendChild(td2)
                    tr.appendChild(td3)
                    tr.appendChild(td4)
                    questionTable.appendChild(tr)


                })

            }
        )
}
buildTable()
// $.ajax({
//     type: "GET",
//     url: "/test_details3/testowy-test-1676896069",
//     success: function (response) {
//         console.log("jest", response)
//     },
//     error: function (error) {
//         console.log("dupa",error)
//     }
// })