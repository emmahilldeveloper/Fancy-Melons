'use strict';

/////// Search Button Functionality ///////
let searchButton = document.getElementById("search");
let clearButton = document.getElementById("clear");

clearButton.addEventListener("click", () => {
    location.reload();
});

if (document.getElementById("tasting-results").innerText == "") {
    document.getElementById("tasting-results").innerText = "No availbility"
}

searchButton.addEventListener("click", (evt) => {
    evt.preventDefault();

    document.getElementById("tasting-results").innerHTML = "";

    const data = {
        date: document.getElementById("floatingInput").value,
    };

    fetch(`/api/search`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then((response) => response.json())
    .then(responseData => {

        responseData.matches.forEach((element) => {

            //Parent div to house all search results
            const parentDiv = document.getElementById("tasting-results");
            parentDiv.style = "text-align: center;";

            //Div for each individual in the loop
            const tastingDivCard = document.createElement("div");
            tastingDivCard.className = "card";
            tastingDivCard.style = "width:18rem; background-color: #d3d3d3; border-color: black; display: inline-block; margin: 20px;";
            tastingDivCard.id = "search-result";
            parentDiv.appendChild(tastingDivCard);

            //Shows the tasting logo
            const tastingPhoto = document.createElement("img");
            tastingPhoto.className = "card-img-top";
            tastingPhoto.alt = "Card image cap";
            tastingPhoto.id = "result-img";
            tastingPhoto.src = element.tasting_photo;
            tastingPhoto.style = "border-color: black; object-fit: cover; width: 286px; height: 286px;";
            tastingDivCard.appendChild(tastingPhoto);
            const divCardBody = document.createElement("div");
            divCardBody.className = "card-body";
            tastingDivCard.appendChild(divCardBody);

            //Shows the tasting name
            const tastingNameCardTitle = document.createElement("h5");
            tastingNameCardTitle.className = "card-title";
            tastingNameCardTitle.innerText = element.tasting_name;
            divCardBody.appendChild(tastingNameCardTitle);

            //Reserve Button
            const reserve = document.createElement("a");
            reserve.id = "reserve-button";
            reserve.setAttribute("href", `/reservations/${element.tasting_id}`);
            reserve.className = "btn btn-primary";
            reserve.innerHTML= "Reserve";
            reserve.type = "click";
            reserve.style = "text-align: left;";
            divCardBody.appendChild(reserve);
        })
    });
});

