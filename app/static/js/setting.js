window.onload = function()
{
    getOldUserInfo();
}

function getOldUserInfo()
{
    var uploadFrofileRequest = new XMLHttpRequest();
    uploadFrofileRequest.open("GET", "/account/output/setting_info");
    uploadFrofileRequest.setRequestHeader("Content-Type", "application/json");
    uploadFrofileRequest.send();
    uploadFrofileRequest.onload = function()
    {
        console.log(uploadFrofileRequest.responseText);
        rst = JSON.parse(uploadFrofileRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("成功讀取舊資料");
                putOldUserInfo(rst);
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert("系統錯誤，無法取得舊資料...");
                break;
        }
    }
}

function putOldUserInfo(oldInfo)
{
    document.getElementById("name").value = oldInfo.name;
    document.getElementById("userEmail").value = oldInfo.userMail;
    document.getElementById("userPhone").value = oldInfo.userPhone;
    document.getElementById("profile").value = oldInfo.userInfo;
    document.getElementById("userBirthday").value = oldInfo.userBirthday;
    console.log(oldInfo.userGender)
    switch (oldInfo.userGender)
    {
        case "0": case 0:
            document.getElementById("genderMale").checked = true;
            break;
        case "1": case 1:
            document.getElementById("genderFemale").checked = true;
            break;
        case "2": case 2:
            document.getElementById("genderElse").checked = true;
            break;
    }
    getPropicMyself(oldInfo.userID);
}

var finished = 0;
function upload()
{
    finished = 0;
    uploadProfile();
    uploadName();
    /*uploadUserName();*/
    uploadNewPassword();
    uploadUserEmail();
    uploadUserPhone();
    uploadGender();
    uploadUserBirthday();
    /*switch (index)
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
            break;
    }*/
}

function uploadProfile()
{
    const profile = document.getElementById("profile");
    var uploadProfileRequest = new XMLHttpRequest();
    uploadProfileRequest.open("POST", "/account/setting/userInfo");
    uploadProfileRequest.setRequestHeader("Content-Type", "application/json");
    uploadProfileRequest.send(JSON.stringify({"userInfo": profile.value}));
    uploadProfileRequest.onload = function()
    {
        finished++;
        console.log(uploadProfileRequest.responseText);
        rst = JSON.parse(uploadProfileRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                //alert("個人簡介修改成功");
                //window.location.reload();
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "401": case 401:
                //alert("個人簡介未作修改");
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert("系統錯誤，個人簡介修改失敗");
                break;
        }
    }
}

function uploadName()
{
    const name = document.getElementById("name");
    var uploadNameRequest = new XMLHttpRequest();
    uploadNameRequest.open("POST", "/account/setting/name");
    uploadNameRequest.setRequestHeader("Content-Type", "application/json");
    uploadNameRequest.send(JSON.stringify({"name": name.value}));
    uploadNameRequest.onload = function()
    {
        finished++;
        console.log(uploadNameRequest.responseText);
        rst = JSON.parse(uploadNameRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                //alert("名稱修改成功");
                //window.location.reload();
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "401": case 401:
                alert("名稱長度需在1~20字元之間，請再次確認");
                break;
            case "402": case 402:
                //alert("名稱未更改");
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "300": case 300:
            case "400": case 400:
            case "403": case 403:
            default:
                alert("系統錯誤，名稱修改失敗");
                break;
        }
    }
}

/*function uploadUserName()
{
    const userName = document.getElementById("userName");

    if (userName.value.length < 1 || userName.value.length > 20)
    {
        alert("使用者名稱長度必須介於1~20字元之間，請再次確認");
        return ;
    }

    var uploadUserNameRequest = new XMLHttpRequest();
    uploadUserNameRequest.open("POST", "/account/setting/accountName");
    uploadUserNameRequest.setRequestHeader("Content-Type", "application/json");
    uploadUserNameRequest.send(JSON.stringify({"userName": userName.value}));
    uploadUserNameRequest.onload = function()
    {
        console.log(uploadUserNameRequest.responseText);
        rst = JSON.parse(uploadUserNameRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("使用者名稱修改成功");
                //window.location.reload();
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
}*/

