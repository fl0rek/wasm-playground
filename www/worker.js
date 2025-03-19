import init, { WasmApp } from "./pkg/wasm_app.js";

async function init_wasm_in_worker() {
  await init();
  console.log("Let's go");

  // sanity check, works
  let error = new Error("Error inside worker");
  console.info("Expecing Error inside worker, js");
  console.error("Error inside worker js:", error);

  let ch = new MessageChannel();
  ch.port1.onmessage = (ev) => {
    // expecting this to be logged twice, as 2 messages are posted in wasm
    console.warn("Received from wasm: ", ev.data);
  };

  let _app = new WasmApp(ch.port2);
}

init_wasm_in_worker();
