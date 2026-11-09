// Local enhancement: each English page advertises the correct document language.
// Search remains the standard Material local client-side index of both corpora.
(function () {
  "use strict";
  function updateLanguage() {
    const isEnglish = /\/en(?:\/|$)/.test(window.location.pathname);
    document.documentElement.lang = isEnglish ? "en" : "bn";
    const input = document.querySelector('.md-search__input');
    if (input) {
      const label = isEnglish ? "Search Bangla and English guides" : "বাংলা ও English গাইডে খুঁজুন";
      input.setAttribute("aria-label", label);
      input.setAttribute("placeholder", label);
    }
  }
  if (typeof document$ !== "undefined") {
    document$.subscribe(updateLanguage); // Material instant navigation, if enabled later.
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", updateLanguage);
  } else {
    updateLanguage();
  }
})();
