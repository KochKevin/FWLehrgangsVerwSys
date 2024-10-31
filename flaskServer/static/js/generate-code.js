/*
In Zukunft hier mit Websockets arbeiten?
-> Dann können Daten in echtzeit angezeigt werden
        -> Anzahl an Benutzungen

Button zum Löschen
Button um neue hinzuzufügen
    -> Es soll ein Formular geöffnet werden
        ->Gleiche sollte auch beim anzeigen der Codes angzeigt werden um diese zu bearbeiten 


Wann der Code abläuft
Wie viele benutzug der Code maximal hat

Limit QR Code auf 5 pro teacher
Löäschen von QR Codes






Beim Laden der Seite:

Die codes des users laden
    -> In eine Liste anlegen, durch welche einfach durch gelooped werden kann

Daten für ertsellen eines neuen Codes
    -> Was für Qualifikations Level gibt es? 




*/


let qrCode

let qualification_certificates;

let codeCreationSettings;
document.addEventListener('DOMContentLoaded', function () {

    qrCode = new QRCode(document.getElementById("qrcode"), {
        text: "",
        width: 600,
        height: 600,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });

    //Load Data from Server
    getCodeCreationSettings();
    getCodes();

});


function getCodes() {
    const jsonData = JSON.stringify({

    })

    fetch("/api/v1/get_qr_codes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: jsonData
    })
        .then(response => {

            if (response.ok) {
                return response.json();
            } else if (response.status == 403) {
                throw new Error("User-Permisson-Error");
            }
            else {
                throw new Error("Network-Error");
            }

        })
        .then(data => {

            console.log("Successful gathered qualifications data: ", data);
            qualification_certificates = data.qualification_certificates;
            renderCodesTableFromUser(data)
        })
        .catch(error => {
            //What happns on Error
            console.error("Error: ", error);
        })
}



//Fix with div
//currentRenderedCode = -1;

function renderCodesTableFromUser(currentSelectedCode) {

    html = "";


    html += "<table>";

    html += "<tr>";
    html += "<th>ID</th>";
    html += "<th>Code</th>";
    html += "<th>Qualifikations Level</th>";
    html += "<th>Anzahl an benutzungen</th>";
    html += "<th>Erstellungs Zeitpunkt</th>";
    html += "<th>Ablauf Zeitpunkt</th>";
    html += "</tr>";

    for (i = 0; i < qualification_certificates.length; i++) {

        html += "<tr>";
        html += "<td>" + qualification_certificates[i].id + "</td>";
        html += "<td>" + qualification_certificates[i].code + "</td>";
        html += "<td>" + qualification_certificates[i].qualification_level + "</td>";
        html += "<td>" + qualification_certificates[i].amount_of_uses + "</td>";
        html += "<td>" + qualification_certificates[i].created_timestamp + "</td>";
        html += "<td>" + qualification_certificates[i].end_timestamp + "</td>";


        if(i != currentSelectedCode){
            html += "<td>" + "<button id='showQRCode' onClick='onShowCode(" + i + ")' >Anzeigen</button>" + "</td>";
        }else{
            html += "<td>" + "Ausgewählt" + "</td>";
        }

        html += "<td>" + "<button id='showQRCode' onClick='onDeleteCode(" + i + ")' >Löschen</button>" + "</td>";


        /*
        if(currentRenderedCode == i){
            html += "<td>" + "Ausgewählt" +"</td>";
        }else{
            html += "<td>" + "<button id='showQRCode' onClick='onRenderQRCodeClicked(" + i +")' >Anzeigen</button>" +"</td>";
        }
        */

        html += "</tr>";
    }

    html += "<tr>";
    html += "<th colspan = '6'>" + "<button id='showQRCode' onClick='onCreateNewCode()' >Neuen Code hinzufügen </button> " + "</th>";
    html += "</tr>";

    html += "</table>";


    document.getElementById("codeTable").innerHTML = html;

}



function onShowCode(i) {
    //Chnage later to ids with specific id in name to look for those
    renderCodesTableFromUser(i); 
    showQRCodeSettings();


    code = qualification_certificates[i].code;

    renderQRCode(code)
    document.getElementById("codeText").innerHTML = "<h2>" + code + "</h2>";
}


function renderQRCode(code) {
    qrCode.clear();
    //Change path in future when page path is changed
    qrData = window.location.origin + "/scann-code?c=" + code;

    console.log("Creating QR-Code with code: " + qrData);
    qrCode.makeCode(qrData)
}

function onCreateNewCode() {

    if(qualification_certificates.length >= codeCreationSettings.max_amount_codes){
        console.log("Limit of Codes reached. Limit: " + codeCreationSettings.max_amount_codes)
        return;
    }

    showQRCodeSettingToCreateNewCode();
    
}

