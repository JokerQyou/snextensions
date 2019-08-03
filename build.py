# coding: utf-8
'''
Parse extensions/*.toml files, output a static site with following structure:
public/
  |-my-extension-1/
  |  |-index.json  <- extension info
  |  |-index.html  <- extension entrance (component)
  |  |-dist  <- extension resources
  |  |-...  <- other files
  |
  |-index.json  <- repo info, contain all extensions' info
'''
import json
import os
import shutil
from subprocess import run

import toml


def main(base_url):
    while base_url.endswith('/'):
        base_url = base_url[:-1]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    extension_dir = os.path.join(base_dir, 'extensions')
    public_dir = os.path.join(base_dir, 'public')

    extensions = []

    # Read and parse all extension info
    for fname in os.listdir(extension_dir):
        if not fname.endswith('.toml'):
            continue

        with open(os.path.join(extension_dir, fname)) as rf:
            ext = toml.load(rf)

        # Build extension info
        # https://example.com/my-extension/index.html
        extension_url = '/'.join([base_url, ext['npm'], ext['main']])
        # https://example.com/my-extension/index.json
        extension_info_url = '/'.join([base_url, ext['npm'], 'index.json'])
        extension = dict(
            identifier=ext['id'],
            name=ext['name'],
            content_type=ext['content_type'],
            area=ext['area'],
            version=ext['version'],
            description=ext['description'],
            marketing_url=ext.get('marketing_url', None),
            thumbnail_url=ext.get('thumbnail_url', None),
            valid_until='2030-05-16T18:35:33.000Z',
            url=extension_url,
            download_url='https://github.com/{github}/archive/{version}.zip'.format(**ext),
            latest_url=extension_info_url,
            flags=ext.get('flags', []),
        )

        # Strip empty values
        for k, v in extension.items():
            if not v:
                extension.pop(k, v)

        # npm install --save
        run(['npm', 'install', '--save', '{npm}@{version}'.format(**ext)])

        # Generate JSON file for each extension
        with open(os.path.join(base_dir, 'node_modules', ext['npm'], 'index.json'), 'w') as wf:
            json.dump(extension, wf)

        extensions.append(extension)
        print('Loaded extension: {}'.format(ext['name']))

    # `node_modules` will be our `public`
    shutil.move(
        os.path.join(base_dir, 'node_modules'),
        os.path.join(base_dir, 'public'),
    )

    # Generate the index JSON file
    with open(os.path.join(base_dir, 'public', 'index.json'), 'w') as wf:
        json.dump(
            dict(
                content_type='SN|Repo',
                valid_until='2030-05-16T18:35:33.000Z',
                packages=extensions,
            ),
            wf,
        )


if __name__ == '__main__':
    main(os.getenv('BASE_URL', 'https://snext.netlify.com/'))

