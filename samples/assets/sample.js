// 見本で共通に使う処理: テーマの切り替え、アイコンの差し込み、見本どうしの行き来。
// アプリへはこのファイルを配らない（決まりは docs/coding.md）。
(() => {
  const THEMES = [
    { key: 'shiro', label: '白' },
    { key: 'kaki', label: 'カーキ' },
    { key: 'ekisho', label: '液晶' },
    { key: 'kuro', label: '黒' },
  ];
  const STORAGE_KEY = 'keiso.theme';
  const PAGES = [
    { href: 'index.html', label: 'Index' },
    { href: 'palette.html', label: 'Palette' },
    { href: 'extra-colors.html', label: 'Extra' },
    { href: 'icons.html', label: 'Icons' },
    { href: 'ui-kit.html', label: 'UI Kit' },
    { href: 'patterns.html', label: 'Patterns' },
    { href: 'layout.html', label: 'Layout' },
  ];

  const read_saved = () => {
    try { return localStorage.getItem(STORAGE_KEY); } catch { return null; }
  };
  const save = (key) => {
    try { localStorage.setItem(STORAGE_KEY, key); } catch { /* 保存できなくても切り替えは効く */ }
  };

  const apply_theme = (key) => {
    const root = document.documentElement;
    if (key && THEMES.some((t) => t.key === key)) {
      root.dataset.theme = key;
    } else {
      delete root.dataset.theme;
    }
    document.querySelectorAll('[data-theme-key]').forEach((btn) => {
      btn.setAttribute('aria-pressed', String(btn.dataset.themeKey === (root.dataset.theme || 'auto')));
    });
    document.dispatchEvent(new CustomEvent('keiso:theme'));
  };

  const initial_theme = new URLSearchParams(location.search).get('theme') || read_saved();
  apply_theme(initial_theme);

  const icon_svg = (spec) => {
    const [set, name] = spec.split(':');
    const icons = window.KEISO_ICONS || {};
    return (icons[set] && icons[set][name]) || '';
  };

  const fill_icons = (scope) => {
    scope.querySelectorAll('[data-icon]').forEach((el) => {
      if (el.dataset.iconDone) return;
      el.innerHTML = icon_svg(el.dataset.icon);
      el.classList.add('k-icon');
      el.setAttribute('aria-hidden', 'true');
      el.dataset.iconDone = '1';
    });
  };

  const build_header = () => {
    const header = document.getElementById('js-sample-header');
    if (!header) return;
    const current = location.pathname.split('/').pop() || 'index.html';
    const nav_links = PAGES.map((p) => `<a href="${p.href}"${p.href === current ? ' aria-current="page"' : ''}>${p.label}</a>`).join('');
    const theme_buttons = [{ key: 'auto', label: 'OS' }, ...THEMES]
      .map((t) => `<button type="button" data-theme-key="${t.key}">${t.label}</button>`).join('');
    header.className = 'k-header';
    header.innerHTML = `
      <div class="k-header__inner sample-header">
        <a class="k-logo" href="index.html"><span data-icon="solid:keiso"></span>keiso</a>
        <nav class="k-nav" aria-label="見本">${nav_links}</nav>
        <div class="k-segment sample-themes" role="group" aria-label="テーマ">${theme_buttons}</div>
      </div>`;
    header.querySelectorAll('[data-theme-key]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.themeKey === 'auto' ? null : btn.dataset.themeKey;
        save(key || '');
        apply_theme(key);
      });
    });
    apply_theme(document.documentElement.dataset.theme || null);
  };

  window.keiso_sample = { THEMES, fill_icons, icon_svg, apply_theme };

  document.addEventListener('DOMContentLoaded', () => {
    build_header();
    fill_icons(document);
  });
})();
