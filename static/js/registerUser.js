// Validtion Code for Input
var userName = document.getElementById("userName");
var userID = document.getElementById("userID");
var userPassword = document.getElementById("userPassword");
var checkPassword = document.getElementById("checkPassword");
var userEmail = document.getElementById("userEmail");
var userPhone = document.getElementById("userPhone");
var gender = document.getElementsByName("gender");
var userBirthday = document.getElementById("userBirthday");
var serviceTerms = document.getElementById("serviceTerms");

// Div of Each Error
var nameError = document.getElementById("nameError");
var idError1 = document.getElementById("idError1");
var idError2 = document.getElementById("idError2");
var idError3 = document.getElementById("idError3");
var passwordError1 = document.getElementById("passwordError1");
var passwordError2 = document.getElementById("passwordError2");
var passwordError3 = document.getElementById("passwordError3");
var passwordError4 = document.getElementById("passwordError4");
var emailError1 = document.getElementById("emailError1");
var emailError2 = document.getElementById("emailError2");
var phoneError1 = document.getElementById("phoneError1");
var phoneError2 = document.getElementById("phoneError2");
var genderError = document.getElementById("genderError");
var birthError1 = document.getElementById("birthError1");
var birthError2 = document.getElementById("birthError2");
var registerError = document.getElementById("registerError");

var request, checkID;

userName.addEventListener("input", userNameVerify);
userID.addEventListener("keyup", userIDVerify);
userPassword.addEventListener("input", userPasswordVerify);
checkPassword.addEventListener("input", checkPasswordVerify);
userEmail.addEventListener("input", userEmailVerify);
userPhone.addEventListener("input", userPhoneVerify);
gender[0].addEventListener("click", userGenderVerify);
gender[1].addEventListener("click", userGenderVerify);
gender[2].addEventListener("click", userGenderVerify);
userBirthday.addEventListener("input", userBirthdayVerify);
serviceTerms.addEventListener("click", termsVerify);

