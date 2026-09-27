# Iconography Guidelines

## Design & style

Icons should follow a consistent style aligned with the platform or brand (e.g. Material Icons, SF Symbols). Consistency in stroke width, corner rounding, and fill (outline vs. filled) is critical. Define a token set for icon sizes (e.g. 16/24/32px) and standard colors (primary, secondary, disabled).

## Formats

SVG is preferred for UI icons — it scales cleanly and can be styled with CSS. Icon fonts (Font Awesome, Material Icons font) need proper fallbacks (they can flash unstyled) and map icons to text glyphs, so handle `font-feature-settings` carefully. Avoid large bitmap (PNG) icons. For animated icons, use SVG+CSS or Lottie for complex sequences.

## Accessibility

Every non-decorative icon needs an accessible name.

```html
<svg role="img" width="24" height="24" aria-labelledby="iconTitle">
  <title id="iconTitle">Search</title>
  <use xlink:href="#search-icon"></use>
</svg>
```

If the icon is purely decorative (paired with visible text that already names the function), mark it `aria-hidden="true"` so assistive tech ignores it. Never ship an unlabeled icon-only button.

## Sizing & touch targets

Per WCAG 2.5.5, interactive icon targets (icons inside buttons, tap areas) should be at least 44×44 CSS px unless an equivalent control sits nearby. On high-DPI screens, use higher-resolution SVG/icon-font rendering to avoid blur.

## Color & contrast

Icons are UI elements and must meet normal contrast rules (≥4.5:1 for small icons is a reasonable bar to check against). Never convey meaning by color alone — pair a color cue with a shape or label difference.

## Icon tokens (example)

```css
--icon-size-xs: 16px;
--icon-size-sm: 20px;
--icon-size-md: 24px;
--icon-size-lg: 32px;
--icon-color-primary: #333;
--icon-color-secondary: #888;
--icon-color-disabled: #CCC;
--icon-stroke-width: 2px;
```

Use these tokens even when mixing multiple icon libraries, so appearance stays normalized across the product.

## Organization

Use an SVG sprite or a component-based icon system (e.g. `<use>` references, or per-icon React/Vue components like Heroicons) to minimize HTTP requests and keep icon usage consistent and swappable.

## Sample React icon component

```jsx
const IconSearch = ({ size = 24, color = "#000", label = "Search" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24"
       fill="none" stroke={color} aria-label={label} role="img">
    <title>{label}</title>
    <circle cx="11" cy="11" r="7" strokeWidth="2"/>
    <line x1="16" y1="16" x2="22" y2="22" strokeWidth="2"/>
  </svg>
);
```
