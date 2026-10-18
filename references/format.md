# The .slate deck format

A deck is a folder whose name ends in `.slate`. Finder shows it as one file and Slate opens it directly.

```
Fractions.slate/
  deck.json            title, theme, slide order (optional but recommended)
  theme.css            deck CSS, loaded after the theme on every slide (optional)
  slides/
    01-title.html
    02-what-is-a-fraction.html
    …
  notes/
    01-title.md        presenter notes for slides/01-title.html (optional)
    …
  assets/
    pizza.jpg          images, video, audio used by slides (optional)
```

## deck.json

```json
{
  "title": "Fractions you can see",
  "theme": "april",
  "transition": "fade",
  "slides": [
    { "file": "01-title.html", "title": "Title" },
    { "file": "02-what-is-a-fraction.html", "title": "What is a fraction?", "transition": "push" }
  ]
}
```

| Field | Meaning |
|---|---|
| `title` | Deck title. Defaults to the folder name. |
| `theme` | One of `april`, `april-night`, `chalkboard`, `notebook`, `ocean`, `sunrise`, `minimal`, `classic`. Default `april`. |
| `transition` | Default transition for every slide: `none`, `fade`, `push`, `zoom`. |
| `slides[].file` | File name inside `slides/`. Required for each entry. |
| `slides[].title` | Title in Slate's slide list. Defaults to the page `<title>` or the file name. |
| `slides[].notes` | Notes file name inside `notes/`. Defaults to the slide's name with `.md`. |
| `slides[].transition` | This slide's transition, overriding the deck default. |
| `slides[].id` | A UUID. Leave it out; Slate assigns one and keeps it when it saves. |

Without `deck.json`, or without a `slides` list, Slate takes every `slides/*.html` in name order, so name files `01-…`, `02-…`. When Slate saves the deck it rewrites `deck.json` in full and renames the files to match the slide titles; that is expected.

## Slides

Each file in `slides/` is one slide: an HTML fragment (recommended) or a full page.

- **Fragment**: any HTML that does not start with `<!doctype` or `<html>`. Slate serves it inside a page that loads `_slate/april.css` (base styles and classes), `_slate/theme.css` (the deck's theme) and `theme.css` (deck CSS), with `<html data-theme="light">`. Scripts and styles in the fragment run as written.
- **Full page**: starts with `<!doctype html>`. Served exactly as written. Link `_slate/april.css` and `_slate/theme.css` in its `<head>` to use the theme.

The page is 1920 × 1080 CSS pixels and is scaled to every screen. Relative URLs resolve against the deck: `assets/pizza.jpg`, `theme.css`.

## Notes

`notes/<same name>.md` holds what the presenter sees under the live slide, never shown to the audience. Plain text with inline Markdown: `**bold**`, `*italic*`. One idea per line; line breaks are kept. Include answer keys, timings and transitions in speech ("Now let's see it move.").

## Assets

Put files in `assets/` and reference them from slides as `assets/<name>`. Use simple file names (letters, digits, `-`, `_`, `.`; no spaces).

## Runtime features slides can use

- `data-step` on an element hides it until the next click while presenting (`data-step="2"` on several elements reveals them together). In the editor every step shows.
- `slate.next()`, `slate.prev()`, `slate.goto(n)` from a slide script.
- `<figure class="chart" data-chart>` with a JSON script inside is drawn as a bar, line or pie chart (see components.md).
- `class="box" data-box` with `left` / `top` (and `width` / `height`) in stage pixels makes an element a free-floating box.
