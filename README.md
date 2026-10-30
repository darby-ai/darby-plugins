# darby plugins for Claude Code

A Claude Code plugin marketplace with one plugin, `darby`. It registers the
remote darby MCP server (HTTP transport) and adds a short skill describing how
to use it. Claude Code handles the OAuth sign-in and keeps the tokens locally.

## Use it

In Claude Code:

1. Add the marketplace:

   ```text
   /plugin marketplace add darby-ai/darby-plugins
   ```

2. Install the plugin:

   ```text
   /plugin install darby@darby-plugins
   ```

   Choose a scope when prompted (user scope is the usual choice).

3. Sign in: run `/mcp`, select the darby server (shown as `plugin:darby:darby`), and authenticate in the browser.

The same steps from a shell:

```bash
claude plugin marketplace add darby-ai/darby-plugins
claude plugin install darby@darby-plugins
```

Then run `/mcp` inside Claude Code to sign in. In a session, call the
`read_client_guide` tool first; the `darby` skill reminds Claude to do this.

## Update

```bash
claude plugin marketplace update darby-plugins
claude plugin update darby@darby-plugins
```

Then run `/reload-plugins` in an open session.

## Sign out

Run `/mcp`, select the darby server (shown as `plugin:darby:darby`), and choose
**Clear authentication**, or run `claude mcp logout plugin:darby:darby`.

## Uninstall

```bash
claude plugin uninstall darby@darby-plugins
claude plugin marketplace remove darby-plugins
```

## Notes

The server entry sets a pre-registered OAuth client id and a fixed callback
port (`oauth.clientId`, `oauth.callbackPort`) so the sign-in matches the
server's registered redirect URI.

## Development

`python3 tests/check_plugin.py` runs offline checks on the manifests.
Sources for the manifest formats are in `docs/SOURCES.md`.

Licensed under Apache-2.0.
