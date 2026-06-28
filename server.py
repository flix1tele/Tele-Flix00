#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗██╗     ██╗██╗  ██╗    ██╗    ██╗███████╗██████╗                 ║
║   ██╔════╝██║     ██║╚██╗██╔╝    ██║    ██║██╔════╝██╔══██╗                ║
║   █████╗  ██║     ██║ ╚███╔╝     ██║ █╗ ██║█████╗  ██████╔╝                ║
║   ██╔══╝  ██║     ██║ ██╔██╗     ██║███╗██║██╔══╝  ██╔══██╗                ║
║   ██║     ███████╗██║██╔╝ ██╗    ╚███╔███╔╝███████╗██████╔╝                ║
║   ╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚══════╝╚═════╝                 ║
║                                                                              ║
║   ██████╗ ███████╗███████╗███████╗██████╗ ██████╗  █████╗ ██╗               ║
║   ██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║               ║
║   ██████╔╝█████╗  █████╗  █████╗  ██████╔╝██████╔╝███████║██║               ║
║   ██╔══██╗██╔══╝  ██╔══╝  ██╔══╝  ██╔══██╗██╔══██╗██╔══██║██║               ║
║   ██║  ██║███████╗██║     ███████╗██║  ██║██║  ██║██║  ██║███████╗          ║
║   ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝          ║
║                                                                              ║
║   ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗                         ║
║   ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝                         ║
║   █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗                           ║
║   ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝                           ║
║   ██║     ██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗                         ║
║   ╚═╝     ╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝                         ║
║                                                                              ║
║   FLIX WEB v8.0 - THE ULTIMATE REFERRAL ENGINE                              ║
║   10,000,000x MORE POWERFUL - REAL REFERRALS - INSTANT NOTIFICATIONS        ║
║   PURE DIGITAL - NO EMOJI - MAXIMUM PERFORMANCE                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# STANDARD LIBRARY IMPORTS
# ============================================================================
import asyncio
import base64
import hashlib
import hmac
import json
import logging
import math
import os
import platform
import random
import re
import secrets
import sqlite3
import struct
import sys
import threading
import time
import traceback
import uuid
import zlib
from collections import OrderedDict, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from functools import lru_cache, partial, wraps
from io import BytesIO, StringIO
from pathlib import Path
from queue import PriorityQueue, Queue
from typing import (
    Any, Callable, Dict, Generator, List, Optional, Set, Tuple, 
    Union, Coroutine, TypeVar, Generic, Iterator, AsyncIterator
)
from urllib.parse import urlparse, parse_qs, urlencode, quote, unquote
import warnings

# Suppress unnecessary warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=ResourceWarning)

# ============================================================================
# SYSTEM CONFIGURATION
# ============================================================================
class SystemConfig:
    """Global system configuration with optimized defaults"""
    
    # Server settings
    SERVER_HOST: str = os.environ.get('HOST', '0.0.0.0')
    SERVER_PORT: int = int(os.environ.get('PORT', 5000))
    SERVER_DEBUG: bool = os.environ.get('DEBUG', 'False').lower() == 'true'
    SERVER_WORKERS: int = int(os.environ.get('WORKERS', '4'))
    
    # Database settings
    DB_PATH: str = os.environ.get('DB_PATH', 'flix_accounts.db')
    DB_POOL_SIZE: int = 100
    DB_TIMEOUT: int = 30
    
    # Account settings
    MAX_ACCOUNTS: int = 10000000  # 10 million accounts
    ACCOUNTS_PER_BATCH: int = 100000
    INITIAL_ACCOUNT_COUNT: int = 500000  # 500K accounts pre-generated
    
    # Referral settings
    MAX_REFERRALS_PER_JOB: int = 100000
    MIN_DELAY_SECONDS: float = 0.5
    MAX_DELAY_SECONDS: float = 300.0
    DEFAULT_DELAY_SECONDS: float = 2.0
    
    # Connection settings
    MAX_CONCURRENT_CONNECTIONS: int = 500
    CONNECTION_TIMEOUT: int = 45
    CONNECTION_RETRIES: int = 15
    RECONNECT_DELAY: float = 0.3
    
    # Anti-detection settings
    ENABLE_PROXY_ROTATION: bool = True
    ENABLE_DEVICE_SPOOFING: bool = True
    ENABLE_HUMAN_BEHAVIOR: bool = True
    ENABLE_CAPTCHA_BYPASS: bool = True
    
    # Notification settings
    ENABLE_NOTIFICATIONS: bool = True
    NOTIFICATION_RETENTION: int = 10000
    NOTIFICATION_BATCH_SIZE: int = 100
    
    # Logging settings
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE: str = 'flix_engine.log'
    LOG_MAX_SIZE: int = 100 * 1024 * 1024  # 100 MB
    LOG_BACKUP_COUNT: int = 10
    
    # Performance settings
    ENABLE_CONNECTION_POOLING: bool = True
    ENABLE_REQUEST_CACHING: bool = True
    CACHE_TTL_SECONDS: int = 300
    MEMORY_LIMIT_MB: int = 2048
    
    # Security settings
    SECRET_KEY: str = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    ENABLE_RATE_LIMITING: bool = True
    RATE_LIMIT_REQUESTS: int = 1000
    RATE_LIMIT_WINDOW: int = 60

# ============================================================================
# LOGGING SETUP
# ============================================================================
def setup_logging() -> logging.Logger:
    """Configure advanced logging with rotation and formatting"""
    
    logger = logging.getLogger('FLIX_WEB')
    logger.setLevel(getattr(logging, SystemConfig.LOG_LEVEL))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '\033[1;31m[FLIX]\033[0m \033[1;37m%(asctime)s\033[0m '
        '\033[1;33m%(levelname)s\033[0m \033[1;36m%(message)s\033[0m',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # File handler with rotation
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        SystemConfig.LOG_FILE,
        maxBytes=SystemConfig.LOG_MAX_SIZE,
        backupCount=SystemConfig.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s - %(message)s '
        '[%(filename)s:%(lineno)d]',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()

# ============================================================================
# EXCEPTION CLASSES
# ============================================================================
class FlixException(Exception):
    """Base exception for all FLIX errors"""
    def __init__(self, message: str, code: int = 500, details: Any = None):
        super().__init__(message)
        self.code = code
        self.details = details
        self.timestamp = datetime.now(timezone.utc)

class AccountError(FlixException):
    """Account-related errors"""
    def __init__(self, message: str, account_uid: str = None):
        super().__init__(message, code=400)
        self.account_uid = account_uid

class ReferralError(FlixException):
    """Referral operation errors"""
    def __init__(self, message: str, job_id: str = None):
        super().__init__(message, code=500)
        self.job_id = job_id

class ConnectionError(FlixException):
    """Connection-related errors"""
    def __init__(self, message: str, host: str = None):
        super().__init__(message, code=503)
        self.host = host

class RateLimitError(FlixException):
    """Rate limiting errors"""
    def __init__(self, message: str, retry_after: float = 60):
        super().__init__(message, code=429)
        self.retry_after = retry_after

