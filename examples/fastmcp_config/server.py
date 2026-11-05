"""Example FastMCP server for demonstrating fastmcp.json configuration."""

from fastmcp import FastMCP

# Create the FastMCP server instance
mcp = FastMCP("Config Example Server")


@mcp.tool   #MCP工具，客户端可以主动调用执行，带参数、有返回，用来做动作（echo 回显、add 计算）
def echo(text: str) -> str:   #参数类型为字符串
    """Echo the provided text back to the user."""
    return f"You said: {text}"


@mcp.tool
def add(a: int, b: int) -> int:  #参数类型为整数
    """Add two numbers together."""
    return a + b

 #MCP资源，客户端是读取获取内容，没有入参，用来读取一段信息、配置、文档，不是执行动作
@mcp.resource("config://example")   #`config://` 是自定义协议前缀，`example` 是资源标识，相当于这个资源的唯一地址，客户端就靠这个地址定位要读取哪一份资源。
#你还可以写别的，比如 `file://xxx`、`info://version`。

def get_example_config() -> str:  
    """Return an example configuration."""
    return """
    This server is configured using fastmcp.json.
    
    The configuration file specifies:
    - Python version
    - Dependencies
    - Transport settings
    - Other runtime options
    """


# This allows the server to run with: fastmcp run server.py
if __name__ == "__main__":
    import asyncio

    asyncio.run(mcp.run_async())
