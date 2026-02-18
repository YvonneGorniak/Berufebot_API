# app/professions.py
import re
import requests
import asyncio

API_BASE = "https://rest.arbeitsagentur.de/infosysbub/bnet/pc/v1/berufe"
API_HEADERS = {
    "X-API-Key": "infosysbub-berufenet",
    "Accept": "application/json",
}

_profession_cache = {}
_title_cache = {}


def extract_ids_from_resp(resp):
    ids = []
    if not resp or not hasattr(resp, "source_nodes"):
        return []
    for sn in resp.source_nodes:
        meta = getattr(sn.node, "metadata", {})
        filename = meta.get("file_name") or meta.get("filename")
        if filename:
            match = re.findall(r"\d{3,}", filename)
            ids.extend(match)
    return list(dict.fromkeys(ids))


def _fetch_profession_json_sync(beruf_id: str):
    try:
        url = f"{API_BASE}/{beruf_id}"
        r = requests.get(url, headers=API_HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except:
        return None


def _normalize_profession_data(data):
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and (item.get("bilder") or item.get("darstellung")):
                return item
        for item in data:
            if isinstance(item, dict):
                return item
    return {}


def _extract_title(data):
    if not isinstance(data, dict):
        return None
    title = data.get("kurzBezeichnungNeutral")
    if isinstance(title, str) and title.strip():
        return title.strip()
    return None


async def fetch_titles_for_ids(ids):
    result = {}

    for pid in ids:
        if pid in _title_cache:
            result[pid] = _title_cache[pid]

    to_fetch = [pid for pid in ids if pid not in result]

    for pid in to_fetch:
        raw = _profession_cache.get(pid)
        if raw is None:
            raw = await asyncio.to_thread(_fetch_profession_json_sync, pid)
            if raw is not None:
                _profession_cache[pid] = raw
        if raw:
            data = _normalize_profession_data(raw)
            title = _extract_title(data)
            if title:
                _title_cache[pid] = title
                result[pid] = title

    return result