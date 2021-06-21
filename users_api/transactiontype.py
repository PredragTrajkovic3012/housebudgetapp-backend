import uuid

import users_models
from users_models import models


async def add_transactiontype(ime=None,description:str="",imeslike:str="",ttype:str=None):
    try:
        t = models.TransactionType(name=ime,description=description, image=imeslike,ttype=ttype)
        await t.save()
    except Exception as e:
        return {'status': 'error',
                'id_error': 'DATABASE_ERROR',
                'message': str(e)}

    return {
        'status': 'ok',
        'id': str(t.id)}



async def getImage(id_transaction_type):
    try:
        transaction_type=await models.TransactionType.filter(id=id_transaction_type).get_or_none()
    except Exception as e:
        raise
    if not transaction_type:
        return {'status': 'error','message':'transaction_type not found'}
    try:
        imeslike=transaction_type.image
        return { 'image': imeslike}
    except Exception as e:
        raise




async  def setTransactionTypes():
    ttypes=[["Clothes","Buy new T-shirt,jeans etc","clothes","outcome"],
            ["Groceries","Green market,supermarket etc","groceries","outcome"],
            ["Eating out","Fast food,Restaurants,family lunch etc","eatout","outcome"],
            ["Bills","pay bills","bills","outcome"],
            ["Car","buy new car,gas etc","car","outcome"],
            ["Communication","Comunication bills","communication","outcome"],
            ["Gift","For your wife friends etc","gift","outcome"],
            ["Transport","Transport tickets","transport","outcome"],
            ["Health","Visit to doctors,supplements etc","health","outcome"],
            ["Sport", "Gym,workout equipment etc", "equipment","outcome"],
            ["Pets", "Toys,food,medicine for pets", "pet","outcome"],
            ["Entertainment", "Cinema,night clubs,concerts etc", "entertainment","outcome"],
            ["Taxi", "Uber,Taxi,Car go...", "taxi","outcome"],
            ["Salary", "You work whole month for that", "salary","income"],
            ["Toiletries", "Toiletries", "toiletries","outcome"],
            ["Other", "Other stuff", "other", "income"]
            ]

    try:
        for t in ttypes:
            print(t)

            await add_transactiontype(t[0],t[1],t[2],t[3])
             #models.TransactionType(name=t[0], description=t[1], image=t[2])


    except Exception as e:
        return {'status': 'error',
                'id_error': 'DATABASE_ERROR',
                'message': str(e)}

    return {'status': 'Niz je ubacen',}


async def get_all_transaction_types():
    ttypes= await models.TransactionType.filter().all()
    if not ttypes:
        return {'status': 'error', 'message': 'transactionsTypes not found'}

    #await ttypes.fetch_related('transaction_types')

    return [{'id': str(t.id), 'name': t.name,'description': t.description,'image':t.image,'ttype':t.ttype} for t in ttypes]






