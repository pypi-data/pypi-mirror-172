from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.consts import inline_query_result_types
from telebox.telegram_bot.types.types.message_entity import MessageEntity
from telebox.telegram_bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.telegram_bot.types.types.input_message_content import InputMessageContent


@dataclass(unsafe_hash=True)
class InlineQueryResultMpeg4Gif(Type):
    id: str
    mpeg4_url: str
    thumb_url: str
    mpeg4_width: Optional[int] = None
    mpeg4_height: Optional[int] = None
    mpeg4_duration: Optional[int] = None
    thumb_mime_type: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    type: str = inline_query_result_types.MPEG4_GIF
