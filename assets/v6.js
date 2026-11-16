/* STMetal v6 */
(function () {
  var d = document, root = d.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Entrada do hero
  requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.add('is-ready'); }); });

  // Cabeçalho sólido ao fazer scroll
  var hdr = d.querySelector('[data-hdr]');
  function onScroll() {
    if (hdr) hdr.classList.toggle('is-solid', window.scrollY > 60);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Menu móvel
  var burger = d.querySelector('.burger'), nav = d.getElementById('nav');
  if (burger && nav) {
    function setMenu(open) {
      burger.setAttribute('aria-expanded', open);
      nav.classList.toggle('is-open', open);
      d.body.style.overflow = open ? 'hidden' : '';
      burger.querySelector('.sr').textContent = open ? burger.dataset.close : burger.dataset.open;
    }
    burger.addEventListener('click', function () { setMenu(burger.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (ev) { if (ev.target.closest('a')) setMenu(false); });
    d.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') setMenu(false); });
  }

  // Menu de línguas: fechar ao clicar fora
  d.addEventListener('click', function (ev) {
    d.querySelectorAll('details.lang[open]').forEach(function (el) { if (!el.contains(ev.target)) el.removeAttribute('open'); });
  });

  // Revelação ao entrar no ecrã, com escalonamento por grupo
  var items = [].slice.call(d.querySelectorAll('[data-r]'));
  if (!('IntersectionObserver' in window) || reduce) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      var batch = entries.filter(function (en) { return en.isIntersecting; });
      batch.forEach(function (en, i) {
        en.target.style.setProperty('--d', Math.min(i * 0.07, 0.42) + 's');
        en.target.classList.add('is-in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  // Processo: a barra laranja avança passo a passo
  var steps = d.querySelector('[data-steps]');
  if (steps) {
    var lis = [].slice.call(steps.querySelectorAll('[data-step]')), bar = steps.querySelector('.steps__bar');
    function light(n) {
      lis.forEach(function (li, i) { li.classList.toggle('is-on', i < n); });
      if (bar) bar.style.width = (n / lis.length * 100) + '%';
    }
    light(1);
    if (reduce || !('IntersectionObserver' in window)) { light(lis.length); }
    else {
      var so = new IntersectionObserver(function (en) {
        if (!en[0].isIntersecting) return;
        so.disconnect();
        var n = 1;
        var timer = setInterval(function () { n++; light(n); if (n >= lis.length) clearInterval(timer); }, 420);
      }, { threshold: 0.5 });
      so.observe(steps);
    }
  }

  // Paralaxe suave nas fotografias de fundo
  var px = [].slice.call(d.querySelectorAll('[data-parallax]'));
  if (px.length && !reduce) {
    var ticking = false;
    function move() {
      var vh = window.innerHeight;
      px.forEach(function (el) {
        var r = el.parentNode.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        var p = (r.top + r.height / 2 - vh / 2) / vh;
        var amp = el.dataset.parallax === 'strong' ? 0.15 : 0.04;
        el.style.transform = 'translate3d(0,' + (p * -amp * r.height * 2).toFixed(1) + 'px,0)';
      });
      ticking = false;
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(move); } }, { passive: true });
    move();
  }

  // Formulário de orçamento: abre o programa de e-mail com o pedido escrito
  var form = d.querySelector('[data-form]');
  if (form) {
    var M = JSON.parse(form.querySelector('[data-msgs]').textContent);
    var consent = form.querySelector('[data-consent]'), submit = form.querySelector('[data-submit]'), msg = form.querySelector('[data-msg]');
    function sync() {
      submit.disabled = !consent.checked;
      submit.textContent = consent.checked ? M.f_send : M.f_locked;
    }
    consent.addEventListener('change', sync);
    sync();
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var f = form.elements;
      if (!f.nome.value.trim() || !f.descricao.value.trim()) {
        msg.textContent = M.f_need;
        (f.nome.value.trim() ? f.descricao : f.nome).focus();
        return;
      }
      var svc = [].slice.call(form.querySelectorAll('input[name=servico]:checked')).map(function (i) { return i.value; }).join(', ');
      var body = [
        M.f_l_service + ': ' + (svc || '-'),
        M.f_l_material + ': ' + f.material.value,
        M.f_l_country + ': ' + f.pais.value,
        '',
        f.descricao.value.trim(),
        '',
        M.f_l_name + ': ' + f.nome.value.trim(),
        M.f_l_company + ': ' + (f.empresa.value.trim() || '-')
      ].join('\n');
      var subject = M.f_subject + ' — ' + (svc.split(',')[0] || 'STMetal');
      window.location.href = 'mailto:' + form.dataset.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      msg.textContent = M.f_done;
    });
  }
})();
