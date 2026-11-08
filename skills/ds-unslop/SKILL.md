---
name: ds-unslop
description: "清除散文和代码注释里的 AI 写作痕迹，然后用简明、具体的英文重写。适用于撰写或修改回复、文档、README、PR 描述、commit message 或注释时，或当用户键入 /ds-unslop 时。"
---

# 去掉 AI 腔

起草时就写干净。然后对照这些痕迹逐条排查并重写。保留原意与语气。

## 需要清除的痕迹

用词
- 浮夸词汇：delve、crucial、pivotal、robust、seamless、leverage、utilize、showcase、underscore、tapestry、landscape、testament、vibrant、intricate。改用朴素的词。
- "Serves as"、"stands as"、"boasts"。改用 "is" 或 "has"。
- 抽象隐喻名词：paradigm、north star、flywheel、substrate、bedrock。直接点明具体事物。
- 用来撑起弱动词的副词："significantly improves"。给出数字，或换一个更有力的动词。

句子
- "Not just X, but Y." 直接说 Y。
- 硬凑的三项并列。按真实数量写。
- 句尾拖出的 "-ing" 从句："ensuring reliability"、"highlighting the need"。删掉，或改成一句实在的论断。
- 含糊的来源："experts say"、"many believe"。点名来源，或整句删掉。
- 填充词："in order to"、"it is important to note that"、"due to the fact that"。
- 叠加的模糊限定："could potentially"。只留一个限定词，或干脆不用。
- 掩盖动作主体的被动语态。点明是谁做的。
- 只谈感受、不谈机制。如果一句话原封不动放进任何项目的文档都成立，就删掉。
- 套路式收尾："the future looks bright"。落到事实或下一步上。
- 过度压缩的片段、箭头和符号简写。写成带冠词和动词的完整句子。

格式
- 破折号。改用句号或逗号。
- 把冒号当作句中连接词。只在列表前保留冒号。
- 每个词都加粗，以及 "**Label:** label restated" 式的条目。
- Title Case 式标题。改用 sentence case。
- 装饰性 emoji 和弯引号。

对话习惯
- 开场白和结束语："Great question"、"Certainly"、"I hope this helps"、"Let me know if"。
- 条件反射式的附和。给出你真实的判断。

代码注释
- 复述下一行代码的注释、横幅式注释，以及被注释掉的代码。删掉。
- 只保留那些解释代码本身无法体现的原因的注释。

## 重写步骤

1. 明确读者是谁，以及读完后他需要做什么或知道什么。
2. 删掉所有不服务于这一需要的句子。
3. 同一事物用了多个同义说法的，统一成一个名称。用真实的文件名、flag 或命令名。
4. 把塞进两个意思的句子拆开。让句子长短有变化。
5. 把条件放在指令之前："To reset the cache, run `make clean`."
6. 让每个 "it" 和 "this" 都明确指向一个名词。
7. 用数字、命令或具体例子替换含糊的说法。
8. 再通读一遍，排查这些痕迹。哪怕每条规定都照做了，生硬的句子仍要改。

## 示例

改写前："This robust tool serves as a powerful way to seamlessly streamline your workflow, ensuring efficiency."

改写后："`sync.sh` copies changed files to the server in about two seconds."
