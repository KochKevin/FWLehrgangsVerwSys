document.addEventListener('DOMContentLoaded', function() {

    const loginForm = document.getElementById("loginForm");
    loginForm.addEventListener("submit", OnLoginFormSubmit);


});


function OnLoginFormSubmit(event){


    event.preventDefault();

    document.getElementById("loginError").innerHTML = "";

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if(!loginForm.checkValidity()){

        const loginError = document.getElementById("loginError");

        loginError.innerHTML = "<p>Ihre Login Daten sind nicht Vollständig</p>";

        console.log("Error: Login information is not valid");
        return
    }

    //Send Data

    const jsonData = JSON.stringify({
        email : email,
        password : password 
    })


    fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: jsonData
    })
    .then(response => {

        if(response.ok){
            return response.json();
        }else{
            throw new Error("Network-Error");
        }

    })
    .then(data => {

        if (data.login_status == "bad"){

            document.getElementById("loginError").innerHTML = data.error_message;
            console.log("Login ERROR: ", data.error_message)
    
        }else{
            console.log("Login Erfolgreich")
            
            //If page parameters have an redirect, rediract o page after login else redirect to dashboard

            const urlParameters = new URLSearchParams(window.location.search);
            if (urlParameters.has("redirect")){
                redirectUrl = urlParameters.get("redirect");
                console.log("Redirect to: " + redirectUrl)
                window.location.href = redirectUrl;
            }else
            {
                console.log("Redirect to: " + data.redirect_url)
                window.location.href = data.redirect_url
            }
        
        }

    })
    .catch(error => {
        document.getElementById("loginError").innerHTML = error;
        console.error("Error: ", error);
    })

}