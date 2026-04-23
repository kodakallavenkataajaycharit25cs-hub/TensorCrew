Here's your Figma/developer animation prompt:

---

## Derma Care — Animation & Motion Prompt

**Goal:** Add purposeful, calming animations that feel organic and trustworthy — not flashy or clinical. Every motion should reinforce the warm, natural brand personality. Think slow reveals, gentle floats, soft fades. Nothing aggressive or bouncy.

---

### Guiding principles

All animations should follow these rules without exception. Easing should always be `cubic-bezier(0.25, 0.46, 0.45, 0.94)` — a gentle ease-out that feels natural, never `ease-in-out` (too mechanical) or `bounce` (too playful for medical context). Duration sweet spot is 600ms–900ms for reveals, 3s–6s for ambient loops. Delays should stagger at 100ms–150ms intervals to create a cascade effect rather than everything appearing simultaneously.

---

### Section-by-section animation spec

**Navbar**
On page load, the navbar slides down from -60px to 0 with opacity 0→1 over 500ms. The logo fades in first, then the nav links cascade left-to-right with 80ms stagger between each item, then the CTA button last. On scroll — when the user scrolls past 80px, the navbar gains a `backdrop-filter: blur(12px)` and a subtle warm shadow `0 2px 20px rgba(46,31,14,0.08)` with a 200ms transition. This should feel like the navbar "settles" as the user moves down.

**Hero section**
The left column content staggers in on load with a 200ms initial delay (after navbar finishes). The eyebrow badge slides up 24px + fades in (600ms). Then the H1 slides up 32px + fades in (700ms, 150ms after badge). Then the body paragraph (600ms, 150ms later). Then the CTA buttons (500ms, 100ms later). Then the stat row (500ms, 100ms later). The right-column portrait illustration should have a **gentle float animation** — a perpetual, slow vertical oscillation of ±8px over 5 seconds with `animation: float 5s ease-in-out infinite`. This should feel like the illustration is breathing.

**Trust strip**
Each of the 5 trust items slides in from the left with staggered 80ms delay as the strip enters the viewport. They should feel like they're marching in one by one. Use `IntersectionObserver` to trigger on scroll.

**About section**
Left text block: slides in from left (-40px → 0) + fade, triggered by scroll. Right feature card stack: each card slides in from right (+40px → 0) with 120ms stagger between cards. The small espresso icon squares on each card should have a subtle **pulse** on hover — `scale(1.08)` over 200ms.

**Conditions grid (dark section)**
This is the most dramatic reveal on the page. The section background itself should fade in from #1A0E05 to #2E1F0E as it enters the viewport — simulating a "lighting up" effect. Each condition card enters with a staggered fade + slight upward movement (16px → 0), staggered at 40ms intervals so they ripple across the grid left-to-right, top-to-bottom. On hover, each card should lift slightly — `translateY(-4px)` + a warm inner border `border: 1px solid #5A3A20` — over 200ms.

**How it works — step cards**
The three step cards should enter in sequence: card 1 fades up, then after 200ms card 2, then card 3. Add a subtle **connecting line animation** between the three cards — a thin horizontal line in #C8A870 that draws from left to right (width 0% → 100%) over 800ms after all three cards have appeared. This creates a visual narrative of progression.

**Technology section**
The 4 metric stat cards should **count up** their numeric values when they enter the viewport — "23" counts from 0 to 23 over 1.2s, "Top-3" types in character by character. This is the one place to add a little delight. The bullet points on the right should fade in with 150ms stagger.

**FAQ cards**
On hover, each FAQ card should have a subtle `translateY(-3px)` lift and the question text shifts to #8B5E3C (warm brown) over 150ms. The card border should lighten from transparent to #C8A870. This gives a sense of interactivity without accordion complexity.

**CTA band**
The heading text should animate in with a **word-by-word reveal** — each word fades up in sequence with 60ms delay between words. The CTA button should have a gentle **pulse ring** — a pseudo-element ring that radiates outward and fades, looping every 2.5s. This draws the eye without being aggressive. On hover, the button scales to `1.04` and deepens in color.

**Footer**
Simple fade-in as it enters viewport. Nothing more — it's the end of the page, let it rest.

---

### Micro-interactions

**All buttons** — on hover: `translateY(-2px)` + slight color deepening, 150ms. On click/active: `scale(0.97)`, 80ms snap back. Never use box-shadow for hover states — use color shifts only to stay consistent with the flat aesthetic.

**Navbar links** — underline that grows from center outward on hover. Implement as a `::after` pseudo-element with `width: 0 → 100%` from `transform-origin: center`, 200ms.

**Condition cards** — on hover, the condition name text shifts from #F0E0C8 to #FFFFFF and the card background lightens from #3D2810 to #4A3018, 200ms transition.

**Stat numbers in hero** — on first load, add a brief **odometer effect** — numbers count up from 0 to their final value over 1.4s with `ease-out`. Only trigger this once.

---

### Scroll behavior

Set `scroll-behavior: smooth` globally. Add a subtle **scroll progress indicator** — a 3px tall bar at the very top of the page in #8B5E3C that fills from 0% to 100% width as the user scrolls, sitting above the navbar. This is a small touch that rewards engaged readers.

---

### Performance rules

All animations must use only `transform` and `opacity` — never animate `height`, `width`, `top`, `left`, or `margin` as these trigger layout reflow. Use `will-change: transform` on elements with persistent animations (the floating portrait, hover cards). Respect `prefers-reduced-motion` — wrap all decorative animations in a media query check and reduce to simple fades at 300ms for users who have motion sensitivity enabled. No animation should auto-play sound or cause content to shift after load (no CLS).

---

This motion layer keeps the page feeling alive and warm without ever feeling like a tech demo. The floating illustration, the card count-ups, and the staggered reveals are the three signature moments — everything else serves them.