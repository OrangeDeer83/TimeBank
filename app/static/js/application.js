window.onload = function()
{
    getGroup();
    getApplier();
    getClass();
}

const error = document.getElementById("error");
const userClass = document.getElementById("userClass");
var classList = [];
var currentQuotaList = [5];

// Show all error.
function showError(rspCode)
{
    error.style.color = "red";
    switch (rspCode)
    {
        case   200: error.innerHTML = "已就緒..."; error.style.color = "white"; return ;
        case   300: error.innerHTML = "系統錯誤"; return ;
        case   400: error.innerHTML = "等待伺服器回應..."; error.style.color = "white"; return ;
        case 40011: error.innerHTML = "系統錯誤，讀取申請對象失敗"; return ;
        case 40013: error.innerHTML = "無法確認檔案狀態"; return ;
        case 40014: error.innerHTML = "系統錯誤，讀取類別失敗"; return ;
        case 40015: error.innerHTML = "系統錯誤，讀取週期與額度失敗"; return ;
        case 40019: error.innerHtml = "系統錯誤，無法送出申請"; return ;
        case 40119: error.innerHtml = "無法送出申請，未知的類別"; return ;
        case 40219: error.innerHtml = "無法送出申請，選擇其他請填寫原因"; return ;
        case 40319: error.innerHtml = "無法送出申請，請確認資料填寫有無錯誤"; return ;
        case 40419: error.innerHtml = "無法送出申請，文件上傳錯誤"; return ;
    }
}

// Get group name from server.
function getGroup()
{
    var getGroupRequest = new XMLHttpRequest();
    getGroupRequest.open("GET", "http://192.168.1.144:5000/apply/output_apply_group");
    getGroupRequest.setRequestHeader("Content-Type", "application/json");
    getGroupRequest.send();
    getGroupRequest.onload = function()
    {
        showError(200);
        console.log(getGroupRequest.responseText);
        rst = JSON.parse(getGroupRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("申請對象讀取成功");
                document.getElementById("group").innerHTML = rst.groupName;
                return ;
            case "300": case 300:
                showError(300); return ;
            case "400": case 400:
                showError(40011); return ;
        }
    }
    showError(400);
}

// Check the condition pdf is exist or not.
function getApplier()
{
    var getApplierRequest = new XMLHttpRequest();
    getApplierRequest.open("GET", "http://192.168.1.144:5000/apply/output_apply_condition_pdf");
    getApplierRequest.setRequestHeader("Content-Type", "application/json");
    getApplierRequest.send();
    getApplierRequest.onload = function()
    {
        showError(200);
        console.log(getApplierRequest.responseText);
        rst = JSON.parse(getApplierRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("申請條件已存在");
                document.getElementById("conditionDescription").style.display = "block";
                return ;
            case "300": case 300:
                showError(300); return ;
            case "400": case 400:
                showError(40013); return ;
            case "401": case 401:
                return ;
        }
    }
    showError(400);
}

// Get class from server and display on html.
function getClass()
{
    var getApplierRequest = new XMLHttpRequest();
    getApplierRequest.open("GET", "http://192.168.1.144:5000/apply/output_apply_class");
    getApplierRequest.setRequestHeader("Content-Type", "application/json");
    getApplierRequest.send();
    getApplierRequest.onload = function()
    {
        showError(200);
        console.log(getApplierRequest.responseText);
        rst = JSON.parse(getApplierRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("類別讀取成功");
                showClass(rst.allClass);
                return ;
            case "300": case 300:
                showError(300); return ;
            case "400": case 400:
                showError(40014); return ;
        }
    }
    showError(400);
}
function showClass(allClass)
{
    allClass.reverse();
    userClass.options.length = 1;
    for (var i = 0; i < allClass.length; i++)
    {
        userClass.add(new Option(allClass[i], allClass[i]));
        classList[i + 1] = userClass[userClass.length - 1].value;
    }
    userClass.add(new Option("其他", "其他"));
    classList[i + 1] = userClass[userClass.length - 1].value;
}
// Show period when user select a class.
userClass.addEventListener("change", getPeriod);
function getPeriod()
{
    console.log(userClass.selectedIndex);
    getPeriodQuota(userClass.selectedIndex);
}

