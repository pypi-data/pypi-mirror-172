# REST API CALL

This **python** library is a REST API Call which generates REST URLs using attributes.",

As an example:

    http://example.org/product/kart/customer?id=3&name=foo'

The URI path:

    product/kart/customer?id=3&name=foo

with this **python** library is the sequence:

    product.kart.customer(id='3', name='foo')

## get()

You can perform the request (Cf. http://docs.python-requests.org/) with `get()`:

    >>> import restapicall
    >>> conn = restapicall.ApiCall(endpoint='http://example.org')
    >>> r = conn.product.kart.customer(id='3', name='foo').get()
    >>> r.url
    http://example.org/product/kart/customer?id=3&name=foo
    >>> r.status_code
    404
    >>> r.headers['content-type']
    'text/html; charset=UTF-8'

## get_url()

the url can be get by `get_url()`:

    >>> import restapicall
    >>> conn = restapicall.ApiCall(endpoint='http://example.org')
    >>> r = conn.product(id='3').kart.customer(name='foo').get_url()
    >>> print(r)
    http://example.org/product/kart/customer?id=3&name=foo'

You can concatenate the attributes. That's exactly the same:

    >>> conn = ApiCall(endpoint='http://example.org')
    >>> r = conn.product.kart.customer(id='3', name='foo').get_url()
    >>> print(r)
    http://example.org/product/kart/customer?id=3&name=foo'


## License

ISC

## Author information

This code was created in 2019 by Olivier Locard.
