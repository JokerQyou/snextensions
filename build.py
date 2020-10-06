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
import glob
import json
import os
import shutil
from subprocess import run

import toml

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def main(base_url):
    while base_url.endswith('/'):
        base_url = base_url[:-1]

    print('Fetching extensions...')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    extension_dir = os.path.join(base_dir, 'extensions')
    public_dir = os.path.join(base_dir, 'public')

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir, ignore_errors=False, onerror=onerror)

    os.makedirs(public_dir)
    os.chdir(public_dir)

    extensions = []

    # Read and parse all extension info
    for fname in os.listdir(extension_dir):
        if not fname.endswith('.toml'):
            continue

        with open(os.path.join(extension_dir, fname)) as rf:
            ext = toml.load(rf)

        # Build extension info
        repo_name = ext['github'].split('/')[-1]
        # https://example.com/my-extension/index.html
        extension_url = '/'.join([base_url, repo_name, ext['main']])
        # https://example.com/my-extension/index.json
        extension_info_url = '/'.join([base_url, repo_name, 'index.json'])
        extension = dict(
            identifier=ext['id'],
            name=ext['name'],
            content_type=ext['content_type'],
            area=ext.get('area', None),
            version=ext['version'],
            description=ext.get('description', None),
            marketing_url=ext.get('marketing_url', None),
            thumbnail_url=ext.get('thumbnail_url', None),
            valid_until='2030-05-16T18:35:33.000Z',
            url=extension_url,
            download_url='https://github.com/{github}/archive/{version}.zip'.format(**ext),
            latest_url=extension_info_url,
            flags=ext.get('flags', []),
            dock_icon=ext.get('dock_icon', {}),
            layerable=ext.get('layerable', None),
            deletion_warning=ext.get('deletion_warning', None),
        )

        # mfa-link (2FA manager) has no expiration
        if ext.get('no_expire', False):
            extension.pop('valid_until', None)

        # Strip empty values
        extension = {k: v for k, v in extension.items() if v}

        # That is very strange, StandardNotes does not upload some npm packages
        # when extensions get updated. We'll have to handle them by git.
        # git clone --branch {version} --depth 1 {github_url}
        run([
            'git', '-c', 'advice.detachedHead=false',
            'clone',
            '--branch', ext['version'],
            '--depth', '1',
            'https://github.com/{github}.git'.format(**ext),
        ])
        shutil.rmtree(os.path.join(public_dir, repo_name, '.git'), ignore_errors=False, onerror=onerror)

        # Generate JSON file for each extension
        with open(os.path.join(public_dir, repo_name, 'index.json'), 'w') as wf:
            json.dump(extension, wf)

        extensions.append(extension)
        print('Loaded extension: {}'.format(ext['name']))

    os.chdir('..')

    # Generate the index JSON file
    with open(os.path.join(public_dir, 'index.json'), 'w') as wf:
        json.dump(
            dict(
                content_type='SN|Repo',
                valid_until='2030-05-16T18:35:33.000Z',
                packages=extensions,
            ),
            wf,
        )

    # Cleanup unnecessary files
    print('Cleaning up...')
    for filename in ['README.md', 'Gruntfile.js', '.babelrc', 'package.json', '*.map', 'src', 'vendor']:
        for matched_fpath in glob.glob(f'public/*/{filename}'):
            if os.path.isdir(matched_fpath):
                shutil.rmtree(matched_fpath, ignore_errors=False, onerror=onerror)
            elif os.path.isfile(matched_fpath):
                os.remove(matched_fpath)
            else:
                continue

            print(f'> Removed {matched_fpath}')

    # Distribute header rules for Netlify
    shutil.copyfile('_headers', os.path.join(public_dir, '_headers'))

    print('Build finished')


if __name__ == '__main__':
    main(os.getenv('URL', 'https://snext.netlify.app/'))

