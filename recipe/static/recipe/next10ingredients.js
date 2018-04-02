'use strict'
// outlines a class that will keep track of which recipes it's grabbed, hold on to the recipes, 
// and interface with Kayson's "addRecipesToPage" function, incrementing on the
// next 10 available recipes (if applicable)

function Next10(recipes) {
    // Constructor stuff

    // add button if recipes count is greater than 10, and remove it if 
    // the last recipe in the list was displayed

    // public
    this.getNext10Recs=function() {
        // check if incrementing another 10 recipes will exceed the bounds of
        // the recipe list
        var START = 0;
        var END = 1;
        var indices = getNextIndices();
        // get starting and ending recipes
        var start_idx = indices[START];
        var end_idx = indices[END];
        addRecipesToPage(found_recipes);
    };
    this.getNumRecs=function() {
        return num_recs;
    };
    this.getLastIdx=function() {
        return rec_end_idx;
    };
    this.getStartIdx=function() {
        return rec_start_idx;
    };
    // private attributes
    var found_recipes = recipes;
    var rec_start_idx = 0;
    var rec_end_idx = 9;
    var num_recs = recipes.length;
    // private methods
    var getNextIndices=function() {
        // Returns a two element array, the first element being
        // the starting index, and second being the ending index of the
        // next recipes to grab.

        // increment indices
        var next_start_idx = rec_start_idx + 10;
        var next_end_idx = rec_end_idx + 10;
        var next_indices = [0, 0];
        var START = 0;
        var END = 1;
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
        // TODO: add else if with above logic here
        else if (rec_end_idx > num_recs)
        {
            next_end_idx = num_recs -1;
            next_indices[START] = rec_start_idx ;
            next_indices[END] = next_end_idx;
        }
        // else, return next_end_idx as ending index, and next_start_idx as starting index
        // TDOO: add else to capture above logic
        else
        {
            next_indices[START] = next_start_idx;
            next_indices[END] = next_end_idx;
        }

        // store used indices in the rec_start_idx and rec_end_idx values 
        rec_start_idx = next_indices[START];
        rec_end_idx = next_indices[END];

        // show or hide button based on recipe status
        addRemoveButton(num_recs, rec_end_idx);

        return next_indices;
    };
}

function addRemoveButton(num_recs, rec_end_idx) {
        // if number of recipes is less than 10, or the last recipe displayed was the 
        // last recipe in the list, don't display the button
        var button = document.getElementById('next_10_button');
        
        //if (num_recs < 0 || rec_end_idx == num_recs - 1)
        //{
        //    button.style = "display: none";
        //}
        // otherwise, display it
        //else
        //{
            button.style = "";
        //}
    };

function runNext10(recipes){
    var next10 = new Next10(recipes);

    // create button to add, if needed
    var button_div = document.getElementById('next_10_button_div');
    alert(button_div.className);
    var button = document.createElement('button');
    button.classList = 'btn btn-dark';
    button.type = 'button';
    button.id = 'next_10_button';
    button.textContent = "Next 10";
    //button.style = 'display: none';
    button.addEventListener('click', next10.getNext10Recs());
    button_div.appendChild(button);

    alert(button_div.children);
    // determine if button is shown or not. 
    //addRemoveButton(next10.getNumRecs, next10.getLastIdx);
}
