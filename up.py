#!/usr/bin/env python3


from __future__ import annotations
import sys
import time
import platform
import uuid
import hashlib
import socket
import asyncio
import collections
import functools
import gc
from collections import defaultdict
import copy
import inspect
import json
import os
import random
import shutil
import statistics
import traceback
import tracemalloc
from collections import deque
from datetime import datetime, UTC
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import aiofiles
import aiohttp
import aiohttp.streams
import ujson as orjson
import hmac
import psutil
import base64
from colorama import Fore, Style, init as colorama_init
from fake_useragent import UserAgent
from multidict import CIMultiDict
from typing import TypedDict, Generic, TypeVar, Any
from collections.abc import Callable, Awaitable
import secrets
import requests as _license_requests

SESSION = globals().get("__SESSION__", {})

SERVER = SESSION.get("server", {})
CLOCK_OFFSET = 0
LOCAL_FAIL_COUNT = 0

aiohttp.streams.DEFAULT_LIMIT = 16 * 1024
aiohttp.streams.DEFAULT_BUFFER = 8 * 1024


class DummyJar(aiohttp.DummyCookieJar):
    def update_cookies(self, *a, **kw) -> None:
        return


aiohttp.DummyCookieJar = DummyJar

LICENSE_CONFIG = {
    "license_sources": [
        {
            "ez4short": "https://ez4short.com/R7bbhm",
            "pastebin_raw": "https://pastebin.com/raw/f5RreEU4",
            "name": "Pool A"
        },
        {
            "ez4short": "https://ez4short.com/phTE",
            "pastebin_raw": "https://pastebin.com/raw/SGZXhEec",
            "name": "Pool B"
        },
        {
            "ez4short": "https://ez4short.com/3YLs5J3P",
            "pastebin_raw": "https://pastebin.com/raw/RhGPFbbG",
            "name": "Pool C"
        },
        {
            "ez4short": "https://ez4short.com/zxuIT",
            "pastebin_raw": "https://pastebin.com/raw/7ZuDrTK6",
            "name": "Pool D"
        },
        {
            "ez4short": "https://ez4short.com/4bGjen",
            "pastebin_raw": "https://pastebin.com/raw/aucpw6sF",
            "name": "Pool E"
        },
        {
            "ez4short": "https://ez4short.com/aEs1i",
            "pastebin_raw": "https://pastebin.com/raw/3E0ZszhA",
            "name": "Pool F"
        }
    ]
}

class _Colors2:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'

class _SecureLicense:
    def __init__(self):
        self.current_source = None
        self.current_password = None
        self.password_hash = None
        self.session_token = secrets.token_hex(32)
        self.is_verified = False
        self.used_sources = []
        
    def hash_password(self, password):
        salt = self.session_token[:16].encode()
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
    
    def get_random_source(self):
        import random as _r
        available = [s for s in LICENSE_CONFIG['license_sources'] 
                    if s['ez4short'] not in self.used_sources]
        
        if not available:
            self.used_sources = []
            available = LICENSE_CONFIG['license_sources'].copy()
        
        chosen = _r.choice(available)
        self.used_sources.append(chosen['ez4short'])
        self.current_source = chosen
        return chosen
    
    def fetch_password_from_pastebin(self, pastebin_url):
        try:
            response = _license_requests.get(pastebin_url, timeout=10)
            if response.status_code != 200:
                return None
            content = response.text.strip()
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    return parts[0].strip()
            return None
        except:
            return None
    
    def verify(self):
        import random as _r
        source = self.get_random_source()
        print(f"\n{_Colors2.CYAN}🔄 Menggunakan sumber: {source.get('name', 'Unknown')}{_Colors2.RESET}")
        
        password = self.fetch_password_from_pastebin(source['pastebin_raw'])
        if not password:
            print(f"{_Colors2.RED}❌ Gagal mengambil password!{_Colors2.RESET}")
            return False
        
        self.current_password = password
        self.password_hash = self.hash_password(password)
        
        max_attempts = 5
        attempt = 0
        
        while attempt < max_attempts:
            print(f"\n{_Colors2.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{_Colors2.RESET}")
            print(f"{_Colors2.MAGENTA}🔐 LICENSE VERIFICATION REQUIRED{_Colors2.RESET}")
            print(f"{_Colors2.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{_Colors2.RESET}")
            print(f"{_Colors2.WHITE}📌 Buka link:{_Colors2.RESET}")
            print(f"{_Colors2.BLUE}   {source['ez4short']}{_Colors2.RESET}")
            print(f"{_Colors2.WHITE}📌 Masukkan password dari Pastebin:{_Colors2.RESET}")
            print(f"{_Colors2.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{_Colors2.RESET}")
            
            remaining = len([s for s in LICENSE_CONFIG['license_sources'] 
                            if s['ez4short'] not in self.used_sources])
            print(f"{_Colors2.YELLOW}💡 Sisa sumber: {remaining} dari {len(LICENSE_CONFIG['license_sources'])}{_Colors2.RESET}")
            print()
            
            user_input = input(f"{_Colors2.GREEN}🔑 Password: {_Colors2.RESET}").strip()
            
            user_hash = self.hash_password(user_input)
            if user_hash == self.password_hash:
                self.is_verified = True
                print(f"{_Colors2.GREEN}✅ Password benar! Sesi aman dimulai!{_Colors2.RESET}")
                return True
            else:
                print(f"{_Colors2.RED}❌ Password salah!{_Colors2.RESET}")
                attempt += 1
                if attempt < max_attempts:
                    print(f"{_Colors2.YELLOW}Kesempatan: {max_attempts - attempt}/{max_attempts}{_Colors2.RESET}")
        
        print(f"{_Colors2.RED}❌ Gagal verifikasi!{_Colors2.RESET}")
        return False

def _check_license():
    print(f"""
{_Colors2.BOLD}{_Colors2.CYAN}
╔══════════════════════════════════════════════════════════╗
║              🔒 LICENSE VERIFICATION                     ║
║                 3 LINK ROTATION                          ║
╚══════════════════════════════════════════════════════════╝
{_Colors2.RESET}""")
    
    license_mgr = _SecureLicense()
    if not license_mgr.verify():
        print(f"\n{_Colors2.RED}❌ License verification failed!{_Colors2.RESET}")
        import sys as _sys
        _sys.exit(1)
    
    print(f"\n{_Colors2.GREEN}✅ License verified!{_Colors2.RESET}")
    print(f"{_Colors2.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{_Colors2.RESET}")
    print()

# Panggil license check sebelum script utama
_check_license()

# ========================================
# SCRIPT ASLI ROLLERCOIN (TIDAK DIUBAH)
# =======================================

async def fast_json(self) -> Any | None:
    body = await self.read()
    try:
        return orjson.loads(body)
    except Exception as e:
        print(f"⚠️ fast_json orjson fail: {e}")
        try:
            return json.loads(body.decode("utf-8", "replace"))
        except Exception as e2:
            print(f"⚠️ fast_json fallback json fail: {e2}")
            return None


aiohttp.ClientResponse.json = fast_json

if sys.platform.startswith("win"):
    if sys.version_info < (3, 14):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass
else:
    pass

DEFAULT_TIMEOUT = 10
NAME_BOT = "Rollercoin"
T = TypeVar("T")


class BoundedSet(Generic[T]):
    def __init__(self, maxlen: int = 10000) -> None:
        self._set: set[T] = set()
        self._dq: deque[T] = deque()
        self.maxlen: int = maxlen

    def __contains__(self, item: T) -> bool:
        return item in self._set

    def add(self, item: T) -> None:
        if item in self._set:
            return
        self._set.add(item)
        self._dq.append(item)
        if len(self._dq) > self.maxlen:
            old: T = self._dq.popleft()
            try:
                self._set.remove(old)
            except KeyError as e:
                print(f"⚠️ BoundedSet.remove error: {e}")

    def clear(self) -> None:
        try:
            self._set.clear()
        except Exception as e:
            print(f"⚠️ BoundedSet.clear.set: {e}")
        try:
            self._dq.clear()
        except Exception as e:
            print(f"⚠️ BoundedSet.clear.deque: {e}")

    def __len__(self) -> int:
        return len(self._dq)


colorama_init(autoreset=True)
_global_ua = None


def now_ts() -> str:
    return datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S]")


# ======================== BANNER BARU ========================
def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║     ██████╗  ██████╗ ██╗     ██╗     ███████╗██████╗    ║")
    print("║     ██╔══██╗██╔═══██╗██║     ██║     ██╔════╝██╔══██╗   ║")
    print("║     ██████╔╝██║   ██║██║     ██║     █████╗  ██████╔╝   ║")
    print("║     ██╔══██╗██║   ██║██║     ██║     ██╔══╝  ██╔══██╗   ║")
    print("║     ██║  ██║╚██████╔╝███████╗███████╗███████╗██║  ██║   ║")
    print("║     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝   ║")
    print("║                                                          ║")
    print(f"║     {Fore.YELLOW}ROLLERCOIN AUTOMATION SYSTEM v2.0{Fore.CYAN}                ║")
    print(f"║     {Fore.BLUE}G H O F U R{Fore.CYAN}                           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Fore.RESET}")


def typing_effect(text: str, color=Fore.CYAN, delay: float = 0.02):
    print(color, end='')
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Fore.RESET)


class ProxyState(TypedDict):
    score: float
    latency: float | None
    fail: int
    success: int
    last_ok: float
    last_fail: float
    alive: bool
    cooldown_until: float
    last_test: float
    last_ip: str | None
    ip_history: set[str]


class ProxyManager:
    def __init__(
        self, proxies: list[str] | None = None, recovery_interval: float = 15, connect_timeout: float = 6
    ) -> None:
        self.lock: asyncio.Lock = asyncio.Lock()
        self.shared_session: aiohttp.ClientSession | None = None
        self.proxies: dict[str, ProxyState] = {}
        for p in proxies or []:
            try:
                self._init_proxy(p)
            except Exception as e:
                print(f"⚠️ ProxyManager init proxy error: {e}")
        self.recovery_interval: float = recovery_interval
        self.connect_timeout: float = connect_timeout
        self.recovery_task: asyncio.Task[None] | None = None
        self._in_use: set[str] = set()

    def _init_proxy(self, p: str) -> None:
        self.proxies[p] = {
            "score": 1.0,
            "latency": None,
            "fail": 0,
            "success": 0,
            "last_ok": 0.0,
            "last_fail": 0.0,
            "alive": True,
            "cooldown_until": 0.0,
            "last_test": 0.0,
            "last_ip": None,
            "ip_history": set(),
        }

    def attach_session(self, session: aiohttp.ClientSession) -> None:
        self.shared_session = session

    async def start_recovery_async(self) -> None:
        if self.recovery_task:
            return
        loop = asyncio.get_running_loop()
        self.recovery_task = loop.create_task(self._recovery_loop())

    async def stop_recovery_async(self) -> None:
        if self.recovery_task:
            self.recovery_task.cancel()
            try:
                await self.recovery_task
            except Exception:
                pass
            self.recovery_task = None

    async def _recovery_loop(self) -> collections.NoReturn:
        while True:
            await asyncio.sleep(self.recovery_interval)
            await self._recovery_cycle()

    async def _recovery_cycle(self) -> None:
        now = time.time()
        async with self.lock:
            plist = [p for p, d in self.proxies.items() if not d["alive"] or now - d["last_ok"] > 45]
        if not plist:
            return
        await asyncio.gather(*(self._test_proxy(p) for p in plist), return_exceptions=True)

    async def _test_proxy(self, proxy: str) -> None:
        if not self.shared_session:
            return
        url = "https://api.ipify.org?format=json"
        timeout = aiohttp.ClientTimeout(total=self.connect_timeout)
        try:
            async with self.shared_session.get(url, proxy=proxy, timeout=timeout) as r:
                data = await r.json()
                ip = data.get("ip")
            async with self.lock:
                d = self.proxies.get(proxy)
                if not d:
                    return
                d["last_ip"] = ip
                d["ip_history"].add(ip)
                if len(d["ip_history"]) > 1:
                    d["score"] += 1.5
            await self._mark_success_internal(proxy, 0.1)
        except:
            await self._mark_failure_internal(proxy)

    async def _mark_success_internal(self, proxy: str, latency: float) -> None:
        async with self.lock:
            d = self.proxies.get(proxy)
            if not d:
                return
            d["alive"] = True
            d["fail"] = 0
            d["success"] += 1
            d["latency"] = latency
            d["score"] = min(d["score"] + 0.5, 10.0)
            d["last_ok"] = time.time()
            d["cooldown_until"] = 0.0

    async def _mark_failure_internal(self, proxy: str) -> None:
        async with self.lock:
            d = self.proxies.get(proxy)
            if not d:
                return
            d["fail"] += 1
            d["score"] = max(d["score"] - 1.0, 0.1)
            d["alive"] = False
            d["last_fail"] = time.time()
            d["cooldown_until"] = time.time() + 8.0

    async def reserve_proxy(self, proxy: str) -> None:
        async with self.lock:
            self._in_use.add(proxy)

    def is_reserved(self, proxy: str) -> bool:
        return proxy in self._in_use

    async def release_proxy(self, proxy: str) -> None:
        async with self.lock:
            self._in_use.discard(proxy)

    def in_use_count(self) -> int:
        return len(self._in_use)

    def available_count(self) -> int:
        return sum((1 for p, d in self.proxies.items() if p not in self._in_use and d["alive"] and (d["score"] >= 1.0)))

    async def mark_success(self, proxy: str, latency: float) -> None:
        await self._mark_success_internal(proxy, latency)

    async def mark_failure(self, proxy: str) -> None:
        await self._mark_failure_internal(proxy)

    async def get_proxy(self) -> str | None:
        async with self.lock:
            now = time.time()
            alive = [
                (p, d)
                for p, d in self.proxies.items()
                if d["alive"] and d["cooldown_until"] <= now and (p not in self._in_use)
            ]
            if not alive:
                return None
            weighted: list[tuple[str, float]] = []
            for p, d in alive:
                if p in self._in_use:
                    continue
                base = max(d["score"], 0.1)
                latf = max(0.0, 0.8 - (d["latency"] or 0) * 2)
                weight = base + latf
                if weight <= 0:
                    weight = 0.1
                weighted.append((p, weight))
            if not weighted:
                return None
            total = sum((w for _, w in weighted))
            if total <= 0:
                return weighted[0][0]
            r = random.uniform(0, total)
            cum = 0.0
            for p, w in weighted:
                cum += w
                if r <= cum:
                    self._in_use.add(p)
                    return p
            p = weighted[-1][0]
            self._in_use.add(p)
            return p

    def get_stats(self, proxy: str) -> tuple[float | None, float, float]:
        d = self.proxies.get(proxy)
        if not d:
            return None, 1.0, 0.0
        total = d.get("success", 0) + d.get("fail", 0)
        fail_rate = d.get("fail", 0) / max(1, total)
        score = d.get("score", 0.0)
        return d.get("latency"), fail_rate, score

    def snapshot(self) -> dict:
        return {
            "total": len(self.proxies),
            "in_use": len(self._in_use),
            "available": self.available_count(),
            "alive": sum(1 for d in self.proxies.values() if d["alive"]),
        }


def _ensure_running_loop_or_raise() -> None:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        raise RuntimeError(
            "This library must be used from within an asyncio event loop. Call from async code (or use asyncio.run() at top-level)."
        )


R = TypeVar("R")


def _run_blocking_in_thread[R](func: Callable[..., R], *args, **kwargs) -> Awaitable[R]:
    try:
        return asyncio.to_thread(functools.partial(func, *args, **kwargs))
    except Exception as e:
        print(f"⚠️ Thread dispatch failed: {e}")
        raise


F = TypeVar("F", bound=Callable[..., Any])


def wrapper_feature[F: Callable[..., Any]](func: F) -> F:
    is_login = func.__name__.lower() == "login"

    async def _wait_proxy_ready(self) -> None:
        while not getattr(self, "_proxy_ready", False):
            await asyncio.sleep(0.02)

    @functools.wraps(func)
    async def _async_wrapper(*args, **kwargs):
        _ensure_running_loop_or_raise()
        self = args[0] if args else None
        if is_login and getattr(self, "prepare_session", None):
            try:
                maybe = self.prepare_session()
                if inspect.isawaitable(maybe):
                    await maybe
                await _wait_proxy_ready(self)
            except Exception:
                pass
        try:
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return await _run_blocking_in_thread(func, *args, **kwargs)
        except Exception as e:
            try:
                if self:
                    self.log(f"Error in {func.__name__}: {e}", Fore.RED)
            except Exception:
                pass
            return None
        finally:
            try:
                if getattr(self, "clear_locals", None):
                    maybe = self.clear_locals()
                    if inspect.isawaitable(maybe):
                        await maybe
                    else:
                        await _run_blocking_in_thread(lambda: maybe)
            except Exception:
                pass

    def wrapper(*args, **kwargs):
        try:
            asyncio.get_running_loop()
            return _async_wrapper(*args, **kwargs)
        except RuntimeError:
            raise RuntimeError("wrapper_feature-decorated function must be called from an asyncio event loop.")

    return wrapper


