// Validtion Code for Inputs
var userID = document.getElementById("userID");
var userPassword = document.getElementById("userPassword");

var idError = document.getElementById("idError");
var passwordError = document.getElementById("passwordError");

var request;

userID.addEventListener("textInput", userIDVerify);
userPassword.addEventListener("textInput", userPasswordVerify);

/* If user didn't fill the input element, and clicked submit button directly. */
function validated()
{
    /* userId must more than 1 char. */
    if (userID.value.length < 1 || userID.value.length > 20)
    {
        userID.style.border = "1px solid red";
        idError.style.display = "block";
        userID.focus();
        console.log("Wrong user id.");
        return false;
    }
    /* userpassword must more than 8 chars. */
    if (userPassword.value.length < 8)
    {
        userPassword.style.border = "1px solid red";
        passwordError.style.display = "block";
        userPassword.focus();
        console.log("Wrong password.");
        return false;
    }
    return true;
}

/* If user input right format of ID and password, hide error div. */
function userIDVerify()
{
    if (userID.value.length >= 0 || userID.value.length <= 21)
    {
        userID.style.border = "1px solid #cccccc";
        idError.style.display = "none";
        console.log("Avalible user id.");
        return true;
    }
}

function userPasswordVerify()
{
    if (userPassword.value.length >= 7)
    {
        userPassword.style.border = "1px solid #cccccc";
        passwordError.style.display = "none";
        console.log("Avalible password.");
        return true;
    }
}

// Main function of login.
function login(num)
{
    console.log("Submit id and password.");
    if (true/*validated()*/)
    {
        console.log("Avalible id and password.");
        if (window.XMLHttpRequest)
            request = new XMLHttpRequest();
        else // Old IE browser.
            request = new ActiveXObject("Microsoft.XMLHTTP");
        
        request.open("POST", "http://192.168.100.50:5000/test/USER/login");
        console.log("XMLHttpRequest opened.");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify({"userID": userID.value, "userPassword": userPassword.value, "type": num}));
        /*req = {"userID": userID, "userPassword": userPassword, "type": num};
        reqJson = JSON.stringify(req);
        request.send(reqJson);*/
        console.log("JSON sent.");
        request.onload = function()
        {
            console.log(request.responseText);
            rst = JSON.parse(request.responseText);
            if (rst.rspCode == "200")
            {
                console.log("Login success!");
                // Different identity.
                if (num == 1)
                    window.location.assign(rst.URL);
            }
            else if(rst.rspCode == "400")
            {
                console.log("Login failed!");
                return false;
            }
            else
            {
                console.log("Login failed! Unknow response text code.");
                return false;
            }
        }
        console.log("Login failed! not onload.");
        return false;
    }
    else
        return false;
}