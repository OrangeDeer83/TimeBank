// Human Resource Management GM -> input email to add GM.
const newEmail = document.getElementById("newEmail");
const error = document.getElementById("error");
newEmail.addEventListener("input", newEmailVerify);
var emailRegexp = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;

function showError(rspCode)
{
    error.style.color = "#EECA00";
    switch (rspCode)
    {
        case   200: error.innerHTML = "已就緒..."; error.style.color = "white"; return ;
        case   300: error.innerHTML = "系統錯誤"; return ;
        case   400: error.innerHTML = "等待伺服器回應..."; error.style.color = "white"; return ;
        case 40015: error.innerHTML = "系統錯誤，評論管理員新增失敗"; return ;
        case 40115: error.innerHTML = "電子郵件格式不符，請再次確認"; return ;
        case 40215: error.innerHTML = "電子郵件重複，請再次確認"; return ;
        case   500: error.innerHTML = "請輸入電子郵件"; return ;
    }
}

function newEmailVerify()
{
    if (newEmail.value.length > 0 && newEmail.value.match(emailRegexp) != null)
    {
        newEmail.style.border = "";
        error.style.color = "white";
        error.innerHTML = "Email格式正確";
    }
}

// When user press enter or click add button.
function addGMEmail()
{
    if (newEmail.value.length == 0)
    {
        showError(500);
        newEmail.style.border = "1px solid red";
        newEmail.focus();
        return ;
    }
    if (newEmail.value.match(emailRegexp) == null)
    {
        showError(40115);
        newEmail.style.border = "1px solid red";
        newEmail.focus();
        return ;
    }

    var addEmailRequest;
    if (window.XMLHttpRequest)
        addEmailRequest = new XMLHttpRequest();
    else
        addEmailRequest = new ActiveXObject("Microsoft.XMLHTTP");
    addEmailRequest.open("POST", "/test/load_GM_mail");
    addEmailRequest.setRequestHeader("Content-Type", "application/json");
    addEmailRequest.send(JSON.stringify({"GMMail": newEmail.value}));
    addEmailRequest.onload = function()
    {
        showError(200);
        console.log(addEmailRequest.responseText);
        rst = JSON.parse(addEmailRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("電子郵件新增成功" + newEmail.value);
                return ;
            case "300": case 300:
                showError(300); return ;
            case "400": case 400:
                showError(40015); return ;
            case "401": case 401:
                showError(40115); return ;
            case "402": case 402:
                showError(40215); return ;
        }
    }
    showError(400);
}