/*
// Zukünftige Implementierung von Websockets für Echtzeitdaten
// -> Anzahl der Benutzungen überwachen
// -> Updates an den Server nur senden, wenn sich die Daten ändern, um Ressourcen zu sparen
Weiters umbennen von QRCode ... zu certificate

*/


let qrCode

let qualification_certificates;

let codeCreationSettings;

let currentSelectedCertificate = -1;
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

    getCertificateCreationSettings();


    //Load created codes from user

    getCodes(function () {
        renderCodesTableFromUser()
    });



    console.log("Inital Load completed")

});


function getCodes(callbackFunction) {
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


            //console.log("Successful gathered qualifications data: ", data);
            qualification_certificates = data.qualification_certificates;

            if (callbackFunction) {
                callbackFunction();
            }
        })
        .catch(error => {
            //What happns on Error
            console.error("Error: ", error);
        })
}



//Fix with div
//currentRenderedCode = -1;

function renderCodesTableFromUser(currentSelectedCertificate) {

    html = "";


    html += "<table>";

    html += "<tr>";
    html += "<th>ID</th>";
    html += "<th>Code</th>";
    html += "<th>Qualifikations Level</th>";
    html += "<th>Anzahl an benutzungen</th>";
    html += "<th>Maximalanzahl an benutzungen</th>";
    html += "<th>Erstellungs Zeitpunkt</th>";
    html += "<th>Ablauf Zeitpunkt</th>";
    html += "</tr>";

    for (i = 0; i < qualification_certificates.length; i++) {

        html += "<tr>";

        html += "<td>" + qualification_certificates[i].id + "</td>";
        html += "<td>" + qualification_certificates[i].code + "</td>";
        html += "<td>" + qualification_certificates[i].qualification_level + "</td>";
        html += "<td>" + qualification_certificates[i].amount_of_uses + "</td>";
        html += "<td>" + qualification_certificates[i].max_amount_of_uses + "</td>";
        html += "<td>" + qualification_certificates[i].created_timestamp + "</td>";
        html += "<td>" + qualification_certificates[i].end_timestamp + "</td>";


        if (i != currentSelectedCertificate) {
            html += "<td>" + "<button id='showQRCode' onClick='onShowCode(" + i + ")' >Anzeigen</button>" + "</td>";
        } else {
            html += "<td>" + "Ausgewählt" + "</td>";
        }

        html += "<td>" + "<button id='showQRCode' onClick='onDeleteCode(" + i + ")' >Löschen</button>" + "</td>";

        html += "</tr>";
    }

    html += "<tr>";
    html += "<th colspan = '6'>" + "<button id='showQRCode' onClick='onCreateNewCode()' >Neuen Code hinzufügen </button> " + "</th>";
    html += "</tr>";

    html += "</table>";


    document.getElementById("codeTable").innerHTML = html;

}



function onShowCode(currentCertificate) {

    currentSelectedCertificate = currentCertificate;

    //Chnage later to ids with specific id in name to look for those
    renderCodesTableFromUser(currentCertificate);
    showCertificateUpdateSettings(currentCertificate);


    code = qualification_certificates[currentCertificate].code;
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

    if (qualification_certificates.length >= codeCreationSettings.max_amount_codes) {
        console.log("Limit of Codes reached. Limit: " + codeCreationSettings.max_amount_codes)
        return;
    }

    showCertficateCreationSettings();

}

function createNewCode(qualificationLevel, maxAmountOfUses) {

    const jsonData = JSON.stringify({
        "qualification_level": qualificationLevel,
        "max_amount_of_uses": maxAmountOfUses

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



            getCodes(function () {
                onShowCode(qualification_certificates.length - 1);
            });
            //renderQRCode(data.code);
            //Show new created code
            //onShowCode(qualification_certificates.length);
            console.log("test 2");
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
    //console.log("Deleting " + i);

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


            //console.log("Deletet " + i + data);


            getCodes(function () {
                hideAllCertificateSettings();
                renderCodesTableFromUser();
            });

        })
        .catch(error => {
            //What happens on Error
            console.error("Error: ", error);
        })
}




