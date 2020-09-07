// Input
const gmName = document.getElementById("gmName");
const gmPassword = document.getElementById("gmPassword");
const checkPassword = document.getElementById("checkPassword");
const gmEmail = document.getElementById("gmEmail");
const gmPhone = document.getElementById("gmPhone");
const gmTerms = document.getElementById("gmTerms");

gmName.addEventListener('input', gmNameVerify);
gmPassword.addEventListener('input', gmPasswordVerify);
checkPassword.addEventListener('input', checkPasswordVerify);
gmEmail.addEventListener('input', gmEmailVerify);
gmPhone.addEventListener('input', gmPhoneVerify);
gmTerms.addEventListener('click', gmTermsVerify);

const passwordRegexp = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\w).{8,30}$/;
const emailRegexp = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
const phoneRegexp = /^(\+886|0)+([0-9]+)*[0-9]+((-+(\d)*)*)+((\#\d+)*)+$/;

// Show and hide error; focus and ignore on the input.
const error0 = document.getElementById("error0");
const error1 = document.getElementById("error1");
const error2 = document.getElementById("error2");
const error3 = document.getElementById("error3");
const error4 = document.getElementById("error4");
const error5 = document.getElementById("error5");
function displayError(inputElement, index, type)
{
    console.log(inputElement + " " + index + " " + type)
    if (type) // Show error.
    {
        console.log(" ");
        if (inputElement)
        {
            console.log(" ");
            inputElement.style.border = "1px solid red";
            inputElement.focus();
        }
        console.log(" ");
        switch (index)
        {
            case  0: break;
            case  1:
                error0.innerHTML = '等待伺服器回應...';
                error0.style.display = "block"; break;
            case  2:
                error0.innerHTML = "系統錯誤，請稍後再試";
                error0.style.display = "block"; break;
            case 3:
                error0,innerHTML = "驗證信寄送失敗，請稍後再試";
                error0.style.display = "block"; break;
            case 11:
                error1.innerHTML = "請輸入管理員名稱，至多20字元";
                error1.style.display = "block"; break;
            case 12:
                error1.innerHTML = "此名稱已有人使用，請再試一次";
                error1.style.display = "block"; break;
            case 13:
                error1.innerHTML = "管理員名稱格式不符，請再試一次";
                error1.style.display = "block"; break;
            case 21:
                error2.innerHTML = "請輸入密碼，8-30字元";
                error2.style.display = "block"; break;
            case 22:
                error2.innerHTML = "密碼格式不符，請再試一次";
                error2.style.display = "block"; break;
            case 31:
                error3.innerHTML = "請再次輸入您的密碼";
                error3.style.display = "block"; break;
            case 32:
                error3.innerHTML = "密碼不相符，請再試一次";
                error3.style.display = "block"; break;
            case 41:
                error4.innerHTML = "請輸入您的電子郵件，至多50字元";
                error4.style.display = "block"; break;
            case 42:
                error4.innerHTML = "電子郵件格式錯誤";
                error4.style.display = "block"; break;
            case 43:
                error4.innerHTML = "電子郵件與他人重複";
                error4.style.display = "block"; break;
            case 51:
                error5.innerHTML = "請輸入您的電話號碼";
                error5.style.display = "block"; break;
            case 52:
                error5.innerHTML = "電話號碼格式錯誤";
                error5.style.display = "block"; break;
            case 61:
                error0.innerHTML = "請閱讀並同意使用者條款";
                error0.style.display = "block"; break;
        }
    }
    else // Hide Error.
    {
        console.log(" ");
        if (inputElement)
        {
            console.log(" ");
            inputElement.style.border = "1px solid #CCCCCC";
        }
        console.log(" ");
        switch (index)
        {
            case 0: error0.style.display = "none"; break;
            case 1: error1.style.display = "none"; break;
            case 2: error2.style.display = "none"; break;
            case 3: error3.style.display = "none"; break;
            case 4: error4.style.display = "none"; break;
            case 5: error5.style.display = "none"; break;
        }
        console.log(" ");
    }
    
}

function validated()
{
    console.log(1)
    // if: Null input or too long; else if: wrong format.
    if (gmName.value.length < 1 || gmName.value.length > 20)
    {
        displayError(gmName, 11, true);
        return false;
    }
    if (gmPassword.value.length < 8 || gmPassword.value.length > 30)
    {
        displayError(gmPassword, 21, true);
        return false;
    }
    else if (gmPassword.value.match(passwordRegexp) == null)
    {
        displayError(gmPassword, 22, true);
        return false;
    }
    if (checkPassword.value.length < 8 || checkPassword.value.length > 30)
    {
        displayError(checkPassword, 31, true);
        return false;
    }
    else if (checkPassword.value != gmPassword.value)
    {
        displayError(checkPassword, 32, true);
        return false;
    }
    if (gmEmail.value.length < 3)
    {
        displayError(gmEmail, 41, true);
        return false;
    }
    else if (gmEmail.value.match(emailRegexp) == null)
    {
        displayError(gmEmail, 42, true);
        return false;
    }
    if (gmPhone.value.length < 8)
    {
        displayError(gmPhone, 51, true);
        return false;
    }
    else if (gmPhone.value.match(phoneRegexp) == null)
    {
        displayError(gmPhone, 52, true);
        return false;
    }
    if (gmTerms.checked != true)
    {
        displayError(false, 61, true);
        return false;
    }
    return true;
}

function gmNameVerify()
{
    displayError(false, 0, false);
    if (gmName.value.length > 0 && gmName.value.length <= 20)
        displayError(gmName, 1, false);
}
function gmPasswordVerify()
{
    displayError(false, 0, false);
    if (gmPassword.value.length >= 8 && gmPassword.value.length <= 30)
        displayError(gmPassword, 2, false);
    if (gmPassword.value.match(passwordRegexp) != null)
        displayError(gmPassword, 2, false);
    if (checkPassword.value == gmPassword.value)
        displayError(checkPassword, 3, false);
}
displayError(false, 0, false);
function checkPasswordVerify()
{
    displayError(false, 0, false);
    if (checkPassword.value.length >= 8 && checkPassword.value.length <= 30)
        displayError(checkPassword, 3, false);
    if (checkPassword.value == gmPassword.value)
        displayError(checkPassword, 3, false);
}
function gmEmailVerify()
{
    displayError(false, 0, false);
    if (gmEmail.value.length >= 3 && gmEmail.value.length <= 50)
        displayError(gmEmail, 4, false);
    if (gmEmail.value.match(emailRegexp) != null)
        displayError(gmEmail, 4, false);
}
function gmPhoneVerify()
{
    displayError(false, 0, false);
    if (gmPhone.value.length >= 8)
        displayError(gmPhone, 5, false);
    if (gmPhone.value.match(phoneRegexp) != null)
        displayError(gmPhone, 5, false);
}
function gmTermsVerify()
{
    if (gmTerms.checked == true)
        displayError(false, 0, false);
    else
        displayError(false, 61, true);
}

function gmRegister()
{
    if (!validated()) return;
    else
    {
        var gmRegisterRequest = new XMLHttpRequest();
        gmRegisterRequest.open("POST", "/account/GM/register");
        gmRegisterRequest.setRequestHeader("Content-Type", "application/json");
        gmRegisterRequest.send(JSON.stringify({"GMName": gmName.value, "GMPassword": gmPassword.value, "GMMail": gmEmail.value, "GMPhone": gmPhone.value}));
        gmRegisterRequest.onload = function()
        {
            displayError(false, 0, false);
            console.log(gmRegisterRequest.responseText);
            rst = JSON.parse(gmRegisterRequest.responseText);
            switch (rst.rspCode)
            {
                case "200": case 200:
                    alert("至電子信箱確認身份後，即可加入");
                    break;
                case "201": case 201:
                    alert("此電子郵件已申請過，再次寄出驗證信，請至信箱確認");
                    break;
                case "202": case 202:
                    alert("申請成功，驗證信已寄出，請至電子信箱確認");
                    break;
                case "300": case 300:
                case "400": case 400:
                    displayError(false, 2, true); break;
                case "401": case 401:
                    displayError(gmName, 12, true); break;
                case "402": case 402:
                    displayError(gmPassword, 22, true); break;
                case "403": case 403:
                    displayError(gmEmail, 41, true); break;
                case "404": case 404:
                    displayError(gmEmail, 42, true); break;
                case "405": case 405:
                    displayError(gmPhone, 52, true); break;
                case "406": case 406:
                    displayError(gmName, 12, true); break;
                case "407": case 407:
                case "408": case 408:
                case "410": case 410:
                    displayError(false, 3, true); break;
                case "409": case 409:
                    displayError(gmEmail, 43, true); break;
            }
        }
    }
}