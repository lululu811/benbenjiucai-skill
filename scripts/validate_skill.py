#!/usr/bin/env python3
"""
Skill 质量验证脚本

检查项目中的常见问题：
1. 禁用词检查（书面语、客套话）
2. 人称一致性检查（是否使用"我"而非第三人称）
3. OMC 与源文件同步状态检查
4. 引用格式规范性检查

用法:
    python scripts/validate_skill.py
"""

import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 禁用词列表（角色扮演中不应出现的书面语/客套话）
FORBIDDEN_WORDS = [
    "您好", "请", "谢谢", "感谢", "不客气",
    "然而", "因而", "故而", "综上所述",
]

# 第三人称表述（角色扮演中应该避免，应使用"我"）
THIRD_PERSON_PATTERNS = [
    r"笨笨的韭菜会认为",
    r"笨笨的韭菜觉得",
    r"笨笨的韭菜认为",
    r"他认为",
    r"她觉得",
    r"作者认为",
]

# 源文件 → OMC 映射
SYNC_MAPPINGS = {
    "modules/on-demand/stock-analysis.md": ".omc/skills/benbenjiucai-stock/SKILL.md",
    "modules/on-demand/portfolio.md": ".omc/skills/benbenjiucai-portfolio/SKILL.md",
    "modules/on-demand/psychology.md": ".omc/skills/benbenjiucai-psychology/SKILL.md",
    "modules/on-demand/market-context.md": ".omc/skills/benbenjiucai-market/SKILL.md",
    "modules/on-demand/industry-chain.md": ".omc/skills/benbenjiucai-industry/SKILL.md",
    "modules/on-demand/quarterly-report.md": ".omc/skills/benbenjiucai-quarterly/SKILL.md",
    "modules/on-demand/take-profit.md": ".omc/skills/benbenjiucai-take-profit/SKILL.md",
    "modules/on-demand/macro-analysis.md": ".omc/skills/benbenjiucai-macro/SKILL.md",
    "modules/on-demand/quant-enhanced.md": ".omc/skills/benbenjiucai-quant/SKILL.md",
    "modules/benben-stock-guide/SKILL.md": ".omc/skills/benben-stock-guide/SKILL.md",
}


def check_forbidden_words(filepath, content):
    """检查禁用词"""
    issues = []
    lines = content.split('\n')
    in_code_block = False
    for i, line in enumerate(lines, 1):
        # 代码块边界
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # 跳过引用块（以 > 开头）——通常是原文引用
        if line.strip().startswith('>'):
            continue
        # 跳过表格行（包含 | 的行）
        if '|' in line:
            continue
        for word in FORBIDDEN_WORDS:
            if word in line:
                # 排除"禁忌词"说明行本身（如"从不使用'您好''请''谢谢'"）
                if '禁忌词' in line or '禁用词' in line or '客套' in line:
                    continue
                # 排除"用「我」而非..."规则描述行
                if '而非' in line and '我' in line:
                    continue
                # 排除"请"字的常见误报（申请/请求/邀请/请问等词中包含"请"）
                if word == '请' and any(w in line for w in ['申请', '请求', '邀请', '请问', '请愿', '提请', '聘请']):
                    continue
                # 排除 UP 主视频口头禅原文（"感谢大家的观看啊"）
                if word == '感谢' and '感谢大家的观看' in line:
                    continue
                # 排除合规声明中的"请"
                if word == '请' and '如有疑问，请优先参考' in line:
                    continue
                # 排除引号内的原文引用（UP主口语原话）
                if '"' in line and word in line.split('"')[1] if '"' in line and line.count('"') >= 2 else False:
                    continue
                issues.append((i, word, line.strip()))
    return issues


def check_third_person(filepath, content):
    """检查第三人称表述"""
    issues = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # 跳过规则描述行（如"用「我」而非「笨笨的韭菜会认为」"）
        if '而非' in line:
            continue
        for pattern in THIRD_PERSON_PATTERNS:
            if re.search(pattern, line):
                issues.append((i, pattern, line.strip()))
    return issues


def check_sync_status(src_path, omc_path):
    """检查 OMC 与源文件的同步状态"""
    src_full = os.path.join(BASE_DIR, src_path)
    omc_full = os.path.join(BASE_DIR, omc_path)

    if not os.path.exists(omc_full):
        return "missing", None

    with open(src_full, 'r') as f:
        src_lines = f.readlines()
    with open(omc_full, 'r') as f:
        omc_lines = f.readlines()

    # 清理源文件正文（去掉触发条件注释和渐进加载声明）
    clean_src = []
    for line in src_lines:
        if re.match(r'^> 触发条件', line) or re.match(r'^> 加载方式', line):
            continue
        clean_src.append(line)
    while clean_src and clean_src[-1].strip() in ['', '---', '*本模块由核心系统渐进加载*']:
        clean_src.pop()
    while clean_src and clean_src[-1].strip() == '':
        clean_src.pop()

    # 清理 OMC 文件（去掉 front matter）
    clean_omc = []
    in_front_matter = False
    front_matter_done = False
    for line in omc_lines:
        if line.strip() == '---' and not front_matter_done:
            in_front_matter = not in_front_matter
            if not in_front_matter:
                front_matter_done = True
            continue
        if front_matter_done:
            clean_omc.append(line)

    # 去掉末尾空行
    while clean_omc and clean_omc[-1].strip() == '':
        clean_omc.pop()

    # 比较（忽略标题的"模块："前缀差异）
    src_body = ''.join(clean_src)
    omc_body = ''.join(clean_omc)

    # 标准化标题差异
    src_normalized = re.sub(r'^# 模块：', '# ', src_body)
    omc_normalized = re.sub(r'^# 模块：', '# ', omc_body)

    if src_normalized == omc_normalized:
        return "synced", None

    # 计算差异大小
    diff_size = len(omc_normalized) - len(src_normalized)
    # 忽略微小差异（尾部换行差异等，容差 50B）
    if abs(diff_size) < 50:
        return "synced", None
    return "diff", diff_size


