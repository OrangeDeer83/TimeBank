// For hrmAdmin. (hrmManager)

window.onload = function()
{
    showError(400);
    document.getElementById('checkSAPassword').style.display = 'none';
    getAdminAmount();
}

const error = document.getElementById("error");
function showError(type)
{
    switch (type)
    {
        case 200: // hide error.
            error.innerHTML = "";
            break;
        case 400: // wait for server
            error.innerHTML = "等待伺服器回應中";
            break;
        // addAdmin
        case 4001:
            error.innerHTML = "系統錯誤，管理員新增失敗，請稍後再試";
            break;
        case 4011:
            error.innerHTML = "請選擇權限";
            break;
        case 4021:
            error.innerHTML = "使用者名稱格式錯誤，應為1~20字元，請避免使用其他語言，僅接受英、數字與符號";
            break;
        case 4031:
            error.innerHTML =
            "密碼格式不符，需為8~30字元，且包含大小寫字母、數字與特殊符號，可使用預設密碼\"Admin.1234\"以方便記憶";
            break;
        case 4041:
            error.innerHTML = "使用者帳號重複，請再次輸入";
            break;
        // deleteAdmin
        case 4002:
            error.innerHTML = "系統錯誤，管理員刪除失敗，請稍後再試";
            break;
        case 4012: case 4022:
            error.innerHTML = "資料庫中無此管理員，請勿修改網頁原始碼";
            break;
        case 4032:
            error.innerHTML = "請輸入您的密碼以刪除管理員";
            document.getElementById("checkSAPassword").style.display = "block";
            break;
        case 4042: case 4027:
            error.innerHTML = "使用者帳號重複，請再次輸入";
            break;
        // check admin name repeat
        case 4007:
            error.innerHTML = "系統錯誤，無法名稱是否重複";
            break;
        case 30022: case 40022:
            error.innerHTML = "系統錯誤，無法驗證密碼";
            break;
        case 40122:
            error.innerHTML = "密碼錯誤，請再試一次";
            break;
    }
}

var adminList = [];
var adminAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
var pageNumber = document.getElementById("pageNumber");

// Get amount of admins.
function getAdminAmount()
{
    var getAdminAmountRequest = new XMLHttpRequest();
    getAdminAmountRequest.open("GET", "http://192.168.1.144:5000/HRManage/Admin_list");
    getAdminAmountRequest.setRequestHeader("Content-Type", "application/json");
    getAdminAmountRequest.send();
    getAdminAmountRequest.onload = function()
    {
        showError(200);
        console.log(getAdminAmountRequest.responseText);
        rst = JSON.parse(getAdminAmountRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("管理員數量讀取成功");
                adminList = rst.AdminList;
                adminAmount = adminList.length;
                pageAmount = Math.ceil(adminAmount / 10);
                if (adminAmount == 0)
                    return;
                showListDiv();
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("系統錯誤，管理員數量讀取失敗，請稍後再試");
                return false;
        }
    }
    console.log("正在等待伺服器回傳管理員數量");
    showError(400);
}

// Add html element
function showListDiv()
{
    const table = document.getElementById('infoTable');
    table.innerHTML = '';
    for (var i = 0; i < 10; i++)
    {
        table.innerHTML += '' +
        '<tr class="list" id="list' + i + '" style="displat:none;"><td>' +
            '<div class="authority" id="authority' + i + '">權限：</div>' +
            '<div class="userName" id="userName' + i + '">使用者帳號：</div>' +
            '<div id="reset">更改密碼：<input type="text" id="newPassword' + i + '" placeholder="輸入新密碼" /></div>' +
            '<div class="delete" id="delete' + i + '" onclick="deleteAdmin(' + i + ')">刪除</div>' +
            '<div id="resetButton"><input type="submit" value="更改密碼" onclick="changePassword(' + i + ')" /></div>' +
        '</td></tr>';
    }
    table.innerHTML += '<tr><td>' +
        '<div id="changePageDiv">' +
            '<button class="pageButton" id="prePageButton" onclick="computePage(1)">上一頁</button>' +
            '<span class="formPageNumber" id="pageNumber">1/1</span>' +
            '<button class="pageButton" id="nextPageButton" onclick="computePage(2)">下一頁</button>' +
        '</div>' +
    '</td></tr>';
    computePage(0);
}

