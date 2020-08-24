getUserID();

// For all myself.
function getUserID()
{
    var getIDRequest;
    if (window.XMLHttpRequest)
        getIDRequest = new XMLHttpRequest();
    else
        getIDRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getIDRequest.open("GET", "/account/get_ID");
    getIDRequest.setRequestHeader("Content-Type", "application/json");
    getIDRequest.send();console.log(1);
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
    var getPropicRequest;
    if (window.XMLHttpRequest)
        getPropicRequest = new XMLHttpRequest();
    else
        getPropicRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getPropicRequest.open("POST", "/account/propic_exist");
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
                console.log("無法取得照片存在");
                break;
        }
    }
}

function getCurrentPointAmount()
{
    var getCurrentPointAmountRequest;
    if (window.XMLHttpRequest)
        getCurrentPointAmountRequest = new XMLHttpRequest();
    else
        getCurrentPointAmountRequest = new ActiveXObject("Microsoft.XMLHTTP");
    getCurrentPointAmountRequest.open("GET", "/point/total");
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

// Find the check word: spanned or unspanned.
// If found, return true; if not found, return false.
function contains(classString, check)
{
    for (var i = 0; i < classString.length; i++)
    {
        console.log("Find " + check + " in " + classString);
        var wordNow = "";
        // Splite the string by " ".
        while(classString[i] != " " && i < classString.length)
        {
            wordNow = wordNow + classString[i];
            i++;
        }
        // Check word found.
        if (wordNow == check)
        {
            return true;
        }
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
        console.log("Spanned.");
    }
    else if (contains(classVal, "unspanned")) // Span the element.
    {
        element.style.display = "block";
        classVal = classVal.replace("unspanned","spanned");
        element.setAttribute("class", classVal);
        console.log("Hide.");
    }
}

// Function for logout
/*const logoutButton = document.getElementById("logout");
logoutButton.addEventListener("click", logout);
function logout()
{
    var request;
    if (window.XMLHttpRequest)
            request = new XMLHttpRequest();
    else // Old IE browser.
        request = new ActiveXObject("Microsoft.XMLHTTP");

    request.open("GET", "/logout");

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