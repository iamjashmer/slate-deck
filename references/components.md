# Slide building blocks

Everything here works in a fragment slide. Sizes are stage pixels (the stage is 1920 × 1080).

## Tokens

Use these instead of colors and fonts; every theme sets them.

| Token | Use |
|---|---|
| `--cream` | Slide ground |
| `--paper` | Cards, table and chart surfaces |
| `--white` | Controls (chips, round buttons) |
| `--navy` | Text |
| `--muted` | Secondary text |
| `--orange` | The one accent: tiles, bars, dots, focus |
| `--orange-ink` | Accent as text (eyebrows, highlighted words) |
| `--on-accent` | Text or icons placed on `--orange` |
| `--line`, `--line-strong` | Hairlines and card borders |
| `--tint`, `--tint-strong` | Quiet fills |
| `--panel-dark`, `--ink`, `--ink-muted` | Dark bands (`.panel`, `.code`) and their text |
| `--success`, `--error` | Right and wrong |
| `--font-sans`, `--font-display` | Body and headline fonts |
| `--pad-x` (128), `--pad-y` (104), `--gap` (28) | Stage padding and spacing |

`data-theme="dark"` on any element switches it and its children to the theme's contrast palette (a dark band in light themes, a light one in dark themes).

## Classes

| Class | What it is |
|---|---|
| `stage` | The slide frame: full size, padded, a column with `gap`. Add `center` (vertically centered) or `middle` (centered both ways). Wrap each slide's content in `<main class="stage">`. |
| `contour` | Animated contour-line ground. Put `<div class="contour"></div>` before the stage. |
| `eyebrow` | Small uppercase kicker in the accent |
| `display`, `h1`, `h2`, `h3` | Headlines (176, 112, 76, 44 px) in the display font |
| `lead` | Large muted paragraph (38px) |
| `small`, `muted`, `accent`, `num`, `label`, `card-title` | Text helpers |
| `row`, `stack`, `spacer` | Flex row, flex column, flexible gap |
| `grid cols-2/3/4 rows-2` | Bento grid filling the rest of the stage |
| `split` | Two columns, vertically centered |
| `card` (+ `lift` for hover) | Paper card; `.desc` inside for muted text |
| `tile` | Orange 64px icon tile |
| `chip` (+ `<span class="dot"></span>`) | Pill label |
| `cta` | The navy pill button (one per slide) |
| `btn` | Round secondary button |
| `kbd` | Keyboard key |
| `list` | Bulleted list with orange dots |
| `choices` + `choice` (`.key` inside), `feedback` | Multiple-choice quiz parts; add `is-correct` / `is-wrong` |
| `stat` (`.v`, `.l`) | Big number with a label |
| `panel` | Dark rounded band |
| `code` | Code block on a dark panel |
| `table` | Themed table |
| `rise d1…d4` | Entrance animation with staggered delays |
| `box` + `data-box` | Free-floating, draggable element (needs `left`/`top`) |
| `text-box`, `shape` | Box presets: 36px text; accent-filled shape |

Icons: inline SVG at `viewBox="0 0 24 24"`, `fill="none" stroke="currentColor" stroke-width="2"`, Phosphor style.

## Patterns

### Title
```html
<div class="contour"></div>
<main class="stage center">
  <span class="eyebrow rise">Lesson one</span>
  <h1 class="display rise d1">Fractions you<br><span class="accent">can see.</span></h1>
  <p class="lead rise d2">By the end you can compare two fractions without a calculator.</p>
  <div class="row rise d3" style="margin-top: 24px"><span class="chip"><span class="dot"></span>Ms. Rivera · Grade 4</span></div>
</main>
```

### Section divider
```html
<main class="stage center" data-theme="dark">
  <span class="h1 accent num" style="font-size: 240px; line-height: 1">02</span>
  <h2 class="h1">Comparing fractions.</h2>
</main>
```

### Four cards
```html
<main class="stage">
  <div class="stack"><span class="eyebrow">Overview</span><h2 class="h2">Four ideas for today.</h2></div>
  <div class="grid cols-2 rows-2">
    <article class="card lift">
      <div class="row" style="gap: 20px"><span class="tile"><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 12 5 5L20 7"/></svg></span><span class="card-title">Notice</span></div>
      <p class="desc">Describe what you see before you explain it.</p>
    </article>
    <!-- three more cards -->
  </div>
</main>
```

### Points one click at a time
```html
<main class="stage">
  <div class="stack"><span class="eyebrow">Step by step</span><h2 class="h2">How to compare.</h2></div>
  <ul class="list" style="font-size: 42px; gap: 34px; margin-top: 24px">
    <li data-step>Find a common denominator.</li>
    <li data-step>Rewrite both fractions.</li>
    <li data-step>Compare the numerators.</li>
  </ul>
</main>
```

### Quick check (self-marking quiz)
```html
<main class="stage">
  <div class="stack"><span class="eyebrow">Quick check</span><h2 class="h2">Which is larger?</h2></div>
  <div class="choices" id="quiz" data-answer="b">
    <button class="choice" data-id="a"><span class="key">A</span>2/3</button>
    <button class="choice" data-id="b"><span class="key">B</span>3/4</button>
  </div>
  <p class="feedback" id="feedback" aria-live="polite"></p>
</main>
<script>
  const quiz = document.getElementById('quiz');
  quiz.addEventListener('click', (e) => {
    const choice = e.target.closest('.choice');
    if (!choice) return;
    const right = choice.dataset.id === quiz.dataset.answer;
    choice.classList.add(right ? 'is-correct' : 'is-wrong');
    const fb = document.getElementById('feedback');
    fb.textContent = right ? 'Yes: 9/12 is more than 8/12.' : 'Not quite. Try twelfths.';
    fb.style.color = right ? 'var(--success)' : 'var(--error)';
  });
</script>
```