// Compute and react nextPage button, prevOage button and number of pages.
function computePage(type)
{
    // type 0: just compute,
    //      1: changePageButton Prev click,
    //      2: changePageButton next click.
    switch (type)
    {
        case 1:
            if (currentPage == 1) return false;
            else currentPage--;
            break;
        case 2:
            if (currentPage == pageAmount) return false;
            else currentPage++;
            break;
    }
     pageNumber.innerHTML = currentPage + "/" + pageAmount;
     computeThisPageList();
}

// Compute the index of this page.
function computeThisPageList()
{
    thisPageList.length = 0;
    var maxPageAmount = 10;
    if (currentPage < pageAmount)
        for (var i = 0; i < maxPageAmount; i++)
            thisPageList.push(adminList[maxPageAmount * (currentPage - 1) + i]);
    else
    {
        if (adminAmount % maxPageAmount != 0)
            for (var i = 0; i < (adminAmount % maxPageAmount); i++)
                thisPageList.push(adminList[maxPageAmount * (currentPage - 1) + i]);
        else if (adminAmount % maxPageAmount == 0)
            for (var i = 0; i < 10; i++)
                thisPageList.push(adminList[maxPageAmount * (currentPage - 1) + i]);
    }
    getNewList();

    for (var i = 0; i < thisPageList.length; i++)
        document.getElementById("list" + i).style.display = "";
    for (var i = thisPageList.length; i < maxPageAmount; i++)
        document.getElementById("list" + i).style.display = "none";
}

// Call getDetail to print the information of this page.
function getNewList()
{
    for (var i = 0; i < thisPageList.length; i++) getDetail(i);
}

function getDetail(index)
{
    var adminType;
    switch (thisPageList[index].adminType)
    {
        case 2: adminType = "AS"; break;
        case 3: adminType = "AA"; break;
        case 4: adminType = "AU"; break;
        case 5: adminType = "AG"; break;
    }
    document.getElementById("authority" + index).innerHTML = "權限：" + adminType;
    document.getElementById("userName" + index).innerHTML = "使用者名稱：" + thisPageList[index].adminName;
    document.getElementById('newPassword' + index).value = '';
}

// Add Admin.
const adminTypeSelect = document.getElementById("selectPermission");
var adminType, adminText;
var adminUserName = document.getElementById("addUserName");
var adminPassword = document.getElementById("addPassword");
adminUserName.addEventListener("input", adminUserNameVerify);
adminPassword.addEventListener("input", adminPasswordVerify);
const passwordRegexp = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\w).{8,30}$/;

function addAdmin()
{
    adminType = adminTypeSelect.options[adminTypeSelect.selectedIndex].value;
    adminText = adminTypeSelect.options[adminTypeSelect.selectedIndex].text;
    if (adminType == -1)
    {
        showError(4011);
        return;
    }
    if (adminUserName.value.length < 1 || adminUserName.value.length > 20)
    {    
        showError(4021);
        return ;
    }
    if (adminPassword.value.match(passwordRegexp) == null)
    {    
        showError(4031);
        return;
    }

    var addAdminRequest = new XMLHttpRequest();
    addAdminRequest.open("POST", "http://192.168.1.144:5000/HRManage/create/Admin");
    addAdminRequest.setRequestHeader("Content-Type", "application/json");
    console.log(adminType + adminUserName.value + adminPassword.value);
    addAdminRequest.send(JSON.stringify({"adminType": adminType, "adminName": adminUserName.value, "adminPassword": adminPassword.value}));
    addAdminRequest.onload = function()
    {
        showError(200);
        console.log(addAdminRequest.responseText);
        rst = JSON.parse(addAdminRequest.responseText);
        switch (rst.rspCode)
        {// 200:管理員新增成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:adminType異常 | 402:帳號格式不符 | 403:密碼格式不符 | 404:帳號重複
            case "200": case 200:
                alert("管理員新增成功：" + adminText + " 帳號：" + adminUserName.value + " 密碼：" + adminPassword.value);
                window.location.reload();
                break;
            case "401": case 401:
                showError(4011);
                break;
            case "402": case 402:
                showError(4021);
                adminUserName.focus();
                break;
            case "403": case 403:
                showError(4031);
                adminPassword.focus();
                break;
            case "404": case 404:
                showError(4041);
                adminUserName.focus();
                break;
            case "300": case 300:
            case "400": case 400:
                showError(4001);
                break;
        }
        return ;
    }
    showError(400);
}
function adminUserNameVerify()
{
    if (adminUserName.value.length < 1 || adminUserName.value.length > 20) showError(4021);
    else showError(200);
    checkUserName();
}
function adminPasswordVerify()
{
    if (adminPassword.value.match(passwordRegexp) != null)
        showError(200);
}

