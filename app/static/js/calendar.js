window.onload = function()
{
    giveDay(0);
}

// Current -> the date at the moment user open the web.
const currentYear = new Date().getFullYear();
var pageYear = currentYear;
const currentMonth = new Date().getMonth() + 1; // 0~11 -> 1~12
var pageMonth = currentMonth;
const currentDay = new Date().getDate();
var selectedDay = currentDay;
// Save date list of this month which has tasks.
// 0-> no task, 1-> at least one task, 2-> the month don't have this date
var thisMonthDateList = [31];
const toDoList = document.getElementById("formToDoList"); // For function putDayList

// Put dates on the schedule, even open the web, or click premonth and nextmonth button.
function giveDay(type)
{
    // type: 0 -> current month; 1 -> prev Month; 2 -> next month
    if (type == 1)
    {
        if (pageMonth == 1)
        {
            pageMonth = 12;
            pageYear--;
        }
        else pageMonth--;
    }
    else if (type == 2)
    {
        if (pageMonth == 12)
        {
            pageMonth = 1;
            pageYear++;
        }
        else pageMonth++;
    }
    // Year
    document.getElementById("year").innerHTML = pageYear;
    // Month
    switch (pageMonth)
    {
        case  1: 
            document.getElementById("month").innerHTML = "January"; break;
        case  2: 
            document.getElementById("month").innerHTML = "February"; break;
        case  3: 
            document.getElementById("month").innerHTML = "March"; break;
        case  4: 
            document.getElementById("month").innerHTML = "April"; break;
        case  5: 
            document.getElementById("month").innerHTML = "May"; break;
        case  6: 
            document.getElementById("month").innerHTML = "June"; break;
        case  7: 
            document.getElementById("month").innerHTML = "July"; break;
        case  8: 
            document.getElementById("month").innerHTML = "August"; break;
        case  9: 
            document.getElementById("month").innerHTML = "September"; break;
        case 10: 
            document.getElementById("month").innerHTML = "October"; break;
        case 11: 
            document.getElementById("month").innerHTML = "November"; break;
        case 12: 
            document.getElementById("month").innerHTML = "December"; break;
    }

    var firstWeekOfMonth = new Date(pageYear, pageMonth - 1, 1).getDay();
    var maxDayOfMonth = new Date(pageYear, pageMonth, 0).getDate();
    for (var i = firstWeekOfMonth; i < firstWeekOfMonth + maxDayOfMonth; i++)
    {
        if (i < 35)
        {
            document.getElementById("formDay" + i).innerHTML = i + 1 - firstWeekOfMonth;
            document.getElementById("formDay" + i).setAttribute("onclick", "selectDay(" + (i + 1 - firstWeekOfMonth) + ",1)");
        }
        else
        {
            document.getElementById("formDay" + (i - 7)).innerHTML += "/" + (i + 1 - firstWeekOfMonth);
            document.getElementById("formDay" + (i - 7)).setAttribute("onclick", "selectDay(" + (i - 6 - firstWeekOfMonth) + "," + (i + 1 - firstWeekOfMonth) +")");
        }
    }
    // Clear old dates.
    for (var i = 0; i < firstWeekOfMonth; i++)
    {
        document.getElementById("formDay" + i).innerHTML = "";
        document.getElementById("formDay" + i).removeAttribute("onclick");
    }
    for (var i = firstWeekOfMonth + maxDayOfMonth; i < 35; i++)
    {
        document.getElementById("formDay" + i).innerHTML = "";
        document.getElementById("formDay" + i).removeAttribute("onclick");
    }

    // Get list of the month.
    if (pageMonth == currentMonth && pageYear == currentYear)
        getMonthList(pageYear, pageMonth, currentDay);
    else
        getMonthList(pageYear, pageMonth, 1);
}

// Get a list of the month to show which day has tasks. (When window onload or page changed)
function getMonthList(year, month, day)
{
    var selectDayRequest = new XMLHttpRequest();
    selectDayRequest.open("POST", "http://192.168.1.144:5000/calendar/one_month_list");
    selectDayRequest.setRequestHeader("Content-Type", "application/json");
    selectDayRequest.send(JSON.stringify({"year": year, "month": month}));
    selectDayRequest.onload = function()
    {
        console.log(selectDayRequest.responseText);
        rst = JSON.parse(selectDayRequest.responseText);
        switch (rst.rspCode)
        {
            case "20": case 20:
                thisMonthDateList = rst.dateList; // 0, 1, 2(number array)
                colorTaskDates();
                selectDay(day, 1);
                break;
            default:
                console.log("無法取得當月有任務日期");
                break;
        }
    }
}

