# Rust project ideas
This page contains a list of ideas for various projects that could help improve
the Rust Project and potentially also the wider Rust community.

These project ideas can be used as inspiration for various OSS contribution programs,
such as [Google Summer of Code](https://summerofcode.withgoogle.com/) or [OSPP](https://summer-ospp.ac.cn/).

In the list below, you can find projects from past GSoC runs:

- Google Summer of Code projects
  - [2025](gsoc/runs/2025.md)
  - [2024](gsoc/runs/2024.md)

**This README contains ideas that are actual for Google Summer of Code 2026.** 

We invite contributors that would like to participate in projects such as GSoC or that would just want to find a Rust project that they would like to work on to examine the project list and use it as an inspiration. Another source of inspiration can be the [Rust Project Goals](https://rust-lang.github.io/rust-project-goals/index.html), particularly the orphaned goals. However, you can also work on these projects outside GSoC or other similar projects! We welcome all contributions.

If you would like to participate in GSoC, please read [this](gsoc/README.md), **in particular the guidance around AI usage!**
If you would like to discuss project ideas or anything related to them, you can do so on our [Zulip](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc).

We use the GSoC project size parameters for estimating the expected time complexity of the project ideas. The individual project sizes have the following expected amounts of hours:
- Small: 90 hours
- Medium: 175 hours
- Large: 350 hours

## Index
- **Rust Compiler**
    - [Implement `impl` and `mut` restrictions](#implementing-impl-and-mut-restrictions)
    - [Improve Rust compiler debuginfo testsuite](#improve-rust-compiler-debuginfo-test-suite)
    - [TPDE codegen backend for `rustc`](#tpde-codegen-backend-for-rustc)
    - [Reproducible builds](#reproducible-builds)
    - [Refactoring of rustc_codegen_ssa to make it more convenient for the GCC codegen](#Refactoring-of-rustc_codegen_ssa-to-make-it-more-convenient-for-the-GCC-codegen)
    - [Reorganisation of `tests/ui/issues`](#reorganisation-of-testsuiissues)
    - [Improve Rust User Experience on Windows](#improve-rust-user-experience-on-windows)
- **Infrastructure**
    - [Port `std::arch` test suite to `rust-lang/rust`](#port-stdarch-test-suite-to-rust-langrust)
- **Cargo**
    - [Improved progress reporting from Cargo](#improved-progress-reporting-from-cargo)
    - [Move cargo shell completions to Rust](#move-cargo-shell-completions-to-Rust)
    - [Cargo: Build script delegation](#cargo-build-script-delegation)
- **Rustup**
    - [XDG path support for rustup](#XDG-path-support-for-rustup)
- **Crate ecosystem**
    - [Modernize the libc crate](#Modernize-the-libc-crate)
    - [Make `cargo-semver-checks` support type-checking lints](#make-cargo-semver-checks-support-type-checking-lints)
    - [Link Linux kernel modules with Wild](#link-linux-kernel-modules-with-wild)
- **Rust Analyzer**
    - [Migrating rust-analyzer assists to `SyntaxEditor`](#migrating-rust-analyzer-assists-to-syntaxeditor)

# Project ideas
The list of ideas is divided into several categories.

## Rust Compiler

### Improve Rust compiler debuginfo test suite

**Description**

The Rust compiler debuginfo test suite should test how Rust programs interact with debuggers, such as GDB, LLDB and CDB. However, it is currently not fully exercised on CI, because it suffers from several issues:

- It is not easily possible to bless the expected output, which makes it quite difficult to maintain the test suite.
- It uses whatever version of a debugger is discovered (through inconsistent and varying means) on the system where the tests run.
- It does not allow specifying different expected outputs per different debugger versions.
- It is difficult (in part) to comprehend test failure, in part because debugger output is captured then fed to LLVM FileCheck, and the FileCheck failures in turn are hard to figure out what's wrong.
- There is a significant lack of docs surrounding the design intention and actual usage of the debuginfo test infra.

We would like to rewrite the test suite to make it more maintainable and thus increase our confidence in the Rust compiler debugger visualizers, and maintain the quality of debuginfo emitted (and detect if there are regressions).

**Expected result**

The Rust compiler debuginfo test suite is running fully on CI and is easier to maintain and bless.

A stretch goal is to also use the new debuginfo test suite to improve Rust debugger visualizers.

**Desirable skills**

Intermediate knowledge of Rust. Knowledge of debuggers and their APIs is a big plus.

**Project size**

Medium to large.

**Difficulty**

Hard.

**Mentors**
- Jakub Beránek ([GitHub](https://github.com/kobzol), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/266526-Jakub-Ber%C3%A1nek))
- Jieyou Xu ([GitHub](https://github.com/jieyouxu), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/259697-Jieyou-Xu))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Improve.20Rust.20compiler.20debuginfo.20test.20suite/with/567914216)

**Related links**
- [New debuginfo test suite MCP](https://github.com/rust-lang/compiler-team/issues/936)

### TPDE codegen backend for `rustc`

[TPDE](https://docs.tpde.org/index.html) is a compiler framework that can act as a LLVM backend with very high build performance. Since slow build times are a constant issue for Rust developers, we would like to experiment with a TPDE-based backend for `rustc`, to see how much faster could compilation times get.

There are essentially two approaches that could be chosen here. Either use the [TPDE-LLVM](https://docs.tpde.org/tpde-llvm-main.html) LLVM backend to generate assembly from LLVM IR emitted by `rustc`, or create a completely separate `rustc` backend that will work on TPDE IR (intermediate representation) directly and avoid going through LLVM.

The TPDE-LLVM-based approach is preferred since it should achieve most of the performance benefits, allows reusing LLVM plugins and infrastructure where desired, and is more likely to succeed. However, we will consider both approaches if the applicant can make good arguments in favor of a completely separate TPDE backend.

Note that this would be experimental work that would most likely have to live out-of-tree, at least at the beginning of the project.

**Expected result**

We have a new `rustc` experimental backend that can be used to compile non-trivial Rust programs (it does not have to be complete though, e.g. inline assembly support will probably not make the cut), and we can evaluate its performance e.g. on the Rust Compiler Benchmark Suite.

**Desirable skills**

Knowledge of Rust, basic familiarity with compiler functionality or LLVM is a bonus.

**Project size**

Large.

**Difficulty**

Medium to hard.

**Mentor**
- Manuel Drehwald ([GitHub](https://github.com/ZuseZ4), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/348574-Manuel-Drehwald))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20TPDE.20codegen.20backend.20for.20rustc/with/571387216)
- [Compiler team](https://rust-lang.zulipchat.com/#narrow/stream/131828-t-compiler)
- [Previous discussion about this topic](https://rust-lang.zulipchat.com/#narrow/channel/131828-t-compiler/topic/TPDE.3A.20A.20Fast.20Adaptable.20Compiler.20Back-End.20Framework/with/570348767)

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

### Reorganisation of `tests/ui/issues`

**Description** 

The `tests/ui/issues` directory of the Rust compiler test suite currently contains a large number of miscellaneous tests — approximately 615 in total. These are primarily regression tests that were added after specific issues were fixed. Over time, this directory has become a catch-all, making the test suite harder to navigate and maintain.

Our goal is to keep the UI tests well organised, with each test placed in an appropriate subdirectory based on what it is actually testing. Consolidating such a large number of unrelated tests in a single directory works against this goal.

This project focuses on systematically reviewing these tests and relocating them to more suitable locations within `tests/ui`.

Here is an approximate plan to tackle this:

1. Inspect each test in `tests/ui/issues`.
2. Identify the issue it relates to (the issue number is typically part of the file name).
3. Determine a more appropriate subdirectory within `tests/ui`, based on the behaviour or feature being tested.
4. Add explanatory comments where the purpose of the test is not immediately obvious.
5. Rename the test file to better reflect what it is testing.
6. Add a link to the original issue at the top of the test file.
7. Reformat the test where appropriate, taking care with tests that intentionally rely on unusual formatting.
8. Re-bless tests where necessary (for example, if a test was previously marked as erroneous), and remove any obsolete `.stderr` files from the original location.

**Expected result**

Complete removal of the `tests/ui/issues/` directory, with all tests relocated to appropriate subdirectories.

**Desirable skills**

Familiarity with Rust and compiler tests. Ability to read and understand regression tests. Attention to detail and comfort working with large codebases.

**Project size**

Small to large. (The size is scalable, depending on how many tests would be ported.)

**Difficulty** 

Medium.

**Mentors**

- Kivooeo ([GitHub](https://github.com/Kivooeo/), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/675515-Kivooeo))
- Teapot ([GitHub](https://github.com/Teapot4195), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/583581-Teapot))

**Zulip streams**

- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20reorganisation.20of.20tests.2Fui.2Fissues/with/568198062)

**Related links**

* [Prior project](gsoc/runs/2025.md/#mapping-the-maze-of-rusts-ui-test-suite-with-established-continuous-integration-practices)

### Improve Rust User Experience on Windows

**Description**

The Rust compiler and its related infrastructure currently include a number of hiccups and roadblocks for Windows users specifically. This can make it more difficult for new contributors using Windows or one of the Unix-to-NT API translation layers (e.g. Cygwin, MSYS2, etc.), to get started with developing the compiler or even using Rust.

It is easy to stumble into rather weird bugs that are both difficult to debug and fix when compiling and working with Rust on Windows. For example, path normalization being done incorrectly for the host OS is a longtime pain point for Unix translation layers (e.g. MSYS2). Additionally, the "put libs wherever you want" strategy Windows has taken with system libraries makes it difficult to configure the build process correctly, especially where linking to external C libraries.

The standard library also has to work around some pecularities of the Windows API. For example, timing on Windows is based on 100ns increments since Jan 1st 1601, whereas most Unix platforms use milliseconds since Jan 1st 1970. In library code, this difference in API behavior is often not well documented and results in many developer surprises. For example, [Checked arithmetic for adding a `Duration` smaller than 100ns results in a noop](https://github.com/rust-lang/rust/issues/149995).

You can find a number of open issues related to Windows in the Rust issue tracker, by filtering for one of the many Windows target categories, for example [O-windows](https://github.com/rust-lang/rust/issues?q=is%3Aissue%20state%3Aopen%20label%3AO-windows).

**Expected result**

An overall improvement to the number of issues and hiccups/roadblocks a compiler developer or Rust user is expected to face when using Rust on Windows-based platforms.

**Desirable skills**

Familiarity with Rust, comfort working with large codebases and, depending on project scope, some of the following (non-exhaustive):
* Familiarity with Windows NT API
* Experience developing on Windows or a translation layer
* A decent amount of experience within your field(s)r of choice

**Project size**

Small to large. (Size is scalable, depending on the scope of the project.)

**Difficulty**

Medium to Hard, depending on the issues to be fixed.

**Mentor**

* Teapot ([GitHub](https://github.com/Teapot4195), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/583581-Teapot))
  * Teapot is happy to mentor projects fixing most compiler and ecosystem components, or any combination of them as the contributor details in their proposal.
  * If you would like to do this project, please reach out so Teapot can tell you if he can mentor the field you would like to work on!

**Zulip streams**

- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Improve.20Rust.20User.20Experience.20on.20Windows/with/574055740)

### Implementing `impl` and `mut` restrictions

**Description** 

Rust doesn't currently have a way to restrict the implementability of a trait, nor does Rust have a way to restrict the
mutability of a field.

The accepted [RFC3323 - Restrictions](https://rust-lang.github.io/rfcs/3323-restrictions.html) aims to improve our story
around those two points by bringing:
 - `impl(..)` restrictions: `pub impl(crate) trait Foo {}`
 - `mut(..)` restrictions: `pub struct Foo { pub mut(crate) foo: u8 }`

*Previous attempts at implementing the RFC have stalled.*

The goal of this project is to implement both impl and mut restrictions in the Rust compiler, fix any resulting bugs that
may be discovered in the course of the project, and add extensive tests for the feature.

**Expected result**

A working implementation of `impl` and `mut` restrictions in the nightly compiler.

**Desirable skills**

Familiarity with Rust. Attention to detail and comfort working with large codebases.

**Project size**

Small to medium.

**Difficulty** 

Medium.

**Mentors**

- Jacob Pratt ([GitHub](https://github.com/jhpratt), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/245610-Jacob-Pratt))
- Urgau ([GitHub](https://github.com/Urgau), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/327095-Urgau))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Implementing.20impl.20and.20mut.20restrictions/with/572758131)

**Related links**

- [Tracking Issue for Restrictions](https://github.com/rust-lang/rust/issues/105077)
- [Restrictions RFC](https://rust-lang.github.io/rfcs/3323-restrictions.html)
- [First attempt](https://github.com/rust-lang/rust/pull/106074)
- [Second attempt](https://github.com/rust-lang/rust/pull/141754)

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

**Mentor**
- Jakub Beránek ([GitHub](https://github.com/kobzol), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/266526-Jakub-Ber%C3%A1nek))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Port.20.60std.3A.3Aarch.60.20test.20suite.20to.20.60rust-lang.2Frust.60)
- [t-libs/stdarch](https://rust-lang.zulipchat.com/#narrow/channel/208962-t-libs.2Fstdarch)

## Cargo

### Improved progress reporting from Cargo

**Description**

Cargo's progress reporting is designed for fairly broad terminal support,
only allowing one line of progress output.
Small steps have been done to take advantage of more terminal features,
like unicode support and hyperlinks,
by providing configuration for these with a terminal allow list.
Something similar can be done to allow for experimenting with richer progress
reporting from Cargo like what [buck2 has](https://crates.io/crates/superconsole).

One proposed idea is for Cargo to track operational spans (e.g. `Updating`, `Compiling`)
and any non-sticky message within one of those spans is cleared upon span close.
Examples of non-sticky messages include warnings, errors, and a summary line for the command (e.g. `Finished`).
This would help make Cargo less noisy which would be particularly helpful for
[cargo script](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#script).

Cargo's internals are tied to the idea of one progress line and will need to be
updated to allow for richer progress reporting.

See also
- [cargo#8889](https://github.com/rust-lang/cargo/issues/8889)
- [cargo#16388](https://github.com/rust-lang/cargo/issues/16388)

**Expected result**

1. Progress style within Cargo is abstracted away
2. Sticky/non-sticky user notifications
3. New compilation progress style with configuration
4. Initial allow list for terminals to use new style

**Desirable skills**

Intermediate knowledge of Rust.

**Project size**

Medium.

**Difficulty**

Medium.

**Mentor**
- Ed Page ([GitHub](https://github.com/epage), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/424212-Ed-Page))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Improved.20progress.20reporting.20from.20Cargo/with/566401899)

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

### Cargo: Build script delegation

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

> Note: there was a project with a similar topic in [GSoC 2025](https://blog.rust-lang.org/2025/11/18/gsoc-2025-results/#cargo-build-script-delegation). But since there is a lot of work to be done, we have published this project idea again. The current idea description reflects the current state.

**Expected result**

Milestones
1. An unstable feature for passing parameters to build scripts from `Cargo.toml`
2. An unstable feature for build script delegation, passing parameters to artifact dependencies

Bonus: preparation work to stabilize a subset of artifact dependencies.

**Project size**

Large.

**Mentor**
- Ed Page ([GitHub](https://github.com/epage), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/424212-Ed-Page))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Project.3A.20Cargo.3A.20Build.20script.20delegation/with/542983512)

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

> Note: there was a project with a similar topic in [GSoC 2025](https://blog.rust-lang.org/2025/11/18/gsoc-2025-results/#modernising-the-libc-crate). But since there is a lot of work to be done, we have published this project idea again. The current idea description reflects the current state.

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

### Make `cargo-semver-checks` support type-checking lints

**Description**

[`cargo-semver-checks`](https://github.com/obi1kenobi/cargo-semver-checks) is a linter for semantic versioning. It ensures
that Rust crates adhere to semantic versioning by looking for breaking changes in APIs. It's used by many of Rust's
most popular libraries — and even within `cargo` itself.

`cargo-semver-checks` can currently catch ~245 different kinds of breaking changes, meaning there are hundreds of kinds of breaking changes it
still cannot catch! Its largest capability gap is the inability to perform type-checking in lints, which is necessary
to detect the breakage between `pub fn example(x: i64) {}` and `pub fn example(x: String) {}`, for example.

The goal of this project idea is to design and implement the systems required to support the first batch of type-checking lints.
This specifically lays the ground work for shipping such lints *by the hundreds* — we're not looking to handle just a few special cases.
[`cargo-semver-checks` has been adding hundreds of new lints per year](https://predr.ag/blog/cargo-semver-checks-2025-year-in-review/),
and this will be the project that makes that possible for 2026 and beyond!

This would be a challenging "high risk, high reward" type of project: perfect for candidates looking to put forward
a significant amount of effort, determination, and skill toward a difficult problem with serious real world impact,
of course with support and guidance from a mentor. With luck and (quite a lot of) hard work, the culmination of
the project could even be _shipping_ the first set of type-checking lints in a new `cargo-semver-checks` release.

**Expected result**

`cargo-semver-checks` will be able to catch the breakage in cases like:
```diff
- pub fn example(x: i64) {}
+ pub fn example(x: String) {}
```

It will do so by using its declarative query language to notice the API change and capture information regarding it,
then plugging that information into a templating system able to generate a "witness" crate for the API change.
`cargo-semver-checks` would then automatically run `cargo check` on the witness crate, which will either pass 
without errors (indicating no breakage), or error out indicating a breaking change.

A possible witness for the above example is:
```
pub fn witness(x: i64) {
    crate_being_checked::example(x);
}
```
which will obviously only compile if the `example()` function takes an `i64`, not a `String`.

While this approach may seem overly complex at first, consider the following change:
```diff
- pub fn example(x: i64) {}
+ pub fn example(x: impl Into<i64>) {}
```
This is a case where the type of `x` changed, but passing `i64` still works fine — so this isn't a SemVer-major change.
Therefore, merely noticing that a type has changed is *not* sufficient to detect breakage, and we must use witness programs instead.
(It is highly impractical to use `rustc` as a library. It's similarly infeasible to reimplement the type-checker and trait solver ourselves.)

**Desirable skills**

Intermediate knowledge of Rust, or better. Familiarity with databases, query engines, code generation, or query language design is welcome but
not required. Willingness to dive into a complex problem space and find your way around (with guidance, of course) is a must.

Contributors interested in this project idea are strongly encouraged to first familiarize themselves with `cargo-semver-checks`
and its linting system, which expresses lints as queries over a database-like schema ([playground](https://play.predr.ag/rustdoc)).
The project will require writing lints, extending the schema, writing code-generation code to create witness crates,
considering ways to improve performance in order to ensure a positive user experience, and designing the entire lint-writing process
such that type-checking lints are not challenging nor bespoke, but as normal and easy to write as any other lint.

**Project size**

Large

**Difficulty**

High

**Mentor**
- Predrag Gruevski ([GitHub](https://github.com/obi1kenobi/), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/474284-Predrag-Gruevski-(he-him)))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Make.20cargo-semver-checks.20support.20type-checking.20lints/with/570662489)

**Related Links**
- [Playground where you can try querying Rust data](https://play.predr.ag/rustdoc)
- [GitHub issues describing not-yet-implemented lints](https://github.com/obi1kenobi/cargo-semver-checks/issues?q=is%3Aissue+is%3Aopen+label%3AE-mentor+label%3AA-lint+)
- [Opportunities to add new schema, enabling new lints](https://github.com/obi1kenobi/cargo-semver-checks/issues/241)
- [Query engine adapter](https://github.com/obi1kenobi/trustfall-rustdoc-adapter)
- [Study of SemVer breakage in Rust, including more details on "witness" programs](https://predr.ag/blog/semver-violations-are-common-better-tooling-is-the-answer/)
- [cargo-semver-checks 2025 year in review, where the "path forward" offers more info about this project idea](https://predr.ag/blog/cargo-semver-checks-2025-year-in-review/)
- [Last year's GSoC project, which built the foundation for type-checking lints that we'd build upon](https://glitchlesscode.ca/posts/2025-11-05a/)

### Link Linux kernel modules with Wild

**Description**

The [Wild linker](https://github.com/davidlattimore/wild) is a very fast linker written in Rust.

We'd like for it to be possible to use the Wild linker for as large a range of Rust development as
possible. Besides porting to other platforms, which is probably too large a scope for a GSoC
project, one gap we currently have on Linux is compiling kernel modules. Linux kernel modules can
now be written in Rust, but the Wild linker, despite having some linker script support, doesn't
support enough linker script features to be able to link a kernel module.

**Expected result**

Implement more linker-script features. Ideally enough that we can support linking of Linux kernel
modules, but even if we can't get that far, getting closer would be awesome. Linker scripts are also
used extensively for embedded development, which may be something we could support with Wild in the
future.

**Desirable skills**

Intermediate knowledge of Rust and a willingness to learn more. You don't need to have existing
experience with implementing linkers, but it'd be good if upon reading the docs for GNU linker
scripts, they at least mostly make sense.

**Project size**

Medium or large depending on which linker script features are implemented.

**Difficulty**

Different linker script features are likely to range between easy and hard.

**Mentor**
- David Lattimore ([GitHub](https://github.com/davidlattimore), [Zulip](https://rust-lang.zulipchat.com/#narrow/dm/198560-David-Lattimore))

**Zulip streams**
- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Link.20Linux.20kernel.20modules.20with.20Wild/with/570521180)

**Related links**

- [Wild linker](https://github.com/davidlattimore/wild/)
- [Contributing docs](https://github.com/davidlattimore/wild/blob/main/CONTRIBUTING.md)
- [GNU linker script docs](https://sourceware.org/binutils/docs/ld/Scripts.html)

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

**Zulip streams**

- [Idea discussion](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc/topic/Idea.3A.20Migrating.20rust-analyzer.20assists.20to.20.60SyntaxEditor.60/with/566388740)

**Related Links**

- [An issue explaining why we should get rid of mutable syntax trees architecture-wise](https://github.com/rust-lang/rust-analyzer/issues/15710)
- [Tracking issue for this effort](https://github.com/rust-lang/rust-analyzer/issues/18285)
- [A prototype exploring how `rowan` without mutable trees could look like](https://github.com/ChayimFriedman2/rowan/tree/next-rowan)
