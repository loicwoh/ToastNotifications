<div class="eyebrow">ToastAPI / Developer guide</div>

# Windows notifications, built in LabVIEW.

<p class="lead">Create interactive toasts, capture a reply, and bring the result back to your application's event loop.</p>

<span class="pill">LabVIEW 2026</span><span class="pill">Windows desktop</span><span class="pill pending">In development</span>

During long-running tests, users may need to work elsewhere. Notifications help
them stay informed. ToastAPI grew out of a broader ambition to give LabVIEW applications
a deliberate, professional user experience.
[Read why this project exists](background.md), from battery testing to the
reflection proof of concept and the experience of working with AI assistance.

<div class="hero">
<h2>Start with a working example</h2>
<p>Send a request, type a reason, and receive it as LabVIEW data. The reply example shows the complete path from construction to callback delivery.</p>
<a href="#/guides/reply">Try the reply example →</a>
</div>

## Examples to explore

<div class="cards">
<a class="card" href="#/guides/reply"><span class="card-number">01 / USER INPUT</span><strong>Receive a text reply</strong><span>Keep application arguments and submitted text separate. Deliver both to your event loop.</span></a>
<a class="card" href="#/guides/multiple-actions"><span class="card-number">02 / ACTIVATION</span><strong>Handle multiple actions</strong><span>Distinguish Accept, Reject, and a click on the notification body.</span></a>
<a class="card" href="#/guides/protocol"><span class="card-number">03 / PROTOCOL</span><strong>Open a link</strong><span>Let Windows open a URI from a notification button.</span></a>
<a class="card" href="#/guides/xml"><span class="card-number">04 / XML SOURCE</span><strong>Display XML content</strong><span>Reuse XML text with the same service and activation handler.</span></a>
</div>

## A small public surface

<div class="cards">
<a class="card module-card family-builder" href="#/api/toastbuilder"><span class="module-symbol" aria-hidden="true">B</span><span class="card-number">COMPOSITION</span><strong>ToastBuilder</strong><span>Compose the message, inputs and actions.</span></a>
<a class="card module-card family-service" href="#/api/toastservice"><span class="module-symbol" aria-hidden="true">S</span><span class="card-number">LIFECYCLE</span><strong>ToastService</strong><span>Display notifications and manage registration.</span></a>
<a class="card module-card family-handler" href="#/api/activationhandler"><span class="module-symbol" aria-hidden="true">H</span><span class="card-number">ACTIVATION</span><strong>ActivationHandler</strong><span>Choose how activations reach your application.</span></a>
</div>

Use [ToastBuilder](api/toastbuilder.md) to construct content,
or [ToastFromXML](api/toastfromxml.md) to start from XML text,
[ToastService](api/toastservice.md) to manage notification registration, and an
[ActivationHandler](api/activationhandler.md) to decide what happens after a click.
The application sees LabVIEW values and classes; the .NET references stay inside the wrapper.

<div class="flow"><a href="#/api/toastbuilder">ToastBuilder</a> → Windows notification → <a href="#/api/activationhandler">ActivationHandler</a> → your LabVIEW loop</div>

[UserEventActivationHandler](api/usereventactivationhandler.md) provides the current working relay. Its event payload
contains `Activation` and the conversion `error`. It allows your application to
handle the result outside the native callback.

Browse the [API by owner](api.md), [concept map](concepts.md) or
[reference index](reference.md) to follow this workflow into the saved methods.

## Know what is ready

Text, application buttons, body arguments, protocol buttons and submitted text
have working examples with manual validation. Handler error reporting and concurrent
shutdown still need work. There is no published compatibility guarantee for LabVIEW 2020 yet.

Read [Getting started](getting-started.md) for the project to open, or
[Coverage & known limits](coverage.md) before selecting features for your application.
