import tornado.ioloop
import tornado.web
import json

import users_api as api
import os

from users_models import models
import users_api.trosak as trosak_api
import users_api.grupe as grupe_api
import users_api.transtactions as transaction_api
import users_api.transactiontype as transactiontype_api


class RegisterHandler(tornado.web.RequestHandler):
    async def post(self):
        body = json.loads(self.request.body.decode())

        id_tenant = body['id_tenant']
        username = body['username']
        password = body['password']
        first_name = body['first_name'] if 'first_name' in body else None
        last_name = body['last_name'] if 'last_name' in body else None
        monthly_income = body['monthly_income'] if 'monthly_income' in body else 0

        res = await api.register(id_tenant, username, password, first_name, last_name, monthly_income)



        if 'id_error' in res:
            self.set_status(400)
            self.write(json.dumps(res, indent=4))
            return

        self.set_status(200)
        self.write(json.dumps(res, indent=4))
        return


class LoginHandler(tornado.web.RequestHandler):
    async def post(self):
        body = json.loads(self.request.body.decode())

        id_tenant = body['id_tenant']
        username = body['username']
        password = body['password']

        res = await api.login(id_tenant, username, password)

        if 'id_error' in res:
            self.set_status(400)
            self.write(json.dumps(res, indent=4))
            return

        self.set_status(200)
        self.write(json.dumps(res, indent=4))
        return


async def authorized(handler):
    if 'Authorization' not in handler.request.headers:
        handler.set_status(401)
        handler.write(json.dumps({'message': 'not authorized'}))
        return False

    id_session = handler.request.headers['Authorization']

    res = await api.check(id_session)
    if 'error' in res['status']:
        handler.set_status(401)
        handler.write(json.dumps({'message': 'not authorized'}))
        return False

    return res


class ProtectedMethodHandler(tornado.web.RequestHandler):

    async def get(self):
        if not await authorized(self):
            return

        self.write(json.dumps({'message': 'This is message only for logged users'}))

        return None


class transactioioTypeMethodHandler(tornado.web.RequestHandler):
    async def get(self, id_trosak):
        self.write(json.dumps(await trosak_api.get(id_trosak=id_trosak)))


class transactioioTypesGetAllMethodHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write(json.dumps(await transactiontype_api.get_all_transaction_types()))

class singleTrosakHandler(tornado.web.RequestHandler):
    # TO DO:
    async def get(self, id_trosak):
        self.write(json.dumps(await trosak_api.get(id_trosak=id_trosak)))

class troskoviMethodHandler(tornado.web.RequestHandler):

    async def get(self):
        auth = await authorized(self)
        if not auth:
            return

        self.write(json.dumps(await trosak_api.get_all(auth['id_user'])))

    async def post(self):
        auth = await authorized(self)
        if not auth:
            return

        body = json.loads(self.request.body.decode())

        name = body['name']
        price = body['price']

        res = await trosak_api.add(auth['id_user'], name, price)

        if 'id_error' in res:
            self.set_status(400)
            self.write(json.dumps(res, indent=4))
            return

        self.set_status(200)
        self.write(json.dumps(res, indent=4))
        return

class transactionTypeOrderByMethodHandler(tornado.web.RequestHandler):

    async def get(self):
        auth = await authorized(self)
        if not auth:
            return

        self.write(json.dumps(await transaction_api.get_all_order_by_spent(auth['id_user'])))

class transactionOutcomeIncometransactionsMethodHandler(tornado.web.RequestHandler):

    async def get(self):
        auth = await authorized(self)
        if not auth:
            return

        self.write(json.dumps(await transaction_api.get_outcome_income_transactions(auth['id_user'])))



