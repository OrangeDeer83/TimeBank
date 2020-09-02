window.onload = function()
{
    showListDiv();
}

//const error = document.getElementById("error");
var applicationList = [];
var applicationAmount = 0;
var pageAmount = 0;
var thisPageList = [];
var currentPage = 1;

function showError(rspCode)
{
    switch (rspCode)
    {
        case   200: error.innerHTML = '已就緒...'; return ;
        case   300: error.innerHTML = '系統錯誤'; return ;
        case   400: error.innerHTML = '等待伺服器回應...'; return ;
        case 40012: error.innerHTML = "系統錯誤，無法同意評論管理員申請"; return ;
        case 40112: error.innerHTML = "未知的評論管理員，請稍後再試"; return ;
        case 40013: error.innerHTML = "系統錯誤，無法拒絕評論管理員申請"; return ;
        case 40113: error.innerHTML = "未知的評論管理員，請稍後再試"; return ;
        case 40016: error.innerHTML = "系統錯誤，無法讀取申請列表"; return ;
    }
}

function showListDiv()
{
    const table = document.getElementById('applicantTable');
    table.innerHTML = '';
    for (var i = 0; i < 10; i++)
    {
        table.innerHTML += '' +
        '<tr id="list' + i + '" style="display:none"><td>' +
            '<div class="managerName">管理員名稱：<span id="managerName' + i + '"></span></div>' +
            '<div class="phone">電話號碼：<span id="managerPhone' + i + '"></span></div>' +
            '<div class="email">電子郵件：<span id="managerEmail' + i + '"></span></div>' +
            '<div class="button">' +
                '<input type="button" class="agree" onclick="approve(' + i + ')" value="同意" />' +
                '<input type="button" class="reject" onclick="reject(' + i + ')" value="拒絕" />' +
            '</div>' +
        '</td></tr>';
    }
    table.innerHTML += '' +
    '<tr><td class="pageTr">' +
        '<button class="pageButton" id="prePageButton" onclick="computePage(1)">上一頁</button>' +
            '<span class="formPageNumber" id="pageNumber">1/1</span>' +
        '<button class="pageButton" id="nextPageButton" onclick="computePage(2)">下一頁</button>' +
    '</td></tr>';
    getGMList();
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
    if (pageAmount == 0)
    {
        document.getElementById("pageNumber").innerHTML = '1/1';
        document.getElementById('applicantTable').innerHTML = '<tr><td目前無申請</td></tr>' +
        '<tr><td class="pageTr">' +
            '<button class="pageButton" id="prePageButton" onclick="computePage(1)">上一頁</button>' +
                '<span class="formPageNumber" id="pageNumber">1/1</span>' +
            '<button class="pageButton" id="nextPageButton" onclick="computePage(2)">下一頁</button>' +
        '</td></tr>';
    }
    else
        document.getElementById("pageNumber").innerHTML = currentPage + "/" + pageAmount;
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
        document.getElementById("list" + i).removeAttribute('style');
    for (var i = thisPageList.length; i < maxPageAmount; i++)
        document.getElementById("list" + i).style.display = "none";
}
function showThisPageList()
{
    if (pageAmount == 0) return ;
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