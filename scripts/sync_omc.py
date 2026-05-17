#!/usr/bin/env python3
"""
OMC 子 Skill 自动同步脚本

将 modules/on-demand/*.md 和 modules/benben-stock-guide/SKILL.md
同步到 .omc/skills/*/SKILL.md

用法:
    python scripts/sync_omc.py [--dry-run]

--dry-run: 只检查差异，不写入文件
"""

import os
import re
import sys
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 源文件 → OMC 子 Skill 名称映射
# 键: 源文件相对路径
# 值: OMC 子 Skill 目录名
MAPPINGS = {
    "modules/on-demand/stock-analysis.md": "benbenjiucai-stock",
    "modules/on-demand/portfolio.md": "benbenjiucai-portfolio",
    "modules/on-demand/psychology.md": "benbenjiucai-psychology",
    "modules/on-demand/market-context.md": "benbenjiucai-market",
    "modules/on-demand/industry-chain.md": "benbenjiucai-industry",
    "modules/on-demand/quarterly-report.md": "benbenjiucai-quarterly",
    "modules/on-demand/take-profit.md": "benbenjiucai-take-profit",
    "modules/on-demand/macro-analysis.md": "benbenjiucai-macro",
    "modules/on-demand/quant-enhanced.md": "benbenjiucai-quant",
    "modules/benben-stock-guide/SKILL.md": "benben-stock-guide",
}


def extract_front_matter(content):
    """从 OMC 文件中提取 front matter (--- ... ---)"""
    match = re.match(r'(---\n.*?\n---\n)', content, re.DOTALL)
    return match.group(1) if match else None


def generate_default_front_matter(skill_name):
    """为不存在的 OMC 子 Skill 生成默认 front matter"""
    return f"""---
name: {skill_name}
description: |
  笨笨的韭菜子模块。
  当用户提到相关关键词时使用。
  在笨笨的韭菜主 Skill 已激活的前提下补充深度内容。
---

"""


def clean_source_body(lines):
    """清理源文件正文：去掉触发条件注释和渐进加载声明"""
    body_lines = []

    for line in lines:
        # 跳过触发条件 / 加载方式注释
        if re.match(r'^> 触发条件', line) or re.match(r'^> 加载方式', line):
            continue
        body_lines.append(line)

    # 去掉末尾的渐进加载声明
    while body_lines and body_lines[-1].strip() in ['', '---', '*本模块由核心系统渐进加载*']:
        body_lines.pop()

    # 去掉末尾空行
    while body_lines and body_lines[-1].strip() == '':
        body_lines.pop()

    return body_lines


def convert_title(body_lines, skill_name):
    """转换标题：去掉 '模块：' 前缀（benben-stock-guide 除外）"""
    if 'benben-stock-guide' in skill_name:
        return body_lines

    if body_lines and re.match(r'^# 模块：(.+?)\n', body_lines[0]):
        body_lines[0] = re.sub(r'^# 模块：(.+?)\n', r'# \1\n', body_lines[0])

    return body_lines


def sync_file(src_path, omc_skill_name, dry_run=False):
    """同步单个文件"""
    src_full = os.path.join(BASE_DIR, src_path)
    omc_dir = os.path.join(BASE_DIR, ".omc/skills", omc_skill_name)
    omc_full = os.path.join(omc_dir, "SKILL.md")

    # 读取源文件
    with open(src_full, 'r') as f:
        src_lines = f.readlines()

    # 清理正文
    body_lines = clean_source_body(src_lines)
    body_lines = convert_title(body_lines, omc_skill_name)
    body = ''.join(body_lines)

    # 获取或生成 front matter
    if os.path.exists(omc_full):
        with open(omc_full, 'r') as f:
            omc_content = f.read()
        front_matter = extract_front_matter(omc_content)
        if not front_matter:
            front_matter = generate_default_front_matter(omc_skill_name)
            print(f"  ⚠️  {omc_skill_name}/SKILL.md 缺少 front matter，已生成默认")
    else:
        front_matter = generate_default_front_matter(omc_skill_name)
        print(f"  ⚠️  {omc_skill_name}/SKILL.md 不存在，将创建")

    # 组合新内容
    new_content = front_matter + '\n' + body + '\n'

    # 检查是否需要更新
    if os.path.exists(omc_full):
        with open(omc_full, 'r') as f:
            old_content = f.read()
        if old_content == new_content:
            return "unchanged", 0

    if dry_run:
        return "changed", len(new_content)

    # 写入
    os.makedirs(omc_dir, exist_ok=True)
    with open(omc_full, 'w') as f:
        f.write(new_content)

    return "updated", len(new_content)


def main():
    parser = argparse.ArgumentParser(description="同步 OMC 子 Skill")
    parser.add_argument("--dry-run", action="store_true", help="只检查差异，不写入文件")
    args = parser.parse_args()

    print("=" * 60)
    print("OMC 子 Skill 同步")
    print("=" * 60)

    if args.dry_run:
        print("(干运行模式 — 不写入文件)\n")

    unchanged = 0
    updated = 0
    created = 0

    for src_path, skill_name in MAPPINGS.items():
        print(f"\n{skill_name}")
        print(f"  源文件: {src_path}")

        status, size = sync_file(src_path, skill_name, dry_run=args.dry_run)

        if status == "unchanged":
            print(f"  ✅ 已是最新，无需同步")
            unchanged += 1
        elif status == "changed":
            print(f"  ⚠️  有差异，需要同步 ({size}B)")
            updated += 1
        else:
            print(f"  ✅ 已同步 ({size}B)")
            if os.path.exists(os.path.join(BASE_DIR, ".omc/skills", skill_name, "SKILL.md")):
                updated += 1
            else:
                created += 1

    print("\n" + "=" * 60)
    print("同步结果")
    print("=" * 60)
    print(f"  无需同步: {unchanged}")
    print(f"  已更新/待更新: {updated}")
    print(f"  新创建: {created}")
    print(f"  总计: {len(MAPPINGS)}")

    if args.dry_run and updated > 0:
        print(f"\n提示: 运行 `python scripts/sync_omc.py` 应用更改")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
