// Carrozzeria PRT – progressive enhancements (the site works without JS).
(function () {
  const header = document.querySelector("[data-header]");
  const nav = document.querySelector("[data-nav]");
  const navToggle = document.querySelector("[data-nav-toggle]");

  // Mobile menu
  function setNav(open) {
    if (!nav || !navToggle) return;
    if (open) {
      nav.style.setProperty("--nav-top", header.getBoundingClientRect().bottom + "px");
    }
    nav.classList.toggle("is-open", open);
    navToggle.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("nav-open", open);
  }
  navToggle?.addEventListener("click", () => setNav(!nav.classList.contains("is-open")));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav?.classList.contains("is-open")) {
      setNav(false);
      navToggle.focus();
    }
  });
  window.matchMedia("(min-width: 1081px)").addEventListener("change", (e) => e.matches && setNav(false));

  // Services submenu toggle (click / tap)
  document.querySelectorAll("[data-sub-toggle]").forEach((btn) => {
    const item = btn.closest("[data-sub]");
    btn.addEventListener("click", () => {
      const open = !item.classList.contains("is-open");
      item.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", (e) => {
      if (!item.contains(e.target) && item.classList.contains("is-open") && window.innerWidth > 1080) {
        item.classList.remove("is-open");
        btn.setAttribute("aria-expanded", "false");
      }
    });
  });

  // Header shadow once the page scrolls
  const onScroll = () => header?.classList.toggle("is-scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();
