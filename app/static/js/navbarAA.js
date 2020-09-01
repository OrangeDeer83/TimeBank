const urlPath = 'http://192.168.1.144:5000';
showNavbar();
function showNavbar()
{
    document.getElementById("navbar").innerHTML = '' +
    '<nav class="nav navbarBack">' +
        '<div class="navbarContainer">' +
            '<div class="navbarLeft">' +
                '<div class="dropdown">' +
                    '<div id="menuIconBack" onclick="clickToSpan(\'menuIconSpan\')"><div id="menuIcon"></div></div>' +
                    '<ul class="dropdownMenu dropdownMenuLeft unspanned" id="menuIconSpan">' +
                        '<li><a href="/Admin/approveSystem" class="dropdownMenuItem">核准系統</a></li>' +
                        '<li><a href="/Admin/updateCondition" class="dropdownMenuItem">更新申請條件</a></li>' +
                        '<li><a href="/Admin/setting" class="dropdownMenuItem">設定</a></li>' +
                    '</ul>' +
                '</div>' +
            '</div>' +
            '<div class="navbarCenter">' +
                '<div class="navbarBrand">' +
                    '<img class="navbarBrandImg" id="navbarBrandImg1" alt="AA" src="' + urlPath + '/static/img/AAWhite.png" />' +
                    '<img class="navbarBrandImg" id="navbarBrandImg2" alt="AA" src="' + urlPath + '/static/img/AAColor.png" />' +
                '</div>' +
            '</div>' +
            '<div class="navbarRight">' +
                '<a class="navbarUl" id="logout" href="/account/logout">登出</a>' +
            '</div>' +
        '</div>' +
    '</nav>';
}