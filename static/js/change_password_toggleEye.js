
const visibilityBtn = document.getElementById("visibilityBtn");
visibilityBtn.addEventListener("click", toggleVisibility)

function toggleVisibility() {
  const passwordInput = document.getElementById("new_password")
  const icon = document.getElementById("icon")
  if (passwordInput.type === "password") {
    passwordInput.type = "text"
    icon.innerText = "visibility_off"
  } else {
    passwordInput.type = "password"
    icon.innerText = "visibility"
  }
}



const visibilityBtn2 = document.getElementById("visibilityBtn2");
visibilityBtn2.addEventListener("click", toggleVisibility2)

function toggleVisibility2() {
  const passwordInput2 = document.getElementById("confirm_password")
  const icon2 = document.getElementById("icon2")
  if (passwordInput2.type === "password") {
    passwordInput2.type = "text"
    icon2.innerText = "visibility_off"
  } else {
    passwordInput2.type = "password"
    icon2.innerText = "visibility"
  }
}