function setupCertificateSettings() {
    //Populate Qualification Level dropdown:
    qualificationLevelDropdowns = document.getElementsByClassName("qualificationLevelDropdown");

    for (qualificationLevelDropdown of qualificationLevelDropdowns) {

        var initalOption = document.createElement("option");
        initalOption.value = "none";
        initalOption.innerHTML = "Auswählen";
        qualificationLevelDropdown.appendChild(initalOption);

        for (i = 0; i < codeCreationSettings.qualification_list.length; i++) {
            var option = document.createElement("option");
            option.value = codeCreationSettings.qualification_list[i].id;
            option.innerHTML = codeCreationSettings.qualification_list[i].titel;

            qualificationLevelDropdown.appendChild(option);
        }
    }

    //Set max user amount
    maxAmountOfUsesElements = document.getElementsByClassName("maxAmountOfUses");
    for (maxAmountOfUses of maxAmountOfUsesElements) {
        maxAmountOfUses.setAttribute("min", codeCreationSettings.amount_uses.min);
        maxAmountOfUses.setAttribute("max", codeCreationSettings.amount_uses.max);
        maxAmountOfUses.setAttribute("setValue", 1);
    }
}

function showCertficateCreationSettings() {
    document.getElementById("certificateCreation").style.visibility = 'visible';
    document.getElementById("certificateUpdate").style.visibility = 'hidden';


    //Set code life time
    endTimeInMilli = codeCreationSettings.code_life_time.in_hours * 60 * 60 * 1000;
    currentDate = new Date();
    endDate = new Date(currentDate.getTime() + endTimeInMilli);
    document.getElementById("provisionalEndTime").innerHTML = "Code läuft ab: " + formatTime(endDate) + "  " + formatDate(endDate)
}

function showCertificateUpdateSettings(currentCertificate) {

    document.getElementById("certificateCreation").style.visibility = 'hidden';
    document.getElementById("certificateUpdate").style.visibility = 'visible';


    //Set Pre Values
    qualificationLevelDropdown = document.getElementById("certificateUpdate").querySelector(".codeSettingsForm").querySelector(".qualificationLevelDropdown");
    qualificationLevelDropdown.value = qualification_certificates[currentCertificate].qualification_level;

    maxAmountOfUses = document.getElementById("certificateUpdate").querySelector(".codeSettingsForm").querySelector(".maxAmountOfUses");
    maxAmountOfUses.value = qualification_certificates[currentCertificate].max_amount_of_uses;

}

function hideAllCertificateSettings() {
    document.getElementById("certificateCreation").style.visibility = 'hidden';
    document.getElementById("certificateUpdate").style.visibility = 'hidden';
}

function onSaveCodeClicked() {

    qualificationLevel = document.getElementById("certificateCreation").querySelector(".codeCreationForm").querySelector(".qualificationLevelDropdown").value;

    if (qualificationLevel == "none") {
        console.error("Select an qualification level");
        return;
    }

    maxAmountOfUses = document.getElementById("certificateCreation").querySelector(".codeCreationForm").querySelector(".maxAmountOfUses").value;

    if (maxAmountOfUses < codeCreationSettings.amount_uses.min) {
        console.error("Max User amount is smaller than " + codeCreationSettings.amount_uses.min);
        return;
    }

    if (maxAmountOfUses > codeCreationSettings.amount_uses.max) {
        console.error("Max User amount is bigger than " + codeCreationSettings.amount_uses.max);
        return;
    }


    createNewCode(qualificationLevel, maxAmountOfUses)
}

function onUpdateCodeClicked() {
    qualificationId = document.getElementById("certificateUpdate").querySelector(".codeSettingsForm").querySelector(".qualificationLevelDropdown").value;

    if (qualificationId == "none") {
        console.error("Select an qualification level");
        return;
    }

    maxAmountOfUses = document.getElementById("certificateUpdate").querySelector(".codeSettingsForm").querySelector(".maxAmountOfUses").value;

    if (maxAmountOfUses < codeCreationSettings.amount_uses.min) {
        console.error("Max User amount is smaller than " + codeCreationSettings.amount_uses.min);
        return;
    }

    if (maxAmountOfUses > codeCreationSettings.amount_uses.max) {
        console.error("Max User amount is bigger than " + codeCreationSettings.amount_uses.max);
        return;
    }


    updateCode(qualification_certificates[currentSelectedCertificate].id, qualificationId, maxAmountOfUses)

}


function updateCode(certificateId, qualificationId, maxAmountOfUses) {

    const jsonData = JSON.stringify({
        "certificate_id": certificateId,
        "qualification_id": qualificationId,
        "max_amount_of_uses": maxAmountOfUses
    })


    fetch("/api/v1/update-qr-code-data", {
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

            getCodes(function () {
                renderCodesTableFromUser();
                showCertificateUpdateSettings(currentSelectedCertificate);
            });
        })
        .catch(error => {
            //What happens on Error
            console.error("Error: ", error);
        })
}


function getCertificateCreationSettings() {

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
            setupCertificateSettings();

        })
        .catch(error => {
            //What happens on Error
            console.error("Error: ", error);
        })
}

