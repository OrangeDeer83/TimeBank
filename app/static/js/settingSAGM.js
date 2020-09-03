const error1 = document.getElementById('error1');
const error2 = document.getElementById('error2');
const error3 = document.getElementById('error3');
const oldPassword = document.getElementById('oldPassword');
const newPassword = document.getElementById('newPassword');
const checkPassword = document.getElementById('checkPassword');
const passwordRegexp = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\w).{8,30}$/;

var passwordChangeSuccess = false;

oldPassword.addEventListener('input', oldVerify);
newPassword.addEventListener('input', newVerify);
checkPassword.addEventListener('input', checkVerify);

function validated()
{
    if (passwordChangeSuccess) return false;
    if (oldPassword.value.length == 0)
    {
        error1.innerHTML = '請輸入舊密碼';
        error1.style.display = 'block';
        oldPassword.focus();
        return false;
    }
    if (newPassword.value.length < 8 || newPassword.value.length > 30)
    {
        error2.innerHTML = '請輸入新密碼，長度需在8~30字元之間';
        error2.style.display = 'block';
        newPassword.focus();
        return false;
    }
    if (newPassword.value.match(passwordRegexp) == null)
    {
        error2.innerHTML = '需包含數字、大小寫字母及特殊符號，請再次確認';
        error2.style.display = 'block';
        newPassword.focus();
        return false;
    }
    if (checkPassword.value.length < 8 || checkPassword.value.length > 30)
    {
        error3.innerHTML = '請再次輸入新密碼，長度需在8~30字元之間';
        error3.style.display = 'block';
        checkPassword.focus();
        return false;
    }
    if (checkPassword.value != newPassword.value)
    {
        error3.innerHTML = '密碼不相符，請再次確認';
        error3.style.display = 'block';
        checkPassword.focus();
        return false;
    }
    return true;
}

function oldVerify()
{
    error1.removeAttribute('style');
}

function newVerify()
{
    error2.removeAttribute('style');
}

function checkVerify()
{
    error3.removeAttribute('style');
}

function uploadNewPassword()
{
    if (!validated()) return ;

    var uploadNewPasswordRequest = new XMLHttpRequest();
    uploadNewPasswordRequest.open('POST', '/account/setting/accountPassword');
    uploadNewPasswordRequest.setRequestHeader('Content-Type', 'application/json');
    uploadNewPasswordRequest.send(JSON.stringify({'adminPassword': newPassword.value, 'adminOldPassword': oldPassword.value}));
    uploadNewPasswordRequest.onload = function()
    {
        console.log(uploadNewPasswordRequest.responseText);
        rst = JSON.parse(uploadNewPasswordRequest.responseText);
        switch (rst.rspCode)
        {
            case '200': case 200:
                document.getElementById('settingButton').value = '密碼修改成功';
                document.getElementById('settingButton').removeAttribute('onclick');
                document.getElementById('settingButton').style.cursor = 'default';
                passwordChangeSuccess = true;
                oldPassword.value = '';
                newPassword.value = '';
                checkPassword.value = '';
                break;
            case '401': case 401:
                error1.innerHTML = '舊密碼錯誤，請再次確認';
                error1.style.display = 'block';
                break;
            case '402': case 402:
                error2.innerHTML = '密碼並未更改';
                error2.style.display = 'block';
                break;
            case '403': case 403:
                error2.innerHTML = '格式不符，請再次確認';
                error2.style.display = 'block';
                break;
            case '300': case 300:
            case '400': case 400:
            default:
                document.getElementById('settingButton').value = '系統錯誤';
                document.getElementById('settingButton').removeAttribute('onclick');
                break;
        }
    }
}