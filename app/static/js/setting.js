var userID;

window.onload = function()
{
    var getIDRequest;
    if (window.XMLHttpRequest)
        getIDRequest = new XMLHttpRequest();
    else
        getIDRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getIDRequest.open("GET", "http://192.168.1.146:5000/test/getID");
    getIDRequest.setRequestHeader("Content-Type", "application/json");
    getIDRequest.send();
    getIDRequest.onload = function()
    {
        console.log(getIDRequest.responseText);
        rst = JSON.parse(getIDRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                userID = rst.ID;
                document.getElementById("userIDFile").value = userID;
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("無法取得userID");
                userID = "10";
                break;
        }
    }
}

function upload(index)
{
    switch (index)
    {
        case 23:
            uploadProfile();
            break;
        case 24:
            uploadName();
            break;
        case 25:
            uploadUserName();
            break;
        case 26:
            uploadNewPassword();
            break;
        case 27:
            uploadUserEmail();
            break;
        case 28:
            uploadUserPhone();
            break;
        case 29:
            uploadGender();
            break;
        case 30:
            uploadUserBirthday();
    }
}

function uploadProfile()
{
    const profile = document.getElementById("profile");
    var uploadFrofileRequest;
    if (window.XMLHttpRequest)
        uploadFrofileRequest = new XMLHttpRequest();
    else
        uploadFrofileRequest = new ActiveXObject("Microsoft.XMLHTTP");
    uploadFrofileRequest.open("POST", "http://192.168.1.146:5000/test/setting/userInfo");
    uploadFrofileRequest.setRequestHeader("Content-Type", "application/json");
    uploadFrofileRequest.send(JSON.stringify({"userInfo": profile.value, "userID": userID}));
    uploadFrofileRequest.onload = function()
    {
        console.log(uploadFrofileRequest.responseText);
        rst = JSON.parse(uploadFrofileRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("名稱修改成功");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                alert("系統錯誤，名稱修改失敗");
                break;
            case "401": case 401:
                alert("名稱長度需在1~20字元之間，請再次確認");
                break;
        }
    }
}

function uploadName()
{
    const name = document.getElementById("name");
    var uploadNameRequest;
    if (window.XMLHttpRequest)
        uploadNameRequest = new XMLHttpRequest();
    else
        uploadNameRequest = new ActiveXObject("Microsoft.XMLHTTP");
    uploadNameRequest.open("POST", "http://192.168.1.146:5000/test/setting/name");
    uploadNameRequest.setRequestHeader("Content-Type", "application/json");
    uploadNameRequest.send(JSON.stringify({"name": name.value, "userID": userID}));
    uploadNameRequest.onload = function()
    {
        console.log(uploadNameRequest.responseText);
        rst = JSON.parse(uploadNameRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("名稱修改成功");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                alert("系統錯誤，名稱修改失敗");
                break;
            case "401": case 401:
                alert("名稱長度需在1~20字元之間，請再次確認");
                break;
        }
    }
}

function uploadUserName()
{
    const userName = document.getElementById("userName");

    if (userName.value.length < 1 || userName.value.length > 20)
    {
        alert("使用者名稱長度必須介於1~20字元之間，請再次確認");
        return ;
    }

    var uploadUserNameRequest;
    if (window.XMLHttpRequest)
        uploadUserNameRequest = new XMLHttpRequest();
    else
        uploadUserNameRequest = new ActiveXObject("Microsoft.XMLHTTP");
    uploadUserNameRequest.open("POST", "http://192.168.1.146:5000/test/setting/userName");
    uploadUserNameRequest.setRequestHeader("Content-Type", "application/json");
    uploadUserNameRequest.send(JSON.stringify({"userName": userName.value, "userID": userID}));
    uploadUserNameRequest.onload = function()
    {
        console.log(uploadUserNameRequest.responseText);
        rst = JSON.parse(uploadUserNameRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("使用者名稱修改成功");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                alert("系統錯誤，使用者名稱修改失敗");
                break;
            case "401": case 401:
                alert("使用者名稱長度需在1~20字元之間，且不得包含特殊字符，請再次確認");
                break;
            case "402": case 402:
                alert("使用者名稱重複");
                break;
        }
    }
}

function uploadNewPassword()
{
    const oldPassword = document.getElementById("oldPassword");
    const newPassword = document.getElementById("newPassword");
    const checkPassword = document.getElementById("checkPassword");
    const passwordRegexp = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\w).{8,30}$/;

    if (newPassword.value.match(passwordRegexp) == null)
    {
        alert("新密碼格式不符，密碼長度需在8~30字元之間，且包含數字、大小寫字母及特殊符號，請再次確認");
        newPassword.focus();
        return;
    }
    if (checkPassword.value != newPassword.value)
    {
        alert("確認密碼與新密碼不同，請再次確認");
        checkPassword.focus();
    }

    var uploadNewPasswordRequest;
    if (window.XMLHttpRequest)
        uploadNewPasswordRequest = new XMLHttpRequest();
    else
        uploadNewPasswordRequest = new ActiveXObject("Microsoft.XMLHTTP");
    uploadNewPasswordRequest.open("POST", "http://192.168.1.146:5000/test/setting/userPassword");
    uploadNewPasswordRequest.setRequestHeader("Content-Type", "application/json");
    uploadNewPasswordRequest.send(JSON.stringify({"userPassword": newPassword.value, "userOldPassword": oldPassword.value, "userID": userID}));
    uploadNewPasswordRequest.onload = function()
    {
        console.log(uploadNewPasswordRequest.responseText);
        rst = JSON.parse(uploadNewPasswordRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("密碼修改成功");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                alert("系統錯誤，密碼修改失敗");
                break;
            case "401": case 401:
                alert("密碼長度需在8~30字元之間，且包含數字、大小寫字母及特殊符號，請再次確認");
                break;
            case "402": case 402:
                alert("舊密碼錯誤，請再次確認");
                break;
        }
    }
}

