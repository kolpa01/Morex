import functions as fns


async def all_received(user, client, current=None) -> dict:
    relationships = await fns.u_relationships()
    data = {}
    i = 0
    if not current:
        for uuid, uid in relationships[str(user.id)]["marriage_received"].items():
            i += 1
            data.update({f"{await client.fetch_user(uid)} | {uuid}": uuid})
            if i == 24:
                break
        return dict(sorted(data.items()))
    else:
        for uuid, uid in relationships[str(user.id)]["marriage_received"].items():
            string = f"{await client.fetch_user(uid)} | {uuid}"
            if str(current.lower()) in string.lower():
                data.update({string: uuid})
            if i == 24:
                break
        return dict(sorted(data.items()))


async def all_married(user, client, current=None) -> dict:
    relationships = await fns.u_relationships()
    data = {}
    i = 0
    if not current:
        for uid in relationships[str(user.id)]["marriages"]:
            i += 1
            data.update({f"{await client.fetch_user(uid)}": uid})
            if i == 24:
                break
        return dict(sorted(data.items()))
    else:
        for uid in relationships[str(user.id)]["marriages"]:
            string = f"{await client.fetch_user(uid)}"
            if str(current.lower()) in string.lower():
                data.update({string: uid})
            if i == 24:
                break
        return dict(sorted(data.items()))
