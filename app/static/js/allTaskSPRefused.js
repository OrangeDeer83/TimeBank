window.onload = function()
{
    showListDiv();
}

var taskList = [];
var taskAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById("pageNumber");
const maxPageAmount = 10;

function showListDiv()
{
    const table = document.getElementById('eRefused');
    for (var i = 0; i < 10; i++)
    {
        table.innerHTML += '' +
        '<tr id="taskList' + i + '" style="display:none"><td>' +
            '<div class="introduction">' +
                '<div>雇主：<span id="taskSR' + i + '"></span></div>' +
                '<div>任務名稱：<span id="taskName' + i + '"></span></div>' +
                '<div>任務時間：<span id="taskTime' + i + '"></span></div>' +
                '<div>任務額度：<span id="taskQuota' + i + '"></span>點</div>' +
            '</div>' +
            '<div class="detailed">' +
                '<div>任務地點：<span id="taskLocation' + i + '"></span></div>' +
                '<div>任務內容：<span id="taskContent' + i + '"></span></div>' +
            '</div>' +
        '</td></tr>';
    }
    getTaskList();
}

function showPrompt(index)
{
    var prompt = document.getElementById('systemPrompt');
    prompt.removeAttribute('style');
    switch (index)
    {
        case 200: prompt.innerHTML = '已就緒...'; return ;
        case 201: prompt.innerHTML = '尚無遭拒絕的申請'; return ;
        case 300: prompt.innerHTML = '系統錯誤'; return ;
        case 400: prompt.innerHTML = '等待伺服器回應...'; return ;
        case 401: prompt.innerHTML = '無法取得任務列表'; return ;
    }
}

function getTaskList()
{
    var taskListRequest = new XMLHttpRequest();
    taskListRequest.open("GET", "/task/SP/output/refused");
    taskListRequest.setRequestHeader("Content-Type", "application/json");
    taskListRequest.send();
    taskListRequest.onload = function()
    {
        showPrompt(200);
        console.log(taskListRequest.responseText);
        rst = JSON.parse(taskListRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                taskList = rst.taskRefused;
                taskAmount = taskList.length;
                pageAmount = Math.ceil(taskAmount / maxPageAmount);
                computePage(0);
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                showPrompt(401);
            }
    }
    showPrompt(400);
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
        showPrompt(201);
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
    document.getElementById("taskSR" + index).innerHTML = thisPageList[index].taskSR;
    document.getElementById("taskLocation" + index).innerHTML = thisPageList[index].taskLocation;
    document.getElementById("taskContent" + index).innerHTML = thisPageList[index].taskContent;
}