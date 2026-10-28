---
name: darby
description: Use when the user wants to work with darby or asks for darby's tools. Explains sign-in and the required first step, read_client_guide.
---

# Using darby

darby is a remote MCP server this plugin registers as the `darby` server.

## Sign in

1. Run `/mcp` in Claude Code, select `darby`, and choose to authenticate.
2. Finish the login in the browser window that opens.

Claude Code performs the OAuth sign-in and keeps the tokens on this machine.
Never ask the user to paste a token, password, or authorization code into the chat.

## Using the tools

1. Call the `read_client_guide` tool FIRST, before any other darby tool, and follow what it says.
2. Then use the other darby tools as the guide describes.

If a darby tool reports an authentication error, ask the user to sign in again through `/mcp`.

## Sign out

Run `/mcp`, select `darby`, and choose **Clear authentication**.
From a shell: `claude mcp logout darby`.
