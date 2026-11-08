#!/usr/bin/env python3
"""盯守一个 GitHub PR，每出现一条新事件就打印一行。需要 gh CLI。

用法：watch_pr.py <pr> [--repo owner/name] [--until green|ready|any] [--interval 30] [--max-minutes 60]

退出码：
  0  满足 --until 条件，或 PR 已合并
  1  需要人工处理：检查失败、存在冲突、被要求修改、PR 已关闭、
     gh 持续报错，或已到时间上限
  2  参数错误或找不到该 PR
"""
import argparse
import json
import subprocess
import sys
import time

FIELDS = "state,mergeable,mergeStateStatus,reviewDecision,headRefOid,statusCheckRollup,comments,reviews,url"
FAILED = {"FAILURE", "ERROR", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED", "STARTUP_FAILURE"}
PASSED = {"SUCCESS", "NEUTRAL", "SKIPPED"}
MAX_GH_ERRORS = 5


def fetch(pr, repo):
    cmd = ["gh", "pr", "view", pr, "--json", FIELDS] + (["--repo", repo] if repo else [])
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or "gh 调用失败")
    return json.loads(out.stdout)


def check_result(c):
    # CheckRun 有 status/conclusion；StatusContext 有 state。
    if c.get("__typename") == "StatusContext":
        state = c.get("state", "")
        return "PENDING" if state in ("PENDING", "EXPECTED") else state
    if c.get("status") != "COMPLETED":
        return "PENDING"
    return c.get("conclusion") or "PENDING"


def summarize(pr):
    checks = {(c.get("name") or c.get("context") or "?"): check_result(c) for c in pr.get("statusCheckRollup") or []}
    failed = sorted(n for n, r in checks.items() if r in FAILED)
    pending = sorted(n for n, r in checks.items() if r not in FAILED | PASSED)
    notes = {("comment", c.get("id") or c.get("url")): c for c in pr.get("comments") or []}
    notes.update({("review", r.get("id")): r for r in pr.get("reviews") or []})
    return {"checks": checks, "failed": failed, "pending": pending, "notes": notes}


def events(prev, cur):
    if prev is None:
        return []
    out = []
    for name in cur["failed"]:
        if name not in prev["failed"]:
            out.append(f"检查失败：{name}")
    if cur["checks"] and not cur["pending"] and prev["pending"]:
        out.append(f"检查结束：{len(cur['checks'])} 项中 {len(cur['failed'])} 项失败")
    for key, note in cur["notes"].items():
        if key not in prev["notes"]:
            who = (note.get("author") or {}).get("login", "?")
            body = " ".join((note.get("body") or "").split())[:120]
            out.append(f"新增 {key[0]}（来自 {who}）：{body}")
    return out


def outcome(pr, cur, until):
    """满足结束条件时返回 (exit_code, reason)，否则返回 None。"""
    if pr["state"] == "MERGED":
        return 0, "已合并"
    if pr["state"] == "CLOSED":
        return 1, "PR 已关闭"
    if cur["failed"]:
        return 1, "检查失败：" + ", ".join(cur["failed"])
    if pr.get("mergeable") == "CONFLICTING" or pr.get("mergeStateStatus") == "DIRTY":
        return 1, "与 base 分支存在冲突"
    if pr.get("reviewDecision") == "CHANGES_REQUESTED":
        return 1, "评审要求修改"
    green = not cur["pending"]
    if until == "green" and green:
        return 0, "检查全绿"
    if until == "ready" and green:
        if pr.get("mergeStateStatus") == "BEHIND":
            return 1, "分支落后于 base 分支"
        if pr.get("mergeStateStatus") in ("CLEAN", "HAS_HOOKS", "UNSTABLE"):
            return 0, "就绪：检查全绿且可合并"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="盯守一个 GitHub PR，直到满足指定条件。")
    ap.add_argument("pr")
    ap.add_argument("--repo")
    ap.add_argument("--until", choices=["green", "ready", "any"], default="ready")
    ap.add_argument("--interval", type=int, default=30)
    ap.add_argument("--max-minutes", type=int, default=60)
    a = ap.parse_args(argv)
    if a.interval < 5 or a.max_minutes < 1:
        ap.error("--interval 必须 >= 5，且 --max-minutes 必须 >= 1")

    deadline = time.time() + a.max_minutes * 60
    prev, errors = None, 0
    while time.time() < deadline:
        try:
            pr = fetch(a.pr, a.repo)
            errors = 0
        except (RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            errors += 1
            print(f"gh 报错（{errors}/{MAX_GH_ERRORS}）：{e}", file=sys.stderr)
            if prev is None and "Could not resolve" in str(e):
                return 2
            if errors >= MAX_GH_ERRORS:
                print("stop: gh 无法访问")
                return 1
            time.sleep(a.interval)
            continue
        cur = summarize(pr)
        new = events(prev, cur)
        for line in new:
            print(line, flush=True)
        if prev is None:
            print(f"正在盯守 {pr['url']} head {pr['headRefOid'][:8]}", file=sys.stderr)
        if a.until == "any" and new:
            return 0
        done = outcome(pr, cur, a.until)
        if done:
            print(f"stop: {done[1]}", flush=True)
            return done[0]
        prev = cur
        time.sleep(a.interval)
    print("stop: 已到时间上限")
    return 1


if __name__ == "__main__":
    sys.exit(main())
