'use strict'
// outlines a class that will keep track of which recipes it's grabbed, hold on to the recipes,
// and interface with Kayson's "addRecipesToPage" function, incrementing on the
// next 10 available recipes (if applicable)

let rec_start_idx = 0;
let rec_end_idx = 9;
let num_recs = 0;
let START = 0;
let END = 1;
let cur_recipes;
let cur_button;
let g_filterLength = 0;
let g_filters = {};
let remove_button = false;

function getNext10Recs(found_recipes, ingLength, filters) {
    // check if incrementing another 10 recipes will exceed the bounds of
    // the recipe list
    let indices = getNextIndices();
    // get starting and ending recipes as an array
    let start_idx = indices[START];
    let end_idx = indices[END];
    // call Kayson's function
    if (start_idx >= num_recs || end_idx >= num_recs)
    {
        remove_button = true;
    }
    addRecipesToPage(found_recipes, start_idx, end_idx, ingLength, filters);
    // show or hide button based on recipe status
    addRemoveButton()
};

function getNextIndices() {
    // Returns a two element array, the first element being
    // the starting index, and second being the ending index of the
    // next recipes to grab.
    // increment indices
    let next_start_idx = rec_start_idx + 10;
    let next_end_idx = rec_end_idx + 10;
    let next_indices = [0, 0];
    // check if last ending index was the last item in the
    // recipes list
    if (rec_end_idx == num_recs - 1)
    {
        // if yes, return the same index it started with
        next_indices[START] = rec_end_idx;
        next_indices[END] = rec_end_idx;
    }
    // else if the ending index is greater than rec_nums, return the position of
        //rec_nums-1 as the ending index, and rec_start_idx as the staring index
    else if (rec_end_idx >= num_recs)
    {
        next_end_idx = num_recs -1;
        next_indices[START] = rec_start_idx ;
        next_indices[END] = next_end_idx;
    }
    // else, return next_end_idx as ending index, and next_start_idx as starting index
    else
    {
        next_indices[START] = next_start_idx;
        next_indices[END] = next_end_idx;
    }
    // store used indices in the rec_start_idx and rec_end_idx values
    rec_start_idx = next_indices[START];
    rec_end_idx = next_indices[END];
    return next_indices;
};

function addRemoveButton() {
    // if number of recipes is less than 10, or the last recipe displayed was the
    // last recipe in the list, don't display the button

    if (num_recs < 10 || remove_button == true)//rec_end_idx == num_recs - 1)
    {
        cur_button.style = "display: none";
    }
     // otherwise display it
    else
    {
        cur_button.style = "";
    }
};

function deleteNext10Button() {
    // looks for a next_10_button on the document, and deletes it
    let next_10_div = document.getElementById('next_10_button_div')
    while (next_10_div.firstChild)
    {
        next_10_div.removeChild(next_10_div.firstChild)
    }
    // reset index values
    rec_start_idx = 0;
    rec_end_idx = 9;
    num_recs = 0;
};

// TODO: Write function to kill the button upon new search

function runNext10(recipes, filterLength, filters){

    num_recs = recipes.length;
    cur_recipes = recipes;
    g_filterLength = filterLength;
    g_filters = filters;

    // create button to add, if needed
    let button_div = document.getElementById('next_10_button_div');
    let next_button = document.createElement('button');
    next_button.classList = 'btn btn-dark';
    next_button.type = 'button';
    next_button.id = 'next_10_button';
    next_button.textContent = "See More...";
    //button.style = 'display: none';
    next_button.setAttribute('onclick', 'getNext10Recs(cur_recipes, g_filterLength, g_filters);');
    button_div.appendChild(next_button);
    cur_button = next_button;
    // console.log(next_button);
    // add button to next_10_button_div

    // determine if button is shown or not.
    addRemoveButton();
}
