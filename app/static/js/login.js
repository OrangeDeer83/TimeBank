// Validtion Code for Inputs
var userName = document.getElementById("userName");
var userPassword = document.getElementById("userPassword");

var idError = document.getElementById("idError");
var passwordError = document.getElementById("passwordError");
var loginError1 = document.getElementById("loginError1");
var loginError2 = document.getElementById("loginError2");

var request;

userName.addEventListener("input", userIDVerify);
userPassword.addEventListener("input", userPasswordVerify);

/* If user didn't fill the input element, and clicked submit button directly. */
function validated()
{
    /* userName must more than 1 char. */
    if (userName.value.length < 1 || userName.value.length > 20)
    {
        userName.style.border = "1px solid red";
        idError.style.display = "block";
        userName.focus();
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
    loginError1.style.display = "none";
    loginError2.style.display = "none";
    if (userName.value.length >= 1 && userName.value.length <= 20)
    {
        userName.style.border = "1px solid #CCCCCC";
        idError.style.display = "none";
        console.log("Avalible user id.");
        return true;
    }
}

function userPasswordVerify()
{
    loginError1.style.display = "none";
    loginError2.style.display = "none";
    if (userPassword.value.length > 7)
    {
        userPassword.style.border = "1px solid #CCCCCC";
        passwordError.style.display = "none";
        console.log("Avalible password.");
        return true;
    }
}

/* ID or password is wrong, server cannot find. */
function showLoginError1()
{
    loginError1.style.display = "block";
    userName.focus();
}

/* Server wrong. */
function showLoginError2()
{
    loginError2.style.display = "block";
}

// Main function of login.
function login()
{
    console.log("Submit id and password.");
    if (validated())
    {
        console.log("Avalible id and password.");
        if (window.XMLHttpRequest)
            request = new XMLHttpRequest();
        else // Old IE browser.
            request = new ActiveXObject("Microsoft.XMLHTTP");
        
        request.open("POST", "/test/USER/login");
        console.log("XMLHttpRequest opened.");

        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify({"userName": userName.value, "userPassword": userPassword.value}));
        console.log("JSON sent.");
        request.onload = function()
        {
            console.log(request.responseText);
            rst = JSON.parse(request.responseText);
            switch (rst.rspCode)
            {
                case "200": case 200:
                    alert("登入成功!");
                    window.location.assign("/USER/");
                    break;
                case "400": case 400:
                    console.log("Login failed!");
                    showLoginError1();
                    break;
                default:
                    console.log("Login failed! Unknow response text code.");
                    showLoginError2();
            }
        }
    }
    else
    {
        console.log("ID or password in wrong format.");
        return false;
    }
}