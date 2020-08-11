window.onload = function()
{
    getIntroduction();
    getNewsAmount();

}

// Introduction
// Get web introduction from server.
var introduction = "";
function getIntroduction()
{
    var getIntroductionRequest;
    if (window.XMLHttpRequest)
        getIntroductionRequest = new XMLHttpRequest();
    else // Old IE browser.
        getIntroductionRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getIntroductionRequest.open("GET", "http://192.168.1.146:5000/test/output_webIntro");
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
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("系統錯誤，網站介紹讀取失敗，請稍後再試");
                break;
        }
        introduction = rst.webIntro;
        document.getElementById("introduction").value = introduction;
        console.log(introduction);//
    }
    if (introduction == "")
        console.log("網站介紹載入失敗或尚無資料。");
}

// Send web introduction to server.
function storeIntroduction()
{
    var sendIntroduction;
    if (window.XMLHttpRequest)
        sendIntroduction = new XMLHttpRequest();
    else
        sendIntroduction = new ActiveXObject("Microsoft.XMLHTTP");
    sendIntroduction.open("POST", "http://192.168.1.146:5000/test/upload_web_intro");
    sendIntroduction.setRequestHeader("Content-Type", "application/json");
    sendIntroduction.send(JSON.stringify({"intro": document.getElementById("introduction").value}));
     
    sendIntroduction.onload = function()
    {
        console.log(sendIntroduction.responseText);
        rst = JSON.parse(sendIntroduction.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("網站介紹更新成功");
                return true;
            case "300": case 300:
            case "400": case 400:
                alert("系統錯誤，網站介紹更新失敗，請稍後再試");
                return false;
        }
    }
}

// News
var existNews;
var newsAmount;
var pageAmount = 1;
var thisPageList = [];
var thisPageTitles = [];
var thisPageText = [];
var currentPage = 1;
var changePage = document.getElementById("changePage");

// Get news amount.
function getNewsAmount()
{
    var getNewsAmountRequest;
    if (window.XMLHttpRequest)
        getNewsAmountRequest = new XMLHttpRequest();
    else
        getNewsAmountRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getNewsAmountRequest.open("GET", "http://192.168.1.146:5000/test/useful_numbers");
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
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("系統錯誤，最新消息數量讀取失敗，請稍後再試");
                return false;
        }
        maxNewsNum = rst.max; console.log(maxNewsNum);//
        existNews = rst.numberList; console.log(existNews);//
        newsAmount = existNews.length; console.log(newsAmount);//
        pageAmount = Math.ceil(newsAmount / 10); console.log(pageAmount);//
        computePage(0);
    }
    computePage(0);
}

// getDetails from server each news
function getTitle(i)
{
    var getOldTitleRequest;
    if (window.XMLHttpRequest)
        getOldTitleRequest = new XMLHttpRequest();
    else
        getOldTitleRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getOldTitleRequest.open("GET", "http://192.168.1.146:5000/test/output_news_title/" + thisPageList[i]);
    getOldTitleRequest.setRequestHeader("Content-Type", "application/json");
    getOldTitleRequest.send();
    var index = i; console.log(i + "" + index);
    getOldTitleRequest.onload = function()
    {
        console.log(getOldTitleRequest.responseText);
        rst = JSON.parse(getOldTitleRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("最新消息標題讀取成功");
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("系統錯誤，最新消息標題讀取失敗，請稍後再試");
                //return;
        }
        //thisPageTitles.push(rst.title);
        document.getElementById("newsOldTitle" + (index + 1)).innerHTML = rst.title;
        document.getElementById("newsTitle" + (index + 1)).value = rst.title;
    }
}
function getText(i)
{
    var getTextRequest;
    if (window.XMLHttpRequest)
        getTextRequest = new XMLHttpRequest();
    else
        getTextRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getTextRequest.open("GET", "http://192.168.1.146:5000/test/output_news_content/" + thisPageList[i]);
    getTextRequest.setRequestHeader("Content-Type", "application/json");
    getTextRequest.send();
    var index = i;
    getTextRequest.onload = function()
    {
        console.log(getTextRequest.responseText);
        rst = JSON.parse(getTextRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("最新消息內容讀取成功");
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("系統錯誤，最新消息內容讀取失敗，請稍後再試");
                //return;
        }
        //thisPageText.push(rst.content); console.log(rst.content);
        document.getElementById("newsText" + (index + 1)).value = rst.content;
    }
}

