function submitText() {
    var text = document.getElementById("textInput").value;
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({text: text})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("offensiveLanguage").innerText = data.langage_offensant ? "Oui" : "Non";
        document.getElementById("dangerFr").innerText = data.pourcentage_dangerosite_fr.toFixed(2);
        document.getElementById("dangerEn").innerText = data.pourcentage_dangerosite_en.toFixed(2);
        document.getElementById("dangerGlobal").innerText = data.pourcentage_dangerosite_global.toFixed(2);

        // var dangerList = document.getElementById("dangerList");
        // dangerList.innerHTML = '';
        // data.nature_dangerosite.forEach(item => {
        //     var listItem = document.createElement('li');
        //     listItem.innerText = item.type_menace + ': ' + item.pourcentage.toFixed(2) + '%';
        //     dangerList.appendChild(listItem);
        // });

        document.getElementById("namedEntities").innerText = data.entites_nommees.join(', ');
        document.getElementById("verbs").innerText = data.verbes.join(', ');
        document.getElementById("adjectives").innerText = data.adjectif.join(', ');

        document.getElementById("resultContainer").style.display = "block";
    })
    .catch(error => console.error('Error:', error));
}
