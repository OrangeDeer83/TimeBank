window.onload = function()
{
    document.getElementById('editTaskDiv').style.display = 'none';
    showListDiv();
}

var taskList = [];
var taskAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById('pageNumber');
const maxPageAmount = 10;

function showListDiv()
{
    const table = document.getElementById('bPass');
    for (var i = 0; i < maxPageAmount; i++)
    {
        table.innerHTML += '' +
        '<tr id="taskList' + i + '" style="display:none;"><td>' +
            '<div class="introduction">' +
                '<div>' +
                    '<div class="button" onclick="deleteTask(' + i + ')">刪除</div>' +
                    '<div class="button" id="edit' + i + '" onclick="showEditDiv(' + i + ')">編輯</div>' +
                '</div>' +
                '<div>任務名稱：<span id="taskName' + i + '"></span></div>' +
                '<div>任務時間：<span id="taskStartTime' + i + '"></span> ~ <span id="taskEndTime' + i + '"></span></div>' +
                '<div>任務額度：<span id="taskQuota' + i + '"></span>點</div>' +
            '</div>' +
            '<div class="detailed">' +
                '<div>任務地點：<span id="taskLocation' + i + '"></span></div>' +
                '<div>任務內容：<span id="taskContent' + i + '"></span></div>' +
                '<div>' +
                    '<div class="title" id="applicationText">' +
                        '申請之雇員：' +
                    '</div>' +
                    '<div class="title" id="choose">' +
                        '<select id="applySP' + i + '">' +
                            '<option disabled selected hidden>尚無申請</option>' +
                        '</select>' +
                    '</div>' +
                    '<div class="title chooseButton">' +
                        '<input type="button" name="submitBottom" value="選擇" onclick="selectSP(' + i + ')" />' +
                    '</div>' +
                '</div>' +
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
        case 201: prompt.innerHTML = '尚無已發布任務，請至新增任務頁面建立新任務'; return ;
        case 300: prompt.innerHTML = '系統錯誤'; return ;
        case 400: prompt.innerHTML = '等待伺服器回應...'; return ;
        case 401: prompt.innerHTML = '無法取得任務列表'; return ;
        case 402: prompt.innerHTML = '僱員選擇失敗'; return ;
    }
}

