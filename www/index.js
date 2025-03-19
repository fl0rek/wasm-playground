import init from "./pkg/wasm_app.js";

init().then(() => {
  let worker = new Worker(new URL("./worker.js", import.meta.url));

  // sanity check, works
  let error = new Error("Error outside worker");
  console.error("Error inside worker js:", error);
});
