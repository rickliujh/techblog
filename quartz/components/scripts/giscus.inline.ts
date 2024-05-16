let firstTime = true

function sendMessage<T>(message: T) {
  const iframe = document.querySelector<HTMLIFrameElement>('iframe.giscus-frame');
  if (!iframe) return;
  iframe.contentWindow.postMessage({ giscus: message }, 'https://giscus.app');
}

const onThemeToggle = ()=>{
  const toggleSwitch = document.querySelector("#darkmode-toggle") as HTMLInputElement
  changeTheme(toggleSwitch.checked)
}

function changeTerm(url) {
  sendMessage({ setConfig: { term: url } })
}

function changeTheme(dark) {
  sendMessage({ setConfig: { theme: dark? "noborder_dark":"noborder_light"} })
}

function loadComments() {
  const toggleSwitch = document.querySelector("#darkmode-toggle") as HTMLInputElement
  const script = document.createElement("script");

  script.type = "text/javascript"
  script.src = "https://giscus.app/client.js"
  script.async = true
  script.setAttribute("data-repo", "rickliujh/techblog")
  script.setAttribute("data-repo-id", "R_kgDOL6VQ_Q")
  script.setAttribute("data-category", "Announcements")
  script.setAttribute("data-category-id", "DIC_kwDOL6VQ_c4CfaND")
  script.setAttribute("data-mapping", "pathname")
  script.setAttribute("data-strict", "0")
  script.setAttribute("data-reactions-enabled", "1")
  script.setAttribute("data-emit-metadata", "0")
  script.setAttribute("data-input-position", "top")
  script.setAttribute("data-theme", toggleSwitch.checked? "noborder_dark":"noborder_light")
  script.setAttribute("data-lang", "en")
  script.setAttribute("crossorigin", "anonymous")
  script.setAttribute("data-loading", "lazy")

  document.body.appendChild(script);
  console.log("appended")
}


document.addEventListener("nav", ({detail}) => {
  if (firstTime) {
    const toggleSwitch = document.querySelector("#darkmode-toggle") as HTMLInputElement
    toggleSwitch.addEventListener("change", onThemeToggle)
    window.addCleanup(() => toggleSwitch.removeEventListener("change", onThemeToggle))

    if (detail.url !== "index") {
      loadComments()
    }
  }

  changeTerm(detail.url)
})

