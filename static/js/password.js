/*jshint esversion: 6 */
const strengthMeter = document.getElementById('strength-meter');
const passwordInput = document.getElementById('password');
const reasonsContainer = document.getElementById('reasons');

// if password input true
if(passwordInput){
passwordInput.addEventListener('input', updateStrengthMeter);
}

// call function on load

function updateStrengthMeter() {
  const weaknesses = calculatePasswordStrength(passwordInput.value);

  let strength = 100;
  reasonsContainer.innerHTML = ''; // output empty first
  weaknesses.forEach(weakness => {
    if (weakness == null) return;
    strength -= weakness.deduction;
    const messageElement = document.createElement('div'); // create new element and display current error message
    messageElement.innerText = weakness.message;
    reasonsContainer.appendChild(messageElement);
  });
  strengthMeter.style.setProperty('--strength', strength); // set strenghh meter
}

function calculatePasswordStrength(password) {
  // create array and push functions to this array
  const weaknesses = [];
  
  weaknesses.push(lengthWeakness(password));
  weaknesses.push(lowercaseWeakness(password));
  weaknesses.push(uppercaseWeakness(password));
  weaknesses.push(numberWeakness(password));
  weaknesses.push(specialCharactersWeakness(password));

  return weaknesses;
}

// functions for validation checking

function lengthWeakness(password) {
  const length = password.length;

  if (length <= 5) {
    return {
      message: 'Your password is too short',
      deduction: 65
    };
  }

}

function uppercaseWeakness(password) {
  return characterTypeWeakness(password, /[A-Z]/g, 'uppercase characters');

}

function lowercaseWeakness(password) {
  return characterTypeWeakness(password, /[a-z]/g, 'lowercase characters');
}

function numberWeakness(password) {
  return characterTypeWeakness(password, /[0-9]/g, 'numbers');
}

function specialCharactersWeakness(password) {
  return characterTypeWeakness(password, /[^0-9a-zA-Z\s]/g, 'special characters');
}

function characterTypeWeakness(password, regex, type) {
  const matches = password.match(regex) || [];

  if (matches.length === 0) {
    return {
      message: `Your password has no ${type}`,
      deduction: 25
    };
  }
}


