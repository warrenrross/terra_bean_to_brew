---
name: zip-deploy-static-site-azure
description: Deploy a static HTML/CSS/JS site (no build step) to an Azure App Service Linux Node web app with a zip deploy, and verify every page. Use whenever the user wants to put a static site, GitHub Pages site, or plain index.html project onto an Azure web app, asks to "deploy the site/app files" after a Terraform apply created the web app, sees the default "Microsoft Azure App Service - Welcome" page, or gets 404s on navigation links after an Azure deploy, even if they never say "zip deploy".
---

# Zip-deploy a static site to an Azure Node web app

A Linux Node web app (for example one Terraform created with `node_version = "22-lts"`) runs `npm start`. A static site has no server, so the app keeps showing Azure's placeholder page until you ship the files plus a tiny server. This skill does that and proves every page loads.

## Why it works this way
- Relative links such as `pages/production.html` behave the same on Azure as on GitHub Pages. If navigation breaks after deploy, suspect missing files in the zip, not link syntax. Do not create a second "Azure version" repo.
- The zip is built outside the site repo so the repo stays untouched and still works on GitHub Pages.

## Steps

1. **Get the site source** (clone to a scratch dir if it is not local) and the target: resource group and web app name (`terraform output web_app_name`, `resource_group_name`, `web_app_url`).
2. **Build the zip** with the bundled script. It packages every git-tracked file (minus docs, skills, tests, Makefile, README, *.py), adds `server.js` and `package.json` if missing, and runs the link check before it writes the zip:
   ```bash
   bash ~/.claude/skills/zip-deploy-static-site-azure/scripts/build_zip.sh <site-dir> <scratch>/site.zip
   ```
   It fails if any local `href`/`src` points at a file that is not in the package. If the site loads something the script excluded (for example a `.py`-generated file, or a `docs/` page that is linked), narrow the exclude regex in `build_zip.sh`.
3. **Deploy:**
   ```bash
   az webapp deploy -g <rg> -n <app> --src-path <scratch>/site.zip --type zip --clean true
   ```
   Look for `"status": "RuntimeSuccessful"`. `--clean true` removes the previous deploy so stale files cannot linger. Basic-auth publishing must be on (the Terraform guide's template leaves it enabled).
4. **Verify over HTTP**, not just "deploy succeeded":
   ```bash
   python3 ~/.claude/skills/zip-deploy-static-site-azure/scripts/check_links.py <staged-or-site-dir> --base-url https://<app>.azurewebsites.net
   curl -s https://<app>.azurewebsites.net/ | grep -i '<title'
   ```
   Expect HTTP 200 for every reference and the site's own `<title>`, not "Microsoft Azure App Service - Welcome".
5. **If the user still sees the default or a broken page**, curl with `-H 'Cache-Control: no-cache'` and a `?x=$RANDOM` query to separate server problems from browser cache. If the server is right, tell them to hard-refresh (Cmd+Shift+R).
6. Repeat for each environment (dev, prod) with the same zip.

## Gotchas
- Never hand-pick folders for the zip. Always package from `git ls-files`; a hand-picked list once omitted `pages/` and `assets/`, and every nav link 404'd.
- Don't truncate file listings (`| head`) when deciding what the site contains.
- A fresh F1 plan may be slow on the first request (cold start); retry once before debugging.
- zsh does not word-split unquoted variables, so don't loop with `set -- $t`; call a shell function with explicit arguments.
- Tearing down: the deployed content disappears with the web app (`terraform destroy`); nothing in the zip needs separate cleanup.
