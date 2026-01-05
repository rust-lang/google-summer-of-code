# Rust project ideas
This page contains a list of ideas for various projects that could help improve
the Rust Project and potentially also the wider Rust community.

These project ideas can be used as inspiration for various OSS contribution programs,
such as [Google Summer of Code](https://summerofcode.withgoogle.com/) or [OSPP](https://summer-ospp.ac.cn/).

This document contains ideas that should still be actual. Here you can also find a list of projects from GSoC runs:

- Google Summer of Code projects
  - [2025](gsoc/runs/2025.md)
  - [2024](gsoc/runs/2024.md)

We invite contributors that would like to participate in projects such as GSoC or that would just want to find a Rust project that they would like to work on to examine the project list and use it as an inspiration. Another source of inspiration can be the [Rust Project Goals](https://rust-lang.github.io/rust-project-goals/index.html), particularly the orphaned goals. However, you can also work on these projects outside GSoC or other similar projects! We welcome all contributions.

If you would like to participate in GSoC, please read [this](gsoc/README.md).
If you would like to discuss projects ideas or anything related to them, you can do so on our [Zulip](https://rust-lang.zulipchat.com/).

We use the GSoC project size parameters for estimating the expected time complexity of the project ideas. The individual project sizes have the following expected amounts of hours:
- Small: 90 hours
- Medium: 175 hours
- Large: 350 hours

## Index
- **Rust Compiler**
    - [Reproducible builds](#reproducible-builds)
    - [Refactoring of rustc_codegen_ssa to make it more convenient for the GCC codegen](#Refactoring-of-rustc_codegen_ssa-to-make-it-more-convenient-for-the-GCC-codegen)
- **Infrastructure**
    - [Port `std::arch` test suite to `rust-lang/rust`](#port-stdarch-test-suite-to-rust-langrust)
- **Cargo**
    - [Move cargo shell completions to Rust](#move-cargo-shell-completions-to-Rust)
- **Rustup**
    - [XDG path support for rustup](#XDG-path-support-for-rustup)
- **Crate ecosystem**
    - [Modernize the libc crate](#Modernize-the-libc-crate)
    - [Add more lints to `cargo-semver-checks`](#add-more-lints-to-cargo-semver-checks)
- **rust-analyzer**
    - [Migrating rust-analyzer assists to `SyntaxEditor`](#migrating-rust-analyzer-assists-to-syntaxeditor)

# Project ideas
The list of ideas is divided into several categories.

## Rust Compiler

### Reproducible builds

**Description**

Recent OSS attacks such as the [XZ backdoor](https://en.wikipedia.org/wiki/XZ_Utils_backdoor)
have shown the importance of having reproducible builds.

Currently, the Rust toolchain distributed to Rust developers is not very reproducible.
Our source code archives should be reproducible as of [this pull request](https://github.com/rust-lang/rust/pull/123246),
however making the actual binary artifacts reproducible is a much more difficult effort.

The goal of this project is to investigate what exactly makes Rust builds not reproducible,
and try to resolve as many such issues as possible.

While the main motivation is to make the Rust toolchain (compiler, standard library, etc.) releases
reproducible, any improvements on this front should benefit the reproducibility of all Rust programs.

See [Tracking Issue for Reproducible Build bugs and challenges](https://github.com/rust-lang/rust/issues/129080)
for a non-exhaustive list of reproducibility challenges.

**Expected result**

Rust builds are more reproducible, ideally the Rust toolchain can be compiled in a reproducible manner.

**Desirable skills**

Knowledge of Rust and ideally also build systems.

**Project size**

Medium.

**Difficulty**

Hard.

**Mentor**
- Jakub Beránek ([GitHub](https://github.com/kobzol), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/266526-Jakub-Ber%C3%A1nek))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20reproducible.20builds)

**Related links**
- [Prior art in Go](https://go.dev/blog/rebuild)

### Refactoring of `rustc_codegen_ssa` to make it more convenient for the GCC codegen

**Description**

[`rustc_codegen_gcc`](https://github.com/rust-lang/rustc_codegen_gcc) uses [`rustc_codegen_ssa`](https://rustc-dev-guide.rust-lang.org/backend/backend-agnostic.html) and implements the traits in this crate in order to have a codegen that plugs in `rustc` seamlessly.
Since `rustc_codegen_ssa` was created based on `rustc_codegen_llvm`, they are somewhat similar, which sometimes makes it awkward for the GCC codegen.
Indeed, some hacks were needed to be able to implement the GCC codegen with this API:

 * Usage of unsafe `transmute`: for instance, [this](https://github.com/rust-lang/rustc_codegen_gcc/blob/8037b6139fea50894978509744f00484150e6816/src/context.rs#L322) or [this](https://github.com/rust-lang/rustc_codegen_gcc/blob/8037b6139fea50894978509744f00484150e6816/src/context.rs#L412). Fixing this might require separating [`Value`](https://github.com/antoyo/rust/blob/c074d8eee765cfd64e6e143d2894c85c7f3ddc1d/compiler/rustc_codegen_ssa/src/traits/backend.rs#L24) into `RValue` and `LValue` or using [`Function`](https://github.com/antoyo/rust/blob/c074d8eee765cfd64e6e143d2894c85c7f3ddc1d/compiler/rustc_codegen_ssa/src/traits/backend.rs#L26) in place of `Value` in some places to better fit the GCC API.
 * Usage of mappings to workaround the API: for instance, [this](https://github.com/rust-lang/rustc_codegen_gcc/blob/8037b6139fea50894978509744f00484150e6816/src/context.rs#L123-L128) or [this](https://github.com/rust-lang/rustc_codegen_gcc/blob/8037b6139fea50894978509744f00484150e6816/src/context.rs#L95-L99).

Some other improvement ideas include:

 * Separate the aggregate operations (structs, arrays): methods like [`extract_value`](https://github.com/rust-lang/rustc_codegen_gcc/blob/8037b6139fea50894978509744f00484150e6816/src/builder.rs#L1423) are generic over structures and arrays because it's the same operation in LLVM, but it is different operations in GCC, so it might make sense to have multiple methods like `extract_field` and `extract_array_element`.
 * Remove duplications between `rustc_codegen_gcc` and `rustc_codegen_llvm` by moving more stuff into `rustc_codegen_ssa`. For instance:
   * [some debuginfo code is exactly the same](https://github.com/rust-lang/rustc_codegen_gcc/blob/8037b6139fea50894978509744f00484150e6816/src/debuginfo.rs#L63)
   * [ABI code](https://github.com/rust-lang/rustc_codegen_gcc/blob/8037b6139fea50894978509744f00484150e6816/src/intrinsic/mod.rs#L509-L569)
   * [the allocator code](https://github.com/rust-lang/rustc_codegen_gcc/blob/8037b6139fea50894978509744f00484150e6816/src/allocator.rs#L16-L91)
   * [the dummy output type for inline assembly](https://github.com/rust-lang/rustc_codegen_gcc/blob/8037b6139fea50894978509744f00484150e6816/src/asm.rs#L704-L793)
   * perhaps we could add a `set_alignment` method in `rustc_codegen_ssa` that asks the backend to set the alignment and is called in `rustc_codegen_ssa` in strategic places so that we don't have to worry as much about alignment in the codegens (not sure if this is possible).

The goal of this project is to improve `rustc_codegen_gcc` by removing hacks, unnecessary unsafe code and/or code duplication with `rustc_codegen_llvm` by refactoring `rustc_codegen_ssa`.
It would be important that this refactoring does not result in a performance degradation for `rustc_codegen_llvm`.

**Expected result**

A `rustc_codegen_gcc` that contains less hacks, unsafe code and/or code duplication with `rustc_codegen_llvm`.

**Desirable skills**

Knowledge of Rust and basic knowledge of `rustc` internals, especially the [codegen part](https://rustc-dev-guide.rust-lang.org/backend/backend-agnostic.html).

**Project size**

Small-Medium depending on the chosen scope.

**Difficulty**

Medium.

**Mentor**
- Antoni Boucher ([GitHub](https://github.com/antoyo), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/404242-antoyo))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Refactoring.20of.20.60rustc_codegen_ssa.60.20for.20cg_gcc)
- [rustc_codegen_gcc](https://rust-lang.zulipchat.com/#narrow/channel/386786-rustc-codegen-gcc/)

## Infrastructure

### Port `std::arch` test suite to `rust-lang/rust`

**Description**

The [`std::arch`](https://doc.rust-lang.org/nightly/std/arch/index.html) module in the standard library provides architecture-specific intrinsic functions, which typically directly map to a single machine instruction.

Currently, it lives in its own [repository](https://github.com/rust-lang/stdarch) outside the main [Rust compiler repository](https://github.com/rust-lang/rust) (`rustc`). The `rustc` repository includes `stdarch` only as a submodule, and does not execute its testsuite on the compiler's CI. This sometimes causes contributor friction, because updates to the compiler can break `stdarch` (and vice versa) and it is not possible to change both the compiler and `stdarch` at once (in the same pull request).

`stdarch` has a comprehensive test suite that tests the intrinsics on several hardware architectures and operating system platforms, and it also includes fuzz tests. It cannot be simply copied over to `rustc`, because that has its own (much more complex) set of CI workflows. The `stdarch` testsuite thus has to be adapted to the way workflows are executed in the compiler repository.

The ultimate goal is to inline `stdarch` into `rustc` completely, and archive the `stdarch` repository. This can be incrementally achieved by the following two steps:

1) Investigate the CI (continuous integration) test suite of `stdarch`, and port as much of it into `rustc`. This will involve implementing new testing and documentation steps for working with `stdarch` in the compiler's build system, [bootstrap](https://rustc-dev-guide.rust-lang.org/building/bootstrapping/how-bootstrap-does-it.html).
2) Once a sufficient portion of the test suite has been ported, `stdarch` should be changed from a submodule to either a git or [Josh](https://josh-project.github.io/josh) subtree, so that compiler contributors are able to make changes to `stdarch` when they modify the compiler. This might involve creating some automation tooling to help with performing regular synchronizations from/to `stdarch`. See [this page](https://rustc-dev-guide.rust-lang.org/external-repos.html#using-external-repositories) for more details.

**Expected result**

The most important parts of the `stdarch` test suite should be running in the CI of the Rust compiler. Ideally, `stdarch` should be included as a git/Josh subtree instead of a submodule, or in the best possible scenario moved completely into `rust-lang/rust`.

**Desirable skills**

Intermediate knowledge of Rust. Experience with GitHub Actions or CI workflows is a benefit.

**Project size**

Small to Medium.

**Difficulty**

Medium.

**Mentors**
- Jakub Beránek ([GitHub](https://github.com/kobzol), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/266526-Jakub-Ber%C3%A1nek))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Port.20.60std.3A.3Aarch.60.20test.20suite.20to.20.60rust-lang.2Frust.60)
- [t-libs/stdarch](https://rust-lang.zulipchat.com/#narrow/channel/208962-t-libs.2Fstdarch)

## Cargo

### Move cargo shell completions to Rust

**Description**

Cargo maintains Bash and Zsh completions, but they are duplicated and limited in features.

A previous GSoC participant added unstable support for completions in Cargo itself,
so we can have a single implementation with per-shell skins ([rust-lang/cargo#6645](https://github.com/rust-lang/cargo/issues/6645)).
- [**Final project report**](https://hackmd.io/@PthRWaPvSmS_2Yu_GLbGpg/Hk-ficKpC)
- [GSoC project annotation](https://summerofcode.withgoogle.com/programs/2024/projects/jjnidpgn)
- [Project discussion on Zulip](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Project.3A.20Move.20cargo.20shell.20completions.20to.20Rust)

There are many more arguments that need custom completers as well as polish in the completion system itself before this can be stabilized.

See
- [Clap's tracking issue](https://github.com/clap-rs/clap/issues/3166)
- [Cargo's tracking issue](https://github.com/rust-lang/cargo/issues/14520)

**Expected result**

Ideal:
- A report to clap maintainers on the state of the unstable completions and why its ready for stabilization
- A report to cargo maintainers on the state of the unstable completions and why its ready for stabilization

**Desirable skills**

Intermediate knowledge of Rust. Shell familiarity is a bonus.

**Project size**

Medium.

**Difficulty**

Medium.

**Mentor**
- Ed Page ([GitHub](https://github.com/epage), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/424212-Ed-Page))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20move.20cargo.20shell.20completions.20to.20Rust)

## Rustup

### XDG path support for rustup

**Description**

[Rustup](https://github.com/rust-lang/rustup) is an indispensable part of
Rust's infrastructure, as it provides easy access to a Rust toolchain to
millions of Rust users.

Historically, rustup has been using `$RUSTUP_HOME` (defaulting to
`$HOME/.rustup`) and a part of `$CARGO_HOME` (defaulting to `$HOME/.cargo`)
environment variable-configurable paths as its config, state, and data
directories, but there has long been a desire to move to a more fine-grained
and standardized solution instead.

It is thus decided by both rustup and cargo teams that, in the future, rustup
will default to using [XDG paths] for its various directories, in collaboration
with corresponding cargo support:

On the one hand, its toolchains, `.env` presets, settings, and cache files
should be placed under the respective XDG paths. An example of this could be
using `$XDG_DATA_HOME/rustup/toolchains` instead of the current
`$RUSTUP_HOME/toolchains`.

On the other hand, its binary proxies (a.k.a. shims) should also be placed
under a reasonable XDG path to be negotiated with the cargo team, so that it
behaves as if it were cargo-installed binary.

The goal of this project is to prepare for the above changes in rustup by:

- Analyzing the dependents of `$RUSTUP_HOME` and `$CARGO_HOME` in rustup (and
  in cargo when necessary) to logically segment them into finer-grained
  directories. The defaults will remain unchanged for now, but the relevant
  code should be refactored to support more flexible directory configuration.

- Establishing a protocol to maintain backward compatibility with existing
  installations of both rustup and cargo and to properly inform users of the
  potential changes.

The above should be implemented in a way that aligns with both rustup and
cargo's progress towards XDG path support, and thus frequent communication with
the cargo team might be necessary in addition to that with rustup.

**Expected result**

- rustup should support fine-grained directory configurations rather than the
  current dual-directory approach, with relevant business logic (esp. that of
  [self-uninstallation][stop nuking `$CARGO_HOME` on `self uninstall`]) and
  docs adjusted accordingly.

  - This means, if the early adopters would like, they will be able to
    manually enforce XDG paths on rustup.

- rustup should be able to no longer enforce `$CARGO_HOME` on cargo to unblock
  relevant cargo changes towards the same direction.

  - On the other hand, rustup should try its best to respect `$RUSTUP_HOME`
    and/or `$CARGO_HOME` overrides and maintain the old behavior if present.

**Desirable skills**

Intermediate knowledge of Rust.

**Project size**

Medium.

**Mentor**
- rami3l ([GitHub](https://github.com/rami3l), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/616990-rami3l))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20XDG.20path.20support.20for.20rustup/with/566344314)
- [Rustup team](https://rust-lang.zulipchat.com/#narrow/channel/490103-t-rustup)

**Related Links**
- [All hands 2025 joint meeting notes on XDG support](https://blog.rust-lang.org/inside-rust/2025/10/01/this-development-cycle-in-cargo-1.90/#all-hands-xdg-paths)
- Rustup issue: [platform-specific config directories](https://github.com/rust-lang/rustup/issues/247)
- Rustup issue: [stop nuking `$CARGO_HOME` on `self uninstall`]
- Pre-RFC: [Split `$CARGO_HOME`](https://internals.rust-lang.org/t/pre-rfc-split-cargo-home/19747)
  - Rustup issue: [stop setting `$CARGO_HOME`](https://github.com/rust-lang/rustup/issues/4502)
- [XDG paths] specification

[XDG paths]: https://specifications.freedesktop.org/basedir/latest/
[stop nuking `$CARGO_HOME` on `self uninstall`]: https://github.com/rust-lang/rustup/issues/285

## Crate ecosystem

### Modernize the libc crate

**Description**

The [libc](https://github.com/rust-lang/libc) crate is one of the oldest crates of the Rust ecosystem, long predating Rust 1.0. Additionally, it is one of the most widely used crates in the ecosystem (#4 most downloaded on crates.io).
This combinations means that the current version of the libc crate (`v0.2`) is very conservative with breaking changes has accumulated a list of things to do in a 1.0 release. Additionally, some of the infrastructure for `lib` is rather outdated.

Most of the changes required for 1.0 are under the [1.0 milestone](https://github.com/rust-lang/libc/milestone/1). Some of these come from the evolution of the underlying platforms, some come from a desire to use newer language features, while others are simple mistakes that we cannot correct without breaking existing code.

The goal of this project is to prepare and release the next major version of the libc crate.

> Note: there was a project with a similar topic in [GSoC 2025](https://blog.rust-lang.org/2025/11/18/gsoc-2025-results/#modernising-the-libc-crate). But since there is a lot of work to be done, we have published this project idea again.

**Expected result**

The libc crate is cleaned up and modernized, and released as version 0.3.

**Desirable skills**

Intermediate knowledge of Rust.

**Project size**

Medium.

**Difficulty**

Medium.

**Mentor**
- Trevor Gross ([GitHub](https://github.com/tgross35), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/532317-Trevor-Gross))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20modernize.20the.20libc.20crate)
- [Library team](https://rust-lang.zulipchat.com/#narrow/stream/219381-t-libs)

### Add more lints to `cargo-semver-checks`

**Description**

[`cargo-semver-checks`](https://github.com/obi1kenobi/cargo-semver-checks) is a linter for semantic versioning. It ensures
that Rust crates adhere to semantic versioning by looking for breaking changes in APIs.

It can currently catch ~120 different kinds of breaking changes, meaning there are hundreds of kinds of breaking changes it
still cannot catch! The goal of this project is to extend its abilities, so that it can catch and prevent more breaking changes, by:
- adding more lints, which are expressed as queries over a database-like schema ([playground](https://play.predr.ag/rustdoc))
- extending the schema, so more Rust functionality is made available for linting

**Expected result**

`cargo-semver-checks` will contain new lints, together with test cases that both ensure the lint triggers when expected
and does not trigger in situations where it shouldn't (AKA false-positives).

**Desirable skills**

Intermediate knowledge of Rust. Familiarity with databases, query engines, or query language design is welcome but
not required.

**Project size**

Medium or large, depends on how many lints will be implemented. The more lints, the better!

**Difficulty**

Medium to high, depends on the choice of implemented lints or schema extensions.

**Mentor**
- Predrag Gruevski ([GitHub](https://github.com/obi1kenobi/), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/474284-Predrag-Gruevski-(he-him)))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20add.20more.20lints.20to.20.60cargo-semver-checks.60)

**Related Links**
- [Playground where you can try querying Rust data](https://play.predr.ag/rustdoc)
- [GitHub issues describing not-yet-implemented lints](https://github.com/obi1kenobi/cargo-semver-checks/issues?q=is%3Aissue+is%3Aopen+label%3AE-mentor+label%3AA-lint+)
- [Opportunities to add new schema, enabling new lints](https://github.com/obi1kenobi/cargo-semver-checks/issues/241)
- [Query engine adapter](https://github.com/obi1kenobi/trustfall-rustdoc-adapter)

## rust-analyzer

### Migrating rust-analyzer assists to `SyntaxEditor`

**Description**

rust-analyzer has many assists (code actions) that operate on the syntax tree. Most of them are implemented via mutable syntax tree editing, with `rowan`, our syntax tree library. Unfortunately, the existence of mutable syntax trees prohibits a lot of optimizations in `rowan` and makes it a lot more memory-heavy and slower. Therefore we'd like to remove our usage of mutable trees.

We developed an API called `SyntaxEditor` that should be used instead of mutable trees. Currently it is implemented with them under the hood, but it is expected to be easier to get rid of them once all mutation is encapsulated in it.

**Expected result**

rust-analyzer has no assists or diagnostics quickfixes that use mutable tree editing. This will likely also involve further development of the `SyntaxEditor` API, as per the needs.

**Desirable skills**

Knowledge of Rust. Knowledge of the rust-analyzer codebase is an advantage but should not be required.

**Project size**

Large. However note that the size is scalable; even if the project isn't completed, every assist we migrate is a net benefit.

**Difficulty**

Easy.

**Mentors**

 - Chayim Refael Friedman ([GitHub](https://github.com/ChayimFriedman2/), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/340138-Chayim-Refael-Friedman))
 - Lukas Wirth ([GitHub](https://github.com/Veykril), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/300586-Lukas-Wirth))

**Related Links**

 - [An issue explaining why we should get rid of mutable syntax trees architecture-wise](https://github.com/rust-lang/rust-analyzer/issues/15710)
 - [Tracking issue for this effort](https://github.com/rust-lang/rust-analyzer/issues/18285)
 - [A prototype exploring how `rowan` without mutable trees could look like](https://github.com/ChayimFriedman2/rowan/tree/next-rowan)
