"""Persian UI strings. Kept separate to make future i18n straightforward.

User-generated text embedded into these messages must already be HTML-escaped
(see app.utils.text_sanitizer). The numeric ``anonymous_id`` is the only sender
identifier ever shown — real usernames / ids are never exposed.
"""
from __future__ import annotations

# --- Buttons ---
BTN_MY_LINK = "🔗 دریافت لینک من"
BTN_SEND_MESSAGE = "✉️ ارسال پیام"
BTN_VIEW = "👁 دیدن پیام"
BTN_REPLY = "✍️ پاسخ دادن"
BTN_BLOCK = "🚫 بلاک کردن"
BTN_UNBLOCK = "♻️ آنبلاک"
BTN_BLOCK_CONFIRM = "✅ بله، بلاک کن"
BTN_BLOCK_CANCEL = "❌ لغو"

# --- Start / main menu ---
WELCOME = (
    "👋 به ربات پیام ناشناس خوش آمدید.\n"
    "از گزینه‌های زیر استفاده کنید:"
)


def your_link(link: str) -> str:
    return (
        "🔗 لینک پیام ناشناس شما:\n\n"
        f"{link}\n\n"
        "هر کسی با این لینک می‌تواند به‌صورت ناشناس برای شما پیام بفرستد."
    )


# --- Send-by-username flow ---
ASK_TARGET_USERNAME = (
    "username فردی که می‌خواهید به او پیام ناشناس بدهید را ارسال کنید.\n\n"
    "مثال:\n@username"
)
USER_NOT_FOUND = (
    "❌ این کاربر هنوز عضو ربات نیست یا username او در ربات ثبت نشده است."
)
TARGET_FOUND_COMPOSE = (
    "✅ کاربر موردنظر پیدا شد.\n"
    "حالا پیام ناشناس خود را ارسال کنید."
)
CANNOT_MESSAGE_SELF = "🚫 نمی‌توانید برای خودتان پیام ناشناس ارسال کنید."


# --- Compose (link) flow ---
def compose_prompt(recipient_label: str) -> str:
    return (
        "✍️ پیام ناشناس خود را بنویسید و ارسال کنید.\n"
        "هویت شما برای گیرنده فاش نخواهد شد."
    )


MESSAGE_SENT = "✅ پیام ناشناس شما ارسال شد."
INVALID_LINK = "❌ این لینک نامعتبر یا منقضی شده است."
EMPTY_MESSAGE = "⚠️ پیام خالی است. لطفاً متنی بنویسید."


# --- Incoming message (notification only — text is hidden until "view") ---
def new_message_alert(sender_label: str, is_reply: bool) -> str:
    if is_reply:
        return f"📨 شما یک پاسخ ناشناس از <code>{sender_label}</code> دارید."
    return f"📩 شما یک پیام ناشناس از <code>{sender_label}</code> دارید."


def revealed_message(sender_label: str, text: str, is_reply: bool) -> str:
    head = "📨 پاسخ ناشناس از" if is_reply else "📩 پیام ناشناس از"
    return f"{head} <code>{sender_label}</code>:\n\n{text}"


# --- Reply flow ---
REPLY_PROMPT = "✍️ پاسخ خود را بنویسید. پاسخ شما نیز ناشناس ارسال می‌شود."
REPLY_SENT = "✅ پاسخ شما ارسال شد."
CONVERSATION_NOT_FOUND = "❌ این گفتگو یافت نشد."

# --- Seen ---
SEEN_NOTIFICATION = "👁 پیام شما دیده شد."
MESSAGE_SEEN_ACK = "✅ نمایش داده شد."

# --- Block ---
BLOCK_CONFIRM_PROMPT = "آیا مطمئن هستید که می‌خواهید این کاربر را بلاک کنید؟"
BLOCKED_DONE = "🚫 این کاربر بلاک شد. دیگر پیامی از او دریافت نمی‌کنید."
UNBLOCKED_DONE = "♻️ این کاربر آنبلاک شد."
BLOCK_CANCELLED = "لغو شد."

# --- Errors / generic ---
RATE_LIMITED = "⏳ کمی آهسته‌تر! لطفاً {seconds} ثانیه دیگر دوباره تلاش کنید."
GENERIC_ERROR = "⚠️ خطایی رخ داد. لطفاً بعداً دوباره تلاش کنید."
NOT_EXPECTING_MESSAGE = (
    "ℹ️ برای شروع، /start را بزنید و یکی از گزینه‌ها را انتخاب کنید."
)
