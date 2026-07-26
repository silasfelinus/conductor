/**
 * Dispatcher map UI (humboldt-scoop-cms/t-008). Self-contained HTML/JS page --
 * no build step, no framework, no bundler -- calls the JSON API in server.ts.
 * Leaflet's JS/CSS/marker images are vendored from node_modules and served by
 * this same service (see server.ts's /vendor/leaflet/* route) rather than
 * fetched from a CDN, so the page has no external script/style dependency at
 * runtime. Map *tiles* still come from the standard public OpenStreetMap tile
 * server (free, no API key, no billing) -- the same "free tile provider"
 * option route-planner/SPEC.md's own §3a/§5 name as acceptable for this
 * scale; a tile-fetch failure only affects the background imagery, not the
 * markers/polyline/stop list. Routing/optimization itself stays server-side and algorithmic
 * (haversine fallback or self-hosted OSRM per OSRM_BASE_URL) -- this page
 * never calls a third-party routing/geocoding API and never sends
 * coordinates anywhere but this service's own /routes/plan endpoint.
 * Dummy data only, per notes_from_silas.
 */
export const DISPATCH_PAGE_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Humboldt Scoop CMS — Dispatcher Route Planner</title>
<link rel="stylesheet" href="/vendor/leaflet/leaflet.css" />
<script src="/vendor/leaflet/leaflet.js"></script>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body { margin: 0; font-family: system-ui, -apple-system, Segoe UI, sans-serif; background: #f4f6f5; color: #1c2b24; }
  header { background: #1f6b4a; color: #fff; padding: 0.75rem 1rem; }
  header h1 { margin: 0; font-size: 1.1rem; }
  header p { margin: 0.15rem 0 0; font-size: 0.8rem; opacity: 0.85; }
  .layout { display: grid; grid-template-columns: 340px 1fr 320px; gap: 0; height: calc(100vh - 58px); }
  .panel { overflow-y: auto; padding: 0.75rem; }
  .controls { background: #fff; border-right: 1px solid #dde3e0; }
  .results { border-left: 1px solid #dde3e0; background: #fff; }
  #map { width: 100%; height: 100%; }
  fieldset { border: 1px solid #dde3e0; border-radius: 6px; margin: 0 0 0.75rem; padding: 0.5rem 0.6rem; }
  legend { font-size: 0.75rem; font-weight: 600; color: #1f6b4a; padding: 0 0.25rem; }
  label { display: block; font-size: 0.78rem; margin: 0.35rem 0 0.15rem; }
  input, select { width: 100%; padding: 0.3rem; font-size: 0.85rem; border: 1px solid #c7d0cb; border-radius: 4px; }
  input[type="radio"], input[type="checkbox"] { width: auto; }
  .row { display: flex; gap: 0.5rem; }
  .row > div { flex: 1; }
  button { cursor: pointer; border: none; border-radius: 4px; padding: 0.45rem 0.7rem; font-size: 0.82rem; font-weight: 600; }
  .btn-primary { background: #1f6b4a; color: #fff; width: 100%; margin-top: 0.4rem; }
  .btn-secondary { background: #e7ede9; color: #1f6b4a; width: 100%; margin-top: 0.4rem; }
  .btn-small { background: #e7ede9; color: #1f6b4a; padding: 0.2rem 0.45rem; font-size: 0.7rem; }
  .customer-item { display: flex; align-items: center; gap: 0.4rem; padding: 0.2rem 0; font-size: 0.8rem; border-bottom: 1px dashed #eef1ef; }
  .customer-item span.meta { color: #6b7a72; font-size: 0.7rem; }
  #totals { background: #eef6f0; border: 1px solid #cfe6d8; border-radius: 6px; padding: 0.5rem 0.6rem; font-size: 0.8rem; margin-bottom: 0.6rem; }
  #totals strong { color: #1f6b4a; }
  .warning { background: #fff6e0; border: 1px solid #edd68a; border-radius: 6px; padding: 0.4rem 0.6rem; font-size: 0.75rem; margin-bottom: 0.4rem; }
  .excluded { background: #fdeeee; border: 1px solid #f0c4c4; border-radius: 6px; padding: 0.4rem 0.6rem; font-size: 0.75rem; margin-bottom: 0.4rem; }
  ul.stop-list { list-style: none; margin: 0; padding: 0; }
  li.stop-card {
    background: #fff; border: 1px solid #dde3e0; border-radius: 6px; padding: 0.45rem 0.6rem;
    margin-bottom: 0.4rem; cursor: grab; font-size: 0.78rem;
  }
  li.stop-card.dragging { opacity: 0.4; }
  li.stop-card.drag-over { border-color: #1f6b4a; border-width: 2px; }
  li.stop-card .seq { display: inline-block; width: 1.4rem; height: 1.4rem; line-height: 1.4rem; text-align: center; background: #1f6b4a; color: #fff; border-radius: 50%; font-size: 0.72rem; margin-right: 0.3rem; }
  li.stop-card .name { font-weight: 600; }
  li.stop-card .leg { color: #6b7a72; font-size: 0.7rem; margin-top: 0.15rem; }
  li.stop-card.locked { border-left: 4px solid #c98a1a; }
  .stop-actions { margin-top: 0.25rem; display: flex; gap: 0.35rem; align-items: center; }
  .stop-actions label { display: inline-flex; align-items: center; gap: 0.2rem; margin: 0; font-size: 0.7rem; }
  small.notice { display: block; color: #6b7a72; font-size: 0.68rem; margin-top: 0.3rem; }
  #draftsList { font-size: 0.75rem; }
  #status { font-size: 0.75rem; min-height: 1rem; margin-top: 0.3rem; }
  #status.error { color: #b3261e; }
  #status.ok { color: #1f6b4a; }
</style>
</head>
<body>
<header>
  <h1>Humboldt Scoop CMS — Dispatcher Route Planner</h1>
  <p>Dummy data only. No real customer records. Routing is deterministic (haversine fallback or self-hosted OSRM) — never an LLM.</p>
</header>
<div class="layout">
  <div class="panel controls">
    <fieldset>
      <legend>1. Date &amp; filter</legend>
      <label for="date">Service date</label>
      <input id="date" type="date" value="2026-07-28" />
      <div class="row">
        <div>
          <label for="neighborhood">Neighborhood (optional)</label>
          <input id="neighborhood" type="text" placeholder="e.g. Eureka" />
        </div>
        <div>
          <label for="frequency">Frequency (optional)</label>
          <select id="frequency">
            <option value="">Any</option>
            <option value="weekly">Weekly</option>
            <option value="twice-weekly">Twice-weekly</option>
            <option value="biweekly">Biweekly</option>
            <option value="monthly">Monthly</option>
            <option value="one-time">One-time</option>
          </select>
        </div>
      </div>
      <button class="btn-secondary" id="loadEligibleBtn">Load eligible customers</button>
    </fieldset>

    <fieldset>
      <legend>2. Selection</legend>
      <label><input type="radio" name="mode" value="explicit" checked /> Explicit (check customers below)</label>
      <label><input type="radio" name="mode" value="fill-to-n" /> Fill-to-N (auto-pick top N)</label>
      <div id="fillToNControls" style="display:none;">
        <div class="row">
          <div>
            <label for="count">Stop count (N)</label>
            <input id="count" type="number" min="0" value="3" />
          </div>
          <div>
            <label for="sortBy">Sort by</label>
            <select id="sortBy">
              <option value="earliest-due">Earliest due</option>
              <option value="proximity">Proximity to start</option>
            </select>
          </div>
        </div>
      </div>
      <div id="customerChecklist" style="max-height: 220px; overflow-y: auto; margin-top: 0.3rem;">
        <small class="notice">Load eligible customers first.</small>
      </div>
    </fieldset>

    <fieldset>
      <legend>3. Start / end / crew time</legend>
      <label for="startLabel">Start label</label>
      <input id="startLabel" type="text" value="Shop" />
      <div class="row">
        <div><label for="startLat">Start lat</label><input id="startLat" type="number" step="any" value="40.8021" /></div>
        <div><label for="startLng">Start lng</label><input id="startLng" type="number" step="any" value="-124.1637" /></div>
      </div>
      <label><input type="checkbox" id="roundTrip" checked /> Round trip (end = start)</label>
      <div id="endControls" style="display:none;">
        <label for="endLabel">End label</label>
        <input id="endLabel" type="text" value="" placeholder="e.g. Home base" />
        <div class="row">
          <div><label for="endLat">End lat</label><input id="endLat" type="number" step="any" /></div>
          <div><label for="endLng">End lng</label><input id="endLng" type="number" step="any" /></div>
        </div>
      </div>
      <label for="crewStartTime">Crew start time (ISO, optional)</label>
      <input id="crewStartTime" type="text" placeholder="2026-07-28T08:00:00Z" />
    </fieldset>

    <button class="btn-primary" id="planBtn">Plan route</button>
    <div id="status"></div>
  </div>

  <div id="map"></div>

  <div class="panel results">
    <div id="totals" style="display:none;"></div>
    <div id="warnings"></div>
    <div id="excludedPanel" style="display:none;"></div>
    <ul class="stop-list" id="stopList"></ul>
    <hr />
    <button class="btn-secondary" id="saveDraftBtn" disabled>Save draft</button>
    <button class="btn-secondary" id="loadDraftsBtn">View saved drafts</button>
    <div id="draftsList"></div>
  </div>
</div>

<script>
(function () {
  var map = L.map('map').setView([40.80, -124.13], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  var routeLayer = L.layerGroup().addTo(map);

  var eligible = [];
  var lastPlan = null;
  /** customerId -> 0-based position, for manually pinned stops. */
  var lockedMap = {};

  var statusEl = document.getElementById('status');
  function setStatus(msg, isError) {
    statusEl.textContent = msg || '';
    statusEl.className = msg ? (isError ? 'error' : 'ok') : '';
  }

  document.querySelectorAll('input[name="mode"]').forEach(function (el) {
    el.addEventListener('change', function () {
      var mode = document.querySelector('input[name="mode"]:checked').value;
      document.getElementById('fillToNControls').style.display = mode === 'fill-to-n' ? 'block' : 'none';
      renderChecklist();
    });
  });

  document.getElementById('roundTrip').addEventListener('change', function (e) {
    document.getElementById('endControls').style.display = e.target.checked ? 'none' : 'block';
  });

  function decodePolyline(str, precision) {
    // Standard Google/OSRM encoded-polyline decoder (precision 5 by default).
    var index = 0, lat = 0, lng = 0, coordinates = [], factor = Math.pow(10, precision || 5);
    var shift, result, byte, latitude_change, longitude_change;
    while (index < str.length) {
      shift = 0; result = 0;
      do { byte = str.charCodeAt(index++) - 63; result |= (byte & 0x1f) << shift; shift += 5; } while (byte >= 0x20);
      latitude_change = (result & 1) ? ~(result >> 1) : (result >> 1);
      shift = 0; result = 0;
      do { byte = str.charCodeAt(index++) - 63; result |= (byte & 0x1f) << shift; shift += 5; } while (byte >= 0x20);
      longitude_change = (result & 1) ? ~(result >> 1) : (result >> 1);
      lat += latitude_change; lng += longitude_change;
      coordinates.push([lat / factor, lng / factor]);
    }
    return coordinates;
  }

  function renderChecklist() {
    var mode = document.querySelector('input[name="mode"]:checked').value;
    var el = document.getElementById('customerChecklist');
    if (eligible.length === 0) {
      el.innerHTML = '<small class="notice">Load eligible customers first.</small>';
      return;
    }
    if (mode === 'fill-to-n') {
      el.innerHTML = eligible.map(function (s) {
        return '<div class="customer-item">' + s.customerName + ' <span class="meta">(' + s.neighborhood + ', ' + s.yardSize + ')</span></div>';
      }).join('') + '<small class="notice">Fill-to-N auto-picks the top N below; switch to Explicit to hand-pick or remove a specific stop.</small>';
      return;
    }
    el.innerHTML = eligible.map(function (s) {
      return '<div class="customer-item"><input type="checkbox" class="cust-check" value="' + s.customerId + '" checked>' +
        s.customerName + ' <span class="meta">(' + s.neighborhood + ', ' + s.yardSize + ')</span></div>';
    }).join('');
  }

  document.getElementById('loadEligibleBtn').addEventListener('click', function () {
    var date = document.getElementById('date').value;
    if (!date) { setStatus('Pick a date first.', true); return; }
    var params = new URLSearchParams({ date: date });
    var neighborhood = document.getElementById('neighborhood').value.trim();
    var frequency = document.getElementById('frequency').value;
    if (neighborhood) params.set('neighborhood', neighborhood);
    if (frequency) params.set('frequency', frequency);

    setStatus('Loading eligible customers...');
    fetch('/routes/eligible?' + params.toString())
      .then(function (r) { return r.json(); })
      .then(function (body) {
        if (!body.success) { setStatus(body.message || 'Failed to load eligible customers.', true); return; }
        eligible = body.data.eligible;
        renderChecklist();
        setStatus(eligible.length + ' eligible customer(s) loaded' +
          (body.data.missingCoordinates.length ? ' (' + body.data.missingCoordinates.length + ' excluded for missing coordinates)' : '') + '.');
      })
      .catch(function (err) { setStatus('Network error: ' + err.message, true); });
  });

  function buildPlanRequest() {
    var date = document.getElementById('date').value;
    var mode = document.querySelector('input[name="mode"]:checked').value;
    var selection;
    if (mode === 'explicit') {
      var ids = Array.prototype.slice.call(document.querySelectorAll('.cust-check:checked')).map(function (el) { return el.value; });
      selection = { mode: 'explicit', customerIds: ids };
    } else {
      selection = { mode: 'fill-to-n', count: Number(document.getElementById('count').value), sortBy: document.getElementById('sortBy').value };
    }

    var neighborhood = document.getElementById('neighborhood').value.trim();
    var frequency = document.getElementById('frequency').value;
    var filter = {};
    if (neighborhood) filter.neighborhood = neighborhood;
    if (frequency) filter.frequency = frequency;

    var start = {
      lat: Number(document.getElementById('startLat').value),
      lng: Number(document.getElementById('startLng').value),
      label: document.getElementById('startLabel').value || undefined,
    };

    var body = { date: date, selection: selection, start: start };
    if (Object.keys(filter).length) body.filter = filter;

    if (!document.getElementById('roundTrip').checked) {
      body.end = {
        lat: Number(document.getElementById('endLat').value),
        lng: Number(document.getElementById('endLng').value),
        label: document.getElementById('endLabel').value || undefined,
      };
    }

    var crewStartTime = document.getElementById('crewStartTime').value.trim();
    if (crewStartTime) body.crewStartTime = crewStartTime;

    var locked = Object.keys(lockedMap).map(function (customerId) {
      return { customerId: customerId, position: lockedMap[customerId] };
    });
    if (locked.length) body.locked = locked;

    return body;
  }

  function planRoute() {
    var body = buildPlanRequest();
    setStatus('Planning route...');
    return fetch('/routes/plan', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (data) { return { ok: r.ok, data: data }; }); })
      .then(function (res) {
        if (!res.data.success) { setStatus(res.data.message || 'Route planning failed.', true); return; }
        lastPlan = res.data.data;
        renderPlan(lastPlan);
        setStatus('Route planned via ' + lastPlan.routingProvider + '.');
      })
      .catch(function (err) { setStatus('Network error: ' + err.message, true); });
  }

  document.getElementById('planBtn').addEventListener('click', function () {
    lockedMap = {}; // a fresh plan resets any manual reorder from a previous run
    planRoute();
  });

  function fmtKm(m) { return (m / 1000).toFixed(1) + ' km'; }
  function fmtMin(s) { return Math.round(s / 60) + ' min'; }
  function fmtTime(iso) { try { return new Date(iso).toISOString().slice(11, 16) + ' UTC'; } catch (e) { return iso; } }

  function renderPlan(plan) {
    routeLayer.clearLayers();
    var latlngs = [];

    var startMarker = L.marker([plan.start.lat, plan.start.lng], { title: plan.start.label || 'Start' })
      .bindPopup('Start: ' + (plan.start.label || 'Start'));
    routeLayer.addLayer(startMarker);
    latlngs.push([plan.start.lat, plan.start.lng]);

    plan.stops.forEach(function (stop) {
      var marker = L.marker([stop.coordinates.lat, stop.coordinates.lng])
        .bindPopup('#' + stop.sequence + ' ' + stop.customerName + ' — ' + stop.propertyLabel);
      routeLayer.addLayer(marker);
      latlngs.push([stop.coordinates.lat, stop.coordinates.lng]);
    });

    var endMarker = L.marker([plan.end.lat, plan.end.lng], { title: plan.end.label || 'End' })
      .bindPopup('End: ' + (plan.end.label || 'End'));
    routeLayer.addLayer(endMarker);
    latlngs.push([plan.end.lat, plan.end.lng]);

    var lineLatLngs = plan.polyline ? decodePolyline(plan.polyline) : latlngs;
    var polyline = L.polyline(lineLatLngs, { color: '#1f6b4a', weight: 4, opacity: 0.8 });
    routeLayer.addLayer(polyline);
    if (latlngs.length) map.fitBounds(L.latLngBounds(latlngs), { padding: [24, 24] });

    var totalsEl = document.getElementById('totals');
    totalsEl.style.display = 'block';
    totalsEl.innerHTML = '<strong>' + plan.stops.length + ' stop(s)</strong> via ' + plan.routingProvider +
      ' &middot; ' + fmtKm(plan.totals.distanceMeters) + ' &middot; ' + fmtMin(plan.totals.durationSeconds) +
      ' &middot; finish ~' + fmtTime(plan.totals.estimatedFinishTime) +
      (plan.polyline ? '' : '<br><small class="notice">No road-network geometry from this provider -- straight-line preview only.</small>');

    var warningsEl = document.getElementById('warnings');
    warningsEl.innerHTML = (plan.warnings || []).map(function (w) { return '<div class="warning">' + w + '</div>'; }).join('');

    var excludedEl = document.getElementById('excludedPanel');
    if (plan.excluded && plan.excluded.length) {
      excludedEl.style.display = 'block';
      excludedEl.innerHTML = '<strong>Skipped this run (' + plan.excluded.length + ')</strong><br>' +
        plan.excluded.map(function (ex) { return ex.customerName + ' — ' + ex.reason; }).join('<br>');
    } else {
      excludedEl.style.display = 'none';
      excludedEl.innerHTML = '';
    }

    renderStopList(plan);
    document.getElementById('saveDraftBtn').disabled = false;
  }

  var dragSrcIdx = null;

  function renderStopList(plan) {
    var list = document.getElementById('stopList');
    list.innerHTML = '';
    plan.stops.forEach(function (stop, idx) {
      var li = document.createElement('li');
      li.className = 'stop-card' + (stop.locked ? ' locked' : '');
      li.draggable = true;
      li.dataset.idx = String(idx);
      li.innerHTML =
        '<span class="seq">' + stop.sequence + '</span><span class="name">' + stop.customerName + '</span>' +
        (stop.locked ? ' 🔒' : '') +
        '<div class="leg">' + stop.propertyLabel + ' (' + stop.neighborhood + ') &middot; leg ' + fmtKm(stop.legDistanceMeters) +
        ' / ' + fmtMin(stop.legDurationSeconds) + ' &middot; ETA ' + fmtTime(stop.eta) + '</div>' +
        '<div class="stop-actions">' +
        '<label><input type="checkbox" class="lock-toggle" ' + (stop.locked ? 'checked' : '') + '> Lock position</label>' +
        '<button type="button" class="btn-small remove-stop">Remove</button>' +
        '</div>';

      li.addEventListener('dragstart', function () { dragSrcIdx = idx; li.classList.add('dragging'); });
      li.addEventListener('dragend', function () { li.classList.remove('dragging'); });
      li.addEventListener('dragover', function (e) { e.preventDefault(); li.classList.add('drag-over'); });
      li.addEventListener('dragleave', function () { li.classList.remove('drag-over'); });
      li.addEventListener('drop', function (e) {
        e.preventDefault();
        li.classList.remove('drag-over');
        var targetIdx = idx;
        if (dragSrcIdx === null || dragSrcIdx === targetIdx) return;
        var reordered = plan.stops.slice();
        var moved = reordered.splice(dragSrcIdx, 1)[0];
        reordered.splice(targetIdx, 0, moved);
        lockedMap = {};
        reordered.forEach(function (s, i) { lockedMap[s.customerId] = i; });
        setStatus('Recalculating with manual order...');
        planRoute();
      });

      li.querySelector('.lock-toggle').addEventListener('change', function (e) {
        if (e.target.checked) {
          lockedMap[stop.customerId] = idx;
        } else {
          delete lockedMap[stop.customerId];
        }
        setStatus('Recalculating...');
        planRoute();
      });

      li.querySelector('.remove-stop').addEventListener('click', function () {
        var mode = document.querySelector('input[name="mode"]:checked').value;
        if (mode !== 'explicit') {
          setStatus('Switch to Explicit mode to remove a specific stop from a Fill-to-N run.', true);
          return;
        }
        var checkbox = document.querySelector('.cust-check[value="' + stop.customerId + '"]');
        if (checkbox) checkbox.checked = false;
        delete lockedMap[stop.customerId];
        setStatus('Recalculating without ' + stop.customerName + '...');
        planRoute();
      });

      list.appendChild(li);
    });
  }

  document.getElementById('saveDraftBtn').addEventListener('click', function () {
    if (!lastPlan) return;
    var label = window.prompt('Optional label for this draft:', '') || null;
    fetch('/routes/draft', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ plan: lastPlan, label: label }) })
      .then(function (r) { return r.json(); })
      .then(function (body) {
        if (!body.success) { setStatus(body.message || 'Failed to save draft.', true); return; }
        setStatus('Saved draft ' + body.data.id + '.');
      })
      .catch(function (err) { setStatus('Network error: ' + err.message, true); });
  });

  document.getElementById('loadDraftsBtn').addEventListener('click', function () {
    fetch('/routes/drafts')
      .then(function (r) { return r.json(); })
      .then(function (body) {
        if (!body.success) { setStatus(body.message || 'Failed to load drafts.', true); return; }
        var el = document.getElementById('draftsList');
        if (!body.data.length) { el.innerHTML = '<small class="notice">No saved drafts yet.</small>'; return; }
        el.innerHTML = '<strong>Saved drafts</strong><br>' + body.data.map(function (d) {
          return d.id + (d.label ? ' — ' + d.label : '') + ' &middot; ' + d.date + ' &middot; ' + d.stopCount + ' stop(s)';
        }).join('<br>');
      })
      .catch(function (err) { setStatus('Network error: ' + err.message, true); });
  });
})();
</script>
</body>
</html>
`
