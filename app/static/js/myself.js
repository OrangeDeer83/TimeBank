// For all myself.
var userID;
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
                userID = rst.ID;
                document.getElementById("navbarUserID").href = "/USER/info/" + rst.ID;
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("無法取得userID");
                break;
        }
    }
}

function getProfile()
{
    var getProfileRequest = new XMLHttpRequest();
    getProfileRequest.open("POST", "http://192.168.1.144:5000/profile/output/info");
    getProfileRequest.setRequestHeader("Content-Type", "application/json");
    getProfileRequest.send(JSON.stringify({"userID": getToken()}));
    getProfileRequest.onload = function()
    {
        console.log(getProfileRequest.responseText);
        rst = JSON.parse(getProfileRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                showProfile(rst);
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("無法取得使用者介紹");
                break;
        }
    }
}

function showProfile(profile)
{
    document.getElementById("name").innerHTML = profile.name;
    switch(profile.userGender * 1)
    {
        case 0: document.getElementById("gender").innerHTML = "男"; break;
        case 1: document.getElementById("gender").innerHTML = "女"; break;
        case 2: document.getElementById("gender").innerHTML = "其他"; break;
    }
    document.getElementById("age").innerHTML = profile.userAge;
    document.getElementById("profile").innerHTML = profile.userInfo;
}

function getPropicMyself()
{
    var propicID = getToken();
    var getPropicRequest = new XMLHttpRequest();
    getPropicRequest.open("POST", "http://192.168.1.144:5000/account/propic_exist");
    getPropicRequest.setRequestHeader("Content-Type", "application/json");
    getPropicRequest.send(JSON.stringify({"userID": propicID}));
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
                if (rst.exist == "1") document.getElementById("profilePicture").src = "/static/img/propic/" + propicID + ".jpg?v=" + time;
                else document.getElementById("profilePicture").src = "/static/img/propic/default.jpg";
                break;
            case "300": case 300:
            case "400": case 400:
                console.log("無法取得照片存在");
                break;
        }
    }
}