const userNameLabel = document.getElementById("userName")
const pswLabel = document.getElementById("psw")
const btnLabel = document.getElementById("btn")
const warn = document.getElementById("warn")

const login = async (name, psw) => {
  let user = {
    userName: name,
    password: psw
  }

  let data = new FormData()
  data.append("json", JSON.stringify(user))

  const response = await fetch('/api/login', {
    body: JSON.stringify({ "userName": name, "password": psw }),
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  return [response.status, response.json()]
}

btnLabel.addEventListener("click", async () => {
  let userName = userNameLabel.value
  let psw = pswLabel.value
  login(userName, psw).then(async ret => {
    status = ret[0]
    data = ret[1]
    if (status != 200) {
      warn.style.display = ""
      warn.style.color = "#ff0000"
      warn.innerHTML = (await data).detail
    } else {
      console.log(userName)
      console.log((await data).token)
      document.cookie = `userName=${userName}`
      document.cookie = `token=${(await data).token}`
      window.location.href = "/"
    }
  })

});
