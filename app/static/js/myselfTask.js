window.onload = function()
{
    getUserID();
}

// For all myself.
var userID;
function getUserID()
{
    var getIDRequest;
    if (window.XMLHttpRequest)
        getIDRequest = new XMLHttpRequest();
    else
        getIDRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getIDRequest.open("GET", "/test/getID");
    getIDRequest.setRequestHeader("Content-Type", "application/json");
    getIDRequest.send();
    getIDRequest.onload = function()
    {
        console.log(getIDRequest.responseText);
        rst = JSON.parse(getIDRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                userID = rst.ID;
                document.getElementById("userIDFile").value = userID;
                getProfile();
                getTaskList();
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                console.log("無法取得userID");
                /*userID = "10"; // for beta
                getProfile();
                getTaskList();*/
                break;
        }
    }
}

function getProfile()
{
    var getProfileRequest;
    if (window.XMLHttpRequest)
        getProfileRequest = new XMLHttpRequest();
    else
        getProfileRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getProfileRequest.open("POST", "/test/output");
    getProfileRequest.setRequestHeader("Content-Type", "application/json");
    getProfileRequest.send(JSON.stringify({"userID": userID}));
    getProfileRequest.onload = function()
    {
        console.log(getProfileRequest.responseText);
        rst = JSON.parse(getProfileRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                showProfile(rst);
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("無法取得使用者介紹");
                break;
        }
    }
}

function showProfile(profile)
{
    document.getElementById("name").innerHTML = profile.name;
    switch(profile.userGender * 1)
    {
        case 0: document.getElementById("gender").innerHTML = "男"; break;
        case 1: document.getElementById("gender").innerHTML = "女"; break;
        case 2: document.getElementById("gender").innerHTML = "其他"; break;
    }
    document.getElementById("age").innerHTML = profile.userAge;
    document.getElementById("profile").innerHTML = profile.userInfo;
    document.getElementById("profilePicture").src = "../static/img/propic/" + userID + ".jpg";
}

var taskList = [];
var taskAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById("pageNumber");
const maxPageAmount = 10;

function getTaskList()
{
    var getTaskRequest;
    if (window.XMLHttpRequest)
        getTaskRequest = new XMLHttpRequest();
    else
        getTaskRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getTaskRequest.open("POST", "/test/output/task");
    getTaskRequest.setRequestHeader("Content-Type", "application/json");
    getTaskRequest.send(JSON.stringify({"userID": userID}));
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
        pageNumber.innerHTML = "尚無已發任務";
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
}

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

function takeTask(index)
{
    var taskTaskRequest;
    if (window.XMLHttpRequest)
        taskTaskRequest = new XMLHttpRequest();
    else
        taskTaskRequest = new ActiveXObject("Microsoft.XMLHTTP");
    taskTaskRequest.open("POST", "/test/SP/taken_task");
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