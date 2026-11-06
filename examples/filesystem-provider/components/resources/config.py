"""Configuration resources - static and templated."""

import json

from fastmcp.resources import resource


# Static resource - no parameters in URI  
 #静态资源（无参数URI->URI地址是写好的，没有{变量名}这种占位符，读取它的时候，不需要额外传任何参数）
@resource("config://app") 
#URI：MCP里面用来唯一标记一个资源的“地址”，类似于网址的作用，但不一定是互联网网址
#URL：是URI的一种，是能在浏览器打开的网络地址
def get_app_config() -> str:
    """Get application configuration."""
    return json.dumps(
        {
            "name": "FilesystemDemo",
            "version": "1.0.0",
            "features": ["tools", "resources", "prompts"],
        },
        indent=2,  #将 Python 字典转换成 JSON 字符串
    )


# Resource template - {env} is a parameter
#模板资源（带占位符参数 `{env}`，客户端读取的时候，把占位替换成具体值）
@resource("config://env/{env}")  
def get_env_config(env: str) -> str:
    """Get environment-specific configuration.

    Args:
        env: Environment name (dev, staging, prod).
    """
    configs = {
        "dev": {"debug": True, "log_level": "DEBUG", "database": "localhost"},
        "staging": {"debug": True, "log_level": "INFO", "database": "staging-db"},
        "prod": {"debug": False, "log_level": "WARNING", "database": "prod-db"},
    }
    config = configs.get(env, {"error": f"Unknown environment: {env}"})
    return json.dumps(config, indent=2)


# Resource with custom metadata
@resource(
    "config://features",
    name="feature-flags",
    mime_type="application/json",
    tags={"config", "features"},
)
def get_feature_flags() -> str:
    """Get feature flags configuration."""
    return json.dumps(
        {
            "dark_mode": True,
            "beta_features": False,
            "max_upload_size_mb": 100,
        },
        indent=2,
    )
