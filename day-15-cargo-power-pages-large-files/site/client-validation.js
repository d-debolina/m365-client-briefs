// CARGO: friendly client-side checks before upload (server-side limits still apply!)
// Paste into the page's custom JavaScript (Power Pages design studio → Edit code) and adjust the selector.
(function () {
  const MAX_MB = 2048;                                   // keep in sync with the form setting
  const ALLOWED = [".pdf", ".jpg", ".jpeg", ".png", ".zip", ".mp4"];
  document.addEventListener("change", function (e) {
    const input = e.target;
    if (!(input instanceof HTMLInputElement) || input.type !== "file") return;
    for (const f of input.files) {
      const ext = f.name.slice(f.name.lastIndexOf(".")).toLowerCase();
      let msg = "";
      if (!ALLOWED.includes(ext)) msg = `“${f.name}”: file type ${ext} isn't allowed.`;
      else if (f.size > MAX_MB * 1024 * 1024) msg = `“${f.name}” is ${(f.size/1048576).toFixed(0)} MB. The limit is ${MAX_MB} MB.`;
      if (msg) { alert(msg); input.value = ""; return; }
    }
  });
})();
