window.onload = function()
{
    getUserList();
}

var allList = [14];
// name, userName, userID, userSRRate, userSPRate, userPoint(pointAmount)
// applyID, applyClass, applyQuota, applyTime, applyPeriod, applyFrequency, applyResult
var userAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById("pageNumber");
const maxPageAmount = 2;
var searchText;

function getUserList()
{
    searchText = document.getElementById("searchUser").value
    var getListRequest = new XMLHttpRequest();
    getListRequest.open("POST", "/apply/show_apply_list");
    getListRequest.setRequestHeader("Content-Type", "application/json");
    getListRequest.send(JSON.stringify({"name": searchText}));
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
                allList[7] = rst.applyClass;
                allList[8] = rst.applyQuota;
                allList[9] = rst.applyTime;
                allList[10] = rst.applyPeriod;
                allList[11] = rst.applyFrequency;
                allList[12] = rst.applyResult;
                allList[13] = rst.applyPdfName;
                console.log(allList[6])
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
                allList[12].length != allList[13].length)
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
    console.log(thisPageList)
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
        document.getElementById("scoreSR" + index).innerHTML = "無";
    else if (SRRate * 10 % 10 != 0)
        document.getElementById("scoreSR" + index).innerHTML = SRRate;
    else
        document.getElementById("scoreSR" + index).innerHTML = SRRate + ".0";
    var SPRate = Math.round(allList[4][thisPageList[index]] * 100) / 100;
    if (SPRate == 0)
        document.getElementById("scoreSP" + index).innerHTML = "無";
    else if (SPRate * 10 % 10 != 0)
        document.getElementById("scoreSP" + index).innerHTML = SPRate;
    else
        document.getElementById("scoreSP" + index).innerHTML = SPRate + ".0";
    document.getElementById("userPoint" + index).innerHTML = allList[5][thisPageList[index]];
    document.getElementById("applyClass" + index).innerHTML = allList[7][thisPageList[index]];
    document.getElementById("applyQuota" + index).innerHTML = allList[8][thisPageList[index]];
    document.getElementById("changeQuota" + index).value = allList[8][thisPageList[index]];
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
    document.getElementById("applyResult" + index).value = allList[12][thisPageList[index]];
    if (allList[13][thisPageList[index]] != "None") {
        document.getElementById("downloadBlock" + index).removeAttribute("style");
        document.getElementById("download" + index).href = "/apply/apply_pdf_download/" + allList[6][thisPageList[index]];
    }
    else {
        document.getElementById("downloadBlock" + index).style.display = 'none';
    }
}
/*function downloadPDF(index)
{
    var downloadPDFRequest = new XMLHttpRequest();
    downloadPDFRequest.open("POST", "/apply/apply_pdf_download");
    downloadPDFRequest.setRequestHeader("Content-Type", "application/json");
    downloadPDFRequest.send(JSON.stringify({"applyID": allList[6][thisPageList[index]]}));
    downloadPDFRequest.onload = function()
    {
        console.log(downloadPDFRequest.responseText);
        rst = JSON.parse(downloadPDFRequest.responseText);
        console.log(rst.rspCode);
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
}*/

function approve(index, type)
{
    if (index == 2)
    {
        var newQuota = document.getElementById("changeQuota" + 0).value;
        if (newQuota == allList[8][thisPageList[0]])
            newQuota = "";
        sendApprove(0, type, newQuota);

        newQuota = document.getElementById("changeQuota" + 1).value;
        if (newQuota == allList[8][thisPageList[1]])
            newQuota = "";
        sendApprove(1, type, newQuota);
    }
    else
    {
        var newQuota = document.getElementById("changeQuota" + index).value;
        if (newQuota == allList[8][thisPageList[index]])
            newQuota = "";
        sendApprove(index, type, newQuota);
    }
}

function sendApprove(index, type ,newQuota)
{
    var approvePDFRequest = new XMLHttpRequest();
    approvePDFRequest.open("POST", "/apply/apply_judge");
    approvePDFRequest.setRequestHeader("Content-Type", "application/json");
    approvePDFRequest.send(JSON.stringify({"applyID": allList[6][thisPageList[index]], "applyStatus": type, "quotaChange": newQuota, "adminID": "1"}));
    approvePDFRequest.onload = function()
    {
        console.log(approvePDFRequest.responseText);
        rst = JSON.parse(approvePDFRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                if (type == 1) alert("已核准申請");
                else alert("已否決申請");
                window.location.reload();
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert("無法送出決定");
                break;
        }
    }
}