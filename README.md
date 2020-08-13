# snextensions

[![Netlify Status](https://api.netlify.com/api/v1/badges/53e5f0b7-02c9-400d-8590-159860892cdc/deploy-status)](https://app.netlify.com/sites/snext/deploys)

A set of open source extensions for StandardNotes.

# Usage

Paste `https://snext.netlify.app/index.json` into `Extended Code` in StandardNotes.

# Notice

Previously (last year) the URL was `https://snext.netlify.com/index.json`.
But early this year Netlify decided to change the domain used by hosted apps.

If you've been experiencing empty editor UI, there's a chance that you're using
the old URL. Netlify is taking care of redirections but they are missing some
headers. You should migrate to the new URL.

These steps are required to migrate:

- Look for the "Repository" options in the "Extensions" menu (on the bottom)
- Delete the repository
- Uninstall all installed themes and editors
- Re-enter the new URL into `Extended Code`
- Re-install all the themes and editors you use

# Contribution

If you'd like an extension to be included in this repository, feel free to open an issue.

# Self-hosting

## With Netlify

In case if you'd like to host your own site other than using ours, you can do so with Netlify:

- Fork this repository;
- Create a Netlify account if you don't have one already;
- In Netlify app, Use "New site from Git" to create a site from your forked GitHub repository;
- Wait for the build to finish;
- After that you can use `YOUR_SITE_URL/index.json` as an `Extended Code`;
- Optionally you can set a human-readable site name (a subdomain of `netlify.app`) from the `Site settings` page.

## Without Netlify

It's easy and recommended to host with Netlify. However if you insist not to use it, it is also possible (notice: the following steps work on Linux or WSL):

- Prepare your environment with `Python 3.7` with `pip`, as well as `Git`;
- Make sure Python 3.7 can be called directly via `python` from the shell;
- Make sure Git is installed and can be called directly via `git` from the shell;
- `pip install -r requirements.txt` to install required Python libraries;
- Run the build script `python build.py`;
- Verify that:
  - the `public` directory is generated;
  - there should be `public/index.json` containing information of all extensions;
  - all extensions should exists in `public` as sub-directories;
- Host the `public` directory like you would do with any static resources, using nginx, caddy, etc.
- You need to enable CORS headers on your reverse proxy (nginx / caddy / traefik). With nginx these rules will be enough:
  ```nginx
  add_header 'Access-Control-Allow-Origin' '*';
  add_header 'Access-Control-Allow-Headers' 'content-type';
  ```

