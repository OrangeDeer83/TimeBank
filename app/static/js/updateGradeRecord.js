window.onload = function()
{
    getGradeList();
}

var gradeList = [];
var gradeAmount = 0;
var currentGrade = 0;
const pageNumber = document.getElementById('pageNumber');

function getGradeList()
{
    var taskListRequest = new XMLHttpRequest();
    taskListRequest.open('GET', 'http://192.168.1.144:5000/comment/rate_history_list_amount');
    taskListRequest.setRequestHeader('Content-Type', 'application/json');
    taskListRequest.send();
    taskListRequest.onload = function()
    {
        console.log(taskListRequest.responseText);
        rst = JSON.parse(taskListRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                gradeList = rst.taskIDList;
                gradeAmount = gradeList.length;
                computePage();
                break;
            default:
                console.log('無法取得評論紀錄數量')
            }
    }
}

function computePage(type)
{
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
        pageNumber.innerHTML = '暫無評論紀錄';
    else
        pageNumber.innerHTML = (currentGrade + 1) + '/' + gradeAmount;
    getDetail();
}

function getDetail()
{
    var detailRequest = new XMLHttpRequest();
    detailRequest.open('POST', 'http://192.168.1.144:5000/comment/rate_history_list');
    detailRequest.setRequestHeader('Content-Type', 'application/json');
    detailRequest.send(JSON.stringify({'taskID': gradeList[currentGrade], 'taskAmount': 1}));
    detailRequest.onload = function()
    {
        console.log(detailRequest.responseText);
        rst = JSON.parse(detailRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                showDetail(rst);
                break;
            default:
                console.log('無法取得評論細節')
            }
    }
}

function showDetail(recordDetail)
{
    document.getElementById('taskID').innerHTML = recordDetail.taskID;
    document.getElementById('taskName').innerHTML = recordDetail.taskName;
    document.getElementById('taskTime').innerHTML = recordDetail.taskStartTime + ' ~ ' + recordDetail.taskEndTime;
    if (recordDetail.approveResult == 1)
        document.getElementById('approveResult').innerHTML = '已確認';
    else if (recordDetail.approveResult == 2)
        document.getElementById('approveResult').innerHTML = '已否決';
    document.getElementById('gmID').innerHTML = recordDetail.gmID;
    document.getElementById('taskContent').value = recordDetail.taskContent;
    document.getElementById('SRName').innerHTML = recordDetail.SRName;
    document.getElementById('SRPhone').innerHTML = recordDetail.SRPhone;
    document.getElementById('SRRate').innerHTML = recordDetail.SRStar;
    document.getElementById('SRComment').value = recordDetail.SRComment;
    document.getElementById('SPName').innerHTML = recordDetail.SPName;
    document.getElementById('SPRate').innerHTML = recordDetail.SPStar;
    document.getElementById('SPComment').value = recordDetail.SPComment;
    document.getElementById('SPPhone').innerHTML = recordDetail.SPPhone;
}