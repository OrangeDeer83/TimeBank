window.onload = function()
{
    getNoticeAmount();
}

var noticeAmount = 0;
var pageAmount = 0;
var currentPage = 1;
var currentPageAmount = 0;
const pageNumber = document.getElementById('pageNumber');
const maxPageAmount = 20;

function getNoticeAmount()
{
    var noticeAmountRequest = new XMLHttpRequest();
    noticeAmountRequest.open('GET', 'http://192.168.1.144:5000/notice/all_list_amount');
    noticeAmountRequest.setRequestHeader('Content-Type', 'application/json');
    noticeAmountRequest.send();
    noticeAmountRequest.onload = function()
    {
        console.log(noticeAmountRequest.responseText);
        rst = JSON.parse(noticeAmountRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                noticeAmount = rst.allNoticeAmount;
                pageAmount = Math.ceil(noticeAmount / maxPageAmount);
                showDiv();
                break;
            default:
                console.log('無法取得通知數量');
                break;
        }
    }
}

function showDiv()
{
    const pointTable = document.getElementById('notificationTable');
    pointTable.innerHTML = '<caption id="tableTitle">通知歷史紀錄</caption>';
    for (var i = 0; i < maxPageAmount && i < noticeAmount; i++)
    {
        pointTable.innerHTML += '<tr id="noticeDiv' + i + '" style="display:none;"><td>' +
        '<span id="noticeTime' + i + '"></span>' +
        '<a class="introduction" id="noticehref' + i + '"><br /><span id="noticeContent' + i + '"></span></a></td></tr>';
    }
    computePage(0);
}

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

    if (noticeAmount == 0)
        currentPageAmount = 0;
    else if (currentPage < pageAmount || (noticeAmount % maxPageAmount) == 0)
        currentPageAmount = maxPageAmount;
    else
        currentPageAmount = noticeAmount % maxPageAmount;
    getDetail();
}

function getDetail()
{
    if (currentPageAmount == 0)
    {
        document.getElementById('notificationTable').innerHTML = '<tr><td>目前沒有通知歷史紀錄</td></tr>';
        return ;
    }
    var getNoticeRequest = new XMLHttpRequest();
    getNoticeRequest.open('POST', 'http://192.168.1.144:5000/notice/all_list');
    getNoticeRequest.setRequestHeader('Content-Type', 'application/json');
    console.log(JSON.stringify({"startNum": (maxPageAmount * currentPage - maxPageAmount), "amount": currentPageAmount}));
    getNoticeRequest.send(JSON.stringify({"startNum": (maxPageAmount * currentPage - maxPageAmount), "amount": currentPageAmount}));
    getNoticeRequest.onload = function()
    {
        console.log(getNoticeRequest.responseText);
        rst = JSON.parse(getNoticeRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                if (rst.noticeList.length != currentPageAmount)
                {
                    document.getElementById('notificationTable').innerHTML += '伺服器錯誤，數量不相符' + rst.noticeList.length + '/' + currentPageAmount;
                    return ;
                }
                showDetail(rst.noticeList);
                break;
            default:
                console.log('無法讀取通知內容');
                break;
        }
    }
}

function showDetail(noticeList)
{
    for (var i = 0; i < currentPageAmount; i++)
    {
        document.getElementById('noticeContent' + i).innerHTML = noticeList[i].content;
        document.getElementById('noticeTime' + i).innerHTML = noticeList[i].time;
        document.getElementById('noticehref' + i).href = numToUrl(noticeList[i].connectTo);
        document.getElementById('noticeDiv' + i).removeAttribute('style');
    }
    for (var i = currentPageAmount; i < maxPageAmount && i < noticeAmount; i++)
    {
        document.getElementById('noticeContent' + i).innerHTML = '';
        document.getElementById('noticeTime' + i).innerHTML = '';
        document.getElementById('noticehref' + i).removeAttribute('href');
        document.getElementById('noticeDiv' + i).style.display = 'none';
    }
}

function numToUrl(type)
{
    switch(type)
    {
        case 1: return '/USER/allTask';
        case 2: return '/USER/SR/allTaskPassed';
        case 3: return '/USER/SR/allTaskAccepted';
        case 4: return '/USER/SR/allTaskRecord';
        case 5: return '/USER/SP/allTaskPassed';
        case 6: return '/USER/SP/allTaskChecking';
        case 7: return '/USER/SP/allTaskRefused';
        case 8: return '/USER/SP/allTaskRecord';
        case 9: return '/USER/pointRecord';
    }
}