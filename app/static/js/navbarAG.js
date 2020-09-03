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
                        '<li><a href="/Admin/GMApplication" class="dropdownMenuItem">人事管理-評論管理員</a></li>' +
                        '<li><a href="/Admin/setting" class="dropdownMenuItem">設定</a></li>' +
                    '</ul>' +
                '</div>' +
            '</div>' +
            '<div class="navbarCenter">' +
                '<div class="navbarBrand">' +
                    '<img class="navbarBrandImg" id="navbarBrandImg1" alt="AG" src="/static/img/AGWhite.png" />' +
                    '<img class="navbarBrandImg" id="navbarBrandImg2" alt="AG" src="/static/img/AGColor.png" />' +
                '</div>' +
            '</div>' +
            '<div class="navbarRight">' +
            '<a class="navbarUl" id="logout" href="/account/logout">登出</a>' +
            '</div>' +
        '</div>' +
    '</nav>';
}