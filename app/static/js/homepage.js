// News and introduction of homepage and portal.
window.onload = function()
{
    getNewsAmount();
    getIntroduction();
}

var existNews = [];
var newsAmount = 0;
var pageAmount = 1;
var thisPageList = [];
var currentPage = 1;
var pageNumber = document.getElementById("pageNumber");
var currentNews = 0;

// Get news amount.
function getNewsAmount()
{
    var getNewsAmountRequest = new XMLHttpRequest();
    getNewsAmountRequest.open("GET", "http://192.168.1.144:5000/portal/useful_numbers");
    getNewsAmountRequest.setRequestHeader("Content-Type", "application/json");
    getNewsAmountRequest.send();
    getNewsAmountRequest.onload = function()
    {
        console.log(getNewsAmountRequest.responseText);
        rst = JSON.parse(getNewsAmountRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("最新消息數量讀取成功");
                maxNewsNum = rst.max;
                existNews = rst.numberList;
                newsAmount = existNews.length;
                pageAmount = Math.ceil(newsAmount / 5);
                computePage(0);
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("系統錯誤，最新消息數量讀取失敗，請稍後再試");
                return false;
        }
    }
    console.log("等待伺服器回應中...");
}

// Compute and react nextPage button, prePage button and number of pages.
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
     pageNumber.innerHTML = currentPage + "/" + pageAmount;
     computePageNews();
     spanNews(0);
}

// Compute the index of this page, and show the titles.
function computePageNews()
{
    thisPageList.length = 0;
    if (currentPage < pageAmount)
        for (var i = 0; i < 5; i++)
            thisPageList.push(existNews[newsAmount - 5 * (currentPage - 1) - i - 1]);
    else
    {
        if (newsAmount % 5 != 0)
            for (var i = 0; i < (newsAmount % 5); i++)
                thisPageList.push(existNews[newsAmount - 5 * (currentPage - 1) - i - 1]);
        else
            for (var i = 0; i < 5; i++)
                thisPageList.push(existNews[newsAmount - 5 * (currentPage - 1) - i - 1]);
    }

    getCarouselImg();
    getNewestNewsTitle();

    for (var i = 0; i < thisPageList.length; i++)
        document.getElementById("newsTitle" + i).style.display = "block";
    for (var i = thisPageList.length; i < 5; i++)
        document.getElementById("newsTitle" + i).style.display = "none";
}

// Put carouselImg
function getCarouselImg()
{
    for (var i = 0; i < thisPageList.length && i < 5; i++)
    {
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
        document.getElementById("carouselImg" + i).src = "../static/uploadFile/newsImage/" + thisPageList[i] + ".jpg?v=" + time;
    }
}

// Call getNewsTitle to put default news on the page.
function getNewestNewsTitle()
{
    for (var i = 0; i < thisPageList.length; i++) getNewsTitle(i);
}

// Get introduction from database.
function getIntroduction()
{
    var getIntroductionRequest = new XMLHttpRequest();
    getIntroductionRequest.open("GET", "http://192.168.1.144:5000/portal/output_webIntro");
    getIntroductionRequest.setRequestHeader("Content-Type", "application/json");
    getIntroductionRequest.send();
    getIntroductionRequest.onload = function()
    {
        console.log(getIntroductionRequest.responseText);
        rst = JSON.parse(getIntroductionRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("網站介紹讀取成功");
                introduction = rst.webIntro;
                console.log(introduction);
                document.getElementById("introduction").innerHTML = introduction;
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("系統錯誤，網站介紹讀取失敗，請稍後再試");
                document.getElementById("introduction").innerHTML = "伺服器錯誤...網站介紹讀取失敗";
                break;
        }
    }
    console.log("等待伺服器回應中...");
}

function getNewsTitle(index)
{
    var getTitleRequest = new XMLHttpRequest();
    getTitleRequest.open("GET", "http://192.168.1.144:5000/portal/output_news_title/" + thisPageList[index]);
    getTitleRequest.setRequestHeader("Content-Type", "application/json");
    getTitleRequest.send();
    getTitleRequest.onload = function()
    {
        console.log(getTitleRequest.responseText);
        rst = JSON.parse(getTitleRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("最新消息標題讀取成功");
                document.getElementById("newsTitle" + index).innerHTML = rst.title;
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("系統錯誤，最新消息標題讀取失敗，請稍後再試");
                //return;
        }
    }
}

// Switch newsContainer and introductionContainer.
function span(index)
{   // index = 0: newsButton; 1: introductionButton
    if (index == 0)
    {
        document.getElementById("newsContainer").style.display = "block";
        document.getElementById("introductionContainer").style.display = "none";
        document.getElementById("newsButton").style.background = "var(--button-hover-background-color)";
        document.getElementById("introductionButton").style.background = "var(--button-background-color)";
    }
    else if (index == 1)
    {
        document.getElementById("newsContainer").style.display = "none";
        document.getElementById("introductionContainer").style.display = "block";
        document.getElementById("introductionButton").style.background = "var(--button-hover-background-color)";
        document.getElementById("newsButton").style.background = "var(--button-background-color)";
    }
}

// Switch between newDetial of different newsTitle.
function spanNews(index)
{
    getNewsContent(index);
    document.getElementById("newsImg").src = "../static/uploadFile/newsImage/" + thisPageList[index] + ".jpg";
    document.getElementById("newsTitle" + currentNews).style.border = "1px solid #CCCCCC";
    currentNews = index;
    document.getElementById("newsTitle" + currentNews).style.border = "3px solid black";
}

function getNewsContent(index)
{
    var getContentRequest = new XMLHttpRequest();
    getContentRequest.open("GET", "http://192.168.1.144:5000/portal/output_news_content/" + thisPageList[index]);
    getContentRequest.setRequestHeader("Content-Type", "application/json");
    getContentRequest.send();
    getContentRequest.onload = function()
    {
        console.log(getContentRequest.responseText);
        rst = JSON.parse(getContentRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("最新消息內容讀取成功");
                document.getElementById("newsContent").value = rst.content;
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("系統錯誤，最新消息內容讀取失敗，請稍後再試");
                document.getElementById("newsContent").value = "伺服器錯誤...內容讀取失敗";
        }
    }
    console.log("等待伺服器回應中...");
}

// Click to span. Login.
// Find the check word: spanned or unspanned.
// If found, return true; if not found, return false.
function contains(classString, check)
{
    for (var i = 0; i < classString.length; i++)
    {
        var wordNow = "";
        // Splite the string by " ".
        while(classString[i] != " " && i < classString.length)
        {
            wordNow = wordNow + classString[i];
            i++;
        }
        // Check word found.
        if (wordNow == check) return true;
    }
    return false;
}

// If unspanned and onclick, span the element of the name by "display: block".
// If spanned and onclick, hide the element of the name by "display: ''".
function clickToSpan(name)
{
    var element = document.getElementById(name); // Save the element of the name.
    var classVal = element.getAttribute("class"); // Save the class string of the element.
    if (contains(classVal, "spanned")) // Hide the element.
    {
        element.style.display = "";
        classVal = classVal.replace("spanned","unspanned");
        element.setAttribute("class", classVal);
    }
    else if (contains(classVal, "unspanned")) // Span the element.
    {
        element.style.display = "block";
        classVal = classVal.replace("unspanned","spanned");
        element.setAttribute("class", classVal);
    }
}