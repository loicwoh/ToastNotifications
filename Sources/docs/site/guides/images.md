# Show a result preview in a toast

Give an operator a quick look at a finished test while they are working in another application. This example puts a simulated battery discharge chart in the toast's hero banner.

## Try it

Open `Toast Notification Examples.lvproj` and run `Toast With Images.vi`. Look for the chart above the notification text. Press **stop** to finish.

The original chart, `battery-test-preview.png`, is supplied with the example under the project's license. If you moved the checkout, select the PNG again in the diagram's **Image** path constant. In **Toast XML**, the hero image should point to a `file:///` URI. If the text appears alone, check that the URI points to an existing, readable image.

## Using this in your application

Use a wide image with legible labels. Windows uses a 364 × 180 pixel hero area at 100% scaling. Resolve your image path from the deployed asset location so the toast works on other machines.

[Add Hero Image](/reference/toastbuilder/add-hero-image.md) · [Microsoft hero image guidance](https://learn.microsoft.com/en-us/windows/apps/develop/notifications/app-notifications/app-notifications-content#hero-image)
