// Validtion Code for Input
const nameOfUser = document.getElementById("name");
const userName = document.getElementById("userName");
const userPassword = document.getElementById("userPassword");
const checkPassword = document.getElementById("checkPassword");
const userEmail = document.getElementById("userEmail");
const userPhone = document.getElementById("userPhone");
const gender = document.getElementsByName("gender");
const userBirthday = document.getElementById("userBirthday");
const serviceTerms = document.getElementById("serviceTerms");

// Div of Each Error
var nameError = document.getElementById("nameError");
var userNameError1 = document.getElementById("userNameError1");
var userNameError2 = document.getElementById("userNameError2");
var userNameError3 = document.getElementById("userNameError3");
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

nameOfUser.addEventListener("input", nameVerify);
userName.addEventListener("keyup", userNameVerify);
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
    console.log(inputElement.name + errorDiv)
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
    checkID.open("POST", "/test/USER/detect_repeated");
    checkID.setRequestHeader("Content-Type", "application/json");
    checkID.send(JSON.stringify({"userName": userName.value}));
    console.log("CheckID JSON sent.");
    setTimeout(function(){}, 300);
    checkID.onload = function()
    {
        console.log(checkID.responseText);
        var rst = JSON.parse(checkID.responseText);
        hideError(userName, userNameError3);
        switch (rst.rspCode)
        {
            case "200": // ID no repeat
                hideError(userName, userNameError2);
                return true;
            case "300": // Database wrong.
                showError(userName, userNameError3);
                return false;
            case "400": // ID repeat
                showError(userName, userNameError3);
                return false;
            case "401": // ID too long
                showError(userName, userNameError1);
                return false;
            case "402": // ID repeat
                showError(userName, userNameError2);
                return false;
            default: // Unkonwn response text
                showError(userName, userNameError3);
                return false;
        }
    }
    showError(userName, userNameError3);
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
    // No future person.
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
    if (nameOfUser.value.length < 1 || nameOfUser.value.length > 20)
    {
        showError(nameOfUser, nameError);
        console.log("Wrong user name.");
        return false;
    }
    if (userName.value.length < 1 || userName.value.length > 20)
    {
        showError(userName, userNameError1);
        console.log("Wrong userName.");
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
function nameVerify()
{
    registerError.style.display = "none";
    if (nameOfUser.value.length >= 0 && nameOfUser.value.length <= 20)
        hideError(nameOfUser, nameError);
        return true;
}

function userNameVerify()
{
    hideError(userName, userNameError3);
    registerError.style.display = "none";
    if (userName.value.length > 0 && userName.value.length <= 20)
        hideError(userName, userNameError1);
    if (idTest(userName)){};
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

        request.open("POST", "/test/USER/register");
        console.log("XMLHttpRequest opened.");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify({"name": nameOfUser.value, "userName": userName.value, "userPassword": userPassword.value, "userMail": userEmail.value, "userPhone": userPhone.value, "userGender": checkGender(), "userBirthday": userBirthday.value}));
        request.onload = function()
        {
            registerError2.style.display = "none";
            console.log(request.responseText);
            var rst = JSON.parse(request.responseText);
            switch (rst.rspCode)
            {
                case "200": case 200: // Register success.
                    console.log("Register success!");
                    alert(nameOfUser.value + " 註冊成功!");
                    window.location.assign("/USER/");
                    return true;
                case "300": case 300: // Methods wrong.
                    registerError.style.display = "block";
                    return false;
                case "400": case 400: // Database wrong.
                    registerError.style.display = "block";
                    return false;
                case "401": case 401: // Length of name is illegal.
                    showError(nameOfUser, nameError);
                    return false;
                case "402": case 402: // Format of userName is illegal?
                    showError(userName, userNameError3);
                    return false;
                case "403": case 403: // Format of password is illegal.
                    showError(userPassword, passwordError2);
                    return false;
                case "404": case 404: // Length of email is illegal.
                case "405": case 405: // Format of email is illegal
                    showError(userEmail, emailError2);
                    return false;
                case "406": case 406: // Format of phone is illegal.
                    showError(userPhone, phoneError2);
                    return false;
                case "407": case 407: // Error of gender.
                    genderError.style.display = "block";
                    return false;
                case "408": case 408: // Format of bithday is illegal.
                case "409": case 409: // No future person.
                    genderError.style.display = "block";
                    return false;
                case "410": case 410: // User ID repeat.
                    showError(userName, userNameError2);
                    return false;
                default:
                    registerError.style.display = "block";
                    return false;
            }
        }
        registerError2.style.display = "block";
    }
    else
    {
        console.log("wrong format.");
        return false;
    }
}