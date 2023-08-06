# thawani Python Client


Python bindings for interacting with the thawani API

This is primarily meant for merchants who wish to perform interactions with the thawani API programatically.

## Installation

```sh
$ pip install thawani
```

## Usage

You need to setup your key and secret using the following:
You can find your API keys at <https://thawani.om//#/app/keys>.

```py
import thawani
client = thawani.Client(secret_key="<Secret_KEY>",publishable_key="<Publishable_KEY>")
```

## App Details

After setting up client, you can set your app details before making any request
to thawani using the following:

```py
client.set_app_details({"title" : "<YOUR_APP_TITLE>", "version" : "<YOUR_APP_VERSION>"})
```

For example, you can set the title to `Django` and version to `1.8.17`. Please ensure
that both app title and version are strings.

## Supported Resources


- [Customer](documents/customer.md)

- [Token](documents/token.md)

- [Order](documents/order.md)

- [Payments](documents/payment.md)

- [Settlements](documents/settlement.md)

- [Refunds](documents/refund.md)

- [Invoice](documents/invoice.md)

- [Subscriptions](documents/subscription.md)

- [Payment Links](documents/paymentLink.md)

- [Smart Collect](documents/virtualAccount.md)







---

## Bugs? Feature requests? Pull requests?

All of those are welcome. You can [file issues][issues] or [submit pull requests][pulls] in this repository.

[issues]: https://github.com/thawani-pay/thawani-python/issues
[pulls]: https://github.com/thawani-pay/thawani-python/pulls
