var newPassword = document.getElementById("newPassword");
var checkPassword = document.getElementById("checkPassword");

var passwordError1 = document.getElementById("passwordError1");
var passwordError2 = document.getElementById("passwordError2");
var passwordError3 = document.getElementById("passwordError3");
var passwordError4 = document.getElementById("passwordError4");
var systemError = document.getElementById("systemError");

var passwordRegexp = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\w).{8,30}$/;

newPassword.addEventListener("input", newPasswordVerify);
checkPassword.addEventListener("input", checkPasswordVerify);

function getToken()
{
    var location = window.location.href;
    var token = "";
    var i = 0;
    while (i != location.length)
    {
        if (location[i] != "/" && location != "?")
            token += location[i];
        else
            token = "";
        i++;
    }
    return token;
}

function newPasswordVerify()
{
    systemError.style.display = "none";
    if (newPassword.value.length >= 8 && newPassword.value.length <= 30)
    {
        newPassword.style.border = "1px solid #CCCCCC";
        passwordError1.style.display = "none";
    }
    if (newPassword.value.match(passwordRegexp) != null)
    {
        newPassword.style.border = "1px solid #CCCCCC";
        passwordError2.style.display = "none";
    }
}

function checkPasswordVerify()
{
    systemError.style.display = "none";
    if (checkPassword.value.length >= 8 && checkPassword.value.length <= 30)
    {
        checkPassword.style.border = "1px solid #CCCCCC";
        passwordError3.style.display = "none";
    }
    if (checkPassword.value == newPassword.value)
    {
        checkPassword.style.border = "1px solid #CCCCCC";
        passwordError4.style.display = "none";
    }
}

function resetPassword()
{
    if (newPassword.value.length < 8 || newPassword.value.length > 30)
    {
        newPassword.style.border = "1px solid red";
        passwordError1.style.display = "block";
        newPassword.focus();
        return false;
    }
    else if (newPassword.value.match(passwordRegexp) == null)
    {
        newPassword.style.border = "1px solid red";
        passwordError2.style.display = "block";
        newPassword.focus();
        return false;
    }
    else if (checkPassword.value.length < 8 || checkPassword.value.length > 30)
    {
        checkPassword.style.border = "1px solid red";
        passwordError3.style.display = "block";
        checkPassword.focus();
        return false;
    }
    else if (checkPassword.value != newPassword.value)
    {
        checkPassword.style.border = "1px solid red";
        passwordError4.style.display = "block";
        checkPassword.focus();
        return false;
    }

    var request = new XMLHttpRequest();
    request.open("POST", "/account/GM/reset_password");
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify({'token': getToken(), "userPassword": newPassword.value}));
    request.onload = function()
    {
        systemError2.style.display = "none";
        console.log(request.responseText);
        rst = JSON.parse(request.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200: // Reset password success.
                console.log("Reset password success.");
                alert("??????????????????????????????????????????");
                window.location.assign("/USER/");
                return true;
            case "402": case 402: // Format of password is illegal.
                newPassword.style.border = "1px solid red";
                passwordError1.style.display = "block";
                newPassword.focus();
                return false;
            case "300": case 300: // Method wrong.
            case "400": case 400: // Database wrong.
            case "401": case 401: // Token wrong.
            default:
                systemError1.style.display = "block";
                return false;
        }
    }
    systemError2.style.display = "block";
}