class transactionsMethodHandler(tornado.web.RequestHandler):

    async def get(self,year,month):

        auth = await authorized(self)

        if not auth:
            return
        # month=self.get_argument('month',1)
        # year=self.get_argument('year',2020)

        transakcije=await transaction_api.get_all(auth['id_user'],month,year)
        balance=await transaction_api.get(auth['id_user'])
        transactiontypes=await transactiontype_api.get_all_transaction_types()
        order_spent=await transaction_api.get_all_order_by_spent(auth['id_user'])
        outcome_income=await transaction_api.get_outcome_income_transactions(auth['id_user'])
        res = {}
        res['transakcije']=transakcije
        res['balance']=balance
        res['transactiontypes']=transactiontypes
        res['order_spent']=order_spent
        res['outcome_income']=outcome_income
        

        self.write(json.dumps({'res': res}))
        return

    async def post(self,g:None):
        auth = await authorized(self)
        if not auth:
            return
        body = json.loads(self.request.body.decode())

        ttype = body['ttype']
        amount= body['amount']
        description = body['description']
        transaction_type= body['transaction_type']

        res = await transaction_api.add_transaction(ttype,auth['id_user'],amount,description,transaction_type)

        if 'id_error' in res:
            self.set_status(400)
            self.write(json.dumps(res, indent=4))
            return

        self.set_status(200)
        self.write(json.dumps(res, indent=4))
        return


class transactionsPostMethodHandler(tornado.web.RequestHandler):

    async def post(self, g= None):
        auth = await authorized(self)
        if not auth:
            return
        body = json.loads(self.request.body.decode())

        ttype = body['ttype']
        amount = body['amount']
        description = body['description']
        transaction_type = body['transaction_type']

        res = await transaction_api.add_transaction(ttype, auth['id_user'], amount, description, transaction_type)

        if 'id_error' in res:
            self.set_status(400)
            self.write(json.dumps(res, indent=4))
            return

        self.set_status(200)
        self.write(json.dumps(res, indent=4))
        return

class singleTransactionHandler(tornado.web.RequestHandler):
    # TO DO:
    async def get(self):
        auth = await authorized(self)
        if not auth:
            return
        x = await transaction_api.get(auth['id_user'])
        self.write(json.dumps(x))
        return


class singleCheckHandler(tornado.web.RequestHandler):

    # TO DO:
    async def get(self, id_session):
        id_session = self.request.headers['Authorization']
        self.write(json.dumps(await api.check(id_session=id_session)))

class singleGrupeHandler(tornado.web.RequestHandler):
    # TO DO:
    async def get(self, id_grupe):
        self.write(json.dumps(await grupe_api.get(id=id_grupe)))

class GrupeMethodHandler(tornado.web.RequestHandler):

    async def get(self):
        auth = await authorized(self)
        if not auth:
            return

        self.write(json.dumps(await grupe_api.get(['id_grupe'])))

    async def post(self):
        auth = await authorized(self)
        if not auth:
            return

        body = json.loads(self.request.body.decode())

        name = body['name']

        #
        res = await grupe_api.add(name)

        if 'id_error' in res:
            self.set_status(400)
            self.write(json.dumps(res, indent=4))
            return

        self.set_status(200)
        self.write(json.dumps(res, indent=4))
        return



def make_app():
    return tornado.web.Application([
        (r"/api/users/register", RegisterHandler),
        (r"/api/users/login", LoginHandler),
        (r"/api/protected", ProtectedMethodHandler),
        (r"/api/troskovi", troskoviMethodHandler),
        (r"/api/troskovi/(.*)", singleTrosakHandler),
        (r"/api/grupe", GrupeMethodHandler),
        (r"/api/grupe/(.*)", singleGrupeHandler),
        (r"/api/transactions/(.*)/(.*)", transactionsMethodHandler),
        (r"/api/transactions", transactionsPostMethodHandler),
        (r"/api/transactiontypeinfo", transactioioTypeMethodHandler),
        (r"/api/transactiontypeamount", transactionTypeOrderByMethodHandler),
        (r"/api/transactiontypeall", transactioioTypesGetAllMethodHandler),
        (r"/api/transactionsbalance", singleTransactionHandler),

        (r"/api/users/check(.*)", singleCheckHandler),


    ],
    debug=True)


import tortoise


async def init_db():
    current_file_folder = os.path.dirname(os.path.realpath(__file__))
    with open(f'{current_file_folder}/users_config/config.json', 'rt') as f:
        c = json.load(f)

    await tortoise.Tortoise.init(
        db_url=f"postgres://{c['user']}:{c['password']}@{c['host']}/{c['dbname']}",
        modules={"models": [models]},
    )

    await tortoise.Tortoise.generate_schemas()


if __name__ == "__main__":
    app = make_app()

    from tornado.ioloop import IOLoop

    loop = IOLoop.current()

    app.listen(8888)

    loop.run_sync(init_db)

    tornado.ioloop.IOLoop.current().start()
