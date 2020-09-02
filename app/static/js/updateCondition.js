window.onload = function()
{
    getGroup();
    getApplier();
    getClass();
}

const error = document.getElementById("error");
const userClass = document.getElementById("userClass");
var classList = [];

// Show all error.
function showError(rspCode)
{
    error.removeAttribute('style');
    switch (rspCode)
    {
        case   200: error.innerHTML = ""; return ;
        case   300: error.innerHTML = '系統錯誤'; return ;
        case   400: error.innerHTML = '等待伺服器回應...'; return ;
        case 40010: error.innerHTML = "系統錯誤，變更申請對象失敗"; return ;
        case 40011: error.innerHTML = "系統錯誤，讀取申請對象失敗"; return ;
        case 40012: error.innerHTML = "系統錯誤，檔案上傳失敗"; return ;
        case 40112: error.innerHTML = "錯誤的檔案類型，僅限PDF檔"; error.style.color = "red"; return ;
        case 40212: error.innerHTML = "檔案過大，勿超過5MB"; error.style.color = "red"; return ;
        case 40013: error.innerHTML = "無法確認檔案狀態"; error.style.color = "red"; return ;
        case 40014: error.innerHTML = "系統錯誤，讀取類別失敗"; return ;
        case 40015: error.innerHTML = "系統錯誤，讀取週期與額度失敗"; return ;
        case 40016: error.innerHTML = "系統錯誤，申請條件更新失敗"; return ;
        case 40116: error.innerHTML = "請檢查輸入值，須介於0~50之間"; error.style.color = "red"; return ;
        case 40017: error.innerHTML = "刪除失敗"; return ;
        case 40018: error.innerHTML = "請選擇類別"; return ;
        case 40118: error.innerHTML = "系統錯誤，額度讀取失敗"; return ;
        case 40218: error.innerHTML = "查無額度資料"; return ;
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
                document.getElementById("group").value = rst.groupName;
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
                document.getElementById("oldFileDownload").style.display = "block";
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
            case "401": case 401:
                return ;
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
        var classQuotaLength = classList.length;
        userClass.add(new Option(allClass[i], allClass[i]));
        classList[classQuotaLength] = [];
        classList[classQuotaLength][0] = allClass[i];
    }
    getAllPeriodQuota();
    //console.log(classList);
}
// When user click 新增類別, show input text and button on the html.
function showAddClass()
{
    document.getElementById("oldClassDiv").style.display = "none";
    document.getElementById("addClassDiv").style.display = "inline-block";
}
// When user click 新增, add new class into select.
function addClass(index)
{
    // index: 1 -> add; 0 -> cancel
    var newClass = document.getElementById("newClass").value;
    if (newClass.length > 10)
    {
        error.innerHTML = "類別名稱請勿超過10字元";
        return ;
    }
    if (index == 1 && newClass != "")
    {
        userClass.add(new Option(newClass, newClass));
        userClass.options[userClass.options.length - 1].selected = true;
        var classQuotaLength = classList.length;
        classList[classQuotaLength] = [];
        classList[classQuotaLength][0] = newClass;
        for ( var i = 1; i <= 5; i++)
            classList[classQuotaLength][i] = 0;
        showQuota();
    }
    document.getElementById("oldClassDiv").style.display = "inline-block";
    document.getElementById("addClassDiv").style.display = "none";
}

// Get period and quota of each class.
function getAllPeriodQuota()
{
    for (var i = 0; i < classList.length; i++)
        getPeriodQuota(i);
}
function getPeriodQuota(index)
{
    var getApplierRequest = new XMLHttpRequest();
    getApplierRequest.open("POST", "http://192.168.1.144:5000/apply/output_allow_period");
    getApplierRequest.setRequestHeader("Content-Type", "application/json");
    //console.log(classList[index][0]);
    getApplierRequest.send(JSON.stringify({"class": classList[index][0]}));
    getApplierRequest.onload = function()
    {
        showError(200);
        console.log(index + getApplierRequest.responseText);
        rst = JSON.parse(getApplierRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                console.log("額度讀取成功");
                computeQuota(index, rst.periodList, rst.quotaList);
                return ;
            case "300": case 300:
                showError(300); return ;
            case "400": case 400:
                showError(40015); return ;
            case "401": case 401:
                return ;
        }
    }
    showError(400);
}
function computeQuota(index, periodList, quotaList)
{
    if (periodList.length != quotaList.length)
        console.log("資料庫錯誤");
    var once = 0, one = 0, three = 0, six = 0, year = 0;
    for (var i = 1; i <= 5; i++)
    {
        if (periodList[0])
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
        else i = 6;
    }
    classList[index][1] = once;
    classList[index][2] = one;
    classList[index][3] = three;
    classList[index][4] = six;
    classList[index][5] = year;
}
// Show quota when user select a class.
userClass.addEventListener("change", showQuota);
function showQuota()
{
    index = userClass.selectedIndex - 1;
    for (var i = 0; i < 5; i++)
    {
        document.getElementById("period" + i).value = classList[index][i + 1];
        if (classList[index][i + 1] != 0)
            document.getElementsByName("period")[i].checked = true;
        else
            document.getElementsByName("period")[i].checked = false;
    }
}

