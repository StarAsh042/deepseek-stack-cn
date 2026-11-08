---
name: ds-review-loop
description: "让作者与全新上下文的评审者围绕当前改动循环评审，直到双方一致认为正确，最多 4 轮。在提交 PR 之前或之后，当用户说「评审循环」「找人评审一下」，或输入 /ds-review-loop 时使用。"
---

让一位全新上下文的评审者不断提出质疑，直到双方达成一致，从而把改动打磨得更正确。

## 步骤

1. 界定改动范围。运行 `git status --short`。不要 stash、丢弃或纳入无关文件。找到基线：`git fetch origin`，再执行 `git merge-base HEAD origin/<base branch>`。每一轮都用同一条 diff 命令。
2. 用 2 句话写下目标和范围外清单。运行覆盖性检查。不要发送未通过检查的代码。
3. 选定评审者：若 harness 能调用更强的模型（带 model 设置的 subagent、团队 worker、第二个 CLI），就用它；否则用无历史记录的全新 DeepSeek 上下文。记录选了哪一种。
4. 发送以下简报：

   ```
   只做评审。不要编辑文件、commit、push、发评论或启动 subagent。
   Repo: <path>  Base: <sha>  Diff: git diff <sha> [-- <paths>]
   Goal: <goal>  Out of scope: <list>  Checks: <results>
   读 diff 附近的代码，找出 bug、被改坏的调用方，以及与目标之间的差距。
   标出目标并不需要的代码。风格问题除非掩盖了 bug，否则一律忽略。
   blocker = 目标用例本身错了；should = 用户会实际遇到的 bug；nit = 其余一切。
   回复格式：VERDICT: APPROVE or CHANGES，随后每条发现一行：
   R1 [blocker|should|nit] file:line claim. Fix: suggestion
   ```

5. 等待回复。评审进行期间不要改动范围内的文件。超时或报错都不算通过。
6. 逐条自行判断。认同：做最小的修复，优先删除或收窄代码。不认同：附上证据回复（file:line、test 输出）。属于 nit 或超出范围：一句话回绝。
7. 维护一份台账：id、严重程度、处理结果、证据。重跑检查并执行 `git diff --shortstat`。若 diff 变大，就把它收回去。
8. 下一轮发送简报、台账以及自上一轮以来的改动。让评审者只检查未结的 id 和变动过的代码。

## 停止条件

- 评审者对当前 diff 返回 APPROVE，没有未结的 blocker 或 should，你也不再有疑虑。
- 某一轮只返回 nits。
- 完成 4 轮，或某一条在 2 轮往来后仍有争议。用各 2 到 3 行陈述双方理由，交由用户决定。这不等于通过。

## 规则

- 一次只用一位评审者。不要为了结束循环而勉强认同。
- 循环期间不要 push。只有用户要求 push 或 ship 时，才在循环结束后 push。
- 若更新了 PR，加上：`Reviewed with ds-review-loop: <N> rounds, <reviewer>, verdict <verdict>.`
- 报告轮数、评审者、已修复与已回绝的发现及理由，以及改动前后 diff 的大小。
