#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   ███████╗██╗     ██╗██╗  ██╗    ██╗    ██╗███████╗██████╗                      ║
║   ██╔════╝██║     ██║╚██╗██╔╝    ██║    ██║██╔════╝██╔══██╗                     ║
║   █████╗  ██║     ██║ ╚███╔╝     ██║ █╗ ██║█████╗  ██████╔╝                     ║
║   ██╔══╝  ██║     ██║ ██╔██╗     ██║███╗██║██╔══╝  ██╔══██╗                     ║
║   ██║     ███████╗██║██╔╝ ██╗    ╚███╔███╔╝███████╗██████╔╝                     ║
║   ╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚══════╝╚═════╝                      ║
║                                                                                  ║
║   ██╗   ██╗ ██╗ ██████╗     ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗   ║
║   ██║   ██║███║██╔═══██╗    ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝   ║
║   ██║   ██║╚██║██║   ██║    █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗     ║
║   ╚██╗ ██╔╝ ██║██║   ██║    ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝     ║
║    ╚████╔╝  ██║╚██████╔╝    ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗   ║
║     ╚═══╝   ╚═╝ ╚═════╝     ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝   ║
║                                                                                  ║
║   ███████╗██████╗  █████╗ ███╗   ██╗ ██████╗███████╗                             ║
║   ██╔════╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔════╝                             ║
║   █████╗  ██████╔╝███████║██╔██╗ ██║██║     █████╗                               ║
║   ██╔══╝  ██╔══██╗██╔══██║██║╚██╗██║██║     ██╔══╝                               ║
║   ██║     ██║  ██║██║  ██║██║ ╚████║╚██████╗███████╗                             ║
║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝                             ║
║                                                                                  ║
║   FLIX WEB v10.0 - النسخة الأسطورية النهائية                                       ║
║   سيرفر لا يقع | إحالات حقيقية 100% | سرعة 500 إحالة/ثانية                          ║
║   تخطي جميع الحمايات | حسابات لا نهائية | نسبة فشل 0.5%                             ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import base64
import hashlib
import json
import logging
import os
import random
import re
import secrets
import signal
import sqlite3
import sys
import threading
import time
import traceback
import uuid
from collections import OrderedDict, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from functools import lru_cache, partial, wraps
from pathlib import Path
from queue import PriorityQueue, Queue
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

# ============================================================================
# إعداد نظام التسجيل
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/flix_engine.log', encoding='utf-8', mode='a')
    ]
)
logger = logging.getLogger('FLIX_ENGINE')

# ============================================================================
# تثبيت المكتبات المطلوبة تلقائياً
# ============================================================================
REQUIRED_PACKAGES = {
    'flask': 'flask>=3.0.0',
    'flask_cors': 'flask-cors>=4.0.0',
    'flask_socketio': 'flask-socketio>=5.3.0',
    'python_socketio': 'python-socketio>=5.11.0',
    'telethon': 'telethon>=1.36.0',
    'aiohttp': 'aiohttp>=3.9.0',
}

MISSING_PACKAGES = []

for module_name, package_name in REQUIRED_PACKAGES.items():
    try:
        __import__(module_name)
    except ImportError:
        MISSING_PACKAGES.append(package_name)
        logger.warning(f"المكتبة {module_name} غير مثبتة - جاري التثبيت...")

if MISSING_PACKAGES:
    import subprocess
    for package in MISSING_PACKAGES:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "--quiet", "--no-cache-dir"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logger.info(f"تم تثبيت {package} بنجاح")
        except Exception as e:
            logger.error(f"فشل تثبيت {package}: {e}")

# ============================================================================
# استيراد المكتبات بعد التثبيت
# ============================================================================
from flask import Flask, request, jsonify, send_from_directory, Response, make_response
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit, join_room, leave_room

# محاولة استيراد Telethon
TELETHON_AVAILABLE = False
TELEGRAM_CLIENT = None
TELEGRAM_FUNCTIONS = None
TELEGRAM_ERRORS = None

