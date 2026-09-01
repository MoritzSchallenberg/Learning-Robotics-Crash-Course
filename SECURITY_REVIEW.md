# Security review

Review of the source material for secrets and sensitive data before publishing
this repository, which is **public**.

**Date:** 2026-09-01
**Scope:** all three source tutorial exports, the generated Markdown sources,
the static assets, the generated HTML output, and the git history of this
repository.


> **This report deliberately contains no secret values.**
> It names the affected source file, the category of finding, and the action
> taken. It never reproduces a password, key, token, address or hostname — not
> in full, not partially, and not in any obfuscated form that would still
> reveal the original.

---

## 1. Summary

| Category | Findings | All remediated |
|---|---|---|
| Cleartext credentials | 4 | Yes |
| Internal network addressing | 3 | Yes |
| Internal hostnames | 1 | Yes |
| Wireless network identifiers | 2 | Yes |
| Signed / expiring media URLs | 1 (10 URLs) | Yes |
| Personal data | 3 | Yes |
| Internal / private repository references | 2 | Yes |
| Internal operational procedures | 3 | Yes |

**No secret of any kind was carried into this repository**, into the generated
site, or into any commit. The remediation for every credential finding was
exclusion of the affected content, not substitution — no placeholder derived
from an original value is used anywhere.

---

## 2. Findings

### 2.1 Cleartext credentials

| # | Source file | Category | Action taken |
|---|---|---|---|
| C-1 | Carologistics — `01 Introductory Information/02 Network-Setup.htm` | Cleartext credentials for network infrastructure devices | Page excluded in full. No credential, and no device-configuration content from this page, appears on the site. Networking guidance was written from scratch from primary documentation instead. |
| C-2 | Carologistics — `01 Introductory Information/02 Network-Setup.htm` | Cleartext credentials for a management console | Page excluded in full, as above. |
| C-3 | Carologistics — `01 Introductory Information/04 Working-on-Remote-Hosts.htm` | Cleartext shared account credential for robot hosts | Page excluded in full. The general SSH and key-based login practice was rewritten generically, with no account names or credentials. |
| C-4 | ALeRT — `Spot Documentation/08 Spot Startup` | Reference to stored credentials in a device web interface, with the access path described | Excluded. The published Spot operating summary omits the interface path and states that credentials and exact procedures are obtained from the team. |