function getTaskList()
{
    var taskListRequest = new XMLHttpRequest();
    taskListRequest.open('GET', 'http://192.168.1.144:5000/task/SR/output/passed');
    taskListRequest.setRequestHeader('Content-Type', 'application/json');
    taskListRequest.send();
    taskListRequest.onload = function()
    {
        showPrompt(200);
        console.log(taskListRequest.responseText);
        rst = JSON.parse(taskListRequest.responseText);
        switch (rst.rspCode)
        {
            case '200': case 200:
                showPrompt(20029);
                taskList = rst.taskList;
                taskAmount = taskList.length;
                pageAmount = Math.ceil(taskAmount / maxPageAmount);
                computePage(0);
                break;
            case '300': case 300: // Methods wrong.
            case '400': case 400: // Database error.
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
        pageNumber.innerHTML = '1/1';
        document.getElementById('bPass').innerHTML = '<tr><td>尚無已發布任務，請至新增任務頁面建立新任務</td></tr>';
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
        document.getElementById('taskList' + i).removeAttribute('style');
    }
    for (var i = thisPageList.length; i < maxPageAmount; i++)
        document.getElementById('taskList' + i).style.display = 'none';
}

function putDetail(index)
{
    var currentTask = thisPageList[index];
    document.getElementById('applySP' + index).length = 1;
    if (currentTask.taskStatus == 0 || currentTask.taskStatus == '0')
    {
        document.getElementById('edit' + index).removeAttribute('style');
        document.getElementById('applySP' + index)[0] = new Option('尚無申請', '');
        document.getElementById('taskName' + index).innerHTML = currentTask.taskName;
        document.getElementById('taskStartTime' + index).innerHTML = currentTask.taskStartTime;
        document.getElementById('taskEndTime' + index).innerHTML = currentTask.taskEndTime;
        document.getElementById('taskQuota' + index).innerHTML = currentTask.taskPoint;
        document.getElementById('taskLocation' + index).innerHTML = currentTask.taskLocation;
        document.getElementById('taskContent' + index).innerHTML = currentTask.taskContent;
    }
    else if (currentTask.taskStatus == 1 || currentTask.taskStatus == '1')
    {
        document.getElementById('edit' + index).style.display = 'none';
        document.getElementById('applySP' + index)[0] = new Option('請選擇僱員', '');
        document.getElementById('taskName' + index).innerHTML = currentTask.taskName;
        document.getElementById('taskStartTime' + index).innerHTML = currentTask.taskStartTime;
        document.getElementById('taskEndTime' + index).innerHTML = currentTask.taskEndTime;
        document.getElementById('taskQuota' + index).innerHTML = currentTask.taskPoint;
        document.getElementById('taskLocation' + index).innerHTML = currentTask.taskLocation;
        document.getElementById('taskContent' + index).innerHTML = currentTask.taskContent;
        for (var i = 0; i < currentTask.CandidateList.length; i++)
            document.getElementById('applySP' + index).add(new Option(currentTask.CandidateList[i][0], currentTask.CandidateList[i][1]));
    }
    else document.getElementById('applySP' + index)[0] = new Option('尚無申請', '');
}

function selectSP(index)
{
    const candidateList = document.getElementById('applySP' + index);
    const selectedIndex = candidateList.selectedIndex;
    const candidate = candidateList[selectedIndex];
    if (candidateList.length == 1)
    {
        alert('此任務尚無人申請：' + thisPageList[index].taskName);
        return ;
    }
    if (selectedIndex == 0)
    {
        alert('請選擇僱員');
        return ;
    }

    var selectSPRequest = new XMLHttpRequest();
    selectSPRequest.open('POST', 'http://192.168.1.144:5000/task/SR/decide_SP');
    selectSPRequest.setRequestHeader('Content-Type', 'application/json');
    selectSPRequest.send(JSON.stringify({'taskID': thisPageList[index].taskID, 'candidateID': candidate.value}));
    selectSPRequest.onload = function()
    {
        showPrompt(200);
        console.log(selectSPRequest.responseText);
        rst = JSON.parse(selectSPRequest.responseText);
        switch (rst.rspCode)
        {
            case '200': case 200:
                alert(thisPageList[index].taskName + '已成功選擇僱員：' + candidate.text);
                window.location.reload();
                break;
            case '300': case 300:
            case '400': case 400:
            default:
                showPrompt(402);
            }
    }
    showPrompt(400);
}

var editTaskIndex = -1;
function showEditDiv(index)
{
    editTaskIndex = index;
    document.getElementById('editTaskDiv').removeAttribute('style');
    document.getElementById('edit' + index).style.display = 'none';
    for (var i = 0; i < 10; i++)
        if (i != index)
            document.getElementById('taskList' + i).style.display = 'none';
    document.getElementById('newTaskName').value = document.getElementById('taskName' + index).innerHTML
    document.getElementById('newTaskStartTime').value = thisPageList[index].taskStartTime;
    document.getElementById('newTaskEndTime').value = thisPageList[index].taskEndTime;
    document.getElementById('newTaskQuota').value = document.getElementById('taskQuota' + index).innerHTML
    document.getElementById('newTaskLocation').value = document.getElementById('taskLocation' + index).innerHTML
    document.getElementById('newTaskContent').value = document.getElementById('taskContent' + index).innerHTML
}
function hideEditDiv()
{
    document.getElementById('editTaskDiv').style.display = 'none';
    document.getElementById('edit' + editTaskIndex).removeAttribute('style');
    for (var i = 0; i < thisPageList.length; i++)
        document.getElementById('taskList' + i).removeAttribute('style');
    document.getElementById('newTaskName').value = '';
    document.getElementById('newTaskStartTime').value = '';
    document.getElementById('newTaskEndTime').value = '';
    document.getElementById('newTaskQuota').value = '';
    document.getElementById('newTaskLocation').value = '';
    document.getElementById('newTaskContent').value = '';
    editTaskIndex = -1;
}
function updateEdit(index)
{
    document.getElementById('taskName' + index).innerHTML = document.getElementById('newTaskName').value;
    document.getElementById('taskStartTime' + index).innerHTML = document.getElementById('newTaskStartTime').value;
    document.getElementById('taskEndTime' + index).innerHTML = document.getElementById('newTaskEndTime').value;
    document.getElementById('taskQuota' + index).innerHTML = document.getElementById('newTaskQuota').value;
    document.getElementById('taskLocation' + index).innerHTML = document.getElementById('newTaskLocation').value;
    document.getElementById('taskContent' + index).innerHTML = document.getElementById('newTaskContent').value;
}
function sendEdit()
{
    var editTaskRequest = new XMLHttpRequest();
    editTaskRequest.open('POST', 'http://192.168.1.144:5000/task/SR/edit_task');
    editTaskRequest.setRequestHeader('Content-Type', 'application/json');
    editTaskRequest.send(JSON.stringify({'taskID': thisPageList[editTaskIndex].taskID, 'taskName': document.getElementById('newTaskName').value,
    'taskStartTime': document.getElementById('newTaskStartTime').value, 'taskEndTime': document.getElementById('newTaskEndTime').value,
    'taskPoint': document.getElementById('newTaskQuota').value, 'taskLocation': document.getElementById('newTaskLocation').value,
    'taskContent': document.getElementById('newTaskContent').value,}));
    editTaskRequest.onload = function()
    {
        console.log(editTaskRequest.responseText);
        rst = JSON.parse(editTaskRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                console.log('任務編輯已送出');
                hideEditDiv();
                window.location.reload();
                editTaskIndex = -1;
                break;
            default:
                alert('系統錯誤，無法編輯任務');
            }
    }
}

function deleteTask(index)
{
    var deleteTaskRequest = new XMLHttpRequest();
    deleteTaskRequest.open('POST', 'http://192.168.1.144:5000/task/SR/delete_task');
    deleteTaskRequest.setRequestHeader('Content-Type', 'application/json');
    deleteTaskRequest.send(JSON.stringify({'taskID': thisPageList[index].taskID}));
    deleteTaskRequest.onload = function()
    {
        showPrompt(200);
        console.log(deleteTaskRequest.responseText);
        rst = JSON.parse(deleteTaskRequest.responseText);
        switch (rst.rspCode)
        {
            case '200': case 200:
                console.log('已刪除任務：' + thisPageList[index].taskName);
                window.location.reload();
                break;
            case '300': case 300:
            case '400': case 400:
            default:
                document.getElementById('systemPrompt').innerHTML = '任務刪除失敗：' + thisPageList[index].taskName;
            }
    }
    showPrompt(400);
}