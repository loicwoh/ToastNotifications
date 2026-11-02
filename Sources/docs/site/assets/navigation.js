/* Keep Docsify's own toggle; synchronize accessibility and mobile drawer behavior. */
(function () {
  window.$docsify.plugins.push(function (hook) {
    var installed = false;
    hook.doneEach(function () {
      var sidebar = document.querySelector('.sidebar');
      var toggle = document.querySelector('.sidebar-toggle');
      var content = document.querySelector('.markdown-section');
      if (!sidebar || !toggle || !content) return;
      content.id = 'main-content';
      content.setAttribute('tabindex', '-1');
      if (installed) return;
      installed = true;
      var mobile = window.matchMedia('(max-width: 768px)');
      sidebar.id = 'documentation-navigation';
      sidebar.setAttribute('aria-label', 'Documentation navigation');
      toggle.setAttribute('aria-controls', sidebar.id);
      var backdrop = document.createElement('button');
      backdrop.className = 'menu-backdrop';
      backdrop.setAttribute('aria-label', 'Close navigation');
      backdrop.setAttribute('tabindex', '-1');
      document.body.appendChild(backdrop);
      function isOpen() { return mobile.matches === document.body.classList.contains('close'); }
      function sync() {
        var open = isOpen();
        toggle.setAttribute('aria-expanded', String(open));
        toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
        sidebar.inert = !open;
        sidebar.setAttribute('aria-hidden', String(!open));
        // A mobile drawer is modal below the toolbar: retain access to version/toggle.
        document.querySelector('.content').inert = mobile.matches && open;
      }
      function close(restoreFocus) {
        document.body.classList.toggle('close', !mobile.matches);
        sync();
        if (restoreFocus) toggle.focus();
      }
      new MutationObserver(sync).observe(document.body, { attributes: true, attributeFilter: ['class'] });
      mobile.addEventListener('change', function () { document.body.classList.remove('close'); sync(); });
      document.querySelector('.skip-link').addEventListener('click', function (event) {
        event.preventDefault();
        if (mobile.matches) close(false);
        content.focus({ preventScroll: true });
        window.scrollTo(0, 0);
      });
      backdrop.addEventListener('click', function () { close(true); });
      sidebar.addEventListener('click', function (event) {
        if (mobile.matches && event.target.closest('a')) {
          close(false);
          content.focus({ preventScroll: true });
        }
      });
      document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && mobile.matches && isOpen()) {
          event.preventDefault(); close(true);
        }
      });
      sync();
    });
  });
})();