// Get news old title and text of current page.
function getDetails()
{
    thisPageTitles.length = 0;
    thisPageText.length = 0;
    
    for (var i = 0; i < thisPageList.length; i++)
    {
        getTitle(i);
        getText(i);
    }
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
     changePage.innerHTML = currentPage + "/" + pageAmount;
     computePageNews();
}

// Compute the index of this page, and show the titles.
function computePageNews()
{
    thisPageList.length = 0;
    if (currentPage < pageAmount)
        for (var i = 0; i < 10; i++)
            thisPageList.push(existNews[newsAmount - 10 * (currentPage - 1) - i - 1]);
    else
        for (var i = 0; i < (newsAmount % 10); i++)
            thisPageList.push(existNews[newsAmount - 10 * (currentPage - 1) - i - 1]);
    console.log(thisPageList);

    getDetails();

    for (var i = 1; i <= thisPageList.length; i++)
    {
        document.getElementById("news" + i).style.display = "block";
        /*document.getElementById("newsOldTitle" + i).innerHTML = thisPageTitles[i - 1];
        document.getElementById("newsTitle" + i).value = thisPageTitles[i - 1];
        document.getElementById("newsText" + i).value = thisPageText[i - 1];*/
    }
    for (var i = thisPageList.length + 1; i <= 10; i++)
        document.getElementById("news" + i).style.display = "none";
}

// Get currentSpannedNews index.
function getCurrentIndex()
{
    var newsSpan = document.getElementsByClassName("newsSpan");
    var currentSpan = document.getElementsByClassName("currentSpannedNews")[0];
    for (var i = 0; i < newsSpan.length; i++)
    {
        if (currentSpan == newsSpan[i])
            return i;
    }
    return -1;
}

// Preview the upload image.
function previewImg()
{
    var currentIndex = getCurrentIndex();
    console.log(currentIndex);//
    var img = document.getElementById("uploadImg" + currentIndex);
    var newsImg = document.getElementById("newsImg" + currentIndex);
    var reader = new FileReader;
    reader.readAsDataURL(img.files[0]);
    reader.onload = function()
    {   newsImg.src = this.result; }
}

// Display old image.
function oldImg(index, imgResult)
{
    var newsImg = document.getElementById("newsImg" + index);
    newsImg.src = imgResult;
}

// Click edit or add news, will span its newsInput.
function changeSpan(newIndex)
{
    var currentIndex = getCurrentIndex();
    if (currentIndex == newIndex); // Didn't change.
    else
    {
        var currentSpan = document.getElementsByClassName("currentSpannedNews")[0];
        var newSpan = document.getElementById("newsSpan" + newIndex);
        var currentClassVal = currentSpan.getAttribute("class");
        var newClassVal = newSpan.getAttribute("class");
        currentClassVal = currentClassVal.replace("currentSpannedNews", "");
        currentSpan.setAttribute("class", currentClassVal);
        newClassVal = newClassVal.replace("newsSpan", "newsSpan currentSpannedNews");
        newSpan.setAttribute("class", newClassVal);
        currentSpan.style.display = "none";
        newSpan.style.display = "block";
    }
    console.log("../static/uploadFile/newsImage/" + thisPageList[newIndex - 1] + ".jpg " + newIndex);
    if (newIndex != 0) // src="../static/uploadFile/newsImage/<number>.jpg"
        document.getElementById("newsImg" + newIndex).src = "../static/uploadFile/newsImage/" + thisPageList[newIndex - 1] + ".jpg";
}

