/**
 * Kerala Master Plan Viewer — main.js
 *
 * Displays Cloud Optimized GeoTIFFs (COGs) and XYZ tiles on an OpenLayers map
 * for all Kerala cities and towns. Built for Kerala First.
 */
(function () {
  'use strict';

  // ── Shared state ─────────────────────────────────────
  var map, cogLayer, basemapLayer, locationLayer, locationFeature;
  var satLayer;
  var swipeX;
  var swipeY;
  var currentTheme = 'light';
  var currentCity = null;
  var suggestionsLayer;
  var loadSuggestionsForCity;
  var cancelActiveFeedback;

  // ── Menu open / close helpers ────────────────────────
  var _menuOpenTimer = null;

  function openMenu() {
    var mc = document.getElementById('menu-content');
    if (!mc) return;
    clearTimeout(_menuOpenTimer);
    mc.style.overflow = 'hidden';
    mc.classList.remove('hidden');
    _menuOpenTimer = setTimeout(function () {
      if (!mc.classList.contains('hidden')) { mc.style.overflow = ''; }
    }, 320);
  }

  function closeMenu() {
    var mc = document.getElementById('menu-content');
    if (!mc || mc.classList.contains('hidden')) return;
    clearTimeout(_menuOpenTimer);
    mc.style.overflow = 'hidden';
    mc.classList.add('hidden');
  }

  // ── Bootstrap ────────────────────────────────────────
  fetch('cities.json')
    .then(function (res) { return res.json(); })
    .then(function (data) { init(data.cities); })
    .catch(function (err) { console.error('Failed to load cities.json:', err); });

  // ── Initialisation ───────────────────────────────────
  function init(cities) {
    setupThemeToggle();

    var IndiaBoundaryCorrectedTileLayer = IndiaBoundaryCorrector.IndiaBoundaryCorrectedTileLayer;
    
    basemapLayer = new IndiaBoundaryCorrectedTileLayer({
      url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      sourceOptions: {
        attributions: '© OpenStreetMap contributors',
        crossOrigin: 'anonymous'
      }
    });

    satLayer = new ol.layer.Tile({
      source: new ol.source.XYZ({
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        maxZoom: 19,
        attributions: 'Tiles &copy; Esri',
        crossOrigin: 'anonymous'
      }),
      visible: false
    });

    window.satLayer = satLayer;

    cogLayer = new ol.layer.WebGLTile();

    locationFeature = new ol.Feature({
      geometry: new ol.geom.Point(ol.proj.fromLonLat([76.2711, 10.8505]))
    });
    locationFeature.setStyle(createLocationStyle());

    locationLayer = new ol.layer.Vector({
      source: new ol.source.Vector({
        features: [locationFeature]
      }),
      zIndex: 1000
    });
    locationFeature.setGeometry(null);

    map = new ol.Map({
      target: 'map',
      layers: [basemapLayer, satLayer, cogLayer, locationLayer],
      controls: ol.control.defaults.defaults({ zoom: false }),
      view: new ol.View({
        center: ol.proj.fromLonLat([76.2711, 10.8505]),
        zoom: 8
      })
    });

    setupCitySelector(cities);
    setupAddressSearch();
    setupGeolocation();
    setupInfoModal();
    setupOpacitySlider();
    setupBasemapToggle();
    setupSwipe();
    setupMenuToggle();
    setupFeedback();
    setupSubmitPlan();

    function closeMenuOnInput() { closeMenu(); }
    var mapViewport = map.getViewport();
    mapViewport.addEventListener('pointerdown', closeMenuOnInput);
    mapViewport.addEventListener('wheel', closeMenuOnInput, { passive: true });
  }

  // ── 1. City Selector ─────────────────────────────────
  function setupCitySelector(cities) {
    var input = document.getElementById('city-search');
    var clearBtn = document.getElementById('city-search-clear');
    var resultsList = document.getElementById('city-results');
    var debounceTimer = null;
    var activeIndex = -1;
    var filteredCities = [];

    function closeResults() {
      resultsList.classList.remove('open');
      resultsList.innerHTML = '';
      activeIndex = -1;
    }

    function updateClearButton() {
      clearBtn.classList.toggle('visible', !!input.value);
    }

    function clearSearch() {
      clearTimeout(debounceTimer);
      input.value = '';
      updateClearButton();
      closeResults();
      input.focus();
    }

    function renderResults(items) {
      resultsList.innerHTML = '';
      activeIndex = -1;
      filteredCities = items;

      if (!items.length) {
        var empty = document.createElement('li');
        empty.className = 'no-results';
        empty.textContent = 'No cities found';
        resultsList.appendChild(empty);
      } else {
        items.forEach(function (city, index) {
          var li = document.createElement('li');
          var hasData = !!(city.cogUrl || city.xyzUrl);
          li.innerHTML = city.name + ' <span class="data-badge ' + (hasData ? 'available' : 'pending') + '">' + (hasData ? 'PLAN' : 'NO DATA') + '</span>';
          li.setAttribute('role', 'option');
          li.addEventListener('mousedown', function (e) {
            e.preventDefault();
            selectCity(city);
          });
          resultsList.appendChild(li);
        });
      }

      resultsList.classList.add('open');
    }

    function filterCities(query) {
      var normalized = query.trim().toLowerCase();
      var sorted = cities.slice().sort(function (a, b) {
        return a.name.localeCompare(b.name);
      });

      if (!normalized) {
        return sorted;
      }

      return sorted.filter(function (city) {
        return city.name.toLowerCase().indexOf(normalized) !== -1;
      });
    }

    function search(query) {
      renderResults(filterCities(query));
    }

    function selectCity(city) {
      input.value = city.name;
      updateClearButton();
      closeResults();
      input.blur();
      loadCity(city);
    }

    closeResults();

    input.addEventListener('focus', function () {
      search(input.value);
    });

    input.addEventListener('input', function () {
      updateClearButton();
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () { search(input.value); }, 150);
    });

    clearBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      clearSearch();
    });

    updateClearButton();

    input.addEventListener('keydown', function (e) {
      var items = resultsList.querySelectorAll('li:not(.no-results)');
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIndex = Math.min(activeIndex + 1, items.length - 1);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIndex = Math.max(activeIndex - 1, 0);
      } else if (e.key === 'Enter') {
        if (activeIndex >= 0 && filteredCities[activeIndex]) {
          selectCity(filteredCities[activeIndex]);
        } else if (filteredCities.length === 1) {
          selectCity(filteredCities[0]);
        }
        return;
      } else if (e.key === 'Escape') {
        closeResults();
        return;
      }

      items.forEach(function (li, i) {
        li.setAttribute('aria-selected', i === activeIndex ? 'true' : 'false');
      });
    });

    document.addEventListener('click', function (e) {
      if (!document.getElementById('city-search-wrapper').contains(e.target)) {
        closeResults();
      }
    });

    function loadCity(city) {
      currentCity = city.name;
      if (cancelActiveFeedback) { cancelActiveFeedback(); }
      var ct = document.getElementById('comments-toggle');
      if (ct) { ct.classList.remove('no-city'); }
      
      var hasData = !!(city.cogUrl || city.xyzUrl);
      
      // Remove any existing proxy layer
      removeProxyLayer();
      hideLegend();

      if (hasData) {
        // Official plan available
        var source;
        if (city.xyzUrl) {
          source = new ol.source.XYZ({
            url: city.xyzUrl,
            crossOrigin: 'anonymous'
          });
        } else {
          source = new ol.source.GeoTIFF({
            sources: [{ url: city.cogUrl }],
            interpolate: true,
            normalize: true,
            wrapX: false
          });
        }

        cogLayer.setSource(source);
        if (city.extent) {
          cogLayer.setExtent(city.extent);
        } else {
          cogLayer.setExtent(undefined);
        }
        cogLayer.setOpacity(parseFloat(document.getElementById('opacity-slider').value));
        cogLayer.setVisible(true);
        updateDataSourceIndicator('official', 'Official Master Plan');
      } else {
        // No official plan — load proxy layer
        cogLayer.setSource(null);
        cogLayer.setVisible(false);
        loadProxyLayer(city);
        updateDataSourceIndicator('proxy', 'Current Land Use (Proxy)');
      }

      map.setView(new ol.View({
        center: ol.proj.fromLonLat(city.center),
        zoom: city.zoom,
        minZoom: 4,
        maxZoom: 20,
        projection: 'EPSG:3857'
      }));

      if (loadSuggestionsForCity) { loadSuggestionsForCity(city.name); }
    }
  }

  // ── Proxy Layer Management ───────────────────────────
  var proxyLayer = null;

  function loadProxyLayer(city) {
    if (!window.KeralaProxyLayer) return;
    
    window.KeralaProxyLayer.load(city, function(layer) {
      proxyLayer = layer;
      map.addLayer(proxyLayer);
      showLegend();
      showNoDataToast(city.name + ' — showing proxy data');
    }, function(err) {
      console.error('Proxy layer failed:', err);
      updateDataSourceIndicator('none', 'No data available');
    });
  }

  function removeProxyLayer() {
    if (proxyLayer) {
      map.removeLayer(proxyLayer);
      proxyLayer = null;
    }
  }

  function updateDataSourceIndicator(type, text) {
    var badge = document.getElementById('data-source-badge');
    if (!badge) return;
    badge.textContent = text;
    badge.className = type;
  }

  function showLegend() {
    var panel = document.getElementById('legend-panel');
    var content = document.getElementById('legend-content');
    if (!panel || !content) return;
    
    if (!window.KeralaProxyLayer) return;
    var legend = window.KeralaProxyLayer.getLegend();
    
    var html = '';
    var currentSection = '';
    legend.categories.forEach(function(cat) {
      var section = cat.label.indexOf('Building') !== -1 ? 'Buildings' :
                    cat.label.indexOf('Area') !== -1 ? 'Land Use' :
                    cat.label.indexOf('Road') !== -1 ? 'Roads' :
                    cat.label.indexOf('Water') !== -1 ? 'Water' :
                    cat.label.indexOf('Rail') !== -1 ? 'Transport' :
                    cat.label.indexOf('Park') !== -1 ? 'Green Space' :
                    cat.label.indexOf('School') !== -1 ? 'Public' :
                    cat.label.indexOf('Hospital') !== -1 ? 'Public' :
                    'Other';
      
      if (section !== currentSection) {
        html += '<div class="legend-section">' + section + '</div>';
        currentSection = section;
      }
      
      html += '<div class="legend-item">' +
        '<div class="legend-color" style="background:' + cat.color + '"></div>' +
        '<span>' + cat.label + '</span>' +
        '</div>';
    });
    
    html += '<div class="legend-note">Data from OpenStreetMap contributors. This shows current land use, not official planning data.</div>';
    
    content.innerHTML = html;
    panel.classList.add('open');
  }

  function hideLegend() {
    var panel = document.getElementById('legend-panel');
    if (panel) panel.classList.remove('open');
  }

  // Legend toggle
  document.addEventListener('DOMContentLoaded', function() {
    var legendToggle = document.getElementById('legend-toggle');
    var legendContent = document.getElementById('legend-content');
    if (legendToggle && legendContent) {
      legendToggle.addEventListener('click', function() {
        legendContent.classList.toggle('collapsed');
        legendToggle.textContent = legendContent.classList.contains('collapsed') ? '+' : '−';
      });
    }
  });

  function showNoDataToast(cityName) {
    var toast = document.getElementById('no-data-toast');
    if (!toast) return;
    toast.textContent = 'No master plan data yet for ' + cityName;
    toast.classList.add('visible');
    clearTimeout(window._noDataToastTimer);
    window._noDataToastTimer = setTimeout(function () {
      toast.classList.remove('visible');
    }, 2500);
  }

  // ── 2. Address Search (Nominatim) ───────────────────
  function setupAddressSearch() {
    var input = document.getElementById('address-search');
    var clearBtn = document.getElementById('address-search-clear');
    var resultsList = document.getElementById('search-results');
    var debounceTimer = null;
    var activeIndex = -1;

    function closeResults() {
      resultsList.classList.remove('open');
      resultsList.innerHTML = '';
      activeIndex = -1;
    }

    function updateClearButton() {
      clearBtn.classList.toggle('visible', !!input.value);
    }

    function clearSearch() {
      clearTimeout(debounceTimer);
      input.value = '';
      updateClearButton();
      closeResults();
      input.focus();
    }

    function renderResults(items) {
      resultsList.innerHTML = '';
      activeIndex = -1;
      if (!items.length) {
        var li = document.createElement('li');
        li.className = 'no-results';
        li.textContent = 'No results found';
        resultsList.appendChild(li);
      } else {
        items.forEach(function (item) {
          var li = document.createElement('li');
          li.textContent = item.display_name;
          li.setAttribute('role', 'option');
          li.addEventListener('mousedown', function (e) {
            e.preventDefault();
            selectResult(item);
          });
          resultsList.appendChild(li);
        });
      }
      resultsList.classList.add('open');
    }

    function selectResult(item) {
      input.value = item.display_name;
      updateClearButton();
      closeResults();
      input.blur();
      var bbox = item.boundingbox;
      var extent = ol.proj.transformExtent(
        [parseFloat(bbox[2]), parseFloat(bbox[0]), parseFloat(bbox[3]), parseFloat(bbox[1])],
        'EPSG:4326',
        'EPSG:3857'
      );
      map.getView().fit(extent, { duration: 600, maxZoom: 17 });
    }

    function search(query) {
      if (!query.trim()) { closeResults(); return; }
      fetch(
        'https://nominatim.openstreetmap.org/search?q=' +
        encodeURIComponent(query) +
        '&format=json&limit=5&addressdetails=0',
        { headers: { 'Accept-Language': 'en' } }
      )
        .then(function (res) { return res.json(); })
        .then(function (data) { renderResults(data); })
        .catch(function () { closeResults(); });
    }

    input.addEventListener('input', function () {
      updateClearButton();
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () { search(input.value); }, 350);
    });

    clearBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      clearSearch();
    });

    updateClearButton();

    input.addEventListener('keydown', function (e) {
      var items = resultsList.querySelectorAll('li:not(.no-results)');
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIndex = Math.min(activeIndex + 1, items.length - 1);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIndex = Math.max(activeIndex - 1, 0);
      } else if (e.key === 'Enter') {
        if (activeIndex >= 0 && items[activeIndex]) {
          items[activeIndex].dispatchEvent(new MouseEvent('mousedown'));
        }
        return;
      } else if (e.key === 'Escape') {
        closeResults();
        return;
      }
      items.forEach(function (li, i) {
        li.setAttribute('aria-selected', i === activeIndex ? 'true' : 'false');
      });
    });

    document.addEventListener('click', function (e) {
      if (!document.getElementById('search-wrapper').contains(e.target)) {
        closeResults();
      }
    });
  }

  // ── 3. User Geolocation ─────────────────
  function setupGeolocation() {
    document.getElementById('geolocate-btn').addEventListener('click', function () {
      if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser.');
        return;
      }
      navigator.geolocation.getCurrentPosition(
        function (pos) {
          var locationCoords = ol.proj.fromLonLat([pos.coords.longitude, pos.coords.latitude]);

          locationFeature.setGeometry(new ol.geom.Point(locationCoords));
          locationLayer.setVisible(true);

          map.getView().animate({
            center: locationCoords,
            zoom: 14,
            duration: 1500
          });
        },
        function (err) {
          alert('Geolocation failed: ' + err.message);
        }
      );
    });
  }

  function createLocationStyle() {
    var circleSvg = [
      '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40">',
      '<circle cx="20" cy="20" r="10" fill="#1a73e8" stroke="#ffffff" stroke-width="4"/>',
      '</svg>'
    ].join('');

    return new ol.style.Style({
      image: new ol.style.Icon({
        src: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(circleSvg),
        anchor: [0.5, 0.5],
        anchorXUnits: 'fraction',
        anchorYUnits: 'fraction',
        scale: 1
      })
    });
  }

  // ── 3.5. Info Modal ─────────────────────────────────
  function setupInfoModal() {
    var infoBtn = document.getElementById('info-btn');
    var modal = document.getElementById('info-modal');
    var closeBtn = document.getElementById('modal-close');

    infoBtn.addEventListener('click', function () {
      modal.classList.add('open');
    });

    closeBtn.addEventListener('click', function () {
      modal.classList.remove('open');
    });

    modal.addEventListener('click', function (e) {
      if (e.target === modal) {
        modal.classList.remove('open');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) {
        modal.classList.remove('open');
      }
    });
  }

  // ── 4. Opacity Slider ────────────────────────────────
  function setupOpacitySlider() {
    document.getElementById('opacity-slider').addEventListener('input', function (e) {
      cogLayer.setOpacity(parseFloat(e.target.value));
    });
  }

  // ── 5. Basemap Toggle ────────────────────────────────
  function setupBasemapToggle() {
    var toggleBtn = document.getElementById('basemap-toggle-btn');
    var isOsm = true;

    toggleBtn.textContent = '🛰️';
    toggleBtn.title = 'Switch to Satellite';

    toggleBtn.addEventListener('click', function () {
      isOsm = !isOsm;
      if (isOsm) {
        basemapLayer.setVisible(true);
        satLayer.setVisible(false);
        toggleBtn.textContent = '🛰️';
        toggleBtn.title = 'Switch to Satellite';
      } else {
        basemapLayer.setVisible(false);
        satLayer.setVisible(true);
        toggleBtn.textContent = '🗺️';
        toggleBtn.title = 'Switch to Street Map';
      }
    });
  }

  // ── 5. Theme Toggle ─────────────────────────────────
  function setupThemeToggle() {
    var toggleBtn = document.getElementById('theme-toggle');

    currentTheme = 'light';

    function applyBasemapFilter(theme) {
      if (!map) return;
      var viewport = map.getViewport();
      if (viewport) {
        if (theme === 'dark') {
          viewport.style.filter = 'invert(0.9) brightness(1.05) contrast(1.05) hue-rotate(180deg)';
        } else {
          viewport.style.filter = 'none';
        }
      }
    }

    function applyTheme(theme) {
      currentTheme = theme;
      document.body.setAttribute('data-theme', theme);
      toggleBtn.textContent = theme === 'dark' ? '☀️' : '🌙';
      toggleBtn.title = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
      applyBasemapFilter(theme);
    }

    setTimeout(function() {
      applyTheme(currentTheme);
    }, 100);

    toggleBtn.addEventListener('click', function () {
      applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });
  }

  // ── 6. Menu Toggle ───────────────────────────────────
  function setupMenuToggle() {
    var toggleBtn = document.getElementById('menu-toggle');
    var menuContent = document.getElementById('menu-content');

    toggleBtn.addEventListener('click', function () {
      if (menuContent.classList.contains('hidden')) { openMenu(); } else { closeMenu(); }
    });
  }

  // ── 7. Swipe Compare ────────────────────────────────
  function setupSwipe() {
    var handle = document.getElementById('swipe-handle');
    var mapEl = document.getElementById('map');
    var dragging = false;
    var swipeEnabled = true;
    var cogCanvas = null;

    function isPortrait() {
      return mapEl.clientHeight > mapEl.clientWidth * 1.01;
    }

    function applyClip() {
      if (!cogCanvas || !swipeEnabled) {
        if (cogCanvas) cogCanvas.style.clipPath = 'none';
        return;
      }
      if (isPortrait()) {
        cogCanvas.style.clipPath =
          'inset(0 0 ' + (mapEl.clientHeight - swipeY) + 'px 0)';
      } else {
        cogCanvas.style.clipPath =
          'inset(0 ' + (mapEl.clientWidth - swipeX) + 'px 0 0)';
      }
    }

    function initOrientation() {
      if (isPortrait()) {
        handle.classList.add('portrait');
        swipeY = mapEl.clientHeight / 2;
        handle.style.top = swipeY + 'px';
        handle.style.left = '';
      } else {
        handle.classList.remove('portrait');
        swipeX = mapEl.clientWidth / 2;
        handle.style.left = swipeX + 'px';
        handle.style.top = '';
      }
      applyClip();
      map.render();
    }

    initOrientation();

    var toggleBtn = document.getElementById('swipe-toggle');
    toggleBtn.addEventListener('click', function () {
      swipeEnabled = !swipeEnabled;
      handle.style.display = swipeEnabled ? '' : 'none';
      toggleBtn.textContent = swipeEnabled ? '⇔ Swipe On' : '⇔ Swipe Off';
      toggleBtn.classList.toggle('active', swipeEnabled);
      applyClip();
      map.render();
    });

    handle.addEventListener('mousedown', function (e) {
      dragging = true;
      e.preventDefault();
    });

    window.addEventListener('mousemove', function (e) {
      if (!dragging) return;
      updateSwipe(e.clientX, e.clientY, mapEl);
    });

    window.addEventListener('mouseup', function () { dragging = false; });

    handle.addEventListener('touchstart', function (e) {
      dragging = true;
      e.preventDefault();
    }, { passive: false });

    window.addEventListener('touchmove', function (e) {
      if (!dragging) return;
      updateSwipe(e.touches[0].clientX, e.touches[0].clientY, mapEl);
    }, { passive: true });

    window.addEventListener('touchend', function () { dragging = false; });

    cogLayer.on('prerender', function (event) {
      if (!swipeEnabled) return;
      var gl = event.context;
      if (!gl || !gl.enable) return;
      var canvas = gl.canvas;
      gl.enable(gl.SCISSOR_TEST);
      if (isPortrait()) {
        var ratioH = canvas.height / mapEl.clientHeight;
        var physH = Math.round(swipeY * ratioH);
        gl.scissor(0, canvas.height - physH, canvas.width, physH);
      } else {
        var ratioW = canvas.width / mapEl.clientWidth;
        gl.scissor(0, 0, Math.round(swipeX * ratioW), canvas.height);
      }
    });

    cogLayer.on('postrender', function (event) {
      var gl = event.context;
      if (!gl || !gl.disable) return;
      gl.disable(gl.SCISSOR_TEST);
      cogCanvas = gl.canvas;
      applyClip();
    });

    window.addEventListener('resize', function () { initOrientation(); });
    window.addEventListener('orientationchange', function () {
      setTimeout(initOrientation, 100);
    });
  }

  function updateSwipe(clientX, clientY, mapEl) {
    var rect = mapEl.getBoundingClientRect();
    if (mapEl.clientHeight > mapEl.clientWidth * 1.01) {
      swipeY = Math.max(0, Math.min(clientY - rect.top, rect.height));
      document.getElementById('swipe-handle').style.top = swipeY + 'px';
    } else {
      swipeX = Math.max(0, Math.min(clientX - rect.left, rect.width));
      document.getElementById('swipe-handle').style.left = swipeX + 'px';
    }
    map.render();
  }

  // ── 8. Comments ───────────────────────────────────────
  function setupFeedback() {
    // NOTE: Replace with your own Supabase instance for production
    var SUPABASE_URL = 'https://rglaghcgwaxtugnphzil.supabase.co';
    var SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJnbGFnaGNnd2F4dHVnbnBoemlsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA4NDU1NzIsImV4cCI6MjA4NjQyMTU3Mn0.wjNeC-K0nxCIoYXC93nH_uAbyInxMExmTL0WSCAWswk';
    var sb;
    try {
      sb = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    } catch (e) {
      console.warn('Supabase not initialized:', e);
      sb = null;
    }

    var commentsVisible = false;
    var addCommentMode = false;
    var pendingCoord = null;
    var longPressTimer = null;
    var suppressNextClick = false;

    var toggleBtn      = document.getElementById('comments-toggle');
    var addCommentFab  = document.getElementById('add-comment-fab');
    var addCommentHint = document.getElementById('add-comment-hint');
    var contextMenu    = document.getElementById('comment-context-menu');
    var formModal    = document.getElementById('comment-form-modal');
    var formClose    = document.getElementById('comment-form-close');
    var nameInput    = document.getElementById('comment-name');
    var textArea     = document.getElementById('comment-text');
    var charCount    = document.getElementById('comment-char-count');
    var submitBtn    = document.getElementById('comment-submit');
    var cancelBtn    = document.getElementById('comment-cancel');
    var formStatus   = document.getElementById('comment-status');
    var popover      = document.getElementById('suggestion-popover');
    var popoverClose = document.getElementById('popover-close');
    var popoverContent = document.getElementById('popover-content');
    var mapViewport  = map.getViewport();

    var rawSource = new ol.source.Vector();
    var clusterSource = new ol.source.Cluster({ distance: 40, source: rawSource });

    suggestionsLayer = new ol.layer.Vector({
      source: clusterSource,
      visible: false,
      zIndex: 999,
      style: function (feature) {
        var features = feature.get('features') || [];
        var size = features.length;
        if (!size) { return null; }
        if (size > 1) {
          return new ol.style.Style({
            image: new ol.style.Circle({
              radius: 14,
              fill: new ol.style.Fill({ color: 'rgba(0, 120, 215, 0.85)' }),
              stroke: new ol.style.Stroke({ color: '#fff', width: 2 })
            }),
            text: new ol.style.Text({
              text: String(size),
              fill: new ol.style.Fill({ color: '#fff' }),
              font: 'bold 11px system-ui, sans-serif'
            })
          });
        }
        var data = features[0].get('suggestionData');
        var fill = (data && data.type === 'objection') ? '#e53935' : '#43a047';
        return new ol.style.Style({
          image: new ol.style.Circle({
            radius: 6,
            fill: new ol.style.Fill({ color: fill }),
            stroke: new ol.style.Stroke({ color: '#fff', width: 2 })
          })
        });
      }
    });
    map.addLayer(suggestionsLayer);

    loadSuggestionsForCity = function (cityName) {
      if (!sb) {
        console.warn('Supabase not available, skipping comment load');
        return;
      }
      sb.from('suggestions').select('*').eq('city', cityName)
        .then(function (result) {
          if (result.error) { console.error('Supabase:', result.error); return; }
          rawSource.clear();
          (result.data || []).forEach(function (row) {
            var feat = new ol.Feature({
              geometry: new ol.geom.Point(ol.proj.fromLonLat([row.lng, row.lat]))
            });
            feat.set('suggestionData', row);
            rawSource.addFeature(feat);
          });
        });
    };

    cancelActiveFeedback = function () {
      exitAddCommentMode();
      closeContextMenu();
      closeCommentForm();
      closePopover();
    };

    toggleBtn.addEventListener('click', function () {
      if (!currentCity) {
        openMenu();
        var cs = document.getElementById('city-search');
        cs.classList.remove('pulse-highlight');
        void cs.offsetWidth;
        cs.classList.add('pulse-highlight');
        var toast = document.getElementById('city-required-toast');
        toast.classList.add('visible');
        clearTimeout(window._cityToastTimer);
        window._cityToastTimer = setTimeout(function () {
          cs.classList.remove('pulse-highlight');
          toast.classList.remove('visible');
        }, 2000);
        return;
      }
      commentsVisible = !commentsVisible;
      suggestionsLayer.setVisible(commentsVisible);
      toggleBtn.classList.toggle('active', commentsVisible);
      toggleBtn.textContent = commentsVisible ? '💬 Hide Comments' : '💬 Show and Leave Comments';
      if (!commentsVisible) { closePopover(); exitAddCommentMode(); }
    });

    function exitAddCommentMode() {
      addCommentMode = false;
      addCommentFab.classList.remove('active');
      addCommentHint.classList.remove('visible');
      document.getElementById('map').style.cursor = '';
    }

    addCommentFab.addEventListener('click', function () {
      if (addCommentMode) { exitAddCommentMode(); return; }
      if (!currentCity) {
        openMenu();
        var cs = document.getElementById('city-search');
        cs.classList.remove('pulse-highlight');
        void cs.offsetWidth;
        cs.classList.add('pulse-highlight');
        var toast = document.getElementById('city-required-toast');
        toast.classList.add('visible');
        clearTimeout(window._cityToastTimer);
        window._cityToastTimer = setTimeout(function () {
          cs.classList.remove('pulse-highlight');
          toast.classList.remove('visible');
        }, 2000);
        return;
      }
      if (!commentsVisible) {
        commentsVisible = true;
        suggestionsLayer.setVisible(true);
        toggleBtn.classList.add('active');
        toggleBtn.textContent = '💬 Hide Comments';
      }
      addCommentMode = true;
      addCommentFab.classList.add('active');
      addCommentHint.classList.add('visible');
      document.getElementById('map').style.cursor = 'crosshair';
      closeContextMenu();
      closePopover();
    });

    map.on('moveend', function () {
      if (!commentsVisible) { return; }
      if (map.getView().getZoom() < 17) { closePopover(); return; }
      var sz = map.getSize();
      var cp = [Math.round(sz[0] / 2), Math.round(sz[1] / 2)];
      var found = null;
      map.forEachFeatureAtPixel(cp, function (f) { found = f; return true; },
        { layerFilter: function (l) { return l === suggestionsLayer; }, hitTolerance: 50 });
      if (found) { openPopover(found, cp); }
    });

    map.on('singleclick', function (e) {
      if (suppressNextClick) { suppressNextClick = false; return; }
      if (addCommentMode) {
        exitAddCommentMode();
        pendingCoord = ol.proj.toLonLat(e.coordinate);
        openCommentForm();
        return;
      }
      if (!commentsVisible) { return; }
      var hit = false;
      map.forEachFeatureAtPixel(e.pixel, function (feature) {
        openPopover(feature, e.pixel); hit = true; return true;
      }, { layerFilter: function (l) { return l === suggestionsLayer; } });
      if (!hit) { closePopover(); }
    });

    mapViewport.addEventListener('contextmenu', function (e) {
      e.preventDefault();
      suppressNextClick = true;
      clearTimeout(longPressTimer);
      if (!currentCity) { return; }
      var pixel = map.getEventPixel(e);
      var onFeature = false;
      map.forEachFeatureAtPixel(pixel, function () { onFeature = true; return true; },
        { layerFilter: function (l) { return l === suggestionsLayer; } });
      if (onFeature) { suppressNextClick = false; return; }
      pendingCoord = ol.proj.toLonLat(map.getCoordinateFromPixel(pixel));
      showContextMenu(e.clientX, e.clientY);
    });

    mapViewport.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1 || !currentCity) { return; }
      var tx = e.touches[0].clientX, ty = e.touches[0].clientY;
      clearTimeout(longPressTimer);
      longPressTimer = setTimeout(function () {
        suppressNextClick = true;
        var pixel = map.getEventPixel({ clientX: tx, clientY: ty });
        var onFeature = false;
        map.forEachFeatureAtPixel(pixel, function () { onFeature = true; return true; },
          { layerFilter: function (l) { return l === suggestionsLayer; } });
        if (onFeature) { suppressNextClick = false; return; }
        pendingCoord = ol.proj.toLonLat(map.getCoordinateFromPixel(pixel));
        showContextMenu(tx, ty);
      }, 600);
    }, { passive: true });

    mapViewport.addEventListener('touchmove', function () { clearTimeout(longPressTimer); }, { passive: true });
    mapViewport.addEventListener('touchend',  function () { clearTimeout(longPressTimer); }, { passive: true });

    document.getElementById('context-menu-add').addEventListener('click', function () {
      closeContextMenu();
      openCommentForm();
    });

    document.addEventListener('click', function (e) {
      if (contextMenu.classList.contains('open') && !contextMenu.contains(e.target)) {
        closeContextMenu();
      }
    });

    function showContextMenu(x, y) {
      contextMenu.style.left = x + 'px';
      contextMenu.style.top  = y + 'px';
      contextMenu.classList.add('open');
    }
    function closeContextMenu() { contextMenu.classList.remove('open'); }

    textArea.addEventListener('input', function () {
      var rem = 150 - textArea.value.length;
      charCount.textContent = rem + ' character' + (Math.abs(rem) === 1 ? '' : 's') + ' remaining';
      charCount.classList.toggle('over', rem < 0);
    });

    function openCommentForm() {
      nameInput.value = '';
      textArea.value = '';
      charCount.textContent = '150 characters remaining';
      charCount.classList.remove('over');
      formStatus.textContent = '';
      submitBtn.disabled = false;
      formModal.classList.add('open');
      setTimeout(function () { textArea.focus(); }, 50);
    }

    function closeCommentForm() {
      formModal.classList.remove('open');
      pendingCoord = null;
    }

    formClose.addEventListener('click', closeCommentForm);
    cancelBtn.addEventListener('click', closeCommentForm);
    formModal.addEventListener('click', function (e) {
      if (e.target === formModal) { closeCommentForm(); }
    });

    document.getElementById('comment-form').addEventListener('submit', function (e) {
      e.preventDefault();
      if (!pendingCoord || !currentCity) { return; }
      var text = textArea.value.trim();
      if (!text) { formStatus.textContent = 'Please enter a comment.'; return; }
      if (text.length > 150) { formStatus.textContent = 'Comment exceeds 150 characters.'; return; }

      if (!sb) {
        formStatus.textContent = 'Comments service unavailable.';
        return;
      }

      submitBtn.disabled = true;
      formStatus.textContent = 'Submitting…';

      sb.from('suggestions').insert({
        city: currentCity,
        lng: pendingCoord[0],
        lat: pendingCoord[1],
        type: 'suggestion',
        category: 'other',
        text: text,
        author_name: nameInput.value.trim() || null
      }).then(function (result) {
        submitBtn.disabled = false;
        if (result.error) { formStatus.textContent = 'Error: ' + result.error.message; return; }
        closeCommentForm();
        loadSuggestionsForCity(currentCity);
      });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') { return; }
      exitAddCommentMode();
      closeContextMenu();
      closeCommentForm();
      closePopover();
    });

    function openPopover(feature, pixel) {
      var features = feature.get('features') || [];
      if (!features.length) { return; }
      var header = features.length + ' Comment' + (features.length === 1 ? '' : 's');
      var items = features.map(function (f) {
        var d = f.get('suggestionData');
        if (!d) { return ''; }
        var date = d.created_at
          ? new Date(d.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
          : '';
        return '<div class="popover-item">' +
          '<div class="popover-meta">' + escapeHtml(d.author_name || 'Anonymous') + (date ? ' · ' + date : '') + '</div>' +
          '<p class="popover-text">' + escapeHtml(d.text) + '</p>' +
          '</div>';
      }).join('');
      popoverContent.innerHTML = '<div class="popover-header">' + escapeHtml(header) + '</div>' + items;

      var mapEl = document.getElementById('map');
      var pw = 260, left = pixel[0] + 14, top = pixel[1] - 24;
      if (left + pw > mapEl.clientWidth - 8) { left = pixel[0] - pw - 14; }
      if (top < 8) { top = 8; }
      if (top + 240 > mapEl.clientHeight) { top = mapEl.clientHeight - 248; }
      popover.style.left = left + 'px';
      popover.style.top  = top  + 'px';
      popover.classList.add('open');
    }

    function closePopover() { popover.classList.remove('open'); }
    popoverClose.addEventListener('click', closePopover);

    function escapeHtml(s) {
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
  }

  // ── 9. Submit Plan ──────────────────────────────────
  function setupSubmitPlan() {
    var submitBtn = document.getElementById('submit-plan-btn');
    var modal = document.getElementById('submit-plan-modal');
    var closeBtn = document.getElementById('submit-plan-modal-close');
    var cancelBtn = document.getElementById('submit-plan-cancel');
    var form = document.getElementById('submit-plan-form');
    var statusEl = document.getElementById('submit-plan-status');
    var citySelect = document.getElementById('submit-city');

    // Populate city dropdown
    function populateCityDropdown() {
      if (!citySelect || !cities) return;
      citySelect.innerHTML = '<option value="">Select a city...</option>';
      cities.forEach(function(city) {
        var opt = document.createElement('option');
        opt.value = city.name;
        opt.textContent = city.name;
        citySelect.appendChild(opt);
      });
    }

    // Wait for cities to load
    setTimeout(populateCityDropdown, 500);

    submitBtn.addEventListener('click', function() {
      modal.classList.add('open');
      populateCityDropdown();
    });

    closeBtn.addEventListener('click', function() { modal.classList.remove('open'); });
    cancelBtn.addEventListener('click', function() { modal.classList.remove('open'); });
    modal.addEventListener('click', function(e) {
      if (e.target === modal) modal.classList.remove('open');
    });

    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var city = document.getElementById('submit-city').value;
      var name = document.getElementById('submit-name').value.trim();
      var email = document.getElementById('submit-email').value.trim();
      var phone = document.getElementById('submit-phone').value.trim();
      var source = document.getElementById('submit-source').value.trim();
      var planType = document.getElementById('submit-plan-type').value;
      var description = document.getElementById('submit-description').value.trim();
      var fileInput = document.getElementById('submit-file');
      var submitBtnEl = document.getElementById('submit-plan-submit');

      if (!city || !name || !email || !source) {
        statusEl.textContent = 'Please fill all required fields.';
        return;
      }

      submitBtnEl.disabled = true;
      statusEl.textContent = 'Submitting...';

      // Prepare email content (since we don't have a backend yet)
      var subject = 'Master Plan Submission: ' + city;
      var body = 'City: ' + city + '\n' +
        'Name: ' + name + '\n' +
        'Email: ' + email + '\n' +
        'Phone: ' + (phone || 'N/A') + '\n' +
        'Source: ' + source + '\n' +
        'Plan Type: ' + planType + '\n' +
        'Description: ' + (description || 'N/A') + '\n';

      // If there's a file, we can't attach it via mailto. We need to handle it differently.
      // For now, we'll send the email without the file and instruct them to email separately
      var mailtoLink = 'mailto:keralafirst@example.com?subject=' + encodeURIComponent(subject) + 
        '&body=' + encodeURIComponent(body);

      // Try to open email client
      window.location.href = mailtoLink;

      // Also log to console for debugging
      console.log('Plan submission:', {
        city: city, name: name, email: email, source: source, description: description
      });

      statusEl.textContent = 'Thank you! Your email client should open. If not, please email us at keralafirst@example.com';
      submitBtnEl.disabled = false;

      // Close modal after 3 seconds
      setTimeout(function() {
        modal.classList.remove('open');
        statusEl.textContent = '';
      }, 3000);
    });
  }

})();
