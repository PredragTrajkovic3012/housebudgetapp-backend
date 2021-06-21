import uuid
from users_models import models

async def add(name: str):

    try:
        grupa = models.Group(name=name)
        await grupa.save()
    except Exception as e:
        return {'status': 'error',
                'id_error': 'DATABASE_ERROR',
                'message': str(e)}

    return {
        'status': 'ok',
        'id': str(grupa.id)}

async def get(id_grupe):

    grupa = await models.Group.filter(id=id_grupe).get_or_none()


    if not grupa:
        return False

    return {
        'id': str(grupa.id),
        'name': grupa.name
    }

async def get_group_budget(id_grupe):
    grupa = await models.Group.filter(id=id_grupe).get_or_none()

    if not grupa:
        return False

    return {
        'id': str(grupa.id),
        'name': grupa.name,
        'group_budget': float(await grupa.group_budget)
    }


async def get_group_spent_on(id_grupe):
    grupa = await models.Group.filter(id=id_grupe).get_or_none()

    if not grupa:
        return False

    await grupa.fetch_related('users')
    nizSvihTransakcija=[]
    for u in grupa.users:
        try:
            await u.fetch_related("transactions")
            last = await models.Transaction.filter(user=u).order_by('amount').limit(4).all()
            nizSvihTransakcija.append(last)
            for t in last:
                if not t.income_outcome:
                    nizSvihTransakcija.append(
                        {
                            'id': str(t.id),
                            'date': t.created.strftime("%d %B, %Y,  %H:%M:%S"),  # estr(t.created),
                            'amount': abs(float(t.amount)),
                            'current_balance': float(t.current_balance),
                            'income-outcome': t.income_outcome,
                            'transaction_type': await t.ttype,
                            'description': t.description
                        }
                    )
            return nizSvihTransakcija

        except Exception as e:
            return {'status': 'error',
                    'message': str(e)}





