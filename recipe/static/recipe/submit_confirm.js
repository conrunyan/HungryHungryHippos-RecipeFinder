'use strict'
// Prompts to user if they want to submit their recipe for public approval
// If yes, the submission goes through, otherwise nothing happens

function submitPublic(url)
{
    // check if user wants to proceed
    if (confirm('Do you really want to submit this recipe to be public?'))
    {
        // generate new url
        let curUrl = location.href;
        let urlParts = [url];
        let newUrl = curUrl.replace(/\/recipe_full_view.*/, urlParts);
        // navigate to submit url
        // This is kind of a hacky way to do this... but it's the only way I could figure out
        // how to get the confirm dialogue to pop up, take you to the submit location, AND actually
        // change the is_private flag...
        window.location.href = newUrl;
        // actually submit GET (This is the method I tried before. Doesn't work exactly how I want)
        //let submitRequest = new XMLHttpRequest();
        //submitRequest.open('GET', newUrl);
        //submitRequest.send();
        return true;
    }
    else
    {
        return false;
    }
}