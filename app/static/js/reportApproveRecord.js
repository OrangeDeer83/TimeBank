window.onload = function()
{
    getReportAmount();
}

var reportList = [];
var reportAmount = 0;
var currentReport = 0;
const pageNumber = document.getElementById('pageNumber');

function getReportAmount()
{
    var reportAmountRequest = new XMLHttpRequest();
    reportAmountRequest.open('GET', 'http://192.168.1.144:5000/report/report_history_list_amount');
    reportAmountRequest.setRequestHeader('Content-Type', 'application/json');
    reportAmountRequest.send();
    reportAmountRequest.onload = function()
    {
        console.log(reportAmountRequest.responseText);
        rst = JSON.parse(reportAmountRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                reportList = rst.reportList;
                reportAmount = reportList.length;
                computePage();
                break;
            default:
                console.log('無法取得檢舉紀錄數量')
            }
    }
}

function computePage(type)
{
    switch (type)
    {
        case 1:
            if (currentReport + 1 == 1) return false;
            else currentReport--;
            break;
        case 2:
            if (currentReport + 1 == reportAmount) return false;
            else currentReport++;
            break;
    }
    if (reportAmount == 0)
        pageNumber.innerHTML = '暫無檢舉紀錄';
    else
        pageNumber.innerHTML = (currentReport + 1) + '/' + reportAmount;
    getDetail();
}

function getDetail()
{
    var detailRequest = new XMLHttpRequest();
    detailRequest.open('POST', 'http://192.168.1.144:5000/report/report_history_list');
    detailRequest.setRequestHeader('Content-Type', 'application/json');
    detailRequest.send(JSON.stringify({'reportID': reportList[currentReport]}));
    detailRequest.onload = function()
    {
        console.log(detailRequest.responseText);
        rst = JSON.parse(detailRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                showDetail(rst.reportList[0]);
                break;
            default:
                console.log('無法取得檢舉細節')
            }
    }
}

function showDetail(recordDetail)
{
    document.getElementById('reportID').innerHTML = reportList[currentReport];
    if (recordDetail.approveResult == 1)
        document.getElementById('approveResult').innerHTML = '已處理';
    else if (recordDetail.approveResult == 2)
        document.getElementById('approveResult').innerHTML = '已略過';
    document.getElementById('gmID').innerHTML = recordDetail.gmID;
    document.getElementById('reportTime').innerHTML = recordDetail.reportTime;
    document.getElementById('reportUserName').innerHTML = recordDetail.reportUserName;
    document.getElementById('reportReason').innerHTML = recordDetail.reportReason;
    document.getElementById('taskName').innerHTML = recordDetail.taskName;
    document.getElementById('taskTime').innerHTML = recordDetail.taskStartTime + ' ~ ' + recordDetail.taskEndTime;
    document.getElementById('taskContent').value = recordDetail.taskContent;
    document.getElementById('SRName').innerHTML = recordDetail.SRName;
    document.getElementById('SRPhone').innerHTML = recordDetail.SRPhone;
    document.getElementById('SRRate').innerHTML = recordDetail.SRRate;
    document.getElementById('SRComment').value = recordDetail.SRComment;
    document.getElementById('SPName').innerHTML = recordDetail.SPName;
    document.getElementById('SPPhone').innerHTML = recordDetail.SPPhone;
    document.getElementById('SPRate').innerHTML = recordDetail.SPRate;
    document.getElementById('SPComment').value = recordDetail.SPComment;
}