window.onload = function()
{
    getUserID();
    getProfile();
    getPropicMyself();
    getRateAmount();
    document.getElementById('hrefMyselfTask').innerHTML = '<a href="myselfTask.html' + /*getToken() + */'">已發任務</a>';
    document.getElementById('hrefMyselfSP').innerHTML = '<a href="myselfSP.html' + /*getToken() + */'">雇員評分</a>';
}

var rateAmount = 0;
var pageAmount = 0;
var currentPage = 1;
var thisPageRateList = [];
const pageNumber = document.getElementById('pageNumber');
const maxPageAmount = 10;

function getToken()
{
    var location = window.location.href;
    var token = '';
    var i = 0;
    while (i != location.length)
    {
        if (location[i] != '/' && location != '?')
            token += location[i];
        else
            token = '';
        i++;
    }
    return token;
}

function getRateAmount()
{
    var getRateAmountRequest = new XMLHttpRequest();
    getRateAmountRequest.open('POST', 'http://192.168.1.144:5000/profile/SR_rate_amount');
    getRateAmountRequest.setRequestHeader('Content-Type', 'application/json');
    getRateAmountRequest.send(JSON.stringify({'userID': getToken()}));
    getRateAmountRequest.onload = function()
    {
        console.log(getRateAmountRequest.responseText);
        rst = JSON.parse(getRateAmountRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                rateAmount = rst.rateAmount;
                pageAmount = Math.ceil(rateAmount / maxPageAmount)
                showDiv();
                break;
            default:
                console.log('無法取得評論數量');
                break;
        }
    }
}

function showDiv()
{
    const srDiv =  document.getElementById('SR');
    srDiv.innerHTML = '';
    for (var i = 0; i < maxPageAmount && i < rateAmount; i++)
    {
        srDiv.innerHTML += '<tr id="rateDiv' + i + '"><td>' +
            '<div>評論者：<span id="commentBy' + i + '"></span></div>' +
            '<div>評分：<span id="rate' + i + '"></span></div>' +
            '<div>評論：<span id="comment' + i + '"></span></div></td></tr>';
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
    {
        document.getElementById('SR').innerHTML = '<tr><td>尚無雇主評分</td></tr>';
        pageNumber.innerHTML = '1/1';
    }
    else
        pageNumber.innerHTML = currentPage + '/' + pageAmount;
    getThisPageList();
}

function getThisPageList()
{
    var rateListRequest = new XMLHttpRequest();
    rateListRequest.open('POST', 'http://192.168.1.144:5000/profile/SR_rate');
    rateListRequest.setRequestHeader('Content-Type', 'application/json');
    if (currentPage < pageAmount && (rateAmount % maxPageAmount) == 0)
        rateListRequest.send(JSON.stringify({'userID': getToken(), 'startNum': currentPage * 10 - 10, 'amount': maxPageAmount}));
    else
        rateListRequest.send(JSON.stringify({'userID': getToken(), 'startNum': currentPage * 10 - 10, 'amount': (rateAmount % maxPageAmount)}));
    rateListRequest.onload = function()
    {
        console.log(rateListRequest.responseText);
        rst = JSON.parse(rateListRequest.responseText);
        switch (rst.rspCode)
        {
            case '20': case 20:
                thisPageList = rst.rateList;
                showDetail();
                break;
            default:
                console.log('無法取得評論數量');
                break;
        }
    }
}

function showDetail()
{
    for (var i = 0; i < thisPageList.length; i++)
    {
        putDetail(thisPageList[i], i);
        document.getElementById('rateDiv' + i).removeAttribute('style');
    }
    for (var i = thisPageList.length; i < maxPageAmount && i < rateAmount; i++)
        document.getElementById('rateDiv' + i).style.display = 'none';
}

function putDetail(rateDetail, index)
{
    document.getElementById('commentBy' + index).innerHTML = rateDetail.commentBy;
    document.getElementById('rate' + index).innerHTML = rateDetail.rate;
    document.getElementById('comment' + index).innerHTML = rateDetail.comment;
}