function uploadNewPassword()
{
    finished++;
    const oldPassword = document.getElementById("oldPassword");
    const newPassword = document.getElementById("newPassword");
    const checkPassword = document.getElementById("checkPassword");
    const passwordRegexp = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\w).{8,30}$/;

    if (oldPassword.value.length == 0 && newPassword.value.length == 0 && checkPassword.value.length == 0)
        return ;

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

    var uploadNewPasswordRequest = new XMLHttpRequest();
    uploadNewPasswordRequest.open("POST", "/account/setting/accountPassword");
    uploadNewPasswordRequest.setRequestHeader("Content-Type", "application/json");
    uploadNewPasswordRequest.send(JSON.stringify({"userPassword": newPassword.value, "userOldPassword": oldPassword.value}));
    uploadNewPasswordRequest.onload = function()
    {
        console.log(uploadNewPasswordRequest.responseText);
        rst = JSON.parse(uploadNewPasswordRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                //alert("密碼修改成功");
                //window.location.reload();
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "401": case 401:
                alert("舊密碼錯誤，請再次確認");
                break;
            case "402": case 402:
                //alert("密碼未更改");
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "403": case 403:
                alert("密碼長度需在8~30字元之間，且包含數字、大小寫字母及特殊符號，請再次確認");
                break;
            case "300": case 300:
            case "400": case 400:
            case "404": case 404:
            default:
                alert("系統錯誤，密碼修改失敗");
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

    var uploadUserEmailRequest = new XMLHttpRequest();
    uploadUserEmailRequest.open("POST", "/account/setting/accountMail");
    uploadUserEmailRequest.setRequestHeader("Content-Type", "application/json");
    uploadUserEmailRequest.send(JSON.stringify({"userMail": userEmail.value}));
    uploadUserEmailRequest.onload = function()
    {
        finished++;
        console.log(uploadUserEmailRequest.responseText);
        rst = JSON.parse(uploadUserEmailRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                //alert("電子信箱修改成功");
                //window.location.reload();
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "401": case 401:
            case "402": case 402:
                alert("電子信箱格式不符，長度不得超過50字元，請再次確認");
                break;
            case "403": case 403:
                //alert("電子信箱並未修改，請再次確認");
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "404": case 404:
                alert("此電子信箱已被使用");
                break;
            case "300": case 300:
            case "400": case 400:
            case "405": case 405:
            default:
                alert("系統錯誤，電子信箱修改失敗");
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

    var uploadUserPhoneRequest = new XMLHttpRequest();
    uploadUserPhoneRequest.open("POST", "/account/setting/accountPhone");
    uploadUserPhoneRequest.setRequestHeader("Content-Type", "application/json");
    uploadUserPhoneRequest.send(JSON.stringify({"userPhone": userPhone.value}));
    uploadUserPhoneRequest.onload = function()
    {
        finished++;
        console.log(uploadUserPhoneRequest.responseText);
        rst = JSON.parse(uploadUserPhoneRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                //alert("電話號碼修改成功");
                //window.location.reload();
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "401": case 401:
                alert("電話號碼格式不符，請再次確認");
                break;
            case "402": case 402:
                //alert("電話號碼未更改");
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "300": case 300:
            case "400": case 400:
            case "403": case 403:
                alert("系統錯誤，電話號碼修改失敗");
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

    var uploadUserGenderRequest = new XMLHttpRequest();
    uploadUserGenderRequest.open("POST", "/account/setting/userGender");
    uploadUserGenderRequest.setRequestHeader("Content-Type", "application/json");
    uploadUserGenderRequest.send(JSON.stringify({"userGender": checkGender}));
    uploadUserGenderRequest.onload = function()
    {
        finished++;
        console.log(uploadUserGenderRequest.responseText);
        rst = JSON.parse(uploadUserGenderRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                //alert("性別修改成功");
                //window.location.reload();
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "401": case 401:
                alert("未知的性別，請再次確認");
                break;
            case "402": case 402:
                //alert("性別未更改");
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "300": case 300:
            case "400": case 400:
            case "403": case 403:
            default:
                alert("系統錯誤，性別修改失敗");
                break;
        }
    }
}

function birthdatTest(birthday)
{
    var birthRegexp = /^((18|19|20)[0-9]{2})[-\/\.](0?[1-9]|1[012])[-\/\.](0?[1-9]|[12][0-9]|3[01])$/; // Oldest person in the world: 1897/04/19
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
    
    var uploadUserBirthdayRequest = new XMLHttpRequest();
    uploadUserBirthdayRequest.open("POST", "/account/setting/userBirthday");
    uploadUserBirthdayRequest.setRequestHeader("Content-Type", "application/json");
    uploadUserBirthdayRequest.send(JSON.stringify({"userBirthday": userBirthday.value}));
    uploadUserBirthdayRequest.onload = function()
    {
        finished++;
        console.log(uploadUserBirthdayRequest.responseText);
        rst = JSON.parse(uploadUserBirthdayRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                //alert("生日修改成功");
                //window.location.reload();
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "401": case 401:
                alert("生日格式不符，請再次確認，避免輸入過於古老的日期");
                break;
            case "402": case 402:
                alert("生日格式不符，請再次確認，避免輸入未來的日期");
                break;
            case "403": case 403:
                //alert("生日未更改");
                if (finished == 7)
                    alert("設定已完成");
                break;
            case "300": case 300:
            case "400": case 400:
            case "404": case 404:
            default:
                alert("系統錯誤，生日修改失敗");
                break;
        }
    }
}

function getPropicMyself(userID)
{
    var getPropicRequest = new XMLHttpRequest();
    getPropicRequest.open("POST", "/account/propic_exist");
    getPropicRequest.setRequestHeader("Content-Type", "application/json");
    getPropicRequest.send(JSON.stringify({"userID": userID}));
    getPropicRequest.onload = function()
    {
        console.log(getPropicRequest.responseText);
        rst = JSON.parse(getPropicRequest.responseText);
        var d = new Date();
		var time = "";
		if (d.getHours() < 10) {
			time += "0" + d.getHours();
		}
		else{
			time += d.getHours();
		}
		if (d.getMinutes() < 10) {
			time += "0" + d.getMinutes();
		}
		else{
			time += d.getMinutes();
		}
		if (d.getSeconds() < 10) {
			time += "0" +d.getSeconds();
		}
		else{
			time += d.getSeconds();
		}
        switch (rst.rspCode)
        {
            case "200": case 200:
                if (rst.exist == "1") document.getElementById("profilePicture").src = "/static/img/propic/" + userID + ".jpg?v=" + time;
                else document.getElementById("profilePicture").src = "/static/img/propic/default.jpg";
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("無法取得照片存在");
                break;
        }
    }
}