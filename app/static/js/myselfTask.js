window.onload = function()
{
    getUserID();
    getProfile();
    getPropicMyself();
    showListDiv();
    document.getElementById('hrefMyselfSR').innerHTML = '<a href="/USER/SR/myself/' + getToken() + '">雇主評分</a>';
    document.getElementById('hrefMyselfSP').innerHTML = '<a href="/USER/SP/myself/' + getToken() + '">雇員評分</a>';
}

var taskList = [];
var taskAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById("pageNumber");
const maxPageAmount = 10;

function getToken()
{
    var location = window.location.href;
    var token = "";
    var i = 0;
    while (i != location.length)
    {
        if (location[i] != "/" && location != "?")
            token += location[i];
        else
            token = "";
        i++;
    }
    return token;
}

function showListDiv()
{
    const table = document.getElementById('task');
    table.innerHTML = '';
    for (var i = 0; i < 10; i++)
    {
        table.innerHTML += '' +
        '<tr id="taskList' + i + '" style="display:none;"><td>' +
            '<div>任務名稱：<span id="taskName' + i + '"></span></div>' +
            '<div>任務時間：<span id="taskTime' + i + '"></span></div>' +
            '<div class="taskBottom">' +
                '<div class="point">任務點數：<span id="taskQuota' + i + '"></span></div>' +
                '<div class="bottonTask" id="taskTaskButton' + i + '" onclick="takeTask(' + i + ')">接任務</div>' +
            '</div>' +
        '</td></tr>';
    }
    getTaskList();
}

function getTaskList()
{
    var getTaskRequest = new XMLHttpRequest();
    getTaskRequest.open("POST", "http://192.168.1.144:5000/profile/output/task");
    getTaskRequest.setRequestHeader("Content-Type", "application/json");
    getTaskRequest.send(JSON.stringify({"userID": getToken()}));
    getTaskRequest.onload = function()
    {
        console.log(getTaskRequest.responseText);
        rst = JSON.parse(getTaskRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                taskList = rst.taskWaiting;
                taskAmount = taskList.length;
                pageAmount = Math.ceil(taskAmount / maxPageAmount);
                computePage(0);
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("無法取得使用者介紹");
                break;
            case "401": case 401:
                console.log("錯誤的userID");
                break;
        }
    }
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
        pageNumber.innerHTML = "1/1";
        document.getElementById('task').innerHTML = '<tr><td>尚無已發任務</td></tr>';
    }
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
    if (pageAmount == 0) return ;
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
}

function takeTask(index)
{
    var taskTaskRequest = new XMLHttpRequest();
    taskTaskRequest.open("POST", "http://192.168.1.144:5000/task/SP/taken_task");
    taskTaskRequest.setRequestHeader("Content-Type", "application/json");
    taskTaskRequest.send(JSON.stringify({"taskID": thisPageList[index].taskID,"userID": getToken()}));
    taskTaskRequest.onload = function()
    {
        console.log(taskTaskRequest.responseText);
        rst = JSON.parse(taskTaskRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("成功送出承接任務之申請：" + thisPageList[index].taskName);
                break;
            case "300": case 300:
            case "400": case 400:
                break;
            case "401": case 401:
                alert("此任務已申請過：" + thisPageList[index].taskName);
                break;
            default:
                alert("系統錯誤，請稍後再試");
            }
    }
}