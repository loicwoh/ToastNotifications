# VIPM installation check

On 2026-11-07 the maintainer built and installed package 1.0.0.1 with VIPM 26.3.2
and LabVIEW 2026 64-bit on Windows. The maintainer confirmed that all four examples
worked from the installed package, including Toast From XML.

- Toast From XML
- Toast With Link Button
- Toast With Multiple Actions
- Toast With Reply

The previous installed build raised a .NET FileNotFoundException in Create Toast
Notifier when resolving the notification manager type by assembly name. The
updated VI finds the DLL under the toolkit root and resolves the type from the
assembly file. Inspection of the package confirmed that it contains the new
reflection helper, the four example VIs and the Microsoft MIT notice.

The maintainer also checked the detailed-help links and confirmed that the
installed examples work through NI Example Finder. Inspection of package
1.0.0.2 confirmed that all four example VIs contain their guide URLs.

These were manual checks on one LabVIEW version.
