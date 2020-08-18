function includeHTML()
{
    var elementList; // Save all elements of document.
    var i; // Counter of for loop.
    var element; // Current element.
    var fileName, xhttp;
    /* Loop through a collection of all HTML elements. */
    elementList = document.getElementsByTagName("*");
    for (i = 0; i < elementList.length; i++)
    {
        element = elementList[i];
        /* Search for elements with a certain atrribute. */
        fileName = element.getAttribute("includeHTML");
        if (fileName)
        {
            /* Make an HTTP request using the attribute value as the fileName name. */
            xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function()
            {
                if (this.readyState == 4)
                {
                    if (this.status == 200) {element.innerHTML = this.responseText;}
                    if (this.status == 404) {element.innerHTML = "Page not found.";}
                    /* Remove the attribute, and call this function again. */
                    element.removeAttribute("includeHTML");
                    includeHTML();
                }
            }      
            xhttp.open("GET", fileName, true);
            xhttp.send();
            return;
        }
    }
}

//HTML: <script src="js/includeHTML.js">includeHTML();</script>