# Open a link from a toast

Give someone a shortcut to the information behind a notification, such as a report or a project page. A protocol button hands the URI to Windows, which opens it in the associated application.

## Try it

Open `ToastAPI.lvproj` and run `Examples/Toast With Link Button.vi`. Click **Open project on GitHub** and watch the repository open in your browser. Press **stop** after each run.

## Using this in your application

Use a protocol button when Windows can handle the action directly, such as opening a report in the browser. Use an application-action button when LabVIEW needs to make a decision after the click. [Offer a choice](/guides/multiple-actions.md)

[Add Link Button](/reference/toastbuilder/add-link-button.md)
