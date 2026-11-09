# 博士申请计划

面向聚变堆屏蔽快速方案迭代的块结构体素—GPU-MOC 协同设计。

**V4.2 起全面改用 LaTeX，不再维护 Word，也不保留历史副本。** 正文只有 `latex/main.tex` 一个来源。

## 当前交付

| 内容 | 路径 |
|---|---|
| LaTeX 源码（单文件：导言区 + 封面 + 六章 + 67 条参考文献） | [`latex/main.tex`](latex/main.tex) |
| 编译脚本 | [`latex/build.sh`](latex/build.sh) |
| 图片（矢量 PDF + 位图 PNG） | `latex/figures/fig1.pdf` … `fig7.pdf`、`fig4.png` |
| 编译产物 | `latex/main.pdf`（本地生成，不入库） |

成稿约 35 页，含 7 幅图、6 张表、67 篇参考文献。

## 编译

需要 XeLaTeX + ctex（TeX Live 或 MacTeX 均可）。

```bash
cd latex
bash build.sh          # 连编两遍，目录与交叉引用才完整
```

字体使用 macOS 系统字体：正文 Songti SC、标题 Heiti SC、西文 Times New Roman。
换到 Linux/Windows 时，把 `main.tex` 里的 `\setCJKmainfont` 等改成 `fandol`
或本机可用字体即可。

版式要点：

- 章标题自动编号「第一章 …第六章」，节标题 `1.1 / 1.2 …`，与原文手工编号一致；
- 引文统一用 `\upcite{1,2}` 渲染为上标 `[1,2]`，对应文末 67 条 `thebibliography`；
- 6 张表用 `longtable` + `booktabs`，跨页自动重复表头；7 幅图为 `figure` 浮动体；
- 公式用 `equation` 自动编号，与原稿（1）—（9）一致。

## 目录结构

```
博士申请计划/
├── README.md                本文件
└── latex/                  ← 正文唯一来源
    ├── main.tex              单文件：导言区 + 封面 + 六章 + 参考文献
    ├── build.sh              编译脚本
    ├── figures/              图 1–7
    └── main.pdf              编译产物（本地生成，不入库）
```

## 版本沿革

| 版本 | 形态 | 说明 |
|---|---|---|
| 导师讨论初稿 → V2 → V3 | Word（已废弃） | 六章骨架、批注处理、63 篇文献收尾 |
| V4 / V4.1 / V4.2 | Word（已废弃） | 陈述式改写、调研深化、两句立场句；67 篇文献 |
| **V4.2（LaTeX）** | **当前** | 由 V4.2 Word 全文转换并重排版式，正文内容等价 |

Word 原件与逐轮修改记录只保留在仓库外的备份
`/Users/sophia_zhou/GPU/_backup_rp_20261108.tar.gz` 与交付快照
`/Users/sophia_zhou/GPU/科研计划与计算迭代汇总_截至V4.2_20261108/` 中；
V2/V3 的 Word 也可从 Git 提交 `171f19d`、`bb17d7a` 取回。