function changePassword(index)
{
    const newPassword = document.getElementById('newPassword' + index).value;
    if (newPassword.match(passwordRegexp) == null)
    {
        alert('新密碼格式錯誤');
        return ;
    }

    var changePasswordRequest = new XMLHttpRequest();
    changePasswordRequest.open('POST', 'http://192.168.1.144:5000/HRManage/changePassword');
    changePasswordRequest.setRequestHeader('Content-Type', 'application/json');
    changePasswordRequest.send(JSON.stringify({'adminID': thisPageList[index].adminID, 'newPassword': newPassword}));
    changePasswordRequest.onload = function()
    {
        console.log(changePasswordRequest.responseText);
        rst = JSON.parse(changePasswordRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                document.getElementById('newPassword' + index).value = '';
                break;
            case '18': case 18:
                document.getElementById("checkSAPassword").style.display = "block";
            default:
                console.log('無法更改密碼');
                break;
        }
    }
}

// Delete admin.
function deleteAdmin(index)
{
    var deleteRequest = new XMLHttpRequest();
    deleteRequest.open("POST", "http://192.168.1.144:5000/HRManage/delete/Admin");
    deleteRequest.setRequestHeader("Content-Type", "application/json");
    deleteRequest.send(JSON.stringify({"adminID": thisPageList[index].adminID}));
    deleteRequest.onload = function()
    {
        showError(200);
        console.log(deleteRequest.responseText);
        rst = JSON.parse(deleteRequest.responseText);
        switch (rst.rspCode)
        {// 200:刪除成功 | 300:method使用錯誤 | 400:資料庫錯誤 | 401:adminUserName不在資料庫中，前端可能遭到竄改 | 402:該帳號目前不是admin | 403:尚未輸入第一次密碼 | 404:密碼輸入錯誤
            case "200": case 200:
                alert("管理員刪除成功");
                window.location.reload();
                break;
            case "401": case 401:
                showError(4012);
                break;
            case "402": case 402:
                showError(4022);
                break;
            case "403": case 403:
                showError(4032);
                break;
            case "300": case 300:
            case "400": case 400:
                showError(4002)
        }
    }
    showError(400);
}

function checkPassword()
{
    var checkPasswordRequest = new XMLHttpRequest();
    checkPasswordRequest.open("POST", "http://192.168.1.144:5000/HRManage/delete/Admin/check_password");
    checkPasswordRequest.setRequestHeader("Content-Type", "application/json");
    checkPasswordRequest.send(JSON.stringify({"SAID": "5", "SAPassword": document.getElementById("password").value}));
    checkPasswordRequest.onload = function()
    {
        showError(200);
        console.log(checkPasswordRequest.responseText);
        rst = JSON.parse(checkPasswordRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("密碼驗證成功");
                document.getElementById("checkSAPassword").style.display = "none";
                break;
            case "300": case 300:
                showError(30022);
                break;
            case "400": case 400:
                showError(40022);
                break;
            case "401": case 401:
                showError(40122);
                break;
        }
    }
    showError(400);
}

function checkUserName()
{
    var checkUserNameRequest = new XMLHttpRequest();
    checkUserNameRequest.open("POST", "http://192.168.1.144:5000/account/Admin/detect_repeated");
    checkUserNameRequest.setRequestHeader("Content-Type", "application/json");
    checkUserNameRequest.send(JSON.stringify({"adminName": adminUserName.value}));
    checkUserNameRequest.onload = function()
    {
        showError(200);
        console.log(checkUserNameRequest.responseText);
        var rst = JSON.parse(checkUserNameRequest.responseText);
        showError(200);
        switch (rst.rspCode)
        {
            case "200": // UserName no repeat
                showError(200);
                break;
            case "300": // Wrong method.
            case "400": // Database wrong.
                showError(4007);
                break;
            case "401": // Format of UserName is illegal
                showError(4017);
                break;
            case "402": // UserName repeat
                showError(4027);
                break;
        }
    }
    showError(400);
}