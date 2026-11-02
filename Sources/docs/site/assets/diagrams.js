/* Render authored Mermaid fences after each Docsify navigation. */
(function () {
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'strict',
    theme: 'neutral',
    layout: 'dagre',
    fontFamily: 'Segoe UI, sans-serif',
    flowchart: { htmlLabels: false }
  });
  var pending = Promise.resolve();
  window.$docsify.plugins.push(function (hook) {
    hook.doneEach(function () {
      var nodes = [];
      document.querySelectorAll('.markdown-section pre > code.lang-mermaid').forEach(function (code) {
        var diagram = document.createElement('div');
        diagram.className = 'mermaid';
        diagram.textContent = code.textContent;
        code.parentElement.replaceWith(diagram);
        nodes.push(diagram);
      });
      if (nodes.length) {
        pending = pending.then(function () { return mermaid.run({ nodes: nodes }); }).catch(function (error) {
          console.error('Documentation diagram rendering failed', error);
        });
      }
    });
  });
})();
