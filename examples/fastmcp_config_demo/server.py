"""
Example server demonstrating fastmcp.json configuration.

This server previously would have used the deprecated dependencies parameter:
    mcp = FastMCP("Demo Server", dependencies=["pyautogui", "Pillow"])

Now dependencies are declared in fastmcp.json alongside this file.
"""

import io   # 提供I/O流抽象接口的标准库；io.BytesIO 在内存中操作二进制字节（图片、音频、压缩包等），io.StringIO 在内存中操作字符串文本
#内存版临时文件，用来给数据套上文件接口，不落盘，用来中转数据

from fastmcp import FastMCP  #用于快速开发MCP的python框架
from fastmcp.utilities.types import Image  # FastMCP内置图片类型，MCP协议标准图片对象

# Create server - dependencies are now in fastmcp.json
mcp = FastMCP("Screenshot Demo")  #定义一个mcp实例


@mcp.tool  
def take_screenshot() -> Image:  
    """
    Take a screenshot of the user's screen and return it as an image.

    Use this tool anytime the user wants you to look at something on their screen.
    """
    import pyautogui  # 图形自动化库，实现屏幕截图、键鼠控制；函数内懒加载，仅调用工具时导入

    buffer = io.BytesIO()  #定义一个局部变量做内存空盒，专门存放字节

    # Capture and compress the screenshot to stay under size limits
    screenshot = pyautogui.screenshot()
    screenshot.convert("RGB").save(buffer, format="JPEG", quality=60, optimize=True)
    #convert颜料模式（RGB去透明度，RGBA）、save（将图片有损压缩成JPEG格式，质量60 、optimize＝true体积再压缩（不损画质），得到的JPEG格式的字节流存到buffer当中）

    return Image(data=buffer.getvalue(), format="jpeg")  #重新包装成mcp认识的图片


@mcp.tool
def analyze_colors() -> dict:
    """
    Analyze the dominant colors in the current screen.

    Returns a dictionary with color statistics from the screen.
    """
    import pyautogui
    from PIL import Image as PILImage  #as？开头已导入过一个image，同样名称会矛盾，故起个别名

    screenshot = pyautogui.screenshot()
    # Convert to smaller size for faster analysis
    small = screenshot.resize((100, 100), PILImage.Resampling.LANCZOS)   #（大小（长，宽），缩小算法）

    # Get colors
    colors = small.getcolors(maxcolors=10000)  #计算小图中每种颜色 出现的次数，返回一个列表，列表元素是元组（出现次数，颜色值），颜色值是一个三元组（R,G,B）
    if not colors:
        return {"error": "Too many colors to analyze"}  #保险检查，预判颜色过多的错误，避免代码直接崩溃

    # Sort by frequency
    sorted_colors = sorted(colors, key=lambda x: x[0], reverse=True)[:10]
    #                        ↑             ↑                 ↑        ↑ 
#                      要排序的列表     "按什么排序"的规则     降序   只取前十个
    return {
        "top_colors": [
            {"count": count, "rgb": color} for count, color in sorted_colors  #循环遍历 `sorted_colors` 里的每一个元组 `(count, color)`
        ],   #每一轮循环生成一个字典：{"count": 次数, "rgb": 颜色}
        "total_pixels": sum(c[0] for c in colors),
    }  #遍历原始 `colors`，取出每一项的 `c[0]`（次数），全部相加，得到图片统计的总像素数。


if __name__ == "__main__":
    import asyncio

    asyncio.run(mcp.run_async())  #好比是计划书和实施者
    #`asyncio.run(...)`：启动异步环境，执行这个MCP服务任务，让服务一直运行、持续接收消息
    #`mcp.run_async()`：异步任务，功能是开启MCP服务，等待客户端连接、调用截图/分析颜色工具