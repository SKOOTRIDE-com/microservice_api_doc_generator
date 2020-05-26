---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - shell
  - ruby
  - python
  - javascript

toc_footers:
  - <a href='#'>Sign Up for a Developer Key</a>
  - <a href='https://github.com/slatedocs/slate'>Documentation Powered by Slate</a>

includes:
  - errors

search: true
---

# Introduction

Welcome to Skoot's API documentation.

# APIs

### Send contacts
Add user friends by phone number hash.

* URL
    * send_contacts
* Method:
    * `POST`
* Data Params:
    * Accepts: `application/json`
    * Required:
        * `token`: User token
        * `contacts`: List of phone hashes
* Success Response:
    * Code: `200`
    * Content: `{"contacts": ["ex4mpl3h4sh"], "status": {"code": 1}}`
* Error Response:
    * Code: `200`
    * Content: `{"contacts": ["ex4mpl3h4sh"], "status": {"code": 2, "0": 400, "error_string": "Ooops, something went wrong. Sorry!"}}`
    * (incorrectly formatted error)

    OR

    * Code: `403`
    * Content: `{"contacts": ["ex4mpl3h4sh"], "status": {"code": 2, "error_string": "Ooops, something went wrong. Sorry!"}}`
* Sample Call:
    ```
    $ curl skoot.com/api/send_contacts\
        -H "Content-Type: application/json" \
        --data '{"contacts": ["ex4mpl3h4sh"], "token": "1234567abc"}'
    ```
    The above call returns
    ```
    {
        "contacts": ["ex4mpl3h4sh"],
        "status": {
            "code": 1
        }
    }
    ```