def check_references(filepath, content):
    """检查 qa_xxxx 引用格式"""
    issues = []
    # 查找所有 qa_xxxx 引用
    refs = re.findall(r'qa_(\d{4,})', content)
    # 检查是否有不完整的引用格式（如缺少括号或标注）
    # 简单检查：查找 qa_ 后面不是数字的情况
    bad_refs = re.findall(r'qa_[^\d\n]', content)
    if bad_refs:
        issues.append((0, f"发现不规范的 qa_ 引用: {bad_refs[0]}", ""))
    return issues


def validate_file(filepath):
    """验证单个文件"""
    full_path = os.path.join(BASE_DIR, filepath)
    if not os.path.exists(full_path):
        return None

    with open(full_path, 'r') as f:
        content = f.read()

    results = {
        'filepath': filepath,
        'forbidden': check_forbidden_words(filepath, content),
        'third_person': check_third_person(filepath, content),
        'references': check_references(filepath, content),
    }
    return results


def main():
    print("=" * 60)
    print("Skill 质量验证")
    print("=" * 60)

    all_issues = 0

    # 1. 检查所有 Markdown 文件
    md_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # 跳过 .git 和 node_modules 等
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv']]
        for f in files:
            if f.endswith('.md'):
                rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
                # 跳过 references/（调研过程文档，不是 Skill 输出）
                # 跳过 templates/（模板文件本身会提到禁用词列表）
                # 跳过 CLAUDE.md（项目说明文档）
                if rel.startswith('references/'):
                    continue
                if rel.startswith('templates/'):
                    continue
                if rel == 'CLAUDE.md':
                    continue
                md_files.append(rel)

    print(f"\n📄 检查 {len(md_files)} 个 Markdown 文件...\n")

    for filepath in sorted(md_files):
        result = validate_file(filepath)
        if not result:
            continue

        file_issues = 0
        lines = []

        if result['forbidden']:
            file_issues += len(result['forbidden'])
            lines.append(f"  ❌ 禁用词 ({len(result['forbidden'])} 处):")
            for line_no, word, context in result['forbidden'][:3]:
                lines.append(f"     第{line_no}行: [{word}] {context[:60]}")
            if len(result['forbidden']) > 3:
                lines.append(f"     ... 还有 {len(result['forbidden']) - 3} 处")

        if result['third_person']:
            file_issues += len(result['third_person'])
            lines.append(f"  ❌ 第三人称 ({len(result['third_person'])} 处):")
            for line_no, pattern, context in result['third_person'][:3]:
                lines.append(f"     第{line_no}行: [{pattern}] {context[:60]}")

        if result['references']:
            file_issues += len(result['references'])
            lines.append(f"  ⚠️  引用格式 ({len(result['references'])} 处)")

        if file_issues > 0:
            print(f"{filepath}")
            for line in lines:
                print(line)
            print()
            all_issues += file_issues

    # 2. 检查 OMC 同步状态
    print("=" * 60)
    print("OMC 同步状态检查")
    print("=" * 60)

    sync_issues = 0
    for src_path, omc_path in SYNC_MAPPINGS.items():
        status, diff_size = check_sync_status(src_path, omc_path)
        skill_name = os.path.basename(os.path.dirname(omc_path))

        if status == "missing":
            print(f"  ❌ {skill_name}: OMC 文件缺失")
            sync_issues += 1
        elif status == "diff":
            print(f"  ⚠️  {skill_name}: 内容不同步 (差异 {diff_size:+d}B)")
            sync_issues += 1
        else:
            print(f"  ✅ {skill_name}: 已同步")

    # 总结
    print("\n" + "=" * 60)
    print("验证结果")
    print("=" * 60)
    print(f"  文件总数: {len(md_files)}")
    print(f"  内容问题: {all_issues} 处")
    print(f"  同步问题: {sync_issues} 处")

    if all_issues == 0 and sync_issues == 0:
        print(f"\n🎉 全部通过！")
        sys.exit(0)
    else:
        print(f"\n⚠️ 发现 {all_issues + sync_issues} 个问题，请修复")
        sys.exit(1)


if __name__ == "__main__":
    main()
