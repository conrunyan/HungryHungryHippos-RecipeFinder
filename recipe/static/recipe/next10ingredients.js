'use strict'
// outlines a class that will keep track of which recipes it's grabbed, hold on to the recipes, 
// and interface with Kayson's "addRecipesToPage" function, incrementing on the
// next 10 available recipes (if applicable).

func = function Next10(recipes) {
    // public
    this.getNext10Recs=function() {
        
        // check if incrementing another 10 recipes will exceed the bounds of
        // the recipe list
        
        
    };
    this.getNumRecs=function() {
        return num_recs;
    }
    // private attributes
    var rec_start_idx = 0;
    var rec_end_idx = 9;
    var num_recs = recipes.results.length;
    // private methods

    this.getNextIndices=function() {
        // Returns a two element array, the first element being
        // the starting index, and second being the ending index of the
        // next recipes to grab.

        // increment indices
        var next_start_idx = rec_start_idx + 10;
        var next_end_idx = rec_end_idx + 10;
        var next_indices = [0, 0];
        var START = 0;
        var END = 1;
        // check if last starting index was the last item in the 
        // recipes list
        if (rec_start_idx == num_recs - 1)
        {
            // if yes, return the same index it started with
            next_indices[START] = rec_start_idx;
            next_indices[END] = rec_start_idx;
        }
        // else if the ending index is greater than rec_nums, return the position of 
            //rec_nums-1 as the ending index, and rec_start_idx as the staring index
        // TODO: add else if with above logic here
        else if (rec_end_idx > num_recs)
        {
            next_end_idx = num_recs -1;
            next_indices[START] = next_start_idx;
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
        // TODO: store used 
        rec_start_idx += 10;
        rec_end_idx += 10;
        rec_start_idx = next_indices[START];
        rec_end_idx = next_indices[END];

        return next_indices;
    }
}

