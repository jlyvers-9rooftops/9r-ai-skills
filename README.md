# 9R AI Skills

Shared AI skills for the 9R team, distributed through a Codex plugin marketplace.
Each plugin has its own directory and version so teammates can select the tools
they need as the catalog grows.

## Available plugins

| Plugin | Skill | Purpose |
| --- | --- | --- |
| `alc-dashboard` | `alcosan-municipal-dashboard` | Build ALCOSAN executive dashboards from Municipal Meeting Monitor CSV reports. |

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

## Use the dashboard skill

In a project containing your current meeting export, ask:

> Use the ALCOSAN municipal dashboard skill to create a dashboard from this
> Municipal Meeting Monitor CSV.

Provide the current CSV in the request. The skill writes results beneath the
project's `web/ALC-MeetingMonitorDashboard-YYYYMMDD/` folder. Reviewed event data
and PDF production follow the packaged skill's instructions. Keep client exports
and generated reports in the working project rather than this marketplace repo.

## Add another skill

1. Create `plugins/<plugin-name>/plugin.json` with a unique kebab-case `name`,
   semantic `version`, description and author. Copy the existing plugin manifest
   as a starting point; adjust its local-execution setting to suit the new tool.
2. Put the skill in `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`. Keep its
   scripts, references and assets together, and use paths relative to the skill.
3. Add a plugin entry to `.agents/plugins/marketplace.json`. Its `source.path`
   is relative to this repository root, such as `./plugins/my-new-tool`.
   Include the installation/authentication policy and category, following the
   existing entry. One plugin may bundle multiple closely related skills.
4. Run `python3 scripts/validate_marketplace.py` from the repository root and
   smoke-test the skill in its actual client with representative input.
5. Commit and push the reviewed files. Teammates refresh the marketplace and
   install the new plugin when they need it.

Increment a plugin's version when publishing changes. Include required assets
but exclude generated reports, runtime environments and dependency trees. Keep
runtime dependencies outside the installed plugin package; npm-created symlinks
inside a plugin can trigger Codex's unsupported-entry error. If a future hook
needs runtime storage, use the host's writable plugin data location rather than
modifying the installed package.

## Layout

```text
.agents/plugins/marketplace.json
plugins/
  alc-dashboard/
    plugin.json
    skills/alcosan-municipal-dashboard/
      SKILL.md
      scripts/build_dashboard.py
      assets/dashboard.html
      references/data-rules.md
scripts/validate_marketplace.py
```

The marketplace uses OpenAI's documented repo-scoped catalog and portable plugin
manifest formats. See the [official packaging and marketplace documentation](https://developers.openai.com/plugins/build/plugins).

