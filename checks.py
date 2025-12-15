import morex.logging as logging
import functions as fns


async def check_item_names(langs=None, serious=False):
    items = await fns.itemsinfo()
    if langs is None:
        langs = ["en", "pl"]

    logging.label("------>     ITEM NAMES CHECK     <------")
    s = 0
    w = 0
    e = 0
    for lang in langs:
        leng = await fns.lang(lang)
        for item in items:
            try:
                name = leng['items']['name'][item['id']]
                if name.lower() in ["none", "placeholder"] and item['id'] != "0007":
                    logging.warn(f"Placeholder detected as {item['id']} name in {lang}.")
                    w += 1
                    continue
                if serious:
                    logging.success(f"Found name for {item['id']} in {lang}.")
                s += 1
            except KeyError:
                logging.critical(f"Missing name for {item['id']} in {lang}.")
                e += 1
    print("")
    logging.info(f"Check has finished. Results: {s}/{w}/{e}") 


async def check_item_descriptions(langs=None, serious=False):
    items = await fns.itemsinfo()
    if langs is None:
        langs = ["en", "pl"]

    logging.label("------>  ITEM DESCRIPTION CHECK  <------")
    s = 0
    w = 0
    e = 0
    for lang in langs:
        leng = await fns.lang(lang)
        for item in items:
            try:
                name = leng['items']['description'][item['id']]
                if name.lower() in ["none", "placeholder"] and item['id'] != "0007":
                    logging.warn(f"Placeholder detected as {item['id']} description in {lang}.")
                    w += 1
                    continue
                if serious:
                    logging.success(f"Found description for {item['id']} in {lang}.")
                s += 1
            except KeyError:
                logging.critical(f"Missing description for {item['id']} in {lang}.")
                e += 1
    print("")
    logging.info(f"Check has finished. Results: {s}/{w}/{e}") 
