"""The stand-in Resource registry the test suite runs against.

WHY THIS EXISTS. The engine builders in `scripts/consume_art_queue_core.py`
resolve their model constants through the Kind Robots Resource registry
(`resolve_model` -> `_load_resource_index`), which issues a real HTTP GET to
`$KR_BASE_URL/api/resources` -- production, by default. An unstubbed test that
reaches `entry_to_job()` therefore depends on kindrobots.org being up.

That was measured on 2026-09-01 (conductor/t-124):

  - A momentary 502 at production failed 17 tests in a roadmap-note-only PR,
    a diff containing no code at all.
  - The registry is memoized into a module global ONLY ON SUCCESS -- the raise
    in `_load_resource_index` precedes `_RESOURCE_INDEX = index` -- so a failing
    registry is re-fetched by every test that reaches `resolve_model`. Against a
    counting stub the suite made 18 separate requests, not one.
  - `http_json` defaults to `timeout=60`, so a registry that HANGS rather than
    erroring costs a full minute per test. Measured: one test 60.27s, two tests
    120.43s -- exactly additive. 18 x 60s is 18 minutes, which is the shape of
    the 20+ minute `Python test suite` stall t-124 was filed for.

Pinning the index in `conftest.py` removes both failure modes and takes CI off
a dependency on production being reachable.

KEEPING THIS CURRENT. It covers exactly the models the engine constants name.
Registering a new engine model means adding it here too -- if you do not,
`resolve_model` warns and passes the logical name through, and the test sees a
name ComfyUI would reject rather than a hard failure.
"""

FAKE_RESOURCE_INDEX = {
    "DIFFUSION_MODEL": {
        "flux2_dev_fp8mixed": "flux2_dev_fp8mixed.safetensors",
        "krea2-turbo": "Krea-2-Turbo-Q5_K_S.gguf",
    },
    "TEXT_ENCODER": {
        "mistral_3_small_flux2_bf16": "mistral_3_small_flux2_bf16.safetensors",
        "qwen_3_8b": "qwen_3_8b.safetensors",
    },
    "VAE": {
        "flux2-vae": "flux2-vae.safetensors",
        "krea2-vae": "krea2_vae.safetensors",
    },
}
