const urlPath = 'http://192.168.1.144:5000';
showNavbar();
function showNavbar()
{
    document.getElementById("GMnavbar").innerHTML =
    '<nav class="nav navbarBack">' +
        '<div class="navbarContainer">' +
            '<div class="navbarLeft">' +
                '<div class="dropdown">' +
                    '<div id="menuIconBack" onclick="clickToSpan(\'menuIconSpan\')"><div id="menuIcon"></div></div>' +
                    '<ul class="dropdownMenu dropdownMenuLeft unspanned" id="menuIconSpan">' +
                        '<li><a href="/GM/reportApprove" class="dropdownMenuItem">檢舉審核</a></li>' +
                        '<li><a href="/GM/updateGrade" class="dropdownMenuItem">評論審核</a></li>' +
                        '<li><a href="/GM/setting" class="dropdownMenuItem">設定</a></li>' +
                    '</ul>' +
                '</div>' +
            '</div>' +
            '<div class="navbarCenter">' +
                '<div class="navbarBrand">' +
                    '<img class="navbarBrandImg" id="navbarBrandImg1" alt="GM" src="' + urlPath + '/static/img/GMWhite.png" />' +
                    '<img class="navbarBrandImg" id="navbarBrandImg2" alt="GM" src="' + urlPath + '/static/img/GMColor.png" />' +
                '</div>' +
            '</div>' +
            '<div class="navbarRight">' +
                '<a class="navbarUl" id="logout" href="/account/logout">登出</a>' +
            '</div>' +
        '</div>' +
    '</nav>';
}