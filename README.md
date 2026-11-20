# 9R AI Skills

Shared AI skills for the 9R team, distributed as one marketplace for Codex,
Grok, and Claude Code. Each plugin has its own directory and version so
teammates can select the tools they need as the catalog grows. A skill is
installable only when its plugin is listed in all three catalogs.

## Available plugins

| Plugin | Skill | Purpose |
| --- | --- | --- |
| `alc-dashboard` | `alcosan-municipal-dashboard` | Build ALCOSAN executive dashboards from Municipal Meeting Monitor CSV reports. |
| `rtp-casestudies` | `rtp-casestudies` | Create editable, client-colored PowerPoint case studies using the shared 9Rooftops framework. |

The dashboard skill includes its Python generator, self-contained HTML template
and data-processing reference. The generator uses Python 3 and the standard
library; no npm dependencies or startup hooks are required. PDF production
requires a browser capable of printing the generated HTML.

## Install for local development

Clone this repository and register its absolute path:

```bash
git clone git@github.com:jlyvers-9rooftops/9r-ai-skills.git
codex plugin marketplace add /absolute/path/to/9r-ai-skills
```

Restart the ChatGPT desktop app, open the Plugins Directory, select **9R AI
Skills**, and install **ALCOSAN Dashboard**. Test in a new Codex conversation.
Marketplace support varies by client; these instructions target supported local
Codex clients. The plugin requires local execution, not web-only execution.

## Install from the shared repository

After the marketplace files have been committed and pushed to GitHub, teammates
with repository access can register the Git source directly:

```bash
codex plugin marketplace add git@github.com:jlyvers-9rooftops/9r-ai-skills.git
codex plugin marketplace list
```

Then select the marketplace and install the plugin in the desktop app as above.
Git authentication and repository access must already be configured.

For updates to a registered Git marketplace:

```bash
codex plugin marketplace upgrade 9r-ai-skills
```

Restart the app and check the installed plugin version. For a local clone, pull
changes first and refresh/reinstall the local plugin if its cached copy has not
updated. Installing a marketplace does not automatically enable every plugin.

## Install in Grok

Register the marketplace, then install the plugin you need:

```bash
grok plugin marketplace add git@github.com:jlyvers-9rooftops/9r-ai-skills.git
grok plugin install alc-dashboard --trust
grok plugin install rtp-casestudies --trust
```

For a local clone, pass its absolute path to `grok plugin marketplace add`.
Refresh a registered marketplace with `grok plugin marketplace update`. Grok
reads `.grok-plugin/marketplace.json`.

## Install in Claude Code

```bash
claude plugin marketplace add git@github.com:jlyvers-9rooftops/9r-ai-skills.git
claude plugin install alc-dashboard@9r-ai-skills
claude plugin install rtp-casestudies@9r-ai-skills
```

For a local clone, pass its absolute path to `claude plugin marketplace add`.
Claude Code reads `.claude-plugin/marketplace.json`. Each plugin also has a
`.claude-plugin/plugin.json` manifest beside its Codex `plugin.json`.

## Use the dashboard skill

In a project containing your current meeting export, ask:

> Use the ALCOSAN municipal dashboard skill to create a dashboard from this
> Municipal Meeting Monitor CSV.

Provide the current CSV in the request. The skill writes results beneath the
project's `web/ALC-MeetingMonitorDashboard-YYYYMMDD/` folder. Reviewed event data
and PDF production follow the packaged skill's instructions. Keep client exports
and generated reports in the working project rather than this marketplace repo.

## Use the case-study skill

Install **9Rooftops Case Studies** from this marketplace, then provide a case brief
and supporting files:

> Use $rtp-casestudies to create a five-slide PowerPoint case study from this brief.

The skill defaults to a leave-behind that also supports live pitches. It uses
Georgia/Calibri typography, a shared story framework with controlled variants,
and client brand colors. Supplied files establish the work and results; limited
web lookup can establish official branding and general context. Missing or
conflicting claims become questions rather than invented proof.

The packaged Python 3 builder has no third-party dependencies. It produces native
editable PowerPoint text/shapes and stores sources in speaker notes. Native
PowerPoint or another compatible renderer is needed for final visual approval;
structural validation alone is explicitly reported as such. Original example
decks and the input brief remain in `plugins/rtp-casestudies/`.

## Add another skill

1. Create `plugins/<plugin-name>/plugin.json` with a unique kebab-case `name`,
   semantic `version`, description and author. Copy the existing plugin manifest
   as a starting point; adjust its local-execution setting to suit the new tool.
2. Create `plugins/<plugin-name>/.claude-plugin/plugin.json` with the same
   `name`, `version`, and `description`.
3. Put the skill in `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`. Keep its
   scripts, references and assets together, and use paths relative to the skill.
   The skill's frontmatter `name` must match its folder name.
4. Add the same plugin to all three catalogs. Use `./plugins/<plugin-name>` as
   the path in each one:
   - `.agents/plugins/marketplace.json` for Codex, with its installation policy
     and category.
   - `.grok-plugin/marketplace.json` for Grok, with `"type": "local"`.
   - `.claude-plugin/marketplace.json` for Claude Code, with the path as a string.
5. Add every packaged skill to `.grok-plugin/plugin-index.json`, using the
   skill folder name and the `SKILL.md` description. One plugin may bundle
   multiple closely related skills.
6. Run `python3 scripts/validate_marketplace.py` from the repository root and
   smoke-test the skill in its actual client with representative input.
7. Commit and push the reviewed files. Teammates refresh the marketplace and
   install the new plugin when they need it.

Increment a plugin's version when publishing changes. Include required assets
but exclude generated reports, runtime environments and dependency trees. Keep
runtime dependencies outside the installed plugin package; npm-created symlinks
inside a plugin can trigger Codex's unsupported-entry error. If a future hook
needs runtime storage, use the host's writable plugin data location rather than
modifying the installed package.

## Layout

```text
.agents/plugins/marketplace.json          # Codex
.grok-plugin/marketplace.json             # Grok
.grok-plugin/plugin-index.json            # Grok browse catalog
.claude-plugin/marketplace.json           # Claude Code
plugins/
  alc-dashboard/
    plugin.json
    .claude-plugin/plugin.json
    skills/alcosan-municipal-dashboard/
      SKILL.md
      scripts/build_dashboard.py
      assets/dashboard.html
      references/data-rules.md
scripts/validate_marketplace.py
```

Codex uses OpenAI's repo-scoped catalog. See the
[OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).
Grok reads `.grok-plugin/marketplace.json`. Claude Code reads
`.claude-plugin/marketplace.json`. The validator rejects a plugin or skill that
is missing from any of them.

