#!/bin/bash
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="N2T2023a" \
--output ./.github/scripts/key.json ./.github/scripts/key.json.gpg