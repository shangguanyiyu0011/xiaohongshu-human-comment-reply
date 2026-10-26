# 上游来源与版权

本项目是基于上游相关方法和接口约定的整合增强版。上游与本项目不存在官方隶属关系。

| 上游项目 | 使用来源 | 原许可与版权 |
| --- | --- | --- |
| [mengke-wang/xiaohongshu-ai-workbench](https://github.com/mengke-wang/xiaohongshu-ai-workbench) | `xiaohongshu-comment-reply` 的自然回复、置顶与讨论方法 | MIT；Copyright (c) 2026 王梦珂；[原许可全文](licenses/xiaohongshu-ai-workbench-LICENSE.txt) |
| [autoclaw-cc/xiaohongshu-mcp-skills](https://github.com/autoclaw-cc/xiaohongshu-mcp-skills) | `xhs-interact` 的评论读取与回复工具接口约定 | MIT；Copyright (c) 2026 Auto-Claw-CC；[原许可全文](licenses/xiaohongshu-mcp-skills-LICENSE.txt) |

原许可于 2026-10-26 从两个项目公开仓库的 `LICENSE` 文件核对并保留。相关文件仍受各自原许可约束。

本地增强包括：通知页入口、已回复去重、默认筛选、发送前计划校验、单一浏览器会话约定、发送后回读、结果不明时先核实，以及草稿／确认发送／范围内自动发送三种模式。

本次公开整理新增通用安装说明、虚构 JSON 示例与回归测试；校验器增加严格字段类型检查和非法编码错误处理，并修正过时的浏览器交接测试断言。真实评论、账号状态与任务日志未纳入公开包。
