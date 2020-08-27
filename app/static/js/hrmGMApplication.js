window.onload = function()
{
    getGMList();
}

//const error = document.getElementById("error");
const pageNumber = document.getElementById("pageNumber");
var applicationList = [];
var applicationAmount = 0;
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
        case 40012: error.innerHTML = "系統錯誤，無法同意評論管理員申請"; return ;
        case 40112: error.innerHTML = "未知的評論管理員，請稍後再試"; return ;
        case 40013: error.innerHTML = "系統錯誤，無法拒絕評論管理員申請"; return ;
        case 40113: error.innerHTML = "未知的評論管理員，請稍後再試"; return ;
        case 40016: error.innerHTML = "系統錯誤，無法讀取申請列表"; return ;
    }
}

// Get application list from server.
function getGMList()
{
    var getALRequest = new XMLHttpRequest();
    getALRequest.open("GET", "http://192.168.1.144:5000/HRManage/GM_apply_list");
    getALRequest.setRequestHeader("Content-Type", "application/json");
    getALRequest.send();
    getALRequest.onload = function()
    {
        showError(200);
        console.log(getALRequest.responseText);
        rst = JSON.parse(getALRequest.responseText);
        if (rst.rspCode == "200" || rst.rspCode == 200)
        {
            applicationAmount = rst.applyList.length;
            pageAmount = Math.ceil(applicationAmount / 10);
            applicationList = rst.applyList;
            if (applicationAmount == 0)
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
            thisPageList.push(applicationList[applicationAmount - maxPageAmount * (currentPage - 1) - i - 1]);
    else
        for (var i = 0; i < (applicationAmount % maxPageAmount); i++)
            thisPageList.push(applicationList[applicationAmount - maxPageAmount * (currentPage - 1) - i - 1]);

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

function approve(index)
{
    var approveRequest = new XMLHttpRequest();
    approveRequest.open("POST", "http://192.168.1.144:5000/HRManage/approveGM");
    approveRequest.setRequestHeader("Content-Type", "application/json");
    approveRequest.send(JSON.stringify({"GMID": thisPageList[index].adminID}));
    approveRequest.onload = function()
    {
        showError(200);
        console.log(approveRequest.responseText);
        rst = JSON.parse(approveRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("已同意並新增評論管理員：" + thisPageList[index].adminName);
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                showError(40012); break;
            case "401": case 401:
                showError(40112); break;
        }
    }
    showError(400);
}

function reject(index)
{
    var rejectRequest = new XMLHttpRequest();
    rejectRequest.open("POST", "http://192.168.1.144:5000/HRManage/rejectGM");
    rejectRequest.setRequestHeader("Content-Type", "application/json");
    rejectRequest.send(JSON.stringify({"GMID": thisPageList[index].adminID}));
    rejectRequest.onload = function()
    {
        showError(200);
        console.log(rejectRequest.responseText);
        rst = JSON.parse(rejectRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("已拒絕 " + thisPageList[index].adminName + " 的評論管理員申請");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                showError(40013); break;
            case "401": case 401:
                showError(40113); break;
        }
    }
    showError(400);
}