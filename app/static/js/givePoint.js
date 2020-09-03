window.onload = function()
{
    getUserList();
}

function showPrompt(index)
{
    const prompt = document.getElementById('systemPrompt');
    prompt.removeAttribute('style');
    switch(index)
    {
        case 200: prompt.innerHTML = '已就緒...'; break;
        case 400: prompt.innerHTML = '等待伺服器回應中...'; break;
        case 401: prompt.innerHTML = '系統錯誤，無法取得使用者列表'; break;
        case 402: prompt.innerHTML = '等待伺服器配發點數中...'; break;
        case 403: prompt.innerHTML = '未選擇使用者'; break;
        case 404: prompt.innerHTML = '請輸入配發額度(1~50)';
                  document.getElementById('quota').focus;
                  prompt.style.color = 'red';
                  break;
        case 405: prompt.innerHTML = '請選擇配發週期';
                  document.getElementById('period').focus;
                  prompt.style.color = 'red';
                  break;
        case 406: prompt.innerHTML = '請輸入發放次數(2~20)';
                  document.getElementById('frequency').focus;
                  prompt.style.color = 'red';
                  break;
        case 407: prompt.innerHTML = '系統錯誤，配發失敗'; break;
    }
}

var allList = [5]; // name, userName, userID, userSRRate, userSPRate, userPoint(pointAmount)
var userAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
const pageNumber = document.getElementById("pageNumber");
const maxPageAmount = 10;
var searchText;
var notOnload = 0;

function getUserList()
{
    searchText = document.getElementById("searchText").value
    var getListRequest = new XMLHttpRequest();
    getListRequest.open("POST", "/allotment/show_user");
    getListRequest.setRequestHeader("Content-Type", "application/json");
    getListRequest.send(JSON.stringify({"target": searchText}));
    getListRequest.onload = function()
    {
        console.log(getListRequest.responseText);
        rst = JSON.parse(getListRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                showPrompt(200);
                allList[0] = rst.userName;
                allList[1] = rst.name;
                allList[2] = rst.userID;
                allList[3] = rst.userSRRate;
                allList[4] = rst.userSPRate;
                allList[5] = rst.userPoint;
                computePage(0);
                break;
            case "300": case 300: // Methods wrong.
            case "400": case 400: // Database error.
                showPrompt(401);
                break;
        }
    }
    showPrompt(400);
}

function computePage(type)
{
    switch (type)
    {
        case 0: 
            if (allList[0].length != allList[1].length || allList[1].length != allList[2].length ||
                allList[2].length != allList[3].length || allList[3].length != allList[4].length ||
                allList[4].length != allList[5].length)
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
    document.getElementById("name" + index).innerHTML = allList[1][thisPageList[index]];
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
    document.getElementById("pointAmount" + index).innerHTML = allList[5][thisPageList[index]];
}

const periodSelect = document.getElementById("period");
periodSelect.addEventListener("change", periodChange);
function periodChange()
{
    var period = periodSelect[periodSelect.selectedIndex].value;
    if (period == "0")
    {
        document.getElementById("frequency").style.display = "none";
        document.getElementById("frequencySpan").style.display = "none";
        document.getElementById("frequency").value = "1";
    }
    else
    {
        document.getElementById("frequency").removeAttribute("style");
        document.getElementById("frequencySpan").removeAttribute("style");
        document.getElementById("frequency").value = "";
    }
}

function allotment(index)
{
    if (notOnload == 1)
    {
        showPrompt(402);
        return ;
    }
    // No user
    if (userAmount == 0)
    {
        showPrompt(403);
        return ;
    }
    // Quota should between 1~50.
    var quota = Math.round(document.getElementById("quota").value);
    if (quota == "" || quota < 1 || quota > 50)
    {
        showPrompt(404);
        return ;
    }
    // Must choose period.
    var period = periodSelect.options[periodSelect.selectedIndex].value;
    if (period == "none")
    {
        showPrompt(405);
        return ;
    }
    // frequency should between 2~50. Only period "0"'s frequency  is "1".
    var frequency = Math.round(document.getElementById("frequency").value);
    if (period != "0" && (frequency < 2 || frequency > 20))
    {
        showPrompt(406);
        return ;
    }
    
    notOnload = 1;
    if (index == 10)
    {
        sendAllotment("all", searchText, quota, period, frequency);
    }
    else if (0 <= index && index < 10)
        sendAllotment("one", allList[2][thisPageList[index]], quota, period, frequency);
}

function sendAllotment(kind, receiver, quota, period, frequency)
{
    var allotmentRequest = new XMLHttpRequest();
    allotmentRequest.open("POST", "/allotment/");
    allotmentRequest.setRequestHeader("Content-Type", "application/json");
    console.log(JSON.stringify({"kind": kind, "receiver": receiver, "quota": quota, "period": period, "frequency": frequency}))
    allotmentRequest.send(JSON.stringify({"kind": kind, "receiver": receiver, "quota": quota, "period": period, "frequency": frequency}));
    allotmentRequest.onload = function()
    {
        notOnload = 0;
        console.log(allotmentRequest.responseText);
        rst = JSON.parse(allotmentRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                showPrompt(200);
                alert("配發成功");
                getUserList();
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                showPrompt(407);
                break;
        }
    }
    showPrompt(400);
}