const passwordForm = document.getElementById("password-form");

passwordForm.addEventListener("submit", () => {
    event.preventDefault();
    const userPassword = document.getElementById("password").value;

    const score = checkPasswordStrength(userPassword);

    passwordForm.reset();
});

function checkPasswordStrength(password) {
    const length = password.length;
    let hasUpperCase = false;
    let hasNumber = false;
    let hasSpecialCharacter = false;
    let hasLowerCase = false;
    let score = 0;

    if (length >= 8) {
        score++;
    }

    for (let i = 0; i < length; i++) {
        if (isUpperCase(password[i]) && hasUpperCase === false) {
            hasUpperCase = true;
        } else if (isLowerCase(password[i]) && hasLowerCase === false) {
            hasLowerCase = true;
        } else if (isNumber(password[i]) && hasNumber === false) {
            hasNumber = true;
        } else if (isSpecialCharacter(password[i]) && hasSpecialCharacter === false) {
            hasSpecialCharacter = true;
        }
    }

    if (hasUpperCase) {
        score++;
    }
    if (hasLowerCase) {
        score++;
    }
    if (hasNumber) {
        score++;
    }
    if (hasSpecialCharacter) {
        score++;
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