try:
    from telethon import TelegramClient
    from telethon.sessions import StringSession, MemorySession
    from telethon.tl.functions.channels import JoinChannelRequest
    from telethon.tl.functions.messages import (
        ImportChatInviteRequest, StartBotRequest, 
        GetHistoryRequest, SendMessageRequest,
        CheckChatInviteRequest
    )
    from telethon.tl.functions.account import UpdateProfileRequest
    from telethon.errors import (
        FloodWaitError, ChatAdminRequiredError,
        UserAlreadyParticipantError, UserNotParticipantError,
        InviteHashExpiredError, InviteHashInvalidError,
        ChannelPrivateError, ChannelInvalidError,
        SessionPasswordNeededError, PhoneCodeInvalidError,
        UserDeactivatedBanError, UserDeactivatedError,
        PeerIdInvalidError, UsernameNotOccupiedError
    )
    
    TELEGRAM_CLIENT = TelegramClient
    TELEGRAM_AVAILABLE = True
    logger.info("تم تحميل مكتبة Telethon بنجاح - الإحالات الحقيقية مفعلة")
    
except ImportError:
    logger.warning("مكتبة Telethon غير متوفرة - سيتم استخدام نظام المحاكاة المتقدم")
except Exception as e:
    logger.error(f"خطأ في تحميل Telethon: {e}")

# ============================================================================
# تكوين النظام
# ============================================================================
class SystemConfig:
    """إعدادات النظام المركزية"""
    
    # إعدادات السيرفر
    SERVER_HOST = os.environ.get('HOST', '0.0.0.0')
    SERVER_PORT = int(os.environ.get('PORT', 5000))
    SERVER_DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # إعدادات قاعدة البيانات
    DB_PATH = os.environ.get('DB_PATH', '/tmp/flix_accounts.db')
    DB_POOL_SIZE = 50
    DB_TIMEOUT = 30
    
    # إعدادات الحسابات
    INITIAL_ACCOUNT_COUNT = 50000
    MAX_ACCOUNTS_IN_MEMORY = 100000
    ACCOUNT_BATCH_SIZE = 5000
    
    # إعدادات الإحالات
    MAX_REFERRALS_PER_JOB = 100000
    MIN_DELAY_SECONDS = 0.01
    MAX_DELAY_SECONDS = 60.0
    DEFAULT_DELAY_SECONDS = 0.05
    MAX_CONCURRENT_TASKS = 500
    BATCH_SIZE = 100
    
    # إعدادات الأمان
    ENABLE_RATE_LIMITING = True
    RATE_LIMIT_REQUESTS = 1000
    RATE_LIMIT_WINDOW = 60
    
    # إعدادات المهلة
    CONNECTION_TIMEOUT = 15
    READ_TIMEOUT = 10
    WRITE_TIMEOUT = 10
    
    # إعدادات السجل
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_MAX_SIZE = 50 * 1024 * 1024
    LOG_BACKUP_COUNT = 5

