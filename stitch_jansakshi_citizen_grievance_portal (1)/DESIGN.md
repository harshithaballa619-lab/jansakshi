---
name: JanSakshi Civic Interface
colors:
  surface: '#f7f9ff'
  surface-dim: '#d0dbea'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#edf4ff'
  surface-container: '#e3effe'
  surface-container-high: '#dee9f8'
  surface-container-highest: '#d8e4f3'
  on-surface: '#111d27'
  on-surface-variant: '#434652'
  inverse-surface: '#26313d'
  inverse-on-surface: '#e8f2ff'
  outline: '#737783'
  outline-variant: '#c3c6d4'
  surface-tint: '#2b5bb5'
  primary: '#003178'
  on-primary: '#ffffff'
  primary-container: '#0d47a1'
  on-primary-container: '#a1bbff'
  inverse-primary: '#b0c6ff'
  secondary: '#a83900'
  on-secondary: '#ffffff'
  secondary-container: '#fc6018'
  on-secondary-container: '#531800'
  tertiary: '#003f0b'
  on-tertiary: '#ffffff'
  tertiary-container: '#14581b'
  on-tertiary-container: '#88cd81'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d9e2ff'
  primary-fixed-dim: '#b0c6ff'
  on-primary-fixed: '#001945'
  on-primary-fixed-variant: '#00429c'
  secondary-fixed: '#ffdbcf'
  secondary-fixed-dim: '#ffb59a'
  on-secondary-fixed: '#380d00'
  on-secondary-fixed-variant: '#802a00'
  tertiary-fixed: '#acf4a4'
  tertiary-fixed-dim: '#91d78a'
  on-tertiary-fixed: '#002203'
  on-tertiary-fixed-variant: '#0c5216'
  background: '#f7f9ff'
  on-background: '#111d27'
  surface-variant: '#d8e4f3'
typography:
  headline-xl:
    fontFamily: Public Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.5px
  headline-xl-mobile:
    fontFamily: Public Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-lg:
    fontFamily: Public Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-lg-mobile:
    fontFamily: Public Sans
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 28px
  headline-md:
    fontFamily: Public Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Public Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  body-lg:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Public Sans
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-sm:
    fontFamily: Public Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-lg:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 20px
    letterSpacing: 0.5px
  label-md:
    fontFamily: Public Sans
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
  label-sm:
    fontFamily: Public Sans
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.5px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system establishes an authoritative, accessible, and deeply trusted civic interface engineered for universal public service delivery across diverse digital literacy levels. Reflecting the visual vernacular of premier Indian digital governance platforms (NIC, CPGRAMS, Spandana, MeeSeva), the interface communicates institutional stability, sovereign integrity, and procedural transparency.

### Core Tenets
- **Institutional Legitimacy:** Structured layouts, sovereign mastheads, bilingual typography (English and Telugu), and civic seals instill immediate citizen confidence.
- **Universal Accessibility (GIGW & WCAG 2.1 AAA Compliance):** Ultra-high contrast ratios, explicit hit areas (minimum 48px), persistent text-scaler utilities (A- / A / A+), and semantic navigation ensure frictionless use for senior citizens and low-vision rural users.
- **Utilitarian Predictability:** Complete absence of startup tropes (no frosted glass, non-standard floating action buttons, dark mode novelties, or abstract decorative blobs). Every container uses explicit borders, structured tabular forms, and dependable visual boundaries.

## Colors

The palette employs authentic Indian institutional colors anchored in civic authority and sovereign identity:

