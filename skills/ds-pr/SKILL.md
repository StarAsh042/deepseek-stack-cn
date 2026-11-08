---
name: ds-pr
description: "为当前分支提交一份简短清晰的 PR。当用户要求开启、提交或创建 PR，或输入 /ds-pr 时使用。"
---

提交一个真实的 PR，让忙碌的评审者能在 10 秒内读完标题和描述。

## 步骤

1. 检查该分支是否已有 PR（`gh pr list --head <branch>`）。若已有，则更新它。
2. 将分支与基线（通常是 `origin/main`）对比，确认 diff 符合目标且不含无关内容。
3. 读几个最近已合并 PR 的标题，沿用其格式。
4. 标题要说明用户侧发生了什么变化、为何重要，而不是哪个函数被挪动。示例："Cut websocket frames by 70% with compression" 胜过 "Negotiate permessage-deflate"。
5. 按以下顺序撰写描述：
   - 问题：用 1 到 2 句平实的话，取自用户的请求。
   - 修复：1 到 2 句。
   - 若有验证依据，用一行说明如何证明。
   - 结尾一行：`Created with <model> in <harness>.`。使用 harness 报告的模型名；若未报告，只写 harness 名称。
6. 检查标题、正文和所有附件中是否含密钥、token、私有路径和个人数据，并删除。
7. 以可评审状态创建 PR，不要用 draft，以便评审机器人运行。
8. 打印 GitHub 返回的 PR URL。

## 停止条件

- GitHub 返回了 PR URL。若用户要求监听，转交 `ds-watch-pr`。
- `gh pr create` 失败 2 次。若错误是 GraphQL 限流，则改用 REST 重试 1 次：`gh api repos/<owner>/<repo>/pulls -f title=... -f head=... -f base=... -F body=@body.md`。若仍失败，报告错误。

## 规则

- 描述中不要逐文件罗列改动。
- 除非请求需要，否则不要追加后续评论；需要时使用 `ds-pr-comments`。
- 绝不猜测模型名。
