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

```对于components里面文件：
resource：
资源函数仅读取内容、不修改数据，返回内容供主服务加载，控制服务行为。
包含三类资源：静态资源、配置资源、模板资源。
配置资源用于区分开发、测试、生产环境，本地开发开启调试与详细日志方便排错；预发布环境模拟线上环境做验收；生产环境关闭调试、精简日志，保障线上稳定性与数据安全，同时隔离不同环境的数据库资源：
开发环境开启调试、详细日志，便于排错；预发布环境复刻线上用于验收；
生产环境关闭调试、压缩日志，保障稳定性与数据安全，各环境数据库相互隔离。


prompts:
预制好的提示词模板，用来快速生成一段发给大模型的文字指令。它本身不执行代码、不运算、不读取文件，只负责拼接文本。
注意！！
- tags、name：用来给客户端做管理、分类、检索、展示，是「目录标签」；
- 函数return出来的字符串：才是真正送到大模型手里的提示词，是给AI看的正文。


tools：
用来注册可执行的功能工具，支持自定义对外名称、描述和标签；
标签用来给客户端分类检索工具，只有带上 @tool装饰器的函数才会暴露给MCP客户端，普通辅助函数不会被外部调用；
tool会运行代码算出结果。


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

