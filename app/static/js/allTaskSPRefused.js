const userID = "8"; // Only for beta.

window.onload = function()
{
    getTaskList();
}

var taskList = [];
var taskAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById("pageNumber");
const maxPageAmount = 10;

/*const error = document.getElementById("error");
function showError(rspCode)
{
    error.style.color = "red";
    switch (rspCode)
    {
        case   200: error.innerHTML = "已就緒..."; error.style.color = ""; return ;
        case   300: error.innerHTML = "系統錯誤"; return ;
        case   400: error.innerHTML = "等待伺服器回應..."; error.style.color = ""; return ;
    }
}*/
function showError() {;}

function getTaskList()
{
    var taskListRequest;
    if (window.XMLHttpRequest)
        taskListRequest = new XMLHttpRequest();
    else
        taskListRequest = new ActiveXObject("Microsoft.XMLHTTP");
    taskListRequest.open("POST", "/test/SP/output/refused");
    taskListRequest.setRequestHeader("Content-Type", "application/json");
    taskListRequest.send(JSON.stringify({"userID": userID}));
    taskListRequest.onload = function()
    {
        showError(200);
        console.log(taskListRequest.responseText);
        rst = JSON.parse(taskListRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                showError(20036);
                taskList = rst.taskRefused;
                taskAmount = taskList.length;
                pageAmount = Math.ceil(taskAmount / maxPageAmount);
                computePage(0);
                break;
            case "300": case 300:
            case "400": case 400:
                showError(30036);
            }
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
        pageNumber.innerHTML = "尚無遭拒絕的申請";
    else
        pageNumber.innerHTML = currentPage + "/" + pageAmount;
    computeThisPageList();
}

// Compute the index of this page.
function computeThisPageList()
{
    thisPageList.length = 0;
    if (currentPage < pageAmount)
        for (var i = 0; i < maxPageAmount; i++)
            thisPageList.push(taskList[maxPageAmount * (currentPage - 1) + i]);
    else
        for (var i = 0; i < (taskAmount % maxPageAmount); i++)
            thisPageList.push(taskList[maxPageAmount * (currentPage - 1) + i]);

    showDetail();
}

function showDetail()
{
    for (var i = 0; i < thisPageList.length; i++)
    {
        putDetail(i);
        document.getElementById("taskList" + i).removeAttribute("style");
    }
    for (var i = thisPageList.length; i < maxPageAmount; i++)
        document.getElementById("taskList" + i).style.display = "none";
}

function putDetail(index)
{
    document.getElementById("taskName" + index).innerHTML = thisPageList[index].taskName;
    document.getElementById("taskTime" + index).innerHTML = thisPageList[index].taskStartTime + " ~ " + thisPageList[index].taskEndTime;
    document.getElementById("taskQuota" + index).innerHTML = thisPageList[index].taskPoint;
    document.getElementById("taskSR" + index).innerHTML = thisPageList[index].SRName;
    document.getElementById("taskLocation" + index).innerHTML = thisPageList[index].taskLocation;
    document.getElementById("taskContent" + index).innerHTML = thisPageList[index].taskContent;
}