- **Primary (`#0D47A1` - Sovereign Navy):** Applied to the main masthead bar, primary action buttons, active navigation states, and official headers. Evokes bureaucratic integrity and dependability.
- **Secondary (`#E65100` - Kesari / National Saffron):** High-priority alerts, civic urgency markers, active indicator pips, call-to-action buttons for urgent grievance filings, and the upper stripe of the civic tri-color rule.
- **Tertiary (`#1B5E20` - India Green):** Verified status badges, successfully resolved grievance markers, secure token verification, and the lower accent band.
- **Neutral Palette:**
  - **Base Canvas (`#F4F7F9`):** A soft, pale grey-blue slate background eliminating glare on low-end budget displays while preserving crisp card contrast.
  - **Surface White (`#FFFFFF`):** High-contrast background for data tables, form fields, and citizen grievance cards.
  - **Neutral Deep Ink (`#1A2530`):** Ultra-dark, high-contrast body text ensuring strict compliance with accessibility standards (minimum 7:1 contrast on white).
  - **Border Gray (`#B0BEC5` / `#CFD8DC`):** Distinct, un-blurred 1px to 2px structural containment lines for form groups, tables, and notices.
  - **Government Gold / Amber (`#FFD54F`):** Dedicated navigation hover highlights and skip-to-content focus indicators.

## Typography

The design system uses **Public Sans**—an open, government-grade geometric grotesque engineered for legibility across varied device resolutions. When rendering regional Indian languages (specifically Telugu for 'జనసాక్షి AI'), Noto Sans Telugu serves as the co-primary fallback, harmonizing weight and baseline metrics.

### System Principles
- **Global Font Scaler Support:** All baseline font sizes scale proportionally via root REM increments when citizens engage the top-tier accessibility toggles (`A-` = 90%, `A` = 100%, `A+` = 115%).
- **High-Density Legibility:** Generous line heights prevent optical crowding in complex administrative tables, grievance petition tracking timelines, and bilingual statutory notices.
- **Bilingual Stacking:** Where Telugu and English appear simultaneously (e.g., in field headers or status tags), the vernacular text renders directly beneath the English label at `body-sm` (13px) with standard 500 weight.

## Layout & Spacing

Layouts adhere to an unyielding, structured 12-column grid optimized for desktop civic back-offices and mobile kiosks.

### Grid & Composition Rules
- **Desktop (1200px+):** Fixed max-container of 1280px centered on screen. 12 columns with 24px (`1.5rem`) gutters and 40px (`2.5rem`) outer canvas margins.
- **Tablet (768px - 1199px):** 8 columns with 16px (`1rem`) gutters and 24px margins. Tabular content remains horizontal with designated scroll gutters.
- **Mobile (< 768px):** 4 columns with 16px (`1rem`) gutters and 16px (`1rem`) margins. Multi-column civic forms collapse into vertical single-column stacks with mandatory minimum 48px touch barriers.

### Layout Chrome Architecture
1. **Top Utility Bar (Height: 36px):** Dark Navy (`#0A2540`) containing the Indian Flag emblem, Emergency Helpline ('112 / 1905'), 'Skip to Main Content' anchor, screen-reader audio mode, and text scale switches (`A- | A | A+`).
2. **Main Masthead (Height: 88px):** Clean white container featuring the National / State emblem at left, Portal Title (`JanSakshi AI / జనసాక్షి AI`) in bold serif-influenced Public Sans, and citizen profile / Grievance ID quick-search on the right.
3. **Primary Horizontal Navigation Bar:** Deep Navy (`#0D47A1`) full-bleed bar featuring home, new grievance submission, grievance status tracker, departmental dashboards, and RTI / citizen charter links. Hover states utilize bold Government Amber (`#FFD54F`) underlines.
4. **Official Bulletin / Marquee Ticker:** A high-contrast Saffron-accented horizontal ticker immediately below navigation for public notices and municipal advisories.

## Elevation & Depth

To reflect functional realism and bureaucratic durability, this design system avoids soft shadows, multi-layered depth, or floating components. Visual differentiation is achieved through **low-contrast outlines, high-contrast borders, and structured surface tiers**:

- **Level 0 (Canvas Base):** Off-white `#F4F7F9` background.
- **Level 1 (Card & Content Blocks):** Pure white `#FFFFFF` surface enclosed by a solid 1px border (`#CFD8DC`). No box-shadow.
- **Level 2 (Active Modules & Form Focus):** White background enclosed by a solid 2px primary border (`#0D47A1`).
- **Level 3 (Modal Dialogs & Critical Alert Banners):** Crisp 1px solid border (`#90A4AE`) with a strict, minimal operational drop shadow: `0 4px 6px -1px rgba(11, 37, 64, 0.12), 0 2px 4px -1px rgba(11, 37, 64, 0.08)`.
- **National Tricolor Accent Rule:** Critical official headers and mastheads incorporate a structural 3px horizontal divider line composed of linear thirds: Saffron (`#E65100`), White (`#FFFFFF`), and Green (`#1B5E20`).

