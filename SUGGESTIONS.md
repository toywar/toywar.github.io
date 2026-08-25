# CV & website backlog

Improvement ideas that are **not** implemented yet, because each one needs facts
only I can supply — or is a judgement call about what to publish.
(GitHub Issues are disabled on this repo, so this file is the tracker.)

## Content — needs real numbers

- [ ] **Team size in the lead role.** "Leading and mentoring the DevOps &
  infrastructure engineering team" — recruiters scan for the headcount,
  e.g. "leading a team of N engineers".
- [ ] **Certifications section.** Nothing in `_data/` today. CKA/CKS, GCP
  ACE/Professional, Terraform Associate, AWS — anything held would strengthen
  the SRE/lead framing. Needs a new `_data/certifications.yml` plus a section in
  `index.html` and `generate_pdf.py`.
- [ ] **Languages section.** Russian / English / Serbian with levels (CEFR).
  Standard expectation for EU and remote roles, currently absent.
- [ ] **More quantitative results.** `-30%` cost and `99.99%` uptime carry the
  whole numeric story. Candidates: cluster/node counts, services or squads
  supported, transactions per second, incident MTTR, deployment frequency,
  audit outcomes.
- [ ] **Work-authorisation / availability line.** "Belgrade, Serbia" says nothing
  about permits, remote preference, or relocation. One clause in `status_badge`
  (`_data/profile.yml`) would answer the recruiter's first question.
- [ ] **Verify the Asterium wording.** The two bullets were written from the
  public Finharbor/Asterium announcement (hybrid neobank: fiat accounts + card
  issuing, crypto wallets + Mirasmanda, unified KYC/KYB/AML/KYT under NAPP).
  Confirm the scope claims match reality — in particular "led the infrastructure
  workstream" and the data-residency mention.

## Site — small, optional

- [ ] **Link the browser CV.** `cv.html` is published (and in `sitemap.xml`) but
  nothing links to it. A "view in browser" link next to the PDF button lets
  people read it without downloading.
- [ ] **Unused assets.** `avatar.jpeg` (~104 KB) is referenced nowhere, and
  `public/fonts/` holds ~2.8 MB of unused Font Awesome files (already excluded
  from the build, but still in the repo). Safe to delete if not wanted.
- [ ] **Theme default is now the OS colour scheme** when the visitor has no saved
  preference — previously always dark. Revert to dark-always if the dark-first
  look is preferred.
- [ ] **Ambient background intensity** is tunable per theme in
  `assets/css/style.css` via `--bg-hex-opacity`, `--bg-grid-line` and
  `--bg-glow-*`.
- [ ] **`_plugins/ruby32_patch.rb` isn't picked up automatically** on local builds
  with Ruby 3.3 + Liquid 4.0.3 — the build needs
  `bundle exec ruby -r./_plugins/ruby32_patch $(gem environment gemdir)/gems/jekyll-3.9.2/exe/jekyll build`
  to get past `tainted?`. GitHub Pages is unaffected, but bumping the local
  Jekyll/Liquid versions (or noting this in a README) would save time later.

## Done — on `claude/cv-website-updates-rdlp18`

- PCI DSS ownership added to the DevOps Lead role (bullet + tech tag).
- Asterium (UZ) hybrid neobank / digital-asset platform added to both Finharbor
  roles: build-out under DevOps Engineer, delivery workstream under DevOps Lead.
- SEO/social: canonical URL, absolute `og:image`/`og:url`, `og:type=profile`,
  large Twitter card, schema.org `Person` JSON-LD, `jekyll-sitemap`, `robots.txt`.
- Favicon + apple-touch-icon (there was none).
- Accessibility: `aria-expanded`/`aria-pressed`, `aria-hidden` on decorative
  icons, labelled nav CV link, `prefers-reduced-motion` block.
- Perf/bugs: `IntersectionObserver` for section highlighting instead of a
  per-scroll handler; fixed the broken "Operating Systems & Linux" card icon;
  nav bar stays on one line below 480px.
- Ambient Linux/Kubernetes background (terminal grid + hex lattice).
- `generate_pdf.py` finds Chrome via `CHROME_BIN`/PATH/common paths; the PDF is
  still 2 pages after the new bullets.
