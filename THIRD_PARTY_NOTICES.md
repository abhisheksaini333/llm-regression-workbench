# Third-party components

This repository's source and owned task fixtures use the MIT license. Dependency packages retain their original licenses and notices; the lockfile is not a relicensing of those packages.

- [React](https://github.com/facebook/react), [Vite](https://github.com/vitejs/vite), [TypeScript](https://github.com/microsoft/TypeScript), [Vitest](https://github.com/vitest-dev/vitest), [Testing Library](https://github.com/testing-library/react-testing-library) and [Playwright](https://github.com/microsoft/playwright) provide browser/build/test tooling.
- Optional inference uses [PyTorch](https://github.com/pytorch/pytorch), [Transformers](https://github.com/huggingface/transformers) and [SentencePiece](https://github.com/google/sentencepiece).
- [Google FLAN-T5-small](https://huggingface.co/google/flan-t5-small) is Apache-2.0 licensed. Its weights remain upstream; the downloader fetches an explicitly pinned revision with SHA-256 verification. See the upstream model card for training information and model limitations.
- The optional Evals JSONL importer accepts a small public data shape described by [OpenAI Evals](https://github.com/openai/evals). No upstream Evals source or datasets are bundled.

All evaluation tasks and demonstration provider outputs in `fixtures/` are project-owned synthetic examples. Browser demonstration labels exercise the workflow and are not human-study data.
