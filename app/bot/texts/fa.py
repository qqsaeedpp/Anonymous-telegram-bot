"""Persian UI strings. Kept separate to make future i18n straightforward.

User-generated text embedded into these messages must already be HTML-escaped
(see app.utils.text_sanitizer).
"""
from __future__ import annotations

# --- Buttons ---
BTN_VIEW = "👁 مشاهده پیام"
BTN_REPLY = "✍️ پاسخ"
BTN_BLOCK = "🚫 بلاک"
BTN_UNBLOCK = "♻️ آنبلاک"
BTN_BLOCK_CONFIRM = "✅ بله، بلاک کن"
BTN_BLOCK_CANCEL = "❌ لغو"
BTN_MY_LINK = "🔗 لینک من"
BTN_TOGGLE_SEEN = "🔔 تنظیم اعلان دیده‌شدن"

# --- Start / menu ---
WELCOME = (
    "👋 به ربات پیام ناشناس خوش آمدید!\n\n"
    "لینک شخصی شما در پایین است. آن را با دیگران به اشتراک بگذارید تا "
    "بتوانند به‌صورت ناشناس برایتان پیام بفرستند."
)


def your_link(link: str) -> str:
    return f"🔗 لینک شخصی شما:\n{link}"


# --- Compose flow ---
def compose_prompt(recipient_label: str) -> str:
    return (
        "✍️ پیام ناشناس خود را بنویسید و ارسال کنید.\n"
        "هویت شما برای گیرنده فاش نخواهد شد."
    )


MESSAGE_SENT = "✅ پیام ناشناس شما ارسال شد."
CANNOT_MESSAGE_SELF = "🚫 نمی‌توانید به خودتان پیام ناشناس بفرستید."
INVALID_LINK = "❌ این لینک نامعتبر یا منقضی شده است."
EMPTY_MESSAGE = "⚠️ پیام خالی است. لطفاً متنی بنویسید."

# --- Incoming message ---
NEW_MESSAGE_HEADER = "📩 یک پیام ناشناس جدید دریافت کردید"
NEW_REPLY_HEADER = "📨 پاسخی به گفتگوی ناشناس شما رسید"


def incoming_message(header: str, sender_label: str, text: str) -> str:
    return f"{header}\nاز: <code>{sender_label}</code>\n\n{text}"


# --- Reply flow ---
REPLY_PROMPT = "✍️ پاسخ خود را بنویسید. پاسخ شما نیز ناشناس ارسال می‌شود."
REPLY_SENT = "✅ پاسخ شما ارسال شد."
CONVERSATION_NOT_FOUND = "❌ این گفتگو یافت نشد."

# --- Seen ---
SEEN_NOTIFICATION = "👁 پیام ناشناس شما دیده شد."
MESSAGE_SEEN_ACK = "✅ پیام به‌عنوان دیده‌شده ثبت شد."

# --- Block ---
BLOCK_CONFIRM_PROMPT = "آیا مطمئن هستید که می‌خواهید این کاربر را بلاک کنید؟"
BLOCKED_DONE = "🚫 این کاربر بلاک شد. دیگر پیامی از او دریافت نمی‌کنید."
UNBLOCKED_DONE = "♻️ این کاربر آنبلاک شد."
BLOCK_CANCELLED = "لغو شد."

# --- Settings ---
def seen_setting_status(enabled: bool) -> str:
    state = "روشن" if enabled else "خاموش"
    return f"🔔 اعلان دیده‌شدن اکنون {state} است."


# --- Errors / generic ---
RATE_LIMITED = "⏳ کمی آهسته‌تر! لطفاً {seconds} ثانیه دیگر دوباره تلاش کنید."
GENERIC_ERROR = "⚠️ خطایی رخ داد. لطفاً بعداً دوباره تلاش کنید."
NOT_EXPECTING_MESSAGE = (
    "ℹ️ برای ارسال پیام ناشناس، از لینک شخصی یک کاربر استفاده کنید."
)
