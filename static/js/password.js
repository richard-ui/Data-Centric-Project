const strengthMeter = document.getElementById('strength-meter')
const passwordInput = document.getElementById('password')
const reasonsContainer = document.getElementById('reasons')

passwordInput.addEventListener('input', updateStrengthMeter)

updateStrengthMeter() // call function on ,oad

function updateStrengthMeter() {
  const weaknesses = calculatePasswordStrength(passwordInput.value)

  let strength = 100
  reasonsContainer.innerHTML = '' // output empty first
  weaknesses.forEach(weakness => {
    if (weakness == null) return
    strength -= weakness.deduction
    const messageElement = document.createElement('div')
    messageElement.innerText = weakness.message
    reasonsContainer.appendChild(messageElement)
  })
  strengthMeter.style.setProperty('--strength', strength)
}

function calculatePasswordStrength(password) {
  const weaknesses = []
  weaknesses.push(lengthWeakness(password))
  weaknesses.push(uppercaseWeakness(password))
  weaknesses.push(specialCharactersWeakness(password))

  return weaknesses
}

// function to test for password length

function lengthWeakness(password) {
  const length = password.length

  if (length <= 5) {
    return {
      message: 'Your password is too short!',
      deduction: 40
    }
  }
}

// for uppercase characters

function uppercaseWeakness(password) {
  return characterTypeWeakness(password, /[A-Z]/g, 'Uppercase Character')

}

// for special characters

function specialCharactersWeakness(password) {
  return characterTypeWeakness(password, /[^0-9a-zA-Z\s]/g, 'Special Character')
}

// function determines character type used.

function characterTypeWeakness(password, regex, type) {
  const matches = password.match(regex) || []

  if (matches.length === 0) {
    return {
      message: `Your password needs at least 1 ${type}!`,
      deduction: 20
    }
  }
}