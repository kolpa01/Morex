import functions as fns


async def all_recipes(leng, current=None) -> dict:
    recipies = await fns.recipies()
    data = {}
    i = 0
    if not current:
        for recip in recipies:
            chk_it = fns.get_recipe(recip['item'], "name", leng)
            if chk_it.available:
                i += 1
                data.update({chk_it.item.disname: chk_it.item.id})
            if i == 24:
                break
        return dict(sorted(data.items()))
    else:
        for recip in recipies:
            chk_it = fns.get_recipe(recip['item'], "name", leng)
            if chk_it.available:
                if str(current.lower()) in chk_it.item.disname.lower():
                    i += 1
                    data.update({chk_it.item.disname: chk_it.item.id})
            if i == 24:
                break
        return dict(sorted(data.items()))
