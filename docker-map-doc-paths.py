#!/usr/bin/python3

# SPDX-License-Identifier: MIT

"""
This is a wrapper script for the Docker/Podman CLIs to make them understand document portal paths.

Inside the Flatpak sandbox, most access to the host system comes through the document portal, a
special FUSE filesystem that reflects the files/directories that the user has chosen to expose
to an application. For Zed, this grant happens when you open a new local project and select a
directory in the standard file chooser, the returned path is in the doc portal filesystem.

The problem for Docker/Podman is that doc portal paths only exist inside the sandbox, not on the
host system where Docker/Podman is running. So if Zed tries to start a Dev Container and mount
the source workspace inside the container, Docker/Podman will not recognize the path and reject
the entire request.

This wrapper steps in and surgically replaces some references to the document portal filesystem
with their corresponding path(s) on the host system, specifically the source(s) of `--mount`
options. Note that labels like `devcontainer.local_folder` are unchanged and will still
reference the doc portal path, which happens to be shared across all Flatpaks (but not the host).
"""

import functools
import json
import os
import re
import subprocess
import sys
import typing
from pathlib import Path, PurePath

# Standard location where the document portal is mounted inside the sandbox
SANDBOX_DOC_PORTAL_PATH = Path("/run/flatpak/doc/")


@functools.cache
def host_path_for(path: Path) -> PurePath:
    "Get the corresponding host path for a doc portal path"
    try:
        return PurePath(
            subprocess.run(
                [
                    "getfattr",
                    "--name=user.document-portal.host-path",
                    "--only-values",
                    "--",
                    path,
                ],
                check=True,
                capture_output=True,
            ).stdout.decode("utf-8")
        )
    except (subprocess.CalledProcessError, UnicodeDecodeError):
        return path


def doc_portal_paths() -> typing.Generator[Path]:
    "Iterate over all the known paths provided by the doc portal"
    for id_dir in SANDBOX_DOC_PORTAL_PATH.iterdir():
        for file in id_dir.iterdir():
            yield file


def re_literal(values) -> str:
    "Return a regex that matches any of the given literal values"
    return "(?:" + "|".join(re.escape(str(val)) for val in values) + ")"


def repl_host_path(match: re.Match) -> str:
    "Replace an re.Match first group with the corresponding host path"
    return (
        match.string[match.start() : match.start(1)]
        + str(host_path_for(match.group(1)))
        + match.string[match.end(1) : match.end()]
    )


def main(exe: str, argv: list[str]) -> None:
    # Replace --mount references to a doc path with its host path
    argv = [
        re.sub(
            rf"(?:source|src)=({re_literal(doc_portal_paths())})", repl_host_path, arg
        )
        for arg in argv
    ]

    if argv[1] == "inspect":
        # As special case, we need to manipulate the output too
        # This should be unnecessary after https://github.com/zed-industries/zed/pull/53829 is merged
        proc = subprocess.run(argv, executable=exe, stdout=subprocess.PIPE)
        output = proc.stdout
        for doc_path in doc_portal_paths():
            doc_path_json = json.dumps(str(doc_path)).encode("utf-8")
            host_path_json = json.dumps(str(host_path_for(doc_path))).encode("utf-8")
            output = re.sub(
                rb'"Source":\s*' + re.escape(doc_path_json),
                b'"Source":' + host_path_json,
                output,
            )
        sys.stdout.buffer.write(output)
        sys.stdout.buffer.flush()
        sys.exit(proc.returncode)

    # Exec to the final command line
    os.execvp(exe, argv)


if __name__ == "__main__":
    main(sys.argv[0] + ".real", sys.argv)
