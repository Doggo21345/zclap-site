// Menu, the estimator starter, the forms, and Microsoft Clarity. No framework.
(function () {
  // Microsoft Clarity session recordings and heatmaps: paste the project ID from
  // clarity.microsoft.com (Settings > Overview) between the quotes. Empty = off.
  var CLARITY_ID = "";
  if (CLARITY_ID) {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", CLARITY_ID);
  }

  var menu = document.getElementById("menu");
  var btn = document.querySelector(".menu");
  if (btn && menu) {
    btn.addEventListener("click", function () {
      menu.classList.toggle("open");
      btn.setAttribute("aria-expanded", menu.classList.contains("open"));
    });
    menu.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { menu.classList.remove("open"); }); });
  }

  // The phone's sticky button hides while the estimator card or the form is on screen.
  var bar = document.querySelector(".mbar");
  if (bar && "IntersectionObserver" in window) {
    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting; });
      bar.style.display = Object.keys(visible).some(function (k) { return visible[k]; }) ? "none" : "";
    });
    ["start", "get", "contact"].forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }

  function track(name, params) { if (window.gtag) window.gtag("event", name, params || {}); }

  // Starter answers. Types the questionnaire covers go to the estimator; the rest
  // pre-fill the contact form, because those are scoped on a call.
  document.querySelectorAll("a[data-project]").forEach(function (el) {
    el.addEventListener("click", function () {
      var type = el.getAttribute("data-project");
      track("estimator_start", { project_type: type, page: location.pathname });
      var select = document.getElementById("f-type");
      if (el.getAttribute("href") === "#contact" && select) {
        for (var i = 0; i < select.options.length; i++) {
          if (select.options[i].getAttribute("data-project") === type) select.selectedIndex = i;
        }
      }
    });
  });
  document.querySelectorAll("[data-track]").forEach(function (el) {
    el.addEventListener("click", function () { track(el.getAttribute("data-track"), { page: location.pathname }); });
  });

  // Where this visitor first came from (tracking tag on the link, or the referring site),
  // kept for 90 days in this browser and sent with the form, so the Pipeline tab in the
  // outreach sheet can tell LinkedIn, outreach, search and direct leads apart.
  var firstTouch = (function () {
    var KEY = "zclap_first_touch", now = Date.now();
    var q = new URLSearchParams(location.search), saved = null;
    try { saved = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (err) { saved = null; }
    if (saved && now - saved.t > 90 * 864e5) saved = null;
    var ref = document.referrer && document.referrer.indexOf(location.origin) !== 0 ? document.referrer : "";
    if (!saved || q.get("utm_source")) {
      saved = { t: now, utm_source: q.get("utm_source") || "", utm_medium: q.get("utm_medium") || "",
        utm_campaign: q.get("utm_campaign") || "", referrer: ref.split("?")[0], landing_page: location.pathname };
      try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (err) { /* private mode: send this page's values */ }
    }
    return saved;
  })();

  document.querySelectorAll("form[data-web3]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      ["utm_source", "utm_medium", "utm_campaign", "referrer", "landing_page"].forEach(function (k) {
        var input = form.querySelector('input[name="' + k + '"]');
        if (!input) { input = document.createElement("input"); input.type = "hidden"; input.name = k; form.appendChild(input); }
        input.value = firstTouch[k] || "";
      });
      var b = form.querySelector("button[type=submit]");
      var label = b.innerHTML;
      b.disabled = true; b.textContent = "Sending…";
      fetch(form.action, { method: "POST", headers: { Accept: "application/json" }, body: new FormData(form) })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (!d.success) throw new Error("not sent");
          form.querySelector(".fields").style.display = "none";
          form.querySelector(".ok").style.display = "block";
          track(form.getAttribute("data-event") || "generate_lead", { form: form.id || "lead", page: location.pathname });
        })
        .catch(function () {
          b.disabled = false; b.innerHTML = label;
          alert("That didn't go through. Please email info@zclap.com and we'll pick it up.");
        });
    });
  });
})();
