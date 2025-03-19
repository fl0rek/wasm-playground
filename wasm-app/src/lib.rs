use wasm_bindgen::prelude::*;
use web_sys::MessagePort;

#[wasm_bindgen]
pub struct WasmApp {
    _port: MessagePort,
}

#[wasm_bindgen]
#[allow(non_snake_case)]
impl WasmApp {
    #[wasm_bindgen(constructor)]
    pub fn new(port: MessagePort) -> Self {
        error_doing_weird_stuff();

        let err1 = JsError::new("JsError inside worker, rust");
        // doesn't seem to be sent at all?
        port.post_message(&err1.into()).expect("sent message");

        // is sent successfully, so above does not panic
        port.post_message(&"Hello, World".into())
            .expect("sent message");

        Self { _port: port }
    }
}

fn error_doing_weird_stuff() {
    let err0 = JsError::new("JsError inside worker, rust");
    web_sys::console::info_1(&"<Expecting JsError>".into());
    // doesn't seem to be printed ??
    web_sys::console::error_2(&"JsError inside worker".into(), &err0.into());
    web_sys::console::info_1(&"</Expecting JsError>".into());
}

#[cfg(test)]
mod browser_tests {
    use super::*;

    use wasm_bindgen_test::wasm_bindgen_test;

    #[wasm_bindgen_test]
    fn test_error() {
        error_doing_weird_stuff();
    }
}