// If that date has at least one task, color it.
function colorTaskDates()
{
    var firstWeekOfMonth = new Date(pageYear, pageMonth - 1, 1).getDay();
    for (var i = 0; i < thisMonthDateList.length; i++)
    {
        if (thisMonthDateList[i] == 1)
        {
            if (firstWeekOfMonth + i < 35)
            {
                var formDay = document.getElementById('formDay' + (firstWeekOfMonth + i));
                formDay.innerHTML = '<span style="text-decoration:underline;">' + formDay.innerHTML + '</span>';
            }
            else
            {
                var formDay = document.getElementById('formDay' + (firstWeekOfMonth + i - 7));
                formDay.innerHTML = '<span style="text-decoration:underline;">' + formDay.innerHTML + '</span>';
            }
        }
    }
}

// Show task list of a day.
// (window onload -> day of the moment; month change -> show first day of the month; select a day -> the day)
function selectDay(day, type)
{
    // type: 1 -> only one date, 3 -> two dates second request(23/30; 24/31)
    //       30 or 31 -> two dates first request
    if (type == 1)
        document.getElementById("toDoListDate").innerHTML = pageMonth + "/" + day + " ";
    else if (type == 30 || type == 31)
        document.getElementById("toDoListDate").innerHTML = pageMonth + "/" + day + "," + pageMonth + "/" + type + " ";

    // A day without task.
    if (thisMonthDateList[day - 1] == 0)
    {
        putDayList(day, null, 0);
        return ;
    }

    var selectDayRequest = new XMLHttpRequest();
    selectDayRequest.open("POST", "http://192.168.1.144:5000/calendar/one_date_list");
    selectDayRequest.setRequestHeader("Content-Type", "application/json");
    selectDayRequest.send(JSON.stringify({"year": pageYear, "month": pageMonth, "day": day}));
    selectDayRequest.onload = function()
    {
        console.log(selectDayRequest.responseText);
        rst = JSON.parse(selectDayRequest.responseText);
        switch (rst.rspCode)
        {
            case "20": case 20:
                if (type == 1)
                    putDayList(day, rst.taskList, 1);
                else if (type == 30 || type == 31)
                {
                    putDayList(day, rst.taskList, 2);
                    selectDay(type, 3)
                }
                else if (type == 3) 
                    putDayList(day, rst.taskList, 3);
                break;
            default:
                console.log("無法取得當日任務列表");
                break;
        }
    }
}

function putDayList(day, taskList, type)
{
    // type: 0 -> no task, 1 -> one date one list, 2 -> first list of two days two lists
    //       3 -> second list of two day two list.

    if (type == 0)
    {
        toDoList.innerHTML = '<div class="formLine"><textarea  class="formText formTextTitle" readonly>' + '這一天沒有任務' + '</textarea></div>';
    }
    else if (type == 1)
    {
        toDoList.innerHTML = "";
        for ( i = 0; i < taskList.length; i++)
        {
            var spsr;
            if (taskList[i].taskSRName != '-')
                spsr = '雇主：' + taskList[i].taskSRName + '\n';
            else if (taskList[i].taskSPName != '-')
                spsr = '雇員：' + taskList[i].taskSPName + '\n';
            else
                spsr = '尚無人承接\n';

            toDoList.innerHTML +=
                '<div class="formLine"><textarea  class="formText" readonly>' +
                taskList[i].taskStartTime + ' ~ ' + taskList[i].taskEndTime + '\n' + spsr +
                '地點：' + taskList[i].taskLocation + '\n' +
                '內容：' + taskList[i].taskContent +
                '</textarea></div>';
        }
    }
    else if (type == 2)
    {
        toDoList.innerHTML = '<div class="formLine"><textarea  class="formText formTextTitle" readonly>' + pageMonth + '/' + day + '</textarea></div>';
        for ( i = 0; i < taskList.length; i++)
            toDoList.innerHTML += '<div class="formLine"><textarea  class="formText" readonly>' + type + i + '</textarea></div>';
    }
    else if (type == 3)
    {
        toDoList.innerHTML = '<div class="formLine"><textarea  class="formText formTextTitle" readonly>' + pageMonth + '/' + day + '</textarea></div>';
        for ( i = 0; i < taskList.length; i++)
            toDoList.innerHTML += '<div class="formLine"><textarea  class="formText" readonly>' + type + i + '</textarea></div>';
    }
}