// Get period and quota of user's select.
function getPeriodQuota(index)
{
    if (index < 0 || classList.length <= index) // Index is out of list.
        return ;
    else  if (index == classList.length - 1) // Option of else.
    {
        for (var i = 0; i < 5; i++) currentQuotaList[i] = 0;
        showPeriod();
        return ;
    }
    
    var getApplierRequest = new XMLHttpRequest();
    getApplierRequest.open("POST", "http://192.168.1.144:5000/apply/output_allow_period");
    getApplierRequest.setRequestHeader("Content-Type", "application/json");
    getApplierRequest.send(JSON.stringify({"class": classList[index]}));
    getApplierRequest.onload = function()
    {
        showError(200);
        console.log(index + getApplierRequest.responseText);
        rst = JSON.parse(getApplierRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("額度讀取成功");
                computeQuota(rst.periodList, rst.quotaList);
                return ;
            case "300": case 300:
                showError(300); return ;
            case "400": case 400:
                showError(40015); return ;
        }
    }
    showError(400);
}
function computeQuota(periodList, quotaList)
{
    if (periodList.length != quotaList.length)
        console.log("資料庫錯誤");
    var once = 0, one = 0, three = 0, six = 0, year = 0;
    for (var i = 0; i < 5; i++)
    {
        if (periodList[0] === "")
        {
            i = 6;
        }
        else
        {
            switch (periodList.shift())
            {
                case "0": case 0:
                    once = quotaList.shift();
                    break;
                case "30": case 30:
                    one = quotaList.shift();
                    break;
                case "90": case 90:
                    three = quotaList.shift();
                    break;
                case "180": case 180:
                    six = quotaList.shift();
                    break;
                case "365": case 365:
                    year = quotaList.shift();
                    break;
            }
        }
    }
    currentQuotaList[0] = once;
    currentQuotaList[1] = one;
    currentQuotaList[2] = three;
    currentQuotaList[3] = six;
    currentQuotaList[4] = year;
    showPeriod();
}
function showPeriod()
{
    for (var i = 4; i >= 0; i--)
    {
        if (currentQuotaList[i] != 0 || userClass.selectedIndex == (classList.length - 1))
        {
            document.getElementById("period" + i).style.display = "inline-block";
            document.getElementById("period" + i).checked = true;
            document.getElementById("periodLabel" + i).style.display = "inline-block";
            showQuota(i);
        }
        else
        {
            document.getElementById("period" + i).style.display = "none";
            document.getElementById("periodLabel" + i).style.display = "none";
        }
    }
}

function showQuota(index)
{
    document.getElementById("applyQuota").value = currentQuotaList[index];
    if (index != 0)
    {
        document.getElementById("applyFrequencyDiv").style.display = "block";
        document.getElementById("applyFrequency").value = "";
    }
    else
    {
        document.getElementById("applyFrequencyDiv").style.display = "none";
        document.getElementById("applyFrequency").value = "1";
    }
}

// Send application to the server.
function sendApplication()
{
    // Get value and check.
    var selectedClass;
    if (userClass.selectedIndex != 0 && userClass.selectedIndex != "0")
    {
        selectedClass = userClass[userClass.selectedIndex].value;
    }
    else
    {
        error.innerHTML = "請選擇類別";
        return ;
    }
    var applyReason = document.getElementById("applyReason").value;
    if (userClass.selectedIndex == (userClass.length - 1) && applyReason == "")
    {
        error.innerHTML = "請輸入申請原因";
        return ;
    }
    var period;
    for (var i = 0; i < 5; i++)
    {
        var radio = document.getElementById("period" + i)
        if (radio.checked)
        {
            period = radio.value;
            i = 5;
        }
    }
    var quota = document.getElementById("applyQuota").value;
    if (quota < 0 || 99999 < quota)
    var frequency = document.getElementById("applyFrequency").value;
    if (frequency < 0 || 999999 < frequency)
    {
        error.innerHTML = "請輸入介於0~999999之間的領取次數";
        return ;
    }

    var sendApplicationRequest = new XMLHttpRequest();
    sendApplicationRequest.open("POST", "http://192.168.1.144:5000/application/json");
    sendApplicationRequest.setRequestHeader("Content-Type", "application/json");
    sendApplicationRequest.send(JSON.stringify({"frequency": frequency, "period": period, "result": applyReason, "class": selectedClass, "quota": quota, "file": ""}));
    sendApplicationRequest.onload = function()
    {
        showError(200);
        console.log(sendApplicationRequest.responseText);
        rst = JSON.parse(sendApplicationRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("申請成功送出");
                return ;
            case "300": case 300:
                showError(300); return ;
            case "400": case 400:
                showError(40019); return ;
            case "401": case 401:
                showError(40119); return ;
            case "402": case 402:
                showError(40219); return ;
            case "403": case 403:
                showError(40319); return ;
            case "404": case 404:
                showError(40419); return ;
        }
    }
    showError(400);
}