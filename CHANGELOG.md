<h1 align = "center">CHANGELOG</h1>

<div align = "justify">

All notable changes to this project will be documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [PEP0440](https://peps.python.org/pep-0440/)
styling guide. For full details, see the [commit logs](https://github.com/PyUtility/autoholidays/commits).

## `PEP0440` Styling Guide

<details>
<summary>Click to open <code>PEP0440</code> Styilng Guide</summary>

Packaging for `PyPI` follows the standard PEP0440 styling guide and is implemented by the **`packaging.version.Version`** class. The other
popular versioning scheme is [`semver`](https://semver.org/), but each build has different parts/mapping.
The following table gives a mapping between these two versioning schemes:

<div align = "center">

| `PyPI` Version | `semver` Version |
| :---: | :---: |
| `epoch` | n/a |
| `major` | `major` |
| `minor` | `minor` |
| `micro` | `patch` |
| `pre` | `prerelease` |
| `dev` | `build` |
| `post` | n/a |

</div>

One can use the **`packaging`** version to convert between PyPI to semver and vice-versa. For more information, check
this [link](https://python-semver.readthedocs.io/en/latest/advanced/convert-pypi-to-semver.html).

</details>

## Release Note(s)

The release notes are documented, the list of changes to each different release are documented. The `major.minor` patch are indicated
under `h3` tags, while the `micro` and "version identifiers" are listed under `h4` and subsequent headlines.

<details>
<summary>Click to open <code>Legend Guidelines</code> for the Project CHANGELOG.md File</summary>

  * 🎉 - **Major Feature** : something big that was not available before.
  * ✨ - **Feature Enhancement** : a miscellaneous minor improvement of an existing feature.
  * 🛠️ - **Patch/Fix** : something that previously didn’t work as documented – or according to reasonable expectations – should now work.
  * ⚙️ - **Code Efficiency** : an existing feature now may not require as much computation or memory.
  * 💣 - **Code Refactoring** : a breakable change often associated with `major` version bump.

</details>

### APTracker v2.2.1 | 2026-03-16

An enhanced version bringing in event management/logging along with terminal client feature to perform tasts easily. In addition,
there were minor bug fixes as below:

  * 🎉 Created event logger table **`apt_events`** to capture all the messages of the current running session, and
  * ✨ Added terminal client **`apt.APTTerminalClient`** to perform any type of operation ((I) `create` to create/register a
    new project; (II) `register` a new session when a code is running in the environment, and (III) `eventlogger` to log
    different types of events for the session.) easily.

**NOTE:** Two pervious PyPI release are yanked because of internal bugs and features not working properly. End users are
requested to upgrade to the latest version, using `pip` command as below.

```shell
pip install -U aptracker
```

**Full Changelog:** is available in https://github.com/PyUtility/aptracker/compare/v2.0.0...v2.2.0 commit messages.

### APTracker v2.0.0 | 2026-03-15

A major upgrade to the **`APTracker`** module that brings unified system and naming bug fixes. The module now handles jobs and
sessions robustly using unified names across the system with additional details for diagnosis and testing.

To explore and understand the full capabilities, upgrade to the latest version using `pip` as:

```shell
pip install -U aptracker
```

### APTracker v1.1.0 | 2026-03-14

The "Advance Python (AP)" Project Tracker **`APTracker`** is a functional module that provides asynchronous functions to track
a project and sessions across a centralized/distributed system by creating unique session keys. The project aims to create an
unified system with minimal dependency overheads.

To explore and understand the full capabilities, upgrade to the latest version using `pip` as:

```shell
pip install -U aptracker
```

### APTracker v1.0.0 | 2026-03-13

A first stable release of a long-standing code file that I ([@ZenithClown](https://github.com/ZenithClown)) typically use for
managing sessions across multiple projects. Creating a release to register the namespace for PyPI release.

To install the package use `pip` as below:

```shell
pip install aptracker
```

</div>