function deleteNews(index)
{
    var deleteNewsRequest;
    if (window.XMLHttpRequest)
        deleteNewsRequest = new XMLHttpRequest();
    else
        deleteNewsRequest = new ActiveXObject("Microsoft.XMLHTTP");
    deleteNewsRequest.open("POST", "http://192.168.1.146:5000/test/delete_news/" + thisPageList[index - 1]);
    deleteNewsRequest.setRequestHeader("Content-Type", "application/json");
    deleteNewsRequest.send();
    deleteNewsRequest.onload = function()
    {
        console.log(deleteNewsRequest.responseText);
        rst = JSON.parse(deleteNewsRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("已刪除此最新消息")
                return true;
            default:
                console.log("系統錯誤，最新消息刪除失敗，請稍後再試");
                return false;
        }
    }
}

function editNews()
{
    var currentIndex = getCurrentIndex();
    var newsTitle = document.getElementById("newsTitle" + currentIndex).value;
    var newsText = document.getElementById("newsText" + currentIndex).value;
    var img = document.getElementById("uploadImg" + currentIndex);
    var reader = new FileReader;
    reader.readAsDataURL(img.files[0]);

    var editNewsRequest;
    if (window.XMLHttpRequest)
        editNewsRequest = new XMLHttpRequest();
    else
        editNewsRequest = new ActiveXObject("Microsoft.XMLHTTP");
    editNewsRequest.open("POST", "http://192.168.1.146:5000/test/edit_news/" + thisPageList[currentIndex - 1]);
    editNewsRequest.setRequestHeader("Content-Type", "application/json");
    editNewsRequest.send(JSON.stringify({"title": newsTitle, "content": newsText, "file": reader.result}));
    editNewsRequest.onload = function()
    {
        console.log(editNewsRequest.responseText);
        rst = JSON.parse(editNewsRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("已儲存最新消息之更新");
                return true;
            case "400": case 400:
                alert("圖片名錯誤，最新消息更新失敗");
                return false;
            case "401": case 401:
                alert("圖片更新失敗");
                return false;
            case "402": case 402:
                alert("標題更新失敗");
                return false;
            case "403": case 403:
                alert("內文更新失敗");
                return false;
            case "404": case 404:
                alert("標題太長");
                return false;
            default:
                alert("系統錯誤，最新消息更新失敗，請稍後再試");
                return false;
        }
    }
}

function addNews()
{
    var newsTitle = document.getElementById("newsTitle0").value;
    var newsText = document.getElementById("newsText0").value;
    var img = document.getElementById("uploadImg0");
    var reader = new FileReader;
    reader.readAsDataURL(img.files[0]);

    var addNewsRequest;
    if (window.XMLHttpRequest)
        addNewsRequest = new XMLHttpRequest();
    else
        addNewsRequest = new ActiveXObject("Microsoft.XMLHTTP");
    addNewsRequest.open("POST", "http://192.168.1.146:5000/test/upload_news/");
    addNewsRequest.setRequestHeader("Content-Type", "application/json");
    addNewsRequest.send(JSON.stringify({"title": newsTitle, "content": newsText, "file": reader.result}));
    addNewsRequest.onload = function()
    {
        console.log(addNewsRequest.responseText);
        rst = JSON.parse(addNewsRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("已新增最新消息");
                return true;
            case "400": case 400:
                alert("資料不完整，照片、標題與內容皆須填寫");
                return false;
            case "401": case 401:
                alert("圖片檔名錯誤");
                return false;
            case "402": case 402:
                alert("圖片新增失敗");
                return false;
            case "403": case 403:
                alert("內文新增失敗");
                return false;
            case "404": case 404:
                alert("標題新增失敗");
                return false;
            case "405": case 405:
                alert("標題過長");
                return false;
            default:
                alert("系統錯誤，最新消息新增失敗，請稍後再試");
                return false;
        }
    }
}