var passwordRegexp = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\w).{8,30}$/;
var emailRegexp = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
var phoneRegexp = /^(\+886|0)+([0-9]+)*[0-9]+((-+(\d)*)*)+((\#\d+)*)+$/;
var birthRegexp = /^((18|19|20)[0-9]{2})[-\/.](0?[1-9]|1[012])[-\/.](0?[1-9]|[12][0-9]|3[01])$/; // Oldest person in the world: 1897/04/19

// Show/Hide error on html
function showError(inputElement, errorDiv)
{
    inputElement.style.border = "1px solid red";
    errorDiv.style.display = "block";
    inputElement.focus();
}

function hideError(inputElement, errorDiv)
{
    inputElement.style.border = "1px solid #CCCCCC";
    errorDiv.style.display = "none";
}

function idTest()
{
    if (window.XMLHttpRequest)
        checkID = new XMLHttpRequest();
    else // Old IE browser.
        checkID = new ActiveXObject("Microsoft.XMLHTTP");

    checkID.open("POST", "http://192.168.1.146:5000/detect_repeated");
    checkID.setRequestHeader("Content-Type", "application/json");
    checkID.send(JSON.stringify({"userID": userID.value}));
    console.log("CheckID JSON sent.");
    checkID.onload = function()
    {
        console.log(checkID.responseText);
        var rst = JSON.parse(checkID.responseText);
        hideError(userID, idError3);
        switch (rst.rspCode)
        {
            case "200": // ID no repeat
                hideError(userID, idError2);
                return true;
            case "400": // ID repeat
                showError(userID, idError2);
                return false;
            case "401": // ID too long
                showError(userID, idError1);
                return false;
            default: // Unkonwn response text
                showError(userID, idError3);
                return false;
        }
    }
    showError(userID, idError3);
    return false;
}

function birthTest(birthday)
{
    if (userBirthday.value.match(birthRegexp) == null)
        return false;
    var year = 0, month = 0; day = 0;
    var i = 0;
    while (birthday[i] != '/' && birthday[i] != '.' && birthday[i] != '-' && i < birthday.length)
    {
        year = year *10 + parseInt(birthday[i], 10);
        i++;
    }
    i++;
    while (birthday[i] != '/' && birthday[i] != '.' && birthday[i] != '-' && i < birthday.length)
    {
        month = month *10 + parseInt(birthday[i], 10);
        i++;
    }
    i++;
    while (i < birthday.length)
    {
        day = day *10 + parseInt(birthday[i], 10);
        i++;
    }
    
    // Date of user's birthday. !month value: 0~11
    var birthDate = new Date(year, month - 1, day);
    // Check day is legal.
    var compare = new Date(year, month, 0).getDate();
    if (compare < day)
        return false;
    // No one could birth before the oldest person.
    compare = new Date(1897, 4 - 1, 19);
    if ((birthDate - compare) < 0)
        return false;
    // No future people.
    compare = new Date();
    if ((birthDate - compare) > 0)
        return false;
    
    return true;
}

function checkGender()
{
    if (gender[0].checked)
        return 0;
    else if (gender[1].checked)
        return 1;
    else if (gender[2].checked)
        return 2;
    else
        return -1;
}

function validated()
{
    // if: Null input or too long; else if: wrong format.
    if (userName.value.length < 1 || userName.value.length > 20)
    {
        showError(userName, nameError);
        console.log("Wrong user name.");
        return false;
    }
    if (userID.value.length < 1 || userID.value.length > 20)
    {
        showError(userID, idError1);
        console.log("Wrong user id.");
        return false;
    }
    else if (!idTest())
    {
        console.log("User id has been used or server error.");
        return false;
    }
    if (userPassword.value.length < 8 || userPassword.value.length > 30)
    {
        showError(userPassword, passwordError1);
        console.log("Wrong user password.");
        return false;
    }
    else if (userPassword.value.match(passwordRegexp) == null)
    {
        showError(userPassword, passwordError2);
        console.log("Wrong user password format.");
        return false;
    }
    if (checkPassword.value.length < 8 || checkPassword.value.length > 30)
    {
        showError(checkPassword, passwordError3);
        console.log("Wrong user check password.");
        return false;
    }
    else if (checkPassword.value != userPassword.value)
    {
        showError(checkPassword, passwordError4);
        console.log("Wrong user password.");
        return false;
    }
    if (userEmail.value.length < 3)
    {
        showError(userEmail, emailError1);
        console.log("Wrong user email.");
        return false;
    }
    else if (userEmail.value.match(emailRegexp) == null)
    {
        showError(userEmail, emailError2);
        console.log("Wrong user email format.");
        return false;
    }
    if (userPhone.value.length < 8)
    {
        showError(userPhone, phoneError1);
        console.log("Wrong user phone.");
        return false;
    }
    else if (userPhone.value.match(phoneRegexp) == null)
    {
        showError(userPhone, phoneError2);
        console.log("wrong user phone format." + userPhone.value.match(phoneRegexp));
        return false;
    }
    if (checkGender() == -1)
    {
        genderError.style.display = "block";
        return false;
    }
    if (userBirthday.value.length < 1)
    {
        showError(userBirthday, birthError1);
        console.log("Wrong user birthday.");
        return false;
    }
    else if (!birthTest(userBirthday.value))
    {
        showError(userBirthday, birthError2);
        console.log("Imposible user birthday.");
        return false;
    }
    if (serviceTerms.checked != true)
    {
        termsError.style.display = "block";
        return false;
    }
    return true;
}

// Check user type status.
function userNameVerify()
{
    registerError.style.display = "none";
    if (userName.value.length >= 0 && userName.value.length <= 20)
        hideError(userName, nameError);
        return true;
}

function userIDVerify()
{
    hideError(userID, idError3);
    registerError.style.display = "none";
    if (userID.value.length > 0 && userID.value.length <= 20)
        hideError(userID, idError1);
    if (idTest(userID)){};
}

function userPasswordVerify()
{
    registerError.style.display = "none";
    if (userPassword.value.length >= 8 && userPassword.value.length <= 30)
        hideError(userPassword, passwordError1);
    if (userPassword.value.match(passwordRegexp) != null)
        hideError(userPassword, passwordError2);
}

function checkPasswordVerify()
{
    registerError.style.display = "none";
    if (checkPassword.value.length >= 1 && checkPassword.value.length <= 30)
        hideError(checkPassword, passwordError3);
    if (checkPassword.value == userPassword.value)
        hideError(checkPassword, passwordError4);
}

function userEmailVerify()
{
    registerError.style.display = "none";
    if (userEmail.value.length >= 3)
        hideError(userEmail, emailError1);
    if (userEmail.value.match(emailRegexp) != null)
        hideError(userEmail, emailError2);
}

function userPhoneVerify()
{
    registerError.style.display = "none";
    if (userPhone.value.length >= 8)
        hideError(userPhone, phoneError1);
    if (userPhone.value.match(phoneRegexp) != null)
        hideError(userPhone, phoneError2);
}

function userGenderVerify()
{
    registerError.style.display = "none";
    if (checkGender != -1)
        genderError.style.display = "none";
}

function userBirthdayVerify()
{
    registerError.style.display = "none";
    if (userBirthday.value.length >= 0)
        hideError(userBirthday, birthError1);
    if (birthTest(userBirthday))
        hideError(userBirthday, birthError2);
}

function termsVerify()
{
    if (serviceTerms.checked == true)
        termsError.style.display = "none";
    else
        termsError.style.display = "block";
}

// Main function of register.
function register()
{
    if (validated())
    {
        console.log("Avalible input.");
        if (window.XMLHttpRequest)
            request = new XMLHttpRequest();
        else // Old IE browser.
            request = new ActiveXObject("Microsoft.XMLHTTP");

        request.open("POST", "http://192.168.1.146:5000/user_register");
        console.log("XMLHttpRequest opened.");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify({"userName": userName.value, "userID": userID.value, "userPassword": userPassword.value, "userMail": userEmail.value, "userPhone": userPhone.value, "userGender": checkGender(), "userBirthday": userBirthday.value}));
        console.log("Register JSON sent.");
        request.onload = function()
        {
            console.log(request.responseText);
            var rst = JSON.parse(request.responseText);
            switch (rst.rspCode)
            {
                case 200: // Register success
                    console.log("Register success!");
                    return true;
                case 300: // Methods wrong
                    registerError.style.display = "block";
                    return false;
                case 400: // Length of userID is illegal ?????
                    showError(userID, idError1);
                    return false;
                case 401: // Format of userID is illegal ?????
                    showError(userID, idError2);
                    return false;
                case 402: // Length of username is illegal
                    showError(userName, nameError);
                    return false;
                case 403: // Length of password is illegal ?????
                    showError(userPassword, passwordError1);
                    return false;
                case 404: // Format of password is illegal ?????
                    showError(userPassword, passwordError2);
                    return false;
                case 405: // Length of email is illegal
                    showError(userEmail, emailError1);
                    return false;
                case 406: // Format of email is illegal
                    showError(userEmail, emailError2);
                    return false;
                default:
                    registerError.style.display = "block";
                    return false;
            }
        }
        console.log("Login failed! not onload.");
        registerError.style.display = "block";
        return false;
    }
    else
    {
        console.log("wrong format.");
        return false;
    }
}