# zclap-site

New zclap.com: plain HTML and CSS, no build step. Preview on GitHub Pages: https://doggo21345.github.io/zclap-site/

- `index.html`: homepage. `healthcare/index.html`: healthcare landing page (the outreach kit's Industries tab links healthcare prospects here).
- `styles.css`, `site.js`: shared by every page. Fonts: Source Serif 4 + IBM Plex Sans (Google Fonts).
- Tracking: the existing Google tag (GA4 + Ads). Events: `estimator_start` (with `project_type`), `generate_lead`, and CTA clicks named by `data-track`.

New industry page: copy `healthcare/`, change the copy, link it from the Industries section, and put its path in the outreach kit's Industries tab > Landing page.

Before going live on zclap.com:
1. Remove the `noindex` meta tag on every page.
2. Point estimator links back to `/estimator/index.html` (they use https://zclap.com/estimator/ for the preview).
3. Team: real photos, names, titles, bios. Confirm the founder bio.
4. Confirm the client logos may be shown.
5. Add Microsoft Clarity (see the comment in `index.html`).
