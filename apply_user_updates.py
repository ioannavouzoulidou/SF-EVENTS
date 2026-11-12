import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update cluster styling and calculation
old_cluster_func = """    iconCreateFunction: function(cluster) {
      const count = cluster.getChildCount();
      let sizeClass = 'small';
      let diameter = 30;
      if (count >= 10) {
        sizeClass = 'large';
        diameter = 42;
      } else if (count >= 5) {
        sizeClass = 'medium';
        diameter = 36;
      }
      return L.divIcon({
        html: `<div class="custom-cluster-marker ${sizeClass}"><span>${count}</span></div>`,
        className: 'custom-cluster-icon',
        iconSize: L.point(diameter, diameter)
      });
    }"""

new_cluster_func = """    iconCreateFunction: function(cluster) {
      const count = cluster.getChildCount();
      // Blue shades: lightest is exactly #3b82f6 (individual event color), transitioning to darkest navy
      let bg = '#3b82f6';
      let diameter = 26;

      if (count <= 2) {
        bg = '#3b82f6'; // Lightest blue - EXACTLY matching individual event marker
        diameter = 26;
      } else if (count <= 5) {
        bg = '#2563eb';
        diameter = 30;
      } else if (count <= 9) {
        bg = '#1d4ed8';
        diameter = 34;
      } else if (count <= 15) {
        bg = '#1e3a8a';
        diameter = 38;
      } else {
        bg = '#0f172a'; // Deepest dark navy for highest numbers
        diameter = 42;
      }

      return L.divIcon({
        html: `<div class="custom-cluster-marker" style="width:${diameter}px; height:${diameter}px; background:${bg};"><span>${count}</span></div>`,
        className: 'custom-cluster-icon',
        iconSize: L.point(diameter, diameter)
      });
    }"""

# 2. Update cluster CSS and individual event color to #3b82f6
old_css = """    .circle-outer-ring {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: #2563eb;
      border: 2px solid #ffffff;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(15, 23, 42, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
    }"""

new_css = """    .circle-outer-ring {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: #3b82f6; /* Base individual event color: vibrant light blue */
      border: 2px solid #ffffff;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(15, 23, 42, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
    }"""

old_cluster_css = """    /* Cluster Marker */
    .custom-cluster-marker {
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      color: #ffffff;
      font-weight: 800;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 3px 10px rgba(15, 23, 42, 0.4), 0 0 0 2px rgba(255, 255, 255, 0.9);
      font-size: 0.78rem;
    }
    .custom-cluster-marker.small { width: 30px; height: 30px; }
    .custom-cluster-marker.medium { width: 36px; height: 36px; background: linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%); }
    .custom-cluster-marker.large { width: 42px; height: 42px; background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); }"""

new_cluster_css = """    /* Cluster Marker with Blue Shades Progression */
    .custom-cluster-marker {
      color: #ffffff;
      font-weight: 800;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 3px 10px rgba(0, 0, 0, 0.35), 0 0 0 2px rgba(255, 255, 255, 0.95);
      font-size: 0.78rem;
      transition: transform 0.15s ease;
    }
    .custom-cluster-marker:hover {
      transform: scale(1.15);
    }"""

# 3. Remove "Κορυφή..." label from HTML
old_header_html = """    <!-- Annual Trend Curve (Αύξουσα / Φθίνουσα Καμπύλη) -->
    <div class="trend-curve-section">
      <div class="trend-curve-header">
        <span>📈 Ετήσια Καμπύλη Εκδηλώσεων</span>
        <span class="trend-curve-badge" id="trend-peak-indicator">Κορυφή: Σεπ–Οκτ</span>
      </div>"""

new_header_html = """    <!-- Annual Trend Curve (Αύξουσα / Φθίνουσα Καμπύλη) -->
    <div class="trend-curve-section">
      <div class="trend-curve-header">
        <span>📈 Ετήσια Καμπύλη Εκδηλώσεων</span>
      </div>"""

# 4. Prominent Website button in Popup and in Card
old_popup_btn = """      ${item.source_url ? `
      <a href="${encodeURI(item.source_url)}" target="_blank" rel="noopener noreferrer" class="popup-link-btn">
        More info ↗
      </a>` : ''}"""

new_popup_btn = """      ${item.source_url ? `
      <a href="${encodeURI(item.source_url)}" target="_blank" rel="noopener noreferrer" class="popup-btn-site">
        <span>🌐 Επίσκεψη Ιστοσελίδας / Info</span>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>
      </a>` : ''}"""

old_card_btn = """        ${item.source_url ? `
        <a href="${encodeURI(item.source_url)}" target="_blank" rel="noopener noreferrer" class="card-detail-link" onclick="event.stopPropagation();">
          More info ↗
        </a>` : ''}"""

new_card_btn = """        ${item.source_url ? `
        <a href="${encodeURI(item.source_url)}" target="_blank" rel="noopener noreferrer" class="card-btn-site" onclick="event.stopPropagation();">
          <span>🌐 Επίσκεψη Ιστοσελίδας</span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>
        </a>` : ''}"""

# Button CSS
button_styles = """
    .popup-btn-site, .card-btn-site {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      background: #2563eb;
      color: #ffffff !important;
      padding: 5px 11px;
      border-radius: 5px;
      font-size: 0.72rem;
      font-weight: 600;
      text-decoration: none;
      box-shadow: 0 1px 3px rgba(37, 99, 235, 0.3);
      transition: all 0.15s ease;
      margin-top: 4px;
      width: fit-content;
    }
    .popup-btn-site:hover, .card-btn-site:hover {
      background: #1d4ed8;
      box-shadow: 0 3px 8px rgba(37, 99, 235, 0.4);
      transform: translateY(-1px);
    }
"""

# Apply replacements
norm_content = content.replace('\r\n', '\n')

assert old_cluster_func.replace('\r\n', '\n') in norm_content, "old_cluster_func not found"
assert old_css.replace('\r\n', '\n') in norm_content, "old_css not found"
assert old_cluster_css.replace('\r\n', '\n') in norm_content, "old_cluster_css not found"
assert old_header_html.replace('\r\n', '\n') in norm_content, "old_header_html not found"
assert old_popup_btn.replace('\r\n', '\n') in norm_content, "old_popup_btn not found"
assert old_card_btn.replace('\r\n', '\n') in norm_content, "old_card_btn not found"

updated = norm_content.replace(old_cluster_func.replace('\r\n', '\n'), new_cluster_func)
updated = updated.replace(old_css.replace('\r\n', '\n'), new_css)
updated = updated.replace(old_cluster_css.replace('\r\n', '\n'), new_cluster_css + button_styles)
updated = updated.replace(old_header_html.replace('\r\n', '\n'), new_header_html)
updated = updated.replace(old_popup_btn.replace('\r\n', '\n'), new_popup_btn)
updated = updated.replace(old_card_btn.replace('\r\n', '\n'), new_card_btn)

# Also update card click to expand for mapped cards too
old_click = """    document.querySelectorAll('.card-minimal').forEach(c => c.classList.remove('card-active'));
    const el = document.querySelector(`.card-minimal[data-idx="${idx}"]`);
    if (el) el.classList.add('card-active');"""

new_click = """    document.querySelectorAll('.card-minimal').forEach(c => c.classList.remove('card-active'));
    const el = document.querySelector(`.card-minimal[data-idx="${idx}"]`);
    if (el) {
      el.classList.add('card-active');
      el.classList.toggle('is-expanded');
    }"""

if old_click in updated:
    updated = updated.replace(old_click, new_click)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated)

print("Applied all 3 user updates successfully to index.html!")