### Table
```html
<main class="stage">
  <div class="stack"><span class="eyebrow">Compare</span><h2 class="h2">Halves, thirds, quarters.</h2></div>
  <table class="table">
    <thead><tr><th>Fraction</th><th>Twelfths</th><th>Decimal</th></tr></thead>
    <tbody>
      <tr><td>1/2</td><td>6/12</td><td>0.5</td></tr>
      <tr><td>2/3</td><td>8/12</td><td>0.67</td></tr>
    </tbody>
  </table>
</main>
```
In a box (`<div class="box" data-box style="left: 300px; top: 330px; width: 1320px;">…</div>`) the user can drag it and add rows and columns in Slate.

### Chart
Data lives in a JSON script; Slate draws it in the theme's colors. `type` is `bar`, `line` or `pie`; `labels` and `values` have the same length.
```html
<main class="stage">
  <div class="stack"><span class="eyebrow">Results</span><h2 class="h2">Scores rose each week.</h2></div>
  <div class="box" data-box style="left: 460px; top: 330px; width: 1000px; height: 620px;">
    <figure class="chart" data-chart><script type="application/json">{"type":"bar","labels":["Week 1","Week 2","Week 3"],"values":[12,18,22]}</script></figure>
  </div>
</main>
```

### Picture with a prompt
```html
<main class="stage">
  <div class="split" style="grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr)">
    <img src="assets/pizza.jpg" alt="A pizza cut into eight slices" style="width: 100%; height: 760px; object-fit: cover; border-radius: var(--radius-card)">
    <div class="stack" style="gap: 26px">
      <span class="eyebrow">Look closely</span>
      <h2 class="h2">How much is left?</h2>
    </div>
  </div>
</main>
```

### Free text box and shapes
```html
<div class="box text-box" data-box style="left: 1240px; top: 860px; width: 520px;"><p>Bring a pencil.</p></div>
<div class="box shape" data-box style="left: 120px; top: 760px; width: 300px; height: 180px; border-radius: 24px;"></div>
```
Place boxes inside `<main class="stage">` so their coordinates are stage pixels.

### Avatar timer (activity countdown)
Use this for any timed activity. Slate 1.1 and later have a living avatar built in: he stands next to a cute alarm clock and reacts as time runs. He presents it at the start, gives a thumbs up at halfway, warns at 1 minute and at 10 seconds, then celebrates at zero with a chime and confetti. The presenter clicks the clock to start and pause it, also from their live view, and hovers it for reset and +1 minute. Every slide with an avatar timer needs the module script.
```html
<main class="stage">
  <div class="split" style="grid-template-columns: minmax(0, 1fr) 900px; gap: 40px">
    <div class="stack">
      <span class="eyebrow">Turn and talk</span>
      <h2 class="h2">Which is bigger, 3/5 or 5/8?</h2>
      <ul class="list lead" style="margin-top: 24px">
        <li>Find a partner next to you</li>
        <li>Each of you explains one way to compare</li>
      </ul>
    </div>
    <avatar-timer duration="2:00" label="Turn and talk" style="width: 900px"></avatar-timer>
  </div>
</main>
<script type="module" src="_slate/avatar/avatar-timer.js"></script>
```
- `duration`: `"3:00"`, `"90"` (seconds), `"1:30:00"`, `"5m"`, `"1m 30s"`. The halfway cheer needs 1 minute or more, the 1-minute warning 2 minutes or more, and the 10-second warning 20 seconds or more.
- `label`: a few words inside the clock. Match the eyebrow.
- `autostart`: starts when the slide appears in the show (never while editing). Good for short timers like a 20-second quiz; leave it off when the presenter explains the task first.
- The width sets the size, and the height follows (about 7 : 8, plus his speech bubble above). 900px suits an activity slide.
- To put the clock on his left, add `side="right"`. He then stands on the right and points at it.
- Bubble text can be changed with `text-start`, `text-half`, `text-warn`, `text-final` and `text-end`, for example `text-end="Pencils down!"`. `muted` turns the sound off.
- The clock keeps its own colors on every theme. To match the deck's accent, add `style="--timer-color: var(--orange)"`.
- A countdown stops when the presenter leaves its slide. In the notes, say how long the activity is and that clicking the clock starts it.

### Avatar pace clock (talk timing)
A small avatar with a talk clock in a slide corner. While presenting, it follows the timer in Slate's presenter view, so it starts with the show and pauses and resets with it, with nothing to click. It shows the time left in the talk. `expect` is where the talk should be by this slide. When the slide appears, he says whether the presenter is ahead, on time (within 30 s), a little behind or way behind (over 2 minutes).
```html
<div class="box" data-box style="left: 1480px; top: 690px; width: 400px;"><avatar-timer mode="pace" duration="20:00" expect="8:00" style="width: 100%"></avatar-timer><script type="module" src="_slate/avatar/avatar-timer.js"></script></div>
```
- `duration` is the whole talk's length. Give every pace clock in the deck the same one.
- `expect` is the time planned for all the slides before this one. In a 20-minute talk planned at a minute a slide, slide 9 gets `expect="8:00"`.
- Put pace clocks on a few checkpoint slides (section starts, the middle, before the wrap-up), not on every slide. He reacts each time one appears.
- Keep the box clear of the slide's content: the bottom-right corner (as above), or `left: 40px` with `side="right"` for the bottom-left.
- `tolerance="1:00"` widens "on time" from 30 seconds.

### Live poll, slider model, embedded page
Slate's own modules (Slide › New Slide in the app) include a tap-to-vote poll, an interactive fraction model and a framed web page. When a slide needs one of these, keep the script self-contained and drive every visible state from the theme tokens.
