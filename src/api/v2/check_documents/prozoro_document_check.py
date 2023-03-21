import aiohttp


async def find_matching_documents(lot_id):
    matching_docs = []
    api_url = f"https://public.api.openprocurement.org/api/2.3/tenders/{lot_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status != 200:
                print(f"Помилка при запиті до API: {response.status}")
                return matching_docs

            lot_data = (await response.json())["data"]
            bids = lot_data.get("bids", [])

    if bids:
        for i, first_bid in enumerate(bids):
            for second_bid in bids[i + 1:]:
                docs1 = first_bid.get("documents", [])
                docs2 = second_bid.get("documents", [])

                for doc1 in docs1:
                    for doc2 in docs2:
                        if doc1["title"] == doc2["title"] and doc1["hash"] == doc2["hash"] \
                                and {first_bid['tenderers'][0]['name']} != {second_bid['tenderers'][0]['name']}:
                            matching_doc = {
                                "title": doc1['title'],
                                "bid_1_name": first_bid['tenderers'][0]['name'],
                                "bid_2_name": second_bid['tenderers'][0]['name'],
                                "lot_id": f"https://prozorro.gov.ua/tender/{lot_id}",
                                "doc_url": doc1['url'],
                                "tender": lot_id
                            }
                            if matching_doc not in matching_docs:
                                matching_docs.append(matching_doc)

    return matching_docs
