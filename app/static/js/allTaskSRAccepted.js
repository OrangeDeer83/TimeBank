window.onload = function()
{
    document.getElementById("rating").style.display = "none";
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
    const table = document.getElementById('ePass');
    table.innerHTML = '';
    for (var i = 0; i < 10; i++)
    {
        table.innerHTML += '' +
        '<tr id="taskList' + i + '"><td>' +
            '<div class="introduction">' +
                '<div>雇員：<span id="taskSP' + i + '"></span></div>' +
                '<div>任務名稱：<span id="taskName' + i + '"></span></div>' +
                '<div>任務時間：<span id="taskTime' + i + '"></span></div>' +
                '<div>任務額度：<span id="taskQuota' + i + '"></span>點</div>' +
            '</div>' +
            '<div class="detailed">            ' +
                '<div>任務地點：<span id="taskLocation' + i + '"></span></div>' +
                '<div>' +
                    '<div>任務內容：<span id="content' + i + '"></span></div><br>' +
                    '<div>' +
                        '<div class="button" id="comment' + i + '" onclick="openRating(' + i + ')" style="display:none;">評論</div>' +
                        '<div class="button" id="undone' + i + '" onclick="finishTask(' + i + ', 0)" style="display:none;">未完成</div>' +
                        '<div class="button" id="done' + i + '" onclick="finishTask(' + i + ', 1)" style="display:none;">完成</div>' +
                        '<div class="button" id="cancel' + i + '" onclick="cancelTask(' + i + ')" style="display:none;">取消任務</div>' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</td></tr>';
    }
    getTaskList();
}

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
    var taskListRequest = new XMLHttpRequest();
    taskListRequest.open("GET", "http://192.168.1.144:5000/task/SR/output/accept");
    taskListRequest.setRequestHeader("Content-Type", "application/json");
    taskListRequest.send();
    taskListRequest.onload = function()
    {
        showError(200);
        console.log(taskListRequest.responseText);
        rst = JSON.parse(taskListRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                showError(20029);
                taskList = rst.taskList;
                taskAmount = taskList.length;
                pageAmount = Math.ceil(taskAmount / maxPageAmount);
                computePage(0);
                break;
            case "300": case 300:
            case "400": case 400:
                showError(30029);
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
        pageNumber.innerHTML = "尚無已接受之任務";
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
    var currentTask = thisPageList[index];
    var startTime = currentTask.taskStartTime;
    var endTime = currentTask.taskEndTime;
    document.getElementById("taskName" + index).innerHTML = currentTask.taskName;
    document.getElementById("taskTime" + index).innerHTML = getDate(startTime) + " ~ " + getDate(endTime);
    document.getElementById("taskQuota" + index).innerHTML = currentTask.taskPoint;
    document.getElementById("taskSP" + index).innerHTML = currentTask.taskSPName;
    document.getElementById("taskLocation" + index).innerHTML = currentTask.taskLocation;
    document.getElementById("content" + index).innerHTML = currentTask.taskContent;

    var taskStatus = currentTask.taskStatus;
    if (taskStatus == 2)
    {
        if (startTime <= Date.now()) // startTime is passed;
        {
            document.getElementById("done" + index).removeAttribute("style");
            document.getElementById("undone" + index).removeAttribute("style");
            document.getElementById("cancel" + index).style.display = "none";
        }
        else
        {
            document.getElementById("done" + index).style.display = "none";
            document.getElementById("undone" + index).style.display = "none";
            document.getElementById("cancel" + index).removeAttribute("style");
        }
        document.getElementById("comment" + index).style.display = "none";
    }
    else if (taskStatus == 3 || taskStatus == 6 || taskStatus == 7 || taskStatus == 8 || taskStatus == 13 || taskStatus == 14)
    {
        document.getElementById("done" + index).style.display = "none";
        document.getElementById("undone" + index).style.display = "none";
        document.getElementById("cancel" + index).style.display = "none";
        if (currentTask.commentStatus == 1)
            document.getElementById("comment" + index).style.display = "none";
        else
            document.getElementById("comment" + index).removeAttribute("style");
    }
    else if (taskStatus == 15 || taskStatus == 16)
    {
        document.getElementById("done" + index).removeAttribute("style");
        document.getElementById("undone" + index).removeAttribute("style");
        document.getElementById("cancel" + index).style.display = "none";
        document.getElementById("comment" + index).style.display = "none";
    }
    else if (taskStatus == 9)
    {
        document.getElementById("done" + index).style.display = "none";
        document.getElementById("undone" + index).style.display = "none";
        document.getElementById("cancel" + index).removeAttribute("style");
        document.getElementById("comment" + index).style.display = "none";
    }
}

function getDate(time) {
    var now = new Date(time),
    y = now.getFullYear(time),
    m = ("0" + (now.getMonth(time) + 1)).slice(-2),
    d = ("0" + now.getDate(time)).slice(-2);
    return y + "-" + m + "-" + d + " " + now.toTimeString().substr(0, 8);
}

function cancelTask(index)
{
    var cancelTaskRequest = new XMLHttpRequest();
    cancelTaskRequest.open("POST", "http://192.168.1.144:5000/task/SR/cancel_task");
    cancelTaskRequest.setRequestHeader("Content-Type", "application/json");
    cancelTaskRequest.send(JSON.stringify({"taskID": thisPageList[index].taskID}));
    cancelTaskRequest.onload = function()
    {
        showError(200);
        console.log(cancelTaskRequest.responseText);
        rst = JSON.parse(cancelTaskRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("任務取消已送出");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert("無法取消任務");
        }
    }
    showError(400);
}

function finishTask(index, type)
{
    var finishTaskRequest = new XMLHttpRequest();
    finishTaskRequest.open("POST", "http://192.168.1.144:5000/task/task_finish_or_not");
    finishTaskRequest.setRequestHeader("Content-Type", "application/json");
    console.log(type)
    finishTaskRequest.send(JSON.stringify({"taskID": thisPageList[index].taskID, "status": type + ""}));
    finishTaskRequest.onload = function()
    {
        showError(200);
        console.log(finishTaskRequest.responseText);
        rst = JSON.parse(finishTaskRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("任務結束，請評論");
                document.getElementById('done' + index).style.display = 'none';
                document.getElementById('undone' + index).style.display = 'none';
                openRating(index);
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert("無法結束任務");
        }
    }
    showError(400);
}

function validated()
{
    // It will be done after all other pages are finished.
    // gradingTask != -1;
    // star 1~5
    return true;
}

var gradingTask = -1;
function openRating(index)
{
    gradingTask = index;
    document.getElementById("rating").removeAttribute("style");
    for (var i = 0; i < 10; i++)
        if (i != index)
            document.getElementById("taskList" + i).style.display = "none";
}
function sendGrade()
{
    var index = gradingTask;
    if (!validated())
        return ;

    const comment = document.getElementById("comment");
    var star = 0
    for (var i = 5; i >= 1; i--)
    {
        var radio = document.getElementById("star" + i)
        if (radio.checked)
        {
            star = i;
            i = -1;
        }
    }
    var sendGradeRequest = new XMLHttpRequest();
    sendGradeRequest.open("POST", "http://192.168.1.144:5000/comment/comment_action");
    sendGradeRequest.setRequestHeader("Content-Type", "application/json");
    sendGradeRequest.send(JSON.stringify({"taskID": thisPageList[index].taskID, "comment": comment.value, "star": star + ""}));
    sendGradeRequest.onload = function()
    {
        showError(200);
        console.log(sendGradeRequest.responseText);
        rst = JSON.parse(sendGradeRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("評論已送出");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert("系統錯誤，無法評論");
        }
    }
    showError(400);
}