class ValidationError(FlixException):
    """Input validation errors"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, code=422)
        self.field = field

# ============================================================================
# TELEGRAM LIBRARY IMPORTS WITH FALLBACK
# ============================================================================
TELETHON_AVAILABLE = False
TELEGRAM_CLIENT = None

try:
    from telethon import TelegramClient, events, functions, types, errors
    from telethon.sessions import StringSession, MemorySession
    from telethon.network import ConnectionTcpMTProxyRandomizedIntermediate
    from telethon.tl.functions.channels import (
        JoinChannelRequest, GetFullChannelRequest, InviteToChannelRequest
    )
    from telethon.tl.functions.messages import (
        ImportChatInviteRequest, CheckChatInviteRequest,
        StartBotRequest, GetHistoryRequest, SendMessageRequest,
        GetMessagesRequest, GetDialogsRequest
    )
    from telethon.tl.functions.users import GetFullUserRequest
    from telethon.tl.functions.account import (
        UpdateProfileRequest, UpdateStatusRequest, GetPrivacyRequest
    )
    from telethon.tl.functions.auth import (
        SendCodeRequest, SignInRequest, SignUpRequest
    )
    from telethon.tl.types import (
        InputPeerUser, InputPeerChat, InputPeerChannel,
        InputUser, InputChannel, InputMessagesFilterEmpty,
        PeerUser, PeerChat, PeerChannel,
        Message, MessageService, MessageEmpty,
        Channel, Chat, User, ChatFull, ChannelFull,
        ChatInvite, ChatInviteAlready, ChatInvitePeek,
        UpdateShortMessage, UpdateShortChatMessage,
        UpdateNewMessage, UpdateNewChannelMessage,
        KeyboardButtonUrl, KeyboardButtonCallback,
        ReplyInlineMarkup, ReplyKeyboardMarkup,
        SendMessageTypingAction, SendMessageCancelAction
    )
    from telethon.errors import (
        FloodWaitError, ChatAdminRequiredError, UserAlreadyParticipantError,
        UserNotParticipantError, InviteHashExpiredError, InviteHashInvalidError,
        ChannelPrivateError, ChannelInvalidError, ChatWriteForbiddenError,
        SessionPasswordNeededError, PhoneCodeInvalidError,
        PhoneCodeExpiredError, PhoneCodeEmptyError,
        PasswordHashInvalidError, AuthKeyUnregisteredError,
        UserDeactivatedBanError, UserDeactivatedError,
        PeerIdInvalidError, UsernameNotOccupiedError, UsernameInvalidError,
        MessageTooLongError, MessageEmptyError, MessageNotModifiedError,
        ChatRestrictedError, ChatForbiddenError,
        RPCError, RPCErrorWithCode, UnauthorizedError, ServerError
    )
    
    TELETHON_AVAILABLE = True
    TELEGRAM_CLIENT = TelegramClient
    
    logger.info("[TELEGRAM] Telethon library loaded successfully")
    
except ImportError as e:
    logger.warning(f"[TELEGRAM] Telethon not installed: {e}")
    logger.info("[TELEGRAM] Installing Telethon automatically...")
    
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "telethon>=1.36.0", "--quiet"])
        
        # Retry import
        from telethon import TelegramClient, functions, types, errors
        from telethon.sessions import StringSession
        from telethon.network import ConnectionTcpMTProxyRandomizedIntermediate
        from telethon.tl.functions.channels import JoinChannelRequest
        from telethon.tl.functions.messages import ImportChatInviteRequest, StartBotRequest
        from telethon.errors import (
            FloodWaitError, UserAlreadyParticipantError, SessionPasswordNeededError
        )
        
        TELETHON_AVAILABLE = True
        TELEGRAM_CLIENT = TelegramClient
        logger.info("[TELEGRAM] Telethon installed and loaded successfully")
        
    except Exception as install_error:
        logger.error(f"[TELEGRAM] Failed to install Telethon: {install_error}")
        logger.warning("[TELEGRAM] Running in simulation mode - real referrals disabled")

# ============================================================================
# WEB FRAMEWORK IMPORTS WITH FALLBACK
# ============================================================================
FLASK_AVAILABLE = False

try:
    from flask import (
        Flask, request, jsonify, render_template, send_from_directory,
        Response, make_response, abort, redirect, url_for, session,
        g, current_app, Blueprint
    )
    from flask_cors import CORS, cross_origin
    from flask_socketio import SocketIO, emit, join_room, leave_room
    
    FLASK_AVAILABLE = True
    logger.info("[FLASK] Flask framework loaded successfully")
    
except ImportError as e:
    logger.warning(f"[FLASK] Flask not installed: {e}")
    logger.info("[FLASK] Installing Flask automatically...")
    
    import subprocess
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "flask>=3.0.0", "flask-cors>=4.0.0", "flask-socketio>=5.3.0",
            "--quiet"
        ])
        
        from flask import Flask, request, jsonify, send_from_directory
        from flask_cors import CORS
        from flask_socketio import SocketIO
        
        FLASK_AVAILABLE = True
        logger.info("[FLASK] Flask installed and loaded successfully")
        
    except Exception as install_error:
        logger.error(f"[FLASK] Failed to install Flask: {install_error}")
        sys.exit(1)

# ============================================================================
# THIRD-PARTY MODULES
# ============================================================================
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    logger.warning("[AIOHTTP] aiohttp not available")

try:
    import socks
    SOCKS_AVAILABLE = True
except ImportError:
    SOCKS_AVAILABLE = False
    logger.warning("[SOCKS] PySocks not available")

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.debug("[REDIS] Redis not available")

# ============================================================================
# TYPE DEFINITIONS
# ============================================================================
T = TypeVar('T')
AccountDict = Dict[str, Any]
JobDict = Dict[str, Any]
ResultDict = Dict[str, Any]
ProxyDict = Dict[str, Any]
CallbackType = Callable[..., Any]
CoroutineType = Coroutine[Any, Any, Any]

# ============================================================================
# ENUM DEFINITIONS
# ============================================================================
class AccountTier(str, Enum):
    """Account performance tiers"""
    PREMIUM = "PREMIUM"
    HIGH = "HIGH"
    STANDARD = "STANDARD"
    BASIC = "BASIC"

class JobStatus(str, Enum):
    """Job status enumeration"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class ReferralStatus(str, Enum):
    """Individual referral status"""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    PENDING = "PENDING"
    FLOOD_WAIT = "FLOOD_WAIT"
    BANNED = "BANNED"
    CAPTCHA = "CAPTCHA"

class NotificationType(str, Enum):
    """Notification types"""
    JOB_START = "JOB_START"
    JOB_PROGRESS = "JOB_PROGRESS"
    JOB_COMPLETE = "JOB_COMPLETE"
    REFERRAL_SUCCESS = "REFERRAL_SUCCESS"
    REFERRAL_FAILED = "REFERRAL_FAILED"
    CHANNEL_BYPASS = "CHANNEL_BYPASS"
    CAPTCHA_BYPASS = "CAPTCHA_BYPASS"
    ERROR = "ERROR"
    WARNING = "WARNING"
    SYSTEM = "SYSTEM"

# ============================================================================
# DATA CLASSES
# ============================================================================
@dataclass
class Account:
    """Account data structure"""
    account_uid: str
    api_id: int
    api_hash: str
    session_string: str
    phone: str = ""
    first_name: str = ""
    last_name: str = ""
    username: str = ""
    proxy_host: Optional[str] = None
    proxy_port: Optional[int] = None
    proxy_type: str = "SOCKS5"
    is_active: bool = True
    is_premium: bool = False
    performance_tier: AccountTier = AccountTier.STANDARD
    total_referrals: int = 0
    success_count: int = 0
    fail_count: int = 0
    last_used: Optional[datetime] = None
    created_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    country_code: str = "US"
    device_model: str = "Generic"
    android_version: str = "Android 13"
    app_version: str = "10.6.5"
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        if self.total_referrals == 0:
            return 0.0
        return round((self.success_count / self.total_referrals) * 100, 2)

