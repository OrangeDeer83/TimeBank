window.onload = function()
{
    document.getElementById('reportDiv').style.display = 'none';
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
    const table = document.getElementById('bRecord');
    for (var i = 0; i < 10; i++)
    {
        table.innerHTML += '' +
        '<tr id="taskList' + i + '" style="display:none"><td>' +
            '<div class="upPart">' +
                '<div>雇員：<a id="taskSP' + i + '"></a></div>' +
                '<div>任務名稱：<span id="taskName' + i + '"></span></div>' +
                '<div>任務時間：<span id="taskTime' + i + '"></span></div>' +
                '<div>任務額度：<span id="taskQuota' + i + '"></span>點</div> ' +
                '<div>任務地點：<span id="taskLocation' + i + '"></span></div>' +
                '<div>任務內容：<span id="taskContent' + i + '"></span></div><br>' +
            '</div>' +
            '<div class="downPart">' +
                '<div id="scorePart' + i + '">' +
                    '<div class="bossScorePart">' +
                        '<div class="formLine">' +
                            '<div class="formLabelDiv">' +
                                '<label for="rate" class="formLabel">雇主評分：</label>' +
                            '</div>' +
                            '<div class="rating">' +
                                '<input type="radio" id="SRRate0' + i + '" name="rating" value="5" hidden/>' +
                                '<label id="RLabel0' + i + '" for="star5"></label>' +
                                '<input type="radio" id="SRRate1' + i + '" name="rating" value="4" hidden/>' +
                                '<label id="RLabel1' + i + '" for="star4"></label>' +
                                '<input type="radio" id="SRRate2' + i + '" name="rating" value="3" hidden/>' +
                                '<label id="RLabel2' + i + '" for="star3"></label>' +
                                '<input type="radio" id="SRRate3' + i + '" name="rating" value="2" hidden/>' +
                                '<label id="RLabel3' + i + '" for="star2"></label>' +
                                '<input type="radio" id="SRRate4' + i + '" name="rating" value="1" hidden/>' +
                                '<label id="RLabel4' + i + '" for="star1"></label>' +
                            '</div>' +
                        '</div>' +
                        '<div>雇主評論：<span id="SRComment' + i + '"></span></div>' +
                    '</div>' +
                    '<div class="employeeScorePart">' +
                        '<div class="formLine">' +
                            '<div class="formLabelDiv">' +
                                '<label for="rate" class="formLabel">雇員評分：</label>' +
                            '</div>' +
                            '<div class="rating">' +
                                '<input type="radio" id="SPRate0' + i + '" name="rating" value="5" hidden/>' +
                                '<label id="PLabel0' + i + '" for="star5"></label>' +
                                '<input type="radio" id="SPRate1' + i + '" name="rating" value="4" hidden/>' +
                                '<label id="PLabel1' + i + '" for="star4"></label>' +
                                '<input type="radio" id="SPRate2' + i + '" name="rating" value="3" hidden/>' +
                                '<label id="PLabel2' + i + '" for="star3"></label>' +
                                '<input type="radio" id="SPRate3' + i + '" name="rating" value="2" hidden/>' +
                                '<label id="PLabel3' + i + '" for="star2"></label>' +
                                '<input type="radio" id="SPRate4' + i + '" name="rating" value="1" hidden/>' +
                                '<label id="PLabel4' + i + '" for="star1"></label>' +
                            '</div>' +
                        '</div>' +
                        '<div>雇員評論：<span id="SPComment' + i + '"></span></div>' +
                    '</div>' +
                '</div>' +
            '</div>' +
            '<div class="button" id="reportButton' + i + '" onclick="showReportDiv(' + i + ')">檢舉</div>' +
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
        case 201: prompt.innerHTML = '尚無雇主歷史紀錄'; return ;
        case 300: prompt.innerHTML = '系統錯誤'; return ;
        case 400: prompt.innerHTML = '等待伺服器回應...'; return ;
        case 401: prompt.innerHTML = '無法取得任務列表'; return ;
        case 402: prompt.innerHTML = '系統錯誤，無法送出檢舉'; return ;
    }
}

