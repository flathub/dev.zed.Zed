# SPDX-License-Identifier: MIT

case "$PATH" in
  /app/bin:*|/app/bin/:*) ;;
  *) export PATH=/app/bin:"$PATH"; ;;
esac
