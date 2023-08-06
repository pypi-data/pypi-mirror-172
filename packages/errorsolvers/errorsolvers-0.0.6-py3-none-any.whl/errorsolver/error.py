import asyncio
import json
import logging
import random
import re
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InputMediaPhoto, Message)
from shortzyy import Shortzy

from database import db

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

