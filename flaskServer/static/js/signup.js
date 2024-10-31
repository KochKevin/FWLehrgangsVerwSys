document.addEventListener('DOMContentLoaded', function() {

    const loginForm = document.getElementById("signupForm");
    loginForm.addEventListener("submit", OnSignupFormSubmit);

});

function OnSignupFormSubmit(event){


    event.preventDefault();

    document.getElementById("signupError").innerHTML = "";

    const municipalitie= document.getElementById("municipalitie").value;
    const fire_station = document.getElementById("fire_station").value;
    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if(!signupForm.checkValidity()){

        const loginError = document.getElementById("loginError");

        loginError.innerHTML = "<p>Ihre Registrier Daten sind nicht Vollständig</p>";

        console.log("Error: Signup information is not valid");
        return
    }

    //Send Data

    const jsonData = JSON.stringify({
        //municipalitie : municipalitie,
        //fire_station : fire_station,
        first_name : firstName,
        last_name : lastName,
        email : email,
        password : password 
    })


    fetch("/auth/signup", {
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

            document.getElementById("signupError").innerHTML = data.error_message;
            console.log("Signup ERROR: ", data.error_message)
    
        }else{
            console.log("Registrieren Erfolgreich")
            //Redirect to dashboard
            window.location.href = data.redirect_url
        }

    })
    .catch(error => {
        document.getElementById("signupError").innerHTML = error;
        console.error("Error: ", error);
    })

}