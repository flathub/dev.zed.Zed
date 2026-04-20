# Flatpak Zed

## Issues
Please open issues under: https://github.com/flathub/dev.zed.Zed/issues

## Usage

Zed's current Flatpak integration runs Zed outside the Flatpak sandbox, on the host system. Users have encountered issues with language toolchains and other commands while in this mode, see e.g. https://github.com/flathub/dev.zed.Zed/issues/330 for discussion.

If you are experiencing these issues, one workaround is to run Zed inside the Flatpak sandbox with:

```shell
flatpak override --user dev.zed.Zed --env=ZED_FLATPAK_NO_ESCAPE=1
```

The Flatpak sandbox provides a basic development environment (Git, GCC, Python, etc.) by default. To use a more complex development environment, you can:
  - use Dev Containers
  - execute commands (including your shell) on the host system
  - enable SDK extensions for additional languages

### Dev Containers

Dev Containers provide a consistent, reproducible environment using Docker/Podman containerization. This description exists as part of the repository in `.devcontainer/`.

Zed has native support for Dev Containers. Use the `project: open dev container` command if you already have a `.devcontainer/`, otherwise you can generate one using the `project: initialize dev container` command.

Note that you need to install the container runtime on your host system. If you are using Podman, you also need to set `"use_podman": true` in your Zed `settings.json`.

#### Docker instructions

1. [Install Docker](https://docs.docker.com/engine/install/) if you haven't already
2. Add your user to the `docker` group (`sudo usermod -aG docker $(whoami)`)
3. Confirm it works by running `docker run --rm docker.io/hello-world` from the Zed built-in terminal

#### Podman instructions

1. [Install Podman](https://podman.io/docs/installation) if you haven't already
2. Enable/start the Podman socket with `systemctl --user enable --now podman.socket`
3. Confirm it works by running `podman -r run --rm quay.io/podman/hello` from the Zed built-in terminal
4. If your host Podman is older than 5.6.0, you also need to set:

```shell
flatpak override --user dev.zed.Zed --filesystem=/tmp/devcontainer-zed:create
```

5. Set `"use_podman": true` in your Zed `settings.json`

See also the [Podman Rootless Tutorial](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md#etcsubuid-and-etcsubgid-configuration) for more detailed instructions and troubleshooting.

#### Podman Desktop instructions

1. [Install Podman Desktop](https://podman-desktop.io/docs/installation/linux-install) if you haven't already
2. Leave Podman Desktop running in the background while using Zed
3. Confirm it works by running `podman -r run --rm quay.io/podman/hello` from the Zed built-in terminal
4. If your host Podman is older than 5.6.0, you also need to set:

```shell
flatpak override --user dev.zed.Zed --filesystem=/tmp/devcontainer-zed:create
```

5. Set `"use_podman": true` in your Zed `settings.json`

See also the [Podman Rootless Tutorial](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md#etcsubuid-and-etcsubgid-configuration) for more detailed instructions and troubleshooting.

### Execute commands on the host system

When Zed's flatpak is running in the sandbox with no escape, it is not possible to execute commands on the host system.

To execute commands on the host system, run inside the sandbox:

```shell
$ flatpak-spawn --host <COMMAND>
```

or

```shell
$ host-spawn <COMMAND>
```

- Most users seem to report a better experience with `host-spawn`

### Use host shell in the integrated terminal.

Another option to execute commands is to use your host shell in the integrated terminal instead of the sandbox one.

For that, open Zed's settings via <kbd>Ctrl</kbd> + <kbd>,</kbd>

The following examples will figure out and launch the current user's preferred terminal. More configuration settings for spawning commands can be found in [Zed's documentation](https://zed.dev/docs/configuring-zed#terminal-shell).

`flatpak-spawn --host`

```json
{
  "terminal": {
    "shell": {
      "with_arguments": {
        "program": "/usr/bin/flatpak-spawn",
        "args": [
          "--host",
          "--env=TERM=xterm-256color",
          "sh",
          "-c",
          "exec $(getent passwd $USER | cut -d: -f7)"
        ]
      }
    }
  },
}
```

`host-spawn`

```json
{
  "terminal": {
    "shell": {
      "with_arguments": {
        "program": "/app/bin/host-spawn",
        "args": [
          "sh",
          "-c",
          "exec $(getent passwd $USER | cut -d: -f7)"
        ]
      }
    }
  },
}
```

### SDK extensions

This flatpak provides a standard development environment (gcc, python, etc).
To see what's available:

```shell
  $ flatpak run --command=sh dev.zed.Zed
  $ ls /usr/bin (shared runtime)
  $ ls /app/bin (bundled with this flatpak)
```
To get support for additional languages, you have to install SDK extensions, e.g.

```shell
  $ flatpak install flathub org.freedesktop.Sdk.Extension.dotnet
  $ flatpak install flathub org.freedesktop.Sdk.Extension.golang
```
To enable selected extensions, set `FLATPAK_ENABLE_SDK_EXT` environment variable
to a comma-separated list of extension names (name is ID portion after the last dot):

```shell
  $ FLATPAK_ENABLE_SDK_EXT=dotnet,golang flatpak run dev.zed.Zed
```
To make this persistent, set the variable via flatpak override:

```shell
  $ flatpak override --user dev.zed.Zed --env=FLATPAK_ENABLE_SDK_EXT="dotnet,golang"
```

You can use:
```shell
  $ flatpak search <TEXT>
```
to find others.

### Run flatpak Zed from host terminal

If you want to run `zed /path/to/file` from the host terminal just add this
to your shell's rc file:

```shell
  $ alias zed="flatpak run dev.zed.Zed"
```

then reload sources, now you could try:

```shell
  $ zed /path/to/
  # or
  $ FLATPAK_ENABLE_SDK_EXT=dotnet,golang zed /path/to/
```

## Related Documentation

- https://zed.dev/docs/
