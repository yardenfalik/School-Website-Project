function getTheme(cookieName) 
{
    var index = document.cookie.indexOf('theme') + 6;
    if (document.cookie.charAt(index) == 'd')
    {
        return "dark";
    }
    return "light";

}



window.addEventListener('load', event => {
    if(getTheme('theme') == "dark")
    {   
        darkMode();
    }   
  });

console.log("%c!!!עצור", "color:red; font-size:600%");
console.log("%c", "font-size:150%");

document.getElementById("english").style.visibility = "hidden";

document.getElementById("box").style.display = "none";

function darkMode() 
{
    var element = document.body;
    element.classList.toggle("dark-mode");
}


function changeLen()
{
    if(document.getElementById("hebrew").style.visibility == "visible")
    {
        document.getElementById("hebrew").style.visibility = "hidden";
        document.getElementById("english").style.visibility = "visible";
        document.cookie = "language=english";
    }
    else
    {
        document.getElementById("english").style.visibility = "hidden";
        document.getElementById("hebrew").style.visibility = "visible";
        document.cookie = "language=hebrew";
    }
}

function darkModeBtn() 
{
    var element = document.body;
    element.classList.toggle("dark-mode");

    if(getTheme('theme') == "dark")
    {
        console.log("enterd");
        document.cookie = "theme=light";
    }
    else
    {
        document.cookie = "theme=dark";
    }
}
       
function showFunction()
{
  if(document.getElementById("box").style.display === "none")
  {
    document.getElementById("box").style.display = "block";
  }
  else
  {
    document.getElementById("box").style.display = "none";
  }
}

function formCheck()
{
    let email = document.getElementById("email");
    let pass = document.getElementById("password");
    let subButton = document.getElementById("submit");

    if(pass.value.length == 0)
    {
        pass.style.borderColor = "red";
        pass.style.backgroundColor = "#FFF2F4";
    }
    else
    {
        pass.style.borderColor = "#ccc";
        pass.style.backgroundColor = "#ffffff";
    }
    if(email.value.length == 0)
    {
        email.style.borderColor = "red";
        email.style.backgroundColor = "#FFF2F4";
    }
    else
    {
        email.style.borderColor = "#ccc";
        email.style.backgroundColor = "#ffffff";
    }

    if(pass.value.length != 0 && email.value.length != 0)
    {
        subButton.disabled = false;
    }
    else
    {
        subButton.disabled = true;
    }
}