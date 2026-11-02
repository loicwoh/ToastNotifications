# Microsoft documentation directory

These pages describe different API families. A feature in Windows App SDK is not
automatically exposed by the current LabVIEW wrapper. Check the API family and
Windows requirements before adapting an example.

## Current toolkit and native API

| Reference | Use in this project |
|---|---|
| [ToastContentBuilder](https://learn.microsoft.com/en-us/dotnet/api/microsoft.toolkit.uwp.notifications.toastcontentbuilder?view=win-comm-toolkit-dotnet-7.1) | Builder methods, overloads and content composition in Microsoft.Toolkit.Uwp.Notifications 7.1 |
| [ToastButton](https://learn.microsoft.com/en-us/dotnet/api/microsoft.toolkit.uwp.notifications.toastbutton?view=win-comm-toolkit-dotnet-7.1) | Application buttons, protocol activation and button properties |
| [ToastNotificationManagerCompat](https://learn.microsoft.com/en-us/dotnet/api/microsoft.toolkit.uwp.notifications.toastnotificationmanagercompat?view=win-comm-toolkit-dotnet-7.1) | Desktop notification registration, activation and notifier |
| [ToastNotification](https://learn.microsoft.com/en-us/uwp/api/windows.ui.notifications.toastnotification) | Native Windows notification object |
| [XmlDocument.LoadXml](https://learn.microsoft.com/en-us/uwp/api/windows.data.xml.dom.xmldocument.loadxml) | Native XML loading; planned ToastFromXML implementation |

## Content and XML schema

| Reference | How to use it |
|---|---|
| [App notification content](https://learn.microsoft.com/en-us/windows/apps/develop/notifications/app-notifications/app-notifications-content?tabs=xml) | Visual elements, text input, buttons, icons, colors, tooltips and context menu. Use XML tabs to study the payload independently of the builder API. |
| [Toast schema](https://learn.microsoft.com/en-us/uwp/schemas/tiles/toastschema/schema-root) | Element and attribute definitions, supported values and platform requirements |

## Windows App SDK

| Reference | Boundary |
|---|---|
| [App notifications overview](https://learn.microsoft.com/en-us/windows/apps/develop/notifications/app-notifications/) | Current Microsoft platform guidance |
| [App notification quickstart](https://learn.microsoft.com/en-us/windows/apps/develop/notifications/app-notifications/app-notifications-quickstart) | AppNotificationManager setup in Windows App SDK; not the registration API currently wrapped here |
| [App notification content — SDK examples](https://learn.microsoft.com/en-us/windows/apps/develop/notifications/app-notifications/app-notifications-content?tabs=appsdk) | AppNotificationBuilder examples. Translate the capability and XML deliberately; do not substitute its types into the current .NET reflection calls. |

For implemented and planned LabVIEW features, see [coverage](coverage.md). This
directory is a curated set of upstream links, not a claim of complete wrapper coverage.
