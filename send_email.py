#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path
from datetime import datetime

# ========== 1. 基本配置（从环境变量读，方便 GitHub Actions 保密） ==========
EMAIL_FROM    = os.getenv("EMAIL_FROM")          # 例：you@163.com
EMAIL_PASSWORD= os.getenv("EMAIL_PASSWORD")      # 授权码，不是登录密码！
EMAIL_TO      = os.getenv("EMAIL_TO")            # 例：a@qq.com,b@gmail.com
SMTP_SERVER   = "smtp.qq.com"                   # 你的发件箱服务器
SMTP_PORT     = 465                             # SSL 端口

# ========== 2. 模板读取 ==========
tpl = Path("email_template.html").read_text(encoding="utf-8")

# ========== 3. 数据拼装（这里仅示例，真实数据可由 crawler 生成） ==========
subject   = "TrendRadar 每日技术热点"
date_str  = datetime.now().strftime("%Y-%m-%d")
bg_url    = "https://cdn.jsdelivr.net/gh/konlyi/image@main/background.jpg "   # 可换自己的图
repo      = "konlyi/TrendRadar"                               # 你的仓库

# 假设 crawler 已经把热点存成 list[dict]
news_list = [
    {"title":"GitHub 推出新 CI 免费额度","desc":"每月 2000 分钟，薅羊毛攻略在此","link":"https://github.blog/2025-11-12"},
    {"title":"Python 3.14 性能翻倍","desc":"全新 JIT 编译器实测","link":"https://python.org/download"},
]

# 把 list 拼成 HTML 行
news_rows = ""
for n in news_list:
    news_rows += f"""
    <tr><td>
      <table class="card" width="100%" cellpadding="0" cellspacing="0">
        <tr><td class="card-body">
          <h2 class="card-title">{n['title']}</h2>
          <p class="card-desc">{n['desc']}</p>
          <a href="{n['link']}" class="card-link" target="_blank">查看全文 →</a>
        </td></tr>
      </table>
    </td></tr>
    """

html = tpl.format(subject=subject, date=date_str, bg_url=bg_url,
                  news_rows=news_rows, repo=repo)

# ========== 4. 群发邮件 ==========
to_list = [e.strip() for e in EMAIL_TO.split(",") if e.strip()]

msg            = MIMEText(html, "html", "utf-8")
msg["From"]    = EMAIL_FROM
msg["To"]      = ",".join(to_list)
msg["Subject"] = Header(subject, "utf-8")

with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
    smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
    smtp.sendmail(EMAIL_FROM, to_list, msg.as_string())

print(f"✅ 邮件已发送至 {len(to_list)} 个邮箱")
