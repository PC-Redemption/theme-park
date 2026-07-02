(function () {
  const THEME_STORAGE = {
    mode: "theme-park.theme.mode",
    color: "theme-park.theme.color"
  };

  const THEME_ALLOWED = {
    mode: ["light", "dark"],
    color: ["black", "green", "blue", "plum", "orange", "red"]
  };

  function isAllowed(kind, value) {
    return THEME_ALLOWED[kind].indexOf(value) >= 0;
  }

  function readStoredTheme(kind, fallback) {
    try {
      const value = window.localStorage.getItem(THEME_STORAGE[kind]);
      return isAllowed(kind, value) ? value : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function writeStoredTheme(kind, value) {
    if (!isAllowed(kind, value)) return;
    try {
      window.localStorage.setItem(THEME_STORAGE[kind], value);
    } catch (error) {
      return;
    }
  }

  function currentTheme() {
    const root = document.documentElement;
    const fallbackMode = isAllowed("mode", root.dataset.themeMode) ? root.dataset.themeMode : "light";
    const fallbackColor = isAllowed("color", root.dataset.themeColor) ? root.dataset.themeColor : "blue";
    return {
      mode: readStoredTheme("mode", fallbackMode),
      color: readStoredTheme("color", fallbackColor)
    };
  }

  function applyTheme(theme, persist) {
    const mode = isAllowed("mode", theme.mode) ? theme.mode : "light";
    const color = isAllowed("color", theme.color) ? theme.color : "blue";
    document.documentElement.dataset.themeMode = mode;
    document.documentElement.dataset.themeColor = color;
    syncThemeButtons({ mode: mode, color: color });
    if (persist) {
      writeStoredTheme("mode", mode);
      writeStoredTheme("color", color);
    }
  }

  function syncThemeButtons(theme) {
    document.querySelectorAll("[data-tp-theme-mode]").forEach(function (button) {
      const selected = button.dataset.tpThemeMode === theme.mode;
      button.setAttribute("aria-pressed", selected ? "true" : "false");
    });
    document.querySelectorAll("[data-tp-theme-color]").forEach(function (button) {
      const selected = button.dataset.tpThemeColor === theme.color;
      button.setAttribute("aria-pressed", selected ? "true" : "false");
    });
  }

  function closePanels(selector) {
    document.querySelectorAll(selector).forEach(function (panel) {
      panel.hidden = true;
    });
  }

  function setupThemeControls() {
    document.addEventListener("click", function (event) {
      const modeButton = event.target.closest("[data-tp-theme-mode]");
      if (modeButton) {
        applyTheme({ mode: modeButton.dataset.tpThemeMode, color: currentTheme().color }, true);
        return;
      }

      const colorButton = event.target.closest("[data-tp-theme-color]");
      if (colorButton) {
        applyTheme({ mode: currentTheme().mode, color: colorButton.dataset.tpThemeColor }, true);
      }
    });
  }

  function setupNavToggle() {
    document.addEventListener("click", function (event) {
      const button = event.target.closest("[data-tp-nav-toggle]");
      if (!button) return;
      const shell = document.querySelector("[data-tp-shell]");
      if (!shell) return;
      shell.classList.toggle("nav-collapsed");
      const expanded = !shell.classList.contains("nav-collapsed");
      button.setAttribute("aria-expanded", expanded ? "true" : "false");
    });
  }

  function setupMenus() {
    document.addEventListener("click", function (event) {
      const toggle = event.target.closest("[data-tp-menu-toggle]");
      if (toggle) {
        const panelId = toggle.getAttribute("aria-controls");
        const panel = panelId ? document.getElementById(panelId) : null;
        if (!panel) return;
        const nextHidden = !panel.hidden;
        closePanels("[data-tp-menu-panel]");
        panel.hidden = nextHidden;
        toggle.setAttribute("aria-expanded", nextHidden ? "false" : "true");
        return;
      }

      if (!event.target.closest("[data-tp-menu-root]")) {
        closePanels("[data-tp-menu-panel]");
        document.querySelectorAll("[data-tp-menu-toggle]").forEach(function (button) {
          button.setAttribute("aria-expanded", "false");
        });
      }
    });
  }

  function toast(message, tone) {
    const region = document.getElementById("tp-toast-region");
    if (!region) return;
    const item = document.createElement("div");
    item.className = "tp-toast " + (tone || "info");
    item.textContent = message || "Action complete";
    region.appendChild(item);
    window.setTimeout(function () {
      item.remove();
    }, 4000);
  }

  function setupActionButtons() {
    document.addEventListener("click", function (event) {
      const button = event.target.closest("[data-tp-action-label]");
      if (!button) return;
      event.preventDefault();
      toast(button.dataset.tpActionLabel, button.dataset.tpActionTone || "info");
    });
  }

  function init() {
    applyTheme(currentTheme(), false);
    setupThemeControls();
    setupNavToggle();
    setupMenus();
    setupActionButtons();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
