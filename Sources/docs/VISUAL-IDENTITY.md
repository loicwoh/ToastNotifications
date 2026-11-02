# ToastAPI visual identity — maintainer reference

Keep this document in the repository, outside the published documentation site.
It records the approved palette and the planned application to LabVIEW class
banners. The website continues to use the same theme.

ToastAPI uses a shared **navy and amber** identity. Each core class adds one accent
to the same layout, typography and navigation. Names and letters remain visible
alongside colors.

- **ToastBuilder · B · blue:** composition of notification content.
- **ToastService · S · teal:** display and integration lifecycle.
- **ActivationHandler · H · violet:** response to activations and submitted input.

The User Event plugin belongs to the **ActivationHandler** family. Libraries such
as Toast Native and Reflection DotNet use the common toolkit treatment. A plugin
does not introduce another unrelated color.

## Palette

| Role | Accent | RGB | Light surface |
|---|---|---|---|
| ToastAPI | Navy `#183247` | 24, 50, 71 | `#F0F4F7` |
| Toolkit highlight | Amber `#F4C95D` | 244, 201, 93 | Use with navy text |
| ToastBuilder · B | Blue `#2455A4` | 36, 85, 164 | `#EDF3FC` |
| ToastService · S | Teal `#176B62` | 23, 107, 98 | `#EDF7F4` |
| ActivationHandler · H | Violet `#704397` | 112, 67, 151 | `#F5EFFA` |

Use white text on the dark accents. Use navy text on amber and light surfaces.
Amber is a brand highlight, not an error or warning indicator.

## Applied to the documentation

- **Toolkit:** common navigation, navy headings, amber brand line and call to action.
- **Class and method pages:** a named owner banner, family accent and the same
  readable content structure. The [Add Text pilot](reference/toastbuilder/add-text.md)
  uses ToastBuilder's blue treatment.
- **Diagrams:** class operations use the same border and light surface as their
  owner. Labels carry the meaning even when colors cannot be distinguished.
- **Native VI illustrations:** retain the original icon, banner and terminal
  labels exported by LabVIEW. The website does not recolor these captures.

## LabVIEW application to carry out

For a future class-owned icon banner, use the family's dark accent with a white
short label, keeping the method pictogram beneath it on a neutral background.
Use the same class accent for documentation callouts; retain the common toolkit
identity around it. The B/S/H blocks used by the website are identity markers,
not replacements for the existing VI icons.

The palette is already applied to the site. LabVIEW class banners and icons
still need their own implementation pass; this reference does not modify them.

Implementation references: [CSS tokens](site/assets/identity.css),
[owner-to-family mapping](api-map.json), [visual review and screenshots](reviews/39-identity.md).
