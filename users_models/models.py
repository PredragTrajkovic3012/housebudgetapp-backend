import uuid
import tortoise
from tortoise import Tortoise, fields
from tortoise.models import Model
import json
import datetime


class Group(Model):
    """
       :type _chunk_pattern: str
       ... other fields
       """
    ...  # rest of class

    class Meta:
        table = 'grupe'

    id = fields.UUIDField(pk=True)
    created = fields.DatetimeField(default=datetime.datetime.now)
    name = fields.CharField(max_length=128)

    @property
    async def group_budget(self):

        await self.fetch_related('users')

        b = 0

        for u in self.users:
           await u.fetch_related("transactions")


           #if u.transactions.order_by('-created').limit(1).all():
           if u.transactions:
               b+= u.transactions[-1].current_balance
                # b += u.transactions[len(u.transactions)-1].current_balance

        return b

    #    group_budget=fields.FloatField()

    users: fields.ReverseRelation["User"] = fields.ReverseRelation


class User(Model):
    class Meta:
        table = 'users'
        unique_together = (('id_tenant', 'username'),)

    id = fields.UUIDField(pk=True)
    id_tenant = fields.UUIDField(index=True)
    username = fields.CharField(max_length=64)
    password = fields.CharField(max_length=128)
    active = fields.BooleanField(null=False, default=True)
    # moj kod
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    monthly_income = fields.FloatField(null=True)
    transactions: fields.ReverseRelation["Transaction"] = fields.ReverseRelation

    troskovi: fields.ReverseRelation["Trosak"] = fields.ReverseRelation
    group = fields.ForeignKeyField('models.Group', index=True, null=True, related_name='users')

    async def plati_trosak(self, id_trosak: uuid.UUID):
        trosak = await Trosak.filter(id=id_trosak).get_or_none()
        if not trosak:
            return {'status': 'error', 'message': 'not-found'}

        self.monthly_income = self.monthly_income - trosak.price
        trosak.placeno = True
        await self.save()
        await trosak.save()

    async def dodaj_usera_u_grupu(self, id_group: uuid.UUID):
        self.group = id_group
        await self.save()

    async def calc_budget_minus_troskovi(self):

        await self.fetch_related("troskovi")
        await self.save()

        for t in self.troskovi:
            if t.placeno == False:
                self.monthly_income = self.monthly_income - t.price
                t.placeno = True
                await  t.save()

        await self.save()

        #        print(self.monthly_income)
        return self.monthly_income


class Session(Model):
    class Meta:
        table = 'sessions'

    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', index=True)

    expires_datetime = fields.DatetimeField(null=True)

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.expires_datetime = datetime.datetime.now() + datetime.timedelta(days=2)


import tortoise.timezone


def tz_now():
    return tortoise.timezone.now()


class Transaction(Model):
    class Meta:
        table = 'transactions'
        ordering = ('created',)

    id = fields.UUIDField(pk=True)
    created = fields.DatetimeField(index=True)
    user = fields.ForeignKeyField('models.User', index=True, null=True, related_name='transactions')
    amount = fields.DecimalField(12, 2)
    current_balance = fields.DecimalField(12, 2)
    income_outcome=fields.BooleanField(default=True,null=True)
    description=fields.CharField(max_length=128,default="Transakcija",null=True)
    #transaction_type=fields.ReverseRelation["TransactionType"] = fields.ReverseRelation
    transaction_type = fields.ForeignKeyField('models.TransactionType', index=True, null=True)


    def serialize(self):
        return {
            "id": str(self.id),
            "created":str( self.created),

            "amount": str(self.amount),
            "current_balance": str(self.current_balance),
            "income_outcome": str(self.income_outcome),
            "description": str(self.description),
        }


    @property
    async def ttype(self):
        if not self.transaction_type:
            return None
        await self.fetch_related('transaction_type')
        return self.transaction_type.serialize()
        return str(self.transaction_type.id)

    def __str__(self):
        return f"{self.id} {self.amount}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created = tz_now()


class Trosak(Model):
    class Meta:
        table = 'trosak'
        ordering = ('created',)

    id = fields.UUIDField(pk=True)
    created = fields.DatetimeField(default=datetime.datetime.now)
    name = fields.CharField(max_length=60)
    price = fields.FloatField()
    placeno = fields.BooleanField(default=False)

    user = fields.ForeignKeyField('models.User', index=True, null=True, related_name='troskovi')


class TransactionType(Model):
    class Meta:
        table = 'transaction_type'


    id = fields.UUIDField(pk=True)
    name=fields.CharField(max_length=128,null=True,default="No-Name")
    description = fields.CharField(max_length=128)
    image = fields.CharField(max_length=128)
    transactions: fields.ReverseRelation["Transaction"] = fields.ReverseRelation
    ttype=fields.CharField(max_length=128,default="outcome",null=True)



    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "ttype":self.ttype
        }

    def getImage(self):
        return self.image



