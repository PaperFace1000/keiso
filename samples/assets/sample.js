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
    { href: 'inputs.html', label: 'Inputs' },
    { href: 'overlays.html', label: 'Overlays' },
    { href: 'records.html', label: 'Records' },
    { href: 'time.html', label: 'Time' },
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

  // ポップオーバー: ボタンで開け閉めし、外側を押す・Esc で閉じて、ボタンにフォーカスを戻す
  const popover = (trigger, panel, options = {}) => {
    const is_open = () => !panel.hidden;
    const close = (return_focus = true) => {
      if (!is_open()) return;
      panel.hidden = true;
      trigger.setAttribute('aria-expanded', 'false');
      if (options.on_close) options.on_close();
      if (return_focus) trigger.focus();
    };
    const open = () => {
      if (is_open()) return;
      panel.hidden = false;
      // 画面の端からはみ出すときは、端から 8px 残して内側へずらす
      panel.style.translate = '';
      const rect = panel.getBoundingClientRect();
      const view_width = document.documentElement.clientWidth;
      const shift = rect.left < 8 ? 8 - rect.left : rect.right > view_width - 8 ? view_width - 8 - rect.right : 0;
      if (shift !== 0) panel.style.translate = `${shift}px 0`;
      trigger.setAttribute('aria-expanded', 'true');
      if (options.on_open) options.on_open();
    };
    trigger.setAttribute('aria-expanded', 'false');
    if (panel.id) trigger.setAttribute('aria-controls', panel.id);
    trigger.addEventListener('click', () => (is_open() ? close() : open()));
    document.addEventListener('pointerdown', (e) => {
      if (is_open() && !panel.contains(e.target) && !trigger.contains(e.target)) close(false);
    });
    panel.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(); }
    });
    panel.addEventListener('focusout', (e) => {
      if (options.close_on_blur && e.relatedTarget && !panel.contains(e.relatedTarget) && e.relatedTarget !== trigger) close(false);
    });
    return { open, close, is_open };
  };

  // メニュー: 開いたら最初の項目へ。↑↓・Home・End で動き、Tab で閉じる
  const menu = (trigger, panel, on_pick) => {
    const items = () => [...panel.querySelectorAll('[role^="menuitem"]:not([aria-disabled="true"])')];
    const pop = popover(trigger, panel, { on_open: () => { const list = items(); const checked = list.find((i) => i.getAttribute('aria-checked') === 'true'); (checked || list[0]).focus(); }, close_on_blur: true });
    trigger.setAttribute('aria-haspopup', 'menu');
    trigger.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); pop.open(); }
    });
    panel.addEventListener('keydown', (e) => {
      const list = items();
      const index = list.indexOf(document.activeElement);
      const go = (i) => { e.preventDefault(); list[(i + list.length) % list.length].focus(); };
      if (e.key === 'ArrowDown') go(index + 1);
      if (e.key === 'ArrowUp') go(index - 1);
      if (e.key === 'Home') go(0);
      if (e.key === 'End') go(list.length - 1);
      if (e.key === 'Tab') pop.close(false);
    });
    panel.addEventListener('click', (e) => {
      const item = e.target.closest('[role^="menuitem"]');
      if (!item || item.getAttribute('aria-disabled') === 'true') return;
      if (item.getAttribute('role') === 'menuitemradio') {
        panel.querySelectorAll('[role="menuitemradio"]').forEach((i) => i.setAttribute('aria-checked', String(i === item)));
      }
      if (on_pick) on_pick(item);
      pop.close();
    });
    return pop;
  };

  // コピーのボタン: 1.5 秒だけ結果の文言とアイコンに変える
  const copy_button = (button, get_text) => {
    const label = button.querySelector('.js-copy-label');
    const icon = button.querySelector('[data-icon]');
    const initial = label.textContent;
    let timer = 0;
    const show = (ok) => {
      clearTimeout(timer);
      button.classList.toggle('is-done', ok);
      button.classList.toggle('is-failed', !ok);
      label.textContent = ok ? 'コピーした' : 'コピーできなかった';
      icon.innerHTML = icon_svg(ok ? 'line:check' : 'line:warning');
      timer = setTimeout(() => {
        button.classList.remove('is-done', 'is-failed');
        label.textContent = initial;
        icon.innerHTML = icon_svg('line:copy');
      }, 1500);
    };
    button.addEventListener('click', () => {
      if (!navigator.clipboard) { show(false); return; }
      navigator.clipboard.writeText(get_text()).then(() => show(true), () => show(false));
    });
  };

  window.keiso_sample = { THEMES, fill_icons, icon_svg, apply_theme, popover, menu, copy_button };

  document.addEventListener('DOMContentLoaded', () => {
    build_header();
    fill_icons(document);
  });
})();
