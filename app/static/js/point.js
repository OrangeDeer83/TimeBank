window.onload = function()
{
    getRecordAmount();
}

var pointRecordIDList;
var recordAmount = 0;
var pageAmount = 0;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById('pageNumber');
const maxPageAmount = 20;

function getRecordAmount()
{
    var recordAmountRequest = new XMLHttpRequest();
    recordAmountRequest.open('GET', 'http://192.168.1.144:5000/point/record_amount');
    recordAmountRequest.setRequestHeader('Content-Type', 'application/json');
    recordAmountRequest.send();
    recordAmountRequest.onload = function()
    {
        console.log(recordAmountRequest.responseText);
        rst = JSON.parse(recordAmountRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                pointRecordIDList = rst.pointRecordIDList;
                recordAmount = pointRecordIDList.length;
                pageAmount = Math.ceil(recordAmount / maxPageAmount);
                showDiv();
                break;
            default:
                console.log('無法取得點數清單');
                break;
        }
    }
}

// Display empty space of list on the HTML.
function showDiv()
{
    const pointTable = document.getElementById('pointTable');
    pointTable.innerHTML = '';
    for (var i = 0; i < maxPageAmount && i < recordAmount; i++)
    {
        pointTable.innerHTML += '<tr id="pointRecordDiv' + i + '"><td>'
        + '<div class="introduction">'
        + '<div class="name">科目：<span id="subject' + i + '"></span></div>'
        + '<div class="name""><span id="detail' + i + '">細節：</span></div>'
        + '<div class="name">時間：<span id="time' + i + '"></span></div></div>'
        + '<div class="point"><span id="amount' + i + '"></span>'
        + '<img class="pointImg" alt="Point" src="../static/img/point1.png" /></div></div></td></tr>';
    }
    computePage(0);
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
        pageNumber.innerHTML = '1/1';
    else
        pageNumber.innerHTML = currentPage + '/' + pageAmount;
    computeThisPageList();
}

// Compute the index of this page.
function computeThisPageList()
{
    thisPageList.length = 0;
    if (currentPage < pageAmount)
        for (var i = 0; i < maxPageAmount; i++)
            thisPageList.push(pointRecordIDList[maxPageAmount * (currentPage - 1) + i]);
    else if (currentPage == pageAmount && (recordAmount % maxPageAmount)== 0)
        for (var i = 0; i < maxPageAmount; i++)
            thisPageList.push(pointRecordIDList[maxPageAmount * (currentPage - 1) + i]);
    else
        for (var i = 0; i < (recordAmount % maxPageAmount); i++)
            thisPageList.push(pointRecordIDList[maxPageAmount * (currentPage - 1) + i]);
    getDetail();
}

// Get detail of this page from server.
function getDetail()
{
    var getRecordRequest = new XMLHttpRequest();
    getRecordRequest.open('POST', 'http://192.168.1.144:5000/point/record');
    getRecordRequest.setRequestHeader('Content-Type', 'application/json');
    getRecordRequest.send(JSON.stringify({"pointRecordID": thisPageList[0], "requestAmount": thisPageList.length}));
    getRecordRequest.onload = function()
    {
        console.log(getRecordRequest.responseText);
        rst = JSON.parse(getRecordRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                showDetail(rst.pointRecord);
                break;
            default:
                console.log('無法取得點數清單細節');
                break;
        }
    }
}

// Put the detail from getDetail().
function showDetail(pointRecordList)
{
    for (var i = 0; i < thisPageList.length; i++)
    {
        putDetail(pointRecordList[i], i);
        document.getElementById('pointRecordDiv' + i).removeAttribute('style');
    }
    for (var i = thisPageList.length; (i < maxPageAmount) && (i < recordAmount); i++)
        document.getElementById('pointRecordDiv' + i).style.display = 'none';
}

function putDetail(pointRecord, index)
{
    switch (pointRecord.subject)
    {
        case '1': case 1:
            document.getElementById('subject' + index).innerHTML = '管理員主動配發';
            document.getElementById('detail' + index).innerHTML = '發放週期：' + pointRecord.detail;
            break;
        case '2': case 2:
            document.getElementById('subject' + index).innerHTML = '點數申請';
            document.getElementById('detail' + index).innerHTML = '申請細節：' + pointRecord.detail;
            break;
        case '3': case 3:
            document.getElementById('subject' + index).innerHTML = '任務收支';
            document.getElementById('detail' + index).innerHTML = '任務名稱：' + pointRecord.detail;
            break;
    }
    document.getElementById("time" + index).innerHTML = pointRecord.time;
    document.getElementById('amount' + index).innerHTML = pointRecord.amount;
}