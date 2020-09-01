const urlPath = 'http://192.168.1.144:5000';
var haveNewNotice = 0;
var lastRequestOnload = 1;
showNavbar();
function showNavbar()
{
    document.getElementById('userNavbar').innerHTML =
    '<nav class="nav navbarBack">' +
    '<div class="navbarContainer">' +
        '<div class="navbarLeft">' +
            '<div class="dropdown menuIconBack" onclick="clickToSpan(\'menuIconSpan\')">' +
                '<div class="menuIcon"></div>' +
                '<ul class="dropdownMenu dropdownMenuLeft unspanned" id="menuIconSpan">' +
                    '<li class="hiddenLarge">' +
                        '<a class="navbarPointA" href="/USER/pointRecord">' +
                            '<img class="navbarPointImg" alt="Point" src="' + urlPath + '/static/img/point3.png" />' +
                            '<span id="navbarPoint1">0</span>' +
                        '</a>' +
                    '</li>' +
                    '<li><a href="/USER/allTask">所有任務</a></li>' +
                    '<li><a href="/USER/createTask">新增任務</a></li>' +
                    '<li><a href="/USER/calendar">行事曆</a></li>' +
                    '<li><a href="/USER/application">點數申請</a></li>' +
                    '<li><a href="/USER/setting">設定</a></li>' +
                    '<li><a id="logout" href="/account/logout">登出</a></li>' +
                '</ul>' +
            '</div>' +
        '</div>' +
        '<div class="navbarCenter">' +
            '<a class="navbarBrand" href="/USER">' +
                '<img class="navbarBrandImg" id="navbarBrandImg1" alt="TimeBank" src="' + urlPath + '/static/img/brandWhite.png" />' +
                '<img class="navbarBrandImg" id="navbarBrandImg2" alt="TimeBank" src="' + urlPath + '/static/img/brandColor.png" />' +
            '</a>' +
        '</div>' +
        '<div class="navbarRight">' +
            '<ul class="nav navbarUl">' +
                '<li class="dropdown">' +
                    '<div class="navbarNotice" id="navbarNotice" onclick="clickToSpan(\'noticeSpan\');getNewNotice();">通知</div>' +
                    '<ul id="noticeSpan" class="dropdownMenu dropdownMenuRight unspanned">' +
                        '<li><a><div>無新通知</div></a></li>' +
                        '<li><a href="/USER/notice"><div>顯示所有通知</div></a></li>' +
                    '</ul>' +
                '</li>' +
                '<li class="hiddenSmall">' +
                    '<a class="navbarPointA" href="/USER/pointRecord">' +
                        '<img class="navbarPointImg" alt="Point" src="' + urlPath + '/static/img/point3.png" />' +
                        '<span id="navbarPoint">0</span>' +
                    '</a>' +
                '</li>' +
            '</ul>' +
            '<a class="navbarPortrait" id="navbarUserID">' +
                '<img class="navbarPortraitImg" alt="Portrait"" />' +
            '</a>' +
        '</div>' +
    '</div>' +
    '</nav>';
    getUserID();
    getCurrentPointAmount();
    checkNoticeIndication();
}

// For all myself.
function getUserID()
{
    var getIDRequest = new XMLHttpRequest();
    getIDRequest.open("GET", "http://192.168.1.144:5000/account/get_ID");
    getIDRequest.setRequestHeader("Content-Type", "application/json");
    getIDRequest.send();
    getIDRequest.onload = function()
    {
        console.log(getIDRequest.responseText);
        rst = JSON.parse(getIDRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log(rst.ID);
                document.getElementById("navbarUserID").href = "/USER/info/" + rst.ID;
                getPropic(rst.ID);
                getCurrentPointAmount();
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("無法取得userID");
                break;
        }
    }
}

function getPropic(navbarUserId)
{
    var getPropicRequest = new XMLHttpRequest();
    getPropicRequest.open("POST", "http://192.168.1.144:5000/account/propic_exist");
    getPropicRequest.setRequestHeader("Content-Type", "application/json");
    getPropicRequest.send(JSON.stringify({"userID": navbarUserId}));
    getPropicRequest.onload = function()
    {
        console.log(getPropicRequest.responseText);
        rst = JSON.parse(getPropicRequest.responseText);
        var d = new Date();
		var time = "";
		if (d.getHours() < 10) {
			time += "0" + d.getHours();
		}
		else{
			time += d.getHours();
		}
		if (d.getMinutes() < 10) {
			time += "0" + d.getMinutes();
		}
		else{
			time += d.getMinutes();
		}
		if (d.getSeconds() < 10) {
			time += "0" +d.getSeconds();
		}
		else{
			time += d.getSeconds();
		}
        switch (rst.rspCode)
        {
            case "200": case 200:
                if (rst.exist == "1") document.getElementsByClassName("navbarPortraitImg")[0].src = "/static/img/propic/" + navbarUserId + ".jpg?v=" + time;
                else document.getElementsByClassName("navbarPortraitImg")[0].src = "/static/img/propic/default.jpg";
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                document.getElementsByClassName("navbarPortraitImg")[0].src = "/static/img/propic/default.jpg";
                break;
        }
    }
}

