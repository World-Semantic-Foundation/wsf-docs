/*
 * WSF Reference Site : application script
 * Vanilla JS, no dependencies. Provides search, tier filters, tabs,
 * collapsible hierarchy, and copy buttons.
 */
(function () {
  'use strict';

  /* ---------------- utilities ---------------- */

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  function debounce(fn, ms) {
    var t;
    return function () {
      var args = arguments, self = this;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(self, args); }, ms);
    };
  }

  function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return Promise.reject(new Error('clipboard unavailable'));
  }

  /* ---------------- copy buttons ---------------- */

  function initCopyButtons() {
    $$('.copy-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var target = $(btn.dataset.copyTarget);
        if (!target) return;
        copyToClipboard(target.textContent).then(function () {
          var orig = btn.textContent;
          btn.textContent = 'Copied';
          btn.classList.add('copied');
          setTimeout(function () { btn.textContent = orig; btn.classList.remove('copied'); }, 1600);
        });
      });
    });
  }

  /* ---------------- tabs ---------------- */

  function initTabs() {
    $$('.tabs').forEach(function (tabsEl) {
      var btns = $$('.tab-btn', tabsEl);
      var owner = tabsEl.closest('.tab-group');
      if (!owner) return;
      btns.forEach(function (btn) {
        btn.addEventListener('click', function () {
          btns.forEach(function (b) { b.classList.remove('active'); b.setAttribute('aria-selected', 'false'); });
          btn.classList.add('active');
          btn.setAttribute('aria-selected', 'true');
          $$('.tab-panel', owner).forEach(function (p) {
            p.hidden = (p.id !== btn.dataset.tabTarget);
          });
          if (window.location.hash !== '#' + btn.id) {
            history.replaceState(null, '', '#' + btn.id);
          }
        });
      });
      // deep-link to a tab
      var hash = window.location.hash.slice(1);
      if (hash) {
        var target = $$('.tab-btn', tabsEl).find(function (b) { return b.id === hash; });
        if (target) { target.click(); }
      }
    });
  }

  /* ---------------- search + tier filter (concepts browser) ---------------- */

  var conceptsIndex = null;

  function normalise(s) { return (s || '').toLowerCase(); }

  function renderConceptList(items) {
    var container = $('#concept-list');
    if (!container) return;
    if (!items.length) {
      container.innerHTML = '<p class="muted">No concepts match your search.</p>';
      return;
    }
    container.innerHTML = items.map(function (c) {
      return (
        '<a class="concept-card" href="' + c.url + '">' +
        '<div class="concept-card-head">' +
        '<span class="concept-name">' + c.preferred_name + '</span>' +
        '<span class="tier-badge tier-' + c.tier_key + '">' + c.tier + '</span>' +
        '</div>' +
        '<p class="concept-card-def">' + (c.definition || '') + '</p>' +
        '<code class="concept-card-id">' + c.semantic_id + '</code>' +
        '</a>'
      );
    }).join('');
    var count = $('#search-count');
    if (count) {
      count.textContent = items.length + ' concept' + (items.length === 1 ? '' : 's');
    }
  }

  function applyFilters() {
    var query = normalise($('#search-box') && $('#search-box').value);
    var activeTier = ($('.tier-filter-btn.active') || {}).dataset ? $('.tier-filter-btn.active').dataset.tier : 'all';
    var items = (conceptsIndex || []).filter(function (c) {
      var matchesTier = (activeTier === 'all' || c.tier_key === activeTier);
      if (!matchesTier) return false;
      if (!query) return true;
      var haystack = normalise([
        c.preferred_name, c.semantic_id, c.definition,
        (c.aliases || []).join(' '), c.domain, c.parent
      ].join(' '));
      return haystack.indexOf(query) !== -1;
    });
    renderConceptList(items);
  }

  function initConceptBrowser() {
    var searchBox = $('#search-box');
    if (!searchBox || !$('#concept-list')) return;
    var done = function (data) {
      conceptsIndex = data.concepts || [];
      applyFilters();
    };
    fetch('data/concepts.json')
      .then(function (r) { return r.json(); })
      .then(done)
      .catch(function () { /* index unavailable; list rendered server-side */ });

    searchBox.addEventListener('input', debounce(applyFilters, 120));

    $$('.tier-filter-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        $$('.tier-filter-btn').forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        applyFilters();
      });
    });
  }

  /* ---------------- hero search (index) ---------------- */

  function initHeroSearch() {
    var input = $('#hero-search');
    if (!input) return;
    var panel = $('#hero-results');
    fetch('data/concepts.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var concepts = data.concepts || [];
        input.addEventListener('input', debounce(function () {
          var q = normalise(input.value).trim();
          if (q.length < 2) { panel.innerHTML = ''; panel.hidden = true; return; }
          var hits = concepts.filter(function (c) {
            return normalise(c.preferred_name + ' ' + c.semantic_id + ' ' + (c.definition || '') + ' ' + (c.aliases || []).join(' ')).indexOf(q) !== -1;
          }).slice(0, 6);
          panel.hidden = false;
          panel.innerHTML = hits.length
            ? hits.map(function (c) {
                return '<a class="hero-hit" href="' + c.url + '"><strong>' + c.preferred_name + '</strong><span>' + (c.definition || c.semantic_id) + '</span></a>';
              }).join('')
            : '<span class="hero-hit muted">No matching concept</span>';
        }, 140));
      })
      .catch(function () {});
  }

  /* ---------------- hierarchy tree ---------------- */

  function initTree() {
    $$('.tree-children').forEach(function (ul) {
      ul.hidden = true;
    });
    $$('.tree-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var children = $('#' + btn.dataset.treeTarget);
        if (!children) return;
        children.hidden = !children.hidden;
        btn.classList.toggle('open', !children.hidden);
      });
    });
  }

  /* ---------------- mobile nav ---------------- */

  function initNav() {
    var toggle = $('#nav-toggle');
    var menu = $('#nav-menu');
    if (toggle && menu) {
      toggle.addEventListener('click', function () {
        menu.classList.toggle('open');
      });
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    initNav();
    initCopyButtons();
    initTabs();
    initConceptBrowser();
    initHeroSearch();
    initTree();
  });
})();
