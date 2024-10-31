let trainingUnitList;


document.addEventListener('DOMContentLoaded', function() {

    trainingUnitList = document.getElementById("trainingUnitList");
    fetchTrainingUnits();



});


function fetchTrainingUnits(){

    const urlParameters = new URLSearchParams(window.location.search);


    const jsonData = JSON.stringify({
        qualification_id : urlParameters.get("id")
    })



    fetch("/api/get_training_units", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: jsonData
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

        console.log("Successful gathered training unit data: ", data);

        document.getElementById("qualificationName").innerHTML = data.qualification_titel;

        renderTrainingUnits(data);

    })
    .catch(error => {
        //What happns on Error
        console.error("Error: ", error);

        console.log()

    })

}


function renderTrainingUnits(data){

    trainingUnitsArray = data.training_units;


    for(i = 0; i < trainingUnitsArray.length; i++){

        sessionListHTML = "";
        sessionsArray = trainingUnitsArray[i].sessions;


        for(n = 0; n < sessionsArray.length; n++){

            sessionId = sessionsArray[n].session_id;
            sessionType = sessionsArray[n].type;
            sessionIsDone = sessionsArray[n].is_done;
            sessionIsDoneTimestamp = sessionsArray[n].is_done_timestamp;

            sessionListHTML += renderSession(sessionId, sessionType, sessionIsDone, sessionIsDoneTimestamp)

        }


        trainigUnitHTML = `
        <div id = "trainingUnit">
        <h3>` + trainingUnitsArray[i].number +" - " + trainingUnitsArray[i].titel + `</h3>
        <div id = "sessionList">` + sessionListHTML + `</div> 
        <hr>
        </div>`

        trainingUnitList.innerHTML += trainigUnitHTML;
    }
}


function renderSession(session_id, type, is_done, is_done_timestamp){
    sessionType = "";

    if(type == "theory"){
        sessionType = "Therorie Stunde";
    }else if (type == "practical"){
        sessionType = "Praxis Stunde";
    }

    sessionStatus = "";
    completeButtonHTML = "";

    if(is_done == 0){
        sessionStatus = "Ausstehend";
        completeButtonHTML = `<button type="button" onclick = "onClickSessionAsDone(` + session_id +  `)">Abschließen</button>`;
    }else if(is_done == 1){
        sessionStatus = "Abgeschlossen";
        completeButtonHTML = `<button type="button" onclick = "onClickResetSession(` + session_id +  `)">Zurücksetzten</button>`;
    }


    isDoneTimestamp = "";
    if(is_done_timestamp != null && is_done == 1){
        timestamp = new Date(is_done_timestamp);
        isDoneTimestamp = timestamp.getDate() + "." + (timestamp.getMonth() + 1) + "." + timestamp.getFullYear(); 
    }
    else{
        is_done_timestamp = "<br>"
    }


    var sessionHTML = `
    <div id = "session-` + session_id + `">
        <h5>` + sessionType + `</h5>
        <p>Status: ` + sessionStatus + `</p>
        <p>` + isDoneTimestamp + `</p>`
        + completeButtonHTML +
        `<br>
    </div>`

    return sessionHTML;
}




function onClickSessionAsDone(sessionId){
    console.log(sessionId)
    //Send at server, that the session is completed, with current timestamp and reload the data of the session

    timeNow = new Date().toISOString();

    const jsonData = JSON.stringify({
        session_id : sessionId,
        is_done_timestamp : timeNow
    });


    fetch("/api/set_user_session_as_done", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: jsonData
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

        console.log("Successful gathered data: ", data);
        updateSession(data);

    })
    .catch(error => {
        //What happns on Error
        console.error("Error: ", error);

        console.log()

    })
}



function onClickResetSession(sessionId){
    console.log("Reset Session: " + sessionId)
    //Send at server, that the session is completed, with current timestamp and reload the data of the session

    timeNow = new Date().toISOString();

    const jsonData = JSON.stringify({
        session_id : sessionId,
    });


    fetch("/api/reset_user_session", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: jsonData
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

        console.log("Successful gathered data: ", data);
        updateSession(data);

    })
    .catch(error => {
        //What happns on Error
        console.error("Error: ", error);

        console.log()

    })
}


function updateSession(data){

    data = data.session;

    let sessionElement = document.getElementById("session-" + data.session_id);

    sessionId = data.session_id;
    sessionType = data.type;
    sessionIsDone = data.is_done;
    sessionIsDoneTimestamp = data.is_done_timestamp;

    sessionElement.innerHTML = renderSession(sessionId, sessionType, sessionIsDone, sessionIsDoneTimestamp)

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



function onToDashboard(){
    window.location.href = "/dashboard";
}