window.onload = function()
{
    getClassList();
    getUserList();
}

var allList = [18];
// name, userName, userID, userSRRate, userSPRate, userPoint(pointAmount)
// applyID, applyClass(className), oldQuota, applyTime, applyPeriod, applyFrequency, applyResult
// applyStatus(applyResult), quota(resultQuota), judgeTime, judgeAdmin
var applyAmount = 0;
var currentApply = 0;
const pageNumber = document.getElementById("pageNumber");
var searchText;

function search()
{
    getUserList();
}

function getClassList()
{
    var getClassListRequest = new XMLHttpRequest();
    getClassListRequest.open("GET", "/apply/history_className_list");
    getClassListRequest.setRequestHeader("Content-Type", "application/json");
    getClassListRequest.send();
    getClassListRequest.onload = function()
    {
        console.log(getClassListRequest.responseText);
        rst = JSON.parse(getClassListRequest.responseText);
        switch (rst.rspCode)
        {
            case "20": case 20:
                putClassName(rst.classList);
                break;
            default:
                pageNumber.innerHTML = "無法取得類別列表";
                break;
        }
    }
}

function putClassName(classList)
{
    const searchClass = document.getElementById('searchClass');
    for (var i = 0; i < classList.length; i++)
    {
        searchClass.add(new Option(classList[i], classList[i]));
    }
    searchClass.add(new Option('其他', '其他'));
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
                applyAmount = allList[0].length;
            }
            break;
        case 1:
            if (currentApply == 0) return false;
            else currentApply--;
            break;
        case 2:
            if (currentApply == applyAmount - 1) return false;
            else currentApply++;
            break;
    }
    if (applyAmount == 0)
    {
        pageNumber.innerHTML = "查無使用者申請紀錄";
        clearDetail();
        return ;
    }
    else
    {
        pageNumber.innerHTML = (currentApply + 1) + "/" + applyAmount;
        putDetail();
    }
}

function putDetail()
{
    document.getElementById("name").innerHTML = allList[0][currentApply];
    document.getElementById("userName").innerHTML = allList[1][currentApply];
    var SRRate = Math.round(allList[3][currentApply] * 100) / 100;
    if (SRRate == 0)
        document.getElementById("SRRate").innerHTML = "無";
    else if (SRRate * 10 % 10 != 0)
        document.getElementById("SRRate").innerHTML = SRRate;
    else
        document.getElementById("SRRate").innerHTML = SRRate + ".0";
    var SPRate = Math.round(allList[4][currentApply] * 100) / 100;
    if (SPRate == 0)
        document.getElementById("SPRate").innerHTML = "無";
    else if (SPRate * 10 % 10 != 0)
        document.getElementById("SPRate").innerHTML = SPRate;
    else
        document.getElementById("SPRate").innerHTML = SPRate + ".0";
    document.getElementById('userPoint').innerHTML = allList[5][currentApply];
    document.getElementById("applyClass").innerHTML = allList[7][currentApply];
    document.getElementById("applyQuota").innerHTML = allList[8][currentApply];
    document.getElementById("applyTime").innerHTML = allList[9][currentApply];
    switch (allList[10][currentApply])
    {
        case '0': case 0:
            document.getElementById("applyPeriod").innerHTML = '一次性'; break;
        case '30': case 30:
            document.getElementById("applyPeriod").innerHTML = '一個月一次'; break;
        case '90': case 90:
            document.getElementById("applyPeriod").innerHTML = '三個月一次'; break;
        case '180': case 180:
            document.getElementById("applyPeriod").innerHTML = '半年一次'; break;
        case '365': case 365:
            document.getElementById("applyPeriod").innerHTML = '一年一次'; break;
    }
    document.getElementById("applyFrequency").innerHTML = allList[11][currentApply];
    document.getElementById("applyReason").value = allList[12][currentApply];
    if (allList[13][currentApply] == 1)
    {
        document.getElementById("applyResult").innerHTML = '核准';
        document.getElementById("resultQuotaDiv").removeAttribute('style');
    }
    else
    {
        document.getElementById("applyResult").innerHTML = '否決';
        document.getElementById("resultQuotaDiv").style.display = 'none';
    }
    document.getElementById("resultQuota").innerHTML = allList[14][currentApply];
    document.getElementById("judgeTime").innerHTML = allList[15][currentApply];
    document.getElementById("judgeAdmin").innerHTML = allList[16][currentApply];
    if (allList[17][currentApply] != "None") {
        document.getElementById("downloadBlock").removeAttribute("style");
        document.getElementById("download").href = "/apply/apply_pdf_download/" + allList[6][currentApply];
    }
    else {
        document.getElementById("downloadBlock").style.display = 'none';
    }
}

function clearDetail()
{
    document.getElementById("name").innerHTML = '';
    document.getElementById("userName").innerHTML = '';
    document.getElementById("SRRate").innerHTML = '';
    document.getElementById("SPRate").innerHTML = '';
    document.getElementById('userPoint').innerHTML = '';
    document.getElementById("applyClass").innerHTML = '';
    document.getElementById("applyQuota").innerHTML = '';
    document.getElementById("applyTime").innerHTML = '';
    document.getElementById("applyPeriod").innerHTML = '';
    document.getElementById("applyFrequency").innerHTML = '';
    document.getElementById("applyReason").value = '';
    document.getElementById("applyResult").innerHTML = '';
    document.getElementById("resultQuota").innerHTML = '';
    document.getElementById("judgeTime").innerHTML = '';
    document.getElementById("judgeAdmin").innerHTML = '';
    document.getElementById("downloadBlock").style.display = 'none';
}

/*function downloadPDF()
{
    var downloadPDFRequest = new XMLHttpRequest();
    downloadPDFRequest.open("POST", "/apply/apply_pdf_download");
    downloadPDFRequest.setRequestHeader("Content-Type", "application/json");
    downloadPDFRequest.send(JSON.stringify({"applyID": allList[6][currentApply]}));
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
}*/