import re
import time
from typing import Any
from urllib.parse import urljoin, urlparse, parse_qs

import httpx
from bs4 import BeautifulSoup


class LZTMarketError(Exception):
    pass


class LZTMarketClient:
    """Placeholder-клиент LZT Market. Нужно подстроить endpoint'ы под актуальную документацию."""

    def __init__(
        self,
        token: str,
        base_url: str = "https://lzt.market",
        proxy: str | None = None,
        user_agent: str | None = None,
        timeout: int = 30
    ):
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": user_agent or (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/html, application/xhtml+xml",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.proxies = {"http://": proxy, "https://": proxy} if proxy else None

    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        data: dict | None = None,
        json_payload: dict | None = None,
        headers: dict | None = None
    ) -> dict | str:
        url = urljoin(self.base_url + "/", path.lstrip("/"))
        req_headers = dict(self.headers)
        if headers:
            req_headers.update(headers)

        with httpx.Client(
            proxies=self.proxies,
            timeout=self.timeout,
            follow_redirects=True
        ) as client:
            if method.lower() == "get":
                r = client.get(url, params=params, headers=req_headers)
            elif method.lower() == "post":
                r = client.post(
                    url,
                    data=data,
                    json=json_payload,
                    headers=req_headers
                )
            else:
                raise LZTMarketError(f"Unsupported method {method}")

        if r.status_code == 401:
            raise LZTMarketError("Unauthorized. Check LZT token.")

        try:
            return r.json()
        except Exception:
            return r.text

    def get_me(self) -> dict:
        """Проверка токена и получение баланса."""
        return self._request("get", "/api/")

    def get_balance(self) -> float | int:
        data = self.get_me()
        if isinstance(data, dict):
            return data.get("balance", 0)
        return 0

    def _extract_price(self, text: str) -> int | None:
        if not text:
            return None
        nums = re.findall(r"[\d\s]+", text.replace(" ", ""))
        if nums:
            try:
                return int(nums[0])
            except ValueError:
                pass
        return None

    def search_accounts(
        self,
        search_url: str,
        max_price: int | None = None,
        max_pages: int = 3,
        delay: float = 2.0,
        blacklist_items: list | None = None,
        blacklist_sellers: list | None = None
    ) -> list[dict]:
        """
        Парсит выдачу LZT Market по URL категории/поиска.
        Возвращает список словарей с ключами id, price, seller, title, link.
        """
        blacklist_items = set(blacklist_items or [])
        blacklist_sellers = set(blacklist_sellers or [])
        results = []

        parsed = urlparse(search_url)
        base_path = parsed.path
        qs = parse_qs(parsed.query)

        for page in range(1, max_pages + 1):
            params = {k: v[0] for k, v in qs.items()}
            params["page"] = page

            html = self._request("get", base_path, params=params)
            if not isinstance(html, str):
                break

            soup = BeautifulSoup(html, "lxml")
            items = soup.select(".market-index-item") or soup.select("[data-item-id]") or soup.select(".item")

            if not items:
                items = soup.find_all("div", class_=re.compile("item|lot|account"))

            for item in items:
                try:
                    link_tag = item.find("a", href=True)
                    if not link_tag:
                        continue
                    href = link_tag["href"]
                    if href.startswith("/"):
                        href = self.base_url + href

                    item_id_match = re.search(r"/(\d+)/", href)
                    item_id = item_id_match.group(1) if item_id_match else href

                    if item_id in blacklist_items:
                        continue

                    title = item.get_text(strip=True, separator=" ")[:120]
                    price = self._extract_price(item.get_text())

                    seller_tag = item.select_one(".seller") or item.select_one(".username") or item.find("a", href=re.compile(r"/members/"))
                    seller = seller_tag.get_text(strip=True) if seller_tag else "unknown"
                    if seller in blacklist_sellers:
                        continue

                    if max_price is not None and price is not None and price > max_price:
                        continue

                    results.append({
                        "id": item_id,
                        "title": title,
                        "price": price,
                        "seller": seller,
                        "link": href
                    })
                except Exception:
                    continue

            if len(items) == 0:
                break

            if page < max_pages:
                time.sleep(delay)

        return results

    def buy_account(self, item_id: str | int) -> dict[str, Any]:
        """
        Покупка товара. Endpoint может отличаться.
        Возвращает данные купленного аккаунта.
        """
        result = self._request(
            "post",
            f"/api/items/{item_id}/buy/",
            data={"currency": "rub"}
        )
        if isinstance(result, dict) and not result.get("ok", True):
            raise LZTMarketError(result.get("error") or str(result))
        return result if isinstance(result, dict) else {"raw": result}

    def get_purchase_data(self, purchase_id: str | int) -> dict[str, Any]:
        """Получение данных купленного товара (логин/пароль)."""
        result = self._request(
            "get",
            f"/api/items/{purchase_id}/data/"
        )
        return result if isinstance(result, dict) else {"raw": result}

    def get_email_password(self, purchase_id: str | int) -> str | None:
        """Получение пароля от временной почты, если поддерживается."""
        if not purchase_id:
            return None
        result = self._request(
            "get",
            f"/api/items/{purchase_id}/email_password/"
        )
        if isinstance(result, dict):
            return result.get("password") or result.get("email_password")
        return None
