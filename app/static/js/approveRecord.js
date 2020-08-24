window.onload = function()
{
    getUserList();
}

var allList = [16];
// name, userName, userID, userSRRate, userSPRate, userPoint(pointAmount)
// applyID, applyClass(className), oldQuota, applyTime, applyPeriod, applyFrequency, applyResult
// applyStatus(applyResult), quota(resultQuota), judgeTime
var userAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById("pageNumber");
const maxPageAmount = 2;
var searchText;

function getUserList()
{
    searchText = "";//document.getElementById("searchUser").value
    var getListRequest;
    if (window.XMLHttpRequest)
        getListRequest = new XMLHttpRequest();
    else
        getListRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getListRequest.open("POST", "/apply/judgement_history");
    getListRequest.setRequestHeader("Content-Type", "application/json");
    getListRequest.send(JSON.stringify({"name": searchText, "status": "", "class": "", "period":""}));
    getListRequest.onload = function()
    {
        console.log(getListRequest.responseText);
        rst = JSON.parse(getListRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                allList[0] = rst.name;
                allList[1] = rst.userName;
                allList[2] = rst.userID;
                allList[3] = rst.userSRRate;
                allList[4] = rst.userSPRate;
                //allList[5] = rst.userPoint;
                allList[6] = rst.applyID;
                allList[7] = rst.className;
                allList[8] = rst.oldQuota;
                allList[9] = rst.applyTime;
                allList[10] = rst.period;
                allList[11] = rst.applyFrequency;
                allList[12] = rst.applyResult;
                allList[13] = rst.applyStatus;
                allList[14] = rst.quota;
                allList[15] = rst.judgeTime;
                computePage(0);
                break;
            case "300": case 300:
            case "400": case 400:
            default:
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
                allList[4].length != allList[6].length || /*allList[5].length != allList[6].length ||*/
                allList[6].length != allList[7].length || allList[7].length != allList[8].length ||
                allList[8].length != allList[9].length || allList[9].length != allList[10].length ||
                allList[10].length != allList[11].length || allList[11].length != allList[12].length ||
                allList[12].length != allList[13].length || allList[13].length != allList[14].length ||
                allList[14].length != allList[15].length)
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
        pageNumber.innerHTML = "尚無使用者申請";
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
        /*document.getElementById("list" + i).removeAttribute("style");*/
    }
    /*for (var i = thisPageList.length; i < maxPageAmount; i++)
        document.getElementById("list" + i).style.display = "none";*/
}

function putDetail(index)
{
    index;
    document.getElementById("userName" + index).innerHTML = allList[0][thisPageList[index]];
    //document.getElementById("userName" + index).innerHTML = allList[1][thisPageList[index]];
    var SRRate = Math.round(allList[3][thisPageList[index]] * 100) / 100;
    if (SRRate == 0)
        document.getElementById("SRRate" + index).innerHTML = "無";
    else if (SRRate * 10 % 10 != 0)
        document.getElementById("SRRate" + index).innerHTML = SRRate;
    else
        document.getElementById("SRRate" + index).innerHTML = SRRate + ".0";
    var SPRate = Math.round(allList[4][thisPageList[index]] * 100) / 100;
    if (SPRate == 0)
        document.getElementById("SPRate" + index).innerHTML = "無";
    else if (SPRate * 10 % 10 != 0)
        document.getElementById("SPRate" + index).innerHTML = SPRate;
    else
        document.getElementById("SPRate" + index).innerHTML = SPRate + ".0";
    document.getElementById("applyClass" + index).innerHTML = allList[7][thisPageList[index]];
    document.getElementById("applyQuota" + index).innerHTML = allList[8][thisPageList[index]];
    document.getElementById("applyTime" + index).innerHTML = allList[9][thisPageList[index]];
    document.getElementById("applyPeriod" + index).innerHTML = allList[10][thisPageList[index]];
    document.getElementById("applyFrequency" + index).innerHTML = allList[11][thisPageList[index]];
    document.getElementById("applyResult" + index).value = allList[12][thisPageList[index]];
    document.getElementById("applyResult" + index).innerHTML = allList[13][thisPageList[index]];
    document.getElementById("resultQuota" + index).innerHTML = allList[14][thisPageList[index]];
    document.getElementById("judgeTime" + index).innerHTML = allList[15][thisPageList[index]];
}

function downloadPDF(index)
{
    var downloadPDFRequest;
    if (window.XMLHttpRequest)
        downloadPDFRequest = new XMLHttpRequest();
    else
        downloadPDFRequest = new ActiveXObject("Microsoft.XMLHTTP");
    downloadPDFRequest.open("POST", "/apply/apply_pdf_download");
    downloadPDFRequest.setRequestHeader("Content-Type", "application/json");
    downloadPDFRequest.send(JSON.stringify({"applyID": allList[6][thisPageList[index]]}));
    downloadPDFRequest.onload = function()
    {
        console.log(downloadPDFRequest.responseText);
        rst = JSON.parse(downloadPDFRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("成功送出下載要求");
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                console.log("無法下載附件");
                break;
        }
    }
}

function search()
{
    alert("此功能尚未完成");
}