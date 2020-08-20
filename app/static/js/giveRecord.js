window.onload = function()
{
    getUserList();
}

var allList = [5]; // name, userName, userID, SRRate, SPRate, quota, time, frequency, period
var userAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById("pageNumber");
const maxPageAmount = 10;
var searchText;

function getUserList(type)
{
    searchText = document.getElementById("searchText").value
    var getListRequest;
    if (window.XMLHttpRequest)
        getListRequest = new XMLHttpRequest();
    else
        getListRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getListRequest.open("POST", "/test/allotment_history");
    getListRequest.setRequestHeader("Content-Type", "application/json");
    getListRequest.send(JSON.stringify({"target": searchText}));
    getListRequest.onload = function()
    {
        console.log(getListRequest.responseText);
        rst = JSON.parse(getListRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                allList[0] = rst.name;
                allList[2] = rst.userID;
                allList[3] = rst.userSRRate;
                allList[4] = rst.userSPRate;
                allList[5] = rst.quota;
                allList[6] = rst.time;
                allList[7] = rst.frequency;
                allList[8] = rst.period;
                computePage(0);
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("無法取得列表");
                break;
        }
    }
}

function computePage(type)
{
    switch (type)
    {
        case 0: 
            if (allList[0].length != allList[2].length || /*allList[1].length != allList[2].length ||*/
                allList[2].length != allList[3].length || allList[3].length != allList[4].length ||
                allList[4].length != allList[5].length || allList[5].length != allList[6].length ||
                allList[6].length != allList[7].length || allList[7].length != allList[8].length)
            {
                console.log("系統錯誤，錯誤的列表");
                return ;
            }
            else
            {
                userAmount = allList[0].length;
                pageAmount = Math.ceil(userAmount / maxPageAmount);
            }
            break;
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
        pageNumber.innerHTML = "尚無使用者";
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
            thisPageList.push(maxPageAmount * (currentPage - 1) + i);
    else
        for (var i = 0; i < (userAmount % maxPageAmount); i++)
            thisPageList.push(maxPageAmount * (currentPage - 1) + i);
    showDetail();
}

function showDetail()
{
    for (var i = 0; i < thisPageList.length; i++)
    {
        putDetail(i);
        document.getElementById("list" + i).removeAttribute("style");
    }
    for (var i = thisPageList.length; i < maxPageAmount; i++)
        document.getElementById("list" + i).style.display = "none";
}

function putDetail(index)
{
    document.getElementById("userName" + index).innerHTML = allList[0][thisPageList[index]];
    var SRRate = allList[3][thisPageList[index]]
    if (SRRate == 0)
        document.getElementById("scoreSR" + index).innerHTML = "無";
    else if (SRRate * 10 % 10 != 0)
        document.getElementById("scoreSR" + index).innerHTML = SRRate;
    else
        document.getElementById("scoreSR" + index).innerHTML = SRRate + ".0";
    var SPRate = allList[4][thisPageList[index]];
    if (SPRate == 0)
        document.getElementById("scoreSP" + index).innerHTML = "無";
    else if (SPRate * 10 % 10 != 0)
        document.getElementById("scoreSP" + index).innerHTML = SPRate;
    else
        document.getElementById("scoreSP" + index).innerHTML = SPRate + ".0";
    document.getElementById("quota" + index).innerHTML = allList[5][thisPageList[index]];
    document.getElementById("time" + index).innerHTML = allList[6][thisPageList[index]];
    document.getElementById("frequency" + index).innerHTML = allList[7][thisPageList[index]];
    document.getElementById("period" + index).innerHTML = allList[8][thisPageList[index]];
}