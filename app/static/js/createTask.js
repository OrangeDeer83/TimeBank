const taskName = document.getElementById("taskName");
const taskStartTime = document.getElementById("taskStartTime");
const taskEndTime = document.getElementById("taskEndTime");
const taskQuota = document.getElementById("taskQuota");
const taskLocation = document.getElementById("taskLocation");
const taskContent = document.getElementById("taskContent");
var firstCheckContent = 0;

function showPrompt(index)
{
    console.log(index)
    var prompt = document.getElementById('systemPrompt');
    //prompt.removeAttribute('style');
    switch (index)
    {
        case 20: prompt.innerHTML = '已就緒...'; return ;
        case 21: prompt.innerHTML = '任務建立成功'; return ;
        case 30: prompt.innerHTML = '系統錯誤，任務建立失敗，請稍後再試'; return false;
        case 40: prompt.innerHTML = '等待伺服器回應...'; return ;
        case 41: prompt.innerHTML = '請輸入任務名稱，不得超過20字'; return false;
        case 42: prompt.innerHTML = '請輸入任務起始時間'; return false;
        case 43: prompt.innerHTML = '請輸入任務結束時間'; return false;
        case 44: prompt.innerHTML = '時間格式錯誤'; return false;
        case 45: prompt.innerHTML = '結束時間請勿在起始時間之前'; return false;
        case 46: prompt.innerHTML = '請輸入任務額度，介於0~99'; return false;
        case 47: prompt.innerHTML = '請輸入任務地點'; return false;
        case 48: prompt.innerHTML = '若確認任務說明留空，請再次點擊新增任務'; return false;
        case 49: prompt.innerHTML = '點數不足，請認真工作，或前往申請補助'; return false;
        case 50: prompt.innerHTML = '請勿輸入已經過的時間'; return false;
    }
}

function validated()
{
    if (taskName.value.length == 0 || taskName.value.length > 20)
        return (showPrompt(41));
    if (taskStartTime.value.length == 0)
        return (showPrompt(42));
    if (taskEndTime.value.length == 0)
        return (showPrompt(43));
    if (taskStartTime.value.length != 19 || taskEndTime.value.length != 19)
        return (showPrompt(44));
    if (taskStartTime.value >= taskEndTime.value)
        return (showPrompt(45));
    if (taskQuota.value.length == 0 || taskQuota.value < 0 || taskQuota.value > 99)
        return (showPrompt(46));
    if (taskLocation.value.length == 0)
        return (showPrompt(47));
    if (taskContent.value.length == 0 && firstCheckContent == 0)
    {
        firstCheckContent++;
        return (showPrompt(48));
    }
    return true;
}

function createTask()
{
    if (!validated()) return ;
    else
    {
        var createTaskRequest = new XMLHttpRequest();
        createTaskRequest.open("POST", "/task/SR/add_task");
        createTaskRequest.setRequestHeader("Content-Type", "application/json");
        createTaskRequest.send(JSON.stringify({"taskName": taskName.value, "taskStartTime": taskStartTime.value, "taskEndTime": taskEndTime.value, "taskPoint": taskQuota.value, "taskLocation": taskLocation.value, "taskContent": taskContent.value}));
        createTaskRequest.onload = function()
        {
            console.log(createTaskRequest.responseText);
            rst = JSON.parse(createTaskRequest.responseText);
            switch (rst.rspCode)
            {
                case "200": case 200:
                    showPrompt(21);
                    window.location.assign('/USER/SR/allTaskPassed');
                    break;
                case "401": case 401:
                    showPrompt(44);
                    break;
                case "402": case 402:
                    showPrompt(50);
                    break;
                case "403": case 403:
                    showPrompt(45);
                    break;
                case "300": case 300:
                case "400": case 400:
                default:
                    if (rst.pointConflit < 0)
                        showPrompt(49);
                    else if (rst.taskConflit.length != 0)
                        document.getElementById('systemPrompt').innerHTML = '與其他任務時間重疊，請再次確認：' + rst.taskConflit[0].taskName;
                    else
                        alert(30);
                    break;
            }
        }
    }
}