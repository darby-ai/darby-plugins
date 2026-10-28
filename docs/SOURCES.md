# Sources

Official Claude Code docs, read 2026-10-28 (Claude Code CLI 2.1.285 on the build host).
Allowed docs domain: code.claude.com

| Page | URL | Used for |
| :- | :- | :- |
| Plugins overview | https://code.claude.com/docs/en/plugins | plugin model, `/plugin` flow, `<plugin>:<skill>` namespacing |
| Plugin manifest reference | https://code.claude.com/docs/en/plugins-reference | `plugin.json` fields (`name` only required; `author.name` required if author set), `.mcp.json` at plugin root, standard layout, `${CLAUDE_PLUGIN_ROOT}`, `claude plugin validate` |
| Create a marketplace | https://code.claude.com/docs/en/plugin-marketplaces | `marketplace.json` requires `name`, `owner`, `plugins`; entry needs `name`, `source` (relative path from marketplace root) |
| Install and manage plugins | https://code.claude.com/docs/en/plugins/install.md | `/plugin marketplace add` sources (GitHub `owner/repo`, git URL, local path), `/plugin install name@marketplace`, update, uninstall, marketplace remove |
| Skills | https://code.claude.com/docs/en/skills | `skills/<name>/SKILL.md`, frontmatter `name`, `description` |
| MCP | https://code.claude.com/docs/en/mcp | remote HTTP servers (`type: http`), `/mcp` OAuth, `oauth.clientId` / `oauth.callbackPort` in `.mcp.json`, `claude mcp add --client-id --callback-port`, Clear authentication, `claude mcp logout <name>` |

## UNVERIFIED

- The MCP page documents `"oauth": {"clientId", "callbackPort"}` for `.mcp.json` entries
  and says plugins define servers in `.mcp.json` at the plugin root, but it does not state
  that the `oauth` object is honored for plugin-bundled servers. It is included on the
  basis that the plugin `.mcp.json` uses the same entry format. Needs a real sign-in test.
- Whether the OAuth client id `bf-gateway-cli` and port `33418` match the server's
  registration (taken from the owner-verified `claude mcp add` command line, not from docs).
- Tool name `read_client_guide` comes from the task brief, not from any doc.
- The marketplace name `darby-plugins` is our choice; the docs only require a unique name
  that is not reserved.
