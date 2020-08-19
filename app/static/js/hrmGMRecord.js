window.onload = function()
{
    getGMList();
}

//const error = document.getElementById("error");
const pageNumber = document.getElementById("pageNumber");
var GMList = [];
var GMAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;

function showError(rspCode)
{
    error.style.color = "#EECA00";
    switch (rspCode)
    {
        case   200: error.innerHTML = "已就緒..."; error.style.color = "white"; return ;
        case   300: error.innerHTML = "系統錯誤"; return ;
        case   400: error.innerHTML = "等待伺服器回應..."; error.style.color = "white"; return ;
        case 40017: error.innerHTML = "系統錯誤，無法讀取評論管理員列表"; return ;
        case 40018: error.innerHTML = "系統錯誤，無法刪除評論管理員"; return ;
        case 40118: error.innerHTML = "無法刪除評論管理員，請稍後再試"; return ;
        case 40318: error.innerHTML = "請輸入密碼以刪除評論管理員";
                    document.getElementById("checkPassword").style.display = "block"; return ;
        case 30022: error.innerHTML = "系統錯誤，無法驗證密碼"; break;
        case 40122: error.innerHTML = "密碼錯誤，請再試一次"; break;
    }
}

// Get GM list from server.
function getGMList()
{
    var getALRequest;
    if (window.XMLHttpRequest)
        getALRequest = new XMLHttpRequest();
    else
        getALRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getALRequest.open("GET", "http://192.168.1.146:5000/test/GM_list");
    getALRequest.setRequestHeader("Content-Type", "application/json");
    getALRequest.send();
    getALRequest.onload = function()
    {
        showError(200);
        console.log(getALRequest.responseText);
        rst = JSON.parse(getALRequest.responseText);
        if (rst.rspCode == "200" || rst.rspCode == 200)
        {
            GMAmount = rst.GMList.length;
            pageAmount = Math.ceil(GMAmount / 10);
            GMList = rst.GMList;
            if (GMAmount == 0)
            {
                error.innerHTML = "目前沒有申請";
                error.style.color = "#EECA00";
                return ;
            }
            computePage(0);
        }
        else showError(40016);
    }
    showError(400);
}

// Compute and react nextPage button, prePage button and number of pages.
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
    var maxPageAmount = 10; // 每頁最多幾個
    
    if (currentPage < pageAmount)
        for (var i = 0; i < maxPageAmount; i++)
            thisPageList.push(GMList[GMAmount - maxPageAmount * (currentPage - 1) - i - 1]);
    else
        for (var i = 0; i < (GMAmount % maxPageAmount); i++)
            thisPageList.push(GMList[GMAmount - maxPageAmount * (currentPage - 1) - i - 1]);

    showThisPageList();

    for (var i = 0; i < thisPageList.length; i++)
        document.getElementById("list" + i).style.display = "";
    for (var i = thisPageList.length; i < maxPageAmount; i++)
        document.getElementById("list" + i).style.display = "none";
}
function showThisPageList()
{
    for (var i = 0; i < thisPageList.length; i++)
    {
        document.getElementById("managerName" + i).innerHTML = thisPageList[i].adminName;
        document.getElementById("managerPhone" + i).innerHTML = thisPageList[i].adminPhone;
        document.getElementById("managerEmail" + i).innerHTML = thisPageList[i].adminMail;
    }
}

function deleteManager(index)
{
    var deleteManagerRequest;
    if (window.XMLHttpRequest)
        deleteManagerRequest = new XMLHttpRequest();
    else
        deleteManagerRequest = new ActiveXObject("Microsoft.XMLHTTP");
    deleteManagerRequest.open("POST", "http://192.168.1.146:5000/test/delete/GM");
    deleteManagerRequest.setRequestHeader("Content-Type", "application/json");
    deleteManagerRequest.send(JSON.stringify({"GMID": thisPageList[index].adminID, "adminID": "39"}));
    deleteManagerRequest.onload = function()
    {
        showError(200);
        console.log(deleteManagerRequest.responseText);
        rst = JSON.parse(deleteManagerRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("已刪除評論管理員：" + thisPageList[index].adminName);
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                showError(40012); break;
            case "401": case 401:
            case "402": case 402:
                showError(40118); break;
            case "403": case 403:
                showError(40318); break;
            
        }
    }
    showError(400);
}

function checkPassword()
{
    var checkPasswordRequest;
    if (window.XMLHttpRequest)
        checkPasswordRequest = new XMLHttpRequest();
    else
        checkPasswordRequest = new ActiveXObject("Microsoft.XMLHTTP");
    checkPasswordRequest.open("POST", "http://192.168.1.146:5000/test/delete/Admin/check_password");
    checkPasswordRequest.setRequestHeader("Content-Type", "application/json");
    checkPasswordRequest.send(JSON.stringify({"SAID": "5", "SAPassword": document.getElementById("deletePassword").value}));
    checkPasswordRequest.onload = function()
    {
        showError(200);
        console.log(checkPasswordRequest.responseText);
        rst = JSON.parse(checkPasswordRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("密碼驗證成功");
                document.getElementById("checkPassword").style.display = "none"; break;
            case "300": case 300:
            case "400": case 400:
                showError(30022); break;
            case "401": case 401:
                showError(40122); break;
        }
    }
    showError(400);
}