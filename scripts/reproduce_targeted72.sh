#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -c "import json; d=json.load(open('${DIR}/../artifacts/icassp2027/requests/targeted72_requests.json')); print(f'Loaded {len(d)} registered Targeted-72 requests.')"
