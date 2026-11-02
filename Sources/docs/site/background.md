<div class="eyebrow">ToastAPI / Project background</div>

# Why this project

<p class="lead">A small notification toolkit, rooted in a longer-standing ambition: building LabVIEW applications that feel thoughtfully designed.</p>

*A note from the project author.*

## Looking beyond the familiar LabVIEW interface

For as long as I have worked with LabVIEW, I have wanted people to open an
application without immediately identifying the technology behind it. I want
the applications I build, and those built by my colleagues, to have their own
identity and a deliberate user experience.

When someone asks whether an interface was built with web technologies or Qt,
I feel that something has worked. Being able to answer that it is LabVIEW often
starts an interesting conversation about what the language can do.

The familiar grey panels, pastel colors and default controls can shape people's
expectations. I would like more applications to show how much room there is
beyond that familiar appearance. I want to challenge the assumption that
measurement software built in LabVIEW has to look dated.

## Measurements come first

Notifications can look like a gadget on a test bench. They are an optional
finishing touch, and I would only spend time on them once the essential work
is in place: reliable measurements, correctly recorded results, useful analyses
and a presentation that helps users understand their data and develop ideas.

Once those foundations are sound, small interactions can make an application
more comfortable and professional to use. Notifications are one of those details.

## A practical need during long-running tests

The idea became useful to me while developing battery-test applications.
These tests can take a long time and generate a great deal of data. In that
environment, it makes sense to let someone know that a task has started, is
still running or has finished, while they continue with something else.

Some of those applications were used early in R&D and reproduced features of
an eventual user interface developed with another technology. I had seen
notifications in those applications and wanted to offer a similar experience
in the LabVIEW tools.

Users could minimize the application, or work in analysis and processing modules
while an acquisition continued. The same need extends to endurance tests and
long recordings. In production, each individual test may be quick, yet a sequence
of dozens or hundreds of tests, or an automated batch, can keep an operator
waiting for a substantial amount of time.

That is the use case behind this project: help users stay informed without
requiring them to keep watching a window. The
[current examples](/examples.md) demonstrate the interactions available today;
the scenarios above explain the motivation, rather than a list of implemented
features.

## From NotifyIcon to interactive toasts

I first integrated notifications through NotifyIcon. It was already a useful
improvement, although I had limited control over the appearance. I also ran into
a build where descriptive application metadata appeared in the notification
instead of the application name I expected.

Other applications showed me that more customized notifications were possible.
Later, notifications in tools such as Outlook and Teams made the possibilities
particularly tangible: images, action buttons and a field for replying directly.
Recreating a notification system from scratch would have been a considerable
amount of work. I wanted to use the existing Windows capabilities from LabVIEW.

Displaying an initial toast with text or a button was relatively straightforward.
Receiving the interaction was the difficult part. In my attempts, accessing
`User Inputs` led to .NET objects and WinRT dependencies that I could not load
successfully into LabVIEW. I tried several approaches, including C# helpers,
looked for answers on forums and found another developer facing the same problem.

I set the subject aside, then returned to it every few months for another
afternoon or evening of investigation. When I installed LabVIEW 2026, I tried
again, hoping that newer .NET integration might open another route.

Around the same time, I started experimenting with AI assistance and the
LabVIEW MCP server. With help understanding .NET reflection and exploring ways
around the WinRT obstacle, I eventually completed the proof of concept:
generate a notification, recover the submitted input and process it in LabVIEW.
ToastAPI grew from that experiment into an effort to make the integration reusable.

The [API overview](/api.md) describes the current classes. The
[coverage page](/coverage.md) records what works today and what still needs work.

## An experiment in AI-assisted development

This project also became a sandbox for finding out where AI assistance was useful
in my own LabVIEW workflow. I adapted Claude skills for Codex and experimented
with generating LabVIEW code through the available tooling.

So far, I have not been convinced by direct code generation for this project.
The results needed substantial work on wiring, connector panes, diagram layout
and implementation conventions. Some generated code provided a starting point
for debugging, but the generation and subsequent cleanup often took longer than
writing the code myself, while consuming a significant number of tokens.
The number of tool calls and intermediate formats also made the workflow feel heavy.

Reading and analyzing existing code, investigating failures and understanding
unfamiliar .NET reflection mechanisms were much more useful applications of
the assistant. Git and GitHub integration also brought considerable value.
The same has been true for CI and this documentation: versioned Markdown,
Docsify and a small amount of CSS have made it practical to build and maintain
a published site alongside the project.

For now, I prefer a human to write the LabVIEW implementation, with AI helping
on investigation, debugging, documentation and the surrounding development work.
Better skills, models and tooling may change that balance. I am also interested
in work an assistant can do while I am away: exploring a plan, running suitable
checks or preparing documentation. The value depends on the time saved after
review and cleanup.

[Try a working example](/getting-started.md) · [Explore the API](/api.md) · [Current limitations](/coverage.md)
