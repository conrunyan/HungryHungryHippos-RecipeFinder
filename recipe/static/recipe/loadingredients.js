'use strict'

function addRecipesToPage(recipes, start_idx, end_idx){
    //get existing div
    let recipes_div = document.getElementById('found_recipes');

    //add header
    let header = document.createElement('h1');
    header.textContent = "Recipes";
    recipes_div.appendChild(header);

    // fix end index if it is greater than array size
    if(end_idx > recipes.length){
        end_idx = recipes.length;
    }

    //create HTML layout for each recipe (reflects myRecipes.html)
    for(let i = start_idx; i < end_idx; i++){
        let recipe = recipes[i];
        
        //add hr tag to recipe
        recipes_div.appendChild(document.createElement('hr'));

        //add a tag to recipe
        let a = document.createElement('a');
        a.setAttribute('class', 'recipe-summary');
        a.setAttribute('href', URL_FULL_VIEW + recipe.id + "/");
        recipes_div.appendChild(a);

        //add img tag to a
        let img = document.createElement('img');
        img.setAttribute('src', recipe.image_url);
        a.appendChild(img);

        //add div tag to a
        let div = document.createElement('div');
        a.appendChild(div)

        //add h3 tag to div
        let h3 = document.createElement('h3');
        h3.textContent = recipe.title;
        div.appendChild(h3);

        //add p tag to div
        let p = document.createElement('p');
        p.textContent = recipe.summary;
        div.appendChild(p);
    }
}

function deleteRecipesFromPage(){
    let recipes_div = document.getElementById('found_recipes');
    while(recipes_div.firstChild){
        recipes_div.removeChild(recipes_div.firstChild);
    }
}