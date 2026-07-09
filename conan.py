#!/usr/bin/env python3

import os
import time
import requests
import sys
import re
from datetime import datetime

# ======================= PREMIUM COLORS =======================
C1 = "\033[38;5;51m"      # Cyan
C2 = "\033[38;5;199m"     # Pink
C3 = "\033[38;5;226m"     # Yellow
C4 = "\033[38;5;46m"      # Green
C5 = "\033[38;5;196m"     # Red
GOLD = "\033[38;5;220m"
PURPLE = "\033[38;5;141m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

HL = "─"
VL = "│"

def clear(): os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"{C1}{HL*60}{RESET}")
    print(f"{C2}{BOLD}")
    print("  ███████╗██╗   ██╗██████╗ ██████╗ ")
    print("  ██╔════╝██║   ██║██╔══██╗██╔══██╗")
    print("  █████╗  ██║   ██║██████╔╝██████╔╝")
    print("  ██╔══╝  ██║   ██║██╔══██╗██╔══██╗")
    print("  ██║     ╚██████╔╝██║  ██║██║  ██║")
    print("  ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝")
    print(f"{RESET}")
    print(f"{C1}{HL*60}{RESET}")
    print(f"{C4}👑 DEV: {WHITE}@FURR_CREATOR {C1}┃ {C2}🚀 TG: {WHITE}https://chat.whatsapp.com/BMXzHOEYdy6AardVjevCX7 {C1}┃ {C3}👛 MODE: {WHITE}GILS")
    print(f"{C1}{HL*60}{RESET}")

class ConanEngine:
    def __init__(self, email, ua):
        self.base_url = "https://conanbtc.com/index.php"
        self.session = requests.Session()
        self.headers = {'User-Agent': ua, 'Referer': "https://conanbtc.com/"}
        self.email = email
        self.stats = {"gold": 0, "gil": 0, "st": 0}
        self.history = [] # For storing logs

    def log_history(self, msg, color=WHITE, icon="●"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f" {PURPLE}│{RESET} {color}[{timestamp}] {icon} {msg}{RESET}"
        self.history.append(formatted)

    def update_stats(self, html):
        try:
            gold = re.search(r'icgold\.png".*?<b>(\d+)</b>', html)
            if gold: self.stats["gold"] = int(gold.group(1))
            gil = re.search(r'money\.png".*?<b>(\d+)</b>', html)
            if gil: self.stats["gil"] = int(gil.group(1))
            st_m = re.search(r'ST:\s*(\d+)', html) or re.search(r'data-current="(\d+)"', html)
            if st_m: self.stats["st"] = int(st_m.group(1))
        except: pass

    def refresh_ui(self):
        clear(); banner()
        print(f"\n {PURPLE}╭─ {GOLD}CONAN LIVE DASHBOARD{RESET}")
        print(f" {VL} {WHITE}USER EMAIL : {C1}{self.email}{RESET}")
        print(f" {VL} {WHITE}BALANCE    : {C4}{self.stats['gil']} Gils 💰{RESET}")
        print(f" {VL} {WHITE}GOLD STOCK : {GOLD}{self.stats['gold']} Gold 🪙{RESET}")
        print(f" {VL} {WHITE}ENERGY     : {C3}{self.stats['st']} Stamina ⚡{RESET}")
        print(f" {PURPLE}╰{HL*35}{RESET}")
        print(f" {C1}{HL*20} CLAIM HISTORY {HL*25}{RESET}")
        print(f" {PURPLE}╭─{RESET} {C4}BOT STATUS: ACTIVE 🚀{RESET}")
        # Print last 15 logs to keep screen clean but show history
        for log in self.history[-15:]:
            print(log)

    def countdown(self, seconds):
        while seconds > 0:
            print(f"\r {PURPLE}│{RESET} {C3}⏳ Next Port Refresh: {seconds:02d}s {RESET}", end="")
            time.sleep(1)
            seconds -= 1
        print("\r" + " " * 50 + "\r", end="")

if __name__ == "__main__":
    clear(); banner()
    email_input = input(f"  {C1}➨ Enter User Email: {RESET}").strip()
    user_agent = input(f"  {C1}➨ Enter Your User-Agent: {RESET}").strip()
    bot = ConanEngine(email_input, user_agent)
    
    # Initial Auth
    params = {'email': bot.email, 'ref': "", 'referringsiteB': "conanbtc.com"}
    resp = bot.session.get(bot.base_url, params=params, headers=bot.headers)
    
    if "logout.php" in resp.text:
        bot.update_stats(resp.text)
        bot.log_history("Engine initialized successfully.", C4, "✅")
        
        while True:
            # 1. Action: Factory
            f_view = bot.session.get(bot.base_url, params={'view': 'collect', 'type': 'gold'}, headers=bot.headers)
            token = re.search(r'action=([A-Z0-9]+)', f_view.text) if f_view else None
            if token:
                bot.session.get(bot.base_url, params={'view': 'collect', 'type': 'gold', 'action': token.group(1)}, headers=bot.headers)
                bot.log_history("Factory: Gold Collected!", GOLD, "🪙")
            
            # 2. Action: Port (Trade)
            p_view = bot.session.get(bot.base_url, params={'view': 'port'}, headers=bot.headers).text
            if "action=claim" in p_view:
                bot.session.get(bot.base_url, params={'view': 'port', 'action': 'claim'}, headers=bot.headers)
                bot.log_history("Port: +20 Gils Claimed Successfully!", C4, "💰")
            
            if "action=deliver" in p_view:
                if bot.stats['gold'] >= 40:
                    d_view = bot.session.get(bot.base_url, params={'view': 'port', 'action': 'deliver'}, headers=bot.headers).text
                    if "tlevelup" in d_view: bot.session.get(bot.base_url, params={'view': 'tlevelup'}, headers=bot.headers)
                    bot.log_history("Port: Gold delivered, trade started.", C1, "🚢")
                else:
                    bot.log_history(f"Port: Waiting for gold ({bot.stats['gold']}/40).", C5, "⏳")

            # 3. Refresh Stats and UI
            final_page = bot.session.get(bot.base_url, headers=bot.headers)
            bot.update_stats(final_page.text)
            bot.refresh_ui()

            bot.countdown(120)
    else:
        print(f"\n  {C5}✖ Login Failed! Check Email/Network.{RESET}")