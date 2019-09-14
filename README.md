# snextensions

[![Netlify Status](https://api.netlify.com/api/v1/badges/53e5f0b7-02c9-400d-8590-159860892cdc/deploy-status)](https://app.netlify.com/sites/snext/deploys)

A set of open source extensions for StandardNotes.

# Usage

Paste `https://snext.netlify.com/index.json` into `Extended Code` in StandardNotes.

# Notice

Currently we only host extensions developed by StandardNotes.
Some of the official extensions are not included.

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
- Optionally you can set a human-readable site name (a subdomain of `netlify.com`) from the `Site settings` page.

## Without Netlify

It's easy and recommended to host with Netlify. However if you insist not to use it, it is also possible:

- Prepare your environment with `Python 3.7` with `pip`, as well as `Git`;
- Make sure Python 3.7 can be called directly via `python` from the shell;
- Make sure Git is installed and can be called directly via `git` from the shell;
- `pip install -r requirements.txt` to install required Python libraries;
- Run the build script `./build.sh`;
- Verify that:
  - the `public` directory is generated;
  - there should be `public/index.json` containing information of all extensions;
  - all extensions should exists in `public` as sub-directories;
- Host the `public` directory like you would do with any static resources, using nginx, caddy, etc.
