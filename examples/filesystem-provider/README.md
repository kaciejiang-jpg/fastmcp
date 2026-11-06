```text
filesystem-provider
├─ components
│  ├─ prompts              # 提示词模板，给AI加载一套固定人设
│  │  └─ assistant.py      # 提示词相关
├─ resources               # 只读资源，不执行操作（@mcp.resource）
│  └─ config.py            # MCP Resource资源
├─ tools                   # 存放MCP所有工具（@mcp.tool）
│  ├─ calculator.py        # 工具1：计算器
│  └─ greeting.py          # 工具2：问候
└─ server.py               # MCP服务主入口，创建FastMCP实例，把tool和resource全部注册进去
```

```注意：
工具不是在 server.py 里直接写的，引入的`FileSystemProvider` 是FastMCP的文件扫描自动加载器：
✅ 它会自动去 `components` 文件夹里面，递归扫所有 `.py` 文件
✅ 只要文件里的函数打上了 `@tool` / `@resource` / `@prompt`，就自动注册成 MCP 的工具，不用手动在 server.py 写 `@mcp.tool`
```


```text
整体运行流程：

1. 启动 `server.py`
2. server.py 导入tools下面所有工具、resources下面的资源、prompts里的提示词
3. 全部注册到同一个 FastMCP 服务实例
4. MCP 客户端连接这个服务之后：
   可以调用 tools 里的计算器、问候功能
   可以读取 resources 里的配置文档
   可以加载 prompts 里预设的助手提示词
```

