// Find the check word: spanned or unspanned.
// If found, return true; if not found, return false.
function contains(classString, check)
{
    for (var i = 0; i < classString.length; i++)
    {
        console.log("Find " + check + " in " + classString);
        var wordNow = "";
        // Splite the string by " ".
        while(classString[i] != " " && i < classString.length)
        {
            wordNow = wordNow + classString[i];
            i++;
        }
        // Check word found.
        if (wordNow == check)
        {
            return true;
        }
    }
    return false;
}

// If unspanned and onclick, span the element of the name by "display: block".
// If spanned and onclick, hide the element of the name by "display: ''".
function clickToSpan(name)
{
    var element = document.getElementById(name); // Save the element of the name.
    var classVal = element.getAttribute("class"); // Save the class string of the element.
    if (contains(classVal, "spanned")) // Hide the element.
    {
        element.style.display = "";
        classVal = classVal.replace("spanned","unspanned");
        element.setAttribute("class", classVal);
        console.log("Spanned.");
    }
    else if (contains(classVal, "unspanned")) // Span the element.
    {
        element.style.display = "block";
        classVal = classVal.replace("unspanned","spanned");
        element.setAttribute("class", classVal);
        console.log("Hide.");
    }
}