// Update eeach data.
function updateGroup()
{
    var updateGroupRequest = new XMLHttpRequest();
    updateGroupRequest.open("POST", "http://192.168.1.144:5000/apply/update_apply_group");
    updateGroupRequest.setRequestHeader("Content-Type", "application/json");
    updateGroupRequest.send(JSON.stringify({"groupName": document.getElementById("group").value}));
    updateGroupRequest.onload = function()
    {
        showError(200);
        console.log(updateGroupRequest.responseText);
        rst = JSON.parse(updateGroupRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("申請對象更新成功");
                return ;
            case "300": case 300:
                showError(300); return ;
            case "400": case 400:
                showError(40010); return ;
            case "401": case 401:
                return ;
        }
    }
    showError(400);
}

function updateFile()
{

}

// Edit quota.
function editQuota()
{
    //var indexList = [0, 30, 90, 180, 365];
    if (userClass.selectedIndex != 0)
    {
        for (var i = 0; i < 5; i++)
        {
            var newQuota = document.getElementById("period" + i).value;
            if(0 <= newQuota && newQuota < 50)
            {
                classList[userClass.selectedIndex - 1][i + 1] = newQuota;
            }
            else error.innerHTML = "請輸入位於0~50之間的數值";
        }
    }
    showQuota();
    //console.log(classList[userClass.selectedIndex - 1]);
}
function updateClassPeriodQuota()
{
    editQuota();
    for (var i = 0; i < classList.length; i++)
        updateOneClassPeriodQuota(i);
}
function updateOneClassPeriodQuota(index)
{
    var updateCPQRequest = new XMLHttpRequest();
    updateCPQRequest.open("POST", "http://192.168.1.144:5000/apply/update_add_apply_quota");
    updateCPQRequest.setRequestHeader("Content-Type", "application/json");
    console.log(JSON.stringify({"class": classList[index][0], "once": classList[index][1], "one": classList[index][2], "three": classList[index][3], "six": classList[index][4], "year": classList[index][5]}));
    updateCPQRequest.send(JSON.stringify({"class": classList[index][0], "once": classList[index][1]+"", "one": classList[index][2]+"", "three": classList[index][3]+"", "six": classList[index][4]+"", "year": classList[index][5]+""}));
    updateCPQRequest.onload = function()
    {
        showError(200);
        console.log(index + updateCPQRequest.responseText);
        rst = JSON.parse(updateCPQRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                error.innerHTML = "更新完成";
                return ;
            case "300": case 300:
                showError(300); return ;
            case "400": case 400:
                alert("系統錯誤，申請條件更新失敗：" + classList[index][0]);
                showError(40016); return ;
            case "401": case 401:
                alert("請檢查輸入值，須介於0~50之間：" + classList[index][0]);
                showError(40116); return ;
        }
    }
    showError(400);
}

// Delete class.
function deleteClass()
{
    index = userClass.selectedIndex - 1;
    var deleteClassRequest = new XMLHttpRequest();
    deleteClassRequest.open("POST", "http://192.168.1.144:5000/apply/delete_apply_class");
    deleteClassRequest.setRequestHeader("Content-Type", "application/json");
    deleteClassRequest.send(JSON.stringify({"class": classList[index][0]}));
    deleteClassRequest.onload = function()
    {
        showError(200);
        console.log(deleteClassRequest.responseText);
        rst = JSON.parse(deleteClassRequest.responseText);
        switch (rst.rspCode)
        {
            case "200": case 200:
                alert("條件已刪除");
                window.location.reload();
                return ;
            case "300": case 300:
                showError(300); return ;
            case "400": case 400:
                showError(40017); return ;
            case "401": case 401:
                return ;
        }
    }
    showError(400);
}