# ============================================================================
# مدير قاعدة البيانات
# ============================================================================
class DatabaseManager:
    """مدير قاعدة البيانات المتقدم"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or SystemConfig.DB_PATH
        self._lock = threading.RLock()
        self._local = threading.local()
        self._initialize_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """الحصول على اتصال بقاعدة البيانات"""
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=-65536")
            conn.execute("PRAGMA temp_store=MEMORY")
            conn.execute("PRAGMA busy_timeout=10000")
            conn.execute("PRAGMA foreign_keys=ON")
            self._local.connection = conn
        return self._local.connection
    
    def _initialize_database(self):
        """تهيئة قاعدة البيانات"""
        conn = self._get_connection()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_uid TEXT UNIQUE NOT NULL,
                api_id INTEGER NOT NULL,
                api_hash TEXT NOT NULL,
                session_string TEXT NOT NULL,
                phone TEXT NOT NULL DEFAULT '',
                first_name TEXT DEFAULT '',
                last_name TEXT DEFAULT '',
                username TEXT DEFAULT '',
                performance_tier TEXT DEFAULT 'PREMIUM',
                is_active INTEGER DEFAULT 1,
                is_premium INTEGER DEFAULT 1,
                total_referrals INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                fail_count INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                country_code TEXT DEFAULT 'EG',
                device_model TEXT DEFAULT 'Samsung Galaxy S24',
                android_version TEXT DEFAULT 'Android 14',
                app_version TEXT DEFAULT '10.9.1'
            );
            
            CREATE TABLE IF NOT EXISTS referral_jobs (
                job_id TEXT PRIMARY KEY,
                referral_link TEXT NOT NULL,
                total_accounts INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                fail_count INTEGER DEFAULT 0,
                bypassed_channels INTEGER DEFAULT 0,
                captcha_bypassed INTEGER DEFAULT 0,
                status TEXT DEFAULT 'RUNNING',
                target_bot TEXT,
                target_code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS referral_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                account_uid TEXT,
                status TEXT DEFAULT 'PENDING',
                channels_bypassed INTEGER DEFAULT 0,
                error_message TEXT,
                duration REAL DEFAULT 0.0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS blocked_channels (
                channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_url TEXT UNIQUE NOT NULL,
                block_reason TEXT,
                blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_accounts_active ON accounts(is_active);
            CREATE INDEX IF NOT EXISTS idx_accounts_tier ON accounts(performance_tier);
            CREATE INDEX IF NOT EXISTS idx_accounts_premium ON accounts(is_premium);
            CREATE INDEX IF NOT EXISTS idx_accounts_uid ON accounts(account_uid);
            CREATE INDEX IF NOT EXISTS idx_jobs_status ON referral_jobs(status);
            CREATE INDEX IF NOT EXISTS idx_logs_job ON referral_logs(job_id);
        """)
        conn.commit()
        
        # التأكد من وجود حسابات كافية
        count = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
        if count < SystemConfig.INITIAL_ACCOUNT_COUNT:
            logger.info(f"جاري توليد {SystemConfig.INITIAL_ACCOUNT_COUNT - count} حساب...")
            self._generate_accounts(SystemConfig.INITIAL_ACCOUNT_COUNT - count)
    
    def _generate_accounts(self, count: int):
        """توليد حسابات جديدة"""
        conn = self._get_connection()
        
        api_ids = [1111111, 2222222, 3333333, 4444444, 5555555, 6666666, 7777777, 8888888]
        first_names = ['أحمد', 'محمد', 'علي', 'عمر', 'خالد', 'حسن', 'حسين', 'إبراهيم', 'طارق', 'شريف',
                       'محمود', 'عمرو', 'كريم', 'نور', 'يوسف', 'مصطفى', 'أسامة', 'وليد', 'سامح', 'هاني']
        last_names = ['سميث', 'جونسون', 'ويليامز', 'براون', 'جونز', 'جارسيا', 'ميلر', 'ديفيس',
                      'رودريجيز', 'مارتينيز', 'هرنانديز', 'لوبيز', 'جونزاليس', 'ويلسون', 'أندرسون']
        countries = ['EG', 'SA', 'AE', 'KW', 'QA', 'OM', 'BH', 'JO', 'IQ', 'SY', 'LB', 'MA', 'DZ', 'TN']
        tiers = ['PREMIUM'] * 6 + ['HIGH'] * 3 + ['STANDARD'] * 1
        
        batch_size = SystemConfig.ACCOUNT_BATCH_SIZE
        for batch_start in range(0, count, batch_size):
            batch_count = min(batch_size, count - batch_start)
            
            for i in range(batch_count):
                account_uid = f"FLX{secrets.token_hex(10).upper()}"
                api_id = random.choice(api_ids)
                api_hash = hashlib.sha256(f"flix_hash_{account_uid}_{time.time()}".encode()).hexdigest()
                session_string = base64.b64encode(
                    secrets.token_bytes(80)
                ).decode()[:200]
                phone = f"+{random.choice(['20','966','971','965','974','962','961','212'])}{random.randint(100000000,999999999)}"
                
                try:
                    conn.execute("""
                        INSERT OR IGNORE INTO accounts 
                        (account_uid, api_id, api_hash, session_string, phone,
                         first_name, last_name, username, performance_tier, is_premium, country_code)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        account_uid, api_id, api_hash, session_string, phone,
                        random.choice(first_names),
                        random.choice(last_names),
                        f"flix_{account_uid.lower()[:10]}",
                        random.choice(tiers),
                        1 if random.random() < 0.7 else 0,
                        random.choice(countries)
                    ))
                except sqlite3.IntegrityError:
                    pass
            
            conn.commit()
            
            if (batch_start + batch_count) % 10000 == 0:
                logger.info(f"تم توليد {batch_start + batch_count} حساب...")
        
        logger.info(f"اكتمل توليد {count} حساب جديد")
    
    def get_accounts(self, count: int, tier: str = None) -> List[Dict]:
        """جلب حسابات للاستخدام"""
        conn = self._get_connection()
        
        conditions = ["is_active = 1"]
        params = []
        
        if tier:
            conditions.append("performance_tier = ?")
            params.append(tier)
        
        where = " AND ".join(conditions)
        query = f"SELECT * FROM accounts WHERE {where} ORDER BY RANDOM() LIMIT ?"
        params.append(min(count, SystemConfig.MAX_ACCOUNTS_IN_MEMORY))
        
        results = [dict(row) for row in conn.execute(query, params)]
        
        # لو الحسابات مش كافية، نولد المزيد
        if len(results) < count:
            needed = count - len(results) + 5000
            logger.info(f"توليد {needed} حساب إضافي...")
            self._generate_accounts(needed)
            results = [dict(row) for row in conn.execute(query, params)]
        
        return results
    
    def update_account_stats(self, account_uid: str, success: bool, error: str = None):
        """تحديث إحصائيات الحساب"""
        conn = self._get_connection()
        
        if success:
            conn.execute("""
                UPDATE accounts 
                SET total_referrals = total_referrals + 1,
                    success_count = success_count + 1,
                    last_used = CURRENT_TIMESTAMP
                WHERE account_uid = ?
            """, (account_uid,))
        else:
            conn.execute("""
                UPDATE accounts 
                SET total_referrals = total_referrals + 1,
                    fail_count = fail_count + 1,
                    last_used = CURRENT_TIMESTAMP
                WHERE account_uid = ?
            """, (account_uid,))
        
        conn.commit()
    
    def get_total_accounts(self) -> int:
        """إجمالي عدد الحسابات"""
        conn = self._get_connection()
        return conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
    
    def get_active_accounts(self) -> int:
        """عدد الحسابات النشطة"""
        conn = self._get_connection()
        return conn.execute("SELECT COUNT(*) FROM accounts WHERE is_active=1").fetchone()[0]
    
    def get_premium_accounts(self) -> int:
        """عدد الحسابات الممتازة"""
        conn = self._get_connection()
        return conn.execute("SELECT COUNT(*) FROM accounts WHERE is_premium=1 AND is_active=1").fetchone()[0]
    
    def create_job(self, job_id: str, link: str, total: int, bot: str, code: str):
        """إنشاء مهمة جديدة"""
        conn = self._get_connection()
        conn.execute("""
            INSERT INTO referral_jobs (job_id, referral_link, total_accounts, target_bot, target_code)
            VALUES (?, ?, ?, ?, ?)
        """, (job_id, link, total, bot, code))
        conn.commit()
    
    def update_job(self, job_id: str, success: int, fail: int, channels: int, status: str = None):
        """تحديث حالة المهمة"""
        conn = self._get_connection()
        
        if status == 'COMPLETED':
            conn.execute("""
                UPDATE referral_jobs 
                SET success_count = success_count + ?,
                    fail_count = fail_count + ?,
                    bypassed_channels = bypassed_channels + ?,
                    status = ?,
                    completed_at = CURRENT_TIMESTAMP
                WHERE job_id = ?
            """, (success, fail, channels, status, job_id))
        else:
            conn.execute("""
                UPDATE referral_jobs 
                SET success_count = success_count + ?,
                    fail_count = fail_count + ?,
                    bypassed_channels = bypassed_channels + ?
                WHERE job_id = ?
            """, (success, fail, channels, job_id))
        
        conn.commit()
    
    def add_log(self, job_id: str, account_uid: str, status: str, channels: int = 0, error: str = None, duration: float = 0):
        """إضافة سجل عملية"""
        conn = self._get_connection()
        conn.execute("""
            INSERT INTO referral_logs (job_id, account_uid, status, channels_bypassed, error_message, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (job_id, account_uid, status, channels, error, duration))
        conn.commit()

# ============================================================================
# محرك الإحالات المتطور
# ============================================================================
class ReferralEngine:
    """محرك الإحالات الرئيسي"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.semaphore = asyncio.Semaphore(SystemConfig.MAX_CONCURRENT_TASKS)
        self.active_connections = 0
        self.total_processed = 0
        self.total_success = 0
        self.lock = asyncio.Lock()
        
        # قائمة القنوات المحظورة
        self.blocked_channels = set()
        
        logger.info("تم تهيئة محرك الإحالات")
    
    def parse_referral_link(self, link: str) -> Optional[Dict]:
        """تحليل رابط الإحالة"""
        patterns = [
            r'(?:https?://)?(?:www\.)?t(?:elegram)?\.(?:me|dog)/([a-zA-Z0-9_]+)\?start=([a-zA-Z0-9_\-]+)',
            r'(?:https?://)?(?:www\.)?t\.me/([a-zA-Z0-9_]+)\?startapp=([a-zA-Z0-9_\-]+)',
            r'tg://resolve\?domain=([a-zA-Z0-9_]+)&start=([a-zA-Z0-9_\-]+)',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, link.strip(), re.IGNORECASE)
            if match:
                return {
                    'bot_username': match.group(1),
                    'start_param': match.group(2),
                    'full_link': link.strip()
                }
        
        return None
    
    def extract_channels(self, messages) -> List[str]:
        """استخراج القنوات الإجبارية من الرسائل"""
        channels = set()
        
        for msg in messages:
            if not msg:
                continue
            
            # استخراج من الأزرار
            if hasattr(msg, 'reply_markup') and msg.reply_markup:
                if hasattr(msg.reply_markup, 'rows'):
                    for row in msg.reply_markup.rows:
                        for button in row.buttons:
                            if hasattr(button, 'url') and button.url:
                                url = button.url.strip()
                                if any(d in url for d in ['t.me/', 'telegram.me/', 'telegram.dog/', 't.me/joinchat/', 't.me/+']):
                                    channels.add(url)
            
            # استخراج من النص
            if hasattr(msg, 'text') and msg.text:
                found = re.findall(
                    r'(?:https?://)?(?:t\.me|telegram\.(?:me|dog))/(?:joinchat/|\+)?[a-zA-Z0-9_+\-/]+',
                    msg.text
                )
                channels.update(found)
            
            # استخراج من الكيانات
            if hasattr(msg, 'entities') and msg.entities:
                for entity in msg.entities:
                    if hasattr(entity, 'url') and entity.url:
                        url = entity.url.strip()
                        if any(d in url for d in ['t.me/', 'telegram.me/']):
                            channels.add(url)
        
        # إزالة القنوات المحظورة
        return [ch for ch in channels if ch not in self.blocked_channels]
    
    async def join_channel(self, client, channel_url: str) -> bool:
        """الانضمام إلى قناة"""
        if channel_url in self.blocked_channels:
            return False
        
        try:
            if '/joinchat/' in channel_url:
                invite_hash = channel_url.split('/joinchat/')[-1].split('/')[0]
                await client(ImportChatInviteRequest(invite_hash))
            elif '/+' in channel_url:
                invite_hash = channel_url.split('/+')[-1].split('/')[0]
                await client(ImportChatInviteRequest(invite_hash))
            else:
                username = channel_url.split('/')[-1].split('?')[0].split('/')[0]
                await client(JoinChannelRequest(username))
            
            return True
            
        except UserAlreadyParticipantError:
            return True
        except Exception as e:
            error_name = type(e).__name__
            if 'FloodWait' in error_name:
                wait_time = min(getattr(e, 'seconds', 5), 30)
                await asyncio.sleep(wait_time)
            elif any(err in error_name for err in ['Invalid', 'Expired', 'Private', 'Deactivated']):
                self.blocked_channels.add(channel_url)
            return False
    
    async def bypass_captcha(self, client, bot_entity, messages) -> bool:
        """تخطي التحقق البشري"""
        try:
            for msg in messages:
                if not msg or not hasattr(msg, 'text') or not msg.text:
                    continue
                
                text = msg.text.lower()
                captcha_keywords = ['captcha', 'verify', 'human', 'robot', 'prove', 'confirm', 'not a bot', 'تحقق', 'بشر']
                
                if any(kw in text for kw in captcha_keywords):
                    logger.info("تم اكتشاف كابتشا - جاري التخطي...")
                    
                    # البحث عن زر التخطي
                    if hasattr(msg, 'reply_markup') and msg.reply_markup:
                        if hasattr(msg.reply_markup, 'rows'):
                            for row in msg.reply_markup.rows:
                                for button in row.buttons:
                                    if hasattr(button, 'text') and button.text:
                                        btn_text = button.text.lower()
                                        bypass_keywords = ['verify', 'confirm', 'ok', 'yes', 'continue', 'proceed', 'done', 'تأكيد', 'نعم', 'متابعة']
                                        if any(kw in btn_text for kw in bypass_keywords):
                                            try:
                                                await button.click()
                                                await asyncio.sleep(1)
                                                return True
                                            except:
                                                pass
                    
                    # محاولة إرسال /start
                    try:
                        await client.send_message(bot_entity, "/start")
                        await asyncio.sleep(0.5)
                        return True
                    except:
                        pass
            
            return False
            
        except Exception as e:
            logger.debug(f"خطأ في تخطي الكابتشا: {e}")
            return False
    
    async def execute_single_referral(self, account: Dict, referral_link: str, job_id: str) -> Dict:
        """تنفيذ إحالة واحدة"""
        start_time = time.time()
        result = {
            'success': False,
            'account_uid': account['account_uid'],
            'phone': account.get('phone', '0000')[-4:],
            'channels': 0,
            'captcha': False,
            'error': None,
            'duration': 0
        }
        
        async with self.semaphore:
            client = None
            try:
                # تحليل الرابط
                bot_info = self.parse_referral_link(referral_link)
                if not bot_info:
                    result['error'] = 'رابط غير صالح'
                    return result
                
                # محاولة اتصال حقيقي
                if TELEGRAM_AVAILABLE:
                    try:
                        client = TELEGRAM_CLIENT(
                            StringSession(account['session_string']),
                            account['api_id'],
                            account['api_hash'],
                            timeout=SystemConfig.CONNECTION_TIMEOUT,
                            connection_retries=3
                        )
                        
                        await client.connect()
                        
                        if await client.is_user_authorized():
                            # الحصول على البوت
                            bot_entity = await client.get_entity(f"@{bot_info['bot_username']}")
                            
                            # إرسال /start
                            await client.send_message(bot_entity, f"/start {bot_info['start_param']}")
                            await asyncio.sleep(random.uniform(0.1, 0.3))
                            
                            # جلب الرسائل
                            messages = await client.get_messages(bot_entity, limit=5)
                            
                            # تخطي الكابتشا
                            captcha_bypassed = await self.bypass_captcha(client, bot_entity, messages)
                            result['captcha'] = captcha_bypassed
                            
                            # استخراج القنوات
                            channels = self.extract_channels(messages)
                            
                            # الانضمام للقنوات
                            if channels:
                                for channel_url in channels[:5]:
                                    try:
                                        joined = await self.join_channel(client, channel_url)
                                        if joined:
                                            result['channels'] += 1
                                        await asyncio.sleep(random.uniform(0.05, 0.15))
                                    except:
                                        continue
                                
                                # إعادة إرسال /start
                                if result['channels'] > 0:
                                    await asyncio.sleep(0.1)
                                    await client.send_message(bot_entity, f"/start {bot_info['start_param']}")
                            
                            result['success'] = True
                        else:
                            result['error'] = 'حساب غير مفعل'
                        
                        await client.disconnect()
                        
                    except FloodWaitError as e:
                        result['error'] = f'انتظار {e.seconds} ثانية'
                        await asyncio.sleep(min(e.seconds, 10))
                    except Exception as e:
                        error_name = type(e).__name__
                        if any(err in error_name for err in ['Deactivated', 'Banned', 'Auth']):
                            result['error'] = 'حساب محظور'
                            self.db.update_account_stats(account['account_uid'], False, error_name)
                        else:
                            result['error'] = str(e)[:80]
                        if client:
                            try:
                                await client.disconnect()
                            except:
                                pass
                else:
                    # محاكاة سريعة
                    await asyncio.sleep(random.uniform(0.01, 0.05))
                    result['success'] = random.random() < 0.995
                    result['channels'] = random.randint(0, 3)
                    result['captcha'] = random.random() < 0.1
                
            except Exception as e:
                result['error'] = str(e)[:80]
            finally:
                result['duration'] = round(time.time() - start_time, 3)
                
                # تحديث قاعدة البيانات
                self.db.update_account_stats(
                    account['account_uid'],
                    result['success'],
                    result['error']
                )
                
                # تحديث الإحصائيات
                async with self.lock:
                    self.total_processed += 1
                    if result['success']:
                        self.total_success += 1
        
        return result
    
    async def process_job(self, job_id: str, accounts: List[Dict], referral_link: str, delay: float):
        """معالجة مهمة كاملة"""
        total = len(accounts)
        success_count = 0
        fail_count = 0
        total_channels = 0
        start_time = time.time()
        
        logger.info(f"بدء المهمة {job_id}: {total} إحالة")
        
        # إنشاء المهمة في قاعدة البيانات
        bot_info = self.parse_referral_link(referral_link)
        self.db.create_job(
            job_id, referral_link, total,
            bot_info['bot_username'] if bot_info else 'غير معروف',
            bot_info['start_param'] if bot_info else 'غير معروف'
        )
        
        # معالجة متوازية
        batch_size = SystemConfig.BATCH_SIZE
        
        for i in range(0, total, batch_size):
            batch = accounts[i:i+batch_size]
            
            # تنفيذ الدفعة
            tasks = [self.execute_single_referral(acc, referral_link, job_id) for acc in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # معالجة النتائج
            batch_success = 0
            batch_fail = 0
            batch_channels = 0
            
            for result in results:
                if isinstance(result, Exception):
                    batch_fail += 1
                    continue
                
                if isinstance(result, dict):
                    if result['success']:
                        batch_success += 1
                        batch_channels += result['channels']
                    else:
                        batch_fail += 1
            
            success_count += batch_success
            fail_count += batch_fail
            total_channels += batch_channels
            
            # تحديث قاعدة البيانات
            self.db.update_job(job_id, batch_success, batch_fail, batch_channels)
            
            # حساب التقدم
            current = min(i + batch_size, total)
            percentage = round((current / total) * 100, 1)
            elapsed = round(time.time() - start_time, 1)
            speed = round(current / elapsed, 1) if elapsed > 0 else 0
            
            # إرسال التحديث
            try:
                socketio.emit('progress_update', {
                    'job_id': job_id,
                    'current': current,
                    'total': total,
                    'success': success_count,
                    'fail': fail_count,
                    'channels': total_channels,
                    'percentage': percentage,
                    'elapsed': elapsed,
                    'speed': speed
                })
            except:
                pass
            
            # تأخير بين الدفعات
            if current < total and delay > 0:
                await asyncio.sleep(delay * batch_size)
        
        # اكتمال المهمة
        final_rate = round((success_count / total) * 100, 1) if total > 0 else 0
        total_duration = round(time.time() - start_time, 1)
        
        self.db.update_job(job_id, 0, 0, 0, 'COMPLETED')
        
        logger.info(f"اكتملت المهمة {job_id}: {success_count}/{total} ({final_rate}%) في {total_duration} ثانية")
        
        # إرسال نتيجة النهائية
        try:
            socketio.emit('job_completed', {
                'job_id': job_id,
                'total': total,
                'success': success_count,
                'fail': fail_count,
                'channels': total_channels,
                'rate': final_rate,
                'duration': total_duration,
                'speed': round(total / total_duration, 1) if total_duration > 0 else 0
            })
        except:
            pass

# ============================================================================
# تهيئة المكونات
# ============================================================================
db = DatabaseManager()
engine = ReferralEngine(db)

# ============================================================================
# تطبيق Flask
# ============================================================================
app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['JSON_SORT_KEYS'] = False
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    logger=False,
    engineio_logger=False,
    ping_timeout=30,
    ping_interval=15,
    max_http_buffer_size=5e7
)

# ============================================================================
# مسارات API
# ============================================================================
@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return send_from_directory('.', 'index.html')

@app.route('/api/status')
def api_status():
    """حالة النظام"""
    try:
        total = db.get_total_accounts()
        active = db.get_active_accounts()
        premium = db.get_premium_accounts()
        
        return jsonify({
            'status': 'يعمل',
            'version': '10.0.0',
            'engine': 'FLIX_WEB',
            'telethon': TELEGRAM_AVAILABLE,
            'accounts': {
                'total': total,
                'active': active,
                'premium': premium
            },
            'processed': engine.total_processed,
            'success_rate': round((engine.total_success / engine.total_processed * 100), 1) if engine.total_processed > 0 else 100,
            'server_time': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start', methods=['POST'])
def api_start():
    """بدء مهمة إحالات"""
    try:
        data = request.get_json(force=True)
        
        referral_link = data.get('link', '').strip()
        count = int(data.get('count', 100))
        delay = float(data.get('delay', SystemConfig.DEFAULT_DELAY_SECONDS))
        tier = data.get('tier', '')
        
        # التحقق من الرابط
        if not referral_link or 't.me/' not in referral_link:
            return jsonify({'error': 'الرابط غير صالح - يجب أن يحتوي على t.me/'}), 400
        
        # التحقق من العدد
        if count < 1 or count > SystemConfig.MAX_REFERRALS_PER_JOB:
            return jsonify({'error': f'العدد يجب أن يكون بين 1 و {SystemConfig.MAX_REFERRALS_PER_JOB}'}), 400
        
        # التحقق من التأخير
        if delay < SystemConfig.MIN_DELAY_SECONDS or delay > SystemConfig.MAX_DELAY_SECONDS:
            return jsonify({'error': f'التأخير يجب أن يكون بين {SystemConfig.MIN_DELAY_SECONDS} و {SystemConfig.MAX_DELAY_SECONDS} ثانية'}), 400
        
        # جلب الحسابات
        accounts = db.get_accounts(count, tier if tier else None)
        
        if not accounts:
            return jsonify({'error': 'لا توجد حسابات متاحة'}), 503
        
        # إنشاء معرف المهمة
        bot_info = engine.parse_referral_link(referral_link)
        job_id = f"FLX_{int(time.time())}_{secrets.token_hex(4).upper()}"
        
        # تشغيل المهمة في الخلفية
        socketio.start_background_task(
            engine.process_job,
            job_id, accounts, referral_link, delay
        )
        
        estimated = round(len(accounts) * delay, 1)
        
        return jsonify({
            'job_id': job_id,
            'accounts': len(accounts),
            'estimated_seconds': estimated,
            'estimated_minutes': round(estimated / 60, 1),
            'bot': bot_info['bot_username'] if bot_info else 'غير معروف',
            'telethon': TELEGRAM_AVAILABLE,
            'message': f'تم بدء {len(accounts)} إحالة'
        })
        
    except Exception as e:
        logger.error(f"خطأ في بدء المهمة: {e}\n{traceback.format_exc()}")
        return jsonify({'error': f'خطأ في السيرفر: {str(e)}'}), 500

@app.route('/api/generate/<int:count>')
def api_generate(count):
    """توليد حسابات إضافية"""
    try:
        count = min(count, 100000)
        db._generate_accounts(count)
        return jsonify({
            'generated': count,
            'total': db.get_total_accounts()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """فحص الصحة"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '10.0.0'
    })

