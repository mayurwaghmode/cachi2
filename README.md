# Cachi2

[![coverage][cachi2-coveralls-badge]][cachi2-coveralls]

Cachi2 is a CLI tool that pre-fetches your project's dependencies to aid in making your build process
[hermetic](https://slsa.dev/spec/v0.1/requirements#hermetic).

The primary intended use of Cachi2's outputs is for network-isolated container builds (see [usage](docs/usage.md)).

## Supported package managers (so far)

* [Go modules](https://go.dev/ref/mod)

## Goals

Please note that Cachi2 is rather picky, aiming to:

* encourage or enforce best practices
* enforce building from source - no pre-built artifacts, such as Python [wheels][wheel-spec]
* never execute arbitrary code - looking at you [setup.py (discouraged)][setuppy-discouraged]
* keep the implementation simple

To play nicely with Cachi2, the build process for your project must be

* **Defined** - Cachi2 only fetches dependencies that are explicitly declared - typically in a lockfile generated by
  your package manager.
* **Reproducible** - Cachi2 will refuse to fetch a dependency if it's not pinned to an exact version. This goes
  for transitive dependencies as well (and ties to the Defined point). Most package managers pin all dependencies
  automatically in lockfiles.
* **Secure** - Even with a lockfile, your build is not truly safe from supply chain attacks unless you verify the
  checksums of all dependencies. If your package manager supports specifying the expected checksums, we strongly
  encourage you to make use of them.

  ⚠ Cachi2 will verify checksums if present, but doesn't require them by default. This may change in the future.

In return, Cachi2 will help make your build

* **Auditable** - by generating a manifest of all the dependencies that go into your build.

The ability to achieve the goals depends on the hermeticity of the build process. Ideally, you should try to isolate the
build from both the internet and the underlying host system to avoid implicit dependencies, irreproducible behavior and
whole hosts of other issues. Cachi2 itself is not a hermetic build system. We suggest you take advantage of existing
technologies - such as containers - to achieve isolation (see [usage](docs/usage.md)).

## Basic usage

```shell
cachi2 fetch-deps \
  --source ./my-repo \
  --output ./cachi2-output \
  --package gomod
```

The `fetch-deps` command fetches your project's dependencies and stores them on your disk. You can then use these
outputs to, say, build a container image.

See [docs/usage.md](docs/usage.md) for a more detailed, practical (*cough*) example of Cachi2 usage.

You might also like to check out `cachi2 --help` and the `--help` texts of the available subcommands.

## Project status

Cachi2 was derived (but is not a direct fork) from [Cachito](https://github.com/containerbuildsystem/cachito) and is
still in early development phase.

[cachi2-coveralls]: https://coveralls.io/github/containerbuildsystem/cachi2?branch=main
[cachi2-coveralls-badge]: https://coveralls.io/repos/github/containerbuildsystem/cachi2/badge.svg?branch=main
[wheel-spec]: https://packaging.python.org/en/latest/specifications/binary-distribution-format/
[setuppy-discouraged]: https://setuptools.pypa.io/en/latest/userguide/quickstart.html#setuppy-discouraged
