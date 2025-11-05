const passwordForm = document.getElementById("password-form");

passwordForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const userPassword = document.getElementById("password").value.trim();
    const strengthBar = document.getElementById("strength-bar");
    const strengthText = document.getElementById("strength-text");
    const resultText = document.getElementById('result-text');
    const passwordScore = checkPasswordStrength(userPassword);
    strengthBar.value = passwordScore;
    strengthText.textContent = `${passwordScore}%`;

    resultText.textContent = `Your password is ${passwordScore}% strong.`;
});

function checkPasswordStrength(password) {

    if (!password) {
        return 0;
    }
    const length = password.length;
    let hasUpperCase = false;
    let hasNumber = false;
    let hasSpecialCharacter = false;
    let hasLowerCase = false;
    let score = 0;

    if (length >= 8) {
        score+=25;
    }
    if (length >= 12) {
        score+=15;
    }

    for (let i = 0; i < length; i++) {
        if (hasUpperCase === false && isUpperCase(password[i])) {
            hasUpperCase = true;
        } else if (hasLowerCase === false && isLowerCase(password[i])) {
            hasLowerCase = true;
        } else if (hasNumber === false && isNumber(password[i])) {
            hasNumber = true;
        } else if (hasSpecialCharacter === false && isSpecialCharacter(password[i])) {
            hasSpecialCharacter = true;
        }
    }

    if (hasUpperCase) {
        score+=15;
    }
    if (hasLowerCase) {
        score+=15;
    }
    if (hasNumber) {
        score+=15;
    }
    if (hasSpecialCharacter) {
        score+=15;
    }

    return score;

}

function isUpperCase(char) {
    return char === char.toUpperCase() && char !== char.toLowerCase();
}

function isLowerCase(char) {
    return char === char.toLowerCase() && char !== char.toUpperCase();
}

function isNumber(char) {
    return /\d/.test(char);
}

function isSpecialCharacter(char) {
    const specialCharsRegex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~`]/;

    return specialCharsRegex.test(char);
}