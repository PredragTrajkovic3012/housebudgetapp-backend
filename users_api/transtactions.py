import uuid
from users_models import models
from tortoise.queryset import Q
import json


id_ttype = '00000000-1111-2222-3333-000000000003'
async def add_transaction(ttype, id_user, amount, description,transaction_type=None):
    incoutc=True
    user = await models.User.filter(id=id_user).get_or_none()
    if not user:
        return {'status': 'error', 'message': 'user not found'}

    if ttype not in ('income', 'outcome'):
        return {'status': 'error', 'message': 'use income/outcome for type'}

    amount = abs(amount)

    if ttype == 'outcome':
        amount = -amount
        incoutc= False


    last = await models.Transaction.filter(user=user).order_by('-created').limit(1).all()

    balance = last[0].current_balance + amount if last else amount

    tttt = await models.TransactionType.filter(id=transaction_type).get_or_none()
    #print(tttt.name)

    t = models.Transaction(user=user, amount=amount, description=description, current_balance=balance,income_outcome=incoutc,transaction_type=tttt)
    await t.save()

    return {'status': 'ok', 'id': str(t.id)}




async def get(id_user):
    try:
        user=await models.User.filter(id=id_user).get_or_none()
    except Exception as e:
        raise
    if not user:
        return {'status': 'error','message':'user not found'}
    try:
        await user.fetch_related('transactions')
    except Exception as e:
        return {'status': 'error',
                'message': str(e)}
    try:
        last = await models.Transaction.filter(user=user).order_by('-created').limit(1).all()
        if not last:
            return []
        else:
            balance = last[0].current_balance
            return { 'current_balance': float(balance)}

    except Exception as e:
        raise



async def get_all(id_user,month:None=6,year:None=2021):
    try:

        user = await models.User.filter(id=id_user).get_or_none()
    except Exception as e:
        raise
    if not user:
        return {'status': 'error', 'message': 'user not found'}

    try:
        await user.fetch_related('transactions')



    except Exception as e:
        return {'status': 'error',
                'message': str(e)}


    try:
        niz=[];
        niz=user.transactions
        niz=niz[::-1]

        noviNiz = []


        for t in niz:

            if int((t.created.strftime("%m"))) == int(month)+1 and int(t.created.strftime("%Y")) == int(year):
                noviNiz.append({
                    'id': str(t.id),
                    'date': t.created.strftime("%d %B, %Y,  %H:%M:%S"),  # estr(t.created),
                    'amount': float(t.amount),
                    'current_balance': float(t.current_balance),
                    'income-outcome': t.income_outcome,
                    'transaction_type': await t.ttype,
                    'description': t.description

                })
        return noviNiz

        

    except Exception as e:
        raise

async def get_avg_of_all_positive_transaction(id_user):
    try:
        user = await models.User.filter(id=id_user).get_or_none()
    except Exception as e:
        raise
    if not user:
        return {'status': 'error', 'message': 'user not found'}

    try:
        await user.fetch_related('transactions')

    except Exception as e:
        return {'status': 'error',
                'message': str(e)}
    try:
        numberofPositiveTrans=0
        totalpositivebalance=0


        for t in user.transactions:
            if t.income_outcome == True:
                numberofPositiveTrans+=1
                totalpositivebalance+=t.amount

        res=totalpositivebalance/numberofPositiveTrans

        return{'Srednja vrednost primanja':res}

    except Exception as e:
        raise


async def get_all_order_by_spent(id_user):
    try:
        user = await models.User.filter(id=id_user).get_or_none()
    except Exception as e:
        raise
    if not user:
        return {'status': 'error', 'message': 'user not found'}

    try:
        await user.fetch_related('transactions')



    except Exception as e:
        return {'status': 'error',
                'message': str(e)}


    try:

        last = await models.Transaction.filter(user=user).order_by('amount').limit(4).all()
        noviNiz = []

        for t in last:
            if not t.income_outcome:
                noviNiz.append({
                'id': str(t.id),
                'date': t.created.strftime("%d %B, %Y,  %H:%M:%S"), #estr(t.created),
                'amount': abs(float(t.amount)),
                'current_balance': float(t.current_balance),
                'income-outcome':t.income_outcome,
                'transaction_type': await t.ttype,
                'description':t.description
            })
        return noviNiz


    except Exception as e:
        raise

async def get_outcome_income_transactions(id_user):
    try:
        user = await models.User.filter(id=id_user).get_or_none()
    except Exception as e:
        raise
    if not user:
        return {'status': 'error', 'message': 'user not found'}

    try:
        await user.fetch_related('transactions')

    except Exception as e:
        return {'status': 'error',
                'message': str(e)}
    try:

        totalnegativebalance=0
        totalpositivebalance=0


        for t in user.transactions:
            if t.income_outcome == False:
                totalnegativebalance+=t.amount
            if t.income_outcome == True:
                totalpositivebalance+=t.amount

        return {'income':float(totalpositivebalance),'outcome':float(totalnegativebalance)}

    except Exception as e:
        raise


async def get_all_method2(id_user, month: int = 6, year: None = 2021):
    try:

        user = await models.User.filter(id=id_user).get_or_none()

    except Exception as e:
        raise
    if not user:
        return {'status': 'error', 'message': 'user not found'}

    try:
        await user.fetch_related('transactions')




    except Exception as e:
        return {'status': 'error',
                'message': str(e)}

    try:

        import datetime
        m1 =int(month)+1
        startDate=datetime.datetime.strptime(f"{year}-{str(month).zfill(2)}-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        endDate = datetime.datetime.strptime(f"{year}-{str(m1).zfill(2)}-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        user=await  models.User.get_or_none()

        filters=[
            Q(created__gte=startDate),
            Q(created__lte =endDate),
            Q(user=user),
        ]
        transac=[]

        transac = [await t.serialize() for t in await models.Transaction.filter(*filters).all()]
        print(transac)
        return transac
    except Exception as e :
        raise





# filters = [Q(id_tenant=id_tenant),
#                Q(username=username.lower()),
#                ]
#
#     user = await models.User.filter(*filters).get_or_none()