function createNewCode(qualificationLevel, maxAmountOfUsers) {

    const jsonData = JSON.stringify({
        "qualification_level": qualificationLevel,
        "max_user_amount": maxAmountOfUsers

    })


    fetch("/api/v1/create-qr-code-data", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: jsonData
    })
        .then(response => {

            if (response.ok) {
                return response.json();
            } else if (response.status == 403) {
                throw new Error("User-Permisson-Error");
            }
            else {
                throw new Error("Network-Error");
            }

        })
        .then(data => {


            console.log("Successful gathered qualifications data: ", data);



            getCodes();
            renderQRCode(data.code);
        })
        .catch(error => {
            //What happens on Error
            console.error("Error: ", error);
        })

}


function onToDashboard() {
    window.location.href = "/dashboard";
}

function formatDate(date) {

    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();

    dateString = `${day}.${month}.${year}`;
    return dateString;
}

function formatTime(date) {

    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    timeString = `${hours}:${minutes}`;
    return timeString;
}

function onDeleteCode(i) {
    console.log("Deleting " + i);

    const jsonData = JSON.stringify({

        "qr_code_id": qualification_certificates[i].id

    })


    fetch("/api/v1/delete_code", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: jsonData
    })
        .then(response => {

            if (response.ok) {
                return response.json();
            } else if (response.status == 403) {
                throw new Error("User-Permisson-Error");
            }
            else {
                throw new Error("Network-Error");
            }

        })
        .then(data => {


            console.log("Deletet " + i + data);



            getCodes();
        })
        .catch(error => {
            //What happens on Error
            console.error("Error: ", error);
        })
}




function showQRCodeSettingToCreateNewCode() {
    document.getElementById("codeSettingsForm").style.visibility = 'hidden';
    document.getElementById("codeCreationForm").style.visibility = 'visible';

    document.getElementById("qrcode").style.visibility = 'hidden';
    document.getElementById("codeText").style.visibility = 'hidden';


    //Populate Qualification Level dropdown:
    qualificationLevelDropdown = document.getElementById("qualificationLevelDropdown");

    var initalOption = document.createElement("option");
    initalOption.value = "none";
    initalOption.innerHTML = "Auswählen";
    qualificationLevelDropdown.appendChild(initalOption);

    for(i = 0; i < codeCreationSettings.qualification_levels.length; i++){
        var option = document.createElement("option");
        option.value = codeCreationSettings.qualification_levels[i].id;
        option.innerHTML = codeCreationSettings.qualification_levels[i].titel;

        qualificationLevelDropdown.appendChild(option);
    }

    //Set  max user amount
    document.getElementById("maxAmountOfUses").setAttribute("min", codeCreationSettings.amount_uses.min);
    document.getElementById("maxAmountOfUses").setAttribute("max", codeCreationSettings.amount_uses.max);
    document.getElementById("maxAmountOfUses").setAttribute("setValue", 1);

    //Set code life time

    endTimeInMilli = codeCreationSettings.code_life_time.in_hours * 60 * 60 * 1000;
    currentDate = new Date();
    endDate = new Date(currentDate.getTime() + endTimeInMilli);
    document.getElementById("provisionalEndTime").innerHTML = "Code läuft ab: " + formatTime(endDate) + "  " + formatDate(endDate)
}

function showQRCodeSettings() {
    document.getElementById("codeSettingsForm").style.visibility = 'visible';
    document.getElementById("codeCreationForm").style.visibility = 'hidden';

    document.getElementById("qrcode").style.visibility = 'visible';
    document.getElementById("codeText").style.visibility = 'visible';
}

function onSaveCodeClicked() {

    qualificationLevel = document.getElementById("qualificationLevelDropdown").value;

    if (qualificationLevel == "none") {
        console.error("Select an qualification level");
        return;
    }

    console.log(qualificationLevel);

    maxAmountOfUsers = document.getElementById("maxAmountOfUses").value;

    if (maxAmountOfUsers < codeCreationSettings.amount_uses.min) {
        console.error("Max User amount is smaller than " + codeCreationSettings.amount_uses.min);
        return;
    }

    if(maxAmountOfUsers > codeCreationSettings.amount_uses.max){
        console.error("Max User amount is bigger than " + codeCreationSettings.amount_uses.max);
        return;
    }


    createNewCode(qualificationLevel, maxAmountOfUsers)
}

function onUpdateCodeClicked() {

}


function updateCode(id, qualificationLevel, maxAmountOfUsers){

    const jsonData = JSON.stringify({
        "qualification_level": qualificationLevel,
        "max_user_amount": maxAmountOfUsers
    })


    fetch("/api/v1/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: jsonData
    })
        .then(response => {

            if (response.ok) {
                return response.json();
            } else if (response.status == 403) {
                throw new Error("User-Permisson-Error");
            }
            else {
                throw new Error("Network-Error");
            }

        })
        .then(data => {

        })
        .catch(error => {
            //What happens on Error
            console.error("Error: ", error);
        })
}


function getCodeCreationSettings(){

    fetch("/api/v1/get_code_creation_settings", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
    })
        .then(response => {

            if (response.ok) {
                return response.json();
            } else if (response.status == 403) {
                throw new Error("User-Permisson-Error");
            }
            else {
                throw new Error("Network-Error");
            }

        })
        .then(data => {

            console.log(data);
            codeCreationSettings = data;

        })
        .catch(error => {
            //What happens on Error
            console.error("Error: ", error);
        })
}

