# 上游来源与本地取舍

- [mengke-wang/xiaohongshu-ai-workbench](https://github.com/mengke-wang/xiaohongshu-ai-workbench) 的 `xiaohongshu-comment-reply`：用于自然、克制、上下文相关的回复写作。
- [autoclaw-cc/xiaohongshu-mcp-skills](https://github.com/autoclaw-cc/xiaohongshu-mcp-skills) 的 `xhs-interact`：提供 `reply_comment_in_feed` 等实际互动接口约定。

本地合并版增加：通知页优先、已回复去重、住宿类默认跳过、发送前计划校验、逐条回读确认、超时不盲目重试，以及草稿/确认发送/自动发送三种授权模式。
