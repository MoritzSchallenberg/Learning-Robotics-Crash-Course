# Rebrand follow-ups: repository transfer / rename

**Not part of the published website.** Internal working document for
Entwicklungsauftrag 8.

The site itself is now branded **ALeRT Advanced Robotics Tutorial**. Per
the task's explicit instruction, the underlying GitHub repository name
(`MoritzSchallenberg/Learning-Robotics-Crash-Course`) and its GitHub Pages
URL were **not** changed or transferred — that requires an explicit target
repository within the `RRL-ALeRT` organisation, which does not yet exist,
and admin rights over both the source and destination repositories.

## What a later transfer/rename would actually require

1. **Decide the target.** Either:
   - transfer this existing repository into the `RRL-ALeRT` GitHub
     organisation (keeps history, stars, issues; requires organisation
     owner permission on the `RRL-ALeRT` side and admin rights on this
     repository), or
   - create a new, empty repository under `RRL-ALeRT` and push this
     repository's history into it (loses the "transferred from" marker
     GitHub shows on a true transfer, but avoids needing organisation-owner
     rights if that is a blocker).
2. **Repository name.** Suggest something that reads as documentation, not
   a fork of the robot's own driver code — e.g. `RRL-ALeRT/tutorial` or
   `RRL-ALeRT/advanced-robotics-tutorial` — to avoid confusion with the
   many `alert_*`/`*_ros2` code repositories already in the organisation.
3. **GitHub Pages re-enablement.** Pages settings do not automatically
   carry over on a transfer in every case; after the move, confirm
   Settings → Pages is still configured to build from the same branch/
   workflow (`.github/workflows/pages.yml` already deploys via the
   `actions/deploy-pages` mechanism, which should keep working once Pages
   is re-enabled on the new location).
4. **Update `html_baseurl` in `docs/conf.py`** to the new
   `https://rrl-alert.github.io/<new-repo-name>/` (or a custom domain, if
   one is set up instead) — every asset path on the site is relative, so
   this is the only required code change for the new URL to work, but the
   value must be updated for the sitemap/canonical-URL machinery Sphinx
   generates from it.
5. **Update every hard-coded reference to the current URL/repo name.**
   `README.md`'s "Website:" line, this file's own text, the "repository
   README" links scattered through several `videos.md` continue-learning
   entries (`https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course`),
   and `scripts/verify-site.py`'s local-serving path
   (`/tmp/site-serve/Learning-Robotics-Crash-Course`) and its `--base-url`
   default.
6. **Decide what happens to the old URL.** GitHub Pages does not
   automatically redirect an old Pages URL to a new one after a repository
   move; anyone with the old bookmark gets a 404 once the old repository's
   Pages are disabled. Consider whether the old repository should be kept
   around (even empty, or as an archived README pointing at the new
   location) specifically to avoid a dead link for anyone who already
   bookmarked or linked the current site.
7. **Update GitHub Actions secrets on the new repository.** Any secret
   configured on the current repository (see
   `maintainers/repository-audit.md` and, once implemented, the
   `STATICRYPT_PASSWORD` secret for the encrypted-deployment gate) does
   **not** carry over automatically on a transfer to a different owner in
   every case — verify and re-set it on the destination repository before
   relying on the workflow there.
8. **Update `docs/conf.py`'s `author`/`copyright` fields** if the
   organisational owner of the content changes as part of the move (e.g.
   if `RRL-ALeRT` becomes the named copyright holder instead of, or
   alongside, the MASKOR Institute).

None of the above was performed as part of this task — the task
explicitly says not to transfer or rename the repository independently,
and several of the steps above need admin rights this session does not
have and should not attempt to bypass.