function getTaskList()
{
    var taskListRequest = new XMLHttpRequest();
    taskListRequest.open("GET", "/task/SR/output/record");
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
                taskList = rst.taskRecord;
                taskAmount = taskList.length;
                pageAmount = Math.ceil(taskAmount / maxPageAmount);
                computePage(0);
                break;
            case "300": case 300: // Methods wrong.
            case "400": case 400: // Database error.
            case '401': case 401: // userID is not exist.
            case '402': case 402: // no userID.
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
    const currentTask = thisPageList[index];
    document.getElementById("taskName" + index).innerHTML = currentTask.taskName;
    document.getElementById("taskTime" + index).innerHTML = currentTask.taskStartTime + " ~ " + thisPageList[index].taskEndTime;
    document.getElementById("taskQuota" + index).innerHTML = currentTask.taskPoint;
    var taskStatus = currentTask.taskStatus
    if (currentTask.taskSP === '' || taskStatus == 4)
    {
        document.getElementById("taskSP" + index).innerHTML = '此任務未成功被承接';
        document.getElementById('reportButton' + index).style.display = 'none';
    }
    else if (taskStatus == 0 || taskStatus == 1 || taskStatus == 9 || taskStatus == 10 || taskStatus == 11)
    {
        document.getElementById('reportButton' + index).style.display = 'none';
    }
    else
    {
        document.getElementById("taskSP" + index).innerHTML = currentTask.taskSP;
        document.getElementById("taskSP" + index).href = '/USER/info/' + thisPageList[index].SPID;
        document.getElementById('reportButton' + index).removeAttribute('style');
    }
    document.getElementById("taskLocation" + index).innerHTML = currentTask.taskLocation;
    document.getElementById("taskContent" + index).innerHTML = currentTask.taskContent;
    document.getElementById("SRComment" + index).innerHTML = currentTask.SRComment;
    document.getElementById("SPComment" + index).innerHTML = currentTask.SPComment;
    if (currentTask.SRScore != "")
    {
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
    }
    else
    {
        for (var i = 0; i < 5; i++)
        {
            document.getElementById("SRRate" + i + index).style.display = "none";
            document.getElementById("RLabel" + i + index).style.display = "none";
        }
    }
    if (currentTask.SPScore != "")
    {
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
    else
    {
        for (var i = 0; i < 5; i++)
        {
            document.getElementById("SPRate" + i + index).style.display = "none";
            document.getElementById("PLabel" + i + index).style.display = "none";
        }
    }
}

var reportTaskIndex = -1;
function showReportDiv(index)
{
    reportTaskIndex = index;
    document.getElementById('reportDiv').removeAttribute('style');
    document.getElementById('reportButton' + index).style.display = 'none';
    for (var i = 0; i < 10; i++)
        if (i != index)
            document.getElementById('taskList' + i).style.display = 'none';
}

function hideReportDiv()
{
    document.getElementById('reportDiv').style.display = 'none';
    document.getElementById('reportButton' + reportTaskIndex).removeAttribute('style');
    for (var i = 0; i < thisPageList.length; i++)
        document.getElementById('taskList' + i).removeAttribute('style');
    document.getElementById('reportReason').value = '';
    reportTaskIndex = -1;
}

var sendReportOnload = 0;
function sendReport()
{
    if (sendReportOnload == 1) return ;
    sendReportOnload = 1;
    var reportRequest = new XMLHttpRequest();
    reportRequest.open("POST", "/report/send_report");
    reportRequest.setRequestHeader("Content-Type", "application/json");
    reportRequest.send(JSON.stringify({'taskID': thisPageList[reportTaskIndex].taskID, 'reportReason': document.getElementById('reportReason').value}));
    reportRequest.onload = function()
    {
        console.log(reportRequest.responseText);
        rst = JSON.parse(reportRequest.responseText);
        switch (rst.rspCode)
        {
            case "20": case 20:
                document.getElementById('systemPrompt').innerHTML = '檢舉已送出：' + thisPageList[reportTaskIndex].taskName;
                sendReportOnload = 0;
                hideReportDiv();
                break;
            case "42": case 42:
                alert('此任務無法檢舉');
                break;
            default:
                showPrompt(402);
            }
    }
}