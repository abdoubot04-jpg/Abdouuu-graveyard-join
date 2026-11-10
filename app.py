# -*- coding: utf-8 -*-
"""
ABDOUUU VIP
- المستخدم: http://127.0.0.1:5000
- الأدمن:   http://127.0.0.1:5000/admin-abdouuu
- الباسورد: Abdouuu-bouchi5i
- ضع صورة باسم abdouuu.png في نفس مجلد الكود
"""

import os, json, time, random, socket, threading, secrets, string, logging, traceback
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, jsonify, render_template_string, send_from_directory

try:
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Cipher import AES
except Exception:
    AES = None; pad = None; unpad = None

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================== إعدادات ==================
ADMIN_PASSWORD   = "Abdouuu-bouchi5i"
ADMIN_PATH       = "admin-abdouuu"
INSTAGRAM_URL    = "https://instagram.com/zi.wr"
KEY_PREFIX       = "ABDOUUU-GRAVEYARD-VIP-"

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DB_DIR    = os.path.join(BASE_DIR, "data")
KEYS_DIR  = os.path.join(BASE_DIR, "keys")
DB_FILE   = os.path.join(DB_DIR, "database.json")

os.makedirs(DB_DIR,   exist_ok=True)
os.makedirs(KEYS_DIR, exist_ok=True)

xK, xV = b'Yg&tc%DEuh6%Zc^8', b'6oyZDr22E3ychjM%'

BOT_ACCOUNTS = [
    ("8425952805", "abdouuuvip_LCS1L_BY_DIVAN_SINGH_7F24W"),
    ("8425952766", "abdouuuvip_X495Y_BY_DIVAN_SINGH_JL43V"),
    ("8425953276", "abdouuuvip_NRCOG_BY_DIVAN_SINGH_R5VLT"),
    ("8425953299", "abdouuuvip_AVQ8D_BY_DIVAN_SINGH_LUIYM"),
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("ABDOUUU")

# ================== قاعدة البيانات ==================
_db_lock = threading.Lock()

def load_db():
    if not os.path.exists(DB_FILE):
        return {"keys": {}, "users": {}, "sessions": {}}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
        for k in ("keys", "users", "sessions"): db.setdefault(k, {})
        return db
    except Exception:
        return {"keys": {}, "users": {}, "sessions": {}}

def save_db(db):
    try:
        with _db_lock:
            tmp = DB_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
            os.replace(tmp, DB_FILE)
    except Exception as e: logger.error(f"DB save error: {e}")

def save_key_file(key, data):
    try:
        safe = key.replace("/", "_").replace("\\", "_")
        path = os.path.join(KEYS_DIR, f"{safe}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e: logger.error(f"save_key_file error: {e}")

def delete_key_file(key):
    try:
        safe = key.replace("/", "_").replace("\\", "_")
        path = os.path.join(KEYS_DIR, f"{safe}.json")
        if os.path.exists(path): os.remove(path)
    except Exception: pass

# ================== تشفير / بروتوكول ==================
def EnV_VaRiAnT(n):
    d = []
    while True:
        b = n & 0x7F; n >>= 7
        if n: b |= 0x80
        d.append(b)
        if not n: break
    return bytes(d)

def ProToBuF(Fields):
    p = bytearray()
    for f, v in Fields.items():
        if isinstance(v, bool):
            p.extend(EnV_VaRiAnT((f << 3) | 0)); p.extend(EnV_VaRiAnT(1 if v else 0))
        elif isinstance(v, int):
            p.extend(EnV_VaRiAnT((f << 3) | 0)); p.extend(EnV_VaRiAnT(v))
        elif isinstance(v, str):
            d = v.encode(); p.extend(EnV_VaRiAnT((f << 3) | 2)); p.extend(EnV_VaRiAnT(len(d))); p.extend(d)
        elif isinstance(v, (bytes, bytearray)):
            d = bytes(v); p.extend(EnV_VaRiAnT((f << 3) | 2)); p.extend(EnV_VaRiAnT(len(d))); p.extend(d)
    return bytes(p)

def Read_VaRiAnT(data, pos):
    result = 0; shift = 0
    while pos < len(data):
        b = data[pos]; pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80): break
        shift += 7
    return result, pos

def Parse_ProToBuF(data):
    fields = {}; pos = 0; n = len(data)
    while pos < n:
        try: key, pos = Read_VaRiAnT(data, pos)
        except Exception: break
        fn = key >> 3; wt = key & 0x07
        try:
            if wt == 0: val, pos = Read_VaRiAnT(data, pos)
            elif wt == 2:
                ln, pos = Read_VaRiAnT(data, pos); val = data[pos:pos + ln]; pos += ln
            elif wt == 5: val = data[pos:pos + 4]; pos += 4
            elif wt == 1: val = data[pos:pos + 8]; pos += 8
            else: break
        except Exception: break
        fields.setdefault(fn, []).append(val)
    return fields

def Ua():
    return random.choice(['4.0.18P6','4.1.0P3','4.2.1P8','5.0.1B2','5.2.0B1','5.3.0B1','5.4.0P1','5.5.2P3'])

def EnC_PacKeT(HeX, K, V):
    return AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(HeX), 16)).hex()

def DEc_PacKeT(HeX, K, V):
    return unpad(AES.new(K, AES.MODE_CBC, V).decrypt(bytes.fromhex(HeX)), 16).hex()

def EnC_Vr(N):
    H = []
    while True:
        b = N & 0x7F; N >>= 7
        if N: b |= 0x80
        H.append(b)
        if not N: break
    return bytes(H)

def CrEaTe_VarianT(field_number, value):
    return EnC_Vr((field_number << 3) | 0) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    ev = value.encode() if isinstance(value, str) else value
    return EnC_Vr((field_number << 3) | 2) + EnC_Vr(len(ev)) + ev

