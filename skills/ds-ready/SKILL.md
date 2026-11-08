---
name: ds-ready
description: "执行完整的 ds-ship 流程，但停在 PR 已备好、可供人工 merge 的状态，绝不自行 merge。当用户说「把它准备好」「让它可合并」「在合并前停下」，或输入 /ds-ready 时使用。"
---

执行 `ds-ship` 的全部步骤，唯独不做 merge。把通过合并门禁、仍开放的 PR 交给用户。

该请求授予与 `ds-ship` 相同的 test 权限：可以 commit、push、rebase，并对本任务分支使用 `--force-with-lease`。但不得 merge。

## 步骤

1. 阅读 `ds-ship`，按其第 1 到 6 步执行：建分支、改动、验证、评审、提交、观察。
2. 首次 push 前，关闭 auto-merge，并把 PR 从任何 merge queue 中移出。每次 push 前再检查一遍。若无法阻止自动 merge，先报告再继续。
3. 最后一次修复后，重新验证任何行为变更和非平凡的冲突处理。
4. 拉取基线分支。读取线上 PR：head SHA、base、checks、reviews、mergeable state。确认它处于开放状态且不是 draft。
5. 套用 `ds-ship` 的合并门禁并选定一种判定：
   - **Ready**：门禁通过。保持 PR 开放。
   - **Waiting on approval**：只缺必需的人工审批。确认这就是真正的阻塞点。
   - **Blocked**：说明是什么卡住、你试过什么、还需要什么。
6. 报告 PR 链接、最终 head SHA、判定、验证依据、评审结果和剩余风险。明确说明 PR 仍开放且未 merge。

## 停止条件

- 得出三种判定之一，且报告已写好。
- PR 被他人 merge 了。报告这一情况。
- 连续 6 次修复并观察的循环后门禁仍未变绿。报告 Blocked。

## 规则

- 绝不 merge、开启 auto-merge、加入 merge queue，也不向默认分支 push。
- 也不要让其他 agent 代你做上述任何一件事。
- 为判定给出证据：你读到的 check 列表和 mergeable state。
