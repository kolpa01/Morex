import functions as fns


async def all_clans(user, current=None) -> dict:
    clans = await fns.get_clans()
    data = {}
    i = 0
    if not current:
        for uuid, clan_data in clans.items():
            i += 1
            data.update({f"{clan_data["name"]} | {uuid}": uuid})
            if i == 24:
                break
        return dict(sorted(data.items()))
    else:
        for uuid, clan_data in clans.items():
            string = f"{clan_data["name"]} | {uuid}"
            if str(current.lower()) in string.lower():
                data.update({string: uuid})
            if i == 24:
                break
        return dict(sorted(data.items()))
