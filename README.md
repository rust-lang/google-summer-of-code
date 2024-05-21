# Rust project ideas
This page contains a list of ideas for medium-sized projects that could help improve
the Rust Project and potentially also the wider Rust community.

Some of these projects were used as inspiration for various OSS contribution programs,
such as [Google Summer of Code](https://summerofcode.withgoogle.com/) and [OSPP](https://summer-ospp.ac.cn/).

- Google Summer of Code projects
  - [2024](gsoc/2024.md)

We invite contributors that would like to participate in projects such as GSoC or that would just want to find a Rust project that they would like to work on to examine the project list and use it as an inspiration.

If you would like to discuss projects ideas or anything related to them, you can do so on our [Zulip](https://rust-lang.zulipchat.com/).

We use the GSoC project size parameters for estimating the expected time complexity of the project ideas. The individual project sizes have the following expected amounts of hours:
- Small: 90 hours
- Medium: 175 hours
- Large: 350 hours

## Index
- **Rust Compiler**
    - [C codegen backend for rustc](#C-codegen-backend-for-rustc)
    - [Extend annotate-snippets with features required by rustc](#Extend-annotate-snippets-with-features-required-by-rustc)
    - [Reproducible builds](#reproducible-builds)
- **Infrastructure**
    - [Add support for multiple collectors to the Rust benchmark suite](#Add-support-for-multiple-collectors-to-the-Rust-benchmark-suite)
    - [Improve bootstrap](#Improve-bootstrap)
    - [Improve infrastructure automation tools](#Improve-infrastructure-automation-tools)
- **Cargo**
    - [Implement workspace publish in Cargo](#implement-workspace-publish-in-cargo)
- **Rustfmt**
    - [Improve rustfmt infrastructure and automation](#improve-rustfmt-infrastructure-and-automation)
- **Crate ecosystem**
    - [Modernize the libc crate](#Modernize-the-libc-crate)
    - [Add more lints to `cargo-semver-checks`](#add-more-lints-to-cargo-semver-checks)
    - [Implement a cryptographic algorithm in RustCrypto](#implement-a-cryptographic-algorithm-in-rustcrypto)

# Project ideas
The list of ideas is divided into several categories.

## Rust Compiler

### C codegen backend for `rustc`

**Description**

`rustc` currently has three in-tree codegen backends: LLVM (the default), Cranelift, and GCC.
These live at <https://github.com/rust-lang/rust/tree/master/compiler>, as `rustc_codegen_*` crates.

The goal of this project is to add a new experimental `rustc_codegen_c` backend that could turn Rust's internal
representations into `C` code (i.e. transpile) and optionally invoke a `C` compiler to build it. This will allow Rust
to use benefits of existing `C` compilers (better platform support, optimizations) in situations where the existing backends
cannot be used.

**Expected result**

The minimum viable product is to turn `rustc` data structures that represent a Rust program into `C` code, and write the
output to the location specified by `--out-dir`. This involves figuring out how to produce buildable `C` code from the
inputs provided by `rustc_codegen_ssa::traits::CodegenBackend`.

A second step is to have `rustc` invoke a `C` compiler on these produced files. This should be designed in a pluggable way,
such that any `C` compiler can be dropped in.

**Desirable skills**

Knowledge of Rust and `C`, basic familiarity with compiler functionality.

**Project size**

Large.

**Difficulty**

Hard.

**Mentor**
- Trevor Gross ([GitHub](https://github.com/tgross35), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/532317-Trevor-Gross))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20C.20codegen.20backend.20for.20.60rustc.60)
- [Compiler team](https://rust-lang.zulipchat.com/#narrow/stream/131828-t-compiler)
- [Previous discussion about this topic](https://rust-lang.zulipchat.com/#narrow/stream/122651-general/topic/rustc_codegen_c)

### Extend `annotate-snippets` with features required by rustc

**Description**

`rustc` currently has incomplete support for using [`annotate-snippets`](https://github.com/rust-lang/annotate-snippets-rs/)
to emit errors, but it doesn't support all the features that `rustc`'s built-in diagnostic rendering does. The goal
of this project is to execute the `rustc` test suite using `annotate-snippets`, identify missing features or bugs,
fix those, and repeat until at feature-parity.

**Expected result**

More of the `rustc` test suite passes with `annotate-snippets`.

**Desirable skills**

Knowledge of Rust.

**Project size**

Medium.

**Difficulty**

Medium or hard.

**Mentor**
- David Wood ([GitHub](https://github.com/davidtwco), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/116107-davidtwco))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20extend.20annotate-snippets)
- [Compiler team](https://rust-lang.zulipchat.com/#narrow/stream/131828-t-compiler)

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

**Expected result**

Rust builds are more reproducible, ideally the Rust toolchain can be compiled in a reproducible manner.

**Desirable skills**

Knowledge of Rust and ideally also build systems.

**Project size**

Medium.

**Difficulty**

Large.

**Mentor**
- Jakub Beránek ([GitHub](https://github.com/kobzol), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/266526-Jakub-Ber%C3%A1nek))

**Related links**
- [Prior art in Go](https://go.dev/blog/rebuild)

## Infrastructure

### Add support for multiple collectors to the Rust benchmark suite

**Description**

Rust has an extensive [benchmark suite](https://github.com/rust-lang/rustc-perf) that measures the performance of the Rust compiler and Rust programs and
visualizes the results in an interactive web application. Currently, the benchmarks are gathered on a single physical
machine, however we are hitting the limits of how many benchmark runs we can perform per day on a single machine,
which in turn limits the benchmark configurations that we can execute after each commit.

The goal of this project is to add support for splitting benchmark execution across multiple machines. This will
require a refactoring of the existing suite and potentially also database schema modifications and implementation of new
features.

**Expected result**

It will be possible to parallelize the execution of the benchmark suite across multiple machines.

**Desirable skills**

Intermediate knowledge of Rust and database technologies (SQL).

**Project size**

Medium or large.

**Difficulty**

Medium.

**Mentor**
- Jakub Beránek ([GitHub](https://github.com/kobzol), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/266526-Jakub-Ber%C3%A1nek))

**Zulip stream**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20multiple.20collectors.20for.20Rust.20benchmark.20suite)
- [Compiler performance working group](https://rust-lang.zulipchat.com/#narrow/stream/247081-t-compiler.2Fperformance)

### Improve bootstrap

**Description**

The Rust compiler it bootstrapped using a complex set of scripts and programs generally called just `bootstrap`.
This tooling is constantly changing, and it has accrued a lot of technical debt. It could be improved in many areas, for example:

- Design a new testing infrastructure and write more tests.
- Write documentation.
- Remove unnecessary hacks.

**Expected result**

The `bootstrap` tooling will have less technical debt, more tests, and better documentation.

**Desirable skills**

Intermediate knowledge of Rust. Knowledge of the Rust compiler bootstrap process is welcome, but not required.

**Project size**

Medium or large.

**Difficulty**

Medium.

**Mentor**
- AlbertLarsan68 ([GitHub](https://github.com/albertlarsan68), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/510016-Albert-Larsan))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20improve.20bootstrap)
- [Bootstreap team](https://rust-lang.zulipchat.com/#narrow/stream/326414-t-infra.2Fbootstrap)

### Improve infrastructure automation tools

**Description**

Rust infrastructure uses many custom tools designed for automating pull request merging, handling discussions on Zulip,
managing GitHub permissions etc. It would be a great help to Rust maintainers if these tools were improved. Here are a
few possible tasks that could be implemented:

- Complete the implementation of [bors](https://github.com/rust-lang/bors), our new implementation of a merge queue
bot for GitHub. It currently lacks support for performing merges (it can only perform so-called "try builds").
- Add support for interacting with the Rust team calendar through Zulip, using e.g. some kind of GitHub app bot.
- Add support for creating Zulip streams using the [Rust team data](https://github.com/rust-lang/team) repository.
- Implement a GitHub app for [sync-team](https://github.com/rust-lang/sync-team), our tool for managing permissions of Rust maintainers.

**Expected result**

Rust infrastructure management tools will receive new features, better documentation and tests.

**Desirable skills**

Intermediate knowledge of Rust. Familiarity with GitHub APIs is a bonus.

**Project size**

Medium.

**Difficulty**

Medium.

**Mentors**
- Jakub Beránek ([GitHub](https://github.com/kobzol), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/266526-Jakub-Ber%C3%A1nek)) (bors, sync-team)
- Jack Huey ([GitHub](https://github.com/jackh726), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/232957-Jack-Huey)) (triagebot)

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20improve.20infrastructure.20automation.20tools)
- [Infra team](https://rust-lang.zulipchat.com/#narrow/stream/242791-t-infra)

## Cargo

### Implement workspace publish in Cargo

**Description**

Today, developers can group Rust packages into a workspace to make it easier to operate on all of them at once.
However, `cargo package` and `cargo publish` do not support operating on workspaces ([rust-lang/cargo#1169](https://github.com/rust-lang/cargo/issues/1169)).

The goal of this project is to modify the Cargo build tool to add support for packaging and publishing Cargo workspaces.

**Expected result**

Milestone 1: `cargo package` can be run, with verification, with the standard package selection flags
Milestone 2: `cargo publish` can do the same as above, but also serially post the `.crate` files to the registry when done,
reporting to the user what was posted/failed if interrupted.

**Desirable skills**

Intermediate knowledge of Rust.

**Project size**

Medium.

**Difficulty**

Medium.

**Mentor**
- Ed Page ([GitHub](https://github.com/epage), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/424212-Ed-Page))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20implement.20workspace.20publish.20in.20Cargo)
- [Cargo team](https://rust-lang.zulipchat.com/#narrow/stream/246057-t-cargo)

## Rustfmt

### Improve rustfmt infrastructure and automation

**Description**

Rustfmt is the code formatter for Rust code. Currently, to ensure stability, rustfmt uses unit tests that ensure a source file do not get reformatted unexpectedly. Additionally, there is a tool (currently a shell script) called [`diffcheck`](https://github.com/rust-lang/rustfmt/blob/master/ci/check_diff.sh#L187-L216) that gets run to check potentially unexpected changes across different large codebases. We would like to improve our tooling around that, namely improving the diffcheck job to include more crates, improve reporting (with HTML output, like a mini [crater](https://crater-reports.s3.amazonaws.com/pr-114776-1/index.html), which runs compiler changes against all Rust crates published to crates.io), potentially rewriting the job in Rust, and reliability.

Rustfmt currently has a versioning system that gates unstable changes behind `Version=Two`, and the diffcheck job may be less reliable to report changes to `Version=One` when changes to unstable formatting are introduced. We'd like to see this story improved to make our test system more robust.

**Expected result**

A more robust and reliable infrastructure for testing the rustfmt codebase, potentially rewritten in Rust, with HTML output.

**Desirable skills**

Intermediate knowledge of Rust. Knowledge of CI and automation welcomed.

**Project size**

Small or medium, depending on the scale proposed.

**Difficulty**

Small or medium.

**Mentor**
- Yacin Tmimi ([GitHub](https://github.com/ytmimi), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/441976-Yacin-Tmimi))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20improve.20rustfmt.20infrastructure.20and.20automation)

**Related Links**
- [Previous discussion around the idea](https://rust-lang.zulipchat.com/#narrow/stream/357797-t-rustfmt/topic/meeting.202023-01-08/near/411836200)

## Crate ecosystem

### Modernize the libc crate

**Description**

The [libc](https://github.com/rust-lang/libc) crate is one of the oldest crates of the Rust ecosystem, long predating
Rust 1.0. Additionally, it is one of the most widely used crates in the ecosystem (#4 most downloaded on crates.io).
This combinations means that the current version of the libc crate (`v0.2`) is very conservative with breaking changes and
remains backwards-compatible with all Rust compilers since Rust 1.13 (released in 2016).

The language has evolved a lot since Rust 1.13, and we would like to make use of these features in libc. The main one is
support for `union` types to proper expose C unions.

At the same time there, is a backlog of desired breaking changes tracked in [this issue](https://github.com/rust-lang/libc/issues/3248). Some of these come from
the evolution of the underlying platforms, some come from a desire to use newer language features, while others are
simple mistakes that we cannot correct without breaking existing code.

The goal of this project is to prepare and release the next major version of the libc crate.

**Expected result**

The libc crate is cleaned up and modernized, and released as version 0.3.

**Desirable skills**

Intermediate knowledge of Rust.

**Project size**

Medium.

**Difficulty**

Medium.

**Mentor**
- Amanieu d'Antras ([GitHub](https://github.com/Amanieu), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/143274-Amanieu))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20modernize.20the.20libc.20crate)
- [Library team](https://rust-lang.zulipchat.com/#narrow/stream/219381-t-libs)

### Add more lints to `cargo-semver-checks`

**Description**

[`cargo-semver-checks`](https://github.com/obi1kenobi/cargo-semver-checks) is a linter for semantic versioning. It ensures
that Rust crates adhere to semantic versioning by looking for breaking changes in APIs.

It can currently catch ~60 different kinds of breaking changes, so there are hundreds of kinds of breaking changes it
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

Small or large (depends on how many lints will be implemented).

**Difficulty**

Small or medium (depends on the choice of implemented lints or schema extensions).

**Mentor**
- Predrag Gruevski ([GitHub](https://github.com/obi1kenobi/), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/474284-Predrag-Gruevski-(he-him)))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20add.20more.20lints.20to.20.60cargo-semver-checks.60)

**Related Links**
- [Playground where you can try querying Rust data](https://play.predr.ag/rustdoc)
- [GitHub issues describing not-yet-implemented lints](https://github.com/obi1kenobi/cargo-semver-checks/issues?q=is%3Aissue+is%3Aopen+label%3AE-mentor+label%3AA-lint+)
- [Opportunities to add new schema, enabling new lints](https://github.com/obi1kenobi/cargo-semver-checks/issues/241)
- [Query engine adapter](https://github.com/obi1kenobi/trustfall-rustdoc-adapter)

### Implement a cryptographic algorithm in RustCrypto

**Description**

The [RustCrypto Project](https://github.com/RustCrypto) maintains pure Rust implementations of
hundreds of cryptographic algorithms, organized into repositories by algorithm type, e.g.
block ciphers, stream ciphers, hash functions.

Each of these repositories contains a tracking issue identifying specific algorithms which currently
lack an implementation, some of which are linked in the "Related Links" section below. Interested
students can look through these issues and identify an algorithm which is currently unimplemented
which sounds interesting to them, and then implement it as part of this project.

Alternatively, instead of implementing a new algorithm from scratch, a student could potentially
choose to implement some significant unit of functionality in an existing algorithm implementation
with an open associated issue on our GitHub trackers, an example of which might be
[implementing hardware acceleration support for our "bignum" library](https://github.com/RustCrypto/crypto-bigint/issues/1).

**Expected result**

One or more Rust crates/libraries containing a new implementation of a cryptographic algorithm implemented in pure Rust.

**Desirable skills**

Intermediate knowledge of Rust.

A background in mathematics, and some prior knowledge of cryptography, is helpful but not required,
and we can provide guidance and review to ensure code is correct and securely implemented.

**Project size**

Will vary depending on the algorithm/project selected, but ideally small.

Note that while the code size of the deliverable may not be significant, due to the nature of
cryptographic work it will typically still involve significant effort and iteration to deliver an
implementation which is correct and secure.

**Difficulty**

Will also vary depending on the algorithm/project selected, but expected difficulty is medium/hard, as noted above.

**Mentor**
- Tony Arcieri ([GitHub](https://github.com/tarcieri/), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/132721-Tony-Arcieri))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20implement.20a.20cryptographic.20algorithm.20in.20RustCrypto)

**Related Links**
- [Potential AEAD cipher projects](https://github.com/RustCrypto/AEADs/issues/1)
- [Potential block cipher projects](https://github.com/RustCrypto/block-ciphers/issues/1)
- [Potential elliptic curve projects](https://github.com/RustCrypto/elliptic-curves/issues/114)
- [Potential hash function projects](https://github.com/RustCrypto/hashes/issues/1)
- [Potential signature algorithm projects](https://github.com/RustCrypto/signatures/issues/8)
- [Potential stream cipher projects](https://github.com/RustCrypto/stream-ciphers/issues/219)
- [Potential SSH-related projects](https://github.com/RustCrypto/SSH/issues/2)
