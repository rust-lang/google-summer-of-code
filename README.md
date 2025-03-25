# Rust project ideas
This page contains a list of ideas for various projects that could help improve
the Rust Project and potentially also the wider Rust community.

These project ideas can be used as inspiration for various OSS contribution programs,
such as [Google Summer of Code](https://summerofcode.withgoogle.com/) or [OSPP](https://summer-ospp.ac.cn/).

This document contains ideas that should still be actual and that were not yet completed. Here you can also find an archive of older projects from past GSoC events:

- Past Google Summer of Code projects
  - [2024](gsoc/past/2024.md)

We invite contributors that would like to participate in projects such as GSoC or that would just want to find a Rust project that they would like to work on to examine the project list and use it as an inspiration. Another source of inspiration can be the [Rust Project Goals](https://rust-lang.github.io/rust-project-goals/index.html), particularly the orphaned goals.

If you would like to participate in GSoC, please read [this](gsoc/README.md).
If you would like to discuss projects ideas or anything related to them, you can do so on our [Zulip](https://rust-lang.zulipchat.com/).

We use the GSoC project size parameters for estimating the expected time complexity of the project ideas. The individual project sizes have the following expected amounts of hours:
- Small: 90 hours
- Medium: 175 hours
- Large: 350 hours

## Index
- **Rust Compiler**
    - [Extend annotate-snippets with features required by rustc](#Extend-annotate-snippets-with-features-required-by-rustc)
    - [Reproducible builds](#reproducible-builds)
    - [Bootstrap of rustc with rustc_codegen_gcc](#Bootstrap-of-rustc-with-rustc_codegen_gcc)
    - [Refactoring of rustc_codegen_ssa to make it more convenient for the GCC codegen](#Refactoring-of-rustc_codegen_ssa-to-make-it-more-convenient-for-the-GCC-codegen)
    - [ABI/Layout handling for the automatic differentiation feature](#abilayout-handling-for-the-automatic-differentiation-feature)
    - [Improving parallel frontend](#improving-parallel-frontend)
    - [Prepare `stable_mir` crate for publishing](#prepare-stable_mir-crate-for-publishing)
    - [C codegen backend for rustc](#C-codegen-backend-for-rustc)
- **Rust standard library**
    - [Extend testing of `std::arch` intrinsics](#extend-testing-of-stdarch-intrinsics)
    - [Add safety contracts](#Add-safety-contracts)
- **Infrastructure**
    - [Implement merge functionality in bors](#implement-merge-functionality-in-bors)
    - [Improve bootstrap](#Improve-bootstrap)
    - [Port `std::arch` test suite to `rust-lang/rust`](#port-stdarch-test-suite-to-rust-langrust)
- **Rustup**
    - [Make rustup concurrent](#make-rustup-concurrent)  
- **Cargo**
    - [Prototype an alternative architecture for `cargo fix`](#prototype-an-alternative-architecture-for-cargo-fix)
    - [Prototype Cargo plumbing commands](#prototype-cargo-plumbing-commands)
    - [Move cargo shell completions to Rust](#move-cargo-shell-completions-to-Rust)
    - [Build script delegation](#build-script-delegation)
- **rust-analyzer**
    - [Implement a new proc-macro server RPC API](#implement-a-new-proc-macro-server-RPC-API)
- **Crate ecosystem**
    - [Modernize the libc crate](#Modernize-the-libc-crate)
    - [Add more lints to `cargo-semver-checks`](#add-more-lints-to-cargo-semver-checks)
    - [Make `cargo-semver-checks` run faster](#make-cargo-semver-checks-run-faster)
    - [Enable witness generation in `cargo-semver-checks`](#enable-witness-generation-in-cargo-semver-checks)
    - [Wild linker with test suites from other linkers](#wild-linker-with-test-suites-from-other-linkers)

# Project ideas
The list of ideas is divided into several categories.

## Rust Compiler

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

### Bootstrap of rustc with `rustc_codegen_gcc`

**Description**

[`rustc_codegen_gcc`](https://github.com/rust-lang/rustc_codegen_gcc) [used to be able to compile `rustc`](https://blog.antoyo.xyz/rustc_codegen_gcc-progress-report-10) and use the resulting compiler to successfully compile a `Hello, World!` program.
While it can still compile a [stage 2](https://rustc-dev-guide.rust-lang.org/building/bootstrapping/what-bootstrapping-does.html#stage-2-the-truly-current-compiler) `rustc`, the resulting compiler cannot compile the standard library anymore.

The goal of this project would be to fix in `rustc_codegen_gcc` any issue preventing the resulting compiler to compile a `Hello, World!` program and the standard library.
Those issues are not known, so the participant would need to attempt to do a bootstrap and investigate the issues that arises.

If time allows, an optional additional goal could be to be able to do a full bootstrap of `rustc` with `rustc_codegen_gcc`, meaning fixing even more issues to achieve this result.

**Expected result**

A `rustc_codegen_gcc` that can compile a stage 2 `rustc` where the resulting compiler can compile a `Hello, World!` program using the standard library (also compiled by that resulting compiler).

An optional additional goal would be: a `rustc_codegen_gcc` that can do a full bootstrap of the Rust compiler. This means getting a stage 3 `rustc` that is identical to stage 2.

**Desirable skills**

Good debugging ability. Basic knowledge of:

 * Intel x86-64 assembly (for debugging purposes).
 * `rustc` internals, especially the [codegen part](https://rustc-dev-guide.rust-lang.org/backend/backend-agnostic.html).
 * [`libgccjit`](https://gcc.gnu.org/onlinedocs/jit/) and [GCC internals](https://gcc.gnu.org/onlinedocs/gccint/).

**Project size**

Medium-Large depending on the chosen scope.

**Difficulty**

Hard.

**Mentor**
- Antoni Boucher ([GitHub](https://github.com/antoyo), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/404242-antoyo))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Bootstrap.20of.20rustc.20with.20.60rustc_codegen_gcc.60)
- [rustc_codegen_gcc](https://rust-lang.zulipchat.com/#narrow/channel/386786-rustc-codegen-gcc/)

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

### ABI/Layout handling for the automatic differentiation feature

**Description**

Over the last year, support for automatic differentiation ('autodiff') was added to the Rust compiler. The autodiff tool which we are using ([Enzyme](https://enzyme.mit.edu/)) operates
on LLVM-IR, which is the intermediate representation of code, used by LLVM. LLVM is the default backend of the Rust compiler. Unfortunately, two layout related problems limit its usability.

A) The Rust compiler has a set of ABI optimizations which can improve performance, but make it harder for autodiff to work. An example is the function `fn foo(a: f32, b: f32) -> f32`,
which the compiler might optimize to `fn foo(x: i64) -> f32`. While this is fine from an LLVM perspective, it makes it hard for Enzyme, the LLVM based autodiff tool.
More information about such optimizations can be found [here](https://rust-lang.zulipchat.com/#narrow/channel/182449-t-compiler.2Fhelp/topic/.E2.9C.94.20Where.20do.20ABI.20.22changes.22.20happen.3F).
If a function has a `#[rustc_autodiff]` attribute, the Rust compiler should simply not perform such optimizations. We don't want to disable these optimizations for all functions, as they are generally beneficial.
Multiple examples of function headers which will get handled incorrectly at the moment are listed [here](https://github.com/EnzymeAD/rust/issues/105).

B) Enzyme requires good information about the memory layout of types, both to be able to differentiate the code, and to do so efficiently. In order to help Enzyme,
we want to lower more Type Information from MIR or even THIR into LLVM-IR metadata, or make better usage of existing debug info. If you are interested in this part and
also have some LLVM experience, please have a look at the LLVM website for the related proposal.

For both A) and B), the online compiler explorer [here](https://enzyme.mit.edu/explorer/) can be used to trigger both types of bugs, to get a feeling for existing problems.

**Expected result**

The Rust compiler should not perform ABI optimizations on functions with the `#[rustc_autodiff]` attribute. As a result, `#[autodiff(..)]` should be able to handle functions with almost arbitrary headers. If a general solution turns out tricky, it is ok to focus on the most common types like those listed in the issue above (e.g. combinations of floats, small arrays/structs/tuples, etc.). We care less about advanced types like those listed [here](https://doc.rust-lang.org/reference/special-types-and-traits.html). These changes can't have a performance impact on functions without the `#[rustc_autodiff]` attribute.

Newly working testcases should be added to the rust test suite. The `rustc_autodiff` parsing in the [autodiff frontend](https://github.com/rust-lang/rust/pull/129458) might need small bugfixes if the new testcases discover additional bugs, but those can also be solved by other contributors.

Examples for code that currently is not handled correctly can be discussed in the project proposal phase.

**Desirable skills**

Intermediate knowledge of Rust. Familiarity with ABIs is a bonus, but not required.

**Project size**

Medium

**Difficulty**

Medium to hard.

**Mentors**
- Manuel Drehwald ([GitHub](https://github.com/zusez4), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/348574-Manuel-Drehwald))
- Oli ([GitHub](https://github.com/oli-obk), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/124288-oli))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20ABI.2FLayout.20handling.20for.20automatic.20differentiation)
- [Automatic differentiation working group](https://rust-lang.zulipchat.com/#narrow/channel/390790-wg-autodiff)

### Improving parallel frontend

**Description**

Improving compiler performance has always been a focus of the Rust community and one of the main tasks of the compiler team. [Parallelization](https://rustc-dev-guide.rust-lang.org/parallel-rustc.html) of rust compiler is an important and effective approach.
Currently, the backend end (codegen part) of the compiler has been parallelized, which has brought a huge improvement in the performance of the compiler. However, there is still much room for improvement in the parallelization of the rust frontend.

The most important and valuable work in this area are two aspects:

A) Diagnosing and fixing deadlock [issues](https://github.com/rust-lang/rust/issues?q=is%3Aopen+label%3AWG-compiler-parallel+deadlock) caused by the execution order of compiler queries in a multithreaded environment.
[Queries](https://rustc-dev-guide.rust-lang.org/query.html) is a unique design of the Rust compiler, which is used to achieve incremental compilation process. It divides the compiler
process into various parts and caches the execution results of each part. However, queries caching dependencies between multiple threads may cause deadlock.
[`Work-stealing`](https://en.wikipedia.org/wiki/Work_stealing), a method used to improve parallelization performance, is the core reason.

To solve these problems, we need to find the part of the compiler process that causes deadlock through diagnosing coredumps in issues, and adjusting the execution order
of this part of code so that there will be no circular dependencies on the query caches between multiple threads. This [PR](https://github.com/rust-lang/rust/pull/118488) is a good example of solving a deadlock problem.

B) Improving the performance of the parallel frontend
The parallel frontend has implemented parallelization in type checking, MIR borrow checking and other parts of the compiler. However, there is still a lot of room for improvement:
- HIR lowering. Modifying the array structure of `tcx.untracked.definitions` so that it can be accessed efficiently in multiple threads is likely to be the key.
- Macro expansion. How to deal with the order problem of name resolution during macro expansion is a difficult problem.
- Lexing and/or parsing.

Achieving the above goals is of big significance to improving the performance of the Rust compiler.

The project could choose either one of these two areas, or try to tackle both of them together.

**Expected result**

Parallel frontend will not cause deadlock issues. We can ensure usability through [UI testing](https://github.com/rust-lang/rust/pull/132051).

The performance of the compiler will be improved, ideally at least by a couple of percentage points.

**Desirable skills**

Intermediate knowledge of Rust. A basic understanding of the implementation of the compiler process (such as typeck, hir_lowering, macro expansion) would be ideal.

**Project size**

Medium to hard (depending on the chosen scope).

**Difficulty**

Medium to hard.

**Mentor**
- Sparrow Li ([GitHub](https://github.com/SparrowLii), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/353056-Sparrow-Li))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Improving.20parallel.20frontend)
- [Parallel frontend working group](https://rust-lang.zulipchat.com/#narrow/channel/187679-t-compiler.2Fwg-parallel-rustc)
- [Parallel frontend project goal](https://rust-lang.github.io/rust-project-goals/2025h1/parallel-front-end.html)

### Prepare `stable_mir` crate for publishing

**Description**

We are advancing the Rust compiler's StableMIR API, which provides a robust foundation for code analysis tool development.
This API was specifically designed to shield developers from compiler internals, provide an intuitive interface, and to follow semantic versioning.

The project currently spans two key crates:
1. `stable_mir`: The public-facing API for tool developers
2. `rustc_smir`: The internal bridge between `stable_mir` and the Rust compiler.

As we prepare to [publish the `stable_mir` crate](https://rust-lang.github.io/rust-project-goals/2025h1/stable-mir.html), we are seeking contributions in these critical areas:

1. Refactor the dependency between `rustc_smir` and the `stable_mir` crates in the compiler to help us prepare for releasing `stable_mir` v0.1. More details of this refactoring can be found [here](https://hackmd.io/jBRkZLqAQL2EVgwIIeNMHg).
2. Implement a build time check on `stable-mir` crate to warn users that are using an unsupported version of the compiler.
3. Improve test coverage and automation including CI improvements to test with different compiler versions.
4. Create comprehensive developer documentation that covers maintenance procedures for both crates, ensuring future maintainers have clear guidelines for updates and compatibility management.
5. Continue the StableMIR integration with MiniRust to help us assess and improve StableMIR as described in [this issue](https://github.com/rust-lang/project-stable-mir/issues/66).

**Expected result**

We are able to publish an initial version of the `stable_mir` crate that works across multiple nightly versions, and that gracefully fails if the version is not supported.

**Desirable skills**

* Good debugging ability.
* Basic knowledge of Rust.
* Basic knowledge of Github CI.

**Project size**

Medium-Large depending on the chosen scope.

**Difficulty**

Medium.

**Mentor**
- Celina Val ([GitHub](https://github.com/celinval), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/442621-celinval))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Prepare.20.60stable_mir.60.20crate.20for.20publishing/with/506581543)
- [stable_mir](https://rust-lang.zulipchat.com/#narrow/channel/320896-project-stable-mir)

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

## Rust standard library

### Extend testing of `std::arch` intrinsics

**Description**

The [`std::arch`](https://doc.rust-lang.org/nightly/std/arch/index.html) module in the standard library provides architecture-specific intrinsic functions, which typically directly map to a single machine instruction.

These intrinsics are based on the architecture-specific intrinsics in C, which are usually based on a vendor specification and then implemented by C compilers such as Clang or GCC.

Rust supports thousands of intrinsics and we need to verify that they match the behavior of the equivalent intrinsics in C. A first step towards this has been the [`intrinsic-test`](https://github.com/rust-lang/stdarch/tree/master/crates/intrinsic-test) which fuzz tests the ARM (AArch32 and AArch64) intrinsics by generating C and Rust programs which call the intrinsics with random data and then verifying that the output is the same in both programs.

While this covers the ARM architectures, we have thousands of intrinsics for other architectures (notably x86) which are only lightly tested with manual tests. The goal of this project is to extend `intrinsic-test` to other architectures: x86, PowerPC, LoongArch, etc.

**Expected result**

By the end of this project `intrinsic-test` should be able to validate the behavior of intrinsics on multiple architectures. The primary goal is to support x86 since this is the most widely used architecture, but stretch goals could include support for other architectures such as PowerPC, LoongArch, WebAssembly, etc.

**Desirable skills**

Intermediate knowledge of Rust and C. Knowledge of intrinsics or assembly is useful but not required.

**Project size**

Small to Medium.

**Difficulty**

Medium.

**Mentors**
- Amanieu d'Antras ([GitHub](https://github.com/Amanieu), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/143274-Amanieu-d'Antras))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Extend.20testing.20of.20.60std.3A.3Aarch.60.20intrinsics)
- [t-libs/stdarch](https://rust-lang.zulipchat.com/#narrow/channel/208962-t-libs.2Fstdarch)

### Add safety contracts

**Description**

There is a Rust project goal to
[instrument the Rust standard library with safety contracts](https://rust-lang.github.io/rust-project-goals/2025h1/std-contracts.html).
With this approach we are moving from informal comments specifying safety
requirements on `unsafe` functions to executable Rust code.
To prioritize which functions to equip with contracts first, we run a
verification contest in the
[verify-rust-std](https://github.com/model-checking/verify-rust-std) fork.
In this contest,
[challenges](https://model-checking.github.io/verify-rust-std/challenges.html)
have been put up that request specific sets of functions to be equipped with
contracts.
We also welcome new challenges being proposed by anyone, or contracts being
contributed outside any of the existing challenges.

For example, we are currently looking for contributions towards the following challenges:
- [Verify the memory safety of core intrinsics using raw pointers](https://model-checking.github.io/verify-rust-std/challenges/0002-intrinsics-memory.html)
- [Memory safety of BTreeMap's `btree::node` module](https://model-checking.github.io/verify-rust-std/challenges/0004-btree-node.html)
- [Safety of Methods for Atomic Types & Atomic Intrinsics](https://model-checking.github.io/verify-rust-std/challenges/0007-atomic-types.html)
- [Contracts for SmallSort](https://model-checking.github.io/verify-rust-std/challenges/0008-smallsort.html)
- [Safety of `NonZero`](https://model-checking.github.io/verify-rust-std/challenges/0012-nonzero.html)

There is, however, no restriction to contribute to just those challenges: any of
the other open challenges are equally of interest, and so is creating new
challenges.

**Expected result**

A set of safety contracts and harnesses have been implemented in
[verify-rust-std](https://github.com/model-checking/verify-rust-std) for one of
the open challenges or any newly created challenge.
A stretch goal is to port upstream as many of those contracts as possible.

**Desirable skills**

* Basic knowledge of Rust.

**Project size**

Small to Large, depending on the number of challenges being addressed.

**Difficulty**

Medium.

**Mentor**
- Michael Tautschnig ([GitHub](https://github.com/tautschnig), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/887765-Michael-Tautschnig))

**Zulip streams**
- None

## Infrastructure

### Implement merge functionality in bors

**Description**

Various Rust repositories under the [rust-lang](https://github.com/rust-lang) organization use a merge queue bot (bors) for testing and merging pull requests. Currently, we use a legacy implementation called [homu](https://github.com/rust-lang/homu), which is quite buggy and very difficult to maintain, so we would like to get rid of it. We have started the implementation of a new bot called simply [bors](https://github.com/rust-lang/bors), which should eventually become the primary method for merging pull requests in the [rust-lang/rust](https://github.com/rust-lang/rust) repository.

The bors bot is a GitHub app that responds to user commands and performs various operations on a GitHub repository. Primarily, it creates merge commits and reports test workflow results for them. It can currently perform so-called "try builds", which can be started manually by users on a given PR to check if a subset of CI passed on the PR. However, the most important functionality, actually merging pull requests into the main branch, has not been implemented yet.

**Expected result**

bors can be used to perform pull request merges, including "rollups". In an ideal case, bors will be already usable on the `rust-lang/rust` repository.

**Desirable skills**

Intermediate knowledge of Rust. Familiarity with GitHub APIs is a bonus.

**Project size**

Medium.

**Difficulty**

Medium.

**Mentors**
- Jakub Beránek ([GitHub](https://github.com/kobzol), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/266526-Jakub-Ber%C3%A1nek))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/stream/421156-gsoc/topic/Idea.3A.20improve.20infrastructure.20automation.20tools)
- [Infra team](https://rust-lang.zulipchat.com/#narrow/stream/242791-t-infra)

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
- [Bootstrap team](https://rust-lang.zulipchat.com/#narrow/stream/326414-t-infra.2Fbootstrap)

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

## Rustup

### Make rustup concurrent

**Description**

[rustup](https://github.com/rust-lang/rustup) is an indispensable part of Rust's infrastructure, as it provides easy access to a Rust toolchain to millions of Rust users.

When installing a toolchain, it first downloads a set of components and then extracts them to disk. Currently, all downloads and disk I/O is performed serially, which makes rustup slower than it could be. Ideally, it should be able to overlap network downloads with disk I/O, and potentially also perform multiple network downloads at once.

Making rustup faster could have a high impact on the Rust ecosystem, particularly in CI environments, where rustup is typically used to download a Rust toolchain in every workflow execution. Since there are tens of thousands of repositories that use Rust in their CI, this can add up quickly.

There has been a prior [experiment](https://github.com/dtolnay/fast-rustup) that showed that concurrent rustup could in fact provide non-trivial performance improvements. [This issue](https://github.com/rust-lang/rustup/issues/731) contains discussion on the topic.

The rustup codebase now uses `async`, which should make implementing concurrent network and disk operations simpler.

The goal of the project is to add concurrency to rustup to enable overlap od network and disk I/O operations and perform benchmarks and experiments to evaluate what is the performance effect of such a change and when it is even worth it to perform it.

**Expected result**

Rustup will be able to overlap network and disk I/O and perform network requests concurrently.

**Desirable skills**

Intermediate knowledge of Rust. Familiarity with async programming or cross-platform filesystem knowledge is a bonus.

**Project size**

Medium.

**Difficulty**

Medium.

**Mentor**
- rami3l ([GitHub](https://github.com/rami3l), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/616990-rami3l))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Make.20rustup.20concurrent/with/506733333)

**Related Links**
- [Rustup discord channel](https://discord.com/channels/442252698964721669/463480252723888159)
- [fast-rustup experiment](https://github.com/dtolnay/fast-rustup)
- [Concurrent rustup GitHub issue](https://github.com/rust-lang/rustup/issues/731)

## Cargo

### Prototype an alternative architecture for `cargo fix`

**Description**

Some compiler errors know how to fix the problem and `cargo fix` is the command for applying those fixes.
Currently, `cargo fix` calls into the APIs that implement `cargo check` with
`cargo` in a way that allows getting the json messages from rustc and apply
them to workspace members.
To avoid problems with conflicting or redundant fixes, `cargo fix` runs `rustc` for workspace members in serial.
As one fix might lead to another, `cargo fix` runs `rustc` for each workspace member in a loop until a fixed point is reached.
This can be very slow for large workspaces.

We want to explore an alternative architecture where `cargo fix` runs the
`cargo check` command in a loop,
processing the json messages,
until a fixed point is reached.

Benefits
- Always runs in parallel
- May make it easier to extend the behavior, like with an interactive mode

Downsides
- Might have issues with files owned by multiple packages or even multiple build targets

This can leverage existing CLI and crate APIs of Cargo and can be developed as a third-party command.

See [cargo#13214](https://github.com/rust-lang/cargo/issues/13214) for more details.

**Expected result**

- A third-party command as described above
- A comparison of performance across representative crates
- An analysis of corner the behavior with the described corner cases

**Desirable skills**

Intermediate knowledge of Rust.

**Project size**

Medium

**Difficulty**

Medium.

**Mentor**
- Ed Page ([GitHub](https://github.com/epage), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/424212-Ed-Page))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Prototype.20an.20alternative.20architecture.20for.20.60cargo.20fix.60)
- [Cargo team](https://rust-lang.zulipchat.com/#narrow/stream/246057-t-cargo)

### Prototype Cargo plumbing commands

**Description**

Cargo is a high-level, opinionated command.
Instead of trying to directly support every use case,
we want to explore exposing the building blocks of the high-level commands as
"plumbing" commands that people can use programmatically to compose together to
create custom Cargo behavior.

This can be prototyped outside of the Cargo code base, using the Cargo API.

See the [Project Goal](https://rust-lang.github.io/rust-project-goals/2025h1/cargo-plumbing.html) for more details.

**Expected result**

Ideal: a performant `cargo porcelain check` command that calls out to
individual `cargo plumbing <name>` commands to implement its functionality.

Depending on the size the participant takes on and their experience,
this may be out of reach.
The priorities are:
1. A shell of `cargo porcelain check`
2. Individual commands until `cargo porcelain check` is functional
3. Performance

**Desirable skills**

Intermediate knowledge of Rust.

**Project size**

Scaleable

**Difficulty**

Medium.

**Mentor**
- Ed Page ([GitHub](https://github.com/epage), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/424212-Ed-Page))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Prototype.20Cargo.20plumbing.20commands)
- [Cargo team](https://rust-lang.zulipchat.com/#narrow/stream/246057-t-cargo)

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

### Build script delegation

**Description**

When developers need to extend how Cargo builds their package,
they can write a [build script](https://doc.rust-lang.org/cargo/reference/build-scripts.html).
This gives users quite a bit of flexibility but
- Allows running arbitrary code on the users system, requiring extra auditing
- Needs to be compiled and run before the relevant package can be built
- They are all-or-nothing, requiring users to do extra checks to avoid running expensive logic
- They run counter to the principles of third-party build tools that try to mimic Cargo

A developer could make their build script a thin wrapper around a library
(e.g. [shadow-rs](https://crates.io/crates/shadow-rs))
but a build script still exists to be audited (even if its small) and each individual wrapper build script must be compiled and linked.
This is still opaque to third-party build tools.

Leveraging an unstable feature,
[artifact dependencies](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#artifact-dependencies),
we could allow a developer to say that one or more dependencies should be run as build scripts, passing parameters to them.

This project would add unstable support for build script delegation that can
then be evaluated for proposing as an RFC for approval.

See [the proposal](https://github.com/rust-lang/cargo/issues/14903#issuecomment-2523803041) for more details.

**Expected result**

Milestones
1. An unstable feature for multiple build scripts
2. An unstable feature for passing parameters to build scripts from `Cargo.toml`, built on the above
3. An unstable feature for build script delegation, built on the above two

Bonus: preparation work to stabilize a subset of artifact dependencies.

**Desirable skills**

Intermediate knowledge of Rust, especially experience with writing build scripts.

**Project size**

Large.

**Difficulty**

Medium.

**Mentor**
- Ed Page ([GitHub](https://github.com/epage), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/424212-Ed-Page))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Build.20script.20delegation)

## rust-analyzer

### Implement a new proc-macro server RPC API

**Description**

Today, rust-analyzer (and RustRover) expands proc-macros by spawning a separate proc-macro server
process that loads and executes the proc-macro dynamic libraries. They communicate to this process
via a JSON RPC interface that has not been given much thought when it was implemented, now starting
to show its limitations.

The goal is to replace this current implementation entirely in favor of a more performant format
that also supports the more complicated needs of the proc-macro API, outlined in
https://github.com/rust-lang/rust-analyzer/issues/19205.

**Expected result**

There exists a new proc-macro server that is more efficient and allows for implementing the
remaining proc-macro API. Ideally, it should be integrated within rust-analyzer.

**Desirable skills**

Intermediate knowledge of Rust.

**Project size**

Medium.

**Difficulty**

Medium.

**Mentor**
- Lukas Wirth ([GitHub](https://github.com/veykril), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/300586-Lukas-Wirth))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/185405-t-compiler.2Frust-analyzer/topic/proc-macro.20server.20IPC.20format)
- [rust-analyzer team](https://rust-lang.zulipchat.com/#narrow/channel/185405-t-compiler.2Frust-analyzer)

## Crate ecosystem

### Modernize the libc crate

**Description**

The [libc](https://github.com/rust-lang/libc) crate is one of the oldest crates of the Rust ecosystem, long predating
Rust 1.0. Additionally, it is one of the most widely used crates in the ecosystem (#4 most downloaded on crates.io).
This combinations means that the current version of the libc crate (`v0.2`) is very conservative with breaking changes
has accumulated a list of things to do in a 1.0 release. Additionally, some of the infrastructure for `lib` is rather
outdated.

Most of the changes required for 1.0 are under the [1.0 milestone](https://github.com/rust-lang/libc/milestone/1). Some
of these come from the evolution of the underlying platforms, some come from a desire to use newer language features,
while others are simple mistakes that we cannot correct without breaking existing code.

The crate used for testing `libc` (`ctest`) uses an old syntax parser that cannot support modern Rust, so some of the
changes will require rewriting `ctest` to use a newer parser (e.g. `syn`). This upgrade is tracked at
https://github.com/rust-lang/libc/issues/4289.

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

### Make `cargo-semver-checks` run faster

**Description**

As more lints get added to [`cargo-semver-checks`](https://github.com/obi1kenobi/cargo-semver-checks), its runtime grows longer.
As a result, users' iteration loops and CI pipelines take longer as well, degrading the overall experience of using the tool.

Figure out ways to speed up `cargo-semver-checks`, and find good ways to deploy them without degrading the maintainability of the codebase!

**Expected result**

The wall-clock runtime of running `cargo-semver-checks` on a large Rust crate gets cut by 50-80%, while still running the same lints as before.

**Desirable skills**

Interest in and at least a bit of experience with performance engineering. Understanding of how to apply techniques like:
- profiling and benchmarking
- parallel programming (e.g. with `rayon`)
- building and applying indexes (in the database sense)

Strong attention to detail. Willingness to learn quickly and perform lots of experiments, even though many of them may prove to be dead ends.
Discipline and thoughtfulness when writing and testing code, to ensure that code changes are not merely *fast* but also *maintainable*.

**Project size**

Ideally large, to have the biggest possible positive performance impact.

**Difficulty**

Medium to high. See the "desirable skills" section above.

**Mentor**
- Predrag Gruevski ([GitHub](https://github.com/obi1kenobi/), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/474284-Predrag-Gruevski-(he-him)))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Make.20.60cargo-semver-checks.60.20run.20faster)

**Related Links**
- [Playground where you can try querying Rust data](https://play.predr.ag/rustdoc)
- [Past optimization work: Speeding up Rust semver-checking by over 2000x](https://predr.ag/blog/speeding-up-rust-semver-checking-by-over-2000x/)
- [Conference talk: How Database Tricks Sped up Rust Linting Over 2000x](https://www.youtube.com/watch?v=Fqo8r4bInsk)
- [Query engine adapter, where many of the optimizations may be deployed](https://github.com/obi1kenobi/trustfall-rustdoc-adapter)

### Enable witness generation in `cargo-semver-checks`

**Description**

When `cargo-semver-checks` reports a breaking change, it in principle has seen enough information for the breakage to be reproduced with an example program: a *witness* program.
Witness programs are valuable as they confirm that the suspected breakage did indeed happen, and is not a false-positive.

**Expected result**

Automatic witness generation is something we've explored, but we've only scratched the surface at implementing it so far.
The goal of this project would be to take it the rest of the way: enable `cargo-semver-checks` to (with the user's opt-in) generate witness programs for each lint, verify that they indeed demonstrate the detected breakage, and inform the user appropriately of the breakage and the manner in which it was confirmed.
If a witness program *fails* to reproduce breakage flagged by one of our lints, we've found a bug — the tool should then prepare a diagnostic info packet and offer to help the user open an auto-populated GitHub issue.

**Stretch goal:** having implemented witness generation, run another study of SemVer compliance in the Rust ecosystem, similar to [the study we completed in 2023](https://predr.ag/blog/semver-violations-are-common-better-tooling-is-the-answer/). The new study would cover many more kinds of breaking changes, since `cargo-semver-checks` today has 2.5x times more lints than it did back then. It would also reveal any new false-positive issues, crashes, or other regressions that may have snuck into the tool in the intervening years.

**Desirable skills**

Intermediate knowledge of Rust. Interest in building dev tools, and empathy for user needs so we can design the best possible user experience.
Familiarity with databases, query engines, or programming language design is welcome but not required.

**Project size**

Large

**Difficulty**

Medium

**Mentor**
- Predrag Gruevski ([GitHub](https://github.com/obi1kenobi/), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/474284-Predrag-Gruevski-(he-him)))

**Zulip streams**

- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Enable.20witness.20generation.20in.20.60cargo-semver-checks.60)

**Related Links**
- [Playground where you can try querying Rust data](https://play.predr.ag/rustdoc)
- [Use of witness programs to verify breaking change lints](https://predr.ag/blog/semver-violations-are-common-better-tooling-is-the-answer/#automated-validation-via-witnesses)

### Wild linker with test suites from other linkers

**Description**

The Wild linker is a project to build a very fast linker in Rust that has incremental linking and
hot reload capabilities.

It currently works well enough to link itself, the Rust compiler, clang (provided you use the right
compiler flags) and a few other things. However, there are various features and combinations of
flags that don’t yet work correctly. Furthermore, we have a pretty incomplete picture of what we
don’t support.

The proposed project is to run the test suite of other linkers with Wild as the linker being tested,
then for each failure, determine what the problem is. It’s expected that many failures will have the
same root cause.

**Expected result**

Write a program, ideally in Rust, that runs the test suite of some other linker. Mold’s test suite
is pretty easy to run with Wild, so that’s probably a good default choice. The Rust program should
emit a CSV file with one row per test, whether the test passes or fails and if it fails, an attempt
to identify the cause based on errors / warnings emitted by Wild.

For tests where Wild doesn’t currently emit any error or warning that is related to the cause of the
test failure, attempt to make it do so. Some of the tests might fail for reasons that are hard to
identify. It’s OK to just leave these as uncategorised. Where tests fail due to bugs or differences
in behaviour of Wild, automatic classification likely isn’t practical. A one-off classification of
these would be beneficial.

If time permits, pick something achievable that seems like an important feature / bug to support /
fix and implement / fix it.

**Desirable skills**

Knowledge of Rust. Any existing knowledge of low-level details like assembly or the ELF binary
format is useful, but can potentially be learned as we go.

**Project size**

Small to large depending on chosen scope.

**Difficulty**

Some of the work is medium. Diagnosing and / or fixing failures is often pretty hard.

**Mentor**

- David Lattimore ([GitHub](https://github.com/davidlattimore), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/198560-David-Lattimore))

**Zulip streams**

- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Wild.20linker.20with.20test.20suites.20from.20other.20linkers)

**Further resources**

- [Wild linker](https://github.com/davidlattimore/wild)
- [Blog posts, most of which are about Wild](https://davidlattimore.github.io/)
