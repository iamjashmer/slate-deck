# slate-deck

A [Claude Code](https://claude.com/claude-code) skill that designs presentations for **Slate**, a macOS presentation app where every slide is a web page. Describe a talk or a lesson, and Claude writes the whole deck (slides, interactions and presenter notes), checks it, and opens it in Slate, ready to edit and present.

**Get Slate:** [download Slate for Mac](https://github.com/iamjashmer/slate-releases/releases/latest/download/Slate.dmg) (macOS 15 or later). Install notes and every version are on the [Slate releases page](https://github.com/iamjashmer/slate-releases/releases).

## Install the skill

For every project (a personal skill):

```bash
git clone https://github.com/iamjashmer/slate-deck.git ~/.claude/skills/slate-deck
```

Or for one project only, clone it into that project's `.claude/skills/slate-deck`.

## Use it

In Claude Code, run the skill with a brief:

```
/slate-deck a 10-minute Grade 6 lesson on ratios, ocean theme, with a quick check
```

or just ask for slides "in Slate". Claude will:

1. Settle the brief: topic, audience, length, theme, and any interactive slides.
2. Outline the deck, one idea per slide.
3. Write `<Name>.slate/`: one HTML file per slide, presenter notes, assets.
4. Check it with `scripts/validate_deck.py`.
5. Open it in Slate with `scripts/open_deck.sh`.

In Slate you can then click any text to change it, drag anything to move it, switch themes, and press ⌥⌘P to present with your notes on your screen only.

## What a deck looks like

A `.slate` deck is a folder of plain files that you can also edit by hand:

```
Comparing-Fractions.slate/
  deck.json        title, theme, slide order
  slides/          one HTML file per slide (01-title.html, …)
  notes/           presenter notes, one Markdown file per slide
  assets/          images, video, audio
  theme.css        optional deck CSS
```

See [`examples/Comparing-Fractions.slate`](examples/Comparing-Fractions.slate) for a finished five-slide lesson, [`references/format.md`](references/format.md) for the format, and [`references/components.md`](references/components.md) for the slide building blocks: titles, cards, step-by-step builds, quizzes, tables, charts, pictures and free-floating boxes.

Themes: `april`, `april-night`, `chalkboard`, `notebook`, `ocean`, `sunrise`, `minimal`, `classic`.

## Scripts

```bash
python3 scripts/validate_deck.py path/to/Deck.slate   # check a deck
bash scripts/open_deck.sh path/to/Deck.slate          # open it in Slate
```

`open_deck.sh` uses the app at `$SLATE_APP` if you set it, otherwise the installed Slate.

## License

MIT. See [LICENSE](LICENSE).
