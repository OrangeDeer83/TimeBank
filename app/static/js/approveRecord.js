window.onload = function()
{
    getUserList();
}

var allList = [18];
// name, userName, userID, userSRRate, userSPRate, userPoint(pointAmount)
// applyID, applyClass(className), oldQuota, applyTime, applyPeriod, applyFrequency, applyResult
// applyStatus(applyResult), quota(resultQuota), judgeTime, judgeAdmin
var userAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById("pageNumber");
const maxPageAmount = 2;
var searchText;

function search()
{
    getUserList();
}

function getUserList()
{
    var searchTextInput = document.getElementById('searchUser');

    var searchClassInput = document.getElementById('searchClass');
    var searchClass = '';
    if (searchClassInput[searchClassInput.selectedIndex].value != '申請類別')
        searchClass = searchClassInput[searchClassInput.selectedIndex].value;

    var searchPeriodInput = document.getElementById('searchPeriod');
    var searchPeriod = '';
    if (searchPeriodInput[searchPeriodInput.selectedIndex].value != '申請週期')
    searchPeriod = searchPeriodInput[searchPeriodInput.selectedIndex].value;

    var searchResultInput = document.getElementById('searchResult');
    var searchStatus = '';
    if (searchResultInput[searchResultInput.selectedIndex].value != '申請結果')
        searchStatus = searchResultInput[searchResultInput.selectedIndex].value;
    
    var getListRequest = new XMLHttpRequest();
    getListRequest.open("POST", "/apply/judgement_history");
    getListRequest.setRequestHeader("Content-Type", "application/json");
    getListRequest.send(JSON.stringify({"name": searchTextInput.value, "class": searchClass, "period": searchPeriod, "status": searchStatus}));
    getListRequest.onload = function()
    {
        console.log(getListRequest.responseText);
        rst = JSON.parse(getListRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                allList[0] = rst.name;
                if (allList[0].length == 0) return ;
                allList[1] = rst.userName;
                allList[2] = rst.userID;
                allList[3] = rst.userSRRate;
                allList[4] = rst.userSPRate;
                allList[5] = rst.userPoint;
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
                allList[16] = rst.judgeAdmin;
                allList[17] = rst.applyPdfName;
                computePage(0);
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                pageNumber.innerHTML = "無法取得列表";
                break;
        }
    }
}

function computePage(type)
{
    switch (type)
    {
        case 0: 
            if (allList[0].length != allList[1].length || allList[1].length != allList[2].length ||
                allList[2].length != allList[3].length || allList[3].length != allList[4].length ||
                allList[4].length != allList[5].length || allList[5].length != allList[6].length ||
                allList[6].length != allList[7].length || allList[7].length != allList[8].length ||
                allList[8].length != allList[9].length || allList[9].length != allList[10].length ||
                allList[10].length != allList[11].length || allList[11].length != allList[12].length ||
                allList[12].length != allList[13].length || allList[13].length != allList[14].length ||
                allList[14].length != allList[15].length || allList[15].length != allList[16].length ||
                allList[16].length != allList[17].length)
            {
                pageNumber.innerHTML = "系統錯誤，列表不全";
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
    else if (i < allList[0].length % maxPageAmount == 0)
        for (var i = 0; i < maxPageAmount; i++)
            thisPageList.push(maxPageAmount * (currentPage - 1) + i);
    else
        for (var i = 0; i < allList[0].length % maxPageAmount; i++)
            thisPageList.push(maxPageAmount * (currentPage - 1) + i);
    showDetail();
}

function showDetail()
{
    for (var i = 0; i < thisPageList.length; i++)
    {
        putDetail(i);
        document.getElementById("formInformation" + (i + 1)).removeAttribute("style");
    }
    for (var i = thisPageList.length; i < maxPageAmount; i++)
        document.getElementById("formInformation" + (i + 1)).style.display = "none";
}

function putDetail(index)
{
    index;
    document.getElementById("name" + index).innerHTML = allList[0][thisPageList[index]];
    document.getElementById("userName" + index).innerHTML = allList[1][thisPageList[index]];
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
    document.getElementById('userPoint' + index).innerHTML = allList[5][thisPageList[index]];
    document.getElementById("applyClass" + index).innerHTML = allList[7][thisPageList[index]];
    document.getElementById("applyQuota" + index).innerHTML = allList[8][thisPageList[index]];
    document.getElementById("applyTime" + index).innerHTML = allList[9][thisPageList[index]];
    switch (allList[10][thisPageList[index]])
    {
        case '0': case 0:
            document.getElementById("applyPeriod" + index).innerHTML = '一次性'; break;
        case '30': case 30:
            document.getElementById("applyPeriod" + index).innerHTML = '一個月一次'; break;
        case '90': case 90:
            document.getElementById("applyPeriod" + index).innerHTML = '三個月一次'; break;
        case '180': case 180:
            document.getElementById("applyPeriod" + index).innerHTML = '半年一次'; break;
        case '365': case 365:
            document.getElementById("applyPeriod" + index).innerHTML = '一年一次'; break;
    }
    document.getElementById("applyFrequency" + index).innerHTML = allList[11][thisPageList[index]];
    document.getElementById("applyReason" + index).value = allList[12][thisPageList[index]];
    document.getElementById("applyResult" + index).innerHTML = allList[13][thisPageList[index]];
    document.getElementById("resultQuota" + index).innerHTML = allList[14][thisPageList[index]];
    document.getElementById("judgeTime" + index).innerHTML = allList[15][thisPageList[index]];
    document.getElementById("judgeAdmin" + index).innerHTML = allList[16][thisPageList[index]];
    if (allList[17][thisPageList[index]] != "None") {
        document.getElementById("downloadBlock" + index).removeAttribute("style");
        document.getElementById("download" + index).href = "/apply/apply_pdf_download/" + allList[6][thisPageList[index]];
    }
    else {
        document.getElementById("downloadBlock" + index).style.display = 'none';
    }
}

function downloadPDF(index)
{
    var downloadPDFRequest = new XMLHttpRequest();
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