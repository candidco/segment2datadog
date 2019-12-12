## Segment2Datadog

This is a simple Flask app that provides an endpoint to receive events from
Segment via the webhooks destination.
The flask app will forward the received events to Datadog as a counter.

## Requirements:

- [Segment](https://segment.com/) account with your source events.
- [Datadog](https://www.datadoghq.com/) account where your events will be forwarded.

## Dependencies:

- [Datadog Python SDK](https://github.com/DataDog/datadogpy).
- [Flask](http://flask.pocoo.org/) to implement the API.

## Installation:

- Set the corresponding keys (you can access your Datadog keys [here](https://app.datadoghq.com/account/settings#api)):
  - **DATADOG_STATSD_HOST**: IP address of a [datadog agent](https://app.datadoghq.com/account/settings#agent) (be sure you've set `DD_DOGSTATSD_NON_LOCAL_TRAFFIC` in the agent if you must).
  - **SEGMENT_SHARED_SECRET**: Your Segment Webhooks destination Shared Secret.
- Add [Webhooks](https://segment.com/docs/destinations/webhooks/) destination in your Segment project.
- Configure your Webhooks destination by setting the webhook URL to a CNAME pointing to the lb fronting the service.
- Activate the webhook destination.
- You should start receiving events in your Datadog dashboard, named **segment.event**.
Datadog tags are included like **source**, **type** and **event** (segment source, type of event (track)
and event name, respectively). You can customize app.py file to add your own
tags or also monitor [other type of events](https://segment.com/docs/connections/spec/), eg: [page events](https://segment.com/docs/connections/spec/page/).
