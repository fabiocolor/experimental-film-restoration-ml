/* Site behaviour. Everything here is optional: without JavaScript every figure
   stays side by side and every video plays on its own.

   1. Compare mode on figure pairs (.pair-media[data-compare]): a wipe between the
      source and the result, dragged with the pointer or the arrow keys.
   2. Video pairs (.pair-media[data-sync]): play, pause and seek both players together.
   3. Reveal videos marked data-autoplay start when they scroll into view and pause when they
      leave it, so a page with several of them only downloads the ones being looked at.
   4. "Look at a frame" on side-by-side videos (.pair-video[data-inspect]): swaps the video for
      a full-size still pair of the same shot, in compare mode, and back. */
(function () {
  'use strict';

  function compare(media, startOn) {
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
    if (startOn) {
      var pending = Array.prototype.filter.call(imgs, function (im) { return !im.complete; });
      if (!pending.length) enable();
      else pending.forEach(function (im) { im.addEventListener('load', function () { if (!on && Array.prototype.every.call(imgs, function (x) { return x.complete; })) enable(); }); });
    }

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

  function lazyPlay() {
    var vids = document.querySelectorAll('video[data-autoplay]');
    if (!vids.length) return;
    if (!('IntersectionObserver' in window)) {
      vids.forEach(function (v) { v.preload = 'auto'; v.play().catch(function () {}); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) { v.preload = 'auto'; v.play().catch(function () {}); }
        else if (!v.paused) v.pause();
      });
    }, { rootMargin: '200px 0px' });
    vids.forEach(function (v) { io.observe(v); });
  }

  function inspect(media) {
    var video = media.querySelector('video');
    if (!video) return;
    var slug = media.getAttribute('data-inspect');
    var frames = (media.getAttribute('data-frames') || 'b').split(',');
    var base = (window.siteBase || '') + '/images_kebab/examples/';
    var figure = media.closest('figure');
    var labelRow = figure && figure.querySelector('.pair-labels');
    var labels = labelRow ? Array.prototype.map.call(labelRow.querySelectorAll('span'), function (s) { return s.textContent; }) : ['Source', 'Result'];
    var tools = document.createElement('div');
    tools.className = 'pair-tools pair-tools-inspect';
    var toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.textContent = 'Look at a frame';
    toggle.setAttribute('aria-pressed', 'false');
    tools.appendChild(toggle);
    media.insertAdjacentElement('afterend', tools);

    var still = null, pickers = [], current = frames.length > 1 ? frames[1] : frames[0];

    function file(frame, kind) {
      var sep = /^[a-z]/.test(frame) ? '-' : '';
      return base + slug + sep + frame + '-' + kind + '.jpg';
    }

    function show(frame) {
      current = frame;
      if (still) still.remove();
      still = document.createElement('div');
      still.className = 'pair-media';
      still.setAttribute('data-compare', labels.join('|'));
      ['source', 'result'].forEach(function (kind, i) {
        var im = document.createElement('img');
        im.src = file(frame, kind);
        im.alt = (labels[i] || kind) + ', one frame of the shot at full size';
        still.appendChild(im);
      });
      media.insertAdjacentElement('afterend', still);
      compare(still, true);
      var own = still.nextElementSibling;   // the still's own Compare button: the wipe stays on while inspecting
      if (own && own.classList.contains('pair-tools') && own !== tools) own.remove();
      pickers.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-frame') === frame ? 'true' : 'false'); });
    }

    function open() {
      if (!video.paused) video.pause();
      media.hidden = true;
      if (frames.length > 1 && !pickers.length) {
        frames.forEach(function (fr, i) {
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'frame-pick';
          b.setAttribute('data-frame', fr);
          b.textContent = /^[a-z]/.test(fr) ? 'Frame ' + (i + 1) : 'Frame ' + fr;
          b.addEventListener('click', function () { show(fr); });
          tools.insertBefore(b, toggle);
          pickers.push(b);
        });
      }
      pickers.forEach(function (b) { b.hidden = false; });
      show(current);
      toggle.textContent = 'Back to the video';
      toggle.setAttribute('aria-pressed', 'true');
    }

    function close() {
      if (still) { still.remove(); still = null; }
      pickers.forEach(function (b) { b.hidden = true; });
      media.hidden = false;
      toggle.textContent = 'Look at a frame';
      toggle.setAttribute('aria-pressed', 'false');
    }

    toggle.addEventListener('click', function () { still ? close() : open(); });
  }

  function init() {
    document.querySelectorAll('.pair-media[data-compare]').forEach(function (m) { compare(m, false); });
    document.querySelectorAll('.pair-media[data-sync]').forEach(sync);
    document.querySelectorAll('.pair-video[data-inspect]').forEach(inspect);
    lazyPlay();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
