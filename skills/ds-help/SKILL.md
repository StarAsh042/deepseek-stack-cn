---
name: ds-help
description: "为任务挑出合适的 deepseek-stack-cn 技能，并讲清整套技能包如何配合。当用户问该用哪个技能、技能包里有什么，或输入 /ds-help 时使用。"
---

# ds-help

把任务匹配到一个技能，用一句话说明原因，然后执行它。

## 选择技能

| 如果任务是…… | 使用 |
|---|---|
| 任何编码任务（始终开启） | ds-mode |
| 目标模糊或风险高 | ds-sharpen，然后 ds-plan-loop |
| 涉及多个文件或步骤 | ds-plan-loop |
| 新模块或新的 API 形态 | ds-blueprint |
| 任何代码改动 | ds-verify-loop |
| 有低成本测试切入点的 bug | ds-tdd |
| 同一个故障出现两次 | ds-unstick |
| 长时间运行或上下文已满 | ds-context-reset、ds-ledger |
| 一次尝试可能做不对的高难产物 | ds-best-of-n |
| 大范围覆盖、审计或竞速 | ds-swarm |
| 合并前的评审 | ds-review-loop，或需要多个模型时用 ds-jury |
| 高风险的改动 | ds-blast-radius |
| 新的 UI | ds-design |
| 看起来千篇一律的 UI | ds-design-audit |
| 开 PR | ds-pr |
| 关注 CI 与机器人 | ds-watch-pr |
| 无人值守地把改动做到 PR 合并 | ds-ship |
| 同上，但在合并前停下 | ds-ready |
| 别人的 PR 或分支 | ds-adopt |
| 陈旧的 PR | ds-revive |
| 理解代码 | ds-explain |
| 长时间运行后回来接手 | ds-catchup |
| agent 反复犯错 | ds-lessons |
| 写叙述性文字或文档 | ds-unslop |
| 经验法则 | ds-principles |

## 规则

- 只推荐一个技能。只有当任务明显分两个阶段时，才点出第二个。
- 若没有合适的技能，就如实说明，并只用 ds-mode 继续工作。
