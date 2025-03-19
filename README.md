Reproduction case for a weird behaviour of JsError when created inside a worker.

Difference in logging can be seen when comparing console output of

```sh
WASM_BINDGEN_USE_BROWSER=1 wasm-pack test --firefox wasm-app
```

vs

```sh
WASM_BINDGEN_USE_DEDICATED_WORKER=1 wasm-pack test --firefox wasm-app
```

In the first case there's a JsError logged and in the second one the same log
does not appear. On chromium, error is logged in both cases.

Example where the JsError cannot be sent over port can be launched in the same
repo by running

```sh
npm run build && npm run start
```

in the `www` directory. This again, works correctly on chromium, but fails on
firefox
