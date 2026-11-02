/* The owner banner is generated from actual library/class membership. */
(function () {
  window.$docsify.plugins.push(function (hook) {
    hook.afterEach(function (html) {
      var match = html.match(/class="module-banner family-(toolkit|builder|service|handler)"/);
      if (!match) return html;
      // Keep breadcrumbs and the banner outside the article styling, like search navigation.
      var end = html.indexOf('</div>', html.indexOf('class="module-banner')) + 6;
      return html.slice(0, end) + '<div class="module-content family-' + match[1] + '">' + html.slice(end) + '</div>';
    });
  });
})();
