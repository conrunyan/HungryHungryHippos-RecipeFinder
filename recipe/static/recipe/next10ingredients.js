'use strict'
// outlines a class that will keep track of which recipes it's grabbed, hold on to the recipes, 
// and interface with Kayson's "addRecipesToPage" function, incrementing on the
// next 10 available recipes (if applicable).

function Next10(recipes) {
    // public
    this.getNext10Recs=function() {
        alert('hello');
    };
    this.getNumRecs=function() {
        return num_recs;
    }
    // private
    var rec_start_idx = 0;
    var num_recs = recipes.results.length;
}