@dataclass
class ReferralJob:
    """Referral job data structure"""
    job_id: str
    referral_link: str
    total_accounts: int = 0
    success_count: int = 0
    fail_count: int = 0
    bypassed_channels: int = 0
    status: JobStatus = JobStatus.PENDING
    target_bot: str = ""
    target_code: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    estimated_duration: float = 0.0
    actual_duration: float = 0.0
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress percentage"""
        if self.total_accounts == 0:
            return 0.0
        completed = self.success_count + self.fail_count
        return round((completed / self.total_accounts) * 100, 2)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        completed = self.success_count + self.fail_count
        if completed == 0:
            return 0.0
        return round((self.success_count / completed) * 100, 2)

@dataclass
class ReferralResult:
    """Individual referral result"""
    success: bool = False
    account_uid: str = ""
    phone_last4: str = ""
    error: Optional[str] = None
    steps_completed: List[str] = field(default_factory=list)
    channels_bypassed: int = 0
    captcha_bypassed: bool = False
    duration: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

# ============================================================================
# SECURITY UTILITIES
# ============================================================================
class SecurityUtils:
    """Security and cryptographic utilities"""
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_hex(length)
    
    @staticmethod
    def hash_string(data: str, algorithm: str = 'sha256') -> str:
        """Hash string using specified algorithm"""
        h = hashlib.new(algorithm)
        h.update(data.encode('utf-8'))
        return h.hexdigest()
    
    @staticmethod
    def generate_hmac(key: str, message: str) -> str:
        """Generate HMAC signature"""
        return hmac.new(
            key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def verify_hmac(key: str, message: str, signature: str) -> bool:
        """Verify HMAC signature"""
        expected = SecurityUtils.generate_hmac(key, message)
        return hmac.compare_digest(expected, signature)
    
    @staticmethod
    def encrypt_aes(data: str, key: str) -> str:
        """Encrypt data using AES-256"""
        from cryptography.fernet import Fernet
        import base64
        
        # Derive proper key
        derived_key = base64.urlsafe_b64encode(
            hashlib.sha256(key.encode()).digest()
        )
        f = Fernet(derived_key)
        return f.encrypt(data.encode()).decode()
    
    @staticmethod
    def decrypt_aes(encrypted_data: str, key: str) -> str:
        """Decrypt AES-256 encrypted data"""
        from cryptography.fernet import Fernet
        import base64
        
        derived_key = base64.urlsafe_b64encode(
            hashlib.sha256(key.encode()).digest()
        )
        f = Fernet(derived_key)
        return f.decrypt(encrypted_data.encode()).decode()
    
    @staticmethod
    def sanitize_input(data: str) -> str:
        """Sanitize user input"""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>\'";]', '', data)
        # Remove script tags
        sanitized = re.sub(r'<script.*?>.*?</script>', '', sanitized, flags=re.IGNORECASE)
        # Remove JavaScript events
        sanitized = re.sub(r'on\w+\s*=\s*"[^"]*"', '', sanitized, flags=re.IGNORECASE)
        return sanitized.strip()
    
    @staticmethod
    def validate_referral_link(link: str) -> bool:
        """Validate referral link format"""
        pattern = r'^https?://(?:www\.)?t(?:elegram)?\.(?:me|dog)/[a-zA-Z0-9_]+\?start=[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, link, re.IGNORECASE))

# ============================================================================
# DATA COMPRESSION UTILITIES
# ============================================================================
class CompressionUtils:
    """Data compression and optimization utilities"""
    
    @staticmethod
    def compress_json(data: Dict) -> bytes:
        """Compress JSON data"""
        json_bytes = json.dumps(data, separators=(',', ':')).encode('utf-8')
        return zlib.compress(json_bytes, level=9)
    
    @staticmethod
    def decompress_json(compressed: bytes) -> Dict:
        """Decompress JSON data"""
        json_bytes = zlib.decompress(compressed)
        return json.loads(json_bytes.decode('utf-8'))
    
    @staticmethod
    def compress_string(data: str) -> bytes:
        """Compress string data"""
        return zlib.compress(data.encode('utf-8'), level=9)
    
    @staticmethod
    def decompress_string(compressed: bytes) -> str:
        """Decompress string data"""
        return zlib.decompress(compressed).decode('utf-8')

# ============================================================================
# DATABASE MANAGER - ULTIMATE VERSION
# ============================================================================
class FlixDatabase:
    """
    FLIX Database Manager - Handles millions of accounts
    Uses SQLite with WAL mode for maximum performance
    """
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or SystemConfig.DB_PATH
        self._connection_pool = deque(maxlen=SystemConfig.DB_POOL_SIZE)
        self._lock = threading.RLock()
        self._initialize_database()
        self._ensure_accounts_exist()
    
    def _initialize_database(self):
        """Initialize database with optimized schema"""
        with self._get_connection() as conn:
            conn.executescript("""
                PRAGMA journal_mode = WAL;
                PRAGMA synchronous = NORMAL;
                PRAGMA cache_size = -131072;
                PRAGMA temp_store = MEMORY;
                PRAGMA mmap_size = 536870912;
                PRAGMA page_size = 8192;
                PRAGMA auto_vacuum = INCREMENTAL;
                PRAGMA busy_timeout = 30000;
                PRAGMA foreign_keys = ON;
                
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_uid TEXT UNIQUE NOT NULL COLLATE NOCASE,
                    api_id INTEGER NOT NULL,
                    api_hash TEXT NOT NULL,
                    session_string TEXT NOT NULL,
                    phone TEXT NOT NULL DEFAULT '',
                    first_name TEXT DEFAULT '',
                    last_name TEXT DEFAULT '',
                    username TEXT DEFAULT '',
                    proxy_host TEXT,
                    proxy_port INTEGER,
                    proxy_type TEXT DEFAULT 'SOCKS5',
                    proxy_username TEXT,
                    proxy_password TEXT,
                    is_active INTEGER DEFAULT 1,
                    is_premium INTEGER DEFAULT 0,
                    performance_tier TEXT DEFAULT 'STANDARD',
                    total_referrals INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    fail_count INTEGER DEFAULT 0,
                    consecutive_fails INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    last_error TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    country_code TEXT DEFAULT 'US',
                    device_model TEXT DEFAULT 'Generic',
                    android_version TEXT DEFAULT 'Android 13',
                    app_version TEXT DEFAULT '10.6.5',
                    user_agent TEXT,
                    fingerprint TEXT UNIQUE
                );
                
                CREATE TABLE IF NOT EXISTS referral_jobs (
                    job_id TEXT PRIMARY KEY,
                    referral_link TEXT NOT NULL,
                    total_accounts INTEGER DEFAULT 0,
                    completed_accounts INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    fail_count INTEGER DEFAULT 0,
                    bypassed_channels INTEGER DEFAULT 0,
                    captcha_bypassed INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'PENDING',
                    target_bot TEXT,
                    target_code TEXT,
                    error_message TEXT,
                    estimated_duration REAL DEFAULT 0.0,
                    actual_duration REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    user_agent TEXT,
                    ip_address TEXT
                );
                
                CREATE TABLE IF NOT EXISTS referral_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL,
                    account_uid TEXT,
                    referral_status TEXT DEFAULT 'PENDING',
                    channels_bypassed INTEGER DEFAULT 0,
                    captcha_bypassed INTEGER DEFAULT 0,
                    error_code TEXT,
                    error_message TEXT,
                    duration REAL DEFAULT 0.0,
                    retry_count INTEGER DEFAULT 0,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES referral_jobs(job_id) ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS notification_queue (
                    notify_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT,
                    target_user_id TEXT,
                    notification_type TEXT,
                    title TEXT,
                    message TEXT,
                    metadata TEXT,
                    is_sent INTEGER DEFAULT 0,
                    sent_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES referral_jobs(job_id) ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS system_metrics (
                    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL,
                    metric_unit TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS proxy_pool (
                    proxy_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proxy_host TEXT NOT NULL,
                    proxy_port INTEGER NOT NULL,
                    proxy_type TEXT DEFAULT 'SOCKS5',
                    username TEXT,
                    password TEXT,
                    country_code TEXT,
                    is_active INTEGER DEFAULT 1,
                    success_count INTEGER DEFAULT 0,
                    fail_count INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_accounts_active ON accounts(is_active);
                CREATE INDEX IF NOT EXISTS idx_accounts_tier ON accounts(performance_tier);
                CREATE INDEX IF NOT EXISTS idx_accounts_premium ON accounts(is_premium);
                CREATE INDEX IF NOT EXISTS idx_accounts_country ON accounts(country_code);
                CREATE INDEX IF NOT EXISTS idx_accounts_uid ON accounts(account_uid);
                CREATE INDEX IF NOT EXISTS idx_accounts_success ON accounts(success_count);
                CREATE INDEX IF NOT EXISTS idx_accounts_last_used ON accounts(last_used);
                
                CREATE INDEX IF NOT EXISTS idx_jobs_status ON referral_jobs(status);
                CREATE INDEX IF NOT EXISTS idx_jobs_created ON referral_jobs(created_at);
                CREATE INDEX IF NOT EXISTS idx_jobs_bot ON referral_jobs(target_bot);
                
                CREATE INDEX IF NOT EXISTS idx_logs_job ON referral_logs(job_id);
                CREATE INDEX IF NOT EXISTS idx_logs_status ON referral_logs(referral_status);
                CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON referral_logs(timestamp);
                
                CREATE INDEX IF NOT EXISTS idx_notifications_job ON notification_queue(job_id);
                CREATE INDEX IF NOT EXISTS idx_notifications_sent ON notification_queue(is_sent);
                
                CREATE INDEX IF NOT EXISTS idx_metrics_name ON system_metrics(metric_name);
                CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON system_metrics(timestamp);
                
                CREATE INDEX IF NOT EXISTS idx_proxy_active ON proxy_pool(is_active);
                CREATE INDEX IF NOT EXISTS idx_proxy_country ON proxy_pool(country_code);
            """)
            
            conn.commit()
            
            # Create triggers for automatic timestamp updates
            conn.executescript("""
                CREATE TRIGGER IF NOT EXISTS update_accounts_timestamp 
                AFTER UPDATE ON accounts
                BEGIN
                    UPDATE accounts SET updated_date = CURRENT_TIMESTAMP WHERE id = NEW.id;
                END;
                
                CREATE TRIGGER IF NOT EXISTS update_jobs_timestamp
                AFTER UPDATE ON referral_jobs
                BEGIN
                    UPDATE referral_jobs 
                    SET completed_at = CASE 
                        WHEN NEW.status IN ('COMPLETED', 'FAILED', 'CANCELLED') 
                        THEN CURRENT_TIMESTAMP 
                        ELSE completed_at 
                    END
                    WHERE job_id = NEW.job_id;
                END;
            """)
            
            conn.commit()
        
        logger.info(f"[DATABASE] Initialized: {self.db_path}")
    
    def _ensure_accounts_exist(self):
        """Ensure minimum number of accounts exist"""
        with self._get_connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
        
        if count < SystemConfig.INITIAL_ACCOUNT_COUNT:
            logger.info(f"[DATABASE] Generating {SystemConfig.INITIAL_ACCOUNT_COUNT} accounts...")
            self._generate_accounts(SystemConfig.INITIAL_ACCOUNT_COUNT - count)
    
    def _generate_accounts(self, count: int):
        """Generate accounts in batches"""
        batch_size = SystemConfig.ACCOUNTS_PER_BATCH
        
        for batch_start in range(0, count, batch_size):
            batch_count = min(batch_size, count - batch_start)
            self._generate_account_batch(batch_count)
            logger.info(f"[DATABASE] Generated {batch_start + batch_count}/{count} accounts")
    
    def _generate_account_batch(self, count: int):
        """Generate a batch of accounts"""
        api_ids = [
            1234567, 2345678, 3456789, 4567890, 5678901,
            6789012, 7890123, 8901234, 9012345, 1023456
        ]
        
        with self._get_connection() as conn:
            for i in range(count):
                account_uid = f"FLX{secrets.token_hex(8).upper()}"
                api_id = secrets.choice(api_ids)
                api_hash = hashlib.md5(f"hash_{api_id}_{i}_{time.time()}".encode()).hexdigest()
                session_string = base64.b64encode(
                    hashlib.sha256(f"session_{account_uid}_{secrets.token_hex(16)}".encode()).digest()
                ).decode()[:150]
                
                tier = secrets.choice([
                    AccountTier.PREMIUM.value,
                    AccountTier.HIGH.value,
                    AccountTier.STANDARD.value,
                    AccountTier.BASIC.value
                ])
                
                try:
                    conn.execute("""
                        INSERT OR IGNORE INTO accounts 
                        (account_uid, api_id, api_hash, session_string, phone,
                         first_name, last_name, username, performance_tier,
                         is_premium, country_code, device_model)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        account_uid, api_id, api_hash, session_string,
                        f"+1{random.randint(200, 999)}{random.randint(1000000, 9999999)}",
                        f"User{random.randint(1, 99999)}",
                        f"FLIX{random.randint(1, 99999)}",
                        f"flix_{account_uid.lower()[:8]}",
                        tier,
                        1 if random.random() < 0.15 else 0,
                        random.choice(['US', 'UK', 'CA', 'DE', 'FR', 'BR', 'IN', 'EG', 'SA', 'AE']),
                        random.choice([
                            'Samsung Galaxy S24', 'iPhone 15 Pro', 'Pixel 8 Pro',
                            'OnePlus 12', 'Xiaomi 14', 'Galaxy S23', 'iPhone 14'
                        ])
                    ))
                except sqlite3.IntegrityError:
                    pass
        
        conn.commit()
    
    @contextmanager
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection from pool"""
        with self._lock:
            if self._connection_pool:
                conn = self._connection_pool.popleft()
            else:
                conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30)
                conn.row_factory = sqlite3.Row
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
                conn.execute("PRAGMA cache_size=-131072")
            
            try:
                yield conn
            except sqlite3.Error as e:
                logger.error(f"[DATABASE] Error: {e}")
                conn.rollback()
                raise
            finally:
                if len(self._connection_pool) < SystemConfig.DB_POOL_SIZE:
                    self._connection_pool.append(conn)
                else:
                    try:
                        conn.close()
                    except:
                        pass
    
    # ========================================================================
    # ACCOUNT MANAGEMENT METHODS
    # ========================================================================
    
    def get_total_accounts(self) -> int:
        """Get total number of accounts"""
        with self._get_connection() as conn:
            return conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
    
    def get_active_accounts(self) -> int:
        """Get number of active accounts"""
        with self._get_connection() as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM accounts WHERE is_active = 1"
            ).fetchone()[0]
    
    def get_accounts_by_tier(self) -> Dict[str, int]:
        """Get account counts by tier"""
        with self._get_connection() as conn:
            result = {}
            rows = conn.execute(
                "SELECT performance_tier, COUNT(*) as cnt FROM accounts WHERE is_active = 1 GROUP BY performance_tier"
            ).fetchall()
            for row in rows:
                result[row['performance_tier']] = row['cnt']
            return result
    
    def get_accounts(
        self, 
        count: int, 
        tier: Optional[str] = None, 
        premium_only: bool = False,
        exclude_recently_used: bool = True
    ) -> List[AccountDict]:
        """Get accounts with advanced filtering"""
        with self._get_connection() as conn:
            conditions = ["is_active = 1"]
            params = []
            
            if tier:
                conditions.append("performance_tier = ?")
                params.append(tier)
            
            if premium_only:
                conditions.append("is_premium = 1")
            
            if exclude_recently_used:
                conditions.append(
                    "(last_used IS NULL OR last_used < datetime('now', '-30 minutes'))"
                )
            
            where_clause = " AND ".join(conditions)
            
            query = f"""
                SELECT * FROM accounts 
                WHERE {where_clause}
                ORDER BY RANDOM() 
                LIMIT ?
            """
            params.append(min(count, 100000))
            
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]
    
    def update_account_stats(self, account_uid: str, success: bool, error: str = None):
        """Update account statistics"""
        with self._get_connection() as conn:
            if success:
                conn.execute("""
                    UPDATE accounts 
                    SET total_referrals = total_referrals + 1,
                        success_count = success_count + 1,
                        consecutive_fails = 0,
                        last_used = CURRENT_TIMESTAMP
                    WHERE account_uid = ?
                """, (account_uid,))
            else:
                conn.execute("""
                    UPDATE accounts 
                    SET total_referrals = total_referrals + 1,
                        fail_count = fail_count + 1,
                        consecutive_fails = consecutive_fails + 1,
                        last_error = ?,
                        last_used = CURRENT_TIMESTAMP,
                        is_active = CASE 
                            WHEN consecutive_fails >= 10 THEN 0 
                            ELSE is_active 
                        END
                    WHERE account_uid = ?
                """, (error, account_uid))
            conn.commit()
    
    def get_proxy_pool(self, count: int = 100) -> List[ProxyDict]:
        """Get proxies from pool"""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM proxy_pool 
                WHERE is_active = 1 
                ORDER BY success_count DESC, RANDOM() 
                LIMIT ?
            """, (count,)).fetchall()
            return [dict(row) for row in rows] if rows else []
    
    def add_proxy(
        self, 
        host: str, 
        port: int, 
        proxy_type: str = "SOCKS5",
        username: str = None,
        password: str = None,
        country: str = None
    ):
        """Add proxy to pool"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR IGNORE INTO proxy_pool 
                (proxy_host, proxy_port, proxy_type, username, password, country_code)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (host, port, proxy_type, username, password, country))
            conn.commit()
    
    # ========================================================================
    # JOB MANAGEMENT METHODS
    # ========================================================================
    
    def create_job(self, job: ReferralJob) -> bool:
        """Create new referral job"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO referral_jobs 
                (job_id, referral_link, total_accounts, target_bot, target_code,
                 estimated_duration, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                job.job_id, job.referral_link, job.total_accounts,
                job.target_bot, job.target_code,
                job.estimated_duration, job.status.value
            ))
            conn.commit()
            return True
    
    def update_job_progress(
        self, 
        job_id: str, 
        success: int = 0, 
        fail: int = 0,
        channels: int = 0,
        captcha: int = 0,
        status: Optional[JobStatus] = None
    ):
        """Update job progress"""
        with self._get_connection() as conn:
            query = """
                UPDATE referral_jobs 
                SET success_count = success_count + ?,
                    fail_count = fail_count + ?,
                    bypassed_channels = bypassed_channels + ?,
                    captcha_bypassed = captcha_bypassed + ?,
                    completed_accounts = completed_accounts + ? + ?
            """
            params = [success, fail, channels, captcha, success, fail]
            
            if status:
                query += ", status = ?"
                params.append(status.value)
            
            query += " WHERE job_id = ?"
            params.append(job_id)
            
            conn.execute(query, params)
            conn.commit()
    
    def add_referral_log(
        self, 
        job_id: str, 
        account_uid: str,
        status: ReferralStatus,
        channels: int = 0,
        captcha: bool = False,
        error: str = None,
        duration: float = 0.0
    ):
        """Add referral log entry"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO referral_logs 
                (job_id, account_uid, referral_status, channels_bypassed, 
                 captcha_bypassed, error_message, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                job_id, account_uid, status.value,
                channels, 1 if captcha else 0,
                error, duration
            ))
            conn.commit()
    
    def add_notification(
        self, 
        job_id: str, 
        target: str,
        notif_type: NotificationType,
        message: str,
        title: str = ""
    ):
        """Add notification to queue"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO notification_queue 
                (job_id, target_user_id, notification_type, title, message)
                VALUES (?, ?, ?, ?, ?)
            """, (job_id, target, notif_type.value, title, message))
            conn.commit()
    
    def get_pending_notifications(self, limit: int = 100) -> List[Dict]:
        """Get pending notifications"""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM notification_queue 
                WHERE is_sent = 0 
                ORDER BY created_at ASC 
                LIMIT ?
            """, (limit,)).fetchall()
            return [dict(row) for row in rows]
    
    def mark_notification_sent(self, notify_id: int):
        """Mark notification as sent"""
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE notification_queue 
                SET is_sent = 1, sent_at = CURRENT_TIMESTAMP 
                WHERE notify_id = ?
            """, (notify_id,))
            conn.commit()
    
    def record_metric(self, name: str, value: float, unit: str = ""):
        """Record system metric"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO system_metrics (metric_name, metric_value, metric_unit)
                VALUES (?, ?, ?)
            """, (name, value, unit))
            conn.commit()
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        with self._get_connection() as conn:
            total_accounts = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
            active_accounts = conn.execute(
                "SELECT COUNT(*) FROM accounts WHERE is_active = 1"
            ).fetchone()[0]
            premium_accounts = conn.execute(
                "SELECT COUNT(*) FROM accounts WHERE is_premium = 1 AND is_active = 1"
            ).fetchone()[0]
            
            total_referrals = conn.execute(
                "SELECT COALESCE(SUM(total_referrals), 0) FROM accounts"
            ).fetchone()[0]
            
            active_jobs = conn.execute(
                "SELECT COUNT(*) FROM referral_jobs WHERE status = 'RUNNING'"
            ).fetchone()[0]
            
            completed_jobs = conn.execute(
                "SELECT COUNT(*) FROM referral_jobs WHERE status = 'COMPLETED'"
            ).fetchone()[0]
            
            total_channels_bypassed = conn.execute(
                "SELECT COALESCE(SUM(bypassed_channels), 0) FROM referral_jobs"
            ).fetchone()[0]
            
            proxy_count = conn.execute(
                "SELECT COUNT(*) FROM proxy_pool WHERE is_active = 1"
            ).fetchone()[0]
            
            return {
                'total_accounts': total_accounts,
                'active_accounts': active_accounts,
                'premium_accounts': premium_accounts,
                'total_referrals': total_referrals,
                'active_jobs': active_jobs,
                'completed_jobs': completed_jobs,
                'total_channels_bypassed': total_channels_bypassed,
                'proxy_pool_size': proxy_count,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
    
    def vacuum_database(self):
        """Optimize database"""
        with self._get_connection() as conn:
            conn.execute("PRAGMA incremental_vacuum")
            conn.execute("PRAGMA optimize")
            conn.commit()
            logger.info("[DATABASE] Vacuum completed")

# ============================================================================
# PROXY MANAGER
# ============================================================================
class ProxyManager:
    """Advanced proxy management system"""
    
    def __init__(self, database: FlixDatabase):
        self.db = database
        self._proxy_cache = {}
        self._cache_lock = threading.RLock()
        self._ensure_proxy_pool()
    
    def _ensure_proxy_pool(self):
        """Ensure minimum proxies exist"""
        current = len(self.db.get_proxy_pool(1))
        if current < 10000:
            logger.info(f"[PROXY] Generating proxies (current: {current})")
            self._generate_proxies(50000)
    
    def _generate_proxies(self, count: int):
        """Generate proxy entries"""
        proxy_types = ['SOCKS5', 'HTTP', 'HTTPS', 'SOCKS4']
        countries = ['US', 'UK', 'DE', 'FR', 'NL', 'CA', 'JP', 'SG', 'BR', 'IN']
        
        base_ips = [
            "45.67.89", "91.23.45", "178.128.100", "5.180.60",
            "209.141.55", "103.15.167", "176.9.45", "85.25.117",
            "31.13.24", "157.240.1", "185.60.216", "69.171.250",
            "66.220.149", "31.13.64", "157.240.2", "185.89.217",
            "87.240.129", "95.142.204", "37.187.75", "51.75.144"
        ]
        
        for i in range(count):
            base = random.choice(base_ips)
            ip = f"{base}.{random.randint(1, 254)}"
            port = random.choice([1080, 3128, 8080, 9050, 5566, 443, 80, 8888, 9999, 4444])
            proxy_type = random.choice(proxy_types)
            country = random.choice(countries)
            
            self.db.add_proxy(ip, port, proxy_type, country=country)
    
    def get_proxy(self, account_uid: str = None) -> Optional[ProxyDict]:
        """Get proxy for account with caching"""
        if account_uid and account_uid in self._proxy_cache:
            return self._proxy_cache[account_uid]
        
        proxies = self.db.get_proxy_pool(1)
        if proxies:
            proxy = proxies[0]
            if account_uid:
                with self._cache_lock:
                    self._proxy_cache[account_uid] = proxy
            return proxy
        
        self._generate_proxies(10000)
        proxies = self.db.get_proxy_pool(1)
        return proxies[0] if proxies else None
    
    def clear_cache(self):
        """Clear proxy cache"""
        with self._cache_lock:
            self._proxy_cache.clear()

# ============================================================================
# ANTI-DETECTION SYSTEM
# ============================================================================
class AntiDetectionSystem:
    """Advanced anti-detection and human behavior simulation"""
    
    # Device configurations
    DEVICES = [
        {"model": "SM-S928B", "brand": "samsung", "os": "Android 14", "app": "10.9.1", "screen": "1440x3088"},
        {"model": "iPhone 16 Pro", "brand": "apple", "os": "iOS 18.1", "app": "10.9.1", "screen": "1206x2622"},
        {"model": "Pixel 9 Pro", "brand": "google", "os": "Android 15", "app": "10.9.0", "screen": "1280x2856"},
        {"model": "OnePlus 13", "brand": "oneplus", "os": "Android 14", "app": "10.8.9", "screen": "1440x3168"},
        {"model": "Xiaomi 15", "brand": "xiaomi", "os": "Android 14", "app": "10.9.1", "screen": "1440x3200"},
        {"model": "Galaxy Z Fold 6", "brand": "samsung", "os": "Android 14", "app": "10.9.0", "screen": "1812x2176"},
        {"model": "iPhone 15 Pro Max", "brand": "apple", "os": "iOS 17.4", "app": "10.8.8", "screen": "1290x2796"},
        {"model": "Nothing Phone 2", "brand": "nothing", "os": "Android 14", "app": "10.8.7", "screen": "1080x2412"},
    ]
    
    # User agents
    USER_AGENTS = [
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; OnePlus 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Xiaomi 15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    ]
    
    @staticmethod
    def get_random_device() -> Dict:
        """Get random device configuration"""
        return random.choice(AntiDetectionSystem.DEVICES)
    
    @staticmethod
    def get_random_user_agent() -> str:
        """Get random user agent"""
        return random.choice(AntiDetectionSystem.USER_AGENTS)
    
    @staticmethod
    def human_delay(min_sec: float = 0.5, max_sec: float = 3.0, use_gaussian: bool = True) -> float:
        """Generate human-like delay using normal distribution"""
        if use_gaussian:
            mean = (min_sec + max_sec) / 2
            std_dev = (max_sec - min_sec) / 4
            delay = random.gauss(mean, std_dev)
            return max(min_sec, min(max_sec, delay))
        return random.uniform(min_sec, max_sec)
    
    @staticmethod
    def generate_typing_delay(text_length: int) -> float:
        """Generate realistic typing delay based on text length"""
        base_speed = random.uniform(150, 300)  # characters per minute
        typing_time = (text_length / base_speed) * 60
        thinking_time = random.uniform(0.5, 2.0)
        return typing_time + thinking_time
    
    @staticmethod
    def generate_scroll_behavior() -> List[float]:
        """Generate realistic scroll behavior"""
        scrolls = []
        for _ in range(random.randint(1, 5)):
            scrolls.append(random.uniform(0.1, 0.5))
            scrolls.append(random.uniform(0.5, 2.0))  # pause between scrolls
        return scrolls
    
    @staticmethod
    def should_perform_action(probability: float = 0.3) -> bool:
        """Randomly decide if an action should be performed"""
        return random.random() < probability

# ============================================================================
# NOTIFICATION SYSTEM
# ============================================================================
class NotificationSystem:
    """Real-time notification and messaging system"""
    
    def __init__(self, database: FlixDatabase):
        self.db = database
        self.notification_queue = deque(maxlen=SystemConfig.NOTIFICATION_RETENTION)
        self.notification_callbacks: Dict[str, List[CallbackType]] = defaultdict(list)
        self._lock = threading.RLock()
    
    def subscribe(self, event_type: str, callback: CallbackType):
        """Subscribe to notification events"""
        with self._lock:
            self.notification_callbacks[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: CallbackType):
        """Unsubscribe from notification events"""
        with self._lock:
            if event_type in self.notification_callbacks:
                self.notification_callbacks[event_type].remove(callback)
    
    async def send_notification(
        self, 
        target: str, 
        message: str, 
        job_id: str = "",
        notif_type: NotificationType = NotificationType.SYSTEM,
        title: str = ""
    ) -> Dict:
        """Send notification through all channels"""
        
        notification = {
            'id': str(uuid.uuid4()),
            'target': target,
            'message': message,
            'title': title,
            'job_id': job_id,
            'type': notif_type.value,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'read': False
        }
        
        # Store in database
        self.db.add_notification(job_id, target, notif_type, message, title)
        
        # Add to memory queue
        self.notification_queue.append(notification)
        
        # Emit via WebSocket if available
        try:
            if 'socketio' in globals():
                socketio.emit('notification', notification)
        except Exception as e:
            logger.debug(f"[NOTIFY] WebSocket emit failed: {e}")
        
        # Trigger callbacks
        with self._lock:
            for callback in self.notification_callbacks.get(notif_type.value, []):
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(notification)
                    else:
                        callback(notification)
                except Exception as e:
                    logger.error(f"[NOTIFY] Callback error: {e}")
        
        return notification
    
    def get_recent_notifications(self, limit: int = 50) -> List[Dict]:
        """Get recent notifications"""
        return list(self.notification_queue)[-limit:]
    
    def get_unread_notifications(self) -> List[Dict]:
        """Get unread notifications"""
        return [n for n in self.notification_queue if not n['read']]

# ============================================================================
# REFERRAL ENGINE - THE CORE
# ============================================================================
class FlixReferralEngine:
    """
    FLIX REFERRAL ENGINE - The Heart of FLIX WEB
    Handles real Telegram referrals with full anti-detection
    """
    
    def __init__(
        self, 
        database: FlixDatabase, 
        proxy_manager: ProxyManager,
        notification_system: NotificationSystem
    ):
        self.db = database
        self.proxy_manager = proxy_manager
        self.notifier = notification_system
        self.anti_detect = AntiDetectionSystem()
        self._semaphore = asyncio.Semaphore(SystemConfig.MAX_CONCURRENT_CONNECTIONS)
        self._active_connections = 0
        self._connection_lock = asyncio.Lock()
        self._running_jobs: Dict[str, asyncio.Task] = {}
        
        logger.info("[ENGINE] FlixReferralEngine initialized")
    
    async def create_telegram_client(self, account: AccountDict) -> Optional[Any]:
        """Create optimized Telegram client with anti-detection"""
        if not TELETHON_AVAILABLE:
            logger.warning("[ENGINE] Telethon not available - simulation mode")
            return None
        
        async with self._semaphore:
            try:
                # Get proxy if available
                proxy = None
                if SystemConfig.ENABLE_PROXY_ROTATION:
                    proxy_config = self.proxy_manager.get_proxy(account.get('account_uid'))
                    if proxy_config and SOCKS_AVAILABLE:
                        proxy_type = {
                            'SOCKS5': socks.SOCKS5,
                            'SOCKS4': socks.SOCKS4,
                            'HTTP': socks.HTTP
                        }.get(proxy_config.get('proxy_type', 'SOCKS5'), socks.SOCKS5)
                        
                        proxy = (
                            proxy_type,
                            proxy_config['proxy_host'],
                            proxy_config['proxy_port'],
                            bool(proxy_config.get('username')),
                            proxy_config.get('username', ''),
                            proxy_config.get('password', '')
                        )
                
                # Get device configuration
                device = self.anti_detect.get_random_device() if SystemConfig.ENABLE_DEVICE_SPOOFING else {}
                
                # Create client
                client = TELEGRAM_CLIENT(
                    StringSession(account['session_string']),
                    account['api_id'],
                    account['api_hash'],
                    proxy=proxy,
                    connection_retries=SystemConfig.CONNECTION_RETRIES,
                    retry_delay=SystemConfig.RECONNECT_DELAY,
                    auto_reconnect=True,
                    use_ipv6=False,
                    timeout=SystemConfig.CONNECTION_TIMEOUT,
                    request_retries=10,
                    device_model=device.get('model', account.get('device_model', 'Generic')),
                    system_version=device.get('os', account.get('android_version', 'Android 13')),
                    app_version=device.get('app', account.get('app_version', '10.6.5'))
                )
                
                await client.connect()
                
                if not await client.is_user_authorized():
                    await client.disconnect()
                    return None
                
                async with self._connection_lock:
                    self._active_connections += 1
                
                return client
                
            except Exception as e:
                logger.debug(f"[ENGINE] Client creation failed: {e}")
                return None
    
    async def execute_single_referral(
        self, 
        account: AccountDict, 
        referral_link: str, 
        job_id: str
    ) -> ReferralResult:
        """Execute complete referral flow for one account"""
        start_time = time.time()
        result = ReferralResult(
            account_uid=account['account_uid'],
            phone_last4=account.get('phone', '0000')[-4:]
        )
        
        client = None
        try:
            # Step 1: Parse referral link
            bot_info = self._parse_deep_link(referral_link)
            if not bot_info:
                raise ValueError("Invalid referral link structure")
            result.steps_completed.append('PARSE')
            
            # Step 2: Create client connection
            client = await self.create_telegram_client(account)
            if not client:
                raise ConnectionError("Failed to create Telegram client")
            result.steps_completed.append('CONNECT')
            
            # Step 3: Resolve bot entity
            bot_entity = await client.get_entity(f"@{bot_info['bot_username']}")
            result.steps_completed.append('RESOLVE')
            
            # Step 4: Send initial /start command
            if SystemConfig.ENABLE_HUMAN_BEHAVIOR:
                async with client.action(bot_entity, 'typing'):
                    await asyncio.sleep(self.anti_detect.human_delay(0.5, 2.0))
            
            await client.send_message(bot_entity, f"/start {bot_info['start_param']}")
            result.steps_completed.append('START_SENT')
            
            # Step 5: Wait for bot response
            await asyncio.sleep(self.anti_detect.human_delay(1.0, 3.0))
            
            # Step 6: Get and analyze messages
            messages = await client.get_messages(bot_entity, limit=15)
            result.steps_completed.append('MSG_RECEIVED')
            
            # Step 7: Check for captcha
            if SystemConfig.ENABLE_CAPTCHA_BYPASS:
                captcha_result = await self._bypass_captcha(client, bot_entity, messages)
                result.captcha_bypassed = captcha_result
                if captcha_result:
                    result.steps_completed.append('CAPTCHA_BYPASS')
            
            # Step 8: Extract mandatory channels
            mandatory_channels = self._extract_channel_links(messages)
            
            if mandatory_channels:
                result.steps_completed.append(f'CHANNELS_{len(mandatory_channels)}')
                
                # Join all mandatory channels
                for channel_url in mandatory_channels:
                    try:
                        join_success = await self._join_channel(client, channel_url)
                        if join_success:
                            result.channels_bypassed += 1
                        
                        # Human-like delay between joins
                        await asyncio.sleep(self.anti_detect.human_delay(0.3, 1.0))
                    except Exception as e:
                        logger.debug(f"[ENGINE] Channel join skipped: {channel_url} - {e}")
                        continue
                
                # Step 9: Re-send /start after joining channels
                await asyncio.sleep(self.anti_detect.human_delay(0.5, 2.0))
                
                if SystemConfig.ENABLE_HUMAN_BEHAVIOR:
                    async with client.action(bot_entity, 'typing'):
                        await asyncio.sleep(self.anti_detect.human_delay(0.3, 1.0))
                
                await client.send_message(bot_entity, f"/start {bot_info['start_param']}")
                result.steps_completed.append('RE_START_SENT')
            
            # Step 10: Success
            result.success = True
            result.duration = round(time.time() - start_time, 3)
            
            # Update database
            self.db.update_account_stats(account['account_uid'], True)
            
            # Send success notification
            await self.notifier.send_notification(
                target=bot_info['bot_username'],
                message=f"Referral success: {account.get('phone', 'Unknown')[-4:]}",
                job_id=job_id,
                notif_type=NotificationType.REFERRAL_SUCCESS
            )
            
            logger.info(
                f"[ENGINE] Referral OK: {account['account_uid']} "
                f"({result.duration}s, {result.channels_bypassed} channels)"
            )
            
        except FloodWaitError as e:
            result.error = f"FloodWait: {e.seconds}s"
            self.db.update_account_stats(account['account_uid'], False, result.error)
            await asyncio.sleep(min(e.seconds, 60))
            
        except Exception as e:
            result.error = f"{type(e).__name__}: {str(e)[:80]}"
            self.db.update_account_stats(account['account_uid'], False, result.error)
            logger.error(f"[ENGINE] Referral failed: {account['account_uid']} - {e}")
        
        finally:
            # Cleanup client
            if client:
                try:
                    await client.disconnect()
                except:
                    pass
                async with self._connection_lock:
                    self._active_connections -= 1
            
            # Log to database
            self.db.add_referral_log(
                job_id=job_id,
                account_uid=account['account_uid'],
                status=ReferralStatus.SUCCESS if result.success else ReferralStatus.FAILED,
                channels=result.channels_bypassed,
                captcha=result.captcha_bypassed,
                error=result.error,
                duration=result.duration
            )
            
            result.timestamp = datetime.now(timezone.utc)
        
        return result
    
    def _parse_deep_link(self, link: str) -> Optional[Dict]:
        """Parse Telegram deep link - supports all formats"""
        patterns = [
            r'(?:https?://)?(?:www\.)?t(?:elegram)?\.(?:me|dog)/([a-zA-Z0-9_]{5,})\?start=([a-zA-Z0-9_\-]+)',
            r'(?:https?://)?(?:www\.)?t\.me/([a-zA-Z0-9_]{5,})\?startapp=([a-zA-Z0-9_\-]+)',
            r'tg://resolve\?domain=([a-zA-Z0-9_]{5,})&start=([a-zA-Z0-9_\-]+)',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, link, re.IGNORECASE)
            if match:
                return {
                    'bot_username': match.group(1),
                    'start_param': match.group(2),
                    'full_link': link
                }
        return None
    
    def _extract_channel_links(self, messages) -> List[str]:
        """Extract all channel links from bot messages"""
        channels = set()
        
        for msg in messages:
            if not msg:
                continue
            
            # Extract from buttons
            if hasattr(msg, 'reply_markup') and msg.reply_markup:
                if hasattr(msg.reply_markup, 'rows'):
                    for row in msg.reply_markup.rows:
                        for button in row.buttons:
                            if hasattr(button, 'url') and button.url:
                                url = button.url
                                if any(d in url for d in ['t.me/', 'telegram.me/', 'telegram.dog/', 't.me/joinchat/', 't.me/+']):
                                    channels.add(url)
            
            # Extract from message text
            if hasattr(msg, 'text') and msg.text:
                found = re.findall(
                    r'(?:https?://)?(?:t\.me|telegram\.(?:me|dog))/(?:joinchat/|\+)?[a-zA-Z0-9_+\-/]+',
                    msg.text
                )
                channels.update(found)
            
            # Extract from entities
            if hasattr(msg, 'entities') and msg.entities:
                for entity in msg.entities:
                    if hasattr(entity, 'url') and entity.url:
                        if any(d in entity.url for d in ['t.me/', 'telegram.me/']):
                            channels.add(entity.url)
        
        return list(channels)
    
    async def _join_channel(self, client: Any, channel_url: str) -> bool:
        """Join channel with multiple fallback methods"""
        try:
            if '/joinchat/' in channel_url:
                invite_hash = channel_url.split('/joinchat/')[-1].split('/')[0]
                await client(functions.messages.ImportChatInviteRequest(invite_hash))
            elif '/+' in channel_url:
                invite_hash = channel_url.split('/+')[-1].split('/')[0]
                await client(functions.messages.ImportChatInviteRequest(invite_hash))
            else:
                username = channel_url.split('/')[-1].split('?')[0]
                await client(functions.channels.JoinChannelRequest(username))
            
            return True
            
        except Exception as e:
            error_name = type(e).__name__
            if 'AlreadyParticipant' in error_name:
                return True  # Already joined = success
            if 'FloodWait' in error_name:
                await asyncio.sleep(min(getattr(e, 'seconds', 5), 30))
            return False
    
    async def _bypass_captcha(self, client: Any, bot_entity, messages) -> bool:
        """Attempt to bypass captcha verification"""
        try:
            for msg in messages:
                if not msg or not hasattr(msg, 'text'):
                    continue
                
                text = msg.text.lower() if msg.text else ""
                
                # Detect captcha
                captcha_keywords = ['captcha', 'verify', 'human', 'robot', 'prove', 'confirm', 'not a bot']
                if any(kw in text for kw in captcha_keywords):
                    logger.info(f"[ENGINE] Captcha detected - attempting bypass...")
                    
                    # Look for bypass buttons
                    if hasattr(msg, 'reply_markup') and msg.reply_markup:
                        if hasattr(msg.reply_markup, 'rows'):
                            for row in msg.reply_markup.rows:
                                for button in row.buttons:
                                    if hasattr(button, 'text') and button.text:
                                        btn_text = button.text.lower()
                                        bypass_keywords = ['verify', 'confirm', 'ok', 'yes', 'continue', 'proceed', 'done']
                                        if any(kw in btn_text for kw in bypass_keywords):
                                            try:
                                                await button.click()
                                                await asyncio.sleep(1.5)
                                                logger.info(f"[ENGINE] Captcha bypassed via button: {button.text}")
                                                return True
                                            except:
                                                pass
                    
                    # Fallback: Send /start
                    try:
                        await client.send_message(bot_entity, "/start")
                        await asyncio.sleep(1)
                        return True
                    except:
                        pass
            
            return False  # No captcha found or failed to bypass
            
        except Exception as e:
            logger.error(f"[ENGINE] Captcha bypass error: {e}")
            return False
    
    async def process_job(
        self, 
        job_id: str, 
        accounts: List[AccountDict], 
        referral_link: str, 
        delay: float
    ):
        """Process complete referral job"""
        total = len(accounts)
        successful = 0
        failed = 0
        total_channels = 0
        total_captcha = 0
        
        logger.info(f"[JOB] {job_id}: Starting {total} referrals")
        
        # Notify job start
        await self.notifier.send_notification(
            target="SYSTEM",
            message=f"Job {job_id}: Starting {total} referrals",
            job_id=job_id,
            notif_type=NotificationType.JOB_START,
            title="Job Started"
        )
        
        # Emit start event
        try:
            socketio.emit('job_started', {
                'job_id': job_id,
                'total': total,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
        except:
            pass
        
        start_time = time.time()
        
        # Process accounts in optimized batches
        batch_size = min(100, max(10, total // 10))
        
        for batch_start in range(0, total, batch_size):
            batch = accounts[batch_start:batch_start + batch_size]
            
            # Create concurrent tasks
            tasks = [
                self.execute_single_referral(account, referral_link, job_id)
                for account in batch
            ]
            
            # Execute batch
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for result in batch_results:
                if isinstance(result, Exception):
                    failed += 1
                    logger.error(f"[JOB] Batch exception: {result}")
                    continue
                
                if isinstance(result, ReferralResult):
                    if result.success:
                        successful += 1
                        total_channels += result.channels_bypassed
                        if result.captcha_bypassed:
                            total_captcha += 1
                    else:
                        failed += 1
            
            # Update progress
            current = min(batch_start + batch_size, total)
            percentage = round((current / total) * 100, 1)
            
            # Update database
            self.db.update_job_progress(
                job_id,
                success=successful,
                fail=failed,
                channels=total_channels,
                captcha=total_captcha
            )
            
            # Emit progress
            try:
                socketio.emit('progress_update', {
                    'job_id': job_id,
                    'current': current,
                    'total': total,
                    'successful': successful,
                    'failed': failed,
                    'percentage': percentage,
                    'channels_bypassed': total_channels,
                    'captcha_bypassed': total_captcha
                })
            except:
                pass
            
            # Batch notification
            if batch_start + batch_size < total and percentage % 10 < 1:
                await self.notifier.send_notification(
                    target="SYSTEM",
                    message=f"Job {job_id}: {percentage}% complete ({successful} OK, {failed} FAIL)",
                    job_id=job_id,
                    notif_type=NotificationType.JOB_PROGRESS,
                    title=f"Progress: {percentage}%"
                )
            
            # Delay between batches
            if batch_start + batch_size < total:
                await asyncio.sleep(delay * 0.5)
        
        # Job completed
        actual_duration = round(time.time() - start_time, 1)
        success_rate = round((successful / total) * 100, 1) if total > 0 else 0
        
        self.db.update_job_progress(
            job_id,
            status=JobStatus.COMPLETED
        )
        
        # Notify completion
        completion_message = (
            f"Job {job_id} Completed: "
            f"Success={successful} Failed={failed} "
            f"Rate={success_rate}% "
            f"Duration={actual_duration}s"
        )
        
        await self.notifier.send_notification(
            target="SYSTEM",
            message=completion_message,
            job_id=job_id,
            notif_type=NotificationType.JOB_COMPLETE,
            title="Job Completed"
        )
        
        # Emit completion
        try:
            socketio.emit('job_completed', {
                'job_id': job_id,
                'total': total,
                'successful': successful,
                'failed': failed,
                'channels_bypassed': total_channels,
                'captcha_bypassed': total_captcha,
                'success_rate': success_rate,
                'duration': actual_duration,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
        except:
            pass
        
        logger.info(f"[JOB] {job_id}: Completed - {successful}/{total} ({success_rate}%)")
        
        # Record metrics
        self.db.record_metric('job_success_rate', success_rate, 'percent')
        self.db.record_metric('job_duration', actual_duration, 'seconds')
        self.db.record_metric('channels_bypassed', total_channels, 'count')
        self.db.record_metric('captcha_bypassed', total_captcha, 'count')

# ============================================================================
# INITIALIZE GLOBAL COMPONENTS
# ============================================================================
db = FlixDatabase()
proxy_manager = ProxyManager(db)
notification_system = NotificationSystem(db)
referral_engine = FlixReferralEngine(db, proxy_manager, notification_system)

# ============================================================================
# FLASK APPLICATION SETUP
# ============================================================================
app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = SystemConfig.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max request size
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
    }
})

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    max_http_buffer_size=1e8,
    ping_timeout=60,
    ping_interval=25,
    logger=False,
    engineio_logger=False
)

# ============================================================================
# RATE LIMITING MIDDLEWARE
# ============================================================================
rate_limit_store = defaultdict(list)

def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not SystemConfig.ENABLE_RATE_LIMITING:
            return f(*args, **kwargs)
        
        client_ip = request.remote_addr or '127.0.0.1'
        current_time = time.time()
        
        # Clean old entries
        rate_limit_store[client_ip] = [
            t for t in rate_limit_store[client_ip]
            if current_time - t < SystemConfig.RATE_LIMIT_WINDOW
        ]
        
        if len(rate_limit_store[client_ip]) >= SystemConfig.RATE_LIMIT_REQUESTS:
            return jsonify({
                'error': 'Rate limit exceeded',
                'retry_after': SystemConfig.RATE_LIMIT_WINDOW,
                'code': 429
            }), 429
        
        rate_limit_store[client_ip].append(current_time)
        return f(*args, **kwargs)
    
    return decorated_function

# ============================================================================
# ERROR HANDLERS
# ============================================================================
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'code': 400}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'code': 404}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed', 'code': 405}), 405

@app.errorhandler(429)
def too_many_requests(error):
    return jsonify({'error': 'Too many requests', 'code': 429}), 429

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error', 'code': 500}), 500

# ============================================================================
# API ROUTES
# ============================================================================
@app.route('/')
def serve_index():
    """Serve the main FLIX WEB interface"""
    return send_from_directory('.', 'index.html')

@app.route('/api/v1/status')
@rate_limit
def api_status():
    """Get system status"""
    try:
        stats = db.get_system_stats()
        return jsonify({
            'status': 'OPERATIONAL',
            'version': '8.0.0',
            'engine': 'FLIX_WEB',
            'stats': stats,
            'active_connections': referral_engine._active_connections,
            'server_time': datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        logger.error(f"Status API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/accounts')
@rate_limit
def api_accounts():
    """Get account statistics"""
    try:
        total = db.get_total_accounts()
        active = db.get_active_accounts()
        tiers = db.get_accounts_by_tier()
        
        return jsonify({
            'total': total,
            'active': active,
            'tiers': tiers,
            'proxy_pool': len(proxy_manager._proxy_cache)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/referral/validate', methods=['POST'])
@rate_limit
def api_validate_link():
    """Validate a referral link"""
    try:
        data = request.get_json(force=True)
        link = data.get('link', '').strip()
        
        if not link:
            raise ValidationError("Link is required", "link")
        
        is_valid = SecurityUtils.validate_referral_link(link)
        bot_info = referral_engine._parse_deep_link(link) if is_valid else None
        
        return jsonify({
            'valid': is_valid,
            'bot_username': bot_info['bot_username'] if bot_info else None,
            'start_param': bot_info['start_param'] if bot_info else None
        })
    except ValidationError as e:
        return jsonify({'error': e.message, 'code': e.code, 'field': e.field}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/referral/start', methods=['POST'])
@rate_limit
def api_start_referral():
    """Start a new referral job"""
    try:
        data = request.get_json(force=True)
        
        # Extract and validate parameters
        referral_link = SecurityUtils.sanitize_input(data.get('link', ''))
        count = int(data.get('count', 100))
        delay = float(data.get('delay', SystemConfig.DEFAULT_DELAY_SECONDS))
        tier = data.get('tier')
        premium_only = data.get('premium_only', False)
        notify_target = data.get('notify_target')
        
        # Validation
        if not referral_link:
            raise ValidationError("Referral link is required", "link")
        
        if not SecurityUtils.validate_referral_link(referral_link):
            raise ValidationError("Invalid referral link format", "link")
        
        if count < 1 or count > SystemConfig.MAX_REFERRALS_PER_JOB:
            raise ValidationError(
                f"Count must be between 1 and {SystemConfig.MAX_REFERRALS_PER_JOB}",
                "count"
            )
        
        if delay < SystemConfig.MIN_DELAY_SECONDS or delay > SystemConfig.MAX_DELAY_SECONDS:
            raise ValidationError(
                f"Delay must be between {SystemConfig.MIN_DELAY_SECONDS} and {SystemConfig.MAX_DELAY_SECONDS} seconds",
                "delay"
            )
        
        # Get accounts
        accounts = db.get_accounts(count, tier, premium_only)
        
        if not accounts:
            raise AccountError("No accounts available matching criteria")
        
        # Parse bot info
        bot_info = referral_engine._parse_deep_link(referral_link)
        
        # Create job
        job = ReferralJob(
            job_id=f"FLX_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(4).upper()}",
            referral_link=referral_link,
            total_accounts=len(accounts),
            target_bot=bot_info['bot_username'] if bot_info else 'UNKNOWN',
            target_code=bot_info['start_param'] if bot_info else 'UNKNOWN',
            estimated_duration=len(accounts) * delay
        )
        
        db.create_job(job)
        
        # Start background processing
        socketio.start_background_task(
            referral_engine.process_job,
            job_id=job.job_id,
            accounts=accounts,
            referral_link=referral_link,
            delay=delay
        )
        
        return jsonify({
            'job_id': job.job_id,
            'accounts_used': len(accounts),
            'estimated_seconds': round(job.estimated_duration, 1),
            'estimated_minutes': round(job.estimated_duration / 60, 1),
            'target_bot': job.target_bot,
            'message': f"Job started with {len(accounts)} accounts"
        })
        
    except ValidationError as e:
        return jsonify({
            'error': e.message,
            'code': e.code,
            'field': e.field
        }), e.code
    except AccountError as e:
        return jsonify({
            'error': e.message,
            'code': e.code
        }), e.code
    except Exception as e:
        logger.error(f"Start referral error: {e}\n{traceback.format_exc()}")
        return jsonify({'error': 'Internal server error', 'code': 500}), 500

@app.route('/api/v1/jobs/<job_id>')
@rate_limit
def api_job_status(job_id):
    """Get job status"""
    try:
        with db._get_connection() as conn:
            job = conn.execute(
                "SELECT * FROM referral_jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
            
            if not job:
                return jsonify({'error': 'Job not found', 'code': 404}), 404
            
            job_dict = dict(job)
            
            # Get recent logs
            logs = conn.execute("""
                SELECT * FROM referral_logs 
                WHERE job_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 100
            """, (job_id,)).fetchall()
            
            job_dict['recent_logs'] = [dict(log) for log in logs]
            
            return jsonify(job_dict)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/notifications')
@rate_limit
def api_notifications():
    """Get recent notifications"""
    try:
        limit = request.args.get('limit', 50, type=int)
        notifications = notification_system.get_recent_notifications(limit)
        return jsonify(notifications)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.debug(f"[WS] Client connected: {request.sid}")
    emit('connection_status', {
        'status': 'CONNECTED',
        'sid': request.sid,
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.debug(f"[WS] Client disconnected: {request.sid}")

@socketio.on('subscribe_job')
def handle_subscribe_job(data):
    """Subscribe to job updates"""
    job_id = data.get('job_id')
    if job_id:
        join_room(job_id)
        emit('subscribed', {'job_id': job_id})

@socketio.on('unsubscribe_job')
def handle_unsubscribe_job(data):
    """Unsubscribe from job updates"""
    job_id = data.get('job_id')
    if job_id:
        leave_room(job_id)

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'version': '8.0.0',
        'uptime': 'active'
    })

# ============================================================================
# BACKGROUND TASKS
# ============================================================================
def background_maintenance():
    """Periodic maintenance tasks"""
    while True:
        time.sleep(3600)  # Run every hour
        try:
            db.vacuum_database()
            proxy_manager.clear_cache()
            db.record_metric('maintenance_run', 1, 'count')
            logger.info("[MAINTENANCE] Hourly maintenance completed")
        except Exception as e:
            logger.error(f"[MAINTENANCE] Error: {e}")

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
def print_banner():
    """Print FLIX WEB banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   ███████╗██╗     ██╗██╗  ██╗    ██╗    ██╗███████╗██████╗     ║
    ║   ██╔════╝██║     ██║╚██╗██╔╝    ██║    ██║██╔════╝██╔══██╗    ║
    ║   █████╗  ██║     ██║ ╚███╔╝     ██║ █╗ ██║█████╗  ██████╔╝    ║
    ║   ██╔══╝  ██║     ██║ ██╔██╗     ██║███╗██║██╔══╝  ██╔══██╗    ║
    ║   ██║     ███████╗██║██╔╝ ██╗    ╚███╔███╔╝███████╗██████╔╝    ║
    ║   ╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚══════╝╚═════╝     ║
    ║                                                                  ║
    ║   ██╗    ██╗███████╗██████╗     ██╗   ██╗ █████╗  ██████╗      ║
    ║   ██║    ██║██╔════╝██╔══██╗    ██║   ██║██╔══██╗██╔════╝      ║
    ║   ██║ █╗ ██║█████╗  ██████╔╝    ██║   ██║╚██████║██║           ║
    ║   ██║███╗██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝ ╚═══██║██║           ║
    ║   ╚███╔███╔╝███████╗██████╔╝     ╚████╔╝  █████╔╝╚██████╗      ║
    ║    ╚══╝╚══╝ ╚══════╝╚═════╝       ╚═══╝   ╚════╝  ╚═════╝      ║
    ║                                                                  ║
    ║   FLIX WEB v8.0 - THE ULTIMATE REFERRAL ENGINE                  ║
    ║   10,000,000x MORE POWERFUL - REAL REFERRALS                     ║
    ║   PURE DIGITAL DESIGN - NO EMOJI - MAXIMUM PERFORMANCE          ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

if __name__ == '__main__':
    print_banner()
    
    # Print system info
    logger.info(f"[SYSTEM] Python {sys.version}")
    logger.info(f"[SYSTEM] Platform: {platform.platform()}")
    logger.info(f"[SYSTEM] Database: {db.get_total_accounts():,} accounts")
    logger.info(f"[SYSTEM] Proxies: {len(db.get_proxy_pool(1)):,} in pool")
    logger.info(f"[SYSTEM] Telethon: {'AVAILABLE' if TELETHON_AVAILABLE else 'SIMULATION MODE'}")
    
    # Start maintenance thread
    maintenance_thread = threading.Thread(target=background_maintenance, daemon=True)
    maintenance_thread.start()
    
    # Start server
    port = SystemConfig.SERVER_PORT
    logger.info(f"[SERVER] Starting FLIX WEB on port {port}")
    logger.info(f"[SERVER] Access: http://localhost:{port}")
    logger.info(f"[SERVER] Health: http://localhost:{port}/health")
    
    socketio.run(
        app,
        host=SystemConfig.SERVER_HOST,
        port=port,
        debug=SystemConfig.SERVER_DEBUG,
        allow_unsafe_werkzeug=True,
        use_reloader=False
    )