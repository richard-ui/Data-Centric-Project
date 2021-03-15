let counter2 = 2;
let limit2 = 30;
const newStep = '<div id="stepholder*" class="input-field col s12"><i class="fas fa-list-ol prefix"></i><input id="prep_steps*" type="text" name="prep_steps" minlength="3" maxlength="300" class="validate" required><label for="prep_steps*" placeholder="Step">Step *</label><a class="waves-effect waves-light btn" onClick="deleteMethod(this)" data-method="stepholder*"><i class="fas fa-times"></i> Remove</a></div>'

function deleteMethod(el) {
    console.log(el.getAttribute("data-method"));
    document.getElementById(el.getAttribute("data-method")).remove();
}
function addStep(divName) {
    if (counter2 === limit2) {
        alert("You have reached the limit of adding " + counter2 + " steps");
    }
    else {
        console.log("Adding New Step")
        let newdiv = document.createElement('div');
        newdiv.innerHTML = newStep.replaceAll("*", counter2); // replace all asterisks with value e.g. 'ingredient 2'
        document.getElementById(divName).appendChild(newdiv);
        counter2++;
    }
};