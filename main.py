from colorama import Fore, Style, init
import ollama
import asyncio
import shlex
import json

from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

init(autoreset=True)

DEEPCODE_BANNER = r"""
________                                  .___
\______ \   ____   ____ ______   ____  ____ | _/____
 |    |  \_/ __ \_/ __ \\____ \_/ ___\/  _ \ / __ |/ __ \
 |    `   \  ___/\  ___/|  |_> >  \__(  <_> ) /_/ \___/
 /_______  /\___  >\___  >   __/ \___  >____/\____ |\___ >
         \/     \/     \/|__|        \/           \/    \/
"""


class MCPManager:
    def __init__(self):
        self.servers = {}

    async def connect(self, name, command, args=None):
        if name in self.servers:
            print(Fore.YELLOW + f"{name} is already connected.")
            return

        stack = AsyncExitStack()

        try:
            params = StdioServerParameters(
                command=command,
                args=args or [],
                env=None
            )

            read, write = await stack.enter_async_context(
                stdio_client(params)
            )

            session = await stack.enter_async_context(
                ClientSession(read, write)
            )

            await session.initialize()
            result = await session.list_tools()

            self.servers[name] = {
                "session": session,
                "tools": result.tools,
                "stack": stack
            }

            print(Fore.GREEN + f"Connected to {name}!")
            print(Fore.CYAN + f"Discovered {len(result.tools)} tools.")

        except Exception as error:
            await stack.aclose()
            print(Fore.RED + f"Connection failed: {error}")

    async def list_servers(self):
        if not self.servers:
            print(Fore.YELLOW + "No MCP servers connected.")
            return

        for name, server in self.servers.items():
            print(Fore.CYAN + f"\n{name}")
            print(f"Tools: {len(server['tools'])}")

    async def list_tools(self):
        if not self.servers:
            print(Fore.YELLOW + "No MCP servers connected.")
            return

        for name, server in self.servers.items():
            print(Fore.CYAN + f"\n{name}")

            for tool in server["tools"]:
                print(Fore.GREEN + f"  {tool.name}")
                if tool.description:
                    print(f"    {tool.description}")

    async def call_tool(self, server_name, tool_name, arguments):
        server = self.servers.get(server_name)

        if not server:
            print(Fore.RED + "Server not found.")
            return

        available = {tool.name for tool in server["tools"]}

        if tool_name not in available:
            print(Fore.RED + "Tool not found.")
            return

        try:
            result = await server["session"].call_tool(
                tool_name,
                arguments=arguments
            )

            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)
                else:
                    print(item)

            if result.isError:
                print(Fore.RED + "The MCP tool reported an error.")

        except Exception as error:
            print(Fore.RED + f"Tool execution failed: {error}")

    async def disconnect(self, name):
        server = self.servers.get(name)

        if not server:
            print(Fore.YELLOW + "Server not found.")
            return

        try:
            await server["stack"].aclose()
        finally:
            del self.servers[name]

        print(Fore.GREEN + f"Disconnected {name}.")

    async def disconnect_all(self):
        for name in list(self.servers.keys()):
            await self.disconnect(name)


async def main():
    mcp = MCPManager()

    print(Fore.CYAN + DEEPCODE_BANNER + Style.RESET_ALL)

    try:
        while True:
            try:
                prompt = input(Fore.CYAN + "\nDeepcode > ").strip()

                if prompt.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break

                if not prompt:
                    continue

                if prompt.lower() == "/mcp" or prompt.lower().startswith("/mcp "):
                    parts = shlex.split(prompt)

                    if len(parts) == 1:
                        print(Fore.CYAN + """
MCP MANAGER
--------------------------------
/mcp connect <name> <command> [args]
/mcp disconnect <name>
/mcp disconnect all
/mcp list
/mcp tools
/mcp call <server> <tool> <json>
--------------------------------
""")

                    elif parts[1] == "connect":
                        if len(parts) < 4:
                            print("Usage: /mcp connect <name> <command> [args]")
                        else:
                            await mcp.connect(
                                parts[2],
                                parts[3],
                                parts[4:]
                            )

                    elif parts[1] == "list":
                        await mcp.list_servers()

                    elif parts[1] == "tools":
                        await mcp.list_tools()

                    elif parts[1] == "disconnect":
                        if len(parts) < 3:
                            print("Specify a server name or 'all'.")
                        elif parts[2] == "all":
                            await mcp.disconnect_all()
                        else:
                            await mcp.disconnect(parts[2])

                    elif parts[1] == "call":
                        if len(parts) < 5:
                            print('Usage: /mcp call <server> <tool> \'{"key":"value"}\'')
                        else:
                            try:
                                arguments = json.loads(" ".join(parts[4:]))
                                if not isinstance(arguments, dict):
                                    raise ValueError("Arguments must be a JSON object.")

                                await mcp.call_tool(
                                    parts[2],
                                    parts[3],
                                    arguments
                                )
                            except (json.JSONDecodeError, ValueError) as error:
                                print(Fore.RED + f"Invalid arguments: {error}")

                    else:
                        print(Fore.RED + "Unknown MCP command.")

                    continue

                response = ollama.chat(
                    model="deepseek-coder:6.7b",
                    messages=[{"role": "user", "content": prompt}],
                )

                print(Fore.RED + response["message"]["content"])

            except KeyboardInterrupt:
                print("\nUse 'exit' to close Deepcode.")
            except Exception as error:
                print(Fore.RED + f"Error: {error}")

    finally:
        await mcp.disconnect_all()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