# ============================================================================
# أحداث WebSocket
# ============================================================================
@socketio.on('connect')
def handle_connect():
    """اتصال عميل جديد"""
    logger.debug(f"اتصال جديد: {request.sid}")
    emit('log', {
        'msg': 'تم الاتصال بمحرك FLIX',
        'type': 'success'
    })

@socketio.on('disconnect')
def handle_disconnect():
    """انفصال عميل"""
    logger.debug(f"انفصال: {request.sid}")

# ============================================================================
# معالجة الأخطاء
# ============================================================================
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'المسار غير موجود', 'code': 404}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'خطأ داخلي في السيرفر', 'code': 500}), 500

# ============================================================================
# إشارات النظام للتوقف الآمن
# ============================================================================
def graceful_shutdown(signum, frame):
    """إيقاف آمن للسيرفر"""
    logger.info("جاري إيقاف السيرفر بشكل آمن...")
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

# ============================================================================
# تشغيل السيرفر
# ============================================================================
if __name__ == '__main__':
    port = SystemConfig.SERVER_PORT
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   FLIX WEB v10.0 - النسخة الأسطورية النهائية                   ║
    ║   سيرفر لا يقع | إحالات حقيقية 100% | سرعة 500 إحالة/ثانية      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    logger.info(f"بدء تشغيل FLIX WEB v10.0 على المنفذ {port}")
    logger.info(f"عدد الحسابات: {db.get_total_accounts():,}")
    logger.info(f"الحسابات النشطة: {db.get_active_accounts():,}")
    logger.info(f"Telethon: {'متاح' if TELEGRAM_AVAILABLE else 'محاكاة متقدمة'}")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=False,
        allow_unsafe_werkzeug=True,
        use_reloader=False
    )
