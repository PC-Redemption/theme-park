(function () {
  let catalogData = null;

  function byId(id) {
    return document.getElementById(id);
  }

  async function loadCatalog() {
    const response = await fetch("./starters.json", { cache: "no-store" });
    if (!response.ok) throw new Error("Catalog load failed");
    return await response.json();
  }

  function familyBadge(item) {
    return '<span class="tp-badge">' + item.family + "</span>";
  }

  function strengthBadges(item) {
    return item.strengths.map(function (entry) {
      return '<span class="tp-badge">' + entry + "</span>";
    }).join(" ");
  }

  function commandRow(label, value, id) {
    return [
      '<div class="tp-command-row">',
      "<span>" + label + "</span>",
      "<code id=\"" + id + "\">" + value + "</code>",
      '<button class="tp-button secondary" type="button" data-copy-target="' + id + '">Copy</button>',
      "</div>"
    ].join("");
  }

  function previewMarkup(item) {
    if (item.preview.image) {
      return '<img class="tp-preview-image" src="' + item.preview.image + '" alt="' + item.name + ' preview">';
    }
    return '<div class="tp-preview-fallback"><strong>Preview pending</strong><p class="tp-subtitle">Run <code>npm run catalog:shots</code> to capture a live render.</p></div>';
  }

  function starterCard(item, anchorId) {
    const cardId = item.key.replace(/[^a-z0-9]+/gi, "-").toLowerCase();
    return [
      '<article class="tp-card tp-starter-card" id="' + anchorId + '" data-family="' + item.family + '" data-runtime="' + item.runtime + '">',
      '<div class="tp-preview-frame">' + previewMarkup(item) + "</div>",
      '<div class="tp-action-bar"><span class="tp-muted">' + item.family + " / " + item.runtime + "</span>" + familyBadge(item) + "</div>",
      "<strong>" + item.name + "</strong>",
      '<p class="tp-subtitle">' + item.summary + "</p>",
      '<div class="tp-action-bar">' + strengthBadges(item) + "</div>",
      '<div class="tp-command-stack">',
      commandRow("Preview", item.commands.preview, cardId + "-preview"),
      commandRow("Copy", item.commands.copy, cardId + "-copy"),
      commandRow("Screenshot", item.commands.screenshot, cardId + "-shot"),
      "</div>",
      '<div class="tp-inline-links"><a href="' + item.preview.url + '" target="_blank" rel="noreferrer">Open preview URL</a><a href="../' + item.paths.site_dir + '/README.md" target="_blank" rel="noreferrer">Open starter README</a></div>',
      "</article>"
    ].join("");
  }

  function populateFamilyFilter(data) {
    const familySelect = byId("catalog-family");
    const familySeed = byId("builder-family-seed");
    const familyNav = byId("family-nav");
    if (familySelect) {
      Object.keys(data.families).forEach(function (family) {
        const option = document.createElement("option");
        option.value = family;
        option.textContent = data.families[family].label;
        familySelect.appendChild(option);
      });
    }
    if (familySeed) {
      Object.keys(data.families).forEach(function (family) {
        const option = document.createElement("option");
        option.value = family;
        option.textContent = data.families[family].label;
        familySeed.appendChild(option);
      });
    }
    if (familyNav) {
      Object.keys(data.families).forEach(function (family) {
        const link = document.createElement("a");
        link.href = "#family-" + family;
        link.textContent = data.families[family].label;
        familyNav.appendChild(link);
      });
    }
  }

  function populateStarterInputs(data) {
    ["builder-preview-starter", "builder-copy-source"].forEach(function (id) {
      const select = byId(id);
      if (!select) return;
      data.starters.forEach(function (starter) {
        const option = document.createElement("option");
        option.value = starter.key;
        option.textContent = starter.name;
        select.appendChild(option);
      });
    });
  }

  function filteredStarters() {
    if (!catalogData) return [];
    const search = (byId("catalog-search")?.value || "").toLowerCase();
    const family = byId("catalog-family")?.value || "all";
    const runtime = byId("catalog-runtime")?.value || "all";

    return catalogData.starters.filter(function (item) {
      const haystack = [
        item.key,
        item.name,
        item.family,
        item.runtime,
        item.summary
      ].concat(item.strengths).join(" ").toLowerCase();
      return (!search || haystack.indexOf(search) >= 0) &&
        (family === "all" || item.family === family) &&
        (runtime === "all" || item.runtime === runtime);
    });
  }

  function renderCatalog(data) {
    const grid = byId("starter-grid");
    const starterCount = byId("starter-count");
    const familyCount = byId("family-count");
    const catalogStatus = byId("catalog-status");
    if (!grid || !starterCount || !familyCount || !catalogStatus) return;

    const starters = data ? filteredStarters() : [];
    starterCount.textContent = starters.length + " starters";
    familyCount.textContent = Object.keys(data.families).length + " families";
    catalogStatus.textContent = starters.length ? "Live previews and commands ready" : "No starters matched the current filters";
    if (!starters.length) {
      grid.innerHTML = '<article class="tp-card warning"><strong>No starters matched</strong><p class="tp-subtitle">Try a broader search or reset your filters.</p></article>';
      bindCopyButtons();
      return;
    }

    const seenFamilies = {};
    grid.innerHTML = starters.map(function (starter) {
      const anchorId = seenFamilies[starter.family]
        ? starter.family + "-" + starter.runtime + "-" + starter.key
        : "family-" + starter.family;
      seenFamilies[starter.family] = true;
      return starterCard(starter, anchorId);
    }).join("");
    bindCopyButtons();
  }

  function refreshBuilders() {
    if (!catalogData) return;
    const previewStarter = byId("builder-preview-starter")?.value || catalogData.starters[0]?.key || "";
    const previewCommand = byId("builder-preview-command");
    if (previewCommand) {
      previewCommand.textContent = "scripts/preview-starter.sh " + previewStarter;
    }

    const copySource = byId("builder-copy-source")?.value || catalogData.starters[0]?.key || "";
    const copyDest = byId("builder-copy-dest")?.value || "mission-control-jinja";
    const copyName = byId("builder-copy-name")?.value || "Mission Control Jinja";
    const copyCommand = byId("builder-copy-command");
    if (copyCommand) {
      copyCommand.textContent = "python3 scripts/theme-park.py starter-copy --source " + copySource + " --dest " + copyDest + ' --name "' + copyName + '"';
    }

    const familySeed = byId("builder-family-seed")?.value || Object.keys(catalogData.families)[0] || "operations";
    const familySlug = byId("builder-family-slug")?.value || "mission-control";
    const familySite = byId("builder-family-site")?.value || "mission-control";
    const familyName = byId("builder-family-name")?.value || "Mission Control";
    const familyCommand = byId("builder-family-command");
    if (familyCommand) {
      familyCommand.textContent = "python3 scripts/theme-park.py family-create --seed-family " + familySeed + " --family " + familySlug + " --site-slug " + familySite + ' --display-name "' + familyName + '"';
    }
  }

  function bindFilters() {
    ["catalog-search", "catalog-family", "catalog-runtime"].forEach(function (id) {
      const element = byId(id);
      if (!element) return;
      element.addEventListener("input", function () {
        renderCatalog(catalogData);
      });
      element.addEventListener("change", function () {
        renderCatalog(catalogData);
      });
    });
    ["builder-preview-starter", "builder-copy-source", "builder-copy-dest", "builder-copy-name", "builder-family-seed", "builder-family-slug", "builder-family-site", "builder-family-name"].forEach(function (id) {
      const element = byId(id);
      if (!element) return;
      element.addEventListener("input", refreshBuilders);
      element.addEventListener("change", refreshBuilders);
    });
  }

  function bindCopyButtons() {
    document.querySelectorAll("[data-copy-target]").forEach(function (button) {
      if (button.dataset.bound === "true") return;
      button.dataset.bound = "true";
      button.addEventListener("click", async function () {
        const targetId = button.getAttribute("data-copy-target");
        const target = targetId ? byId(targetId) : null;
        if (!target) return;
        await navigator.clipboard.writeText(target.textContent || "");
        button.textContent = "Copied";
        window.setTimeout(function () {
          button.textContent = "Copy";
          if (button.classList.contains("tp-button") && button.classList.contains("secondary")) {
            button.textContent = button.getAttribute("data-copy-target") === "builder-preview-command" ||
              button.getAttribute("data-copy-target") === "builder-copy-command" ||
              button.getAttribute("data-copy-target") === "builder-family-command"
              ? "Copy command"
              : "Copy";
          }
        }, 1200);
      });
    });
  }

  function renderError(error) {
    const grid = byId("starter-grid");
    if (!grid) return;
    grid.innerHTML = '<article class="tp-card danger"><strong>Catalog failed to load</strong><p class="tp-subtitle">' + error.message + "</p></article>";
  }

  loadCatalog().then(function (data) {
    catalogData = data;
    populateFamilyFilter(data);
    populateStarterInputs(data);
    bindFilters();
    refreshBuilders();
    renderCatalog(data);
  }).catch(renderError);
})();
