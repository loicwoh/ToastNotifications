/* A shared manifest is installed alongside each version during the Pages build. */
(function () {
  'use strict';
  fetch('versions.json', {cache: 'no-store'}).then(function (response) {
    if (!response.ok) return null;
    return response.json();
  }).then(function (manifest) {
    if (!manifest) return;
    var label = document.createElement('label');
    label.className = 'version-picker';
    label.textContent = 'Documentation version ';
    var select = document.createElement('select');
    select.setAttribute('aria-label', 'Documentation version');
    manifest.versions.forEach(function (version) {
      var option = document.createElement('option');
      option.value = version.path;
      option.textContent = version.label + ' · ' + version.commit.slice(0, 7);
      option.selected = version.id === manifest.current;
      select.appendChild(option);
    });
    select.addEventListener('change', function () {
      window.location.href = select.value + (window.location.hash || '#/');
    });
    label.appendChild(select);
    document.body.appendChild(label);
  }).catch(function () { /* A local single-version preview has no manifest. */ });
}());
