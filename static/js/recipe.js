let counter = 2;
let limit = 30;
const newIngredient = '<div id="ingredientholder*" class="input-field col s12"><i class="fas fa-pizza-slice prefix"></i><input id="ingredients*" type="text" name="ingredients" minlength="3" maxlength="60" class="validate" required><label for="ingredients*" placeholder="Ingredient">Ingredient *</label><a class="waves-effect waves-light btn" onClick="deleteIngredient(this)" data-ingredient="ingredientholder*"><i class="fas fa-times"></i> Remove</a></div>'

function deleteIngredient(el) {
    console.log(el.getAttribute("data-ingredient"));
    document.getElementById(el.getAttribute("data-ingredient")).remove();
}
function addIngredient(divName) {
    if (counter === limit) {
        alert("You have reached the limit of adding " + counter + " ingredients");
    }
    else {
        console.log("Adding Ingredient")
        let newdiv = document.createElement('div');
        newdiv.innerHTML = newIngredient.replaceAll("*", counter);
        document.getElementById(divName).appendChild(newdiv);
        counter++;
    }
};