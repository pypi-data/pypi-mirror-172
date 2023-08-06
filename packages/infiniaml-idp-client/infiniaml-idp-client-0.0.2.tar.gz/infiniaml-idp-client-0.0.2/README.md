# IDP Client Library

## 🚀 Setup

### Initializing the Python virtual environment

To begin development, initialize the Python virtual environment with the command `make init`.

### Installing the library in development mode

In order to test changes iteratively, it's recommended to install the library via an [editable installation](https://setuptools.pypa.io/en/latest/userguide/development_mode.html). To do this, simply run `make install`. This will also install the optional `cli` dependency exposing the `idp-client-lib` command in your virtual environment.

Should you want to test the library within a different environment, run the command `pip install --editable {PATH}` where `PATH` is the location of this repo on your computer. 

If you're working in *Visual Studio Code*, you'll have to add `"python.analysis.extraPaths": [{PATH}]` to your `.vscode/settings.json` in order for *Pylance* to recognize the library import.


## ➰ Notes on Async

This library uses the package [`unasync`](https://github.com/python-trio/unasync) in order to transform asynchronous code into synchronous code. As a result, development happens with async Python and we let the tool write the sync part.

The `unasync` script resides in `scripts/unasync-files.py`. In it are rules for where to find the async files and where to output the sync files. Additionally, some "replacement" rules are defined to transform certain python tokens, i.e. transforming `httpx.AsyncClient` to `httpx.Client`.

All async code lives in `idp_client_lib.aio` and all synchronous code is outputted to `idp_client_lib`. Code that needs to be shared by both async and sync code can belong anywhere except inside `idp_client_lib.aio`.

A `Make` command `make unasync` is available to quickly run `unasync-files.py` during development.

## 🧪 Testing

Testing relies on a `.env` to inject variables into the testing config. 

Available in the respository is a `.env.template` that can be used to create the `.env`. The `Make` automation will handle the templating steps for you. All you need is to create your own `.env.secret` and in it set the variables seen in `.env.template`.

Here is an example of a `.env.secret`:

<details>
    <summary>Example .env.secret</summary>

```
IDP_URL=http://idp.infiniaml.com
ACCESS_KEY_ID=myaccesskeyid
ACCESS_KEY_SECRET=myaccesskeysecret
PROJECT_ID=1234
```

</details>

Running `make compose-env` should build the `.env` from the provided `.env.template` and created `.env.secret`. Then, testing should be ready to go with the command `make test`.