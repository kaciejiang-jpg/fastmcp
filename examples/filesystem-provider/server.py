"""Filesystem-based MCP server using FileSystemProvider.

This example demonstrates how to use FileSystemProvider to automatically
discover and register tools, resources, and prompts from the filesystem.

Run:
    fastmcp run examples/filesystem-provider/server.py

Inspect:
    fastmcp inspect examples/filesystem-provider/server.py

Dev mode (re-scan files on every request):
    Change reload=True below, then modify files while the server runs.
"""

"""提供器会递归扫描目录下所有py文件；
只要函数带对应装饰器就自动注册；文件夹只是用来分类，
装饰器决定它是工具/资源/提示词"""

from pathlib import Path

from fastmcp import FastMCP
from fastmcp.server.providers import FileSystemProvider

# The provider scans all .py files in the directory recursively.
# Functions decorated with @tool, @resource, or @prompt are registered.
# Directory structure is purely organizational - decorators determine type.
provider = FileSystemProvider(
    root=Path(__file__).parent / "components",
    reload=True,  # 开发模式，每次客户端调用工具的时候，重新扫描一遍 components 下面的文件，改代码不用重启服务
)

mcp = FastMCP("FilesystemDemo", providers=[provider])  #把这个扫描器挂载给FastMCP实例，让服务启动时走这个扫描逻辑
