#!/bin/sh
# Print a public, third-party https URL that serves index-noscheme.html verbatim.
# dia's moderation blocks github.io / jsdelivr / raw.githubusercontent for this page in 1.55.1,
# but httpbin's base64 mirror serves it (text/plain) and is accepted.
B64=$(base64 < "$(dirname "$0")/index-noscheme.html" | tr -d '\n')
echo "https://httpbin.org/base64/$B64"
