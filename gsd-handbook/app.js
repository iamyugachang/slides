'use strict';
(() => {
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  const key = 'gsd-handbook-v1';
  let state = { runtime: 'codex', done: {}, notes: {} };
  let timer;
  function notify(message) {
    $('#status').textContent = message;
    clearTimeout(timer);
    timer = setTimeout(() => { $('#status').textContent = ''; }, 4500);
  }
  try {
    const saved = JSON.parse(localStorage.getItem(key));
    if (saved && typeof saved === 'object') {
      if (['codex', 'claude', 'opencode'].includes(saved.runtime)) state.runtime = saved.runtime;
      if (saved.done && typeof saved.done === 'object') state.done = saved.done;
      if (saved.notes && typeof saved.notes === 'object') state.notes = saved.notes;
    }
  } catch { notify('無法讀取本機紀錄；你仍可閱讀與下載筆記。'); }
  function save() {
    try { localStorage.setItem(key, JSON.stringify(state)); }
    catch { notify('瀏覽器未能保存。請下載筆記備份。'); }
  }
  function runtime() {
    const r = $('#runtime').value;
    const tokens = { GSD: r === 'codex' ? '$gsd-' : '/gsd-', CLI: r, INSTALL: '--' + r };
    $$('[data-token]').forEach(n => { n.textContent = tokens[n.dataset.token]; });
    state.runtime = r;
  }
  $('#runtime').value = state.runtime;
  runtime();
  $('#runtime').addEventListener('change', () => { runtime(); save(); notify('指令已切換；終端機與 AI 對話框請分開操作。'); });
  function progress() {
    const checks = $$('[data-complete]');
    checks.forEach(n => { n.checked = state.done[n.dataset.complete] === true; });
    $$('[data-chapter]').forEach(n => { n.querySelector('.nav-check').textContent = state.done[n.dataset.chapter] === true ? '✓' : ''; });
    const count = checks.filter(n => n.checked).length;
    $('#progress-label').textContent = `${count} / ${checks.length}`;
    $('#reading-progress').max = checks.length;
    $('#reading-progress').value = count;
  }
  $$('[data-complete]').forEach(n => n.addEventListener('change', () => { state.done[n.dataset.complete] = n.checked; save(); progress(); }));
  progress();
  function closeMenu() { $('#rail').classList.remove('open'); $('#menu-toggle').setAttribute('aria-expanded', 'false'); }
  $('#menu-toggle').addEventListener('click', () => {
    const open = $('#rail').classList.toggle('open');
    $('#menu-toggle').setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && $('#rail').classList.contains('open')) { closeMenu(); $('#menu-toggle').focus(); } });
  function navigate(focus = false) {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { id = 'start'; }
    const target = document.getElementById(id);
    const chapter = target?.closest('.chapter') || $('#start');
    $$('.chapter').forEach(n => { n.hidden = n !== chapter; });
    $$('[data-chapter]').forEach(n => {
      if (n.dataset.chapter === chapter.id) n.setAttribute('aria-current', 'page');
      else n.removeAttribute('aria-current');
    });
    document.title = `${chapter.querySelector('h1').textContent} — GSD × SDLC`;
    closeMenu();
    if (focus) chapter.querySelector('h1').focus({ preventScroll: true });
    if (target && target !== chapter) target.scrollIntoView();
    else window.scrollTo({ top: 0, behavior: 'instant' });
  }
  document.documentElement.classList.add('js');
  window.addEventListener('hashchange', () => navigate(true));
  navigate();
  $$('.copy').forEach(button => button.addEventListener('click', async () => {
    const text = button.closest('.code-block').querySelector('pre').textContent;
    try {
      if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(text);
      else {
        const area = document.createElement('textarea');
        area.value = text; area.style.position = 'fixed'; area.style.opacity = '0';
        document.body.append(area); area.select();
        const ok = document.execCommand('copy'); area.remove();
        if (!ok) throw new Error('copy failed');
        button.focus();
      }
      notify('已複製。請貼到此區塊標示的位置。');
    } catch { notify('無法自動複製；請選取指令文字手動複製。'); }
  }));
  $$('[data-note]').forEach(n => {
    n.value = typeof state.notes[n.dataset.note] === 'string' ? state.notes[n.dataset.note] : '';
    n.addEventListener('input', () => { state.notes[n.dataset.note] = n.value; save(); });
  });
  $('#export-notes').addEventListener('click', () => {
    let body = '# Habit Quest — 我的產品構想\n\n這是探索草稿，尚未確認的內容請先討論，不要直接實作。\n';
    $$('[data-note]').forEach(n => { body += `\n## ${n.parentElement.firstChild.textContent.trim()}\n\n${n.value.trim() || '（尚待討論）'}\n`; });
    body += '\n## 下一步\n\n先 brainstorm 與 refine，再用 GSD new-project 初始化。每次只問一個問題，等我回答。\n';
    const url = URL.createObjectURL(new Blob([body], { type: 'text/markdown;charset=utf-8' }));
    const a = document.createElement('a'); a.href = url; a.download = 'idea.md'; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  $('#reset-progress').addEventListener('click', () => {
    if (!confirm('清除這個瀏覽器的全部練習進度與筆記？此動作無法復原，請先下載備份。')) return;
    state.done = {}; state.notes = {};
    $$('[data-note]').forEach(n => { n.value = ''; }); save(); progress(); notify('已清除本機練習紀錄。');
  });
  const rows = $$('#command-table tbody tr');
  function filter() {
    const query = $('#command-search').value.trim().toLowerCase();
    rows.forEach(n => { n.hidden = !n.textContent.toLowerCase().includes(query); });
    $('#command-count').textContent = `顯示 ${rows.filter(n => !n.hidden).length} / ${rows.length} 個常用指令`;
  }
  $('#command-search').addEventListener('input', filter); filter();
  let xp = 0;
  function showXP() {
    const level = 1 + Math.floor(xp / 100);
    $('#xp-level').textContent = `Lv.${level}`;
    $('#xp-total').textContent = `${xp} XP`;
    $('#xp-bar').value = xp % 100;
    $('#xp-unlock').textContent = level >= 3 ? 'Lv.3：解鎖故事第二節' : level >= 2 ? 'Lv.2：獲得晨光徽章' : '下一個里程碑：100 XP → Lv.2 晨光徽章';
  }
  $('#xp-add').addEventListener('click', () => { xp += 20; showXP(); });
  $('#xp-reset').addEventListener('click', () => { xp = 0; showXP(); });
  showXP();
  $('#print').addEventListener('click', () => window.print());
})();
