window.onload = function()
{
    getUserList();
}

var allList = [14];
// name, userName, userID, userSRRate, userSPRate, userPoint(pointAmount)
// applyID, applyClass, applyQuota, applyTime, applyPeriod, applyFrequency, applyResult
var applyAmount = 0;
var currentApply = 0;
const pageNumber = document.getElementById("pageNumber");
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
                applyAmount = allList[0].length;
                if (currentApply >= applyAmount)
                    currentApply = applyAmount - 1;
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
        pageNumber.innerHTML = "查無使用者申請";
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
    console.log(currentApply)
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
    document.getElementById("userPoint").innerHTML = allList[5][currentApply];
    document.getElementById("applyClass").innerHTML = allList[7][currentApply];
    document.getElementById("applyQuota").innerHTML = allList[8][currentApply];
    document.getElementById("changeQuota").value = allList[8][currentApply];
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
    document.getElementById("applyResult").value = allList[12][currentApply];
    if (allList[13][currentApply] != "None") {
        document.getElementById("downloadBlock").removeAttribute("style");
        document.getElementById("download").href = "/apply/apply_pdf_download/" + allList[6][currentApply];
    }
    else {
        document.getElementById("downloadBlock").style.display = 'none';
    }
    document.getElementById('approve').removeAttribute('style');
    document.getElementById('deny').removeAttribute('style');
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
    document.getElementById("downloadBlock").style.display = 'none';
    document.getElementById('approve').style.display = 'none';
    document.getElementById('deny').style.display = 'none';
}

/*function downloadPDF(index)
{
    var downloadPDFRequest = new XMLHttpRequest();
    downloadPDFRequest.open("POST", "/apply/apply_pdf_download");
    downloadPDFRequest.setRequestHeader("Content-Type", "application/json");
    downloadPDFRequest.send(JSON.stringify({"applyID": allList[6][currentApply]}));
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

var approveAllAmount = 0;
function approve(index, applyStatus)
{
    if (index == 2) // Approve all application
    {
        approveAllAmount = 0;
        for (var i = 0; i < applyAmount; i++)
            sendApproveAll(allList[6][i], applyStatus, "");
    }
    else
    {
        var newQuota = document.getElementById("changeQuota").value;
        if (newQuota == allList[8][currentApply])
            newQuota = "";
        sendApprove(allList[6][currentApply], applyStatus, newQuota);
    }
}

var waitingOnload = 0;
function sendApprove(applyID, applyStatus, newQuota)
{
    if (waitingOnload == 1)
    {
        alert('請稍候伺服器回應');
        return ;
    }
    waitingOnload = 1;
    var approvePDFRequest = new XMLHttpRequest();
    approvePDFRequest.open("POST", "/apply/apply_judge");
    approvePDFRequest.setRequestHeader("Content-Type", "application/json");
    approvePDFRequest.send(JSON.stringify({"applyID": applyID, "applyStatus": applyStatus, "quotaChange": newQuota}));
    approvePDFRequest.onload = function()
    {
        waitingOnload = 0;
        console.log(approvePDFRequest.responseText);
        rst = JSON.parse(approvePDFRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                /*if (applyStatus == 1) alert("已核准申請");
                else alert("已否決申請");*/
                getUserList();
                break;
            case "401": case 401:
                alert('此申請已審核過');
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

function sendApproveAll(applyID, applyStatus, newQuota)
{
    if (waitingOnload == 1)
    {
        alert('請稍候伺服器回應');
        return ;
    }
    waitingOnload = 1;
    var approvePDFRequest = new XMLHttpRequest();
    approvePDFRequest.open("POST", "/apply/apply_judge");
    approvePDFRequest.setRequestHeader("Content-Type", "application/json");
    approvePDFRequest.send(JSON.stringify({"applyID": applyID, "applyStatus": applyStatus, "quotaChange": newQuota}));
    approvePDFRequest.onload = function()
    {
        waitingOnload = 0;
        console.log(approvePDFRequest.responseText);
        rst = JSON.parse(approvePDFRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                approveAllAmount++;
                if (approveAllAmount == applyAmount)
                {
                    if (applyStatus == 1) alert("已核准所有申請");
                    else alert("已否決所有申請");
                    window.location.reload();
                }
                break;
            case "401": case 401:
                approveAllAmount++;
                //alert('此申請已審核過');
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                alert("無法送出決定");
                window.location.reload();
                break;
        }
    }
}