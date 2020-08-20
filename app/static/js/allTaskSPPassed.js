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
    taskListRequest.open("POST", "/test/SP/output/passed");
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
                taskList = rst.taskPassed;
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
        pageNumber.innerHTML = "尚無以通過的任務";
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
    document.getElementById("gradingDiv").style.display = "none";
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
    document.getElementById("taskName" + index).innerHTML = currentTask.taskName;
    document.getElementById("taskTime" + index).innerHTML = currentTask.taskStartTime + " ~ " + currentTask.taskEndTime;
    document.getElementById("taskQuota" + index).innerHTML = currentTask.taskPoint;
    document.getElementById("taskSR" + index).innerHTML = currentTask.taskSR;
    document.getElementById("Location" + index).innerHTML = currentTask.taskLocation;
    document.getElementById("content" + index).innerHTML = currentTask.taskContent;

    if (currentTask.taskStatus == 2)
    {
        // Time up or not will be finished later.
        document.getElementById("done1" + index).removeAttribute("style"); // time up
        document.getElementById("done2" + index).removeAttribute("style");
        document.getElementById("undone1" + index).removeAttribute("style"); // time up
        document.getElementById("undone2" + index).removeAttribute("style");
        document.getElementById("cancel1" + index).removeAttribute("style"); // befortime up
        document.getElementById("cancel2" + index).removeAttribute("style");
        document.getElementById("comment1" + index).style.display = "none";
        document.getElementById("comment2" + index).style.display = "none";
    }
    else if (currentTask.taskStatus == 14)
    {
        document.getElementById("done1" + index).style.display = "none";
        document.getElementById("done2" + index).style.display = "none";
        document.getElementById("undone1" + index).style.display = "none";
        document.getElementById("undone2" + index).style.display = "none";
        document.getElementById("cancel1" + index).style.display = "none";
        document.getElementById("cancel2" + index).style.display = "none";
        document.getElementById("comment1" + index).style.display = "none";
        document.getElementById("comment2" + index).style.display = "none";
    }
    else
    {
        document.getElementById("done1" + index).style.display = "none";
        document.getElementById("done2" + index).style.display = "none";
        document.getElementById("undone1" + index).style.display = "none";
        document.getElementById("undone2" + index).style.display = "none";
        document.getElementById("cancel1" + index).style.display = "none";
        document.getElementById("cancel2" + index).style.display = "none";
        document.getElementById("comment1" + index).removeAttribute("style");
        document.getElementById("comment2" + index).removeAttribute("style");
    }
}

function cancelTask(index)
{
    var cancelTaskRequest;
    if (window.XMLHttpRequest)
        cancelTaskRequest = new XMLHttpRequest();
    else
        cancelTaskRequest = new ActiveXObject("Microsoft.XMLHTTP");
    cancelTaskRequest.open("POST", "/test/SP/cancel_task");
    cancelTaskRequest.setRequestHeader("Content-Type", "application/json");
    cancelTaskRequest.send(JSON.stringify({"taskID": thisPageList[index].taskID, "userID": userID}));
    cancelTaskRequest.onload = function()
    {
        showError(200);
        console.log(cancelTaskRequest.responseText);
        rst = JSON.parse(cancelTaskRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("任務取消已送出，等待雇員回應");
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
    var finishTaskRequest;
    if (window.XMLHttpRequest)
        finishTaskRequest = new XMLHttpRequest();
    else
        finishTaskRequest = new ActiveXObject("Microsoft.XMLHTTP");
    finishTaskRequest.open("POST", "/test/task_finish_or_not");
    finishTaskRequest.setRequestHeader("Content-Type", "application/json");
    console.log(type)
    finishTaskRequest.send(JSON.stringify({"taskID": thisPageList[index].taskID, "status": type + "", "userID": userID}));
    finishTaskRequest.onload = function()
    {
        showError(200);
        console.log(finishTaskRequest.responseText);
        rst = JSON.parse(finishTaskRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("任務結束，請評論");
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
function openGradingDiv(index)
{
    gradingTask = index;
    document.getElementById("gradingDiv").removeAttribute("style");
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
    var sendGradeRequest;
    if (window.XMLHttpRequest)
        sendGradeRequest = new XMLHttpRequest();
    else
        sendGradeRequest = new ActiveXObject("Microsoft.XMLHTTP");
    sendGradeRequest.open("POST", "/test/comment_action");
    sendGradeRequest.setRequestHeader("Content-Type", "application/json");
    sendGradeRequest.send(JSON.stringify({"taskID": thisPageList[index].taskID, "comment": comment.value, "star": star + "", "userID": userID}));
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