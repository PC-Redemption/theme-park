(function () {
  let catalogData = null;

  async function loadCatalog() {
    const response = await fetch("./starters.json", { cache: "no-store" });
    if (!response.ok) throw new Error("Catalog load failed");
    return await response.json();
  }

  function starterCard(item) {
    const strengths = item.strengths.map(function (entry) {
      return '<span class="tp-badge">' + entry + "</span>";
    }).join(" ");

    return [
      '<article class="tp-card" data-family="' + item.family + '" data-runtime="' + item.runtime + '">',
      '<img src="' + item.preview.image + '" alt="' + item.name + ' preview" style="width:100%; border-radius:12px; border:1px solid var(--tp-color-border); margin-bottom:12px;">',
      '<span class="tp-muted">' + item.family + " / " + item.runtime + "</span>",
      "<strong>" + item.name + "</strong>",
      '<p class="tp-subtitle">' + item.summary + "</p>",
      '<p><code>' + item.paths.site_dir + "</code></p>",
      '<p><strong>Preview</strong><br><code>' + item.preview.script + "</code></p>",
      '<p><strong>URL</strong><br><code>' + item.preview.url + "</code></p>",
      '<div class="tp-action-bar">' + strengths + "</div>",
      "</article>"
    ].join("");
  }

  function populateFamilyFilter(data) {
    const familySelect = document.getElementById("catalog-family");
    if (!familySelect) return;
    Object.keys(data.families).forEach(function (family) {
      const option = document.createElement("option");
      option.value = family;
      option.textContent = family;
      familySelect.appendChild(option);
    });
  }

  function filteredStarters() {
    if (!catalogData) return [];
    const search = (document.getElementById("catalog-search")?.value || "").toLowerCase();
    const family = document.getElementById("catalog-family")?.value || "all";
    const runtime = document.getElementById("catalog-runtime")?.value || "all";

    return catalogData.starters.filter(function (item) {
      const haystack = [
        item.key,
        item.name,
        item.family,
        item.runtime,
        item.summary
      ].concat(item.strengths).join(" ").toLowerCase();
      const matchesSearch = !search || haystack.indexOf(search) >= 0;
      const matchesFamily = family === "all" || item.family === family;
      const matchesRuntime = runtime === "all" || item.runtime === runtime;
      return matchesSearch && matchesFamily && matchesRuntime;
    });
  }

  function renderCatalog(data) {
    const grid = document.getElementById("starter-grid");
    const starterCount = document.getElementById("starter-count");
    const familyCount = document.getElementById("family-count");
    if (!grid || !starterCount || !familyCount) return;

    const starters = data ? filteredStarters() : [];
    starterCount.textContent = starters.length + " starters";
    familyCount.textContent = Object.keys(data.families).length + " families";
    grid.innerHTML = starters.length ? starters.map(starterCard).join("") : '<article class="tp-card warning"><strong>No starters matched</strong><p class="tp-subtitle">Try a broader search or reset your filters.</p></article>';
  }

  function bindFilters() {
    ["catalog-search", "catalog-family", "catalog-runtime"].forEach(function (id) {
      const element = document.getElementById(id);
      if (!element) return;
      element.addEventListener("input", function () {
        renderCatalog(catalogData);
      });
      element.addEventListener("change", function () {
        renderCatalog(catalogData);
      });
    });
  }

  function renderError(error) {
    const grid = document.getElementById("starter-grid");
    if (!grid) return;
    grid.innerHTML = '<article class="tp-card danger"><strong>Catalog failed to load</strong><p class="tp-subtitle">' + error.message + "</p></article>";
  }

  loadCatalog().then(function (data) {
    catalogData = data;
    populateFamilyFilter(data);
    bindFilters();
    renderCatalog(data);
  }).catch(renderError);
})();
