# Interaction Patterns & Micro-Interactions

- **Buttons**: instantaneous response on press (color/highlight, brief scale or brightness change). After the action completes, show the result (a check icon morphing in, or a toast notification).
- **Form elements**: animate focus (underline expand, background highlight). On validation error, a brief shake or border color transition draws attention without being disruptive.
- **Toggle switches/checkboxes**: animate the thumb position and background color smoothly.
- **Progress feedback**: long tasks get a progress bar or spinner — e.g. an upload button can transition into an embedded progress indicator.
- **Drag-and-drop**: drag-over highlighting or placeholder animations so the drop target is unambiguous.
- **Scroll-based effects**: parallax or fade-on-scroll must be optional/subtle — heavy scroll-linked animation risks vestibular discomfort for some users.
- **Micro-interactions**: a "like" button that briefly bursts or pulses, pull-to-refresh, a drawer that reveals a hidden menu.

Each micro-interaction needs a clear trigger and outcome, should take minimal time (roughly 100–300ms), and should loop only while the user is actually waiting on something. Treat any complex micro-interaction (e.g. an avatar flying into a header) as a Level 3 (visual/risk) review item — check performance and accessibility before keeping it.
