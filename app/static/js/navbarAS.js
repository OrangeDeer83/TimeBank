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
                        '<li><a href="/Admin/givePoint" class="dropdownMenuItem">配發系統</a></li>' +
                        '<li><a href="/Admin/setting" class="dropdownMenuItem">設定</a></li>' +
                    '</ul>' +
                '</div>' +
            '</div>' +
            '<div class="navbarCenter">' +
                '<div class="navbarBrand">' +
                    '<img class="navbarBrandImg" id="navbarBrandImg1" alt="AS" src="/static/img/ASWhite.png" />' +
                    '<img class="navbarBrandImg" id="navbarBrandImg2" alt="AS" src="/static/img/ASColor.png" />' +
                '</div>' +
            '</div>' +
            '<div class="navbarRight">' +
            '<a class="navbarUl" id="logout" href="/account/logout">登出</a>' +
            '</div>' +
        '</div>' +
    '</nav>';
}