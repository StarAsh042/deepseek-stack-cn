# deepseek-stack-cn

让 DeepSeek 模型（V4.1 Flash、V4 Pro）表现得像一个昂贵得多的模型。便宜模型翻车的方式往往就那么几种：跳过计划、没跑就说修好了、反复重试同一个坏思路、长任务里逐渐跑偏。这里的每个技能都用一个短循环、一个硬性停止条件和「拿真实证据来」的要求，补上其中一个缺口。

任何会读取 `SKILL.md` 文件的 harness 都能用：Claude Code、Codex、Cline、OpenCode、PandaCode 等。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 安装

```bash
npx skills add StarAsh042/deepseek-stack-cn
```

加 `-g` 可为所有项目安装。只安装单个技能：

```bash
npx skills add StarAsh042/deepseek-stack-cn --skill ds-verify-loop
```

手动安装：把 `skills/*` 复制到 `~/.claude/skills/`、`~/.codex/skills/` 或你所用 harness 的 skills 目录。

不知道从哪开始？运行 `/ds-help`。

## 技能列表

### 核心

| 技能 | 作用 |
|---|---|
| `ds-mode` | 始终开启的工作方式：先复述、先读、小步验证、有证据才说「完成」。 |
| `ds-principles` | 21 条工程经验法则，每条都带触发条件。 |
| `ds-help` | 为任务挑对技能。 |

### 循环

| 技能 | 作用 |
|---|---|
| `ds-plan-loop` | 每步都检查的计划，用全新的一轮做一次批判，然后一次只做一步。 |
| `ds-verify-loop` | 改代码、跑真检查、读真报错、修根因。最多 5 轮。 |
| `ds-unstick` | 同一处失败两次：点出共同假设、验证它、换一条路。 |
| `ds-context-reset` | 维护一份 `PROGRESS.md`，任务变长时换到全新上下文继续。 |
| `ds-ledger` | 长任务或无人值守任务里一条决策一行，每步前重读一遍。 |
| `ds-review-loop` | 作者与全新上下文的评审者轮流来，直到双方一致。最多 4 轮。 |
| `ds-jury` | 由两三个不同模型评审，直到意见一致。 |
| `ds-best-of-n` | N 个并行尝试，挑最好的，把其余里出彩的部分嫁接进来。 |
| `ds-swarm` | 把并行 worker 铺开，再把结果汇成一份报告。 |

### 构建

| 技能 | 作用 |
|---|---|
| `ds-sharpen` | 复述目标、把任务挖深、重写 prompt。 |
| `ds-blueprint` | 先定类型、签名和模块布局，再实现。 |
| `ds-tdd` | 先写一个失败的测试，再做最小的修复。 |
| `ds-blast-radius` | 找出改动在 diff 之外可能弄坏什么，并证明它是安全的。 |
| `ds-design` | 做有明确视觉方向的前端，而不是千篇一律的 AI 味。 |
| `ds-design-audit` | 用证据给现有 UI 打分，修掉最要紧的问题，再复检。 |

### 交付

| 技能 | 作用 |
|---|---|
| `ds-pr` | 提交一份以问题开头的简短 PR。 |
| `ds-watch-pr` | 盯着 CI 和评审机器人，修真正的问题。 |
| `ds-ship` | 从改动一路到合并 PR，全程无人值守。 |
| `ds-ready` | 与 `ds-ship` 相同，但在合并前停下。 |
| `ds-adopt` | 完成别人的 PR 或分支，并保留他们的署名。 |
| `ds-revive` | 给旧 PR rebase，或判断它该被关掉。 |
| `ds-pr-comments` | 规范 agent 代你发出的评论格式。 |

### 理解

| 技能 | 作用 |
|---|---|
| `ds-explain` | 用大白话讲清代码怎么工作、为什么这么写。 |
| `ds-catchup` | 你不在时发生了什么，以及有哪些事在等你。 |
| `ds-lessons` | 把 agent 反复犯的错变成类型、lint 或测试。 |
| `ds-unslop` | 去掉散文和注释里的 AI 腔。 |

## 使用 DeepSeek 的建议

- 规划和评审开到最大思考强度。这比任何技能都管用。
- 大任务放到低峰时段跑，API 价格更便宜。
- DeepSeek 很便宜，把 token 花在质量上：`ds-best-of-n`、`ds-review-loop` 和 `ds-jury` 花不了多少，却能兜住很多问题。
- 如果你的 harness 支持把规划与执行模型分开，就用更强的规划器搭配 DeepSeek 当执行者。

## 环境要求

- `gh`（GitHub CLI）并已登录，供交付类技能使用。
- `python3`，供 `ds-watch-pr/scripts/watch_pr.py` 使用。
- `ds-jury`、`ds-best-of-n` 和 `ds-swarm` 需要 subagent 或第二个模型；没有的话，这些技能会在全新上下文里逐个串行跑尝试。

## 许可证

本项目采用 MIT 许可证 [LICENSE](LICENSE)。

[![](https://img.shields.io/badge/powered_by-dsh-4D6BFE?style=flat-square&logo=deepseek&logoColor=white)](https://github.com/deepseek-ai/deepseek-harness)
