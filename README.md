# NME themes

Community themes for [Animatek NME](https://github.com/animatek/Animatek-NME), the editor for the
Clavia Nord Modular G1. A theme is a small JSON file of colours: no code, nothing to install.

## Use a theme

1. Download a `.json` file from [`themes/`](themes/).
2. Put it in `~/.AnimatekNME/themes` (create the folder if it does not exist).
3. In NME, open **View > Theme** and pick it from the list.

Open **View > Theme > Edit Theme Colours** to change one: the canvas follows live while you drag a
colour, and Save writes your own file.

## Share a theme

Open a pull request that adds your file to `themes/`:

- one theme per file, named in lowercase with dashes (`my-theme.json`);
- a unique `"name"` inside it;
- say in the pull request who made it, so it can be credited.

By sending a theme you agree that it can be redistributed with NME and used by anyone (see the
licence below).

## The file format

```json
{
  "format": 1,
  "name": "My theme",
  "base": "Dark",
  "app":    { "backgroundMain": "#323232", "accentActive": "#e0af68" },
  "canvas": { "gridBackground": "#1f2125",
              "morphColor": ["#cb4f4f", "#4fcb4f", "#4f4fcb", "#cbcb4f"] }
}
```

- Colours are `"#rrggbb"` or `"#aarrggbb"`.
- **Every key is optional.** A missing or unreadable one keeps the value of the `base` theme, so a
  half-written file still loads. `base` is the name of a built-in theme.
- Easiest way to get every key: save a theme from the editor and open the file.
- Render styles (Wireframe, Hardware look, Flat knobs) are not part of a theme: they stay global options.

[`themes/_template.json`](themes/_template.json) is the smallest useful file.

## Licence

[CC0 1.0](LICENSE): the themes are public domain.
