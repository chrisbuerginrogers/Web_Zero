# InventZero - Film Finder PoC

An experiment in making the simplest and smallest app framework.

This is a shonky proof-of-concept and needs to be re-written properly. But it
proves (hopefully) this approach works.

Created by: Nicholas H.Tollervey and Chris Rogers.

While Nicholas wrote all the code, it's mostly Chris's fault though.

## Run the app

1. Clone this repository.
2. In the root of the repository type:

```shell
$ python -m http.server
```

3. Visit [localhost:8000](http://localhost:8000/)
4. It should be self-evident.

## Developer Info

We started with a simple app, written using an imaginary API. You can find that
in the `main.py` file. Once happy with the way `main.py` felt, we created the
actual API to make it work properly. This is the experimental "InventZero"
framework, found in the `iz.py` module.

The rest is just a standard PyScript app.
