#!/bin/bash

# Create a default config if not present
if [ ! -f "$XDG_CONFIG_HOME/zed/settings.json" ]; then
  cat >$XDG_CONFIG_HOME/zed/settings.json <<EOF
// Zed settings
//
// For information on how to configure Zed, see the Zed
// documentation: https://zed.dev/docs/configuring-zed
//
// To see all of Zed's default settings without changing your
// custom settings, run `zed: open default settings` from the
// command palette (cmd-shift-p / ctrl-shift-p)
{
"auto_update": false
}
EOF
fi

exec zed-wrapper "$@"
