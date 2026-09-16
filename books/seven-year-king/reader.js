(function () {
  var body = document.body;
  var toggle = document.getElementById("nav-toggle");
  var closeBtn = document.getElementById("nav-close");
  var backdrop = document.getElementById("nav-backdrop");
  var side = document.getElementById("chapter-side");
  if (!toggle || !side) return;

  function isMobileNav() {
    return window.matchMedia("(max-width: 900px)").matches;
  }

  function openNav() {
    body.classList.add("nav-open");
    toggle.setAttribute("aria-expanded", "true");
    if (backdrop) backdrop.hidden = false;
  }

  function closeNav() {
    body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
    if (backdrop) backdrop.hidden = true;
  }

  toggle.addEventListener("click", function (e) {
    e.preventDefault();
    e.stopPropagation();
    if (body.classList.contains("nav-open")) closeNav();
    else openNav();
  });
  if (closeBtn) {
    closeBtn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      closeNav();
    });
  }
  if (backdrop) {
    backdrop.addEventListener("click", function (e) {
      e.preventDefault();
      closeNav();
    });
  }
  side.querySelectorAll("a.nav-item").forEach(function (a) {
    a.addEventListener("click", function () {
      if (isMobileNav()) setTimeout(closeNav, 10);
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeNav();
  });
  window.addEventListener("resize", function () {
    if (!isMobileNav()) closeNav();
  });
})();

(function () {
  var body = document.body;
  var buttons = document.querySelectorAll(".mode button[data-mode]");
  if (!buttons.length) return;

  function setMode(mode) {
    if (mode !== "desk" && mode !== "prose" && mode !== "both") mode = "both";
    body.setAttribute("data-mode", mode);
    try {
      localStorage.setItem("syk-mode", mode);
    } catch (e) {}
    buttons.forEach(function (b) {
      b.classList.toggle("on", b.getAttribute("data-mode") === mode);
    });
  }

  var saved = null;
  try {
    saved = localStorage.getItem("syk-mode");
  } catch (e) {}
  setMode(saved || "both");

  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      setMode(b.getAttribute("data-mode"));
    });
  });
})();
