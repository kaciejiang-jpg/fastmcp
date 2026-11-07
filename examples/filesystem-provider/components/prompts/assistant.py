"""Assistant prompts."""

from fastmcp.prompts import prompt


@prompt
def code_review(code: str, language: str = "python") -> str:
    """Generate a code review prompt.

    Args:
        code: The code to review.
        language: Programming language (default: python).
    """
    return f"""Please review this {language} code:

```{language}
{code}
```

Focus on:
- Code quality and readability  #代码质量和可读性
- Potential bugs or issues    #潜在问题
- Performance considerations  #性能
- Best practices   #开发规范 
"""  
#传入一段代码 + 语言，自动拼好一段代码审查的prompt，让大模型帮你审代码。
#你传给它 `code="xxx"`，它输出一整段带代码块的评审指令
#只是拼接文字，不会自己去分析代码，文字交给客户端，再发给大模型执行评审

@prompt(
    name="explain-concept",  #给MCP客户端看的对外名字
    description="Generate a prompt to explain a technical concept.",
    tags={"education", "explanation"},  #标签，用来分类，客户端可以按标签筛选 prompt。
)
def explain(topic: str, audience: str = "developer") -> str:  #Python函数名，写代码的时候、在Python内部用的
    """Generate an explanation prompt.

    Args:
        topic: The concept to explain.
        audience: Target audience level.
    """
    return f"Explain {topic} to a {audience}. Use clear examples and analogies."
# 输入一个技术主题、听众身份，返回一句指令：让大模型用适合这个听众的方式讲明白这个知识点，还要举例子类比。