function uploadUserEmail()
{
    const userEmail = document.getElementById("userEmail");
    const emailRegexp = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;

    if (userEmail.value.match(emailRegexp) == null || userEmail.value.length > 50)
    {
        alert("電子信箱格式不符，長度不得超過50字元，請再次確認");
        return ;
    }

    var uploadUserEmailRequest;
    if (window.XMLHttpRequest)
        uploadUserEmailRequest = new XMLHttpRequest();
    else
        uploadUserEmailRequest = new ActiveXObject("Microsoft.XMLHTTP");
    uploadUserEmailRequest.open("POST", "http://192.168.1.146:5000/test/setting/userMail");
    uploadUserEmailRequest.setRequestHeader("Content-Type", "application/json");
    uploadUserEmailRequest.send(JSON.stringify({"userMail": userEmail.value, "userID": userID}));
    uploadUserEmailRequest.onload = function()
    {
        console.log(uploadUserEmailRequest.responseText);
        rst = JSON.parse(uploadUserEmailRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("電子信箱修改成功");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                alert("系統錯誤，電子信箱修改失敗");
                break;
            case "401": case 401:
            case "402": case 402:
                alert("電子信箱格式不符，長度不得超過50字元，請再次確認");
                break;
            case "403": case 403:
                alert("電子信箱並未修改，請再次確認");
                break;
            case "404": case 404:
                alert("此電子信箱已被使用");
                break;
        }
    }
}

function uploadUserPhone()
{
    const userPhone = document.getElementById("userPhone");
    const phoneRegexp = /^(\+886|0)+([0-9]+)*[0-9]+((-+(\d)*)*)+((\#\d+)*)+$/;

    if (userPhone.value.match(phoneRegexp) == null && userPhone.value.length < 8)
    {
        alert("電話號碼格式不符，請再次確認");
        return ;
    }

    var uploadUserPhoneRequest;
    if (window.XMLHttpRequest)
        uploadUserPhoneRequest = new XMLHttpRequest();
    else
        uploadUserPhoneRequest = new ActiveXObject("Microsoft.XMLHTTP");
    uploadUserPhoneRequest.open("POST", "http://192.168.1.146:5000/test/setting/userPhone");
    uploadUserPhoneRequest.setRequestHeader("Content-Type", "application/json");
    uploadUserPhoneRequest.send(JSON.stringify({"userPhone": userPhone.value, "userID": userID}));
    uploadUserPhoneRequest.onload = function()
    {
        console.log(uploadUserPhoneRequest.responseText);
        rst = JSON.parse(uploadUserPhoneRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("電話號碼修改成功");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                alert("系統錯誤，電話號碼修改失敗");
                break;
            case "401": case 401:
                alert("電話號碼格式不符，請再次確認");
                break;
        }
    }
}

function uploadGender()
{
    const gender = document.getElementsByName("gender");

    var checkGender
    if (gender[0].checked)
        checkGender = "0";
    else if (gender[1].checked)
        checkGender = "1";
    else if (gender[2].checked)
        checkGender = "2";
    else
    {
        alert("未知的性別，請再次確認");
        return ;
    }

    var uploadUserGenderRequest;
    if (window.XMLHttpRequest)
        uploadUserGenderRequest = new XMLHttpRequest();
    else
        uploadUserGenderRequest = new ActiveXObject("Microsoft.XMLHTTP");
    uploadUserGenderRequest.open("POST", "http://192.168.1.146:5000/test/setting/userGender");
    uploadUserGenderRequest.setRequestHeader("Content-Type", "application/json");
    uploadUserGenderRequest.send(JSON.stringify({"userGender": checkGender, "userID": userID}));
    uploadUserGenderRequest.onload = function()
    {
        console.log(uploadUserGenderRequest.responseText);
        rst = JSON.parse(uploadUserGenderRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("性別修改成功");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                alert("系統錯誤，性別修改失敗");
                break;
            case "401": case 401:
                alert("未知的性別，請再次確認");
                break;
        }
    }
}

function birthdatTest(birthday)
{
    var birthRegexp = /^((18|19|20)[0-9]{2})[-\/.](0?[1-9]|1[012])[-\/.](0?[1-9]|[12][0-9]|3[01])$/; // Oldest person in the world: 1897/04/19
    if (birthday.match(birthRegexp) == null)
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

function uploadUserBirthday()
{
    const userBirthday = document.getElementById("userBirthday");
    if (!birthdatTest(userBirthday.value))
    {
        alert("請輸入正確的生日格式");
        return ;
    }
    
    var uploadUserBirthdayRequest;
    if (window.XMLHttpRequest)
        uploadUserBirthdayRequest = new XMLHttpRequest();
    else
        uploadUserBirthdayRequest = new ActiveXObject("Microsoft.XMLHTTP");
    uploadUserBirthdayRequest.open("POST", "http://192.168.1.146:5000/test/setting/userBirthday");
    uploadUserBirthdayRequest.setRequestHeader("Content-Type", "application/json");
    uploadUserBirthdayRequest.send(JSON.stringify({"userBirthday": userBirthday.value, "userID": userID}));
    uploadUserBirthdayRequest.onload = function()
    {
        console.log(uploadUserBirthdayRequest.responseText);
        rst = JSON.parse(uploadUserBirthdayRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("生日修改成功");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                alert("系統錯誤，生日修改失敗");
                break;
            case "401": case 401:
                alert("生日格式不符，請再次確認，避免輸入未來或過於古老的日期");
                break;
        }
    }
}