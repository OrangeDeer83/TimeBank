repeat = false;

function detect_repeated(){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://114.39.116.18:5000/detect_repeated");
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({"userID": document.getElementById('userID').value}));
    xhr.onload = function(){
        rsp = JSON.parse(xhr.responseText);
        console.log(xhr.responseText);
        if (rsp.rspCode == "400") {
            document.getElementById('warning').innerHTML = "帳號重複";
            repeat = true;
        }
        else {
            document.getElementById('warning').innerHTML = "";
            repeat = false;
        }
    }
}

function register(){
    if (!repeat) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://192.168.100.50:5000/USER_register");
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({"userName": document.getElementById('userName').value, "userID": document.getElementById('userID').value, "userPassword": document.getElementById('userPw').value, "userMail": document.getElementById('userMail').value, "userPhone": document.getElementById('userPhone').value, "userGender": document.getElementById('userGender').value, "userBirthday": document.getElementById('userBirthday').value}))
        xhr.onload = function(){
            alert(xhr.responseText)
            rsp = JSON.parse(xhr.responseText);
            if (rsp.rspCode == "200") {
                alert("註冊成功");
                window.location.assign("http://114.39.116.18:5000/directory");
            }
            else {
                alert("註冊失敗，請再試一次");
            }
        }
    }
}