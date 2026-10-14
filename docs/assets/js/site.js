/* Site behaviour. Everything here is optional: without JavaScript every figure
   stays side by side and every video plays on its own.

   1. Compare mode on figure pairs (.pair-media[data-compare]): a wipe between the
      source and the result, dragged with the pointer or the arrow keys.
   2. Video pairs (.pair-media[data-sync]): play, pause and seek both players together. */
(function () {
  'use strict';

  function compare(media) {
    var imgs = media.querySelectorAll('img');
    if (imgs.length !== 2) return;
    // The browser's own image drag would take over the pointer; turn it off for the pair.
    imgs.forEach(function (im) { im.draggable = false; im.addEventListener('dragstart', function (e) { e.preventDefault(); }); });
    var figure = media.closest('figure');
    var labels = media.getAttribute('data-compare').split('|');
    if (figure && !figure.querySelector('.pair-labels')) {
      var row = document.createElement('span');
      row.className = 'pair-labels';
      labels.forEach(function (t) { var s = document.createElement('span'); s.textContent = t; row.appendChild(s); });
      media.insertAdjacentElement('beforebegin', row);
    }
    var tools = document.createElement('div');
    tools.className = 'pair-tools';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = 'Compare';
    btn.setAttribute('aria-pressed', 'false');
    tools.appendChild(btn);
    media.insertAdjacentElement('afterend', tools);

    var handle, labelA, labelB, on = false;

    function setWipe(fraction) {
      fraction = Math.min(1, Math.max(0, fraction));
      media.style.setProperty('--wipe', (fraction * 100).toFixed(2) + '%');
    }

    function fromEvent(e) {
      var r = media.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      setWipe(x / r.width);
    }

    function enable() {
      on = true;
      media.classList.add('is-compare');
      media.setAttribute('tabindex', '0');
      media.setAttribute('role', 'slider');
      media.setAttribute('aria-label', 'Wipe between ' + (labels[0] || 'source') + ' and ' + (labels[1] || 'result'));
      media.setAttribute('aria-valuemin', '0');
      media.setAttribute('aria-valuemax', '100');
      // Fix the height to the side-by-side rendering so the frame doesn't jump
      var h = imgs[0].getBoundingClientRect().height;
      if (h) media.style.height = h + 'px';
      handle = document.createElement('div');
      handle.className = 'wipe-handle';
      labelA = document.createElement('span');
      labelA.className = 'wipe-label wipe-label-a';
      labelA.textContent = labels[0] || 'Source';
      labelB = document.createElement('span');
      labelB.className = 'wipe-label wipe-label-b';
      labelB.textContent = labels[1] || 'Result';
      media.appendChild(handle);
      media.appendChild(labelA);
      media.appendChild(labelB);
      setWipe(0.5);
      btn.setAttribute('aria-pressed', 'true');
      btn.textContent = 'Side by side';
    }

    function disable() {
      on = false;
      media.classList.remove('is-compare');
      media.removeAttribute('tabindex');
      media.removeAttribute('role');
      media.style.height = '';
      [handle, labelA, labelB].forEach(function (el) { if (el) el.remove(); });
      btn.setAttribute('aria-pressed', 'false');
      btn.textContent = 'Compare';
    }

    btn.addEventListener('click', function () { on ? disable() : enable(); });

    var dragging = false;
    media.addEventListener('pointerdown', function (e) {
      if (!on) return;
      e.preventDefault();
      dragging = true;
      media.setPointerCapture(e.pointerId);
      fromEvent(e);
    });
    media.addEventListener('pointermove', function (e) { if (on && dragging) fromEvent(e); });
    media.addEventListener('pointerup', function () { dragging = false; });
    media.addEventListener('pointercancel', function () { dragging = false; });
    media.addEventListener('keydown', function (e) {
      if (!on) return;
      var cur = parseFloat(media.style.getPropertyValue('--wipe')) || 50;
      if (e.key === 'ArrowLeft') { setWipe((cur - 2) / 100); e.preventDefault(); }
      if (e.key === 'ArrowRight') { setWipe((cur + 2) / 100); e.preventDefault(); }
    });
    window.addEventListener('resize', function () {
      if (!on) return;
      media.style.height = '';
      var h = imgs[0].getBoundingClientRect().height;
      if (h) media.style.height = h + 'px';
    });
  }

  function sync(media) {
    var vids = media.querySelectorAll('video');
    if (vids.length < 2) return;
    var lock = false;
    vids.forEach(function (v) {
      v.addEventListener('play', function () {
        if (lock) return; lock = true;
        vids.forEach(function (o) { if (o !== v) { o.currentTime = v.currentTime; o.play().catch(function () {}); } });
        lock = false;
      });
      v.addEventListener('pause', function () {
        if (lock) return; lock = true;
        vids.forEach(function (o) { if (o !== v && !o.paused) o.pause(); });
        lock = false;
      });
      v.addEventListener('seeked', function () {
        if (lock) return; lock = true;
        vids.forEach(function (o) { if (o !== v && Math.abs(o.currentTime - v.currentTime) > 0.05) o.currentTime = v.currentTime; });
        lock = false;
      });
    });
  }

  function init() {
    document.querySelectorAll('.pair-media[data-compare]').forEach(compare);
    document.querySelectorAll('.pair-media[data-sync]').forEach(sync);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
