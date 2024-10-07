# Flatpak Zed

## Issues
Please open issues under: https://github.com/flathub/dev.zed.Zed/issues

## Usage

Zed's current Flatpak integration exits the sandbox on startup and most functionality works out of the box. Workflows that rely on Flatpak's sandboxing may not work as expected by default.

Please note that Zed's flatpak still runs in an isolated environment and some language toolchains might misbehave when executed from the host OS into the sandbox.  
The Zed's flatpak supports sandbox escape at startup disablement and SDK extensions that can be enabled to support problematic additional languages.

### Environment variables

- `ZED_FLATPAK_NO_ESCAPE`: disable flatpak sandbox escape (default: not set)
  ```shell
    $ flatpak override --user dev.zed.Zed --env=ZED_FLATPAK_NO_ESCAPE=1
  ```

### Execute commands on the host system

When Zed's flatpak is running in the sandbox with no escape, it is not possible to execute commands on the host system.

To execute commands on the host system, run inside the sandbox:
```shell
  $ flatpak-spawn --host <COMMAND>
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
