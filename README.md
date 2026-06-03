# Anonymous Telegram Bot — ربات تلگرام ناشناس

ربات پیام ناشناس تلگرام با معماری لایه‌ای، نوشته‌شده با **Python + aiogram 3 + SQLAlchemy 2 (async)**.

هر کاربر یک لینک شخصی (deep link) می‌گیرد؛ دیگران از طریق آن لینک به‌صورت ناشناس برایش پیام می‌فرستند. گیرنده می‌تواند پیام را ببیند، پاسخ ناشناس بدهد و فرستنده را با تایید دو مرحله‌ای بلاک کند.

## معماری (Layered)

```
Telegram (aiogram) → Middlewares → Handlers → Services → Repositories → Database
```

- **handlers/** فقط ورودی/خروجی تلگرام
- **services/** منطق دامنه
- **repositories/** دسترسی به داده
- هر ماژول دامنه (`users`, `messages`, `conversations`, `blocks`, `states`, `links`, `notifications`, `rate_limits`) مستقل است.

## ساختار پروژه

```
app/
  bot/            handlers, keyboards, middlewares, texts, callbacks
  modules/        دامنه‌ها (models/service/repository)
  database/       base, connection, session, registry, migrations (Alembic)
  config/         settings, bot_config, database_config
  utils/          id/token generators, sanitizer, logger
main.py           entrypoint (wiring + polling)
```

## امکانات

- `/start` و `/start <token>` (deep link)
- ارسال پیام ناشناس متنی
- مشاهده پیام + اعلان «دیده شد» (قابل خاموش‌کردن)
- پاسخ ناشناس دوطرفه در قالب thread
- بلاک با تایید دو مرحله‌ای + آنبلاک
- محدودسازی ضد اسپم (sliding window + cooldown)
- محافظت در برابر IDOR روی callbackها، HTML-escape ورودی کاربر

## راه‌اندازی

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env   # سپس BOT_TOKEN و BOT_USERNAME را پر کنید
python main.py
```

برای نسخه اولیه، جداول به‌صورت خودکار ساخته می‌شوند. در محیط production از Alembic استفاده کنید:

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## دیتابیس

- پیش‌فرض: **SQLite** (async via `aiosqlite`)
- مهاجرت به **PostgreSQL**: کافی است `DATABASE_URL` را به
  `postgresql+asyncpg://user:pass@host:5432/db` تغییر دهید و
  `asyncpg` را نصب کنید (`pip install asyncpg`).

## تست

```bash
pip install -e ".[dev]"
pytest
```

## امنیت و حریم خصوصی

- `telegram_id` و نام واقعی هیچ‌گاه به طرف مقابل نمایش داده نمی‌شود.
- توکن‌ها با `secrets` تولید می‌شوند و از `telegram_id` مشتق نمی‌شوند.
- محتوای پیام‌ها در لاگ نوشته نمی‌شود.