def sync_feature(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        self = args[0]
        # Initialize _sync_lock if it doesn't exist
        if not hasattr(self, '_sync_lock'):
            self._sync_lock = asyncio.Lock()
        async with self._sync_lock:
            return await func(*args, **kwargs)

    return wrapper


class Bot:
    BASE_URL = "https://rollercoin.com"
    HEADERS = {
        "Accept": "application/json",
        "Accept-Encoding": "br",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://rollercoin.com/game",
        "Sec-Ch-Ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    def __init__(self, use_proxy: bool = False, proxy_list: list | None = None, load_on_init: bool = True) -> None:
        self.use_proxy = use_proxy
        self.proxy_list_raw = proxy_list or []
        self.load_on_init = load_on_init
        self._aiohttp_session = None
        self.session_lock = asyncio.Lock()
        self._prepared = False
        self._preparing = False
        self._suppress_local_session_log = not load_on_init
        self._base_headers = dict(getattr(self, "HEADERS", {}) or {})
        self.shared_executor = None
        self.executor = None
        self._transport_pref = "aiohttp"
        self.proxy_manager = None
        self.config = {}
        self.query_list = []
        self.proxy_list = []
        self.good_proxies = []
        self.bad_proxies = []
        self.active_workers = 0
        self.dynamic_worker_target = 1
        self.io_sema = None
        self.account_index = None
        self.access_token = None
        self.refresh_token = None
        self.csrf_token = None
        self.error_count = 0
        # Initialize these here
        self._sync_lock = asyncio.Lock()
        self._file_cache = {}
        
        # --- VARIABEL UNTUK SATU KOTAK BERJALAN ---
        self._dashboard_header_printed = False
        self._account_name = "Akun Tidak Diketahui"

    # ==================== TAMPILAN SATU KOTAK BERJALAN (DASHBOARD) ====================
    def print_dashboard_header(self, account_label: str = "Akun"):
        """Mencetak header kotak utama yang berisi informasi akun"""
        if self._dashboard_header_printed:
            return
        self._dashboard_header_printed = True
        
        # Simpan nama akun
        if account_label:
            self._account_name = account_label
            
        timestamp = now_ts()
        width = 64
        border = Fore.CYAN + "═" * width + Fore.RESET
        title = f"{Fore.YELLOW}🤖 ROLLERCOIN BOT DASHBOARD{Fore.RESET}"
        account_info = f"{Fore.MAGENTA}👤 AKUN: {self._account_name}{Fore.RESET}"
        time_info = f"{Fore.GREEN}⏰ WAKTU: {timestamp}{Fore.RESET}"
        
        print(f"\n{border}")
        print(f"{title:^{width}}")
        print(f"{border}")
        print(f"{account_info:<{width}}")
        print(f"{time_info:<{width}}")
        print(f"{border}")
        print(f"{Fore.CYAN}📌 STATUS LOG{Fore.RESET}")
        print(f"{border}")

    def log(self, message: str, color: str = Fore.WHITE, account_name: str = None):
        """
        Menampilkan log mengalir di DALAM satu kotak dashboard yang sama.
        """
        # HAPUS TOTAL SPAM WS.RECV
        if "ws.recv got data" in message:
            return

        timestamp = now_ts()
        prefix = ""
        if getattr(self, "account_index", None) is not None:
            prefix = f" A{self.account_index}"

        # Cetak hanya isi lognya saja, karena header kotak sudah dicetak di awal
        print(f"{color}│  {timestamp}{prefix} → {message}{Fore.RESET}")

    # ==========================================================================

    async def ainit_main(self) -> None:
        self.config = await self.load_config()
        # Ensure these are initialized
        if not hasattr(self, '_sync_lock'):
            self._sync_lock = asyncio.Lock()
        if not hasattr(self, '_file_cache'):
            self._file_cache = {}
            
        if self.config.get("reff", False):
            try:
                self.log("Reff mode diaktifkan via config.json", Fore.CYAN)
                await self.reff()
            except Exception:
                pass
        # Load tokens from config or use direct input
        if self.config.get("access_token") and self.config.get("refresh_token") and self.config.get("csrf_token"):
            self.access_token = self.config.get("access_token")
            self.refresh_token = self.config.get("refresh_token")
            self.csrf_token = self.config.get("csrf_token")
            self.log("Tokens berhasil dimuat dari config.json", Fore.GREEN)
        
        # If no config tokens, try to get from query_list or ask user
        if not self.access_token:
            self.query_list = await self.load_query(self.config.get("query_file", "query.txt"))
            if not self.query_list:
                self.log("Tidak ada token ditemukan. Silakan input token manual.", Fore.YELLOW)
                await self.get_tokens_from_input()
                if self.access_token and self.refresh_token and self.csrf_token:
                    self.query_list = [f"{self.access_token}|{self.refresh_token}|{self.csrf_token}"]
        
        self.proxy_list = await self.load_proxies(self.config.get("proxy_file", "proxy.txt"))
        self._prepared = True

    async def get_tokens_from_input(self) -> None:
        """Get tokens directly from user input (Fallback)"""
        print("\n" + "═" * 60)
        print(f"{Fore.CYAN}🔑 TOKEN INPUT MANUAL DIPERLUKAN{Fore.RESET}")
        print("═" * 60)
        print(f"{Fore.YELLOW}Silakan masukkan token Rollercoin Anda:{Fore.RESET}")
        print(f"(Cari di Developer Tools Browser -> Application -> Local Storage)")
        print("")
        
        self.access_token = input(f"{Fore.GREEN}Access Token: {Fore.RESET}").strip()
        self.refresh_token = input(f"{Fore.GREEN}Refresh Token: {Fore.RESET}").strip()
        self.csrf_token = input(f"{Fore.GREEN}CSRF Token: {Fore.RESET}").strip()
        
        if self.access_token and self.refresh_token and self.csrf_token:
            self.log("Token berhasil diterima.", Fore.GREEN)
            # Save to config for future use
            try:
                cfg = await self.load_config(suppress_log=True)
                if not cfg:
                    cfg = {}
                cfg["access_token"] = self.access_token
                cfg["refresh_token"] = self.refresh_token
                cfg["csrf_token"] = self.csrf_token
                async with aiofiles.open("config.json", "w", encoding="utf-8") as f:
                    await f.write(json.dumps(cfg, indent=2))
                self.log("Token disimpan ke config.json untuk penggunaan berikutnya.", Fore.GREEN)
            except Exception as e:
                self.log(f"Gagal menyimpan token ke config: {e}", Fore.YELLOW)
        else:
            self.log("Input token tidak valid. Semua token wajib diisi.", Fore.RED)

    async def ainit_worker(self, base) -> None:
        self.config = base.config
        # Copy sync lock and file cache from base
        self._sync_lock = getattr(base, "_sync_lock", asyncio.Lock())
        self._file_cache = getattr(base, "_file_cache", {})
        
        try:
            self.query_list = list(base.query_list)
        except Exception:
            self.query_list = copy.deepcopy(base.query_list)
        self.proxy_list = list(getattr(base, "proxy_list", []))
        self.good_proxies = list(getattr(base, "good_proxies", []))
        self.bad_proxies = list(getattr(base, "bad_proxies", []))
        self.proxy_manager = getattr(base, "proxy_manager", None)
        self.shared_executor = getattr(base, "shared_executor", None)
        self._aiohttp_session = getattr(base, "_aiohttp_session", None)
        self.access_token = getattr(base, "access_token", None)
        self.refresh_token = getattr(base, "refresh_token", None)
        self.csrf_token = getattr(base, "csrf_token", None)
        self._prepared = True

    def banner(self) -> None:
        banner()

    async def _merge_headers(self, extra: dict | None) -> dict:
        if not extra:
            return self._base_headers
        new_hdr = self._base_headers.copy()
        new_hdr.update(extra)
        return new_hdr

    class AioRespWrapper:
        __slots__ = ("_text_cache", "body", "headers", "reason", "status", "url")

        def __init__(self, orig, body) -> None:
            self.status = orig.status
            self.headers = orig.headers
            self.reason = getattr(orig, "reason", "")
            self.url = getattr(orig, "url", None)
            self.body = body
            self._text_cache = None

        async def text(self):
            if self._text_cache is None:
                try:
                    content_type = self.headers.get("Content-Type", "")
                    if "charset=" in content_type:
                        charset = content_type.split("charset=")[-1].split(";")[0].strip()
                    else:
                        charset = "utf-8"
                    self._text_cache = self.body.decode(charset, errors="replace")
                except:
                    self._text_cache = self.body.decode("utf-8", errors="replace")
            return self._text_cache

        async def json(self):
            return json.loads(await self.text())

        async def read(self):
            return self.body

    async def set_header(self, key, value) -> None:
        if not hasattr(self, "_base_headers"):
            self._base_headers = {}
        self._base_headers[key] = value

    async def del_header(self, key) -> None:
        if hasattr(self, "_base_headers") and key in self._base_headers:
            del self._base_headers[key]

    class _TLSLikeResponse:
        __slots__ = ("headers", "reason", "status", "url")

        def __init__(self, status, headers, url) -> None:
            self.status = status
            self.headers = headers or {}
            self.reason = "TLS"
            self.url = url

    async def _request_curl_cffi(
        self,
        method: str,
        url: str,
        *,
        headers: dict | None = None,
        params: dict | None = None,
        data=None,
        json_data=None,
        timeout: float | None = None,
        proxy: str | None = None,
    ):
        from curl_cffi import requests

        method = method.upper()
        headers = headers or {}
        timeout = timeout or 12.0

        def _sync_call():
            session = requests.Session(impersonate="chrome124", timeout=timeout)
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
            try:
                method_lower = method.lower()
                if not hasattr(session, method_lower):
                    raise RuntimeError(f"curl_cffi does not support method: {method}")
                func = getattr(session, method_lower)
                resp = func(url, headers=headers, params=params, data=data, json=json_data)
                return resp
            finally:
                try:
                    session.close()
                except:
                    pass

        resp = await asyncio.to_thread(_sync_call)
        body = resp.content or b""
        normalized_headers = CIMultiDict()
        for k, v in resp.headers.items():
            if isinstance(v, list):
                for item in v:
                    normalized_headers.add(k, item)
            else:
                normalized_headers.add(k, v)
        fake_resp = self._TLSLikeResponse(status=resp.status_code, headers=normalized_headers, url=url)
        return self.AioRespWrapper(fake_resp, body)

    async def _request_tls(
        self,
        method: str,
        url: str,
        *,
        headers: dict | None = None,
        params: dict | None = None,
        data=None,
        json_data=None,
        timeout: float | None = None,
        proxy: str | None = None,
    ):
        import tls_client

        method = method.upper()
        headers = headers or {}
        timeout = timeout or 12.0

        def _sync_tls_call():
            session = tls_client.Session(
                client_identifier=random.choice(["chrome_120", "chrome_119", "chrome_118"]),
                random_tls_extension_order=True,
            )
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
            try:
                method_lower = method.lower()
                if not hasattr(session, method_lower):
                    raise RuntimeError(f"TLS client does not support method: {method}")
                func = getattr(session, method_lower)
                resp = func(url, headers=headers, params=params, data=data, json=json_data, timeout_seconds=timeout)
                return resp
            finally:
                try:
                    session.close()
                except:
                    pass

        resp = await asyncio.to_thread(_sync_tls_call)
        body = resp.content or b""
        normalized_headers = CIMultiDict()
        for k, v in resp.headers.items():
            if isinstance(v, list):
                for item in v:
                    normalized_headers.add(k, item)
            else:
                normalized_headers.add(k, v)
        fake_resp = self._TLSLikeResponse(status=resp.status_code, headers=normalized_headers, url=url)
        return self.AioRespWrapper(fake_resp, body)

    async def _request_aiohttp(
        self,
        method: str,
        url: str,
        *,
        headers: dict | None = None,
        params: dict | None = None,
        data=None,
        json_data=None,
        files: dict | None = None,
        timeout: float | None = None,
        proxy: str | None = None,
        allow_redirects: bool = True,
        use_session: bool = True,
    ):
        method = method.upper()
        headers = headers or {}
        timeout = timeout or 10.0
        temp_session = False
        if use_session:
            if getattr(self, "_aiohttp_session", None) is None or self._aiohttp_session.closed:
                await self.prepare_session()
            session = self._aiohttp_session
        else:
            session = aiohttp.ClientSession()
            temp_session = True
        try:
            req_kwargs = {
                "allow_redirects": allow_redirects,
                "timeout": aiohttp.ClientTimeout(total=timeout),
                "headers": headers,
            }
            if params:
                req_kwargs["params"] = params
            if files is not None:
                form = aiohttp.FormData()
                if data:
                    if isinstance(data, dict):
                        for k, v in data.items():
                            form.add_field(k, str(v))
                    else:
                        raise TypeError("data must be dict when using files")
                for field, fileinfo in files.items():
                    form.add_field(
                        name=field,
                        value=fileinfo.get("content", b""),
                        filename=fileinfo.get("filename", "file.bin"),
                        content_type=fileinfo.get("content_type", "application/octet-stream"),
                    )
                req_kwargs["data"] = form
            elif json_data is not None:
                req_kwargs["json"] = json_data
            elif data is not None:
                req_kwargs["data"] = data
            if proxy:
                req_kwargs["proxy"] = proxy
            resp = await session.request(method, url, **req_kwargs)
            body = await resp.read()
            return self.AioRespWrapper(resp, body)
        finally:
            if temp_session:
                try:
                    await session.close()
                except:
                    pass

    async def _get_ip(self, proxy=None):
        try:
            import aiohttp

            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get("https://api.ipify.org?format=json", proxy=proxy) as r:
                    data = await r.json()
                    return data.get("ip")
        except:
            return "unknown"

    async def _request(
        self,
        method: str,
        url_or_path: str,
        *,
        headers: dict | None = None,
        params: dict | None = None,
        data=None,
        json_data=None,
        files: dict | None = None,
        timeout: float | None = None,
        use_session: bool = True,
        allow_redirects: bool = True,
        read_body: bool = True,
        parse_json: bool = True,
        retries: int = 3,
        backoff: float = 0.5,
        allow_proxy: bool = True,
        debug: bool = False,
        transport: str = "aiohttp",
        clean_headers: bool = False,
        early_return_status: set[int] | None = None,
    ):
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        method = method.upper()
        headers = headers or {}
        timeout = timeout or 10.0
        if not url_or_path.lower().startswith("http"):
            url = self.BASE_URL.rstrip("/") + "/" + url_or_path.lstrip("/")
        else:
            url = url_or_path
        last_exc = None
        attempt = 1
        adaptive_retries = retries
        switch_to_tls = False
        rate_limit_hits = 0
        MAX_429_BEFORE_TLS = 3
        early_return_status = early_return_status or set()
        while attempt <= adaptive_retries + 1:
            chosen_proxy = None
            if debug and self.proxy_manager:
                self.log(
                    f"📊 Proxy stats → total={len(self.proxy_manager.proxies)} | available={self.proxy_manager.available_count()} | in_use={self.proxy_manager.in_use_count()}",
                    Fore.GREEN,
                )
            if allow_proxy and getattr(self, "proxy_manager", None):
                try:
                    chosen_proxy = await self.proxy_manager.get_proxy()
                    chosen_proxy = self.normalize_proxy(chosen_proxy)
                    if chosen_proxy:
                        self.proxy = chosen_proxy
                except Exception as e:
                    self.log(f"❌ Error in chosen proxy: {e}", Fore.RED)
                    chosen_proxy = None
            if chosen_proxy:
                p = self.compute_adaptive_proxy_params(chosen_proxy)
                adaptive_retries = int(p.get("retries", retries))
            else:
                adaptive_retries = retries
            if clean_headers:
                if headers:
                    final_headers = headers
                else:
                    final_headers = {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}
            else:
                final_headers = await self._merge_headers(headers)
            if debug:
                ip_info = None
                if debug and chosen_proxy:
                    ip_info = await self._get_ip(chosen_proxy)
                self.log(
                    f"\n[DEBUG REQ] {method} {url}\n  • proxy={chosen_proxy}\n  • ip={ip_info}\n • timeout={timeout}\n  • attempt={attempt}/{adaptive_retries}\n  • headers={final_headers}\n  • params={params}\n  • json={json_data}\n  • data={str(data)[:200]}\n",
                    Fore.CYAN,
                )
            try:
                if switch_to_tls or transport == "tls" or self._transport_pref == "tls":
                    resp = await self._request_tls(
                        method,
                        url,
                        headers=final_headers,
                        params=params,
                        data=data,
                        json_data=json_data,
                        timeout=timeout,
                        proxy=chosen_proxy,
                    )
                elif transport == "curl" or self._transport_pref == "curl":
                    resp = await self._request_curl_cffi(
                        method,
                        url,
                        headers=final_headers,
                        params=params,
                        data=data,
                        json_data=json_data,
                        timeout=timeout,
                        proxy=chosen_proxy,
                    )
                else:
                    resp = await self._request_aiohttp(
                        method,
                        url,
                        headers=final_headers,
                        params=params,
                        data=data,
                        json_data=json_data,
                        files=files,
                        timeout=timeout,
                        proxy=chosen_proxy,
                        allow_redirects=allow_redirects,
                        use_session=use_session,
                    )
                if resp.status in early_return_status:
                    if debug:
                        self.log(f"⚡ Early return triggered for status {resp.status}", Fore.MAGENTA)
                    body_bytes = b""
                    decoded = None
                    if read_body:
                        body_bytes = resp.body
                        if parse_json:
                            try:
                                decoded = json.loads(body_bytes.decode("utf-8", "replace"))
                            except:
                                decoded = None
                    return (resp, decoded)
                if resp.status == 429:
                    rate_limit_hits += 1
                    delay = 10 * rate_limit_hits * random.uniform(0.8, 1.2)
                    self.log(
                        f"⏳ 429 detected ({rate_limit_hits}/{MAX_429_BEFORE_TLS}) — sleeping {delay}s", Fore.YELLOW
                    )
                    if rate_limit_hits >= MAX_429_BEFORE_TLS:
                        self.log("🧬 Switching transport to TLS after repeated 429", Fore.MAGENTA)
                        self._transport_pref = "tls"
                        switch_to_tls = True
                        rate_limit_hits = 0
                        attempt += 1
                        continue
                    await asyncio.sleep(delay)
                    attempt += 1
                    continue
                if resp.status == 403:
                    if not switch_to_tls:
                        self.log(f"🚪 Auth gate {resp.status} — TLS fallback (once)", Fore.MAGENTA)
                        switch_to_tls = True
                        attempt += 1
                        continue
                    self.log(f"❌ Auth failed ({resp.status}) — returning to caller", Fore.RED)
                    return (resp, None)
                if resp.status == 401:
                    await self.refresh_token_flow(refresh_token=self.refresh_token, identity=self.csrf_token)
                    continue
                body_bytes = b""
                decoded = None
                if read_body:
                    body_bytes = resp.body
                    if debug:
                        preview = body_bytes[:300]
                        try:
                            preview = preview.decode("utf-8", "replace")
                        except:
                            preview = repr(preview)
                        try:
                            headers_str = "\n".join([f"    {k}: {v}" for k, v in resp.headers.items()])
                        except:
                            headers_str = str(resp.headers)
                        self.log(
                            f"[DEBUG RESP]\n  • status={resp.status}\n  • headers=\n{headers_str}\n  • body_bytes={len(body_bytes)}\n  • preview={preview}\n",
                            Fore.BLUE,
                        )
                    if parse_json:
                        try:
                            decoded = json.loads(body_bytes.decode("utf-8", "replace"))
                        except:
                            decoded = None
                return (resp, decoded)
            except Exception as e:
                last_exc = e
                self.log(
                    f"⚠️ Error attempt {attempt} | {method} {url}\n  • proxy={chosen_proxy}\n  • error={e}", Fore.YELLOW
                )
                if chosen_proxy and getattr(self, "proxy_manager", None):
                    try:
                        await self.proxy_manager.mark_failure(chosen_proxy)
                    except:
                        pass
                    self.proxy = None
                await asyncio.sleep(backoff * 2 ** (attempt - 1) * random.uniform(0.9, 1.1))
                attempt += 1
                continue
            finally:
                if chosen_proxy and getattr(self, "proxy_manager", None):
                    try:
                        await self.proxy_manager.release_proxy(chosen_proxy)
                    except:
                        pass
        self.log(f"❌ Gave up after {attempt - 1} attempts | {method} {url}\n  • last_error={last_exc}", Fore.RED)
        dummy = self.AioRespWrapper(
            type("Dummy", (), {"status": 599, "headers": {}, "reason": "FAILED", "url": url})(), b""
        )
        return (dummy, None)

    def memory_monitor(self) -> str:
        try:
            p = psutil.Process()
            mem = p.memory_info().rss
            return f"RSS={mem / 1024 / 1024:.2f} MB"
        except Exception:
            try:
                tracemalloc.start()
                s = tracemalloc.take_snapshot()
                total = sum(stat.size for stat in s.statistics("filename"))
                return f"tracemalloc_total={total / 1024 / 1024:.2f} MB"
            except Exception:
                return "unknown"

    def clear_locals(self) -> None:
        try:
            self.log(f"🔎 Memory before clear: {self.memory_monitor()}", Fore.MAGENTA)
        except Exception:
            pass
        try:
            frame = inspect.currentframe()
            if not frame:
                return
            caller = frame.f_back
            if caller and caller.f_back:
                caller = caller.f_back
            if not caller:
                return
            names = list(caller.f_locals.keys())
            for name in names:
                if name not in ("self",) and (not name.startswith("__")):
                    try:
                        del caller.f_locals[name]
                    except Exception:
                        try:
                            caller.f_locals[name] = None
                        except Exception:
                            pass
        except Exception:
            pass
        finally:
            try:
                gc.collect()
            except:
                pass
            try:
                self.log(f"✅ Memory after clear: {self.memory_monitor()}", Fore.LIGHTBLACK_EX)
            except:
                pass
            try:
                del frame
                del caller
            except:
                pass

    async def get_ua(self) -> str:
        global _global_ua
        if _global_ua is None:
            try:
                _global_ua = UserAgent()
            except Exception:
                _global_ua = None
        try:
            if _global_ua:
                ua = _global_ua.random
                if isinstance(ua, str):
                    return ua
        except:
            pass
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    async def _record_proxy_result(self, proxy, success: bool, latency: float | None = None) -> None:
        try:
            pm = getattr(self, "proxy_manager", None)
            if not pm:
                return
            proxy = self.normalize_proxy(proxy)
            if not proxy:
                return
            if success:
                try:
                    if latency is None:
                        await pm.mark_success(proxy)
                    else:
                        await pm.mark_success(proxy, latency=latency)
                except Exception:
                    pass
            else:
                try:
                    await pm.mark_failure(proxy)
                except Exception:
                    pass
        except Exception:
            pass

    def compute_adaptive_proxy_params(self, proxy) -> dict:
        pm = getattr(self, "proxy_manager", None)
        if pm is None or proxy is None:
            return {"timeout": 1.5, "retries": 1, "quarantine": 30}
        try:
            avg_lat, fail_rate, score = pm.get_stats(proxy)
            fail_rate = max(0.0, min(1.0, float(fail_rate or 0.0)))
            if avg_lat is None:
                timeout = 1.0
            else:
                timeout = max(2.0, min(15.0, avg_lat * 2.5 + 1.0))
            if fail_rate < 0.25:
                retries = 1
            elif fail_rate < 0.6:
                retries = 2
            else:
                retries = 3
            return {
                "timeout": float(timeout),
                "retries": retries,
                "quarantine": int(getattr(pm, "_quarantine_seconds", 30)),
            }
        except Exception:
            return {"timeout": 1.2, "retries": 1, "quarantine": 30}

    async def rotate_proxy_and_ua(self, force_new_proxy: bool = True, quick_test: bool = True) -> None:
        if not force_new_proxy and getattr(self, "proxy", None):
            return
        plist = list(getattr(self, "proxy_list", []) or [])
        if not plist:
            self.proxy = None
            return
        good_list = list(getattr(self, "good_proxies", []) or [])
        pm = getattr(self, "proxy_manager", None)

        async def choose_candidate_list():
            if good_list:
                return good_list[:]
            if pm:
                try:
                    c = await pm.get_proxy()
                    return [self.normalize_proxy(c)]
                except:
                    pass
            return plist[:]

        candidates = await choose_candidate_list()
        if not candidates:
            self.proxy = None
            return
        if quick_test:
            sem = asyncio.Semaphore(25)

            async def test_one(purl):
                async with sem:
                    ok = await self._async_test_proxy(purl)
                    return (purl, ok)

            tasks = [test_one(self.normalize_proxy(c)) for c in candidates]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            good = [p for p, ok in results if ok]
            if good:
                candidate = random.choice(good)
            else:
                candidate = random.choice(candidates)
        else:
            candidate = random.choice(candidates)
        await self.prepare_session()
        self.proxy = candidate

    @wrapper_feature
    async def reff(self) -> None:
        try:
            self.log("🎯 Running reff placeholder...", Fore.CYAN)
        except Exception as e:
            self.log(f"❌ reff error: {e}", Fore.RED)

    async def load_config(self, suppress_log: bool = False):
        try:
            async with aiofiles.open("config.json", encoding="utf-8") as f:
                text = await f.read()
                cfg = json.loads(text)
            if not suppress_log:
                self.log("✅ Config loaded", Fore.GREEN)
            return cfg
        except FileNotFoundError:
            if not suppress_log:
                self.log("⚠️ config.json not found (using minimal)", Fore.YELLOW)
            return {}
        except Exception as e:
            if not suppress_log:
                self.log(f"❌ Config parse error: {e}", Fore.RED)
            return {}

    async def load_query(self, path_file: str = "query.txt", limit: int | None = None, offset: int = 0) -> list:
        try:
            if not os.path.exists(path_file):
                return []
            async with aiofiles.open(path_file, encoding="utf-8") as f:
                lines = await f.readlines()
            queries = [ln.strip() for ln in lines if ln.strip()]
            total = len(queries)
            offset = max(offset, 0)
            offset = min(offset, total)
            sliced = queries[offset:]
            if limit is not None:
                limit = max(limit, 0)
                sliced = sliced[:limit]
            return sliced
        except Exception as e:
            try:
                self.log(f"❌ Query load error: {e}", Fore.RED)
            except Exception:
                pass
            return []

    async def write_file(self, task=None, file_key=None, return_cache=False):
        try:
            if not hasattr(self, "_file_cache"):
                self._file_cache = {}
            if file_key and file_key not in self._file_cache:
                self._file_cache[file_key] = set()
                try:
                    if os.path.exists(file_key):
                        async with aiofiles.open(file_key, encoding="utf-8") as f:
                            lines = await f.readlines()
                            self._file_cache[file_key] = {line.strip() for line in lines if line.strip()}
                except Exception as e:
                    print(f"⚠️ cache load error: {e}")
            if return_cache:
                return set(self._file_cache.get(file_key, set()))
            if task is None:
                if file_key and (not os.path.exists(file_key)):
                    async with aiofiles.open(file_key, "a"):
                        pass
                return True
            if not callable(task):
                raise TypeError("Task must be callable.")
            await self.file_writer_queue.put(task)
            return True
        except Exception as e:
            self.log(f"❌ Write File Error: {e}.", Fore.RED)
            return False

    async def get_tokens(self, filename="tokens.json"):
        if not hasattr(self, "_file_cache"):
            self._file_cache = {}
        if filename not in self._file_cache:
            self._file_cache[filename] = {}
            try:
                if os.path.exists(filename):
                    async with aiofiles.open(filename, encoding="utf-8") as f:
                        content = await f.read()
                        if content.strip():
                            self._file_cache[filename] = json.loads(content)
            except Exception as e:
                self.log(f"⚠️ Token cache init error: {e}", Fore.YELLOW)
        return self._file_cache[filename]

    async def save_token(self, identity, access, refresh, filename="tokens.json"):
        try:
            data = await self.get_tokens(filename)
            data[identity] = {"access_token": access, "refresh_token": refresh, "updated_at": int(time.time())}

            async def task(file_key=filename, payload=dict(data)):
                self._file_cache[file_key] = payload
                async with aiofiles.open(file_key, "w", encoding="utf-8") as f:
                    await f.write(json.dumps(payload, indent=2))

            await self.write_file(task, file_key=filename)
            self.log("💾 Token saved (cache + queue)", Fore.GREEN)
            return True
        except Exception as e:
            self.log(f"❌ Token save error: {e}", Fore.RED)
            return False

    @sync_feature
    async def refresh_token_flow(self, refresh_token: str | None = None, identity: str | None = None) -> bool:
        self.log("🔄 Refreshing access token...", Fore.YELLOW)
        refresh_token = refresh_token or self.refresh_token
        identity = identity or self.csrf_token
        if not refresh_token or not identity:
            self.log("❌ Refresh token / identity missing.", Fore.RED)
            return False
        try:
            await self.del_header("Authorization")
            _, res = await self._request("POST", "api/auth/refresh", json_data={"refresh_token": refresh_token})
            data = res.get("data", {})
            access = data.get("access_token")
            refresh = data.get("refresh_token")
            if not access or not refresh:
                raise ValueError("refresh response incomplete")
            self.access_token = access
            self.refresh_token = refresh
            await self.set_header("Authorization", f"Bearer {access}")
            await self.save_token(identity, access, refresh)
            self.log("✅ Token refreshed & persisted (cache + queue)", Fore.GREEN)
            self.log(f"    - Access : {access[:16]}...", Fore.CYAN)
            self.log(f"    - Refresh: {refresh[:16]}...", Fore.CYAN)
            await asyncio.sleep(3)
            return True
        except Exception as e:
            self.log(f"❌ Refresh token failed: {e}", Fore.RED)
            return False

    @wrapper_feature
    async def login(self, index: int) -> bool:
        self.log("🔐 Phase 1: access|refresh|csrf → profile", Fore.GREEN)
        if index < 0 or index >= len(self.query_list):
            self.log("❌ Invalid login index.", Fore.RED)
            return False
        raw = str(self.query_list[index]).strip()
        
        # Try to get tokens from config first, then fallback to query
        if self.access_token and self.refresh_token and self.csrf_token:
            self.log("🔑 Using tokens from config", Fore.GREEN)
        else:
            if raw.count("|") != 2:
                self.log("❌ Token format invalid (access|refresh|csrf) and no config tokens.", Fore.RED)
                return False
            access_old, refresh_old, csrf = map(str.strip, raw.split("|", 2))
            self.csrf_token = csrf
            self.access_token = access_old
            self.refresh_token = refresh_old
        
        tokens = await self.get_tokens()
        if self.csrf_token in tokens:
            t = tokens[self.csrf_token]
            self.access_token = t.get("access_token", self.access_token)
            self.refresh_token = t.get("refresh_token", self.refresh_token)
            self.log("🔁 Token loaded from cache", Fore.GREEN)
        
        await self.set_header("Authorization", f"Bearer {self.access_token}")
        await self.set_header("csrf-token", self.csrf_token)
        self.log("✅ Access & CSRF injected", Fore.GREEN)

        async def try_profile():
            try:
                resp, res = await self._request("GET", "api/profile/user-profile-data")
                data = res.get("data", {})
                if not data:
                    raise ValueError("profile data empty")
                self.log("👤 User Profile:", Fore.GREEN)
                self.log(f"    - Name      : {data.get('name')}", Fore.CYAN)
                self.log(f"    - Email     : {data.get('email')}", Fore.CYAN)
                self.log(f"    - User ID   : {data.get('id')}", Fore.CYAN)
                self.log(f"    - Premium   : {data.get('is_premium')}", Fore.CYAN)
                self.log(f"    - Miners    : {data.get('user_miners_amount')}", Fore.CYAN)
                self.log(f"    - Max Power : {data.get('max_total_power')}", Fore.CYAN)
                self.log(f"    - Banned    : {data.get('is_banned')}", Fore.CYAN)
                return True
            except Exception as e:
                self.log(f"❌ profile-data failed: {e}", Fore.RED)
                return False

        result = await try_profile()
        if result is True:
            return True
        self.log("🆘 Falling back to query_list token...", Fore.YELLOW)
        if raw.count("|") == 2:
            access_old, refresh_old, csrf = map(str.strip, raw.split("|", 2))
            self.access_token = access_old
            self.refresh_token = refresh_old
            self.csrf_token = csrf
            await self.set_header("Authorization", f"Bearer {self.access_token}")
            await self.set_header("csrf-token", self.csrf_token)
            if await try_profile():
                return True
        self.log("💀 Login totally failed.", Fore.RED)
        return False

    @wrapper_feature
    async def daily(self) -> bool:
        self.log("🎁 Phase: daily-bonus → collect", Fore.GREEN)
        if not getattr(self, "access_token", None) or not getattr(self, "csrf_token", None):
            self.log("❌ Token or CSRF not initialized. Login first.", Fore.RED)
            return False
        try:
            _, res = await self._request("GET", "api/season/daily-bonus")
            data = res.get("data", {})
            if not data:
                raise ValueError("daily bonus data empty")
            current_day = data.get("current_user_day", 0)
            rewards = data.get("daily_rewards") or []
            if current_day == 0 or not rewards:
                self.log("ℹ️ No active daily bonus (day=0). Skipped.", Fore.YELLOW)
                return True
            self.log(f"📆 Current Day: {current_day}", Fore.CYAN)
            target = next((r for r in rewards if not r.get("claimed")), None)
            if not target:
                self.log("✅ Daily bonus already claimed today.", Fore.GREEN)
                return True
            day = target.get("day")
            xp = target.get("xp")
            self.log(f"🎯 Claiming Day {day} reward (+{xp} XP)", Fore.YELLOW)
            _, res = await self._request("POST", "api/season/collect-daily")
            if not res.get("success"):
                raise ValueError(res.get("error") or "claim failed")
            claim_data = res.get("data", {})
            self.log("✅ Daily bonus claimed!", Fore.GREEN)
            self.log(f"    - Day       : {day}", Fore.CYAN)
            self.log(f"    - XP        : +{xp}", Fore.CYAN)
            self.log(f"    - Level Up  : {claim_data.get('is_level_up')}", Fore.CYAN)
            self.log(f"    - Claim Date: {claim_data.get('claim_date')}", Fore.CYAN)
            return True
        except Exception as e:
            self.log(f"❌ Daily bonus failed: {e}", Fore.RED)
            return False

    @wrapper_feature
    async def batery(self) -> bool:
        self.log("🔋 Phase: battery-check → recharge", Fore.GREEN)
        if not getattr(self, "access_token", None) or not getattr(self, "csrf_token", None):
            self.log("❌ Token or CSRF not initialized. Login first.", Fore.RED)
            return False
        try:
            _, res = await self._request("GET", "api/league/user-electricity-info")
            if not res or not res.get("success"):
                raise ValueError(res.get("error") if res else "failed to get battery info")
            data = res.get("data", {})
            batteries = data.get("user_batteries_count", 0)
            total_cells = data.get("total_cells_count")
            active_cells = data.get("active_cells_count", 0)
            recharge_time = data.get("time_to_recharge")
            self.log(f"🔋 Batteries      : {batteries}", Fore.CYAN)
            self.log(f"🧬 Total Cells   : {total_cells}", Fore.CYAN)
            self.log(f"⚡ Active Cells  : {active_cells}", Fore.CYAN)
            self.log(f"⏳ Recharge Time : {recharge_time}", Fore.CYAN)
            if total_cells != 4:
                self.log("❌ Total cells is not 4. Abort.", Fore.RED)
                return False
            if active_cells > 1:
                self.log("ℹ️ Cells still sufficient. Skipping recharge.", Fore.YELLOW)
                return True
            if active_cells == 0:
                self.log("🆓 Active cells = 0 → claiming FREE recharge first!", Fore.YELLOW)
                _, free_res = await self._request("POST", "api/league/recharge-electricity-free")
                if not free_res or not free_res.get("success"):
                    raise ValueError(free_res.get("error") if free_res else "free recharge failed")
                fdata = free_res.get("data", {})
                active_cells = fdata.get("active_cells_count", 0)
                self.log("✅ Free recharge success!", Fore.GREEN)
                self.log(f"    - Active Cells  : {active_cells}", Fore.CYAN)
                self.log(f"    - Next Recharge : {fdata.get('time_to_recharge')}", Fore.CYAN)
            if active_cells <= 1:
                if batteries <= 0:
                    self.log("❌ No batteries left. Cannot do normal recharge.", Fore.RED)
                    return False
                self.log("🚀 Active cells <= 1, starting paid recharge!", Fore.YELLOW)
                _, res = await self._request("POST", "api/league/recharge-electricity")
                if not res or not res.get("success"):
                    raise ValueError(res.get("error") if res else "recharge failed")
                rdata = res.get("data", {})
                self.log("✅ Recharge successful!", Fore.GREEN)
                self.log(f"    - Batteries Left : {rdata.get('user_batteries_count')}", Fore.CYAN)
                self.log(f"    - Active Cells  : {rdata.get('active_cells_count')}", Fore.CYAN)
                self.log(f"    - Next Recharge : {rdata.get('time_to_recharge')}", Fore.CYAN)
            return True
        except Exception as e:
            self.log(f"❌ Battery process failed: {e}", Fore.RED)
            return False

    @wrapper_feature
    async def hamster(self) -> bool:
        self.log("🐹 Phase: hamster-check → upgrade → expedition", Fore.GREEN)
        if not getattr(self, "access_token", None) or not getattr(self, "csrf_token", None):
            self.log("❌ Token or CSRF not initialized. Login first.", Fore.RED)
            return False
        try:
            _, res = await self._request(
                "GET", "api/pets/user-pets", params={"type": "hamsters", "skip": 0, "limit": 20}
            )
            if not res or not res.get("success"):
                raise ValueError(res.get("error") if res else "failed to get hamster list")
            pets = res.get("data", {}).get("pets", [])
            if not pets:
                self.log("ℹ️ No hamsters found.", Fore.YELLOW)
                return True
            _, exp_res = await self._request("GET", "api/expeditions/list")
            if not exp_res or not exp_res.get("success"):
                raise ValueError(exp_res.get("error") if exp_res else "failed to get expeditions")
            expeditions = exp_res.get("data", [])
            expedition_map = {}
            for exp in expeditions:
                name = exp.get("title", {}).get("en", "")
                expedition_map[name] = exp
            upgraded = 0
            expedition_started = 0
            now = datetime.now(UTC)
            claimed_expeditions = 0
            _, user_exp_res = await self._request("GET", "api/expeditions/user-expeditions")
            if not user_exp_res or not user_exp_res.get("success"):
                self.log("❌ Failed to fetch user expeditions.", Fore.RED)
            else:
                user_expeditions = user_exp_res.get("data", [])
                if user_expeditions:
                    self.log(f"📦 Found {len(user_expeditions)} expedition record(s).", Fore.CYAN)
                for expedition in user_expeditions:
                    users_expeditions_id = expedition.get("users_expeditions_id")
                    is_completed = expedition.get("is_complited", False)
                    expedition_name = (
                        expedition.get("title", {}).get("en")
                        or expedition.get("expedition_data", {}).get("title", {}).get("en")
                        or "Unknown Expedition"
                    )
                    if not is_completed:
                        self.log(f"⏳ Expedition still running: {expedition_name}", Fore.YELLOW)
                        continue
                    self.log(f"🎉 Completed expedition detected: {expedition_name}", Fore.GREEN)
                    rewards = expedition.get("recieved_expedition_boxes", [])
                    if rewards:
                        self.log(f"🎁 Rewards received: {len(rewards)}", Fore.MAGENTA)
                    for idx, reward_box in enumerate(rewards, start=1):
                        reward = reward_box.get("reward", {})
                        reward_type = reward.get("type", "unknown")
                        amount = reward.get("amount", 0)
                        item_info = reward.get("item_info", {})
                        reward_name = (
                            item_info.get("title", {}).get("en") or item_info.get("name", {}).get("en") or reward_type
                        )
                        self.log(f"   [{idx}] {reward_type.upper()} → {reward_name} x{amount}", Fore.CYAN)
                    claim_payload = {"users_expeditions_id": users_expeditions_id}
                    _, claim_res = await self._request("POST", "api/expeditions/finish", json_data=claim_payload)
                    if not claim_res or not claim_res.get("success"):
                        self.log(
                            f"❌ Failed claiming expedition: {(claim_res.get('error') if claim_res else 'unknown error')}",
                            Fore.RED,
                        )
                        continue
                    claim_data = claim_res.get("data", {})
                    received_xp = claim_data.get("received_xp_amount", 0)
                    shared_xp = claim_data.get("shared_xp_amount", 0)
                    self.log(
                        f"✅ Expedition claimed successfully! (XP={received_xp} | SharedXP={shared_xp})", Fore.GREEN
                    )
                    claimed_expeditions += 1
                    await asyncio.sleep(random.uniform(1.5, 3.0))
            for pet in pets:
                title = pet.get("title", {}).get("en", "Unknown")
                users_pets_id = pet.get("users_pets_id")
                distribute_points = pet.get("skills_points_to_distribute", 0)
                in_expedition = pet.get("is_in_expedition", False)
                level = pet.get("level", 0)
                next_expedition_date = pet.get("next_expedition_date")
                self.log(
                    f"🐹 {title} | Lv.{level} | Points={distribute_points} | Expedition={in_expedition}", Fore.CYAN
                )
                if not in_expedition and distribute_points >= 3:
                    balanced_points = distribute_points // 3
                    if balanced_points > 0:
                        payload = {
                            "users_pets_id": users_pets_id,
                            "charachteristics": {
                                "strength": balanced_points,
                                "health": balanced_points,
                                "luck": balanced_points,
                            },
                        }
                        self.log(
                            f"🚀 Balanced upgrade for {title} (+{balanced_points} STR / +{balanced_points} HP / +{balanced_points} LUCK)",
                            Fore.GREEN,
                        )
                        _, up_res = await self._request("POST", "api/pets/update-charachteristics", json_data=payload)
                        if up_res and up_res.get("success"):
                            used_points = balanced_points * 3
                            leftover = distribute_points - used_points
                            self.log(f"✅ Upgrade success | Used={used_points} | Leftover={leftover}", Fore.GREEN)
                            upgraded += 1
                            await asyncio.sleep(random.uniform(1.2, 2.4))
                        else:
                            self.log(
                                f"❌ Upgrade failed for {title}: {(up_res.get('error') if up_res else 'unknown error')}",
                                Fore.RED,
                            )
                if in_expedition:
                    self.log(f"⏭️ {title} is already in expedition.", Fore.YELLOW)
                    continue
                if not next_expedition_date:
                    self.log(f"⏭️ {title} has no expedition cooldown info.", Fore.YELLOW)
                    continue
                try:
                    expedition_time = datetime.fromisoformat(next_expedition_date.replace("Z", "+00:00"))
                except Exception:
                    self.log(f"❌ Invalid expedition date for {title}", Fore.RED)
                    continue
                if expedition_time > now:
                    remain = expedition_time - now
                    self.log(f"⏳ {title} expedition cooldown active ({remain})", Fore.YELLOW)
                    continue
                selected_name = None
                if level <= 15:
                    selected_name = "Deep Forest"
                elif 15 < level <= 35:
                    selected_name = "Tousland"
                elif level > 35:
                    selected_name = "Snowlit Avenue"
                expedition = expedition_map.get(selected_name)
                if not expedition:
                    self.log(f"❌ Expedition '{selected_name}' not found.", Fore.RED)
                    continue
                expedition_id = expedition.get("id")
                self.log(f"🗺️ Selected expedition for {title}: {selected_name}", Fore.MAGENTA)
                start_payload = {
                    "expeditions_id": expedition_id,
                    "users_pets_ids": [users_pets_id],
                    "used_abilities_codes": [],
                }
                _, start_res = await self._request("POST", "api/expeditions/start", json_data=start_payload)
                if not start_res or not start_res.get("success"):
                    self.log(
                        f"❌ Failed starting expedition for {title}: {(start_res.get('error') if start_res else 'unknown error')}",
                        Fore.RED,
                    )
                    continue
                self.log(f"✅ Expedition started for {title} → {selected_name}", Fore.GREEN)
                expedition_started += 1
                await asyncio.sleep(random.uniform(2.0, 4.0))
            self.log(f"🏁 Hamster phase completed | Upgraded={upgraded} | Expeditions={expedition_started}", Fore.GREEN)
            return True
        except Exception as e:
            self.log(f"❌ Hamster process failed: {e}", Fore.RED)
            return False

    @wrapper_feature
    async def task(self) -> bool:
        self.log("📋 Phase: tasks → auto-claim (daily + major)", Fore.GREEN)
        if not getattr(self, "access_token", None) or not getattr(self, "csrf_token", None):
            self.log("❌ Token or CSRF not initialized. Login first.", Fore.RED)
            return False
        try:
            claimed_any = False
            for task_type in ["daily", "major"]:
                self.log(f"🔍 Fetching {task_type} tasks...", Fore.BLUE)
                _, res = await self._request("GET", f"api/quests/tasks?type={task_type}")
                if not res or not res.get("success"):
                    self.log(f"❌ Failed to fetch {task_type}: {res}", Fore.RED)
                    continue
                data = res.get("data", {})
                tasks = data.get("tasks", [])
                if not tasks:
                    self.log(f"ℹ️ No {task_type} tasks found.", Fore.YELLOW)
                    continue
                for task in tasks:
                    task_id = task.get("id")
                    title = task.get("title", {}).get("en", "Unknown Task")
                    progress = task.get("progress", 0)
                    repeats = task.get("count_repeats", 0)
                    is_claimed = task.get("is_claimed", False)
                    task_kind = task.get("type")
                    self.log(f"🧩 [{task_type}] {title} | {progress}/{repeats} | Claimed: {is_claimed}", Fore.CYAN)
                    if is_claimed:
                        self.log("↪️ Already claimed. Skip.", Fore.YELLOW)
                        continue
                    if task_type == "major" and task_kind != "games":
                        self.log("⛔ Not a games task. Skip.", Fore.YELLOW)
                        continue
                    if progress < repeats:
                        self.log("⏳ Not completed yet. Skip.", Fore.YELLOW)
                        continue
                    self.log(f"🎯 Claiming {task_type} task {task_id} ...", Fore.YELLOW)
                    _, cres = await self._request(
                        "POST", "api/quests/collect-tasks", json_data={"task_id": task_id, "type": task_type}
                    )
                    if not cres or not cres.get("success"):
                        self.log(f"❌ Failed to claim {task_id}: {cres}", Fore.RED)
                        continue
                    self.log("✅ Task claimed successfully!", Fore.GREEN)
                    claimed_any = True
            if not claimed_any:
                self.log("ℹ️ No completed tasks to claim.", Fore.YELLOW)
            return True
        except Exception as e:
            self.log(f"❌ Task process failed: {e}", Fore.RED)
            return False

    @wrapper_feature
    async def achievements(self) -> bool:
        self.log("🏆 Phase: achievements → scan & claim", Fore.GREEN)
        if not getattr(self, "access_token", None) or not getattr(self, "csrf_token", None):
            self.log("❌ Token or CSRF not initialized. Login first.", Fore.RED)
            return False
        try:
            _, res = await self._request("GET", "api/main/achievements/tasks-progress")
            if not res or not res.get("success"):
                raise ValueError(res.get("error") if res else "empty response")
            data = res.get("data", {})
            if not data:
                self.log("ℹ️ No achievement data found.", Fore.YELLOW)
                return True
            claimable_ids = []
            for category_name, items in data.items():
                if not isinstance(items, list):
                    continue
                for item in items:
                    if item.get("is_completed") is True and item.get("is_claimed") is False:
                        claimable_ids.append(
                            {"id": item.get("id"), "type": item.get("type"), "category": category_name}
                        )
            if not claimable_ids:
                self.log("✅ No claimable achievements found.", Fore.GREEN)
                return True
            self.log(f"🎯 Found {len(claimable_ids)} claimable achievements", Fore.CYAN)
            for ach in claimable_ids:
                self.log(f"🚀 Claiming [{ach['category']}] → {ach['type']}", Fore.YELLOW)
                _, claim_res = await self._request("POST", "api/main/achievements/claim", json_data={"id": ach["id"]})
                if not claim_res or not claim_res.get("success"):
                    self.log(
                        f"❌ Failed to claim {ach['type']} | {(claim_res.get('error') if claim_res else 'no response')}",
                        Fore.RED,
                    )
                    continue
                self.log(f"✅ Claimed → {ach['type']}", Fore.GREEN)
            self.log("🏁 Achievement phase completed.", Fore.GREEN)
            return True
        except Exception as e:
            self.log(f"❌ Achievement phase failed: {e}", Fore.RED)
            return False

    async def generate_constructed(self, uid: str) -> str:
        digits = [int(c) for c in uid if c.isdigit()]
        s = sum(digits)
        n = sorted(digits)
        uid_prefix = list(uid[: len(n)])
        constructed = "".join(map(str, n + uid_prefix + [s]))
        return constructed

    async def encrypt_data(self, plaintext: str, uid: str, iv: bytes = b"dYQ9R99bkKLsLHad") -> str:
        constructed = await self.generate_constructed(uid)
        key_md5_hex = hashlib.md5(constructed.encode()).hexdigest()
        key = key_md5_hex.encode("utf-8")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
        return base64.b64encode(encrypted).decode("utf-8")

    GAME_NAMES = {
        12: "Hamster Climber",
        13: "Coin Fisher",
        3: "Flappy Rocket",
        14: "Mission Hampossible",
        6: "Crypto Hamster",
        7: "2048 Coin",
        5: "Coin Match",
        10: "Token Surfer: Snow Ride",
        2: "Token Blaster",
        15: "Crypto Hex",
        1: "Coin Click",
        9: "Dr. Hamster",
        4: "Cryptonoid",
        8: "Coin Flip",
        11: "Lambo Rider",
    }

    async def get_game_name(self, num) -> str:
        if num is None:
            return "Unknown Game"
        try:
            n = int(num)
        except Exception:
            return "Unknown Game"
        return self.GAME_NAMES.get(n, f"Game #{n}")

    REWARD_TABLE = {
        1: {1: 1200, 2: 1200, 3: 1200, 4: 1200, 5: 1440, 6: 1440, 7: 1440, 8: 1440, 9: 1680, 10: 1680},
        2: {1: 6552, 2: 7224, 3: 7722, 4: 8400, 5: 8961, 6: 9540, 7: 10062, 8: 10647, 9: 11232, 10: 14040},
        3: {1: 2376, 2: 2592, 3: 2730, 4: 2940, 5: 3150, 6: 3360, 7: 3570, 8: 3780, 9: 3990, 10: 4200},
        4: {1: 6768, 2: 6912, 3: 7200, 4: 7488, 5: 7632, 6: 7920, 7: 10944, 8: 11136, 9: 11520, 10: 11712},
        5: {1: 2160, 2: 2196, 3: 2232, 4: 2646, 5: 2688, 6: 2730, 7: 2772, 8: 2814, 9: 2856, 10: 3126},
        6: {1: 6090, 2: 6492, 3: 6906, 4: 7332, 5: 7770, 6: 8226, 7: 8688, 8: 9168, 9: 9654, 10: 10152},
        7: {1: 1008, 2: 1071, 3: 1134, 4: 1197, 5: 1260, 6: 1323, 7: 1386, 8: 1449, 9: 1512, 10: 1575},
        8: {1: 1152, 2: 1152, 3: 1152, 4: 1536, 5: 1608, 6: 1608, 7: 1608, 8: 2010, 9: 2010, 10: 2010},
        9: {1: 3012, 2: 3294, 3: 3558, 4: 3804, 5: 4026, 6: 4230, 7: 4410, 8: 4584, 9: 4734, 10: 4866},
        10: {1: 3528, 2: 3822, 3: 4116, 4: 4410, 5: 4704, 6: 4998, 7: 5292, 8: 5586, 9: 5880, 10: 6174},
        11: {1: 6528, 2: 6975, 3: 7425, 4: 7872, 5: 8319, 6: 8769, 7: 9216, 8: 9663, 9: 10113, 10: 10560},
        12: {1: 2550, 2: 2970, 3: 3330, 4: 3720, 5: 4080, 6: 4470, 7: 4860, 8: 5250, 9: 5640, 10: 6000},
        13: {1: 2550, 2: 2970, 3: 3330, 4: 3720, 5: 4080, 6: 4470, 7: 4860, 8: 5250, 9: 5640, 10: 6000},
        14: {1: 7000, 2: 8000, 3: 9000, 4: 10000, 5: 11000, 6: 12000, 7: 13000, 8: 14000, 9: 15000, 10: 16000},
        15: {1: 2550, 2: 2970, 3: 3330, 4: 3720, 5: 4080, 6: 4470, 7: 4860, 8: 5250, 9: 5640, 10: 6000},
    }
    TIME_TABLE = {
        13: {1: 40, 2: 35, 3: 35, 4: 30, 5: 25, 6: 25, 7: 25, 8: 25, 9: 25, 10: 25},
        14: {1: 45, 2: 45, 3: 40, 4: 40, 5: 35, 6: 35, 7: 30, 8: 30, 9: 25, 10: 25},
        15: {1: 30, 2: 34, 3: 38, 4: 42, 5: 46, 6: 50, 7: 54, 8: 58, 9: 62, 10: 70},
    }

    async def get_reward(self, game_number: int, level: int) -> int:
        try:
            return self.REWARD_TABLE[game_number][level]
        except KeyError:
            self.log(f"⚠️ rewardTable missing game={game_number} level={level}", Fore.YELLOW)
            return 0

    async def get_time_sec(self, game_number: int, level: int) -> int:
        try:
            return self.TIME_TABLE[game_number][level]
        except KeyError:
            self.log(f"⚠️ timeTable missing game={game_number} level={level}, fallback 60s", Fore.YELLOW)
            return 60

    def decode_event_data(self, b64: str) -> dict:
        raw = base64.b64decode(b64)
        return json.loads(raw.decode("utf-8"))

    async def get_event_max_level(self) -> int | None:
        _, res = await self._request("GET", "api/progression-event/progression-tasks")
        tasks = res.get("data", [])
        if not any(t.get("type") == "game_level" for t in tasks):
            self.log("🟡 No game_level task → non-event mode", Fore.YELLOW)
            return None
        _, res = await self._request("GET", "api/progression-event/progression-event")
        if not res.get("success") or not res.get("data"):
            return None
        decoded = self.decode_event_data(res["data"])
        event = decoded.get("event", {})
        end_date = event.get("end_date")
        if end_date:
            end_ts = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            if datetime.now(UTC) > end_ts:
                self.log("⏰ Event expired → fallback non-event", Fore.YELLOW)
                return None
        return int(event.get("max_level", 0)) or None

    async def get_event_end_ts(self) -> float | None:
        _, res = await self._request("GET", "api/progression-event/progression-event")
        if not res.get("success") or not res.get("data"):
            return None
        decoded = self.decode_event_data(res["data"])
        event = decoded.get("event", {})
        end_date = event.get("end_date")
        if not end_date:
            return None
        end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        return end_dt.timestamp()

    async def get_active_events(self) -> dict:
        _, res = await self._request("GET", "api/events/events-count")
        if not res.get("success"):
            return {}
        return res.get("data", {}) or {}

    async def has_unfinished_puzzle_games(self):
        _, res = await self._request("GET", "api/events/spin-event/tasks-list")
        if not res.get("success"):
            return False
        for task in res["data"].get("tasks", []):
            if task.get("type") == "games":
                if not task.get("is_claimed") and task.get("progress", 0) < task.get("count_repeats", 0):
                    return True
        return False

    async def check_and_claim_puzzle_tasks(self):
        self.log("🧩 Checking puzzle event tasks…", Fore.CYAN)
        _, res = await self._request("GET", "api/events/spin-event/tasks-list")
        if not res.get("success"):
            self.log("❌ Failed to fetch puzzle tasks", Fore.RED)
            return
        data = res.get("data", {})
        tasks = data.get("tasks", [])
        if not tasks:
            self.log("ℹ️ No puzzle tasks found", Fore.YELLOW)
            return
        for task in tasks:
            if task.get("type") != "games":
                continue
            task_id = task.get("id")
            progress = task.get("progress", 0)
            repeats = task.get("count_repeats", 0)
            claimed = task.get("is_claimed", False)
            title = task.get("title", {}).get("en", "Unknown")
            self.log(f"🎮 Puzzle Task: {title} | {progress}/{repeats} | Claimed: {claimed}", Fore.MAGENTA)
            if claimed:
                continue
            if progress < repeats:
                continue
            self.log(f"🎯 Claiming puzzle task {task_id}", Fore.YELLOW)
            _, cres = await self._request("POST", "api/events/spin-event/claim-task", json_data={"task_id": task_id})
            if cres.get("success"):
                self.log("✅ Puzzle task claimed!", Fore.GREEN)
                await asyncio.sleep(1)
            else:
                self.log(f"❌ Claim failed: {cres.get('error')}", Fore.RED)

    async def should_continue_event_grind(self) -> bool:
        events = await self.get_active_events()
        if events.get("puzzle_event") == 1:
            if await self.has_unfinished_puzzle_games():
                return True
        max_level = await self.get_event_max_level()
        if max_level is not None:
            return True
        return False

    @wrapper_feature
    async def game(self):
        self.log("🎮 Main game flow started (time-based loop)", Fore.CYAN)
        exit_reason = None
        MAX_LEVEL = int(self.config.get("max_level_game", 10))
        MODE = (self.config.get("mode_game") or "win").lower()
        RUNNING_MODE = (self.config.get("mode_game_running") or "non_event").lower()
        event_end = await self.get_event_end_ts()
        if RUNNING_MODE == "event":
            events = await self.get_active_events()
            puzzle_on = events.get("puzzle_event") == 1
            max_level = await self.get_event_max_level()
            progress_flag = max_level is not None
            progress_on = False
            puzzle_unfinished = False
            if puzzle_on:
                self.log("🧩 Puzzle event detected → checking tasks", Fore.CYAN)
                try:
                    await self.check_and_claim_puzzle_tasks()
                except Exception as e:
                    self.log(f"⚠️ Puzzle pre-check failed: {e}", Fore.YELLOW)
                try:
                    puzzle_unfinished = await self.has_unfinished_puzzle_games()
                except Exception as e:
                    self.log(f"⚠️ Puzzle check failed: {e}", Fore.YELLOW)
                event_alive = event_end and time.time() < event_end
                if puzzle_unfinished:
                    self.log("🔥 Puzzle unfinished → TASK MODE", Fore.GREEN)
                    progress_on = True
                elif progress_flag:
                    if event_alive:
                        self.log("📈 Progress event active", Fore.CYAN)
                        progress_on = True
                    else:
                        self.log("⏰ Progress event expired", Fore.YELLOW)
                else:
                    self.log("🟡 No active event → fallback NON-EVENT", Fore.YELLOW)
            if not progress_on and progress_flag:
                self.log(f"📈 Progress event active (max_level={max_level})", Fore.GREEN)
                progress_on = True
            if not progress_on:
                self.log("🟡 No active event → fallback NON-EVENT (LOSE MODE)", Fore.YELLOW)
                RUNNING_MODE = "non_event"
                MODE = "win"
                hours = float(self.config.get("time_game", 1))
                end_time = time.time() + hours * 3600
                self.log(f"⏱️ NON-EVENT (LOSE) → running for {hours} hour(s)", Fore.GREEN)
            else:
                max_event_runtime = 12 * 3600
                event_cap = time.time() + max_event_runtime
                if puzzle_unfinished:
                    self.log("🧩 Puzzle mode → runtime capped (max 12h if tasks remain)", Fore.CYAN)
                    end_time = event_cap
                elif progress_flag:
                    if event_end and time.time() > event_end:
                        self.log("🟡 Progress event expired → fallback non-event", Fore.YELLOW)
                        RUNNING_MODE = "non_event"
                        MODE = "lose"
                        hours = float(self.config.get("time_game", 1))
                        end_time = time.time() + hours * 3600
                    elif not event_end:
                        self.log("⚠️ Progress event end unknown → safe cap 12h", Fore.YELLOW)
                        end_time = event_cap
                    else:
                        end_time = min(event_end, event_cap)
                else:
                    self.log("🟡 No active event → fallback NON-EVENT", Fore.YELLOW)
                    RUNNING_MODE = "non_event"
                    MODE = "lose"
                    hours = float(self.config.get("time_game", 1))
                    end_time = time.time() + hours * 3600
                self.log(f"🔥 EVENT MODE → running until {datetime.fromtimestamp(end_time)}", Fore.GREEN)
        else:
            hours = float(self.config.get("time_game", 1))
            end_time = time.time() + hours * 3600
            self.log(f"⏱️ NON-EVENT → running for {hours} hour(s)", Fore.GREEN)

        # ========== VARIABEL UNTUK MELACAK KEMENANGAN PER GAME ==========
        game_wins = {}  # {game_number: wins_count}
        all_games_done = False  # Flag untuk menandai semua game sudah 15 win
        total_games_with_15_wins = 0
        total_unique_games = 15  # Jumlah total game yang tersedia (1-15)
        last_game_number = None  # Untuk tracking game terakhir

        while True:
            # Cek apakah waktu sudah habis
            if time.time() >= end_time:
                if RUNNING_MODE == "event":
                    self.log("⏹️ Event runtime limit reached (12h cap)", Fore.CYAN)
                else:
                    self.log("⏹️ Non-event time limit reached", Fore.CYAN)
                break

            # ========== CEK APAKAH SEMUA GAME SUDAH 15 WIN ==========
            if not all_games_done:
                # Hitung berapa game yang sudah mencapai 15 win
                games_with_15 = sum(1 for wins in game_wins.values() if wins >= 15)
                
                if games_with_15 >= total_unique_games:
                    all_games_done = True
                    self.log(f"🎉 SEMUA {total_unique_games} GAME SUDAH MENCAPAI 15 KEMENANGAN!", Fore.GREEN)
                    self.log("🔄 Melanjutkan sisa waktu sampai semua game level 10...", Fore.CYAN)
                else:
                    self.log(f"📊 Progress: {games_with_15}/{total_unique_games} game sudah 15 win", Fore.CYAN)

            ws = None
            user_id = None
            try:
                await self.refresh_token_flow(refresh_token=self.refresh_token, identity=self.csrf_token)
                ws_url = f"wss://ws.rollercoin.com/cmd?token={self.access_token}"
                ws = await self.ws_connect(ws_url)
                timeout_count = 0
                MAX_TIMEOUT = 3
                if ws and ws.is_open:
                    await self.ws_send(ws, json.dumps({"cmd": "profile_data"}))
                while ws and ws.is_open:
                    raw = await self.ws_recv(ws, timeout=random.randint(50, 65))
                    if raw == "TIMEOUT":
                        timeout_count += 1
                        self.log(f"⌛ WS timeout ({timeout_count}/{MAX_TIMEOUT})", Fore.YELLOW)
                        if timeout_count >= MAX_TIMEOUT:
                            self.log("🔁 Too many timeouts → reconnect", Fore.CYAN)
                            await self.refresh_token_flow(refresh_token=self.refresh_token, identity=self.csrf_token)
                            break
                        continue
                    if raw in ("CLOSED", "ERROR"):
                        self.log("💥 WS dead → reconnecting", Fore.RED)
                        break
                    if not raw:
                        continue
                    timeout_count = 0
                    try:
                        msg = json.loads(raw)
                    except Exception:
                        self.log("⚠️ Invalid WS payload → skip", Fore.YELLOW)
                        continue
                    cmd = msg.get("cmd")
                    if cmd == "profile":
                        user_id = msg["cmdval"]["userid"]
                        if ws and ws.is_open:
                            await self.ws_send(ws, json.dumps({"cmd": "games_data_request"}))
                    elif cmd == "games_data_response":
                        games = msg.get("cmdval", [])
                        
                        # Filter game yang levelnya <= MAX_LEVEL dan cooldown 0
                        available = [
                            g for g in games
                            if int(g.get("level", {}).get("level", 0)) <= MAX_LEVEL and g.get("cool_down") == 0
                        ]
                        
                        if not available:
                            sleep_sec = random.randint(300, 420)
                            self.log(f"😴 No games available → closing ws & sleeping {sleep_sec // 60}m", Fore.MAGENTA)
                            await self.ws_close(ws)
                            await asyncio.sleep(sleep_sec)
                            break

                        # ========== PILIH GAME BERDASARKAN LOGIKA BARU ==========
                        chosen = None
                        
                        if not all_games_done:
                            # FASE 1: Prioritaskan game yang belum mencapai 15 win
                            # Cari game yang tersedia dan belum mencapai 15 win
                            candidates = []
                            for g in available:
                                game_num = g["game_number"]
                                current_wins = game_wins.get(game_num, 0)
                                if current_wins < 15:
                                    candidates.append((g, current_wins))
                            
                            if candidates:
                                # Urutkan dari yang paling sedikit kemenangannya
                                candidates.sort(key=lambda x: x[1])
                                # Pilih yang paling sedikit kemenangannya (untuk meratakan)
                                chosen = candidates[0][0]
                                game_num = chosen["game_number"]
                                last_game_number = game_num
                                self.log(f"🎯 Memilih game {await self.get_game_name(game_num)} (wins: {game_wins.get(game_num, 0)}/15)", Fore.CYAN)
                            else:
                                # Semua game sudah 15 win, lanjut ke fase 2
                                all_games_done = True
                                self.log(f"🎉 SEMUA GAME SUDAH 15 WIN! Melanjutkan ke level 10...", Fore.GREEN)
                        
                        if all_games_done:
                            # FASE 2: Semua game sudah 15 win, mainkan semua game sampai level 10
                            # Pilih game dengan level terendah yang tersedia
                            candidates = []
                            for g in available:
                                level = int(g.get("level", {}).get("level", 0))
                                if level < MAX_LEVEL:
                                    candidates.append((g, level))
                            
                            if candidates:
                                # Urutkan dari level terendah
                                candidates.sort(key=lambda x: x[1])
                                chosen = candidates[0][0]
                                game_num = chosen["game_number"]
                                last_game_number = game_num
                                level = candidates[0][1]
                                self.log(f"🎯 Fase Leveling: {await self.get_game_name(game_num)} (level {level} → target {MAX_LEVEL})", Fore.CYAN)
                            else:
                                # Semua game sudah level MAX_LEVEL
                                self.log(f"✅ SEMUA GAME SUDAH LEVEL {MAX_LEVEL}! Selesai.", Fore.GREEN)
                                exit_reason = "all-max-level"
                                await self.ws_close(ws)
                                return exit_reason
                        
                        # Jika tidak ada game yang dipilih (should not happen), pilih random
                        if chosen is None:
                            chosen = random.choice(available)
                            last_game_number = chosen["game_number"]
                        
                        game_number = chosen["game_number"]
                        level = chosen["level"]["level"]
                        self.log(f"🎯 Picked {await self.get_game_name(game_number)} (lvl {level})", Fore.GREEN)
                        
                        enc = await self.encrypt_data(json.dumps({"game_number": game_number}), user_id)
                        _, body = await self._request(
                            "POST", f"api/game/encode-start-game-data/{user_id}", json_data={"data": enc}
                        )
                        if ws and ws.is_open:
                            await self.ws_send(ws, json.dumps({"cmd": "game_start_request", "cmdval": body["data"]}))
                    elif cmd == "game_start_response":
                        info = msg["cmdval"]
                        reward = await self.get_reward(info["game_number"], info["level"]["level"])
                        base = await self.get_time_sec(info["game_number"], info["level"]["level"])
                        play_sec = max(1, base - random.randint(2, 5))
                        self.log(f"🎮 Playing for {play_sec}s...", Fore.BLUE)
                        await asyncio.sleep(play_sec)
                        
                        # Tentukan apakah menang atau kalah
                        game_num = info["game_number"]
                        last_game_number = game_num
                        current_wins = game_wins.get(game_num, 0)
                        
                        # Jika game ini belum mencapai 15 win, mainkan untuk MENANG
                        if current_wins < 15:
                            win_status = 3  # WIN
                            power = reward
                            self.log(f"🏆 TARGET WIN #{current_wins + 1}/15 untuk game ini!", Fore.GREEN)
                        else:
                            # Game sudah 15 win, mainkan untuk KALAH (agar tidak membuang waktu)
                            win_status = 2  # LOSE
                            power = 0
                            self.log(f"💤 Game sudah 15 win → main KALAH (fase leveling)", Fore.MAGENTA)
                        
                        end_obj = {
                            "power": power,
                            "time": int(time.time() * 1000),
                            "user_game_id": info["user_game_id"],
                            "win_status": win_status,
                        }
                        enc_end = await self.encrypt_data(json.dumps(end_obj), user_id)
                        _, body = await self._request(
                            "POST", f"api/game/encode-data/{user_id}", json_data={"data": enc_end}
                        )
                        if not ws or not ws.is_open:
                            self.log("⚠️ WS closed before game_end_request → restarting round", Fore.YELLOW)
                            break
                        if ws and ws.is_open:
                            await self.ws_send(ws, json.dumps({"cmd": "game_end_request", "cmdval": body["data"]}))
                            self.log(
                                f"📤 Sending game_end_request → power={end_obj['power']} | status={end_obj['win_status']} ({'WIN' if win_status == 3 else 'LOSE'})",
                                Fore.BLUE,
                            )
                        else:
                            self.log("❌ Failed to send game_end_request (ws dead)", Fore.RED)
                    elif cmd == "game_finished_accepted":
                        # ========== UPDATE COUNTER KEMENANGAN ==========
                        # Update counter untuk game yang baru selesai (berdasarkan last_game_number)
                        if last_game_number is not None:
                            # Cek apakah game tersebut menang (berdasarkan mode dan status)
                            # Kita update hanya jika game tersebut belum mencapai 15 win
                            current_wins = game_wins.get(last_game_number, 0)
                            if current_wins < 15:
                                # Tambah 1 kemenangan (karena kita selalu bermain untuk menang di fase 1)
                                game_wins[last_game_number] = current_wins + 1
                                self.log(f"✅ {await self.get_game_name(last_game_number)} → {game_wins[last_game_number]}/15 wins!", Fore.GREEN)
                        
                        self.log(f"🏁 Game finished → MODE: {MODE.upper()}", Fore.GREEN if MODE == "win" else Fore.MAGENTA)
                        
                        if RUNNING_MODE == "event":
                            try:
                                await self.check_and_claim_puzzle_tasks()
                                continue_grind = False
                                try:
                                    continue_grind = await self.should_continue_event_grind()
                                except Exception as e:
                                    self.log(f"⚠️ Event check failed → assume continue: {e}", Fore.YELLOW)
                                    continue_grind = True
                                if continue_grind:
                                    self.log("🔥 Event still active → continue grinding", Fore.GREEN)
                                    break
                                self.log("✅ All event objectives completed", Fore.CYAN)
                                exit_reason = "event-finished"
                                return exit_reason
                            except Exception as e:
                                self.log(f"⚠️ Event handling failed: {e}", Fore.YELLOW)
                        break
            except Exception as e:
                self.log(f"⚠️ Game round error (ignored): {e}", Fore.YELLOW)
            finally:
                if ws:
                    await self.ws_close(ws)
            await asyncio.sleep(random.randint(3, 7))
        
        self.log("⏹️ Game loop finished (time limit reached)", Fore.CYAN)
        return exit_reason

    @wrapper_feature
    async def token_mining(self):
        self.log("⛏️ Phase: token-mining decision", Fore.GREEN)
        MODE = (self.config.get("mode_mining") or "profit").lower()
        try:
            _, res = await self._request("GET", "api/profile/user-profile-data")
            if not res or not res.get("success"):
                raise ValueError("failed get profile")
            data = res["data"]
            user_id = data["id"]
            league_id = data["leagues_ids"][0]
            last_update = data.get("last_update_mining_settings_time")
            self.log(f"🧬 User: {user_id} | League: {league_id}", Fore.CYAN)
            if last_update:
                try:
                    last_dt = datetime.fromisoformat(last_update.replace("Z", "+00:00"))
                    now = datetime.now(UTC)
                    diff_hours = (now - last_dt).total_seconds() / 3600
                    if diff_hours < 12:
                        self.log(f"⏳ Cooldown active ({diff_hours:.2f}h < 12h) → skip", Fore.YELLOW)
                        return True
                except Exception as e:
                    self.log(f"⚠️ Failed parse cooldown: {e}", Fore.YELLOW)
            _, res = await self._request("GET", "api/league/user-settings", params={"league_id": league_id})
            if not res or not res.get("success"):
                raise ValueError("failed get settings")
            currencies = res.get("data", [])
            valid_currencies = [c["currency"] for c in currencies]
            current_map = {c["currency"]: c.get("percent", 0) for c in currencies}
            results = {}
            for cur in valid_currencies:
                _, pres = await self._request(
                    "GET", "api/league/power-info", params={"league_id": league_id, "currency": cur}
                )
                if not pres or not pres.get("success"):
                    self.log(f"⚠️ skip {cur} (no data)", Fore.YELLOW)
                    continue
                pdata = pres["data"]
                total_power = pdata.get("total_block_power", 0)
                payout = pdata.get("block_payout", 0)
                if total_power <= 0 or payout <= 0:
                    continue
                score = payout / total_power
                results[cur] = score
                self.log(f"📊 {cur} → payout={payout} | net={total_power} | score={score:.12f}", Fore.BLUE)
            if not results:
                self.log("❌ No valid mining candidates", Fore.RED)
                return False
            if MODE == "progress":
                target = "RLT" if "RLT" in valid_currencies else "RST"
                self.log(f"🎯 Progress mode → {target}", Fore.YELLOW)
            else:
                target = max(results.items(), key=lambda x: x[1])[0]
                self.log(f"💰 Profit mode → {target}", Fore.GREEN)
            already_correct = current_map.get(target, 0) == 100 and all(
                current_map.get(c, 0) == (100 if c == target else 0) for c in valid_currencies
            )
            if already_correct:
                self.log(f"😴 Already optimal ({target} 100%) → skip", Fore.YELLOW)
                return True
            settings_payload = [
                {"currency": cur, "percent": 100 if cur == target else 0, "league_id": league_id}
                for cur in valid_currencies
            ]
            _, ures = await self._request(
                "POST", "api/league/update-settings", json_data={"settings": settings_payload}
            )
            if not ures or not ures.get("success"):
                raise ValueError(ures.get("error") if ures else "update failed")
            self.log(f"✅ Mining updated → {target}", Fore.GREEN)
            return True
        except Exception as e:
            self.log(f"❌ token_mining failed: {e}", Fore.RED)
            return False

    async def get_full_inventory(self, item_type):
        self.log(f"📦 Fetching FULL inventory: {item_type}", Fore.GREEN)
        all_items = []
        skip = 0
        limit = 24
        while True:
            url = f"api/game/inventory?itemType={item_type}&type={item_type}&skip={skip}&limit={limit}"
            _, res = await self._request("GET", url)
            if not res or not res.get("success"):
                self.log("❌ Failed fetch inventory", Fore.RED)
                break
            data = res.get("data", {})
            items = data.get("items", [])
            if not items:
                self.log("📭 No more items", Fore.YELLOW)
                break
            all_items.extend(items)
            self.log(f"   ➕ Got {len(items)} items (total {len(all_items)})", Fore.CYAN)
            if len(items) < limit:
                self.log("✅ Reached last page", Fore.GREEN)
                break
            skip += limit
            await asyncio.sleep(0.2)
        self.log(f"📦 TOTAL {item_type}: {len(all_items)}", Fore.MAGENTA)
        return all_items

    @wrapper_feature
    async def layout(self):
        self.log("🏗️ Phase: Layout Analyzer", Fore.GREEN)
        try:

            def calc_miner_score(account_power, account_bonus, miner):
                miner_power = miner.get("power", 0)
                miner_bonus = miner.get("bonus_percent", 0) / 10000
                delta = miner_power * (1 + account_bonus + miner_bonus) + account_power * miner_bonus
                return delta

            _, res = await self._request("GET", "api/profile/user-profile-data")
            if not res or not res.get("success"):
                raise ValueError("failed get profile")
            user_id = res["data"]["id"]
            self.log(f"🧬 User ID: {user_id}", Fore.CYAN)
            _, res = await self._request("GET", f"api/game/room-config/{user_id}")
            if not res or not res.get("success"):
                raise ValueError("failed get room config")
            data = res["data"]
            rooms = data.get("rooms_available", [])
            racks = data.get("racks", [])
            miners = data.get("miners", [])
            racks_by_room = defaultdict(list)
            racks = sorted(racks, key=lambda r: r.get("bonus", 0), reverse=True)
            for r in racks:
                racks_by_room[r["placement"]["user_room_id"]].append(r)
            miners_by_rack = defaultdict(list)
            for m in miners:
                miners_by_rack[m["placement"]["user_rack_id"]].append(m)
            total_empty_room_slots = 0
            total_empty_rack_slots = 0
            for room in rooms:
                if room["room_info"]["level"] == -1:
                    continue
                cols = room["room_info"]["cols"] // 2
                rows = room["room_info"]["rows"]
                all_slots = {(x, y) for x in range(cols) for y in range(rows)}
                used_slots = {(r["placement"]["x"], r["placement"]["y"]) for r in racks_by_room.get(room["_id"], [])}
                total_empty_room_slots += len(all_slots - used_slots)
            room_index_map = {room["_id"]: i for i, room in enumerate(rooms, start=1)}
            for rack in racks:
                rack_cols = rack.get("rack_info", {}).get("width", 1)
                rack_rows = rack.get("rack_info", {}).get("height", 1)
                all_slots = {(x, y) for x in range(rack_cols) for y in range(rack_rows)}
                used = set()
                for m in miners_by_rack.get(rack["_id"], []):
                    mx, my = (m["placement"]["x"], m["placement"]["y"])
                    mw = m.get("width", 1)
                    for dx in range(mw):
                        if mx + dx < rack_cols:
                            used.add((mx + dx, my))
                total_empty_rack_slots += len(all_slots - used)
            rack_inventory = await self.get_full_inventory("rack")
            miner_inventory = await self.get_full_inventory("miner")
            has_miner_inventory = any(m.get("quantity", 0) > 0 for m in miner_inventory)
            has_rack_inventory = any(r.get("quantity", 0) > 0 for r in rack_inventory)
            _, power_res = await self._request("GET", "api/profile/user-power-data")
            power_data = power_res["data"]
            account_power = power_data.get("current_power", 0)
            account_bonus = power_data.get("bonus_percent", 0) / 10000
            miner_inventory = sorted(
                miner_inventory, key=lambda m: calc_miner_score(account_power, account_bonus, m), reverse=True
            )
            for m in miner_inventory:
                score = calc_miner_score(account_power, account_bonus, m)
                self.log(
                    f"🧠 {m['name']} | Power={m['power']} | Bonus={m['bonus_percent'] / 100}% | Score={score:,.2f}",
                    Fore.MAGENTA,
                )
            total_miner_qty = sum(m.get("quantity", 0) for m in miner_inventory)
            if total_miner_qty <= 0 and len(miners) == 0:
                self.log("😴 No miners in inventory → skip layout", Fore.BLUE)
                return True
            self.log(f"📦 Empty Room Slots: {total_empty_room_slots}", Fore.YELLOW)
            self.log(f"📭 Empty Rack Slots: {total_empty_rack_slots}", Fore.YELLOW)
            installed_racks = sorted(racks, key=lambda r: r.get("bonus", 0))
            best_inventory_rack = max(
                [r for r in rack_inventory if r.get("quantity", 0) > 0], key=lambda r: r.get("bonus", 0), default=None
            )
            need_rack_evolution = False
            if installed_racks and best_inventory_rack:
                weakest_installed = installed_racks[0]
                if best_inventory_rack.get("bonus", 0) > weakest_installed.get("bonus", 0):
                    need_rack_evolution = True
                    self.log(
                        f"🧱 Better rack found! [{best_inventory_rack['name']}] > [{weakest_installed['name']}]",
                        Fore.MAGENTA,
                    )
            installed_miners = sorted(
                miners, key=lambda m: calc_miner_score(account_power, account_bonus, m), reverse=True
            )
            inventory_miners = [m for m in miner_inventory if m.get("quantity", 0) > 0]
            inventory_miners = sorted(
                inventory_miners, key=lambda m: calc_miner_score(account_power, account_bonus, m), reverse=True
            )
            need_miner_evolution = False
            if installed_miners and inventory_miners:
                installed_scores = sorted(
                    [calc_miner_score(account_power, account_bonus, m) for m in miners], reverse=True
                )
                inventory_scores = []
                for m in miner_inventory:
                    if m.get("quantity", 0) <= 0:
                        continue
                    score = calc_miner_score(account_power, account_bonus, m)
                    inventory_scores.extend([score] * m["quantity"])
                need_miner_evolution = False
                if installed_scores:
                    slot_count = len(installed_scores)
                    inventory_scores = sorted(inventory_scores, reverse=True)[:slot_count]
                    current_total = sum(installed_scores)
                    candidate_total = sum(inventory_scores)
                    gain = candidate_total - current_total
                    if gain > 0:
                        need_miner_evolution = True
                        self.log(f"🧠 Evolution gain +{gain:,.0f}", Fore.MAGENTA)
                    else:
                        self.log("😴 Current layout already optimal", Fore.BLUE)
            if (
                total_empty_room_slots == 0
                and total_empty_rack_slots == 0
                and (not need_rack_evolution)
                and (not need_miner_evolution)
            ):
                self.log("🧠 Layout already optimal, skipping...", Fore.GREEN)
                return True
            mixed_rack_detected = False
            mixed_miner_detected = False
            for _room_id, rack_list in racks_by_room.items():
                names = {r["name"] for r in rack_list}
                if len(names) > 1:
                    mixed_rack_detected = True
                    break

            def is_unsorted(scores):
                return any(scores[i] < scores[i + 1] for i in range(len(scores) - 1))

            for rack_id, miner_list in miners_by_rack.items():
                scores = [calc_miner_score(account_power, account_bonus, m) for m in miner_list]
                if is_unsorted(scores):
                    mixed_miner_detected = True
                    break
            do_rack_layout = has_rack_inventory and total_empty_room_slots > 0 or need_rack_evolution
            do_miner_layout = has_miner_inventory and total_empty_rack_slots > 0 or need_miner_evolution
            self.log("🧠 Checking layout consistency...", Fore.MAGENTA)
            self.log(f"🗄️ Mixed Rack: {mixed_rack_detected}", Fore.YELLOW)
            self.log(f"⚙️ Mixed Miner: {mixed_miner_detected}", Fore.YELLOW)
            if mixed_miner_detected or (need_miner_evolution and has_miner_inventory):
                self.log("⚙️ Reorganizing miners (cleanup)...", Fore.MAGENTA)
                all_miner_ids = [m["_id"] for m in miners]
                for i in range(0, len(all_miner_ids), 20):
                    chunk = all_miner_ids[i : i + 20]
                    await self._request(
                        "POST",
                        "api/game/move-miners-to-inventory",
                        json_data={"type": "default", "user_miners_id": chunk},
                    )
                    self.log(f"   • Pulled {len(chunk)} miners", Fore.YELLOW)
                _, res = await self._request("GET", f"api/game/room-config/{user_id}")
                racks = res["data"].get("racks", [])
                miners = res["data"].get("miners", [])
            if mixed_rack_detected or (need_rack_evolution and has_rack_inventory):
                self.log("🧱 Reorganizing racks (cleanup)...", Fore.MAGENTA)
                all_rack_ids = [r["_id"] for r in racks]
                for i in range(0, len(all_rack_ids), 20):
                    chunk = all_rack_ids[i : i + 20]
                    await self._request(
                        "POST",
                        "api/game/move-racks-to-inventory",
                        json_data={"type": "default", "user_racks_id": chunk},
                    )
                    self.log(f"   • Pulled {len(chunk)} racks", Fore.YELLOW)
                _, res = await self._request("GET", f"api/game/room-config/{user_id}")
                racks = res["data"].get("racks", [])
                rack_inventory = await self.get_full_inventory("rack")
                self.log("🔄 Inventory refreshed after cleanup", Fore.MAGENTA)
                for r in rack_inventory:
                    self.log(f"   • {r['name']} | qty={r.get('quantity')}", Fore.CYAN)
            if not do_rack_layout and (not do_miner_layout):
                self.log("😴 Layout skipped (no matching inventory or no space)", Fore.BLUE)
                return True
            racks_by_name = defaultdict(list)
            for r in rack_inventory:
                if r.get("quantity", 0) > 0 and "rack_id" in r:
                    racks_by_name[r["name"]].append(r)
                else:
                    self.log(f"⚠️ Skipping invalid rack item: {r.get('name')}", Fore.RED)
            miners_by_name = defaultdict(list)
            for m in miner_inventory:
                if m["quantity"] > 0:
                    miners_by_name[m["name"]].append(m)
            if do_rack_layout:
                self.log("🧱 Smart placing racks...", Fore.GREEN)
                while True:
                    rack_inventory = await self.get_full_inventory("rack")
                    total_qty = sum(r.get("quantity", 0) for r in rack_inventory)
                    self.log(f"🔄 Loop inventory check → total rack qty: {total_qty}", Fore.MAGENTA)
                    if total_qty <= 0:
                        self.log("✅ All racks placed (inventory empty)", Fore.GREEN)
                        break
                    _, res = await self._request("GET", f"api/game/room-config/{user_id}")
                    data = res["data"]
                    rooms = data.get("rooms_available", [])
                    racks = data.get("racks", [])
                    racks = sorted(racks, key=lambda r: r.get("bonus", 0), reverse=True)
                    racks_by_room = defaultdict(list)
                    for r in racks:
                        racks_by_room[r["placement"]["user_room_id"]].append(r)
                    total_empty = 0
                    room_slot_map = {}
                    for room in rooms:
                        if room["room_info"]["level"] == -1:
                            continue
                        cols = room["room_info"]["cols"] // 2
                        rows = room["room_info"]["rows"]
                        used = {(r["placement"]["x"], r["placement"]["y"]) for r in racks_by_room.get(room["_id"], [])}
                        free_slots = [(x, y) for x in range(cols) for y in range(rows) if (x, y) not in used]
                        total_empty += len(free_slots)
                        room_slot_map[room["_id"]] = free_slots
                    self.log(f"📦 Remaining room slots: {total_empty}", Fore.YELLOW)
                    if total_empty <= 0:
                        self.log("🛑 No more room space available", Fore.RED)
                        break
                    rack_inventory = sorted(rack_inventory, key=lambda r: r.get("bonus", 0), reverse=True)
                    placed_any = False
                    for item in rack_inventory:
                        if item.get("quantity", 0) <= 0:
                            continue
                        name = item["name"]
                        while item["quantity"] > 0:
                            placed = False
                            for room_id, slots in room_slot_map.items():
                                if not slots:
                                    continue
                                x, y = slots.pop(0)
                                await self._request(
                                    "POST",
                                    "api/game/move-racks-from-inventory",
                                    json_data={
                                        "items": [
                                            {
                                                "rack_id": item["rack_id"],
                                                "placement": {"user_room_id": room_id, "x": x, "y": y, "room_level": 1},
                                            }
                                        ]
                                    },
                                )
                                item["quantity"] -= 1
                                placed = True
                                placed_any = True
                                room_label = room_index_map.get(room_id, "?")
                                self.log(
                                    f"   ➕ [{name} | Bonus Percent: {item.get('bonus')}] → Room#{room_label} @ ({x},{y})",
                                    Fore.CYAN,
                                )
                                break
                            if not placed:
                                break
                    if not placed_any:
                        self.log("🛑 Nothing placed this cycle → stop", Fore.RED)
                        break
            _, res = await self._request("GET", f"api/game/room-config/{user_id}")
            data = res["data"]
            racks = data.get("racks", [])
            miners = data.get("miners", [])
            if not racks:
                self.log("🛑 No installed racks → skip miner layout", Fore.RED)
                return True
            miners = [m for m in miners if any(r["_id"] == m["placement"]["user_rack_id"] for r in racks)]
            miners_by_rack = defaultdict(list)
            for m in miners:
                miners_by_rack[m["placement"]["user_rack_id"]].append(m)
            total_empty_rack_slots = 0
            self.log(f"DEBUG racks={len(racks)} miners={len(miners)}", Fore.YELLOW)
            for rack in racks:
                rack_cols = rack.get("rack_info", {}).get("width", 1)
                rack_rows = rack.get("rack_info", {}).get("height", 1)
                used = set()
                for m in miners_by_rack.get(rack["_id"], []):
                    mx, my = (m["placement"]["x"], m["placement"]["y"])
                    mw = m.get("width", 1)
                    for dx in range(mw):
                        used.add((mx + dx, my))
                total_empty_rack_slots += rack_cols * rack_rows - len(used)
            self.log(f"🔄 Updated rack slots: {total_empty_rack_slots}", Fore.CYAN)
            do_miner_layout = has_miner_inventory and total_empty_rack_slots > 0 or need_miner_evolution
            if do_miner_layout and racks:
                self.log("⚙️ Smart placing miners (sorted)...", Fore.GREEN)
                while True:
                    miner_inventory = await self.get_full_inventory("miner")
                    miner_inventory = sorted(
                        miner_inventory, key=lambda m: calc_miner_score(account_power, account_bonus, m), reverse=True
                    )
                    placed_any_global = False
                    for item in miner_inventory:
                        if item.get("quantity", 0) <= 0:
                            continue
                        name = item["name"]
                        width = item.get("width", 1)
                        while item["quantity"] > 0:
                            _, res = await self._request("GET", f"api/game/room-config/{user_id}")
                            data = res["data"]
                            racks = data.get("racks", [])
                            racks = sorted(racks, key=lambda r: r.get("bonus", 0), reverse=True)
                            miners = data.get("miners", [])
                            miners_by_rack = defaultdict(list)
                            for mm in miners:
                                miners_by_rack[mm["placement"]["user_rack_id"]].append(mm)
                            placed = False
                            for rack in racks:
                                rack_id = rack["_id"]
                                cols = rack.get("rack_info", {}).get("width", 1)
                                rows = rack.get("rack_info", {}).get("height", 1)
                                used = set()
                                for mm in miners_by_rack.get(rack_id, []):
                                    mx, my = (mm["placement"]["x"], mm["placement"]["y"])
                                    mw = mm.get("width", 1)
                                    for dx in range(mw):
                                        if mx + dx < cols:
                                            used.add((mx + dx, my))
                                free_slots = {(x, y) for y in range(rows) for x in range(cols) if (x, y) not in used}
                                if not free_slots:
                                    continue
                                for x, y in free_slots:
                                    if any(x + dx >= cols or (x + dx, y) not in free_slots for dx in range(width)):
                                        continue
                                    status, res_place = await self._request(
                                        "POST",
                                        "api/game/move-miners-from-inventory",
                                        json_data={
                                            "items": [
                                                {
                                                    "miner_id": item["miner_id"],
                                                    "placement": {"user_rack_id": rack_id, "x": x, "y": y},
                                                }
                                            ]
                                        },
                                    )
                                    if not res_place or not res_place.get("success"):
                                        continue
                                    await asyncio.sleep(0.1)
                                    self.log(
                                        f"➕ [{name} | Bonus Percent: {item.get('bonus_percent')}] → Rack({rack_id[:6]}) @ ({x},{y})",
                                        Fore.CYAN,
                                    )
                                    item["quantity"] -= 1
                                    placed = True
                                    placed_any_global = True
                                    break
                                if placed:
                                    break
                            if not placed:
                                self.log(f"🛑 Cannot place [{name}] anymore", Fore.RED)
                                break
                    if not placed_any_global:
                        self.log("💀 No placement happened → stop", Fore.RED)
                        break
            self.log("✅ Layout adjustment complete", Fore.GREEN)
            return True
        except Exception as e:
            self.log(f"❌ Layout failed: {e}", Fore.RED)
            return False

    async def get_balance_ws(self, currency="rlt", log=False):
        balance = 0
        try:
            ws_url = f"wss://ws.rollercoin.com/cmd?token={self.access_token}"
            ws = await self.ws_connect(ws_url)
            if ws and ws.is_open:
                await self.ws_send(ws, json.dumps({"cmd": "balance_request"}))
                for _ in range(10):
                    raw = await self.ws_recv(ws, timeout=2)
                    if not raw or raw in ("TIMEOUT", "ERROR"):
                        continue
                    if raw == "CLOSED":
                        break
                    try:
                        msg = json.loads(raw)
                    except:
                        continue
                    if msg.get("cmd") == "balance":
                        balance = int(msg.get("cmdval", {}).get(currency, 0))
                        if log:
                            self.log(f"💰 {currency.upper()} Balance: {balance}", Fore.YELLOW)
                        break
            await self.ws_close(ws)
        except Exception as e:
            self.log(f"⚠️ WS balance error: {e}", Fore.YELLOW)
        return balance

    async def auto_buy_parts(self, missing):
        self.log("🛒 AUTO BUY PARTS START", Fore.GREEN)
        balance_rst = await self.get_balance_ws("rst", log=True)
        if balance_rst <= 0:
            self.log("🛑 No RST balance", Fore.RED)
            return False
        _, market_res = await self._request("GET", "api/market/offers?category[]=season_store&limit=16")
        if not market_res or not market_res.get("success"):
            self.log("❌ Failed get market offers", Fore.RED)
            return False
        offers = market_res["data"]["offers"]
        target_cases = {"Wire": None, "Fan": None, "Hashboard": None}
        for off in offers:
            try:
                title = off.get("title", {}).get("en", "").lower()
                if "wire" in title:
                    target_cases["Wire"] = off
                elif "fan" in title:
                    target_cases["Fan"] = off
                elif "hashboard" in title:
                    target_cases["Hashboard"] = off
            except Exception as e:
                self.log(f"⚠️ Parse error: {e}", Fore.YELLOW)
                continue
        self.log(f"📦 Available cases: {list((k for k, v in target_cases.items() if v))}", Fore.CYAN)

        async def purchase(offer):
            payload = {
                "offer_id": offer["market_offers_id"],
                "quantity": 1,
                "price": offer["price_info"]["price"],
                "currency": offer["price_info"]["currency"],
            }
            _, res = await self._request("POST", "api/market/purchase", json_data=payload)
            return res and res.get("success")

        async def open_box(item_id):
            payload = {"mystery_box_id": item_id, "quantity": 1}
            _, res = await self._request("POST", "api/mystery-boxes/open", json_data=payload)
            return res

        for (name, lvl), need in missing.items():
            if lvl != 0:
                continue
            case = target_cases.get(name)
            if not case:
                self.log(f"⚠️ No case for {name}", Fore.YELLOW)
                continue
            price = case["price_info"]["price"]
            item_id = case["items"][0]["item_id"]
            self.log(f"🛒 Buying {name} → need {need}", Fore.GREEN)
            collected = 0
            while collected < need:
                if balance_rst < price:
                    self.log("🛑 Not enough RST", Fore.RED)
                    return False
                ok = await purchase(case)
                if not ok:
                    self.log("❌ Purchase failed", Fore.RED)
                    return False
                balance_rst -= price
                res = await open_box(item_id)
                if not res or not res.get("success"):
                    self.log("❌ Open box failed", Fore.RED)
                    return False
                rewards = res.get("data", [])
                gained = 0
                for r in rewards:
                    item = r.get("item", {})
                    if item.get("level") == 0:
                        gained += item.get("amount", 0)
                collected += gained
                self.log(f"🎁 Opened {name} case → +{gained} (total {collected}/{need})", Fore.CYAN)
                await asyncio.sleep(random.uniform(0.5, 1.2))
        self.log("✅ AUTO BUY DONE", Fore.GREEN)
        return True

    @wrapper_feature
    async def merge(self):
        self.log("🧬 Phase: merge miner scan", Fore.GREEN)
        try:
            _, res = await self._request("GET", "api/profile/user-profile-data")
            if not res or not res.get("success"):
                raise ValueError("failed get profile")
            user_id = res["data"]["id"]
            self.log(f"🧬 User ID: {user_id}", Fore.CYAN)
            _, room_res = await self._request("GET", f"api/game/room-config/{user_id}")
            if not room_res or not room_res.get("success"):
                raise ValueError("failed get room")
            room_data = room_res.get("data", {})
            miners_room = room_data.get("miners", [])
            self.log(f"🏠 Room miners: {len(miners_room)}", Fore.BLUE)
            inv_items = await self.get_full_inventory("miner")
            self.log(f"🎒 Inventory miners: {len(inv_items)}", Fore.BLUE)
            all_miners = []
            for m in miners_room:
                all_miners.append(
                    {
                        "id": m.get("_id"),
                        "name": m.get("name"),
                        "level": m.get("level"),
                        "width": m.get("width"),
                        "source": "room",
                    }
                )
            for m in inv_items:
                qty = m.get("quantity", 0)
                if qty <= 0:
                    continue
                for _ in range(qty):
                    all_miners.append(
                        {
                            "id": m.get("miner_id"),
                            "name": m.get("name"),
                            "level": m.get("level", 0),
                            "width": m.get("width", 1),
                            "source": "inventory",
                        }
                    )
            self.log(f"🧩 Total miners collected: {len(all_miners)}", Fore.CYAN)
            grouped = defaultdict(list)
            for m in all_miners:
                if not m["name"]:
                    continue
                key = (m["name"], m["level"], m["width"])
                grouped[key].append(m)
            pairs = []
            for _key, items in grouped.items():
                if len(items) < 2:
                    continue
                for i in range(0, len(items) // 2 * 2, 2):
                    pairs.append((items[i], items[i + 1]))
            if not pairs:
                self.log("😴 No mergeable miners found", Fore.YELLOW)
                return True
            self.log(f"🔥 Found {len(pairs)} merge pairs!", Fore.GREEN)
            for i, (a, b) in enumerate(pairs, 1):
                self.log(
                    f"🔗 Pair {i} → {a['name']} | lvl={a['level']} | width={a['width']} [{a['source']} + {b['source']}]",
                    Fore.MAGENTA,
                )
            _, part_res = await self._request(
                "GET",
                "api/forge/crafting-list?sort=level&sort_direction=-1&group_code=parts_merge&is_craftable=false&skip=0&limit=50&group=merge",
            )
            part_recipes = part_res.get("data", {}).get("craftings", []) if part_res else []
            part_map = {}
            for p in part_recipes:
                prev = p.get("prev_item_info", {})
                name = prev.get("name", {}).get("en")
                level = prev.get("level")
                if name:
                    part_map[name, level] = p

            def resolve_component(name, level, count, inventory, visited=None, depth=0):
                plan = []
                indent = "  " * depth
                key = (name, level)
                if visited is None:
                    visited = set()
                if key in visited:
                    self.log(f"{indent}⚠️ Loop detected {name} lvl {level} (skip)", Fore.RED)
                    return {"base": {}, "rlt": 0}
                visited = visited or set()
                visited.add(key)
                have = inventory.get(key, 0)
                if have > 0:
                    used = min(have, count)
                    count -= used
                    inventory[key] -= used
                    self.log(f"{indent}♻️ Use inventory {name} lvl {level} x{used}", Fore.MAGENTA)
                if count <= 0:
                    return {"base": {}, "rlt": 0}
                if level == 0:
                    return {"base": {(name, 0): count}, "rlt": 0}
                recipe = part_map.get((name, level - 1))
                if not recipe:
                    self.log(f"{indent}❌ Missing recipe for {name} lvl {level}", Fore.RED)
                    return {"base": {(name, level): count}, "rlt": 0}
                price = recipe.get("price_with_discount", {})
                rlt_cost = price.get("amount", 0) * count
                total_base = {}
                total_rlt = rlt_cost
                for req in recipe.get("required_items", []):
                    sub_name = req.get("name", {}).get("en")
                    sub_lvl = req.get("level", 0)
                    sub_count = req.get("count", 0) * count
                    self.log(f"{indent}↘️ need {sub_name} lvl {sub_lvl} x{sub_count}", Fore.CYAN)
                    res = resolve_component(sub_name, sub_lvl, sub_count, inventory, visited.copy(), depth + 1)
                    total_rlt += res["rlt"]
                    plan.extend(res.get("plan", []))
                    for k, v in res["base"].items():
                        total_base[k] = total_base.get(k, 0) + v
                plan.append((name, level, count))
                return {"base": total_base, "rlt": total_rlt, "plan": plan}

            _, part_inv_res = await self._request(
                "GET", "api/storage/inventory/parts?sort=date&sort_direction=-1&skip=0&limit=24"
            )
            if not part_inv_res or not part_inv_res.get("success"):
                self.log("❌ Failed get parts inventory", Fore.RED)
                return False
            user_parts = {}
            rarity_to_lvl = {"Common": 0, "Uncommon": 1, "Rare": 2, "Epic": 3, "Legendary": 4}
            for item in part_inv_res["data"]["items"]:
                name = item["name"]["en"]
                rarity = item["rarity_name"]["en"]
                lvl = rarity_to_lvl.get(rarity, 0)
                qty = item.get("quantity", 0)
                key = (name, lvl)
                user_parts[key] = user_parts.get(key, 0) + qty
            self.log("📦 USER PARTS:", Fore.BLUE)
            for (n, l), q in user_parts.items():
                self.log(f"   - {n} lvl {l}: {q}", Fore.BLUE)
            self.log("🧠 Analyzing merge recipes...", Fore.GREEN)
            best_choice = None
            best_score = 0
            rankings = []
            for i, (a, _b) in enumerate(pairs, 1):
                name = a["name"]
                level = a["level"]
                total_plan = []
                search_name = name.replace(" ", "+")
                url = f"api/forge/crafting-list?search={search_name}&sort=created&sort_direction=-1&group_code=miners_merge&is_craftable=false&skip=0&limit=12&group=merge"
                _, craft_res = await self._request("GET", url)
                if not craft_res or not craft_res.get("success"):
                    self.log(f"⚠️ No recipe for {name}", Fore.YELLOW)
                    continue
                craftings = craft_res.get("data", {}).get("craftings", [])
                recipe = None
                for c in craftings:
                    prev = c.get("prev_item_info", {})
                    if prev.get("level") == level:
                        recipe = c
                        break
                if not recipe:
                    self.log(f"⚠️ No matching recipe lvl {level} for {name}", Fore.YELLOW)
                    continue
                curr_info = recipe.get("prev_item_info", {})
                next_info = recipe.get("result_item_info", {})
                curr_power = curr_info.get("power", 0)
                next_power = next_info.get("power", 0)
                curr_percent = curr_info.get("percent", 0)
                next_percent = next_info.get("percent", 0)
                power_gain = next_power - curr_power
                percent_gain = next_percent - curr_percent
                price = recipe.get("price_with_discount", {})
                rlt_cost = price.get("amount", 0)
                required = recipe.get("required_items", [])
                self.log(f"🧪 [{i}] {name} lvl {level} → lvl {level + 1}", Fore.CYAN)
                self.log(f"💰 Cost: {rlt_cost} {price.get('currency')}", Fore.YELLOW)
                total_rlt_all = rlt_cost
                total_base_all = {}
                temp_inventory = copy.deepcopy(user_parts)
                for item in required:
                    itype = item.get("type")
                    iname = item.get("name", {}).get("en")
                    count = item.get("count")
                    lvl = item.get("level", 0)
                    if itype == "miners" or iname == name:
                        self.log(f"   🧩 Miner: {iname} lvl {lvl} x{count} (skip)", Fore.MAGENTA)
                        continue
                    self.log(f"   🔧 Component: {iname} lvl {lvl} x{count} → breakdown...", Fore.BLUE)
                    res = resolve_component(iname, lvl, count, temp_inventory)
                    total_rlt_all += res["rlt"]
                    total_plan.extend(res.get("plan", []))
                    for k, v in res["base"].items():
                        total_base_all[k] = total_base_all.get(k, 0) + v
                self.log(f"💰 Total REAL Cost (RLT + craft): {total_rlt_all}", Fore.YELLOW)
                self.log("🧱 FINAL BASE MATERIALS:", Fore.GREEN)
                for (bname, blvl), bcount in total_base_all.items():
                    self.log(f"   - {bname} lvl {blvl} x{bcount}", Fore.GREEN)
                K = 1000
                score = (power_gain + percent_gain * K) / max(total_rlt_all, 1)
                rankings.append(
                    {
                        "name": name,
                        "level": level,
                        "score": score,
                        "power_gain": power_gain,
                        "percent_gain": percent_gain,
                        "cost": total_rlt_all,
                        "base": total_base_all,
                        "plan": total_plan,
                    }
                )
                if score > best_score:
                    best_score = score
                    best_choice = rankings[-1]
            if not rankings:
                self.log("😴 No available merge choice", Fore.YELLOW)
                return True
            rankings.sort(key=lambda x: x["score"], reverse=True)
            self.log("🏆 TOP MERGE 🔥", Fore.GREEN)
            for i, r in enumerate(rankings[:5], 1):
                self.log(f"#{i} {r['name']} lvl {r['level']}", Fore.CYAN)
                self.log(f"⚡ Power +{r['power_gain']} | 📈 Percent +{r['percent_gain']}", Fore.YELLOW)
                self.log(f"💰 Total Cost: {r['cost']} RLT", Fore.YELLOW)
                self.log("🧱 Base Materials (lvl 0):", Fore.BLUE)
                for (bname, blvl), bcount in r["base"].items():
                    self.log(f"   - {bname} lvl {blvl} x{bcount}", Fore.BLUE)
                self.log(f"🧠 Score: {r['score']:.6f}", Fore.MAGENTA)
            best_choice = rankings[0]
            self.log("🚀 EXECUTE BEST MERGE", Fore.GREEN)
            self.log(f"🎯 Target: {best_choice['name']} lvl {best_choice['level']}", Fore.CYAN)
            balance_rlt = await self.get_balance_ws("rlt")
            need_rlt = best_choice["cost"]
            self.log(f"💰 RLT Balance: {balance_rlt:,}".replace(",", "."), Fore.YELLOW)
            self.log(f"💸 Required RLT: {need_rlt:,}".replace(",", "."), Fore.YELLOW)
            if balance_rlt < need_rlt:
                self.log("🛑 Not enough RLT → skip merge", Fore.RED)
                return True
            missing = {}
            for k, need in best_choice["base"].items():
                have = user_parts.get(k, 0)
                if have < need:
                    missing[k] = need - have
            if missing:
                self.log("⚠️ Missing materials → trying auto buy...", Fore.YELLOW)
                ok = await self.auto_buy_parts(missing)
                if not ok:
                    self.log("❌ Auto buy failed", Fore.RED)
                    return True
                self.log("🔁 Re-run merge after buying...", Fore.CYAN)
                return await self.merge()
            self.log("✅ All materials available → start crafting", Fore.GREEN)

            async def craft_item(recipe_id, amount):
                payload = {"crafting_offer_id": recipe_id, "amount": amount}
                _, res = await self._request("POST", "api/forge/start-crafting", json_data=payload)
                if res and (not res.get("success")):
                    err = str(res)
                    if "Not enough money" in err:
                        self.log("💀 Insufficient RLT balance during crafting!", Fore.RED)
                        return False
                return res and res.get("success")

            plan = best_choice.get("plan", [])
            merged_plan = defaultdict(int)
            for name, lvl, amount in plan:
                merged_plan[name, lvl] += amount
            plan = [(n, l, c) for (n, l), c in merged_plan.items()]
            plan.sort(key=lambda x: (x[1], x[0]))
            self.log("🧠 FINAL CRAFT PLAN:", Fore.GREEN)
            for n, l, c in plan:
                self.log(f"   - {n} lvl {l} x{c}", Fore.BLUE)
            self.log("🔍 VALIDATING FINAL PLAN...", Fore.YELLOW)
            check_inventory = dict(user_parts)
            for (name, lvl), amount in best_choice["base"].items():
                key = (name, lvl)
                have = check_inventory.get(key, 0)
                if have < amount:
                    self.log(f"❌ NOT ENOUGH {name} lvl {lvl}: need {amount}, have {have}", Fore.RED)
                    return False
                check_inventory[key] -= amount
            self.log("✅ Validation passed, safe to craft", Fore.GREEN)
            for name, lvl, amount in plan:
                recipe = part_map.get((name, lvl - 1))
                if not recipe:
                    self.log(f"⚠️ No recipe for {name} lvl {lvl}", Fore.RED)
                    continue
                recipe_id = recipe["_id"]
                self.log(f"🔧 Craft {name} lvl {lvl} x{amount}", Fore.CYAN)
                for i in range(amount):
                    self.log(f"   ↪️ crafting {name} lvl {lvl} {i + 1}/{amount}", Fore.YELLOW)
                    ok = await craft_item(recipe_id, 1)
                    if not ok:
                        self.log(f"❌ Failed craft {name} at {i + 1}", Fore.RED)
                        return False
                    await asyncio.sleep(random.uniform(0.6, 1.2))
            name = best_choice["name"]
            level = best_choice["level"]
            search_name = name.replace(" ", "+")
            url = f"api/forge/crafting-list?search={search_name}&group=merge"
            _, craft_res = await self._request("GET", url)
            if not craft_res or not craft_res.get("success"):
                self.log("❌ Failed get miner recipe", Fore.RED)
                return False
            recipe = None
            for c in craft_res["data"]["craftings"]:
                prev = c.get("prev_item_info", {})
                if prev.get("level") == level:
                    recipe = c
                    break
            if not recipe:
                self.log("❌ No miner recipe found", Fore.RED)
                return False
            recipe_id = recipe["_id"]
            self.log(f"⛏️ FINAL MERGE → {name} lvl {level + 1}", Fore.GREEN)
            ok = await craft_item(recipe_id, 1)
            if ok:
                self.log("🎉 MERGE SUCCESS!", Fore.GREEN)
            else:
                self.log("❌ MERGE FAILED!", Fore.RED)
            return True
        except Exception as e:
            self.log(f"❌ merge failed: {e}", Fore.RED)
            return False

    async def load_proxies(self, filename="proxy.txt"):
        try:
            if not os.path.exists(filename):
                return []
            async with aiofiles.open(filename, encoding="utf-8") as file:
                proxies = []
                async for line in file:
                    line = line.strip()
                    if line:
                        proxies.append(line)
                proxies = list(dict.fromkeys(proxies))
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Proxy load error: {e}", Fore.RED)
            return []

    def normalize_proxy(self, proxy):
        if isinstance(proxy, dict):
            return proxy.get("http") or proxy.get("https")
        return proxy

    def _format_aiohttp_proxy(self, proxy):
        try:
            if not proxy:
                return None
            if isinstance(proxy, dict):
                p = proxy.get("http") or proxy.get("https")
            else:
                p = proxy
            if not p:
                return None
            if "://" not in p:
                p = "http://" + p
            return p
        except Exception:
            return None

    async def prepare_session(self) -> None:
        if getattr(self, "_prepared", False):
            sess = getattr(self, "_aiohttp_session", None)
            if sess and (not sess.closed):
                return
            self._aiohttp_session = None
        if getattr(self, "_preparing", False):
            while getattr(self, "_preparing", False):
                await asyncio.sleep(0.03)
            sess = getattr(self, "_aiohttp_session", None)
            if sess and (not sess.closed) and getattr(self, "_proxy_ready", False):
                return
        self._preparing = True
        self._proxy_ready = False
        try:
            old = getattr(self, "_aiohttp_session", None)
            if old and (not old.closed) and getattr(self, "_proxy_ready", False):
                self._prepared = True
                return
            try:
                ua_func = getattr(self, "get_ua", None)
                if ua_func:
                    maybe = ua_func()
                    if inspect.isawaitable(maybe):
                        maybe = await maybe
                    if isinstance(maybe, str):
                        await self.set_header("user-agent", maybe)
            except:
                pass
            timeout = aiohttp.ClientTimeout(total=12)
            connector = aiohttp.TCPConnector(force_close=True, enable_cleanup_closed=True, use_dns_cache=False)
            async with self.session_lock:
                self._aiohttp_session = aiohttp.ClientSession(
                    timeout=timeout, connector=connector, cookie_jar=aiohttp.DummyCookieJar(), trust_env=False
                )
            use_proxy = bool(self.config.get("proxy", False))
            if use_proxy and getattr(self, "proxy_manager", None) is None:
                try:
                    if self.good_proxies:
                        self.log(f"🔥 ProxyManager using {len(self.good_proxies)} GOOD proxies", Fore.GREEN)
                        self.proxy_manager = ProxyManager(
                            proxies=list(self.good_proxies), recovery_interval=25, connect_timeout=6
                        )
                    else:
                        self.proxy_manager = None
                except Exception as e:
                    self.log(f"❌ ProxyManager creation FAILED: {e}", Fore.RED)
                    self.proxy_manager = None
            if use_proxy and self.proxy_manager:
                if hasattr(self, "good_proxies") and self.good_proxies:
                    proxy_mode = self.config.get("proxy_mode", "random")
                    idx = getattr(self, "account_index", None)
                    if proxy_mode == "index" and idx is not None:
                        self.proxy = self.good_proxies[idx % len(self.good_proxies)]
                        self.log(f"🔗 Using proxy(index={idx}): {self.proxy}", Fore.GREEN)
                    else:
                        self.proxy = random.choice(self.good_proxies)
                        self.log(f"🔗 Using proxy(random): {self.proxy}", Fore.GREEN)
                    self._proxy_ready = True
                else:
                    self.proxy = None
                    self._proxy_ready = True
                    self.log("⚠️ No good proxies. Using local.", Fore.YELLOW)
            else:
                self.proxy = None
                self._proxy_ready = True
                if not getattr(self, "_suppress_local_session_log", False):
                    self.log("🌐 Using local IP (no proxy)", Fore.YELLOW)
            self._prepared = True
        except Exception as e:
            self.log(f"❌ prepare_session error: {e}\n{traceback.format_exc()}", Fore.RED)
            self._prepared = False
            self._proxy_ready = True
            if self.proxy_manager:
                try:
                    await self.proxy_manager.start_recovery_async()
                except Exception as e:
                    self.log(f"❌ Failed to start proxy recovery: {e}", Fore.RED)
        finally:
            self._preparing = False

    async def initial_proxy_test(self):
        self.log("🧪 Testing proxies once before start...", Fore.CYAN)
        sem = asyncio.Semaphore(40)

        async def test(purl):
            async with sem:
                try:
                    ok = await self._async_test_proxy(purl)
                    if ok:
                        return ("OK", purl)
                    else:
                        return ("BAD", purl)
                except:
                    return ("ERROR", purl)

        tasks = []
        for p in self.proxy_list:
            purl = self.normalize_proxy(p)
            if "@" not in purl or purl.count(":") < 2:
                continue
            tasks.append(test(purl))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if not r:
                continue
            status, proxy = r
            if status == "OK":
                self.good_proxies.append(proxy)
            elif status == "BAD":
                pass
            elif status == "ERROR":
                self.log("ERROR")
                pass
        if not self.good_proxies:
            self.log("⚠️ No valid proxy detected, using local IP", Fore.YELLOW)
        else:
            self.log(f"✅ {len(self.good_proxies)} valid proxies 🚀", Fore.GREEN)

    async def _async_test_proxy(self, proxy_url: str, debug: bool = False) -> bool:
        if not proxy_url:
            return False
        test_url = "http://httpbin.org/ip"
        timeout = aiohttp.ClientTimeout(total=10, connect=5)
        start = time.time()
        try:
            async with aiohttp.ClientSession(timeout=timeout) as s:
                async with s.get(test_url, proxy=proxy_url) as resp:
                    latency = time.time() - start
                    if resp.status == 200:
                        await self._record_proxy_result(proxy_url, True, latency)
                        self.log(f"⚡ OK {latency * 1000:.0f}ms → {proxy_url}", Fore.GREEN)
                        return True
                    elif resp.status == 407:
                        self.log(f"🚫 407 AUTH FAIL → {proxy_url}", Fore.RED)
                    elif resp.status == 402:
                        self.log(f"💸 402 QUOTA → {proxy_url}", Fore.YELLOW)
                    else:
                        self.log(f"❌ {resp.status} → {proxy_url}", Fore.RED)
                    await self._record_proxy_result(proxy_url, False, latency)
                    return False
        except aiohttp.ClientHttpProxyError:
            self.log(f"🚫 PROXY ERROR (likely 407) → {proxy_url}", Fore.RED)
            return False
        except Exception as e:
            if debug:
                self.log(f"❌ ERROR → {proxy_url} | {type(e).__name__}", Fore.RED)
            return False

    class _WSHandle:
        def __init__(self, parent, ws) -> None:
            self._parent = parent
            self.ws = ws
            self._closed = False

        @property
        def is_open(self) -> bool:
            try:
                return not self._closed and (not getattr(self.ws, "closed", False))
            except Exception:
                return False

        async def send(self, data) -> bool:
            try:
                if isinstance(data, str):
                    await self.ws.send_str(data)
                else:
                    await self.ws.send_bytes(data)
                return True
            except Exception as e:
                try:
                    await self._parent._record_proxy_result(self._parent.proxy, False)
                except Exception:
                    pass
                self._parent.log(f"❌ ws.send error: {e}", Fore.RED)
                return False

        async def recv(self, timeout=None):
            try:
                if timeout:
                    msg = await asyncio.wait_for(self.ws.receive(), timeout=timeout)
                else:
                    msg = await self.ws.receive()
                if msg.type in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):
                    return msg.data
                if msg.type == aiohttp.WSMsgType.CLOSED:
                    self._closed = True
                    raise ConnectionError("WS closed")
                if msg.type == aiohttp.WSMsgType.ERROR:
                    raise ConnectionError("WS error")
                return None
            except TimeoutError:
                raise TimeoutError("WS timeout")
            except Exception:
                self._closed = True
                raise

        async def close(self) -> None:
            if self._closed:
                return
            try:
                await self.ws.close()
            except Exception:
                pass
            self._closed = True

    def _proxy_enabled(self) -> bool:
        try:
            return bool(self.config.get("proxy"))
        except Exception:
            return False

    async def ws_connect(self, url: str, *, timeout: float = 30.0, debug: bool = False, headers: dict | None = None):
        try:
            await self.prepare_session()
        except Exception:
            pass
        if getattr(self, "_aiohttp_session", None) is None:
            timeout_obj = aiohttp.ClientTimeout(total=None)
            self._aiohttp_session = aiohttp.ClientSession(timeout=timeout_obj)
        use_proxy = bool(self.config.get("proxy", False))
        if use_proxy and self.proxy_manager:
            chosen_proxy = await self.proxy_manager.get_proxy()
        else:
            chosen_proxy = None
        aio_proxy = self._format_aiohttp_proxy(chosen_proxy) if chosen_proxy else None
        ws_headers = {}
        if headers:
            ws_headers.update(headers)
        if debug:
            self.log(
                f"[DEBUG] ws_connect url={url} proxy={('on' if aio_proxy else 'off')} headers={list(ws_headers.keys())}",
                Fore.MAGENTA,
            )
        errors = []
        for attempt in (1, 2):
            try:
                ws_timeout = aiohttp.ClientWSTimeout(ws_close=timeout)
                ws = await self._aiohttp_session.ws_connect(
                    url, proxy=aio_proxy, timeout=ws_timeout, headers=ws_headers or None
                )
                try:
                    if chosen_proxy:
                        await self._record_proxy_result(chosen_proxy, True, 0.0)
                except Exception:
                    pass
                handle = self._WSHandle(self, ws)
                if debug:
                    self.log("🧠 ws connected (custom headers enabled)", Fore.BLUE)
                self.log(f"🐾 WebSocket connected -> {url[:16]}...", Fore.CYAN)
                return handle
            except Exception as e:
                errors.append(e)
                try:
                    if chosen_proxy:
                        await self._record_proxy_result(chosen_proxy, False, None)
                except Exception:
                    pass
                if self._proxy_enabled():
                    try:
                        await self.rotate_proxy_and_ua(force_new_proxy=True, quick_test=True)
                    except Exception:
                        pass
                if attempt == 1:
                    await asyncio.sleep(0.12)
                    continue
                break
        self.log(f"❌ ws_connect failed: {(errors[-1] if errors else 'unknown')}", Fore.RED)
        raise Exception("ws_connect failed")

    async def ws_send(
        self,
        handle,
        message,
        *,
        close_after: bool = False,
        close_delay: float = 0.0,
        wait_ack: bool = False,
        ack_timeout: float | None = None,
    ):
        try:
            ok = await handle.send(message)
            if not ok:
                raise Exception("send failed")
            self.log("📤 message sent", Fore.GREEN)
            resp = None
            if wait_ack:
                resp = await handle.recv(timeout=ack_timeout)
            if close_after:
                if close_delay and close_delay > 0:
                    await asyncio.sleep(close_delay)
                await handle.close()
            return resp
        except Exception as e:
            self.log(f"❌ ws_send error: {e}", Fore.RED)
            raise

    async def ws_recv(self, handle, *, timeout=None):
        try:
            msg = await handle.recv(timeout=timeout)
            return msg
        except TimeoutError:
            self.log("⌛ ws.recv timeout", Fore.YELLOW)
            return "TIMEOUT"
        except ConnectionError as e:
            self.log(f"💀 ws closed: {e}", Fore.RED)
            return "CLOSED"
        except Exception as e:
            self.log(f"⚠️ ws_recv error: {e}", Fore.YELLOW)
            return "ERROR"

    async def ws_close(self, handle) -> None:
        try:
            await handle.close()
            self.log("🔐 WebSocket closed", Fore.MAGENTA)
        except Exception as e:
            self.log(f"⚠️ ws_close error: {e}", Fore.YELLOW)
            raise

    async def close_async(self) -> None:
        try:
            pm = getattr(self, "proxy_manager", None)
            if pm:
                try:
                    await pm.stop_recovery_async()
                except Exception:
                    pass
        except Exception:
            pass
        try:
            if getattr(self, "_aiohttp_session", None):
                try:
                    await self._aiohttp_session.close()
                except Exception:
                    pass
                self._aiohttp_session = None
        except Exception:
            pass
        try:
            execu = getattr(self, "executor", None)
            if execu:
                try:
                    execu.shutdown(wait=False)
                except Exception:
                    pass
                self.executor = None
        except Exception:
            pass


tasks_config = {
    "batery": "Auto recharge battery",
    "daily": "Auto claim daily",
    "achievements": "Auto claim achievements",
    "task": "Auto claim task daily",
    "hamster": "Auto manage hamster",
    "merge": "Auto merge miner",
    "layout": "Auto layouting room",
    "token_mining": "Auto choose profitable token",
    "game": "Auto playing game",
}


async def call_maybe_async(func, *args, executor=None, **kwargs):
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    maybe = func(*args, **kwargs)
    if inspect.isawaitable(maybe):
        return await maybe
    if executor is not None:
        return maybe
    return await asyncio.to_thread(lambda: maybe)


async def _force_cleanup(blu) -> None:
    if blu.config.get("proxy") and getattr(blu, "proxy_manager", None) and blu.proxy:
        try:
            await blu.proxy_manager.release_proxy(blu.proxy)
            blu.log(
                f"🔁 Proxy released ({blu.proxy}) | good={len(blu.good_proxies)} in_use={blu.proxy_manager.in_use_count()}",
                Fore.GREEN,
            )
        except Exception as e:
            print(f"⚠️ release_proxy: {e}")
            blu.log("⚠️ release proxy failed", Fore.YELLOW)
        finally:
            blu.proxy = None
    if hasattr(blu, "close_async"):
        async with blu.session_lock:
            try:
                await blu.close_async()
                blu.log("📦 session closed", Fore.BLUE)
            except Exception as e:
                print(f"⚠️ close_async: {e}")
                blu.log(f"⚠️ close() error: {e}", Fore.YELLOW)
    try:
        await ultra_slim_self(blu)
    except Exception as e:
        print(f"⚠️ ultra_slim_self: {e}")


async def process_account(
    account, original_index, account_label, blu: Bot, sema: asyncio.Semaphore | None = None
) -> None:
    try:
        display_account = account[:12] + "..." if len(account) > 12 else account
        blu.print_dashboard_header(account_label)
        blu.log(f"👤 Account ID: {display_account}", Fore.YELLOW)
        
        blu.account_index = original_index
        blu.error_count = 0
        try:
            blu.config = await blu.load_config(suppress_log=True)
        except Exception as e:
            print(f"⚠️ load_config: {e}")
            blu.config = blu.config or {}
        blu.config["_task_workers"] = 1
        blu.log("🎛️ Task Workers forced to 1 (sequential mode)", Fore.MAGENTA)
        if sema is None:
            sema = asyncio.Semaphore(1)
        try:
            async with sema:
                login_ok = await call_maybe_async(blu.login, original_index, executor=getattr(blu, "executor", None))
        except Exception as e:
            blu.log(f"❌ login error: {e}", Fore.RED)
            blu.error_count += 1
            return
        if not login_ok:
            blu.log("⛔ Login failed — skipping all tasks.", Fore.RED)
            await _force_cleanup(blu)
            return
        cfg = blu.config or {}
        enabled = [name for key, name in tasks_config.items() if cfg.get(key, False)]
        blu.log("🛠️ Tasks enabled: " + (", ".join(enabled) if enabled else "(none)"), Fore.CYAN if enabled else Fore.RED)
        for task_key, _ in tasks_config.items():
            if not cfg.get(task_key, False):
                continue
            if not hasattr(blu, task_key):
                blu.log(f"⚠️ {task_key} missing", Fore.YELLOW)
                continue
            fn = getattr(blu, task_key)
            blu.log(f"▶️ Running task: {task_key}", Fore.GREEN)
            try:
                if inspect.iscoroutinefunction(fn):
                    await fn()
                else:
                    async with sema:
                        await call_maybe_async(fn, executor=getattr(blu, "executor", None))
            except Exception as e:
                print(f"⚠️ task {task_key} error: {e}")
                blu.log(f"❌ {task_key} error: {e}", Fore.RED)
                blu.error_count += 1
        delay_switch = cfg.get("delay_account_switch", 10)
        blu.log(f"➡️ Done {account_label}. wait {delay_switch}s", Fore.CYAN)
        await asyncio.sleep(delay_switch)
        if cfg.get("proxy") and getattr(blu, "proxy_manager", None) and blu.proxy:
            try:
                await blu.proxy_manager.release_proxy(blu.proxy)
                blu.log(
                    f"🔁 Proxy released ({blu.proxy}) | good={len(blu.good_proxies)} in_use={blu.proxy_manager.in_use_count()}",
                    Fore.GREEN,
                )
            except Exception as e:
                print(f"⚠️ release_proxy: {e}")
                blu.log("⚠️ release proxy failed", Fore.YELLOW)
            finally:
                blu.proxy = None
        try:
            await blu.close_async()
            blu.log("📦 session closed", Fore.BLUE)
        except Exception as e:
            print(f"⚠️ close_async: {e}")
            blu.log(f"⚠️ close() error: {e}", Fore.YELLOW)
        try:
            await ultra_slim_self(blu)
        except Exception as e:
            print(f"⚠️ ultra_slim_self: {e}")
    except Exception as mega:
        print(f"💥 FATAL error in account {account_label}: {mega}")
        blu.log(f"💥 [FATAL] Account crashed: {mega}", Fore.RED)
        blu.error_count += 1
        try:
            await ultra_slim_self(blu)
        except Exception:
            pass


async def ultra_slim_self(obj) -> None:
    keep = {
        "config",
        "query_list",
        "proxy_list",
        "proxy_manager",
        "executor",
        "shared_executor",
        "_aiohttp_session",
        "HEADERS",
        "good_proxies",
        "session_lock",
        "_transport_pref",
        "_file_cache",
        "file_writer_queue",
        "_sync_lock",
        "access_token",
        "refresh_token",
        "csrf_token",
    }
    sess = getattr(obj, "_aiohttp_session", None)
    if sess is not None:
        try:
            try:
                sess.cookies.clear()
            except Exception as e:
                print(f"⚠️ sess.cookies.clear: {e}")
            try:
                for ad in getattr(sess, "adapters", {}).values():
                    try:
                        ad.close()
                    except Exception as e:
                        print(f"⚠️ adapter.close: {e}")
            except Exception as e:
                print(f"⚠️ sess.adapters-loop: {e}")
        except Exception as e:
            print(f"⚠️ session cleanup main: {e}")
    for name in list(vars(obj).keys()):
        if name in keep:
            continue
        try:
            setattr(obj, name, None)
        except Exception as e:
            print(f"⚠️ unset attr {name}: {e}")
    try:
        snapshot = {k: getattr(obj, k, None) for k in keep}
        try:
            obj.__dict__.clear()
        except Exception as e:
            print(f"⚠️ __dict__.clear: {e}")
        for k, v in snapshot.items():
            try:
                setattr(obj, k, v)
            except Exception as e:
                print(f"⚠️ restore {k}: {e}")
    except Exception as e:
        print(f"⚠️ snapshot-restore: {e}")
    try:
        obj._base_headers = dict(getattr(obj, "HEADERS", {}) or {})
    except Exception as e:
        print(f"⚠️ _base_headers rebuild: {e}")
    obj._prepared = False
    obj._preparing = False
    obj._aiohttp_session = False
    try:
        gc.collect()
        gc.collect()
    except Exception as e:
        print(f"⚠️ gc.collect: {e}")


async def worker(worker_id: int, base_blu: Bot, queue: asyncio.Queue) -> None:
    blu = Bot(use_proxy=base_blu.config.get("proxy", False), proxy_list=base_blu.proxy_list, load_on_init=False)
    await blu.ainit_worker(base_blu)
    blu.file_writer_queue = base_blu.file_writer_queue
    blu.executor = base_blu.shared_executor
    blu.log("🔁 Worker using shared executor", Fore.CYAN)
    sema = base_blu.io_sema
    max_thread = int(base_blu.config.get("_max_workers", 1))
    blu.log(f"👷 Worker-{worker_id} started | threads={worker_id}/{max_thread}", Fore.CYAN)
    try:
        while True:
            try:
                original_index, account = await asyncio.wait_for(queue.get(), timeout=3)
            except TimeoutError:
                blu.log("⏳ timeout waiting queue, exit loop", Fore.YELLOW)
                break
            except asyncio.CancelledError:
                blu.log("🛑 worker cancelled while waiting queue", Fore.RED)
                break
            if account is None:
                blu.log("🔻 stop-signal received", Fore.YELLOW)
                break
            account_label = f"W{worker_id}-A{original_index + 1}"
            try:
                await process_account(account, original_index, account_label, blu, sema)
            except Exception as e:
                blu.log(f"❌ {account_label} error: {e}", Fore.RED)
            finally:
                try:
                    queue.task_done()
                except Exception:
                    blu.log("⚠ queue.task_done failed", Fore.YELLOW)
    except asyncio.CancelledError:
        blu.log("🛑 worker cancelled (outer loop)", Fore.RED)
    finally:
        base_blu.log(f"🧾 Worker-{worker_id} stopped", Fore.CYAN)
        async with blu.session_lock:
            try:
                await blu.close_async()
            except Exception:
                base_blu.log(f"⚠ Worker-{worker_id} session close failed", Fore.YELLOW)


async def worker_manager(base_blu: Bot, queue, stop_event) -> None:
    workers = []
    next_id = 1
    base_blu.log("🚀 worker-manager started", Fore.CYAN)
    while True:
        if stop_event.is_set():
            base_blu.log("🛑 stop_event triggered, stopping manager", Fore.RED)
            break
        workers = [w for w in workers if not w.done()]
        base_blu.active_workers = len(workers)
        if queue._getters and queue.empty():
            base_blu.log("⚠ clearing stuck queue._getters", Fore.YELLOW)
            queue._getters.clear()
        if queue.empty() and len(workers) == 0:
            base_blu.log("✨ queue empty & no workers, stopping manager", Fore.CYAN)
            break
        desired = base_blu.dynamic_worker_target
        running = len(workers)
        if running < desired and (not queue.empty()):
            w = asyncio.create_task(worker(next_id, base_blu, queue))
            workers.append(w)
            base_blu.log(f"🟢 spawn worker-{next_id}", Fore.CYAN)
            next_id += 1
        elif running > desired:
            await queue.put(None)
            base_blu.log("🔴 request-stop worker", Fore.CYAN)
        await asyncio.sleep(1)
    for _ in workers:
        await queue.put(None)
    for w in workers:
        w.cancel()
    base_blu.log("📥 worker-manager stopped cleanly", Fore.CYAN)


def estimate_network_latency(base_blu, host="1.1.1.1", port=53, attempts=2, timeout=0.6) -> float:
    latencies = []
    for i in range(attempts):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            start = time.perf_counter()
            try:
                s.connect((host, port))
            finally:
                s.close()
            lat = time.perf_counter() - start
            latencies.append(lat)
            base_blu.log(f"⚡ Latency attempt {i + 1}: {lat:.4f}s", Fore.GREEN if lat < 0.15 else Fore.YELLOW)
        except Exception as e:
            latencies.append(timeout)
            base_blu.log(f"❌ Latency attempt {i + 1} failed: {e}", Fore.RED)
    try:
        m = statistics.median(latencies)
        color = Fore.GREEN if m < 0.12 else Fore.YELLOW
        base_blu.log(f"📡 Median latency: {m:.4f}s", color)
        return max(0.005, min(m, timeout))
    except Exception as e:
        base_blu.log(f"❌ Failed calculate median: {e}", Fore.RED)
        return timeout


def auto_tune_config_async(base_blu, existing_cfg=None, prefer_network_check=True):
    cfg = dict(existing_cfg or {})
    base_blu.log("🛠 Starting auto-tune...", Fore.CYAN)
    try:
        total_mem_gb = float(psutil.virtual_memory().total) / 1024**3
        base_blu.log(f"💾 Total RAM: {total_mem_gb:.2f} GB", Fore.YELLOW)
    except Exception as e:
        total_mem_gb = 1.0
        base_blu.log(f"❌ Failed get RAM info: {e}", Fore.RED)
    try:
        disk_free_gb = float(shutil.disk_usage(os.getcwd()).free) / 1024**3
        base_blu.log(f"📂 Free disk: {disk_free_gb:.2f} GB", Fore.YELLOW)
    except Exception as e:
        disk_free_gb = 1.0
        base_blu.log(f"❌ Failed disk check: {e}", Fore.RED)
    if prefer_network_check:
        try:
            net_lat = estimate_network_latency(base_blu=base_blu)
        except Exception as e:
            base_blu.log(f"❌ Network latency check failed: {e}", Fore.RED)
            net_lat = 0.8
    else:
        net_lat = 1.0
    base_blu.log(f"🌐 Net latency: {net_lat:.4f}s", Fore.GREEN)
    if total_mem_gb < 1:
        q_recommend = 200
    elif total_mem_gb < 2.5:
        q_recommend = 450
        base_blu.log("📊 RAM class: LOW-MID", Fore.MAGENTA)
    elif total_mem_gb < 8:
        q_recommend = 900
        base_blu.log("📊 RAM class: MID", Fore.MAGENTA)
    else:
        q_recommend = 2000
        base_blu.log("📊 RAM class: HIGH", Fore.MAGENTA)
    if total_mem_gb < 1.0:
        poll = 1.1
    elif net_lat < 0.05:
        poll = 0.22
    elif net_lat < 0.12:
        poll = 0.35
    elif net_lat < 0.3:
        poll = 0.55
    else:
        poll = 0.75
    base_blu.log(f"🧮 Recommended queue: {q_recommend}", Fore.CYAN)
    base_blu.log(f"⏱ Poll interval: {poll}", Fore.CYAN)
    merged = dict(cfg)
    merged.setdefault("queue_maxsize", q_recommend)
    merged.setdefault("poll_interval", poll)
    merged.setdefault("dedupe", total_mem_gb >= 1.0)
    merged.setdefault("run_mode", cfg.get("run_mode", "continuous"))
    merged["_autotune_meta"] = {
        "total_mem_gb": round(total_mem_gb, 2),
        "disk_free_gb": round(disk_free_gb, 2),
        "net_latency_s": round(net_lat, 4),
        "queue_recommendation": q_recommend,
        "poll_recommendation": poll,
    }
    base_blu.log("✅ Auto-tune complete.", Fore.GREEN)
    return merged


def cleanup_after_batch(base_blu: Bot, keep_refs: dict | None = None, deep=False) -> None:
    try:
        sess = getattr(base_blu, "_aiohttp_session", None)
        if sess is not None:
            try:
                sess.cookies.clear()
            except Exception as e:
                print(f"⚠️ sess.cookies.clear: {e}")
        if keep_refs is None:
            keep_refs = {}
        for k in ("last_items", "promo_data", "last_shop", "items_data"):
            if k not in keep_refs:
                try:
                    setattr(base_blu, k, None)
                except Exception as e:
                    print(f"⚠️ unset attr {k}: {e}")
        if deep:
            for name in list(vars(base_blu).keys()):
                if name.startswith("_") or name in ("logger", "log", "_aiohttp_session", "config"):
                    continue
                try:
                    setattr(base_blu, name, None)
                except Exception as e:
                    print(f"⚠️ deep unset attr {name}: {e}")
        try:
            gc.collect()
        except Exception as e:
            print(f"⚠️ gc.collect #1: {e}")
        try:
            pm = getattr(base_blu, "proxy_manager", None)
            if pm:
                snap = pm.snapshot()
                if snap.get("in_use", 0) > 0:
                    base_blu.log(f"⚠️ cleanup: {snap['in_use']} proxies still in-use; snapshot={snap}", Fore.YELLOW)
        except Exception as e:
            print(f"⚠️ proxy_manager cleanup: {e}")
        try:
            CLEAN_ALLOW = (
                "requests",
                "urllib3",
                "aiohttp",
                "websocket",
                "brotli",
                "gzip",
                "zlib",
                "chardet",
                "fake_useragent",
                "psutil",
                "hashlib",
                "hmac",
                "base64",
                "cryptography",
            )
            CORE_BLOCKLIST = (
                "asyncio",
                "concurrent",
                "threading",
                "socket",
                "os",
                "sys",
                "time",
                "gc",
                "json",
                "queue",
                "statistics",
                "inspect",
                "traceback",
                "datetime",
                "random",
                "signal",
                "shutil",
                "tracemalloc",
                "collections",
                "psutil",
            )
            for name, module in list(sys.modules.items()):
                if name.startswith(CORE_BLOCKLIST):
                    continue
                if any(p in name for p in CLEAN_ALLOW):
                    try:
                        del sys.modules[name]
                    except Exception as e:
                        print(f"⚠️ sys.modules.del(clean_allow): {e}")
                else:
                    try:
                        attrs = dir(module)
                        if (
                            "HTTPConnection" in attrs
                            or "HTTPSConnection" in attrs
                            or "PoolManager" in attrs
                            or ("ClientSession" in attrs)
                            or ("WebSocketClientProtocol" in attrs)
                        ):
                            try:
                                del sys.modules[name]
                            except Exception as e:
                                print(f"⚠️ sys.modules.del(http-related): {e}")
                    except Exception as e:
                        print(f"⚠️ sys.modules.attr-scan: {e}")
        except Exception as e:
            print(f"⚠️ sys.modules cleanup: {e}")
        try:
            gc.collect()
            gc.collect()
        except Exception as e:
            print(f"⚠️ gc.collect #2: {e}")
        try:
            emoji = random.choice(["🧹", "♻️", "🧽", "🌀", "🚿"])
            base_blu.log(f"{emoji} cleanup done | {base_blu.memory_monitor()}", Fore.LIGHTBLACK_EX)
        except Exception as e:
            print(f"⚠️ emoji/status log: {e}")
    except Exception as e:
        print(f"⚠️ cleanup_after_batch: {e}")


async def file_writer_worker(base_blu: Bot, queue, stop_event, sema=None) -> None:
    base_blu.log("📝 file-writer started", Fore.GREEN)
    sema = sema or asyncio.Semaphore(1)
    while not stop_event.is_set():
        try:
            task = await asyncio.wait_for(queue.get(), timeout=2)
        except TimeoutError:
            continue
        if task is None:
            break
        try:
            async with sema:
                if callable(task):
                    if inspect.iscoroutinefunction(task):
                        await task()
                    else:
                        result = task()
                        if asyncio.iscoroutine(result):
                            await result
                else:
                    print("❌ invalid task (not callable)")
        except Exception as e:
            print(f"❌ file task error: {e}")
        queue.task_done()
    base_blu.log("🛑 file-writer stopped", Fore.RED)


async def main() -> None:
    loop_counter = 0
    max_once_loops = None
    while True:
        stop_event = asyncio.Event()
        manager_task = None
        base_blu = Bot()
        try:
            await base_blu.ainit_main()
            # Ensure sync lock and file cache exist
            if not hasattr(base_blu, '_sync_lock'):
                base_blu._sync_lock = asyncio.Lock()
            if not hasattr(base_blu, '_file_cache'):
                base_blu._file_cache = {}
            
            base_blu.active_workers = 0
            cfg_file = base_blu.config
            effective = auto_tune_config_async(base_blu=base_blu, existing_cfg=cfg_file)
            base_blu.config = effective
            run_mode = effective.get("run_mode", "repeat")
            max_once_loops = int(effective.get("once_loops", 1))
            base_blu.log(f"🎉 [LIVEXORDS] === Welcome to Automation === [Mode: {run_mode}] ===", Fore.YELLOW)
            query_file = effective.get("query_file", "query.txt")
            queue_maxsize = int(effective.get("queue_maxsize", 200))
            query_offset = int(effective.get("query_offset", 0))
            base_blu.query_list = await base_blu.load_query(query_file, limit=queue_maxsize, offset=query_offset)
            base_blu.banner()
            base_blu.log(f"📂 Query file: {query_file} | Queue size: {queue_maxsize} | Mode: {run_mode}", Fore.YELLOW)
            global_workers = int(base_blu.config.get("_max_workers", 1))
            base_blu.dynamic_worker_target = global_workers
            base_blu.log(f"🎛️ Max workers allowed: {global_workers}", Fore.MAGENTA)
            base_blu.io_sema = asyncio.Semaphore(global_workers)
            stop_event.clear()
            queue = asyncio.Queue()
            file_write_queue = asyncio.Queue()
            base_blu.file_writer_queue = file_write_queue
            
            # If query_list is empty but we have tokens from input, use them
            if not base_blu.query_list and base_blu.access_token:
                base_blu.query_list = [f"{base_blu.access_token}|{base_blu.refresh_token}|{base_blu.csrf_token}"]
                base_blu.log("✅ Using manually entered tokens", Fore.GREEN)
            
            for i, account in enumerate(base_blu.query_list):
                orig_index = query_offset + i
                await queue.put((orig_index, account))
            if base_blu.config.get("proxy", False):
                await base_blu.initial_proxy_test()
            manager_task = asyncio.create_task(worker_manager(base_blu, queue, stop_event))
            file_writer_task = asyncio.create_task(file_writer_worker(base_blu, file_write_queue, stop_event))
            await manager_task
            await file_write_queue.join()
            await file_write_queue.put(None)
            stop_event.set()
            if file_writer_task:
                try:
                    await file_writer_task
                except:
                    pass
            try:
                cleanup_after_batch(base_blu)
            except Exception:
                pass
            base_blu.log("🔁 Batch completed", Fore.CYAN)
            base_blu.log(f"🧾 Memory: {base_blu.memory_monitor()}", Fore.MAGENTA)
            if run_mode == "once":
                loop_counter += 1
                base_blu.log(f"🔁 Once loop progress: {loop_counter}/{max_once_loops}", Fore.YELLOW)
                if loop_counter >= max_once_loops:
                    base_blu.log("🏁 Mode 'once' loops finished. Exiting...", Fore.GREEN)
                    break
            delay_loop = int(effective.get("delay_loop", 30))
            coffee_types = ["Americano", "Espresso", "Latte", "Cappuccino", "Long Black", "Mocha"]
            coffee_pick = random.choice(coffee_types)
            base_blu.log(f"☕ Brewing {coffee_pick}... {delay_loop}s cooldown begins", Fore.CYAN)
            for _ in range(delay_loop):
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            base_blu.log("🛑 CTRL+C detected, shutting down...", Fore.RED)
            break
        except Exception as e:
            try:
                base_blu.log(f"❌ Main loop exception: {e}", Fore.RED)
            except Exception:
                print("Main loop exception:", e)
        finally:
            stop_event.set()
            session = getattr(base_blu, "_aiohttp_session", None)
            if session and (not getattr(session, "closed", True)):
                try:
                    await session.close()
                except Exception:
                    pass
    base_blu.log("✅ Shutdown complete", Fore.MAGENTA)


async def launcher() -> None:
    try:
        await main()
    except Exception as e:
        print("Error:", e)
    finally:
        print("🔥 ensuring clean shutdown...")


if __name__ == "__main__":
    try:
        asyncio.run(launcher())
    except KeyboardInterrupt:
        print("Interrupted by user. Bye!")