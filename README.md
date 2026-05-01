# Rust project ideas
This page contains a list of ideas for various projects that could help improve
the Rust Project and potentially also the wider Rust community.

These project ideas can be used as inspiration for various OSS contribution programs,
such as [Google Summer of Code](https://summerofcode.withgoogle.com/) or [OSPP](https://summer-ospp.ac.cn/).

In the list below, you can find projects from past GSoC runs:

- Google Summer of Code projects
  - [2026](gsoc/runs/2026.md)
  - [2025](gsoc/runs/2025.md)
  - [2024](gsoc/runs/2024.md)

We invite contributors that would like to participate in projects such as GSoC or that would just want to find a Rust project that they would like to work on to examine the project list and use it as an inspiration. Another source of inspiration can be the [Rust Project Goals](https://rust-lang.github.io/rust-project-goals/index.html), particularly the orphaned goals. However, you can also work on these projects outside GSoC or other similar projects! We welcome all contributions.

If you would like to participate in GSoC, please read [this](gsoc/README.md), **in particular the guidance around AI usage!**
If you would like to discuss project ideas or anything related to them, you can do so on our [Zulip](https://rust-lang.zulipchat.com/#narrow/channel/421156-gsoc).

We use the GSoC project size parameters for estimating the expected time complexity of the project ideas. The individual project sizes have the following expected amounts of hours:
- Small: 90 hours
- Medium: 175 hours
- Large: 350 hours

## Index
- **Rust Compiler**
    - [TPDE codegen backend for `rustc`](#tpde-codegen-backend-for-rustc)
    - [Improve Rust User Experience on Windows](#improve-rust-user-experience-on-windows)
- **Crate ecosystem**
    - [Modernize the libc crate](#Modernize-the-libc-crate)
    - [Make `cargo-semver-checks` support type-checking lints](#make-cargo-semver-checks-support-type-checking-lints)

# Project ideas
The list of ideas is divided into several categories.

## Rust Compiler

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
