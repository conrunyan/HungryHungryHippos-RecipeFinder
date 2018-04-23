'use strict'

function addRecipesToPage(recipes, start_idx, end_idx, listIngLength, filters){
    //get existing div
    let recipes_div = document.getElementById('found_recipes');

    // fix end index if it is greater than array size
    if(end_idx >= recipes.length){
        end_idx = recipes.length ;
    }

    if(recipes.length === 0 && listIngLength !== 0) {
      let recipes_div = document.getElementById('found_recipes');
      let note = document.createElement('p');
      note.textContent = "No recipes could be found that matched the ingredients you searched";
      recipes_div.appendChild(note);
      return;
    }

    //create HTML layout for each recipe (reflects myRecipes.html)
    for(let i = start_idx; i < end_idx; i++){
        let recipe = recipes[i];

        // Perform additional filtering on time, appliance, difficulty, etc.
        // Skip adding recipe if it doesn't conform to filters
        if(filters !== null && shouldSkipRecipe(recipe, filters)) {
          if(end_idx < recipes.length - 1) {
            end_idx++;
          }
          continue;
        }

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
        img.setAttribute('alt', "recipe image");
        a.appendChild(img);

        //add div tag to a
        let div = document.createElement('div');
        a.appendChild(div)

        //add h3 tag to div
        let h3 = document.createElement('h3');
        h3.textContent = recipe.title + " - (" + recipe.percentage + "% match)";
        div.appendChild(h3);

        //add p tag to div
        let p = document.createElement('p');
        p.textContent = recipe.summary;
        div.appendChild(p);
    }
}

function deleteRecipesFromPage(listLength){
    let recipes_div = document.getElementById('found_recipes');
    while(recipes_div.firstChild){
        recipes_div.removeChild(recipes_div.firstChild);
    }
    //add header
    if(listLength !== 0) {
      let header = document.createElement('h1');
      header.setAttribute('id', 'recipe-header');
      header.textContent = "Recipes";
      recipes_div.appendChild(header);
    }
}

function shouldSkipRecipe(recipe, filters) {
  let shouldSkipAppliance = false;
  if(filters['appliances'].length !== 0 && recipe['appliances'] !== null) {
    shouldSkipAppliance = true;
    for(let appliance of filters['appliances']) {
      for(let recipeAppliance of recipe['appliances']) {
        if(recipeAppliance.name.toUpperCase() === appliance.toUpperCase()) {
          shouldSkipAppliance = false;
        }
      }
    }
  }

  let shouldSkipDifficulty = false;
  if(filters['difficulty'].length !== 0 && recipe['difficulty'] !== null) {
    shouldSkipDifficulty = true;
    if(filters['difficulty'].includes(recipe['difficulty'])) {
      shouldSkipDifficulty = false;
    }
  }

  let shouldSkipTime = false;
  if(filters['time'].length !== 0 && recipe['time'] !== null) {
    shouldSkipTime = true;
    let maxTime = Math.max(filters['time']);
    if(recipe.time <= maxTime) {
      shouldSkipTime = false;
    }
  }

  return shouldSkipAppliance || shouldSkipDifficulty || shouldSkipTime;
}
