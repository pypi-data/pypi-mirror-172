# Changelog

<!-- prettier-ignore -->
Name | PR | Developer | Date | Version
--- | --- | --- | --- | ---
:bento: Generate collision-safe cell ranger dummy data | [41](https://github.com/laminlabs/lnbfx/pull/41) | [bpenteado](https://github.com/bpenteado) | 2022-10-22 | 0.4.5
🐛 Fix migration | [40](https://github.com/laminlabs/lnbfx/pull/40) | [falexwolf](https://github.com/falexwolf) | 2022-10-20 | 0.4.4
🧑‍💻 Added naming convention | [39](https://github.com/laminlabs/lnbfx/pull/39) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-20 |
🎨 Handle `str` as input to bfx file type annotation | [38](https://github.com/laminlabs/lnbfx/pull/38) | [bpenteado](https://github.com/bpenteado) | 2022-10-17 | 0.4.3
🎨 Improve bfx file type annotation | [37](https://github.com/laminlabs/lnbfx/pull/37) | [bpenteado](https://github.com/bpenteado) | 2022-10-12 |
🩹 Return None for fastq_r2 | [35](https://github.com/laminlabs/lnbfx/pull/35) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-05 | 0.4.2
🍱 Pull pipeline metadata from json in S3 bucket | [34](https://github.com/laminlabs/lnbfx/pull/34) | [bpenteado](https://github.com/bpenteado) | 2022-10-05 |
🍱 Add migrations infra | [33](https://github.com/laminlabs/lnbfx/pull/33) | [falexwolf](https://github.com/falexwolf) | 2022-10-03 | 0.4.1
⬆️ Upgrade to lnschema_core 0.9.0 | [32](https://github.com/laminlabs/lnbfx/pull/32) | [falexwolf](https://github.com/falexwolf) | 2022-09-30 | 0.4.0
🗃️ Update column defaults and id generators | [31](https://github.com/laminlabs/lnbfx/pull/31) | [bpenteado](https://github.com/bpenteado) | 2022-09-29 | 0.3.10
🩹 Return `BfxRun` outputs as `Path` instances | [30](https://github.com/laminlabs/lnbfx/pull/30) | [bpenteado](https://github.com/bpenteado) | 2022-09-29 | 0.3.9
📝 Added API reference | [29](https://github.com/laminlabs/lnbfx/pull/29) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-29 | 0.3.8
🎨 Enrich `BfxRun` properties | [28](https://github.com/laminlabs/lnbfx/pull/28) | [bpenteado](https://github.com/bpenteado) | 2022-09-29 | 0.3.7
🗃️ Add composite fk constraint in `dobject_bfxmeta` | [27](https://github.com/laminlabs/lnbfx/pull/27) | [bpenteado](https://github.com/bpenteado) | 2022-09-29 |
♻️ Move dev functions to `BfxRun` | [26](https://github.com/laminlabs/lnbfx/pull/26) | [bpenteado](https://github.com/bpenteado) | 2022-09-27 |
♻️ Move all ingestion-related logic to `lamindb` | [25](https://github.com/laminlabs/lnbfx/pull/25) | [bpenteado](https://github.com/bpenteado) | 2022-09-23 | 0.3.6
🎨 Sanitize `fastq_bcl_path` (`BfxRun` parameter) | [24](https://github.com/laminlabs/lnbfx/pull/24) | [bpenteado](https://github.com/bpenteado) | 2022-09-23 |
✨ Ingest bfx outs with sample metadata | [23](https://github.com/laminlabs/lnbfx/pull/23) | [bpenteado](https://github.com/bpenteado) | 2022-09-22 |
🐛 Fix run_name return type | [22](https://github.com/laminlabs/lnbfx/pull/22) | [bpenteado](https://github.com/bpenteado) | 2022-09-14 | 0.3.5
🎨 Fix `bfx_run` setup and ingestion | [21](https://github.com/laminlabs/lnbfx/pull/21) | [bpenteado](https://github.com/bpenteado) | 2022-09-14 | 0.3.4
✨ Create pipeline lookup functionality | [17](https://github.com/laminlabs/lnbfx/pull/17) | [bpenteado](https://github.com/bpenteado) | 2022-09-13 | 0.3.3
🚚 Move utility functions to `dev` submodule | [16](https://github.com/laminlabs/lnbfx/pull/16) | [bpenteado](https://github.com/bpenteado) | 2022-09-13 |
📝 Add _001 to fastq names | [19](https://github.com/laminlabs/lnbfx/pull/19) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-12 | 0.3.2
✨ Added dev api | [18](https://github.com/laminlabs/lnbfx/pull/18) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-12 |
Update documentation to `lnbfx` 0.3.2 | [15](https://github.com/laminlabs/lnbfx/pull/15) | [bpenteado](https://github.com/bpenteado) | 2022-08-29 |
🔧 Do not pin schema version in `lnbfx` | [14](https://github.com/laminlabs/lnbfx/pull/14) | [falexwolf](https://github.com/falexwolf) | 2022-08-26 | 0.3.1
🐛 Fix parsing of bfx file type | [9](https://github.com/laminlabs/lnbfx/pull/9) | [bpenteado](https://github.com/bpenteado) | 2022-08-26 | 0.3.0
🏗️ Link bfx pipeline to pipeline | [13](https://github.com/laminlabs/lnbfx/pull/13) | [bpenteado](https://github.com/bpenteado) | 2022-08-26 |
🐛 Remove positional argument `pipeline_run_id` from `check_and_ingest()` | [12](https://github.com/laminlabs/lnbfx/pull/12) | [bpenteado](https://github.com/bpenteado) | 2022-08-26 | 0.2.2
🎨 Rename `BfxRun` attributes and refactor ingestion logic | [11](https://github.com/laminlabs/lnbfx/pull/11) | [bpenteado](https://github.com/bpenteado) | 2022-08-25 | 0.2.1
♻️ Assign run id at `BfxRun` instantiation | [10](https://github.com/laminlabs/lnbfx/pull/10) | [bpenteado](https://github.com/bpenteado) | 2022-08-25 |
🎨 Simplify schema and clean up documentation | [8](https://github.com/laminlabs/lnbfx/pull/8) | [falexwolf](https://github.com/falexwolf) | 2022-08-23 | 0.2.0
🚚 Rename `lndb-bfx-pipeline` to `lnbfx` | [6](https://github.com/laminlabs/lnbfx/pull/6) | [falexwolf](https://github.com/falexwolf) | 2022-08-19 | 0.1.1
✨ Create initial demo functionality | [5](https://github.com/laminlabs/lnbfx/pull/5) | [bpenteado](https://github.com/bpenteado) | 2022-08-18 | 0.1.0
🎉 Create simple pipeline schema and fastq ingestion functionality | [3](https://github.com/laminlabs/lnbfx/pull/3) | [bpenteado](https://github.com/bpenteado) | 2022-07-31 |
⬇️ Downgrade pip to 22.1.2 for CI | [2](https://github.com/laminlabs/lnbfx/pull/2) | [sunnyosun](https://github.com/sunnyosun) | 2022-07-26 |
