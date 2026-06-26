# HSS Theme — Block Class Reference

Add these via: Block → Advanced → Additional CSS class(es)

---

## SECTIONS (apply to Group blocks)

| Class                  | Effect                              |
|------------------------|-------------------------------------|
| hss-section            | Full-width section + padding        |
| hss-section--sand      | Sand/cream background               |
| hss-section--dark      | Navy background + white text        |
| hss-section--redwood   | Deep red background + white text    |
| hss-container          | Max-width centered content wrapper  |
| hss-center             | Center-align text & inline content  |

> Typical pattern: outer Group = `hss-section hss-section--dark`
>                  inner Group = `hss-container`

---

## TYPOGRAPHY

| Class              | Effect                              |
|--------------------|-------------------------------------|
| hss-label          | Tiny all-caps section label         |
| hss-title          | Large bold heading                  |
| hss-subtitle       | Italic serif supporting text        |
| hss-tagline        | Italic amber tagline                |
| hss-color--seafoam | Text color: seafoam green           |
| hss-color--amber   | Text color: amber/gold              |
| hss-color--redwood | Text color: deep red                |
| hss-color--white   | Text color: white                   |

---

## BUTTONS (apply to the Button block)

| Class              | Effect                              |
|--------------------|-------------------------------------|
| hss-btn--primary   | Red filled button                   |
| hss-btn--secondary | Seafoam outline button              |
| hss-btn--white     | White outline (for dark sections)   |

---

## CARDS (Group blocks)

| Class          | Effect                                      |
|----------------|---------------------------------------------|
| hss-cards      | Auto-fit grid wrapper for cards             |
| hss-card       | Sand card, seafoam top border, hover lift   |
| hss-card-icon  | Large emoji/icon display                    |

---

## SERVICE TILES (for navy sections)

| Class              | Effect                              |
|--------------------|-------------------------------------|
| hss-service-grid   | Auto-fit grid wrapper for tiles     |
| hss-service-tile   | Translucent tile with hover effect  |

---

## TAGS / PILLS

| Class      | Effect                              |
|------------|-------------------------------------|
| hss-tags   | Flex wrap container                 |
| hss-tag    | Individual pill — add to Paragraph  |

---

## HERO (apply to a full-width Group block)

| Class          | Effect                              |
|----------------|-------------------------------------|
| hss-hero       | Dark gradient hero background       |
| hss-hero-logo  | Animated floating logo image        |
| hss-hero-cta   | Flex row for hero buttons           |

---

## NAV ANCHORS

Set these in Block → Advanced → HTML anchor on your section Group blocks
so the nav links scroll to the right spot:

| Anchor         | Nav link        |
|----------------|-----------------|
| hss-why        | Why Us          |
| hss-services   | Services        |
| hss-who        | Who We Serve    |
| hss-poopstakes | Poopstakes      |
| hss-contact    | Get a Quote     |

---

## LOGO

Upload your logo via Appearance → Customize → Site Identity → Logo
The nav will use it automatically.

Or drop logo_clean.jpg directly into the theme's /assets/ folder via FTP.
