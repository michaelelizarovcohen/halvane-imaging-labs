/* Halvane Imaging Labs — navigation toggle and gallery filtering. No tracking, no network requests. */
(function () {
  var btn = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var dataEl = document.getElementById("gallery-data");
  if (!dataEl) return;
  var data = JSON.parse(dataEl.textContent);
  var RAW = ["cr2", "cr3", "crw", "nef", "arw", "raf", "rw2", "orf", "pef", "dng", "x3f", "erf", "dcr", "mrw", "gpr"];
  var byId = {};
  data.forEach(function (d) { byId[d.id] = d; });
  var q = document.getElementById("q"), sec = document.getElementById("sec"), fmt = document.getElementById("fmt");
  var count = document.getElementById("count");
  var items = Array.prototype.slice.call(document.querySelectorAll(".g-item"));

  function apply() {
    var term = (q.value || "").trim().toLowerCase(), s = sec.value, f = fmt.value, shown = 0;
    items.forEach(function (el) {
      var d = byId[el.getAttribute("data-id")];
      var hay = (d.id + " " + d.t + " " + d.c + " " + d.s + " " + d.f).toLowerCase();
      var ok = (!term || hay.indexOf(term) !== -1) && (!s || d.s === s) &&
               (!f || (f === "__raw" ? RAW.indexOf(d.x) !== -1 : d.x === f));
      el.hidden = !ok;
      if (ok) shown++;
    });
    count.textContent = shown + " of " + items.length + " files";
    try {
      var params = new URLSearchParams();
      if (term) params.set("q", term);
      if (s) params.set("section", s);
      if (f) params.set("format", f);
      history.replaceState(null, "", params.toString() ? "?" + params.toString() : location.pathname);
    } catch (e) { /* ignore */ }
  }
  try {
    var p = new URLSearchParams(location.search);
    if (p.get("q")) q.value = p.get("q");
    if (p.get("section")) sec.value = p.get("section");
    if (p.get("format")) fmt.value = p.get("format");
  } catch (e) { /* ignore */ }
  [q, sec, fmt].forEach(function (el) { el.addEventListener("input", apply); el.addEventListener("change", apply); });
  apply();
})();
