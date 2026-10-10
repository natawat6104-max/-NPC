#!/usr/bin/env python3
"""Generate docs/BALANCE.md from data/balance.json (the single source of numbers)."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "balance.json"
DST = ROOT / "docs" / "BALANCE.md"


def fmt(value):
    if isinstance(value, bool):
        return "ใช่" if value else "ไม่"
    if isinstance(value, dict):
        return ", ".join(f"{k}={fmt(v)}" for k, v in value.items())
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def cell(text):
    return str(text).replace("|", "\\|")


def render(data):
    lines = [
        "# ตารางตัวเลขกลาง (Balance)",
        "",
        "> ไฟล์นี้สร้างอัตโนมัติจาก `data/balance.json` — ห้ามแก้ด้วยมือ",
        "> แก้ตัวเลขที่ JSON แล้วรัน `python3 tools/gen_balance_doc.py`",
        "> ค่าที่ระบุที่มาว่า \"ใหม่ — ต้องทดสอบ\" ไม่มีในเอกสาร GDD เดิม",
        "",
    ]
    for group, entries in data.items():
        if group.startswith("_"):
            continue
        lines += [f"## {entries.get('_title', group)}", "",
                  "| คีย์ | ค่า | หน่วย | หมายเหตุ | ที่มา |",
                  "|---|---|---|---|---|"]
        for key, e in entries.items():
            if key.startswith("_"):
                continue
            lines.append(f"| `{group}.{key}` | {cell(fmt(e['value']))} | {cell(e['unit'])} "
                         f"| {cell(e['note'])} | {cell(e['source'])} |")
        lines.append("")
    return "\n".join(lines)


def main():
    text = render(json.loads(SRC.read_text(encoding="utf-8")))
    if "--check" in sys.argv:
        if not DST.exists() or DST.read_text(encoding="utf-8") != text:
            sys.exit("docs/BALANCE.md ไม่ตรงกับ data/balance.json — รัน tools/gen_balance_doc.py")
        return
    DST.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
