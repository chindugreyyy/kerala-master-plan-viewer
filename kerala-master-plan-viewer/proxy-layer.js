/**
 * Kerala Proxy Layer — Current Land Use Visualization
 *
 * Uses OpenStreetMap data via Overpass API to show:
 * - Buildings (by type: residential, commercial, industrial, etc.)
 * - Roads (by classification: primary, secondary, tertiary, etc.)
 * - Land use polygons (residential, commercial, industrial, agricultural, etc.)
 * - Water bodies (rivers, lakes, reservoirs)
 * - Rail lines
 * - Parks and green spaces
 *
 * This is a "proxy" visualization showing current urban fabric,
 * useful for understanding city structure before official plans are added.
 */
(function() {
  'use strict';

  // ── Overpass API endpoint ──────────────────────────
  var OVERPASS_URL = 'https://overpass-api.de/api/interpreter';

  // ── Cache management ───────────────────────────────
  var CACHE_PREFIX = 'kerala_proxy_';
  var CACHE_TTL = 24 * 60 * 60 * 1000; // 24 hours

  function getCacheKey(cityName, type) {
    return CACHE_PREFIX + cityName.toLowerCase().replace(/\s+/g, '_') + '_' + type;
  }

  function getCached(cityName, type) {
    try {
      var key = getCacheKey(cityName, type);
      var item = localStorage.getItem(key);
      if (!item) return null;
      var parsed = JSON.parse(item);
      if (Date.now() - parsed.timestamp > CACHE_TTL) {
        localStorage.removeItem(key);
        return null;
      }
      return parsed.data;
    } catch (e) {
      return null;
    }
  }

  function setCached(cityName, type, data) {
    try {
      var key = getCacheKey(cityName, type);
      localStorage.setItem(key, JSON.stringify({
        timestamp: Date.now(),
        data: data
      }));
    } catch (e) {
      console.warn('Proxy cache failed:', e);
    }
  }

  // ── Overpass Query Builder ───────────────────────────
  function buildQuery(lat, lon, radiusKm) {
    // Query for buildings, land use, roads, water, rail, parks
    var radius = Math.round(radiusKm * 1000);
    return '[out:json][timeout:60];\n' +
      '(' +
      '  way["building"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  relation["building"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  way["landuse"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  relation["landuse"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  way["natural"="water"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  way["waterway"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  relation["natural"="water"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  way["highway"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  way["railway"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  way["leisure"="park"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  relation["leisure"="park"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  way["amenity"="school"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      '  way["amenity"="hospital"](around:' + radius + ',' + lat + ',' + lon + ');\n' +
      ');\n' +
      'out body;\n' +
      '>;\n' +
      'out skel qt;\n';
  }

  // ── Fetch from Overpass ──────────────────────────────
  function fetchProxyData(lat, lon, radiusKm, cityName) {
    var cached = getCached(cityName, 'full');
    if (cached) {
      return Promise.resolve(cached);
    }

    var query = buildQuery(lat, lon, radiusKm);

    return fetch(OVERPASS_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: 'data=' + encodeURIComponent(query)
    })
    .then(function(res) {
      if (!res.ok) throw new Error('Overpass API error: ' + res.status);
      return res.json();
    })
    .then(function(data) {
      // Process and categorize
      var processed = processOverpassData(data);
      setCached(cityName, 'full', processed);
      return processed;
    });
  }

  // ── Process Overpass Data ────────────────────────────
  function processOverpassData(data) {
    var elements = data.elements || [];
    var nodes = {};
    var ways = [];
    var relations = [];

    // Separate nodes, ways, relations
    elements.forEach(function(el) {
      if (el.type === 'node') {
        nodes[el.id] = [el.lon, el.lat];
      } else if (el.type === 'way') {
        ways.push(el);
      } else if (el.type === 'relation') {
        relations.push(el);
      }
    });

    // Categorize features
    var buildings = [];
    var landUse = [];
    var roads = [];
    var water = [];
    var rail = [];
    var parks = [];
    var schools = [];
    var hospitals = [];

    ways.forEach(function(way) {
      var tags = way.tags || {};
      var coords = (way.nodes || []).map(function(nid) {
        return nodes[nid];
      }).filter(function(c) { return c; });

      if (coords.length < 2) return;

      if (tags.building) {
        buildings.push({
          type: 'building',
          subtype: tags.building,
          coords: coords,
          tags: tags
        });
      } else if (tags.landuse) {
        landUse.push({
          type: 'landuse',
          subtype: tags.landuse,
          coords: coords,
          tags: tags
        });
      } else if (tags.highway) {
        roads.push({
          type: 'road',
          subtype: tags.highway,
          coords: coords,
          tags: tags,
          name: tags.name || ''
        });
      } else if (tags.natural === 'water' || tags.waterway) {
        water.push({
          type: 'water',
          subtype: tags.waterway || tags.natural,
          coords: coords,
          tags: tags
        });
      } else if (tags.railway) {
        rail.push({
          type: 'rail',
          subtype: tags.railway,
          coords: coords,
          tags: tags
        });
      } else if (tags.leisure === 'park') {
        parks.push({
          type: 'park',
          subtype: 'park',
          coords: coords,
          tags: tags
        });
      } else if (tags.amenity === 'school') {
        schools.push({
          type: 'school',
          subtype: 'school',
          coords: coords,
          tags: tags
        });
      } else if (tags.amenity === 'hospital') {
        hospitals.push({
          type: 'hospital',
          subtype: 'hospital',
          coords: coords,
          tags: tags
        });
      }
    });

    return {
      buildings: buildings,
      landUse: landUse,
      roads: roads,
      water: water,
      rail: rail,
      parks: parks,
      schools: schools,
      hospitals: hospitals,
      timestamp: new Date().toISOString()
    };
  }

  // ── Color scheme for proxy layer ─────────────────────
  var COLORS = {
    // Buildings
    building: {
      residential: 'rgba(255, 200, 150, 0.7)',
      commercial: 'rgba(255, 150, 100, 0.7)',
      industrial: 'rgba(150, 150, 150, 0.7)',
      retail: 'rgba(255, 180, 120, 0.7)',
      office: 'rgba(180, 180, 220, 0.7)',
      school: 'rgba(200, 220, 100, 0.7)',
      hospital: 'rgba(255, 100, 100, 0.7)',
      public: 'rgba(150, 200, 255, 0.7)',
      default: 'rgba(200, 200, 200, 0.5)'
    },
    // Land use
    landuse: {
      residential: 'rgba(255, 230, 200, 0.4)',
      commercial: 'rgba(255, 200, 180, 0.4)',
      industrial: 'rgba(180, 180, 180, 0.4)',
      retail: 'rgba(255, 210, 190, 0.4)',
      agricultural: 'rgba(200, 255, 200, 0.4)',
      forest: 'rgba(150, 220, 150, 0.4)',
      recreation: 'rgba(180, 255, 180, 0.4)',
      default: 'rgba(240, 240, 240, 0.3)'
    },
    // Roads
    road: {
      motorway: 'rgba(255, 50, 50, 0.9)',
      trunk: 'rgba(255, 100, 50, 0.9)',
      primary: 'rgba(255, 150, 50, 0.9)',
      secondary: 'rgba(255, 200, 50, 0.8)',
      tertiary: 'rgba(255, 230, 100, 0.8)',
      residential: 'rgba(255, 255, 255, 0.7)',
      service: 'rgba(200, 200, 200, 0.7)',
      default: 'rgba(220, 220, 220, 0.7)'
    },
    // Water
    water: 'rgba(50, 150, 255, 0.6)',
    // Rail
    rail: 'rgba(100, 100, 100, 0.8)',
    // Parks
    park: 'rgba(100, 200, 100, 0.5)',
    // Schools
    school: 'rgba(220, 240, 100, 0.7)',
    // Hospitals
    hospital: 'rgba(255, 100, 100, 0.7)'
  };

  // ── Create OpenLayers Vector Layer ───────────────────
  function createProxyLayer(processedData) {
    var features = [];

    // Process buildings
    processedData.buildings.forEach(function(b) {
      var color = COLORS.building[b.subtype] || COLORS.building.default;
      if (b.coords.length >= 3) {
        var coords = b.coords.map(function(c) {
          return ol.proj.fromLonLat(c);
        });
        // Close polygon
        if (coords[0][0] !== coords[coords.length-1][0] || coords[0][1] !== coords[coords.length-1][1]) {
          coords.push(coords[0]);
        }
        var feature = new ol.Feature({
          geometry: new ol.geom.Polygon([coords])
        });
        feature.set('type', 'building');
        feature.set('subtype', b.subtype);
        feature.set('style', new ol.style.Style({
          fill: new ol.style.Fill({ color: color }),
          stroke: new ol.style.Stroke({ color: 'rgba(0,0,0,0.2)', width: 1 })
        }));
        features.push(feature);
      }
    });

    // Process land use
    processedData.landUse.forEach(function(lu) {
      var color = COLORS.landuse[lu.subtype] || COLORS.landuse.default;
      if (lu.coords.length >= 3) {
        var coords = lu.coords.map(function(c) {
          return ol.proj.fromLonLat(c);
        });
        if (coords[0][0] !== coords[coords.length-1][0] || coords[0][1] !== coords[coords.length-1][1]) {
          coords.push(coords[0]);
        }
        var feature = new ol.Feature({
          geometry: new ol.geom.Polygon([coords])
        });
        feature.set('type', 'landuse');
        feature.set('subtype', lu.subtype);
        feature.set('style', new ol.style.Style({
          fill: new ol.style.Fill({ color: color }),
          stroke: new ol.style.Stroke({ color: 'rgba(0,0,0,0.1)', width: 1 })
        }));
        features.push(feature);
      }
    });

    // Process roads
    processedData.roads.forEach(function(r) {
      var color = COLORS.road[r.subtype] || COLORS.road.default;
      var width = r.subtype === 'motorway' || r.subtype === 'trunk' ? 4 :
                  r.subtype === 'primary' ? 3 :
                  r.subtype === 'secondary' ? 2.5 :
                  r.subtype === 'tertiary' ? 2 : 1;
      
      if (r.coords.length >= 2) {
        var coords = r.coords.map(function(c) {
          return ol.proj.fromLonLat(c);
        });
        var feature = new ol.Feature({
          geometry: new ol.geom.LineString(coords)
        });
        feature.set('type', 'road');
        feature.set('subtype', r.subtype);
        feature.set('name', r.name);
        feature.set('style', new ol.style.Style({
          stroke: new ol.style.Stroke({ color: color, width: width })
        }));
        features.push(feature);
      }
    });

    // Process water
    processedData.water.forEach(function(w) {
      if (w.coords.length >= 3) {
        var coords = w.coords.map(function(c) {
          return ol.proj.fromLonLat(c);
        });
        if (coords[0][0] !== coords[coords.length-1][0] || coords[0][1] !== coords[coords.length-1][1]) {
          coords.push(coords[0]);
        }
        var feature = new ol.Feature({
          geometry: new ol.geom.Polygon([coords])
        });
        feature.set('type', 'water');
        feature.set('style', new ol.style.Style({
          fill: new ol.style.Fill({ color: COLORS.water }),
          stroke: new ol.style.Stroke({ color: 'rgba(0,100,200,0.8)', width: 1 })
        }));
        features.push(feature);
      }
    });

    // Process rail
    processedData.rail.forEach(function(r) {
      if (r.coords.length >= 2) {
        var coords = r.coords.map(function(c) {
          return ol.proj.fromLonLat(c);
        });
        var feature = new ol.Feature({
          geometry: new ol.geom.LineString(coords)
        });
        feature.set('type', 'rail');
        feature.set('style', new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: COLORS.rail,
            width: 2,
            lineDash: [5, 5]
          })
        }));
        features.push(feature);
      }
    });

    // Process parks
    processedData.parks.forEach(function(p) {
      if (p.coords.length >= 3) {
        var coords = p.coords.map(function(c) {
          return ol.proj.fromLonLat(c);
        });
        if (coords[0][0] !== coords[coords.length-1][0] || coords[0][1] !== coords[coords.length-1][1]) {
          coords.push(coords[0]);
        }
        var feature = new ol.Feature({
          geometry: new ol.geom.Polygon([coords])
        });
        feature.set('type', 'park');
        feature.set('style', new ol.style.Style({
          fill: new ol.style.Fill({ color: COLORS.park }),
          stroke: new ol.style.Stroke({ color: 'rgba(0,150,0,0.5)', width: 1 })
        }));
        features.push(feature);
      }
    });

    // Process schools
    processedData.schools.forEach(function(s) {
      if (s.coords.length >= 3) {
        var coords = s.coords.map(function(c) {
          return ol.proj.fromLonLat(c);
        });
        if (coords[0][0] !== coords[coords.length-1][0] || coords[0][1] !== coords[coords.length-1][1]) {
          coords.push(coords[0]);
        }
        var feature = new ol.Feature({
          geometry: new ol.geom.Polygon([coords])
        });
        feature.set('type', 'school');
        feature.set('style', new ol.style.Style({
          fill: new ol.style.Fill({ color: COLORS.school }),
          stroke: new ol.style.Stroke({ color: 'rgba(150,150,0,0.5)', width: 1 })
        }));
        features.push(feature);
      }
    });

    // Process hospitals
    processedData.hospitals.forEach(function(h) {
      if (h.coords.length >= 3) {
        var coords = h.coords.map(function(c) {
          return ol.proj.fromLonLat(c);
        });
        if (coords[0][0] !== coords[coords.length-1][0] || coords[0][1] !== coords[coords.length-1][1]) {
          coords.push(coords[0]);
        }
        var feature = new ol.Feature({
          geometry: new ol.geom.Polygon([coords])
        });
        feature.set('type', 'hospital');
        feature.set('style', new ol.style.Style({
          fill: new ol.style.Fill({ color: COLORS.hospital }),
          stroke: new ol.style.Stroke({ color: 'rgba(200,0,0,0.5)', width: 1 })
        }));
        features.push(feature);
      }
    });

    var vectorSource = new ol.source.Vector({
      features: features
    });

    var layer = new ol.layer.Vector({
      source: vectorSource,
      style: function(feature) {
        return feature.get('style');
      },
      zIndex: 500,
      visible: true
    });

    layer._isProxyLayer = true;
    layer._proxyTimestamp = processedData.timestamp;
    layer._proxyStats = {
      buildings: processedData.buildings.length,
      roads: processedData.roads.length,
      landuse: processedData.landUse.length,
      water: processedData.water.length,
      parks: processedData.parks.length,
      schools: processedData.schools.length,
      hospitals: processedData.hospitals.length
    };

    return layer;
  }

  // ── Public API ─────────────────────────────────────
  window.KeralaProxyLayer = {
    load: function(city, callback, errorCallback) {
      var lat = city.center[1];
      var lon = city.center[0];
      var radius = city.zoom >= 13 ? 5 : city.zoom >= 11 ? 10 : 15;

      // Show loading indicator
      showLoading('Loading current land use data...');

      fetchProxyData(lat, lon, radius, city.name)
        .then(function(data) {
          hideLoading();
          var layer = createProxyLayer(data);
          if (callback) callback(layer);
        })
        .catch(function(err) {
          hideLoading();
          console.error('Proxy layer error:', err);
          if (errorCallback) errorCallback(err);
        });
    },

    getLegend: function() {
      return {
        title: 'Current Land Use (OSM Proxy)',
        categories: [
          { label: 'Residential Buildings', color: COLORS.building.residential },
          { label: 'Commercial Buildings', color: COLORS.building.commercial },
          { label: 'Industrial Buildings', color: COLORS.building.industrial },
          { label: 'Schools', color: COLORS.building.school },
          { label: 'Hospitals', color: COLORS.building.hospital },
          { label: 'Residential Area', color: COLORS.landuse.residential },
          { label: 'Commercial Area', color: COLORS.landuse.commercial },
          { label: 'Industrial Area', color: COLORS.landuse.industrial },
          { label: 'Agricultural', color: COLORS.landuse.agricultural },
          { label: 'Forest', color: COLORS.landuse.forest },
          { label: 'Water Bodies', color: COLORS.water },
          { label: 'Major Roads', color: COLORS.road.motorway },
          { label: 'Primary Roads', color: COLORS.road.primary },
          { label: 'Secondary Roads', color: COLORS.road.secondary },
          { label: 'Parks', color: COLORS.park },
          { label: 'Railway', color: COLORS.rail }
        ]
      };
    },

    clearCache: function(cityName) {
      if (cityName) {
        localStorage.removeItem(getCacheKey(cityName, 'full'));
      } else {
        // Clear all proxy cache
        Object.keys(localStorage).forEach(function(key) {
          if (key.indexOf(CACHE_PREFIX) === 0) {
            localStorage.removeItem(key);
          }
        });
      }
    }
  };

  // ── Loading indicators ─────────────────────────────
  function showLoading(text) {
    var el = document.getElementById('proxy-loading');
    if (el) {
      el.textContent = text || 'Loading...';
      el.classList.add('visible');
    }
  }

  function hideLoading() {
    var el = document.getElementById('proxy-loading');
    if (el) {
      el.classList.remove('visible');
    }
  }

})();
