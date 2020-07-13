# coding: utf-8
'''
Update all extensions to their latest release.
This script only updates version numbers in .toml files,
 please remember to build again after the update.

Caution: this script uses unauthenticated requests to call GitHub API,
 so it is limited by the same rate limit as unauthenticated users.
 Please don't run this script repeatedly in a short period.

See https://developer.github.com/v3/#rate-limiting for more details.
'''
import collections
from http import HTTPStatus as hstatus
import json
import os

import requests
import toml


def get_latest_version(repo):
    resp = requests.get(
        f'https://api.github.com/repos/{repo}/releases/latest',
        headers={
            'user-agent': 'snextensions-updater',
        },
    )
    if resp.status_code != hstatus.OK:
        raise Exception(f'Unexpected HTTP status: {resp.status_code}')

    return resp.json()['tag_name']


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    extension_dir = os.path.join(base_dir, 'extensions')

    # Read and parse all extension info
    for fname in os.listdir(extension_dir):
        if not fname.endswith('.toml'):
            continue

        with open(os.path.join(extension_dir, fname)) as rf:
            # Notice the `_dict`, this is to retain key order,
            # avoiding unnecessary diffs between commits
            ext = toml.load(rf, _dict=collections.OrderedDict)
            repo_name = ext['github']
            version = ext['version']

        try:
            latest_version = get_latest_version(repo_name)
        except Exception as e:
            print(f'❌ {repo_name} : Failed <{e}>')
            continue
        else:
            if latest_version == version:
                print(f'🟢 {repo_name} : {version} is already the latest version')
                continue

            with open(os.path.join(extension_dir, fname), 'w') as wf:
                ext['version'] = latest_version
                toml.dump(ext, wf)
                print(f'✅ {repo_name} : {version} => {latest_version}')


if __name__ == '__main__':
    main()