## Shapes

The design system strictly adheres to **Level 0 (Sharp)** corner styling. 

- All buttons, input fields, notification banners, status chips, table containers, and modal dialogs use `0px` border-radius.
- Rectangular sharpness conveys official permanence, legal standing, and systematic structure.
- Micro-elements such as checkboxes and radio selectors remain crisp geometric forms (square checkboxes and concentric circular radio inputs with no smoothed inner bezels).

## Components

### Buttons
- **Primary Civic Action (Submit Grievance / శోధించండి):** Solid Navy (`#0D47A1`) fill, crisp white text, 0px border radius, min-height 48px, horizontal padding `1.5rem` (`space-lg`). 1px border (`#082E6B`). Hover shifts to `#0A3880`. Focus ring: 3px solid `#FFD54F` with 2px offset.
- **Secondary / Action (Draft / Reset):** Pure white fill, Navy (`#0D47A1`) text, 2px solid Navy border. Hover shifts to `#F4F7F9`.
- **Urgent / Emergency Action (Escalate / Police & Disaster):** Solid Kesari Saffron (`#E65100`) fill, white text, 1px border (`#BF360C`). Hover shifts to `#D84315`.
- **Text / Utility Actions:** Underlined, Navy text with bold chevron indicators (`→`).

### Input Fields & Form Controls
- **Form Fields:** White background, 1.5px solid `#78909C` border, 0px border radius. Padding: `0.75rem` vertical by `1rem` horizontal. Required markers use distinct red asterisks (`#C62828`).
- **Focus State:** 2px solid `#0D47A1` border with no ambient blur.
- **Bilingual Field Labels:** Top-aligned; English headline (`label-lg`) paired with Telugu subtext in muted `#455A64`.
- **Validation Messages:** Inline boxes with solid left border (3px) in Green (`#1B5E20`) for valid or Crimson (`#C62828`) for error, accompanied by clear descriptive icons.

### Badges & Grievance Status Chips
- **Geometry:** Sharp rectangular tags (padding: `0.25rem 0.75rem`), uppercase `label-sm` bold font.
- **Submitted / Pending:** Muted Amber background (`#FFF8E1`), border 1px solid (`#FFE082`), text `#E65100`.
- **In Inquiry / Assigned:** Sky tint background (`#E3F2FD`), border 1px solid (`#90CAF9`), text `#0D47A1`.
- **Redressed / Resolved:** Light Green background (`#E8F5E9`), border 1px solid (`#A5D6A7`), text `#1B5E20`.
- **Rejected / Escalated:** Light Red background (`#FFEBEE`), border 1px solid (`#FFCDD2`), text `#C62828`.

### Data Tables (Grievance Log / Public Ledger)
- **Header:** Deep Navy `#0D47A1` background with white text (`label-lg`), vertical dividers in `#1565C0`.
- **Rows:** Alternating zebra striping (Row A: `#FFFFFF`, Row B: `#F8FAFC`). Row borders: 1px solid `#CFD8DC`.
- **Row Height:** Roomy 52px baseline for touch-friendly row selection and tracking expansion.

### Citizen Alert Marquee Ticker
- Deep saffron `#E65100` label box ("LATEST ANNOUNCEMENTS / తాజా సమాచారం") pinned to the left, with an off-white `#FFF3E0` scrolling belt showing hyperlinked departmental notifications bordered by a 1px solid `#FFE082` frame.

### Official Municipal Helpdesk Footer
- Deep institutional Navy (`#0A2540`) background. 4-column structured footer detailing NIC hosting disclaimers, GIGW compliance badges, toll-free grievance helplines (1800-series), website policy links, and last-updated statutory timestamps.