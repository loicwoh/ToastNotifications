# Show a result preview in a toast

Give an operator a quick look at a finished test while they are working in another application. This example puts a simulated battery discharge chart in the toast's hero banner.

## Try it

Open `Toast Notification Examples.lvproj` and run `Toast With Images.vi`. Look for the chart above the notification text. Press **stop** to finish.

The original chart, `battery-test-preview.png`, is supplied under the project's license. The example resolves it from the VI's folder, so keep the PNG alongside the VI if you move the example. If the file is missing, the error reports the resolved path. On success, **Toast XML** shows the hero image's `file:///` URI.

## Using this in your application

Use a wide image with legible labels. Windows uses a 364 × 180 pixel hero area at 100% scaling. Resolve your image path from the deployed asset location so the toast works on other machines.

[Add Hero Image](/reference/toastbuilder/add-hero-image.md) · [Microsoft hero image guidance](https://learn.microsoft.com/en-us/windows/apps/develop/notifications/app-notifications/app-notifications-content#hero-image)
