window.onload = function()
{
    console.log(" ")
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
    taskListRequest.open("GET", "/task/SR/output/release");
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
    document.getElementById("applySP" + index).length = 1;
    if (currentTask.taskStatus == 1 || currentTask.taskStatus == "1")
    {
        document.getElementById("edit1" + index).style.display = "none";
        document.getElementById("edit2" + index).style.display = "none";
        document.getElementById("applySP" + index)[0] = new Option("請選擇僱員", "");
        document.getElementById("taskName" + index).innerHTML = currentTask.taskName;
        document.getElementById("taskTime" + index).innerHTML = currentTask.taskStartTime + " ~ " + currentTask.taskEndTime;
        document.getElementById("taskQuota" + index).innerHTML = currentTask.taskPoint;
        document.getElementById("taskLocation" + index).innerHTML = currentTask.taskLocation;
        document.getElementById("taskContent" + index).innerHTML = currentTask.taskContent;
        for (var i = 0; i < currentTask.CandidateList.length; i++)
            document.getElementById("applySP" + index).add(new Option(currentTask.CandidateList[i][0], currentTask.CandidateList[i][1]));
    }
    else if (currentTask.taskStatus == 0 || currentTask.taskStatus == "0")
    {
        document.getElementById("edit1" + index).style.display = "block";
        document.getElementById("edit2" + index).style.display = "block";
        document.getElementById("applySP" + index)[0] = new Option("請選擇僱員", "");
        document.getElementById("taskName" + index).innerHTML = currentTask.taskName;
        document.getElementById("taskTime" + index).innerHTML = currentTask.taskStartTime + " ~ " + currentTask.taskEndTime;
        document.getElementById("taskQuota" + index).innerHTML = currentTask.taskPoint;
        document.getElementById("taskLocation" + index).innerHTML = currentTask.taskLocation;
        document.getElementById("taskContent" + index).innerHTML = currentTask.taskContent;
        document.getElementById("applySP" + index)[0] = new Option("尚無申請", "");
    }
    else document.getElementById("applySP" + index)[0] = new Option("尚無申請", "");
}

function selectSP(index)
{
    const candidateList = document.getElementById("applySP" + index);
    const selectedIndex = candidateList.selectedIndex;
    const candidate = candidateList[selectedIndex];
    if (candidateList.length == 1)
    {
        alert("此任務尚無人申請：" + thisPageList[index].taskName);
        return ;
    }
    if (selectedIndex == 0)
    {
        alert("請選擇僱員");
        return ;
    }

    var selectSPRequest;
    if (window.XMLHttpRequest)
        selectSPRequest = new XMLHttpRequest();
    else
        selectSPRequest = new ActiveXObject("Microsoft.XMLHTTP");
    selectSPRequest.open("POST", "/task/SR/decide_SP");
    selectSPRequest.setRequestHeader("Content-Type", "application/json");
    selectSPRequest.send(JSON.stringify({"taskID": thisPageList[index].taskID, "candidateID": candidate.value}));
    selectSPRequest.onload = function()
    {
        showError(200);
        console.log(selectSPRequest.responseText);
        rst = JSON.parse(selectSPRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert(thisPageList[index].taskName + "已成功選擇僱員：" + candidate.text);
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert(thisPageList[index].taskName + "僱員選擇失敗");
            }
    }
    showError(400);
}

function editTask(index)
{
    // It will be done after all other pages can run.
    alert("此功能尚未完成");
}

function deleteTask(index)
{
    var deleteTaskRequest;
    if (window.XMLHttpRequest)
        deleteTaskRequest = new XMLHttpRequest();
    else
        deleteTaskRequest = new ActiveXObject("Microsoft.XMLHTTP");
    deleteTaskRequest.open("POST", "/task/SR/delete_task");
    deleteTaskRequest.setRequestHeader("Content-Type", "application/json");
    deleteTaskRequest.send(JSON.stringify({"taskID": thisPageList[index].taskID}));
    deleteTaskRequest.onload = function()
    {
        showError(200);
        console.log(deleteTaskRequest.responseText);
        rst = JSON.parse(deleteTaskRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("已刪除任務：" + thisPageList[index].taskName);
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert("任務刪除失敗：" + thisPageList[index].taskName);
            }
    }
    showError(400);
}