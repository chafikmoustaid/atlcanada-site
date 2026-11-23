/* Page Actualités : filtres par thème et affichage progressif (amélioration progressive :
   sans JavaScript, toutes les actualités restent visibles). */
(function () {
  var list = document.getElementById('news-list');
  var bar = document.querySelector('.news-filters');
  var btn = document.getElementById('news-more');
  if (!list || !bar || !btn) return;
  var items = [].slice.call(list.querySelectorAll('.news-item'));
  var chips = [].slice.call(bar.querySelectorAll('.news-chip'));
  var PAGE = 8, theme = 'all', shown = PAGE;
  var ar = document.documentElement.lang.indexOf('ar') === 0;

  function render() {
    var n = 0, rest = 0;
    items.forEach(function (it) {
      var ok = theme === 'all' || it.getAttribute('data-theme') === theme;
      if (ok && n < shown) { it.hidden = false; n++; }
      else { it.hidden = true; if (ok) rest++; }
    });
    chips.forEach(function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-theme') === theme ? 'true' : 'false'); });
    btn.parentNode.hidden = rest === 0;
    btn.textContent = (ar ? 'عرض المزيد (' : 'Afficher plus (') + rest + ')';
  }
  function reveal(id) {
    var el = id && document.getElementById(id);
    if (!el || !el.classList.contains('news-item')) return;
    theme = 'all'; shown = items.length; render();
    setTimeout(function () { el.scrollIntoView(); }, 30);
  }
  bar.hidden = false;
  chips.forEach(function (c) {
    c.addEventListener('click', function () { theme = c.getAttribute('data-theme'); shown = PAGE; render(); });
  });
  btn.addEventListener('click', function () { shown += PAGE; render(); });
  window.addEventListener('hashchange', function () { reveal(location.hash.slice(1)); });
  render();
  if (location.hash) reveal(decodeURIComponent(location.hash.slice(1)));
})();
