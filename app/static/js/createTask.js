const userID = "10"; // Only for beta.

const taskName = document.getElementById("taskName");
const taskStartTime = document.getElementById("taskStartTime");
const taskEndTime = document.getElementById("taskEndTime");
const taskQuota = document.getElementById("taskQuota");
const taskLocation = document.getElementById("taskLocation");
const taskContent = document.getElementById("taskContent");

function displayError(inputElement, index, type)
{
    console.log(inputElement + " " + index + " " + type);
    if (type) // Show error.
    {
        if (inputElement)
        {
            inputElement.style.border = "1px solid red";
            inputElement.focus();
        }
        switch (index)
        {
            case  0: break;
            case  1:
                error0.innerHTML = "等待伺服器回應...";
                error0.style.display = "block"; break;
            case  2:
                error0.innerHTML = "系統錯誤，請稍後再試";
                error0.style.display = "block"; break;
            case 11:
                error1.innerHTML = "請輸入任務名稱，不得超過20字";
                error1.style.display = "block"; break;
            case 21:
                error2.innerHTML = "請輸入任務起始時間";
                error2.style.display = "block"; break;
            case 22:
                error2.innerHTML = "格式錯誤";
                error2.style.display = "block"; break;
            case 23:
                error2.innerHTML = "請勿輸入已過去的時間點";
                error2.style.display = "block"; break;
            case 31:
                error3.innerHTML = "請輸入任務結束時間";
                error3.style.display = "block"; break;
            case 32:
                error3.innerHTML = "格式錯誤";
                error3.style.display = "block"; break;
            case 33:
                error3.innerHTML = "結束時間請勿在起始時間之前";
                error3.style.display = "block"; break;
            case 41:
                error4.innerHTML = "請輸入任務額度，介於0~99";
                error4.style.display = "block"; break;
            case 51:
                error5.innerHTML = "請輸入任務地點";
                error5.style.display = "block"; break;
        }
    }
    else // Hide Error.
    {
        if (inputElement)
            inputElement.style.border = "1px solid #CCCCCC";
        switch (index)
        {
            case 0: error0.style.display = "none"; break;
        }
    }
}

function validated()
{
    // It will be done when all other pages can run.
    return true;
}

function createTask()
{
    if (!validated)
        return ;

    var createTaskRequest;
    if (window.XMLHttpRequest)
        createTaskRequest = new XMLHttpRequest();
    else
        createTaskRequest = new ActiveXObject("Microsoft.XMLHTTP");
    createTaskRequest.open("POST", "//test/SR/add_task");
    createTaskRequest.setRequestHeader("Content-Type", "application/json");
    // userId is for test.
    createTaskRequest.send(JSON.stringify({"taskName": taskName.value, "taskStartTime": taskStartTime.value, "taskEndTime": taskEndTime.value, "taskPoint": taskQuota.value, "taskLocation": taskLocation.value, "taskContent": taskContent.value, "userID": userID}));
    createTaskRequest.onload = function()
    {
        console.log(createTaskRequest.responseText);
        rst = JSON.parse(createTaskRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("任務建立成功");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
                if (rst.pointConflit < 0)
                    alert("點數不足，請認真工作，或前往申請補助");
                else if (rst.taskConflit.length != 0)
                    alert("與其他任務時間重疊，請再次確認：" + rst.taskConflit[0].taskName);
                else
                    alert("系統錯誤，任務建立失敗，請稍後再試");
        }
    }
}