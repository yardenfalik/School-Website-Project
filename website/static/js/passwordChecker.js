function passwordChecker()
{
    let listTitle = document.getElementById("listTitle");
    let submitButt = document.getElementById("submit");


    const specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
    let pass = document.getElementById("password1");
    let howLong = document.getElementById("howLong");
    let hasNumbers = document.getElementById("hasNumbers");
    let lowerUpper = document.getElementById("lowerUpper");
    const lowerCase = /[a-z]/;
    const upperCase = /[A-Z]/;


    if (pass.value.length >= 8)
    {
        howLong.style.color = "#00D959";
    }
    else
    {
        howLong.style.color = "#ccc";
    }

    if (/\d/.test(pass.value) && specialChars.test(pass.value))
    {
        hasNumbers.style.color = "#00D959";
    }
    else
    {
        hasNumbers.style.color = "#ccc";
    }

    if (lowerCase.test(pass.value) && upperCase.test(pass.value))
    {
        lowerUpper.style.color = "#00D959";
    }
    else
    {
        lowerUpper.style.color = "#ccc";
    }

    if(lowerCase.test(pass.value) && upperCase.test(pass.value) && /\d/.test(pass.value) && specialChars.test(pass.value) && pass.value.length >= 8)
    {
        listTitle.style.color = "#00D959";
        submitButt.disabled = false; 
    }
    else
    {
        listTitle.style.color = "#ccc";
        submitButt.disabled = true; 
    }
}