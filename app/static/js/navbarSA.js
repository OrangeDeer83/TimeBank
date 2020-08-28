showNavbar();
function showNavbar()
{
    document.getElementById("SAnavbar").innerHTML =
    '<nav class="nav navbarBack">' +
    '<div class="navbarContainer">' +
        '<div class="navbarLeft">' +
            '<div class="dropdown">' +
                '<div id="menuIconBack" onclick="clickToSpan(\'menuIconSpan\')"><div id="menuIcon"></div></div>' +
                '<ul class="dropdownMenu dropdownMenuLeft unspanned" id="menuIconSpan">' +
                    '<li><div class="dropdownMenuItem" onclick="clickToSpan(\'HRSpan\')">人事管理</div></li>' +
                    '<div class="unspanned" id="HRSpan">' +
                        '<div class="dropdownMenuItem HRSpanItem"><a href="hrmManager.html">系統管理員</a></div>' +
                        '<div class="dropdownMenuItem HRSpanItem"><a href="hrmGMApplicationSA.html">評論管理員</a></div>' +
                    '</div>' +
                    '<li><a href="/Admin/givePoint" class="dropdownMenuItem">配發系統</a></li>' +
                    '<li><a href="/Admin/approveSystem" class="dropdownMenuItem">核准系統</a></li>' +
                    '<li><a href="/Admin/updateCondition" class="dropdownMenuItem">更新申請條件</a></li>' +
                    '<li><a href="/Admin/updateWeb" class="dropdownMenuItem">更新入口網站</a></li>' +
                    '<li><a href="/Admin/setting" class="dropdownMenuItem">設定</a></li>' +
                '</ul>' +
            '</div>' +
        '</div>' +
        '<div class="navbarCenter">' +
            '<div class="navbarBrand">' +
                '<img class="navbarBrandImg" id="navbarBrandImg1" alt="SA" src="../static/img/SAWhite.png" />' +
                '<img class="navbarBrandImg" id="navbarBrandImg2" alt="SA" src="../static/img/SAColor.png" />' +
            '</div>' +
        '</div>' +
        '<div class="navbarRight">' +
            '<a class="navbarUl" id="logout" href="{{url_for(\'account.logout\')}}">登出</a>' +
        '</div>' +
    '</div>' +
    '</nav>';
}