def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            packet.extend(CrEaTe_LenGTh(field, CrEaTe_ProTo(value)))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))
        elif isinstance(value, (str, bytes)):
            packet.extend(CrEaTe_LenGTh(field, value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    packet.extend(CrEaTe_LenGTh(field, CrEaTe_ProTo(item)))
    return packet

def DecodE_HeX(H):
    F = hex(H)[2:]
    return "0" + F if len(F) == 1 else F

def GeneRaTePk(Pk, N, K, V):
    PkEnc = EnC_PacKeT(Pk, K, V)
    _ = DecodE_HeX(int(len(PkEnc) // 2))
    if len(_) == 2: HeadEr = N + "000000"
    elif len(_) == 3: HeadEr = N + "00000"
    elif len(_) == 4: HeadEr = N + "0000"
    elif len(_) == 5: HeadEr = N + "000"
    else: HeadEr = N + "00000"
    return bytes.fromhex(HeadEr + _ + PkEnc)

def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        fd = {'wire_type': result.wire_type}
        if result.wire_type == "varint": fd['data'] = result.data
        if result.wire_type == "string": fd['data'] = result.data
        if result.wire_type == "bytes": fd['data'] = result.data
        elif result.wire_type == 'length_delimited':
            fd["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = fd
    return result_dict

def DeCode_PackEt(input_text):
    try:
        from protobuf_decoder.protobuf_decoder import Parser
        return json.dumps(Fix_PackEt(Parser().parse(input_text)))
    except Exception:
        return None

def Join_Team(team_code, key, iv):
    fields = {1: bytes.fromhex("01090a0b121619201d2729"), 2: 40, 3: bytes.fromhex("01090a0b121619201d2729"), 4: "w\\Z]", 6: 12, 7: bytes.fromhex("01090a0b121619201d2729"), 8: "1.132.9", 9: 6, 10: 2, 11: bytes.fromhex("01090a0b121619201d2729")}
    f = {1: 4, 2: {4: bytes.fromhex("01090a0b121619201d2729"), 5: str(team_code), 6: 6, 8: 1, 9: fields, 11: {1: "IDC1", 2: 99, 3: "ME"}, 13: "ar", 16: bytes.fromhex("374f521955"), 20: [{1: 3, 2: 360}, {1: 4, 2: 391}, {1: 5, 2: 156}, {1: 29, 2: 204}, {1: 22, 2: 118}, {1: 14, 2: 139}, {1: 21}], 27: {1: 2, 2: 4}}}
    return GeneRaTePk(CrEaTe_ProTo(f).hex(), "0519", key, iv)

def SendInv(bot_uid, uid, K, V):
    fields = {1: 33, 2: {1: int(uid), 2: "ME", 3: 1, 4: 1, 6: "yyt", 7: 330, 8: 1000, 9: 100, 10: "DZ", 12: 1, 13: int(uid), 16: 1, 17: {2: 159, 4: "y[WW", 6: 11, 8: "1.118.1", 9: 3, 10: 1}, 18: 306, 19: 18, 24: 902000306, 26: {}, 27: {1: 11, 2: int(bot_uid), 3: 999}, 28: {}, 31: {1: 1, 2: 32768}, 32: 32768, 34: {1: int(bot_uid), 2: 8, 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"}}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0519', K, V)

def Send_GhosTs(uid, name, sq, key, iv, lang="en"):
    fields = {1: 61, 2: {1: int(uid), 2: {1: int(uid), 2: 1159, 3: name, 5: 12, 6: 9999, 7: 1, 8: {2: 1, 3: 1}, 9: 3, 10: lang}, 3: sq}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0519', key, iv)

def ExiT(key, iv):
    fields = {1: 7, 2: {1: 0}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0519', key, iv)

def PyL(access_token, open_id):
    P = {}
    P[3] = time.strftime("%Y-%m-%d %H:%M:%S"); P[4]="free fire"; P[5]=1; P[7]="1.132.9"
    P[8]="Android OS 14 / API-34 (UP1A.231005.007/V816.0.15.0.UNQMIXM)"
    P[9]="Handheld"; P[10]="Grameenphone"; P[11]="CarrierDataNetwork"
    P[12]=1666; P[13]=750; P[14]="352"; P[15]="ARM64 FP ASIMD AES | 2400 | 8"
    P[16]=5563; P[17]="Mali-G57 MC2"
    P[18]="OpenGL ES 3.2 v1.r32p1-01eac0.0a0b917d9265b4c01be9925306306139"
    P[19]="Google|9cc73f7a-91f6-40f6-87ec-5b67e597eb8c"; P[20]="59.152.5.188"
    P[21]="en"; P[22]=open_id; P[23]="8"; P[24]="Handheld"
    P[25]="Xiaomi 2312DRAABI"; P[26]="BD"; P[29]=access_token; P[30]=1
    P[41]="Grameenphone"; P[42]="Cellular"
    P[57]="7428b253defc164018c604a1ebbfebdf"
    P[60]=109685; P[61]=58294; P[62]=797; P[63]=18000; P[64]=58818; P[65]=109685
    P[66]=58818; P[67]=109685; P[73]=2
    P[74]="/data/app/~~cqQgpdMykLQEM3odipXatw==/com.dts.freefireth-G6e5yOt1dtuXG5Ambhj18g==/lib/arm64"
    P[76]=1
    P[77]="b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~cqQgpdMykLQEM3odipXatw==/com.dts.freefireth-G6e5yOt1dtuXG5Ambhj18g==/base.apk"
    P[78]=3; P[79]=2; P[81]="64"; P[83]="2019121229"; P[85]=3; P[86]="OpenGLES2"
    P[87]=4095; P[88]=8
    P[89]=b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    P[90]="Dhaka"; P[91]="C"; P[92]=8043; P[93]="android"
    P[94]="KqsHT4XbSZhqerDNUhjbS3DxG/4+I62zQU2tZFJN91kBUICAlZ5yujshLKvjlk/KiShfKfis8EeB1PMhFHIodWPncZC4fCHYF3TcTwNj95aWY/S3"
    P[95]=111207; P[96]='{"cur_rate":[60,90,120],"support_etc2":false}'
    P[97]=1; P[98]=1; P[99]="4"; P[100]="4"; P[102]="GQ]        e"; P[103]=1
    P[104]=45174; P[105]=1
    P[106]="https://dl-bs.ggpolarbear.com/live/ABHotUpdates/|https://core-bs.ggpolarbear.com/live/ABHotUpdates/|a4332cb1c1a84e51dd77441e4856ed5a"
    P[107]="1.9393e7b8e53e8aeb"
    return AES.new(xK, AES.MODE_CBC, xV).encrypt(pad(ProToBuF(P), 16))

def Strip_MajorLogin_Prefix(body):
    if len(body) <= 64: return body
    try:
        if 8 in Parse_ProToBuF(body): return body
    except Exception: pass
    try:
        if 8 in Parse_ProToBuF(body[64:]): return body[64:]
    except Exception: pass
    return body[64:]

def GeT_AccEss(uid, password):
    url = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
    headers = {"User-Agent": Ua(), "Content-Type": "application/json; charset=utf-8"}
    try:
        R = requests.post(url, headers=headers, json={
            "client_id": 100067,
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_type": 2, "device_id": "", "password": password,
            "response_type": "token", "uid": int(uid)
        }, verify=False, timeout=15)
    except Exception: return None
    if R.status_code not in (200, 201): return None
    try: J = R.json()
    except Exception: return None
    if J.get("code") != 0: return None
    d = J.get("data", {})
    return {"access_token": d.get("access_token"), "open_id": d.get("open_id")}

def MajorLogin(Payload):
    url = "https://loginbp.ppmainecoonghj.com/MajorLogin"
    headers = {"User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)", "Accept": "*/*", "Accept-Encoding": "deflate, gzip", "X-GA-SV": str(int(time.time())), "Authorization": "Bearer ", "X-GA": "v1 1", "ReleaseVersion": "OB55", "Content-Type": "application/x-www-form-urlencoded", "X-Unity-Version": "2018.4.12f1"}
    try:
        R = requests.post(url, headers=headers, data=Payload, verify=False, timeout=15)
    except Exception: return None
    return R.content if R.status_code in (200, 201) and R.content else None

def GeTLoginDaTa(client_url, payload, jwt):
    url = f"{client_url}/GetLoginData"
    headers = {"User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)", "Accept": "*/*", "Accept-Encoding": "deflate, gzip", "X-GA-SV": str(int(time.time())), "Authorization": f"Bearer {jwt}", "X-GA": "v1 1", "ReleaseVersion": "OB55", "Content-Type": "application/x-www-form-urlencoded", "X-Unity-Version": "2018.4.12f1"}
    try:
        R = requests.post(url, headers=headers, data=payload, verify=False, timeout=15)
    except Exception: return None
    return R.content if R.status_code == 200 and R.content else None

def _gv(fields, n):
    v = fields.get(n)
    if v is None: return None
    if isinstance(v, list): v = v[0]
    return v

def ExtractMajorLogin(ml_resp):
    body = Strip_MajorLogin_Prefix(ml_resp)
    f = Parse_ProToBuF(body)
    jwt_b = _gv(f, 8); url_b = _gv(f, 10); ts_v = _gv(f, 21)
    key_b = _gv(f, 22); iv_b = _gv(f, 23); acct_v = _gv(f, 1)
    jwt = jwt_b.decode("utf-8", errors="ignore") if isinstance(jwt_b, bytes) else jwt_b
    url = url_b.decode("utf-8", errors="ignore") if isinstance(url_b, bytes) else url_b
    ts = ts_v if isinstance(ts_v, int) else None
    acct = acct_v if isinstance(acct_v, int) else None
    if not jwt or not isinstance(key_b, bytes) or not isinstance(iv_b, bytes): return None
    return {"jwt": jwt, "url": url, "ts": ts, "key": key_b, "iv": iv_b, "account_id": acct}

def BuildAuthToken(uid, jwt_str, ts, key, iv, mode="online"):
    ah = f"{int(uid):x}"
    if len(ah) > 16: raise ValueError("uid hex too long")
    ah = ah.zfill(16)
    enc = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(jwt_str.encode(), 16)).hex()
    th = f"{int(ts):x}"
    if len(th) % 2: th = "0" + th
    tsz = f"{len(enc)//2:02x}"
    pad_ = "00000" if mode == "chat" else "0000000000000"
    return f"9015{ah}{th}{pad_}{tsz}{enc}"

def _TuneSock(s):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    try:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
    except Exception: pass

def login_account(acc_uid, acc_pass):
    td = GeT_AccEss(acc_uid, acc_pass)
    if not td: return None
    at = td["access_token"]; oid = td["open_id"]
    if not at or not oid: return None
    lp = PyL(at, oid)
    ml = MajorLogin(lp)
    if not ml: return None
    ad = ExtractMajorLogin(ml)
    if not ad: return None
    jwt = ad["jwt"]; ts = ad["ts"]; key = ad["key"]; iv = ad["iv"]
    url = ad["url"] or "https://clientbp.ppmainecoonghj.com"
    if not url.startswith(("http://", "https://")): url = "https://" + url
    account_id = ad["account_id"]
    ld = GeTLoginDaTa(url, lp, jwt)
    if not ld: return None
    gl = Parse_ProToBuF(ld)
    def gv(n):
        v = gl.get(n)
        if v is None: return None
        if isinstance(v, list): v = v[0]
        return v
    def gs(n):
        v = gv(n); return v.decode() if isinstance(v, bytes) else v
    def gi(n):
        v = gv(n); return int(v) if isinstance(v, int) else None
    name = gs(4) or ""
    fa = gs(14); ia = gs(32)
    if not fa or not ia: return None
    ip, port = fa.split(":"); ip2, port2 = ia.split(":")
    if not account_id: account_id = gi(1) or gi(5) or 0
    return {"uid": account_id, "jwt": jwt, "ts": ts, "key": key, "iv": iv,
            "ip": ip, "port": port, "ip2": ip2, "port2": port2, "name": name, "token": at}

# ================== AttackJob ==================
class AttackJob:
    def __init__(self, session_id, user_id, team_code, accounts, status_cb=None):
        self.session_id = session_id
        self.user_id    = user_id
        self.team_code  = team_code
        self.accounts   = accounts
        self.stop_flag  = threading.Event()
        self.barrier    = threading.Barrier(max(1, len(accounts) * 2))
        self.threads    = []
        self.status_cb  = status_cb or (lambda *a, **k: None)
        self.anyone_in_team = False
        self.last_check     = time.time()
        self.started_at     = time.time()
        self.stop_reason    = None

    def _session(self, host, port, uid, jwt, ts, key, iv, mode, tag):
        s = None
        try:
            if self.stop_flag.is_set(): return
            s = socket.create_connection((host, int(port)), timeout=15)
            s.settimeout(20); _TuneSock(s)
            auth_hex = BuildAuthToken(uid, jwt, ts, key, iv, mode=mode)
            s.sendall(bytes.fromhex(auth_hex))
            try: self.barrier.wait(timeout=20)
            except Exception: pass
            if self.stop_flag.is_set():
                try: s.close()
                except Exception: pass
                return
            s.sendall(Join_Team(self.team_code, key, iv))
            s.settimeout(1.0)
            target_uid = None; squad_code = None
            start = time.time()
            while time.time() - start < 15:
                if self.stop_flag.is_set(): break
                try:
                    data = s.recv(65536)
                    if not data: break
                    hx = data.hex()
                    if hx.startswith('0500') and 100 < len(hx) < 5000:
                        try:
                            js = DeCode_PackEt(hx[10:])
                            if js:
                                pk = json.loads(js)
                                t_uid = pk.get('5', {}).get('data', {}).get('1', {}).get('data')
                                sq = pk.get('5', {}).get('data', {}).get('5', {}).get('data', {}).get('31', {}).get('data')
                                if not sq: sq = pk.get('5', {}).get('data', {}).get('31', {}).get('data')
                                if t_uid and sq: target_uid = t_uid; squad_code = sq; break
                        except Exception: pass
                except socket.timeout: pass
                except Exception: break
            if not target_uid or not squad_code:
                try: self.barrier.wait(timeout=10)
                except Exception: pass
                return
            self.anyone_in_team = True
            self.last_check = time.time()
            try: s.close()
            except Exception: pass
            if self.stop_flag.is_set(): return
            s = socket.create_connection((host, int(port)), timeout=15)
            s.settimeout(20); _TuneSock(s)
            s.sendall(bytes.fromhex(auth_hex)); time.sleep(0.3)
            s.sendall(SendInv(uid, target_uid, key, iv))
            for _ in range(3):
                s.sendall(Join_Team(self.team_code, key, iv)); time.sleep(0.02)
            try: self.barrier.wait(timeout=20)
            except Exception: pass
            if self.stop_flag.is_set(): return
            gp = Send_GhosTs(int(target_uid), "[C][B][FF00FF]بوشي؁خي̶", squad_code, key, iv)
            for _ in range(3):
                if self.stop_flag.is_set(): break
                try: s.sendall(gp)
                except Exception: break
                time.sleep(0.01)
            try: self.barrier.wait(timeout=20)
            except Exception: pass
            if not self.stop_flag.is_set():
                try: s.sendall(ExiT(key, iv))
                except Exception: pass
            time.sleep(0.3)
        except Exception as e: pass
        finally:
            try:
                if s: s.close()
            except Exception: pass

    def _loop(self, host, port, uid, jwt, ts, key, iv, mode, tag):
        while not self.stop_flag.is_set():
            try: self._session(host, port, uid, jwt, ts, key, iv, mode, tag)
            except Exception: pass
            for _ in range(10):
                if self.stop_flag.is_set(): return
                time.sleep(0.1)

    def _watchdog(self):
        time.sleep(20)
        while not self.stop_flag.is_set():
            time.sleep(5)
            if not self.anyone_in_team and (time.time() - self.last_check) > 60:
                self.stop_reason = "empty_team"
                self.stop()
                try: self.status_cb(self.session_id, "stopped_empty")
                except Exception: pass
                return
            self.anyone_in_team = False

    def start(self):
        for acc in self.accounts:
            t1 = threading.Thread(target=self._loop, args=(acc["ip"], acc["port"], acc["uid"], acc["jwt"], acc["ts"], acc["key"], acc["iv"], "online", "ChaT"), daemon=True)
            t2 = threading.Thread(target=self._loop, args=(acc["ip2"], acc["port2"], acc["uid"], acc["jwt"], acc["ts"], acc["key"], acc["iv"], "chat", "OnLinE"), daemon=True)
            t1.start(); t2.start()
            self.threads.extend([t1, t2])
        wd = threading.Thread(target=self._watchdog, daemon=True)
        wd.start(); self.threads.append(wd)

    def stop(self, reason=None):
        if reason: self.stop_reason = reason
        self.stop_flag.set()

ACTIVE_ATTACKS = {}
_attack_lock   = threading.Lock()

def stop_session(sid, reason="manual"):
    with _attack_lock:
        job = ACTIVE_ATTACKS.get(sid)
        if job:
            job.stop(reason)
            del ACTIVE_ATTACKS[sid]
            return True
    return False

def get_user_sessions(user_id):
    res = []
    with _attack_lock:
        for sid, job in ACTIVE_ATTACKS.items():
            if job.user_id == user_id: res.append(job)
    return res

# ================== Flask ==================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "abdouuu-super-secret-key-2024")

def now(): return time.time()
def is_admin(): return session.get("admin_ok") is True

def key_is_valid(key):
    db = load_db()
    kd = db["keys"].get(key)
    if not kd: return False, "مفتاح غير صالح"
    if kd.get("disabled"): return False, "المفتاح معطل"
    if now() > kd.get("expires_at", 0): return False, "المفتاح منتهي الصلاحية"
    return True, "ok"

def get_session_id(): return session.get("user_id", "guest")
def get_user_key(uid):
    u = load_db()["users"].get(str(uid))
    return u.get("key") if u else None

def on_job_status(sid, status):
    try:
        db = load_db()
        if sid in db["sessions"]:
            db["sessions"][sid]["status"] = status
            db["sessions"][sid]["ended_at"] = now()
            save_db(db)
    except Exception: pass

# ================== HTML (تصميم الصورة الجديد) ==================
BASE_HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>ABDOUUU</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #000000;
    --panel: #0a0a0a;
    --red: #ff1a1a;
    --red-glow: rgba(255, 26, 26, 0.4);
    --text-muted: #888888;
    --border: #222222;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Oswald', sans-serif; }
  body {
    background-color: var(--bg);
    color: #ffffff;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    overflow-x: hidden;
  }
  .container {
    width: 100%;
    max-width: 420px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-top: 40px;
  }
  /* Avatar */
  .avatar-container {
    position: relative;
    width: 160px;
    height: 160px;
    margin-bottom: 30px;
  }
  .avatar-img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--red);
    box-shadow: 0 0 30px var(--red-glow), inset 0 0 10px rgba(0,0,0,0.8);
    background: #111;
  }
  /* Text */
  .subtitle {
    color: var(--text-muted);
    font-size: 13px;
    letter-spacing: 1px;
    line-height: 1.6;
    margin-bottom: 40px;
    max-width: 320px;
    font-weight: 500;
  }
  /* Form */
  .form-group {
    width: 100%;
    margin-bottom: 20px;
    text-align: right;
  }
  .form-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #ccc;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
  }
  .red-square {
    width: 8px;
    height: 8px;
    background-color: var(--red);
    display: inline-block;
  }
  .input-wrapper {
    display: flex;
    width: 100%;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
    transition: border-color 0.2s;
    direction: ltr;
  }
  .input-wrapper:focus-within {
    border-color: #444;
  }
  .input-field {
    flex: 1;
    background: transparent;
    border: none;
    padding: 16px;
    color: #fff;
    font-size: 15px;
    outline: none;
    font-family: 'Oswald', sans-serif;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .input-field::placeholder {
    color: #333;
  }
  .btn-paste {
    background: transparent;
    border: none;
    border-left: 1px solid var(--border);
    color: #fff;
    font-size: 12px;
    padding: 0 20px;
    cursor: pointer;
    letter-spacing: 1px;
    font-weight: 700;
    transition: background 0.2s;
  }
  .btn-paste:hover {
    background: rgba(255,255,255,0.05);
  }
  /* Main Button */
  .btn-primary {
    width: 100%;
    background: var(--red);
    color: #fff;
    border: none;
    padding: 18px;
    font-size: 22px;
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 2px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    margin-bottom: 15px;
    clip-path: polygon(0 0, 100% 0, 100% 100%, 4% 100%);
    transition: background 0.2s;
  }
  .btn-primary:hover {
    background: #ff3333;
  }
  /* Contact Button */
  .btn-contact {
    width: 100%;
    background: var(--panel);
    color: #fff;
    border: 1px solid var(--border);
    padding: 14px;
    font-size: 13px;
    font-family: 'Oswald', sans-serif;
    letter-spacing: 1px;
    cursor: pointer;
    text-decoration: none;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    transition: background 0.2s;
    margin-bottom: 30px;
    font-weight: 700;
    direction: ltr;
  }
  .btn-contact:hover {
    background: #151515;
  }
  /* Footer */
  .footer-text {
    color: var(--text-muted);
    font-size: 12px;
    line-height: 1.8;
    letter-spacing: 0.5px;
    max-width: 300px;
  }
  .footer-text span {
    color: #fff;
  }
  .btn-buy {
    display: inline-block;
    margin-top: 10px;
    color: var(--red);
    font-weight: bold;
    text-decoration: none;
    border-bottom: 1px solid var(--red);
    padding-bottom: 2px;
    transition: color 0.2s;
  }
  .btn-buy:hover {
    color: #ff5555;
  }
  /* Messages */
  .msg {
    width: 100%;
    padding: 12px;
    font-size: 13px;
    margin-bottom: 15px;
    text-align: center;
    border-radius: 4px;
  }
  .msg.err { background: rgba(255,0,0,0.1); border: 1px solid #ff3333; color: #ff6666; }
  .msg.ok  { background: rgba(0,255,0,0.1); border: 1px solid #00cc66; color: #66ff99; }
</style>
</head>
<body>
<div class="container">
  <!-- الصورة الرمزية -->
  <div class="avatar-container">
    <!-- تم ربط الصورة باسم abdouuu.png -->
    <img src="/abdouuu.png" alt="Avatar" class="avatar-img">
  </div>

  <div class="subtitle">
    لا حساب. لا كلمة مرور. فقط مفتاحك.
  </div>

  {% if msg %}<div class="msg {{ msg_type }}">{{ msg }}</div>{% endif %}

  <form method="POST" action="/activate" style="width:100%;">
    <div class="form-group">
      <div class="form-label">
        <span class="red-square"></span>
        مفتاح الدخول
      </div>
      <div class="input-wrapper">
        <button type="button" class="btn-paste" onclick="pasteKey()">لصق</button>
        <input type="text" name="key" id="keyInput" class="input-field" placeholder="ABDOUUU-XXXX-XXXX-XXXX" required autofocus>
      </div>
    </div>

    <button type="submit" class="btn-primary">OUVRIR</button>
  </form>

  <a href="{{ instagram_url }}" target="_blank" class="btn-contact">
    تواصل مع المطور · @zi.wr ↗
  </a>

  <div class="footer-text">
    ليس لديك مفتاح؟ تواصل مع البائع.<br>
    <span>الوقت يبدأ من لحظة الاتصال.</span><br>
    <a href="{{ instagram_url }}" target="_blank" class="btn-buy">BUY KEY</a>
  </div>
</div>

<script>
  function pasteKey() {
    navigator.clipboard.readText().then(text => {
      document.getElementById('keyInput').value = text.trim();
    }).catch(err => {
      alert("يرجى السماح بالوصول إلى الحافظة.");
    });
  }
</script>
</body>
</html>
"""

# ================== Routes: المستخدم ==================
@app.route("/", methods=["GET"])
def index():
    if session.get("user_id") and get_user_key(session.get("user_id")):
        return redirect(url_for("dashboard"))
    msg = session.pop("msg", None)
    mt  = session.pop("msg_type", "info")
    
    return render_template_string(
        BASE_HTML, msg=msg, msg_type=mt, instagram_url=INSTAGRAM_URL
    )

# مسار لعرض صورة المستخدم
@app.route("/abdouuu.png")
def serve_avatar():
    return send_from_directory(BASE_DIR, "abdouuu.png")

@app.route("/activate", methods=["POST"])
def activate():
    key = (request.form.get("key") or "").strip()
    if not key:
        session["msg"] = "الرجاء إدخال المفتاح."
        session["msg_type"] = "err"
        return redirect(url_for("index"))
    db = load_db()
    ok, msg = key_is_valid(key)
    if not ok:
        session["msg"] = msg; session["msg_type"] = "err"
        return redirect(url_for("index"))

    if "user_id" not in session:
        session["user_id"] = "u_" + secrets.token_hex(6)
    uid = session["user_id"]

    kd = db["keys"][key]
    used_by = kd.setdefault("used_by", [])
    if uid not in used_by:
        if len(used_by) >= kd.get("max_users", 1):
            session["msg"] = "هذا المفتاح مستخدم من قبل شخص آخر."
            session["msg_type"] = "err"
            return redirect(url_for("index"))
        used_by.append(uid)
    db["users"][uid] = {"key": key, "activated_at": now()}
    save_db(db)
    save_key_file(key, kd)

    session["msg"] = "✅ تم تفعيل المفتاح بنجاح."
    session["msg_type"] = "ok"
    return redirect(url_for("dashboard"))

@app.route("/dashboard", methods=["GET"])
def dashboard():
    uid = session.get("user_id")
    if not uid:
        session["msg"] = "الرجاء تسجيل الدخول."
        session["msg_type"] = "err"
        return redirect(url_for("index"))
    db = load_db()
    u = db["users"].get(uid)
    if not u:
        session["msg"] = "الحساب غير موجود."
        session["msg_type"] = "err"
        return redirect(url_for("index"))
    key = u.get("key")
    ok, msg = key_is_valid(key) if key else (False, "لا يوجد مفتاح")
    if not ok:
        session["msg"] = msg; session["msg_type"] = "err"
        return redirect(url_for("index"))
    kd = db["keys"][key]
    exp_date = time.strftime("%Y-%m-%d", time.localtime(kd.get("expires_at", 0)))
    key_short = key[:10] + "..." + key[-4:]

    user_jobs = get_user_sessions(uid)
    sessions_list = []
    for job in user_jobs:
        sessions_list.append({
            "sid":        job.session_id,
            "sid_short":  job.session_id[:14] + "…" if len(job.session_id) > 15 else job.session_id,
            "team_code":  job.team_code,
            "accounts":   len(job.accounts),
            "started":    time.strftime("%H:%M:%S", time.localtime(job.started_at)),
        })

    msg = session.pop("msg", None)
    mt  = session.pop("msg_type", "info")
    
    # صفحة الداشبورد
    dash_html = """
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>لوحة التحكم - ABDOUUU</title>
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap" rel="stylesheet">
    <style>
      body { background: #000; color: #fff; font-family: 'Oswald', sans-serif; text-align: right; padding: 20px; }
      .card { background: #0a0a0a; border: 1px solid #333; border-radius: 8px; padding: 20px; max-width: 500px; margin: 0 auto; }
      h2 { color: #ff1a1a; text-align: center; }
      input[type=text] { width: 100%; padding: 12px; background: #000; border: 1px solid #444; color: #fff; margin: 10px 0; font-size: 16px; font-family: inherit; }
      button { width: 100%; padding: 14px; background: #ff1a1a; color: #fff; border: none; cursor: pointer; font-size: 16px; font-weight: bold; margin-top: 10px; font-family: inherit; }
      button:hover { background: #ff3333; }
      .session-item { background: rgba(255,255,255,0.05); border: 1px solid #333; padding: 12px; margin: 10px 0; border-radius: 6px; }
      .btn-stop { background: #444; padding: 8px; font-size: 14px; width: auto; margin-top: 8px; }
      .btn-stop:hover { background: #ff1a1a; }
      .stat { color: #888; font-size: 14px; margin-bottom: 20px; text-align: center; }
      .msg { padding: 10px; margin-bottom: 15px; text-align: center; border-radius: 4px; font-size: 14px; }
      .msg.err { background: rgba(255,0,0,0.1); border: 1px solid #ff3333; }
      .msg.ok { background: rgba(0,255,0,0.1); border: 1px solid #00cc66; }
      .msg.info { background: rgba(255,255,255,0.1); border: 1px solid #666; }
      a { color: #ff1a1a; text-decoration: none; font-size: 14px; display: inline-block; margin: 10px; }
    </style>
    </head>
    <body>
      <div class="card">
        <h2>⚔️ لوحة التحكم</h2>
        <div class="stat">
          المعرف: <b>{{ user_id }}</b> | المفتاح: <b>{{ key_short }}</b><br>
          ينتهي في: <b>{{ exp_date }}</b>
        </div>
        
        {% if msg %}<div class="msg {{ msg_type }}">{{ msg }}</div>{% endif %}

        <form method="post" action="/attack">
          <label>كود الفريق</label>
          <input type="text" name="team_code" placeholder="أدخل كود الفريق" required>
          <button type="submit">🚀 بدء الجلسة</button>
        </form>

        <h3 style="margin-top:20px; color:#ff1a1a;">الجلسات النشطة ({{ sessions|length }})</h3>
        {% for s in sessions %}
          <div class="session-item">
            <div>🎯 الفريق: <b>{{ s.team_code }}</b> | 🤖 {{ s.accounts }} بوت</div>
            <div style="font-size:12px; color:#888;">بدأت في: {{ s.started }}</div>
            <form method="post" action="/stop_session" style="display:inline;">
              <input type="hidden" name="sid" value="{{ s.sid }}">
              <button type="submit" class="btn-stop">⛔ إيقاف</button>
            </form>
          </div>
        {% else %}
          <div class="msg info">لا توجد جلسات نشطة.</div>
        {% endfor %}

        {% if sessions %}
        <form method="post" action="/stop_all">
          <button type="submit" style="background:#333; margin-top:15px;">⛔ إيقاف الكل</button>
        </form>
        {% endif %}
        
        <div style="text-align:center; margin-top:20px;">
          <a href="/dashboard">🔄 تحديث</a>
          <a href="/logout">🚪 تسجيل الخروج</a>
        </div>
      </div>
    </body>
    </html>
    """
    
    return render_template_string(
        dash_html, msg=msg, msg_type=mt, user_id=uid,
        key_short=key_short, exp_date=exp_date,
        sessions=sessions_list
    )

@app.route("/attack", methods=["POST"])
def attack():
    uid = session.get("user_id")
    if not uid: return redirect(url_for("index"))
    key = get_user_key(uid)
    ok, msg = key_is_valid(key) if key else (False, "لا يوجد مفتاح")
    if not ok:
        session["msg"] = msg; session["msg_type"] = "err"
        return redirect(url_for("index"))

    team_code = (request.form.get("team_code") or "").strip()
    if not team_code:
        session["msg"] = "أدخل كود الفريق."
        session["msg_type"] = "err"
        return redirect(url_for("dashboard"))

    existing = get_user_sessions(uid)
    for j in existing:
        if j.team_code == team_code:
            session["msg"] = "لديك جلسة نشطة بالفعل على هذا الفريق."
            session["msg_type"] = "err"
            return redirect(url_for("dashboard"))

    accounts = []
    for a_uid, a_pass in BOT_ACCOUNTS:
        try:
            res = login_account(a_uid, a_pass)
            if res: accounts.append(res)
        except Exception: pass
    if not accounts:
        session["msg"] = "فشل الاتصال بالحسابات. حاول لاحقاً."
        session["msg_type"] = "err"
        return redirect(url_for("dashboard"))

    sid = f"{uid}_{int(time.time()*1000)}_{secrets.token_hex(3)}"
    job = AttackJob(sid, uid, team_code, accounts, status_cb=on_job_status)
    with _attack_lock:
        ACTIVE_ATTACKS[sid] = job
    job.start()

    db = load_db()
    db["sessions"][sid] = {"user_id": uid, "team_code": team_code, "started_at": now(), "status": "running", "accounts": len(accounts)}
    save_db(db)
    session["msg"] = f"✅ بدأت الجلسة على الفريق {team_code}"
    session["msg_type"] = "ok"
    return redirect(url_for("dashboard"))

@app.route("/stop_session", methods=["POST"])
def stop_specific_session():
    uid = session.get("user_id")
    if not uid: return redirect(url_for("index"))
    sid = request.form.get("sid")
    if not sid: return redirect(url_for("dashboard"))

    with _attack_lock:
        job = ACTIVE_ATTACKS.get(sid)
    if not job or job.user_id != uid:
        session["msg"] = "الجلسة غير موجودة."
        session["msg_type"] = "err"
        return redirect(url_for("dashboard"))

    if stop_session(sid, reason="manual"):
        session["msg"] = f"✅ تم إيقاف الجلسة."
        session["msg_type"] = "ok"
    return redirect(url_for("dashboard"))

@app.route("/stop_all", methods=["POST"])
def stop_all_sessions():
    uid = session.get("user_id")
    if not uid: return redirect(url_for("index"))
    user_jobs = get_user_sessions(uid)
    for job in user_jobs:
        stop_session(job.session_id, reason="manual")
    session["msg"] = "✅ تم إيقاف جميع الجلسات."
    session["msg_type"] = "ok"
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    uid = session.get("user_id")
    if uid:
        for j in get_user_sessions(uid):
            stop_session(j.session_id, reason="logout")
    session.clear()
    return redirect(url_for("index"))

# ================== Routes: الأدمن (تم تعديل التصميم والنسخ) ==================
@app.route(f"/{ADMIN_PATH}", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        pw = (request.form.get("password") or "").strip()
        if pw == ADMIN_PASSWORD:
            session["admin_ok"] = True
            session["admin_logged_at"] = now()
            return redirect(url_for("admin_panel"))
        return "كلمة المرور غير صحيحة."
    if is_admin():
        return redirect(url_for("admin_panel"))
    
    admin_html = """
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
    <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>دخول الأدمن</title>
    <style>
      body { background: #000; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
      form { background: #0a0a0a; padding: 30px; border: 1px solid #333; border-radius: 8px; text-align: center; }
      input { padding: 12px; font-size: 16px; margin-bottom: 15px; width: 100%; background: #000; border: 1px solid #444; color: #fff; }
      button { padding: 12px; width: 100%; background: #ff1a1a; color: #fff; border: none; font-size: 16px; cursor: pointer; }
    </style>
    </head>
    <body>
      <form method="POST" action="/{{ admin_path }}">
        <h2>👑 دخول الأدمن</h2>
        <input type="password" name="password" placeholder="كلمة المرور" required>
        <button type="submit">تسجيل الدخول</button>
      </form>
    </body>
    </html>
    """
    return render_template_string(admin_html, admin_path=ADMIN_PATH)

@app.route(f"/{ADMIN_PATH}/panel", methods=["GET"])
def admin_panel():
    if not is_admin(): return redirect(url_for("admin_login"))
    db = load_db()
    keys_list = []
    for k, v in db["keys"].items():
        days_left = max(0, int((v.get("expires_at", 0) - now()) // 86400))
        keys_list.append({
            "key": k, "days_left": days_left, "used": len(v.get("used_by", [])),
            "max_users": v.get("max_users", 1), "exp_date": time.strftime("%Y-%m-%d", time.localtime(v.get("expires_at", 0))),
            "disabled": v.get("disabled", False)
        })
    keys_list.sort(key=lambda x: x["exp_date"], reverse=True)
    
    admin_panel_html = """
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
    <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>لوحة الأدمن - ABDOUUU</title>
    <style>
      body { background: #000; color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; }
      .container { max-width: 800px; margin: auto; }
      h2 { color: #ff1a1a; text-align: center; border-bottom: 1px solid #333; padding-bottom: 15px; }
      .stats { display: flex; gap: 15px; justify-content: center; margin-bottom: 30px; }
      .stat-box { background: #0a0a0a; border: 1px solid #333; padding: 15px 25px; border-radius: 8px; text-align: center; }
      .stat-box h3 { margin: 0 0 5px 0; color: #888; font-size: 14px; }
      .stat-box p { margin: 0; font-size: 24px; font-weight: bold; color: #ff1a1a; }
      .form-create { background: #0a0a0a; padding: 20px; border-radius: 8px; border: 1px solid #333; margin-bottom: 30px; display: flex; gap: 10px; align-items: flex-end; flex-wrap: wrap; }
      .form-create input { padding: 10px; background: #000; border: 1px solid #444; color: #fff; border-radius: 4px; width: 100px; }
      .form-create button { padding: 10px 20px; background: #ff1a1a; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
      .key-list { display: flex; flex-direction: column; gap: 10px; }
      .key-card { background: #0a0a0a; border: 1px solid #333; border-radius: 8px; padding: 15px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; }
      .key-info { display: flex; flex-direction: column; gap: 5px; direction: ltr; text-align: left; }
      .key-code { font-family: monospace; font-size: 16px; color: #fff; font-weight: bold; }
      .key-meta { font-size: 12px; color: #888; display: flex; gap: 10px; }
      .key-actions { display: flex; gap: 8px; margin-top: 10px; }
      .key-actions button { padding: 8px 15px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
      .btn-copy { background: #00cc66; color: #fff; }
      .btn-delete { background: #333; color: #fff; }
      .btn-delete:hover { background: #ff1a1a; }
      .toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #00cc66; color: #fff; padding: 10px 20px; border-radius: 5px; display: none; z-index: 100; }
      .logout { display: block; text-align: center; color: #ff1a1a; text-decoration: none; margin-top: 30px; }
    </style>
    </head>
    <body>
      <div class="container">
        <h2>👑 لوحة تحكم الأدمن</h2>
        
        <div class="stats">
          <div class="stat-box">
            <h3>إجمالي المفاتيح</h3>
            <p>{{ keys_count }}</p>
          </div>
        </div>

        <form method="post" action="/{{ admin_path }}/create_key" class="form-create">
          <div>
            <label>الأيام</label><br>
            <input type="number" name="days" value="30" min="1">
          </div>
          <div>
            <label>عدد المستخدمين</label><br>
            <input type="number" name="max_users" value="1" min="1">
          </div>
          <button type="submit">➕ إنشاء مفتاح</button>
        </form>

        <h3 style="color:#fff;">قائمة المفاتيح ({{ keys_count }})</h3>
        <div class="key-list">
          {% for k in keys %}
          <div class="key-card">
            <div class="key-info">
              <span class="key-code">{{ k.key }}</span>
              <div class="key-meta">
                <span>⏳ {{ k.days_left }} يوم</span>
                <span>👥 {{ k.used }}/{{ k.max_users }}</span>
                <span>📅 {{ k.exp_date }}</span>
              </div>
            </div>
            <div class="key-actions">
              <button class="btn-copy" onclick="copyText('{{ k.key }}')">📋 نسخ</button>
              <form method="post" action="/{{ admin_path }}/delete_key" style="display:inline;">
                <input type="hidden" name="key" value="{{ k.key }}">
                <button type="submit" class="btn-delete">🗑️ حذف</button>
              </form>
            </div>
          </div>
          {% else %}
          <p style="text-align:center; color:#666;">لا توجد مفاتيح بعد.</p>
          {% endfor %}
        </div>

        <a href="/{{ admin_path }}/logout" class="logout">🚪 تسجيل الخروج</a>
      </div>

      <div id="toast" class="toast">✅ تم النسخ!</div>
      <script>
        function copyText(text) {
          if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(() => {
              showToast();
            }).catch(err => fallbackCopy(text));
          } else {
            fallbackCopy(text);
          }
        }
        function fallbackCopy(text) {
          const ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand('copy'); showToast(); } catch(e) { alert('فشل النسخ'); }
          document.body.removeChild(ta);
        }
        function showToast() {
          const t = document.getElementById('toast');
          t.style.display = 'block';
          setTimeout(() => t.style.display = 'none', 2000);
        }
      </script>
    </body>
    </html>
    """
    return render_template_string(admin_panel_html, keys=keys_list, keys_count=len(keys_list), admin_path=ADMIN_PATH)

@app.route(f"/{ADMIN_PATH}/create_key", methods=["POST"])
def admin_create_key():
    if not is_admin(): return redirect(url_for("admin_login"))
    try:
        days = int(request.form.get("days", 30))
        max_users = int(request.form.get("max_users", 1))
    except: return redirect(url_for("admin_panel"))
    
    rand = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    key  = KEY_PREFIX + rand
    data = {"created_at": now(), "expires_at": now() + days * 86400, "max_users": max_users, "used_by": [], "disabled": False}
    db = load_db()
    db["keys"][key] = data
    save_db(db)
    save_key_file(key, data)
    return redirect(url_for("admin_panel"))

@app.route(f"/{ADMIN_PATH}/delete_key", methods=["POST"])
def admin_delete_key():
    if not is_admin(): return redirect(url_for("admin_login"))
    key = request.form.get("key")
    db = load_db()
    if key in db["keys"]:
        del db["keys"][key]
        save_db(db)
        delete_key_file(key)
    return redirect(url_for("admin_panel"))

@app.route(f"/{ADMIN_PATH}/logout")
def admin_logout():
    session.pop("admin_ok", None)
    return redirect(url_for("index"))

# ================== Main ==================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print("=" * 50)
    print("   ABDOUUU VIP - Web Panel")
    print("=" * 50)
    print(f"   المستخدم: http://127.0.0.1:{port}")
    print(f"   الأدمن:   http://127.0.0.1:{port}/{ADMIN_PATH}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)