function getCurrentPointAmount()
{
    var getCurrentPointAmountRequest = new XMLHttpRequest();
    getCurrentPointAmountRequest.open("GET", "http://192.168.1.144:5000/point/total");
    getCurrentPointAmountRequest.setRequestHeader("Content-Type", "application/json");
    getCurrentPointAmountRequest.send();
    getCurrentPointAmountRequest.onload = function()
    {
        console.log(getCurrentPointAmountRequest.responseText);
        rst = JSON.parse(getCurrentPointAmountRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                document.getElementById("navbarPoint1").innerHTML = rst.point;
                document.getElementById("navbarPoint").innerHTML = rst.point;
                break;
            case "300": case 300:
            case "400": case 400:
            default:
                console.log("系統錯誤，無法取得點數數量")
                break;
        }
    }
}

function checkNoticeIndication()
{
    getNoticeIndication();
    // Check for new notice every second.
    window.setInterval(getNoticeIndication, 1500);///////////////////////////////////////
    // More then 10 sec not onload, reset the standard.
    window.setInterval(function(){ if (lastRequestOnload == 0)lastRequestOnload = 1;}, 10000);
}
function getNoticeIndication()
{
    if (haveNewNotice == 1 || lastRequestOnload == 0) return true;
    
    lastRequestOnload = 0;
    var noticeIndicateRequest = new XMLHttpRequest();
    noticeIndicateRequest.open('GET', 'http://192.168.1.144:5000/notice/new_indicate');
    noticeIndicateRequest.setRequestHeader('Content-Type', 'application/json');
    noticeIndicateRequest.send();
    noticeIndicateRequest.onload = function()
    {
        console.log(noticeIndicateRequest.responseText);
        rst = JSON.parse(noticeIndicateRequest.responseText);
        switch (rst.rspCode)
        {
            case "20": case 20:
                lastRequestOnload = 1;
                if (rst.notice == 1)
                {
                    haveNewNotice = 1;
                    document.getElementById('navbarNotice').setAttribute('style', 'background-color:rgba(255, 0, 0, .5);');
                    getCurrentPointAmount();
                }
                break;
            default:
                console.log('系統錯誤，無法確認通知');
                break;
        }
    }
}
function getNewNotice()
{
    console.log('getNewNotice')
    document.getElementById('navbarNotice').removeAttribute('style');
    lastRequestOnload = 0;
    
    var getNewNoticeRequest = new XMLHttpRequest();
    getNewNoticeRequest.open('GET', 'http://192.168.1.144:5000/notice/new_list');
    getNewNoticeRequest.setRequestHeader('Content-Type', 'application/json');
    getNewNoticeRequest.send();
    getNewNoticeRequest.onload = function()
    {
        console.log(getNewNoticeRequest.responseText);
        rst = JSON.parse(getNewNoticeRequest.responseText);
        switch (rst.rspCode)
        {
            case "20": case 20:
                haveNewNotice = 0;
                putNewNotice(rst.newNoticeList)
                break;
            default:
                console.log('系統錯誤，無法讀取新通知');
                break;
        }
    }
}
function putNewNotice(noticeList)
{
    const noticeSpan = document.getElementById('noticeSpan');
    noticeSpan.innerHTML = '';
    if (noticeList.length > 0)
    {
        
        for (var i = noticeList.length - 1; i >= 0; i--)
        {
            noticeSpan.innerHTML += '<li><a href="' + numToUrl(noticeList[i]['connectTo']) + '">' +
            '<div>' + noticeList[i].time +
            '</div><div>' + noticeList[i].content +'</div></a></li>';
        }
    }
    else
    {
        noticeSpan.innerHTML += '<li><a><div>無新通知</div></a></li>';
    }
    noticeSpan.innerHTML += '<li><a href="/USER/notice"><div>顯示所有通知</div></a></li>';
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
        case 9: return '/Admin/pointRecord';
    }
}

// Function for logout
/*const logoutButton = document.getElementById("logout");
logoutButton.addEventListener("click", logout);
function logout()
{
    var request = new XMLHttpRequest();

    request.open("GET", "http://192.168.1.144:5000/logout");

    if (request.readyState == 4 && request.status == 200)
    {
        console.log(request.responseText);
        rst = JSON.parse(request.responseText);

        if (rst.rspCode == "200" || rst.rspCode == 200)
        {
            console.log("Logout success");

        }
        else
        {
            alert("Error! Logout failed!");
        }
    }
    return false;
}*/