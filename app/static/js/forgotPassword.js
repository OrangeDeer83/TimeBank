var userEmail = document.getElementById("userEmail");

var emailError1 = document.getElementById("emailError1");
var emailError2 = document.getElementById("emailError2");
var registerError1 = document.getElementById("systemError1");
var registerError2 = document.getElementById("systemError2");

var request;
const emailRegexp = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;

userEmail.addEventListener("input", userEmailVerify);

function userEmailVerify()
{
    registerError1.style.display = "none";
    registerError2.style.display = "none";
    if (userEmail.value.length >= 3)
    {
        userEmail.style.border = "1px solid #CCCCCC";
        emailError1.style.display = "none";
    }
    if (userEmail.value.match(emailRegexp) != null)
    {
        userEmail.style.border = "1px solid #CCCCCC";
        emailError2.style.display = "none";
    }
}

function forgotPasswordEmail()
{
    if (userEmail.value.length < 3 || userEmail.value.length > 50)
    {
        userEmail.style.border = "1px solid red";
        emailError1.style.display = "block";
        userEmail.focus();
        return false;
    }
    else if (userEmail.value.match(emailRegexp) == null)
    {
        userEmail.style.border = "1px solid red";
        emailError2.style.display = "block";
        userEmail.focus();
        return false;
    }

    if (window.XMLHttpRequest)
        request = new XMLHttpRequest();
    else // Old IE browser.
        request = new ActiveXObject("Microsoft.XMLHTTP");

    request.open("POST", "http://192.168.1.146:5000/test/USER/forget_password");
    request.onreadystatechange = function()
    {
        if (request.readyState == 4 && request.status == 200)
        {
            request.setRequestHeader("Content-Type", "application/json");
            request.send(JSON.stringify({"userMail": userEmail.value}));
            console.log(request.responseText);
            rst = JSON.parse(request.responseText);

            request.onload = function()
            {
                switch (rst.rspCode)
                {
                    case "200": case 200: // Email send success.
                        console.log("Email send success!");
                        window.location.assign("");
                        return true;
                    case "300": case 300: // Method wrong.
                    case "400": case 400: // Database wrong.
                        systemError1.style.display = "block";
                        return false;
                    case "401": case 401: // Length of email is illegal.
                        userEmail.style.border = "1px solid red";
                        emailError1.style.display = "block";
                        userEmail.focus();
                        return false;
                    case "402": case 402: // Format of email os illegal.
                        userEmail.style.border = "1px solid red";
                        emailError2.style.display = "block";
                        userEmail.focus();
                        return false;
                    case "403": case 403: // Didn't find the user of this email.
                        userEmail.style.border = "1px solid red";
                        emailError3.style.display = "block";
                        userEmail.focus();
                        return false;
                    case "404": case 404: // Reset mail send failed.
                        systemError2.style.display = "block";
                        return false;
                    default:
                        systemError1.style.display = "block";
                        return false;
                }
            }
        }
    }
    systemError1.style.display = "block";
    return false;
}