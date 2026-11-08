# 外部审阅实际可用性（2026-11-08）

## Claude

- 命令：`/opt/homebrew/bin/claude`，`claude --version`返回`2.1.241 (Claude Code)`。
- 本地设置报告默认模型名`claude-opus-5[1m]`；设置含自定义网关。本记录只确认CLI调用与实际返回，不独立验证网关后端模型身份。
- 阶段1调用使用`claude -p --tools '' --no-session-persistence --output-format json`，完整输入留在`claude_stage1_prompt.txt`，输出留在`claude_stage1_result.json`，调用返回成功（`is_error=false`、`num_turns=1`）；可读版为`claude_stage1_review.md`。禁用工具，仅审查输入中的基准保护与章节重构计划，不把它记为原文核查或全文终审。

## DeepSeek Harness

- `command -v deepseek`、`command -v harness`未找到可执行文件。
- 当前注册工具名称与描述中无DeepSeek/Harness接口。
- 在项目、`~/.codex`、`~/.claude`及常见配置目录中按`deepseek`/`harness`文件名检索未发现调用入口；未读取或输出密钥。
- 因未发现实际可调用入口，本轮DeepSeek Harness独立学术审查未完成。Codex自检和Claude调用不能冒充该项审查。

## Claude阶段2

实际调用已返回，`is_error=False`、`num_turns=1`。完整正文、canon/argument_map、几何/GPU证据摘要及原9公式与表3/4均随输入提供；输出`claude_stage2_result.json`及可读版`claude_stage2_review.md`。本轮审查源稿快照以`claude_stage2_prompt.txt`和manifest锁定，后续修订由Codex逐项处置，未提供的论文仍无独立全文核查。

## Claude最终定向复核

实际调用已返回，`is_error=False`、`num_turns=1`。输入47,334字符，包含当前第4/5/6章、2章MOC积分约定、全部13公式、阶段2真实意见、保护比较、69项矩阵摘要及应用证据。原始输出`claude_final_result.json`，可读版`claude_final_review.md`，源稿及输入哈希见`claude_final_manifest.json`。本轮不是PDF逐页排版审核，亦不能补足未提供的论文全文核验。