**Verification:** a keyword scan for credential terms (`password`, `passwd`,
`secret`, `api[-_]key`, `token`, `credential`, `passphrase`, `psk`) was run
across the repository sources, static assets and generated HTML. Every
remaining match is a *generic instruction* ("you will be prompted for a
password", "give the key a passphrase") containing no value.

### 2.2 Internal network addressing

| # | Source file | Category | Action taken |
|---|---|---|---|
| N-1 | Carologistics — `Network-Setup.htm` | Internal subnet, gateway and DNS addressing for the team network | Excluded. The site explains subnets and netmasks with a generic textbook example (`192.168.1.100`) that corresponds to no real host. |
| N-2 | Carologistics — `Working-on-Remote-Hosts.htm` | Complete internal IP-to-host mapping table for robots and infrastructure | Excluded in full. |
| N-3 | Carologistics — `06 Information on Projects/04 gripper-pi-img.htm` | Internal NFS server address in boot and mount configuration | Excluded. The network-boot procedure is not published. |

Additionally, an institute-range IP prefix and a device-specific address that
appeared in the Summer School networking material were removed; the site uses
`<ip-address>` placeholders that carry no information about the originals.

**Verification:** a regular-expression scan for RFC 1918 ranges
(`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) and for the institute's
public range was run over all sources, assets and generated HTML. The only
remaining private-range literals anywhere in the repository or the built site
are the textbook example `192.168.1.100 / 255.255.255.0 / 192.168.1.0`, used on
one page to explain how a netmask works, and `127.0.0.1` in a DDS configuration
example. Neither identifies any real host. No address from any source file
survives.

### 2.3 Internal hostnames

| # | Source file | Category | Action taken |
|---|---|---|---|
| H-1 | Carologistics — `Working-on-Remote-Hosts.htm`, `Starting-a-Robot.htm`, `Automated-Setup-using-Ansible.htm` | Internal hostnames and SSH host aliases for robots, referee box and central agent | Excluded. Where a deployment command is shown for teaching purposes, the host argument is a `<host>` placeholder. |

### 2.4 Wireless network identifiers

| # | Source file | Category | Action taken |
|---|---|---|---|
| W-1 | Carologistics — `Network-Setup.htm` | Team wireless network identifier | Excluded. |
| W-2 | ALeRT — `Spot Documentation/08 Spot Startup` | Operations wireless network identifier | Excluded. The published procedure says "the team's operations network". |

### 2.5 Signed / expiring media URLs

| # | Source file | Category | Action taken |
|---|---|---|---|
| U-1 | Carologistics — `05 Setup Guides/07 Labeling-Data.htm` | 10 image URLs on a private user-content host, each carrying a signed JWT with an embedded cloud credential identifier and an expiry | All excluded. No image from this page is published, and no URL from it appears in any source file, asset or generated page. The labeling *guidance* was rewritten in prose without the reference images. |

This is the most sensitive category found: the query strings embed
authentication material, and republishing them would expose it.

**Verification:** a scan for `X-Amz-`, `Signature=`, `jwt=`, `token=` and
`Expires=` across the repository and generated HTML returns no matches.

### 2.6 Personal data

| # | Source file | Category | Action taken |
|---|---|---|---|
| P-1 | Carologistics — `02 Organization/02 Milestones.htm` | Named individuals assigned to work items | Page excluded in full. |
| P-2 | Carologistics — `02 Organization/01 Agenda.htm` | Meeting notes naming individuals, plus travel and visa discussion | Page excluded in full. |
| P-3 | Carologistics — `04 Learn more about our Hardware/02 CAD-Tutorial.htm`; ALeRT — `08 Spot Startup` | Named individuals as contact points, and an instruction to send account details to a named person | Excluded. The site says "ask your team lead" without naming anyone. |

Personal names, personal email addresses and personal account identifiers do
not appear anywhere on the site. The example email address used on the Git page
is a generic `example.org` address.

### 2.7 Internal and private repository references

| # | Source file | Category | Action taken |
|---|---|---|---|
| R-1 | Summer School — `Session 3/2. LASER Scanner` | Clone URL for a fork on the institute's internal GitLab, under a personal user namespace | Excluded. The site does not reproduce this URL. |
| R-2 | Carologistics — several wiki pages | Links into a private team wiki and private repository paths | Excluded. Only public repository URLs under the public `carologistics`, `MASKOR` and `RRL-ALeRT` organisations are linked. |

### 2.8 Internal operational procedures

| # | Source file | Category | Action taken |
|---|---|---|---|
| O-1 | Carologistics — `Network-Setup.htm` | Network infrastructure configuration and device reset procedures | Excluded. |
| O-2 | Carologistics — `05 Setup Guides/04 Setting-up-the-Refbox.htm`, `06 Official-Competitions.htm` | Competition infrastructure setup | Excluded as internal operations, and not relevant to the general course. |
| O-3 | ALeRT — `08 Spot Startup` | Full step-by-step operating procedure for expensive hardware, including exact control sequences and fault-recovery via a device management interface | Reduced to a safety-focused overview that states the procedure must be obtained from the team with a hands-on briefing. Exact sequences and interface access are not published. |

---

## 3. Controls in place

### 3.1 `.gitignore`

Raw source material can never be committed. `.gitignore` excludes:

```gitignore
*.zip
source-material/
raw-material/
extracted/
Verschiedene Tutorials*/
00-0*/
_build/
docs/_build/
.venv/
__pycache__/
.DS_Store
```

The extracted source directories live **outside** this repository, and the
working copies used during analysis were written to a temporary directory
outside it as well.

### 3.2 Pre-push scan

The scan below was run over the git index, the working tree, the static assets
and the generated HTML before pushing, and returns no findings:

```bash
# Credentials and keys
grep -rniE '(password|passwd|secret|api[_-]?key|token|credential|passphrase)[[:space:]]*[:=]' \
  --include='*.md' --include='*.py' --include='*.yml' --include='*.yaml' \
  --include='*.css' --include='*.js' --include='*.html' .

# Private key material
grep -rnE 'BEGIN [A-Z ]*PRIVATE KEY|ssh-rsa AAAA|ssh-ed25519 AAAA' .

# Private network addressing
grep -rnE '\b(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.)[0-9]{1,3}\.[0-9]{1,3}' \
  --include='*.md' --include='*.html' .

# Signed / expiring URLs
grep -rnE 'X-Amz-|Signature=|[?&]jwt=|[?&]token=|Expires=' .
```

The only matches are the documented, intentional examples listed in §2.2.

### 3.3 Verified in the build output

The generated HTML in `docs/_build/html/` was scanned with the same patterns
after a clean build. No secret, internal address, internal hostname or signed
URL appears in the published output.

### 3.4 Repository history

This repository's history was created fresh for this work. No commit contains
raw source material, and no commit has ever contained a secret. No history
rewrite was necessary.

---

## 4. Recommendations to the institute

These are **outside** the scope of this repository, but follow directly from
what the review found.

1. **Rotate the credentials found in cleartext in the Carologistics wiki.**
   They were readable to anyone with wiki access and have now also been present
   in an exported copy of that wiki. They should be treated as compromised and
   changed.

2. **Move credentials out of the wiki entirely.** A password manager or an
   Ansible Vault is the right place; a wiki page is not, regardless of how
   access is restricted.

3. **Review who has access to the exported tutorial archive.** It contains
   every finding in this report.

4. **Regenerate the reference images on the Labeling Data page.** They are
   currently served from signed URLs that will expire; hosting them properly
   would both fix that and make them publishable if the rights allow.

5. **Consider a secret-scanning pre-commit hook** on the team wikis and
   repositories. The teams already use `pre-commit`, so adding a
   `detect-secrets` or `gitleaks` hook is a small change.

---

## 5. Statement

Every finding above has been remediated by **exclusion**. No credential, key,
token, internal address, internal hostname, wireless identifier, signed URL or
personal identifier from the source material has been published to this
repository or to the generated website — neither directly, nor as a placeholder
from which the original could be recovered.

Related records:

- `CONTENT_REVIEW.md` — what was included, merged, made platform-specific, or
  excluded, and why
- `LICENSES.md` — licensing and attribution
