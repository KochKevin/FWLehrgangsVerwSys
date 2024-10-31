let qualificationList;

document.addEventListener('DOMContentLoaded', function() {

    fetchUserData();
    qualificationList = document.getElementById("qualificationList");
    fetchQualificationList();
});


function fetchQualificationList(){
    
    fetch("/api/get_qualifications_for_user", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        }
    })
    .then(response => {

        if(response.ok){
            return response.json();
        }else if (response.status == 403)
        {
            throw new Error("User-Permisson-Error");
        }
        else{
            throw new Error("Network-Error");
        }

    })
    .then(data => {

        console.log("Successful gathered qualifications data: ", data);
        renderQualifications(data);

    })
    .catch(error => {
        //What happns on Error
        console.error("Error: ", error);
    })
}

function renderQualifications(data){

    const qualificationArray = data.qualifications;

    for(i = 0; i < qualificationArray.length; i++){
        addQualification(qualificationArray[i].id, qualificationArray[i].titel, qualificationArray[i].total_session_amount, qualificationArray[i].sessions_done_amount, qualificationArray[i].is_done);
    }
}

function addQualification(id, titel, totalSessionAmount, totalSessionsDone, is_done){
    let pdfExportButton = "<br>"

    if(is_done){
        pdfExportButton = "<button type='button' onclick = 'onClickExportPDF(" + id + ")'>Export PDF</button>"
    }


    qualificationHTML = `
    <div id = "qualification">

        <div onclick= 'onQualificationClick(` + id + `)'>

            <h5 class = "qualificationName">` + titel + `<h5>
            <p>` + totalSessionsDone + ` von ` + totalSessionAmount + ` Abgeschlossen</p>
        </div>

        ` + pdfExportButton + ` 
        <hr>
    </div>
    `
    qualificationList.innerHTML += qualificationHTML;
}


function onQualificationClick(id){
    //Open qualification with qualification ID
    console.log("Clicked on Qualification " + id);
    const paramtersForGET = "?id=" + id;
    window.location.href = "../qualification" + paramtersForGET;
}

function onLogout(){
    console.log("Logout");

    fetch("/auth/logout", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
    })
    .then(response => {

        if(response.ok){
            return response.json();
        }else if (response.status == 403)
        {
            throw new Error("User-Permisson-Error");
        }
        else{
            throw new Error("Network-Error");
        }

    })
    .then(data => {
        if (data.logout_status == "bad"){
            console.log("Logout ERROR: ", data.error_message)
    
        }else{
            console.log("Logout Erfolgreich")
            window.location.href = data.redirect_url
        }

    })
    .catch(error => {
        console.error("Error: ", error);
        console.log()
    })

}


function onClickExportPDF(qualificationId){
    console.log("PDF EXPORT")


    const jsonData = JSON.stringify({
        qualification_id : qualificationId
    })


    fetch("/api/generate_pdf", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: jsonData
    })
    .then(response => {


        if (response.ok) {
            return response.blob(); // Erstelle einen Blob von der Antwort
        } else {
            throw new Error("Fehler beim Generieren der PDF");
        }
    })
    .then(blob => {


        // Erstelle eine URL für den Blob
        const url = window.URL.createObjectURL(blob);
        
        // Öffne die URL in einem neuen Tab
        window.open(url, '_blank');
        
        // Gib die URL frei
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error("Error: ", error);
    })
}



function onManageCodesClicked(){
    window.location.href = "../generate-code"
}

function onScannCodeClicked(){
    window.location.href = "../scann-code"
}

function onProfilSettingsClicked(){
    //window.location.href = "../scann-code"
}

function fetchUserData(){


    fetch("/api/get_user_information", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
    })
    .then(response => {

        if(response.ok){
            return response.json();
        }else if (response.status == 403)
        {
            throw new Error("User-Permisson-Error");
        }
        else{
            throw new Error("Network-Error");
        }

    })
    .then(data => {
        
        console.log(data)

        //Hide manage codes button when user rank is lower than teacher rank
        if(data.rank < 1){
            document.getElementById("manageCodesButton").style.visibility = 'hidden';
        }else{
            document.getElementById("manageCodesButton").style.visibility = 'visible';
    }

    })
    .catch(error => {
        console.error("Error: ", error);
        console.log()
    })
}