# One toolkit, three class families

ToastAPI uses a shared **navy and amber** identity. Each core class adds one accent
to the same layout, typography and navigation. Names and letters remain visible
alongside colors.

<div class="cards">
<a class="card module-card family-builder" href="#/api/toastbuilder"><span class="module-symbol" aria-hidden="true">B</span><span class="card-number">BLUE · COMPOSITION</span><strong>ToastBuilder</strong><span>Build the notification content.</span></a>
<a class="card module-card family-service" href="#/api/toastservice"><span class="module-symbol" aria-hidden="true">S</span><span class="card-number">TEAL · LIFECYCLE</span><strong>ToastService</strong><span>Display notifications and manage their integration.</span></a>
<a class="card module-card family-handler" href="#/api/activationhandler"><span class="module-symbol" aria-hidden="true">H</span><span class="card-number">VIOLET · ACTIVATION</span><strong>ActivationHandler</strong><span>React to a click or submitted input.</span></a>
</div>

The User Event plugin belongs to the **ActivationHandler** family. Libraries such
as Toast Native and Reflection DotNet use the common toolkit treatment. A plugin
does not introduce another unrelated color.

## Palette

| Role | Accent | RGB | Light surface |
|---|---|---|---|
| <span class="palette-swatch family-toolkit" aria-hidden="true"></span>ToastAPI | Navy `#183247` | 24, 50, 71 | `#F0F4F7` |
| Toolkit highlight | Amber `#F4C95D` | 244, 201, 93 | Use with navy text |
| <span class="palette-swatch family-builder" aria-hidden="true"></span>ToastBuilder · B | Blue `#2455A4` | 36, 85, 164 | `#EDF3FC` |
| <span class="palette-swatch family-service" aria-hidden="true"></span>ToastService · S | Teal `#176B62` | 23, 107, 98 | `#EDF7F4` |
| <span class="palette-swatch family-handler" aria-hidden="true"></span>ActivationHandler · H | Violet `#704397` | 112, 67, 151 | `#F5EFFA` |

Use white text on the dark accents. Use navy text on amber and light surfaces.
Amber is a brand highlight, not an error or warning indicator.

## Applied to the documentation

- **Toolkit:** common navigation, navy headings, amber brand line and call to action.
- **Class and method pages:** a named owner banner, family accent and the same
  readable content structure. The [Add Text pilot](/reference/toastbuilder/add-text.md)
  uses ToastBuilder's blue treatment.
- **Diagrams:** class operations use the same border and light surface as their
  owner. Labels carry the meaning even when colors cannot be distinguished.
- **Native VI illustrations:** retain the original icon, banner and terminal
  labels exported by LabVIEW. The website does not recolor these captures.

## Possible LabVIEW application

For a future class-owned icon banner, use the family's dark accent with a white
short label, keeping the method pictogram beneath it on a neutral background.
Use the same class accent for documentation callouts; retain the common toolkit
identity around it. The B/S/H blocks shown here are website identity markers,
not replacements for the existing VI icons.

This is a visual proposal applied to the site. The LabVIEW class banners and
icons can be aligned with it after the proposal is accepted.

[Explore the API](/api.md) · [See the current examples](/examples.md)
