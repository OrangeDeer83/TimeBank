window.onload = function()
{
    getGradeList();
}

var gradeList = [];
var gradeAmount = 0;
var currentGrade = 0;
const pageNumber = document.getElementById("pageNumber");

function getGradeList()
{
    var taskListRequest = new XMLHttpRequest();
    taskListRequest.open("GET", "/comment/GM/output/judge_comment_page");
    taskListRequest.setRequestHeader("Content-Type", "application/json");
    taskListRequest.send();
    taskListRequest.onload = function()
    {
        console.log(taskListRequest.responseText);
        rst = JSON.parse(taskListRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                gradeList = rst.commentList;
                gradeAmount = gradeList.length;
                computePage();
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert('系統錯誤，無法顯示待審核評論');
            }
    }
}

function computePage(type)
{
    if (currentGrade >= gradeAmount)
        currentGrade = gradeAmount - 1;
    switch (type)
    {
        case 1:
            if (currentGrade + 1 == 1) return false;
            else currentGrade--;
            break;
        case 2:
            if (currentGrade + 1 == gradeAmount) return false;
            else currentGrade++;
            break;
    }
    if (gradeAmount == 0)
        pageNumber.innerHTML = "暫無評論";
    else
        pageNumber.innerHTML = (currentGrade + 1) + "/" + gradeAmount;
    showDetail();
}

function showDetail()
{
    document.getElementById("taskID").innerHTML = gradeList[currentGrade].taskID;
    document.getElementById("taskName").innerHTML = gradeList[currentGrade].taskName;
    document.getElementById("taskTime").innerHTML = gradeList[currentGrade].taskStartTime + " ~ " + gradeList[currentGrade].taskEndTime;
    document.getElementById("taskContent").value = gradeList[currentGrade].taskContent;
    document.getElementById("SRName").innerHTML = gradeList[currentGrade].SRName;
    document.getElementById("SRPhone").innerHTML = gradeList[currentGrade].SRPhone;
    document.getElementById("SRRate").innerHTML = gradeList[currentGrade].SRStar;
    document.getElementById("SRComment").value = gradeList[currentGrade].SRComment;
    document.getElementById("SPName").innerHTML = gradeList[currentGrade].SPName;
    document.getElementById("SPRate").innerHTML = gradeList[currentGrade].SPStar;
    document.getElementById("SPComment").value = gradeList[currentGrade].SPComment;
    document.getElementById("SPPhone").innerHTML = gradeList[currentGrade].SPPhone;
}

function grade(type)
{
    var updateGradeRequest = new XMLHttpRequest();
    updateGradeRequest.open("POST", "/comment/judge_commentaction");
    updateGradeRequest.setRequestHeader("Content-Type", "application/json");
    updateGradeRequest.send(JSON.stringify({"taskID": gradeList[currentGrade].taskID, "status": type, "adminID": "5"})); // adminID only for beta
    updateGradeRequest.onload = function()
    {
        console.log(updateGradeRequest.responseText);
        rst = JSON.parse(updateGradeRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                if (type == 1) alert("評論已確認");
                else alert("評論已否決");
                getGradeList();
                break;
            case "403": case 403:
                alert('此評論已審核過');
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert("系統錯誤，評論審核失敗");
            }
    }
}

var count, success;
var gradeAllType;
function gradeAll(type)
{
    count = 0;
    success = 0;
    gradeAllType = type;
    for (var i = 0; i < gradeAmount; i++)
    {
        sendGradeAll(i, type);
    }
}

function sendGradeAll(index, type)
{
    var updateGradeRequest = new XMLHttpRequest();
    updateGradeRequest.open("POST", "/comment/judge_commentaction");
    updateGradeRequest.setRequestHeader("Content-Type", "application/json");
    updateGradeRequest.send(JSON.stringify({"taskID": gradeList[index].taskID, "status": type, "adminID": "1"})); // adminID only for beta
    updateGradeRequest.onload = function()
    {
        console.log(updateGradeRequest.responseText);
        rst = JSON.parse(updateGradeRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
            case "403": case 403:
                counting(1);
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                success = gradeList[index].taskID;
                alert(gradeList[index].taskID + " grade send false");
                counting(0);
            }
    }
}
// Until success == gradeAmount, alert message.
function counting(type)
{
    count++;
    if (type == 1) success++;
    if (success == gradeAmount)
    {
        if (gradeAllType == 1) alert("已確認所有評論");
        else alert("已否決所有評論");
        window.location.reload();
    }
    else if (count == gradeAmount)
    {
        alert("系統錯誤，無法審核所有任務");
    }
}