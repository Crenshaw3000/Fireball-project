

const visibilityBtn = document.getElementById("visibilityBtn");
visibilityBtn.addEventListener("click", toggleVisibility)

function toggleVisibility() {
  const passwordInput = document.getElementById("password")
  const icon = document.getElementById("icon")
  if (passwordInput.type === "password") {
    passwordInput.type = "text"
    passwordInput.type = "visibility_off"
    icon.innerText = "visibility_off"
  } else {
    passwordInput.type = "password"
    icon.innerText = "visibility"
  }
}
