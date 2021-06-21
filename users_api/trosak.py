import uuid
from users_models import models


async def add(id_user: uuid.UUID, name: str, price: int):
    try:
        trosak = models.Trosak(user_id=id_user, name=name, price=price)
        await trosak.save()
    except Exception as e:
        return {'status': 'error',
                'id_error': 'DATABASE_ERROR',
                'message': str(e)}

    return {
        'status': 'ok',
        'id': str(trosak.id)}


async def get(id_trosak):
    trosak = await models.Trosak.filter(id=id_trosak).get_or_none()

    if not trosak:
        return False

    return {
        'id': str(trosak.id),
        'name': trosak.name
    }


from users_api.common import tz_now

async def add_transaction(ttype, id_user, amount, description):
    user = await models.User.filter(id=id_user).get_or_none()
    if not user:
        return {'status': 'error', 'message': 'user not found'}

    if ttype not in ('income', 'outcome'):
        return {'status': 'error', 'message': 'use income/outcome for type'}

    amount = abs(amount)

    if ttype == 'outcome':
        amount = -amount

    last = await models.Transaction.filter(user=user).order_by('-created').limit(1).all()

    balance = last[0].current_balance + amount if last else amount

    t = models.Transaction(user=user, amount=amount, description=description, current_balance=balance)
    await t.save()

    return {'status': 'ok', 'id': str(t.id)}


async def get_all(id_user):
    user = await models.User.filter(id=id_user).get_or_none()
    if not user:
        return {'status': 'error', 'message': 'user not found'}

    await user.fetch_related('troskovi')

    return [{'id': str(t.id), 'name': t.name} for t in user.troskovi]

    # return [{'id': str(b.id), 'name': b.name} for b in await models.Trosak.filter(user_id=id_user).all().order_by('name')]
