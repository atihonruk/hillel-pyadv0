console.log('Hello, JS')
/* XMLHttpRequest */

function autocomplete(elem) {
    elem.addEventListener("input", function(e) {
        val = this.value
        // check length of the value
        //                               lambda response: response.json()
        fetch('/autocomplete?' + new URLSearchParams({term: val}))
            .then(response => response.json())
            .then(data => makeList(this, data))
    })

    function makeList(container, compl) {
        console.log(container)
        div = document.createElement("DIV")
        container.parentNode.appendChild(div)
        for (i=0; i < compl.length; i++) {
            title = compl[i].title
            e = document.createElement("div") // <div></div>
            div.appendChild(e)
            e.innerHTML += "<strong>" + title + "</strong>" // <div>...</div>
        }
    }
}
