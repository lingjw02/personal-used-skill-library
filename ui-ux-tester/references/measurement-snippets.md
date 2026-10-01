# Measurement Snippets

Run these through the browser tool's "evaluate JavaScript" / DevTools console on the live page, to get real values instead of eyeballing. They only read the page. Pair them with screenshots. If your driver cannot execute JS, estimate from screenshots and label values `approx.`

## Contents
- Computed style of an element
- Interactive element audit (names, sizes)
- Focus indicator check
- Horizontal overflow finder
- Style inventory for design-system extraction
- Contrast (use scripts/contrast.py)

## Computed style of an element
```js
(sel) => { const e = document.querySelector(sel); if(!e) return null; const s = getComputedStyle(e);
  return {color:s.color, bg:s.backgroundColor, font:`${s.fontSize}/${s.lineHeight} ${s.fontWeight} ${s.fontFamily}`,
  radius:s.borderRadius, shadow:s.boxShadow, border:s.border, padding:s.padding, margin:s.margin, cursor:s.cursor,
  outline:s.outline, size:e.getBoundingClientRect().toJSON()}; }
```
Note: `backgroundColor` may be transparent; walk up parents to find the effective background before computing contrast.

## Interactive element audit (names and target size)
```js
[...document.querySelectorAll('a,button,input,select,textarea,[role=button],[role=link],[tabindex]')].map(e=>{
  const r=e.getBoundingClientRect(); const name=(e.getAttribute('aria-label')||e.innerText||e.value||e.title||e.placeholder||'').trim().slice(0,40);
  const label=e.id&&document.querySelector(`label[for="${e.id}"]`)?.innerText;
  return {tag:e.tagName.toLowerCase(), name, hasLabelFor:!!label, w:Math.round(r.width), h:Math.round(r.height), visible:r.width>0&&r.height>0};
}).filter(x=>x.visible && (!x.name && !x.hasLabelFor || x.w<24 || x.h<24))
```
Returns controls that lack an obvious accessible name or are smaller than about 24px. Each hit needs manual confirmation (a name can come from `aria-labelledby`, a wrapping label, or an SVG title).

## Focus indicator check
After pressing Tab, inspect the focused element:
```js
(()=>{const e=document.activeElement, s=getComputedStyle(e); return {el:e.tagName+'.'+e.className, outline:s.outline, outlineOffset:s.outlineOffset, boxShadow:s.boxShadow, border:s.border};})()
```
`outline: none` with no box-shadow/border change suggests an invisible focus indicator. Confirm visually with a screenshot.

## Horizontal overflow finder
```js
(()=>{const vw=document.documentElement.clientWidth; return {pageScrollsX: document.documentElement.scrollWidth>vw,
 offenders:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>vw+1).slice(0,15).map(e=>e.tagName+'.'+e.className)};})()
```
Run after each viewport resize.

## Style inventory for design-system extraction
```js
(()=>{const c=(m,v)=>m.set(v,(m.get(v)||0)+1); const col=new Map(),bg=new Map(),rad=new Map(),fs=new Map(),sh=new Map();
 document.querySelectorAll('body *').forEach(e=>{const s=getComputedStyle(e); if(!e.getBoundingClientRect().width) return;
  c(col,s.color); if(s.backgroundColor!=='rgba(0, 0, 0, 0)') c(bg,s.backgroundColor); c(rad,s.borderRadius); c(fs,s.fontSize+' / '+s.fontWeight); if(s.boxShadow!=='none') c(sh,s.boxShadow);});
 const top=m=>[...m.entries()].sort((a,b)=>b[1]-a[1]).slice(0,8); return {text:top(col),bg:top(bg),radius:top(rad),type:top(fs),shadow:top(sh)};})()
```
Counts show which values dominate (likely the system) and the long tail (likely inconsistencies). Run per page and compare.

## Contrast
Use the bundled calculator with measured foreground/background values:
```bash
python scripts/contrast.py "rgb(107,114,128)" "#ffffff" --size 14 --bold false
```
Thresholds applied (WCAG 2.x reference values): 4.5:1 normal text, 3:1 large text (>=24px, or >=18.66px bold) and non-text UI components. Report the measured ratio and context; this is a measurement, not a compliance audit.
