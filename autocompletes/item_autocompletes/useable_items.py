import functions as fns


async def useable_items(leng, current=None) -> dict:
    language = await fns.lang(leng)
    data = {}
    i = 0
    if not current:
        for item in language['items']['name']:
            chk_it = fns.get_item(item, "id", leng)
            if chk_it.useable:
                i += 1
                data.update({chk_it.disname: chk_it.id})
            if i == 24:
                break
        return dict(sorted(data.items()))
    else:
        for item in language['items']['name']:
            chk_it = fns.get_item(item, "id", leng)
            if chk_it.useable:
                if str(current.lower()) in chk_it.disname.lower():
                    i += 1
                    data.update({chk_it.disname: chk_it.id})
            if i == 24:
                break
        return dict(sorted(data.items()))
