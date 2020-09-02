const adminName = document.getElementById("adminName");
const adminPassword = document.getElementById("adminPassword");

const error0 = document.getElementById("error0");
const error1 = document.getElementById("error1");

adminName.addEventListener("input", adminNameVerify);
adminPassword.addEventListener("input", adminPasswordVerify);

function displayError(inputElement, index, type)
{
    console.log(inputElement+ index+ type)
    if (type)
    {
        if (inputElement)
        {
            inputElement.style.border = "1px solid red";
            inputElement.focus();
        }
        switch (index)
        {
            case  0: break;
            case  1:
                error0.innerHTML = '等待伺服器回應...';
                error0.style.display = "block"; break;
            case  2:
                error0.innerHTML = "系統錯誤，請稍後再試";
                error0.style.display = "block"; break;
            case  3:
                error0.innerHTML = "管理員名稱或密碼錯誤，請再試一次";
                error0.style.display = "block"; break;
            case 11:
                error1.innerHTML = "請輸入使用者名稱(1至20位字元)";
                error1.style.display = "block"; break;
            case 21:
                error0.innerHTML = "請輸入密碼，8-30字元";
                error0.style.display = "block"; break;
        }
    }
    else
    {
        if (inputElement)
            inputElement.style.border = "1px solid #CCCCCC";
        switch (index)
        {
            case 0:
                error0.style.display = "none"; break;
            case 1:
                error1.style.display = "none"; break;
            case 2:
                error0.style.display = "none"; break;
        }
    }
}

function validated()
{
    if (adminName.value.length < 1 || adminName.value.length > 20)
    {
        displayError(adminName, 11, true);
        return false;
    }
    if (adminPassword.value.length < 8)
    {
        displayError(adminPassword, 21, true);
        return false;
    }
    return true;
}

function adminNameVerify()
{
    displayError(adminPassword, 0, false);
    if (adminName.value.length > 0 && adminName.value.length <= 20)
        displayError(adminName, 1, false);
}

function adminPasswordVerify()
{
    if (adminPassword.value.length >= 8)
        displayError(adminPassword, 2, false);
}

function gmLogin()
{
    if (!validated()) return ;
    else
    {
        var loginGMRequest = new XMLHttpRequest();
        loginGMRequest.open("POST", "http://192.168.1.144:5000/account/GM/login");
        loginGMRequest.setRequestHeader("Content-Type", "application/json");
        loginGMRequest.send(JSON.stringify({ "adminName": adminName.value, "adminPassword": adminPassword.value }));
        loginGMRequest.onload = function()
        {
            displayError(false, 0, false);
            console.log(loginGMRequest.responseText);
            rst = JSON.parse(loginGMRequest.responseText);
            switch (rst.rspCode)
            {
                case "200": case 200:
                    window.location.assign("/GM/updateGrade");
                    break;
                case "300": case 300:
                case "400": case 400:
                    displayError(false, 2, true);
                    break;
                case "401": case 401:
                case "402": case 402:
                    displayError(adminPassword, 3, true);
                    break;
            }
        }
    }
}