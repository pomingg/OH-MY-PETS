"""
LLM 推理引擎 - 地端部署與雲端兜底混合架構

模組概覽：
  - engine/: Text-to-SQL 引擎核心
  - safety/: 五層安全防護
  - schema/: Schema 精簡與描述
  - prompts/: Prompt 範本
  - config/: 配置管理
"""

__version__ = "1.0.0"
__author__ = "毛孩生活科技 AI 小組"

from .engine import SmartSQLGenerator
from .safety import SafeSQLExecutor

__all__ = [
    "SmartSQLGenerator",
    "SafeSQLExecutor",
]
