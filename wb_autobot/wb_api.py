import aiohttp

API_BASE = "https://suppliers-api.wildberries.ru"

async def get_available_slots(token):
    headers = {"Authorization": token}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/api/v2/delivery/service/intervals", headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"WB API error {resp.status}")
            return await resp.json()

async def get_available_draft_supplies(token):
    headers = {"Authorization": token}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/api/v2/supplies", headers=headers) as resp:
            if resp.status != 200:
                raise Exception("Не удалось получить список поставок")
            supplies = await resp.json()
            return [s for s in supplies if s['status'] == 'draft']

async def book_slot(token, slot, supply_id):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    body = {
        "date": slot['date'],
        "warehouse": slot['warehouse'],
        "type": slot['type']
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(f"{API_BASE}/api/v2/supplies/{supply_id}/date", headers=headers, json=body) as resp:
            if resp.status != 200:
                raise Exception("Не удалось забронировать слот")
            return await resp.json()