---
name: slate-deck
description: Design a presentation as a Slate deck (a .slate folder of HTML slides with private presenter notes) and open it in the Slate macOS app. Use when asked to make, draft, design or build slides, a deck, a lesson presentation, a pitch or a talk "in Slate", or to turn an outline, notes or a document into slides the user can present and edit in Slate.
---

# Slate deck

Slate is a macOS presentation app where every slide is an HTML module styled by the deck's theme. You design the deck here as plain files; Slate opens the folder, renders each slide on a 1920 × 1080 stage, and the user edits, rehearses and presents it there, with presenter notes only they can see.

## Workflow

1. **Brief.** Get the topic, the audience, how long the talk is (about one slide per minute), the theme (see below), and whether they want interactive slides (quizzes, polls, timers, sliders). Ask only for what you cannot infer. Use real facts only; mark anything unknown as an example rather than inventing numbers, quotes or credentials.
2. **Outline.** Write the slide list in chat: number, title, one-line purpose, and the module each slide uses. Keep one idea per slide. Confirm it when the deck is long or the brief was thin; otherwise go on.
3. **Write the deck** as `<Name>.slate/` (default location `decks/` in the current project unless the user names one). Follow `references/format.md` for the files and `references/components.md` for the HTML building blocks. Every slide gets presenter notes: what to say, in the speaker's voice, plus any answer keys or timings.
4. **Validate.** Run `python3 <this skill's folder>/scripts/validate_deck.py <Name>.slate` (the skill's folder is the base directory given when the skill loads) and fix every error. Read the warnings and fix those that matter.
5. **Open it.** Run `bash <this skill's folder>/scripts/open_deck.sh <Name>.slate`. It opens the deck in the installed Slate (or the app at `$SLATE_APP`). If Slate is not installed, the script prints where to download it; pass that on to the user, and still give them the deck's path.
6. **Report.** List the slides, the theme, which slides are interactive, and anything marked as an example for the user to replace. Tell them: Play with ⌥⌘P; in Edit mode they can click any text to change it, drag anything to move it, and switch themes from the Deck panel.

## Themes

`april` (cream, navy, orange; Poppins), `april-night` (the same, dark), `chalkboard` (green board, chalk font), `notebook` (ruled paper, handwritten headings), `ocean` (deep blue, teal), `sunrise` (warm peach, coral, Futura), `minimal` (white, black, red; Helvetica Neue), `classic` (parchment, Baskerville). Pick from the audience and tone; default to `april`.

## Rules

- Design for a **1920 × 1080 stage**. Sizes are in stage pixels. Text under 24px is too small to read in a room.
- Write **fragments** (no `<html>`, `<head>` or `<body>`): Slate wraps them with the base styles, the theme and the deck CSS. Use a full HTML page only when a slide needs to own the whole document, and then link `_slate/april.css` and `_slate/theme.css` yourself.
- Use the **theme tokens** (`var(--navy)`, `var(--orange)`, `var(--paper)`…) and the documented classes, never literal colors, so the deck restyles when the user changes theme.
- Keep each slide self-contained: its own `<style>` and `<script>` if needed, unique ids within the slide, no `localStorage`, no `position: fixed`.
- Prefer no network: no CDN scripts or remote images unless the user asks; slides may be presented offline. Put images in `assets/` and reference them as `assets/<file>`.
- Use `data-step` for points revealed one click at a time. Put anything the user may want to drag freely in a box (`class="box" data-box` with `left`/`top`).
- Never put presenter notes or private remarks on the slide itself; they go in `notes/`.

## References

- `references/format.md`: the `.slate` folder, `deck.json`, notes, transitions and assets.
- `references/components.md`: classes, tokens and ready-made slide patterns (title, section, cards, steps, quiz, poll, timer, table, chart, picture, text box).
- `scripts/validate_deck.py`: checks a deck before opening it.
- `scripts/open_deck.sh`: opens a deck in Slate (the app at `$SLATE_APP`, or the installed app).
- `examples/Comparing-Fractions.slate`: a small finished deck to copy patterns from.
