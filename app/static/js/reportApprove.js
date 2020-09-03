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
    reportAmountRequest.open('GET', '/report/list_amount');
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
                computePage(0);
                break;
            default:
                alert('系統錯誤，無法取得檢舉清單');
            }
    }
}

function computePage(type)
{
    if (currentReport >= reportAmount)
        currentReport = reportAmount - 1;
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
        pageNumber.innerHTML = '暫無檢舉';
    else
        pageNumber.innerHTML = (currentReport + 1) + '/' + reportAmount;
    getDetail();
}

function getDetail()
{
    if (reportAmount == 0) return ;
    var reportDetailRequest = new XMLHttpRequest();
    reportDetailRequest.open('POST', '/report/list');
    reportDetailRequest.setRequestHeader('Content-Type', 'application/json');
    reportDetailRequest.send(JSON.stringify({'reportID': reportList[currentReport]}));
    reportDetailRequest.onload = function()
    {
        console.log(reportDetailRequest.responseText);
        rst = JSON.parse(reportDetailRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                showDetail(rst.reportList[0]);
                break;
            default:
                alert('無法取得檢舉清單');
            }
    }
}

function showDetail(reportDetail)
{
    document.getElementById('reportID').innerHTML = reportList[currentReport];
    document.getElementById('reportTime').innerHTML = reportDetail.reportTime;
    document.getElementById('reportUserName').innerHTML = reportDetail.reportUserName;
    document.getElementById('reportReason').innerHTML = reportDetail.reportReason;
    document.getElementById('taskName').innerHTML = reportDetail.taskName;
    document.getElementById('taskTime').innerHTML = reportDetail.taskStartTime + ' ~ ' + reportDetail.taskEndTime;
    document.getElementById('taskContent').value = reportDetail.taskContent;
    document.getElementById('SRName').innerHTML = reportDetail.SRName;
    document.getElementById('SRPhone').innerHTML = reportDetail.SRPhone;
    document.getElementById('SRRate').innerHTML = reportDetail.SRRate;
    document.getElementById('SRComment').value = reportDetail.SRComment;
    document.getElementById('SPName').innerHTML = reportDetail.SPName;
    document.getElementById('SPPhone').innerHTML = reportDetail.SPPhone;
    document.getElementById('SPRate').innerHTML = reportDetail.SPRate;
    document.getElementById('SPComment').value = reportDetail.SPComment;
}

function report(type)
{
    var approveRequest = new XMLHttpRequest();
    approveRequest.open('POST', '/report/approve');
    approveRequest.setRequestHeader('Content-Type', 'application/json');
    approveRequest.send(JSON.stringify({'reportID': reportList[currentReport], 'reportStatus': type}));
    approveRequest.onload = function()
    {
        console.log(approveRequest.responseText);
        rst = JSON.parse(approveRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                getReportAmount();
                break;
            case '42': case 42:
                alert('此檢舉已被審理');
                getReportAmount();
                break;
            default:
                alert('系統錯誤，無法審核檢舉');
            }
    }
}