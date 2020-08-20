const userID = "10"; // Only for beta.

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
    taskListRequest.open("POST", "/test/SR/output/record");
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
                showError(20033);
                taskList = rst.taskRecord;
                taskAmount = taskList.length;
                pageAmount = Math.ceil(taskAmount / maxPageAmount);
                computePage(0);
                break;
            case "300": case 300:
            case "400": case 400:
                showError(30033);
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
        pageNumber.innerHTML = "尚無歷史紀錄";
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
    const currentTask = thisPageList[index];
    document.getElementById("taskName" + index).innerHTML = currentTask.taskName;
    document.getElementById("taskTime" + index).innerHTML = currentTask.taskStartTime + " ~ " + thisPageList[index].taskEndTime;
    document.getElementById("taskQuota" + index).innerHTML = currentTask.taskPoint;
    document.getElementById("taskSP" + index).innerHTML = currentTask.taskSP;
    document.getElementById("taskLocation" + index).innerHTML = currentTask.taskLocation;
    document.getElementById("taskContent" + index).innerHTML = currentTask.taskContent;
    document.getElementById("SRComment" + index).innerHTML = currentTask.SRComment;
    document.getElementById("SPComment" + index).innerHTML = currentTask.SPComment;
    for (var i = 0; i < currentTask.SRScore; i++)
    {
        document.getElementById("SRRate" + i + index).removeAttribute("style");
        document.getElementById("RLabel" + i + index).removeAttribute("style");
    }
    for (var i = currentTask.SRScore; i < 5; i++)
    {
        document.getElementById("SRRate" + i + index).style.display = "none";
        document.getElementById("RLabel" + i + index).style.display = "none";
    }
    for (var i = 0; i < currentTask.SPScore; i++)
    {
        document.getElementById("SPRate" + i + index).removeAttribute("style");
        document.getElementById("PLabel" + i + index).removeAttribute("style");
    }
    for (var i = currentTask.SPScore; i < 5; i++)
    {
        document.getElementById("SPRate" + i + index).style.display = "none";
        document.getElementById("PLabel" + i + index).style.display = "none";
    }
}

function report(index)
{
    // Not now.
    index++;
    alert("此功能尚未完成");
}