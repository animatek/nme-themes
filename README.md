# NME themes

Community themes for [Animatek NME](https://github.com/animatek/Animatek-NME), the editor for the
Clavia Nord Modular G1. A theme is a small JSON file of colours: no code, nothing to run.

## Use a theme

In NME 0.22 and later, open **View > Theme > Community Themes**. It lists every theme in this repository; a dot
marks the ones that are new or have changed since you last looked, and clicking one installs it
and switches to it. NME looks here at most once a day when it starts (Editor Options can turn
that off) and whenever you choose **Check Now**.

By hand: download a `.json` file from [`themes/`](themes/) and use **View > Theme > Import Theme
File...** (0.22), or put it in `~/.AnimatekNME/themes` and choose **Reload Theme Files** (0.20 on).

Open **View > Theme > Edit Theme Colours** to change one: the canvas follows live while you drag a
colour, and Save writes your own file. **Export Current Theme...** writes the theme in use to a
file you can share.

## Share a theme

Open a pull request that adds your file to `themes/`:

- one theme per file, named in lowercase with dashes (`my-theme.json`);
- a unique `"name"` inside it, not one of NME's own themes;
- your name in `"author"`, so it can be credited.

A check runs on every pull request and says what is wrong with a file, if anything. Once it is
merged, `index.json` is rebuilt by itself and the theme shows up in everyone's editor. Do not
edit `index.json` by hand.

By sending a theme you agree that it can be redistributed with NME and used by anyone (see the
licence below).

## The file format

```json
{
  "format": 1,
  "name": "My theme",
  "author": "Your name",
  "description": "One line about it",
  "base": "Dark",
  "app":    { "backgroundMain": "#323232", "accentActive": "#e0af68" },
  "canvas": { "gridBackground": "#1f2125",
              "morphColor": ["#cb4f4f", "#4fcb4f", "#4f4fcb", "#cbcb4f"] },
  "render": { "flatKnobs": true }
}
```

- Colours are `"#rrggbb"` or `"#aarrggbb"`.
- **Every key is optional** except `format` and `name`. A missing colour keeps the value of the
  `base` theme, so a half-written file still loads. `base` is the name of a built-in theme.
- `render` is the render style the theme turns on when it is chosen: `wireframe`, `hardwareLook`
  and `flatKnobs` (true or false) and `knobStyle` (0 domed cap, 1 black knurled, 2 aluminium
  knurled). Leave out what the theme does not care about; choosing a theme without `render` gives
  the user back their own style. NME 0.22 and later.
- Easiest way to get every key: save a theme from the editor and open the file.
- At most 256 KB.

[`themes/_template.json`](themes/_template.json) is the smallest useful file. To check your files
before sending them: `python3 tools/build_index.py --check`.

## Licence

[CC0 1.0](LICENSE): the themes are public domain.
