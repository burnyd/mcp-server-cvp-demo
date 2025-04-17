# MCP-Server-Demo

This is a quick demo of what is possible within MCP and Cloudvision portal.  This can be further found on my blog if interested at danielhertzberg.net

### To make this run

Please add a .env file like the following.

```bash
CVPTOKEN="Somesupersecuretoken"
CVP="www.arista.io"
```

Afterwards please add it to Claude desktop for example.

```json
{
  "mcpServers": {
    "CVP MCP Server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "/mcp-server-cvp-demo/secondmcpserver.py"
      ]
    }
  }
}
```
