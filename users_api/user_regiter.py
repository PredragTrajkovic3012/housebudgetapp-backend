import re
import uuid
import users_models as models
from tortoise.queryset import Q
import datetime
import bcrypt


id_tenant = '00000000-1111-2222-3333-000000000001'


def is_valid_username(username):
    if len(username) < 2:
        return False

    username = username.lower()

    r = re.fullmatch("[a-z0-9_\.]+", username)
    if not r:
        r = re.fullmatch('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', username)
        if not r:
            return False

    return True


def password_strength(password, username=None):
    result = []
    max_strength = 0

    max_strength += 1
    if len(password) < 6:
        result.append('minimum 6 characters is required')

    max_strength += 1
    if re.match(".*[a-zA-Z]+.*", password) is None:
        result.append('minimum 1 character is required')

    max_strength += 1
    if password == password.lower():
        result.append('minimum 1 uppercase letter is required')

    max_strength += 1
    if password == password.upper():
        result.append('minimum 1 lowercase letter is required')

    max_strength += 1
    if re.match(".*[0-9]+.*", password) is None:
        result.append('minimum 1 number is required')

    if username:
        max_strength += 1
        if username.strip().lower() in password.strip().lower():
            result.append('password should not contains username')

    max_strength += 1
    contains_spec = False
    for s in '!@#$%^&*()_-+=/.,;':
        if s in password:
            contains_spec = True
            break
    if not contains_spec:
        result.append('minimum 1 special character !@#$%^&*()_-+=/.,; is required')

    return {'max_strength': max_strength,
            'strength_mark': max_strength - len(result),
            'suggestions': result}


def format_password(username, password):
    return f'{username}:{password}'.encode()


def mk_password(username, password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(format_password(username, password), salt)
    return hashed.decode()


def check_password(username, password, hashed_password):
    return bcrypt.checkpw(format_password(username, password), hashed_password.encode()) == True


def is_valid_password(password, username=None):
    strength = password_strength(password, username)
    if strength['strength_mark'] == strength['max_strength']:
        return True, ''

    return False, strength['suggestions'][0]


async def register(id_tenant: uuid.UUID, username: str, password: str, fn: str=None, ln: str=None, monthly_income: float=0) -> dict:
    username = username.strip().lower()

    if not is_valid_username(username):
        return {'status': 'error', 'id_error': 'REGISTER_ERROR', 'message': 'invalid username'}

    vp, reason = is_valid_password(password)
    if not vp:
        return {'status': 'error', 'id_error': 'PASSWORD_TO_WEAK', 'message': reason}

    try:
        exist = await models.User.filter(id_tenant=id_tenant, username=username).get_or_none()
    except Exception as e:
        raise
    if exist:
        return {'status': 'error', 'id_error': 'REGISTER_ERROR', 'message': "can't register user"}

    try:
        user = models.User(id_tenant=id_tenant, username=username, password=mk_password(username, password), first_name=fn, last_name=ln,
                           monthly_income=monthly_income)
        await user.save()
    except Exception as e:
        raise

    login_user = await login(id_tenant, username, password)

    if login_user and 'status' in login_user and login_user['status'] == 'ok':
        return {'status': 'ok', 'id_user': str(user.id), 'id_session': login_user['id_session'], 'expires_on': login_user['expires_on']}

    return login_user


async def login(id_tenant: uuid.UUID, username: str, password: str) -> dict:
    filters = [Q(id_tenant=id_tenant),
               Q(username=username.lower()),
               ]

    user = await models.User.filter(*filters).get_or_none()

    if not user:
        return {'status': 'error', 'id_error': 'ERROR_LOGGING_USER', 'message': "invalid username/password combination/NoUser"}

    try:
        if not check_password(username, password, user.password):
            return {'status': 'error', 'id_error': 'ERROR_LOGGING_USER', 'message': "invalid username/password combination"}
    except Exception as e:
        raise

    session = models.Session(user=user)

    await  session.save()

    return {'status': 'ok',
            'id_user': str(user.id),
            'id_session': str(session.id),
            'expires_on': str(session.expires_datetime)[:19]
            }


async def check(id_session: uuid.UUID):
    session = await models.Session.filter(id=id_session).get_or_none()

    if not session:
        return {'status': 'error', 'id_message': 'SESSION_NOT_FOUND_OR_EXPIRED', 'message': 'Session not found or expired'}

    import tortoise.timezone

    if session.expires_datetime < tortoise.timezone.make_aware(datetime.datetime.now()):
        return {'status': 'error', 'id_message': 'SESSION_NOT_FOUND_OR_EXPIRED', 'message': 'Session not found or expired'}

    return {'status': 'ok',
            'id_user': str(session.user_id)}


async def add(username: str,password:str,first_name:str,last_name:str,monthly_income:float):

    try:
        user = models.User(id_tenant=id_tenant, username=username, password=password, first_name=first_name, last_name=last_name,
                           monthly_income=monthly_income)
        await user.save()
    except Exception as e:
        return {'status': 'error',
                'id_error': 'DATABASE_ERROR',
                'message': str(e)}

    return {
        'status': 'ok',
        'id': str(user.id)}


async def get(id_user):

    user = await models.User.filter(id=id_user).get_or_none()

    if not user:
        return False

    return {
        'id': str(user.id),
        'name': user.username
    }


async def patch_user_group(id_user:uuid.UUID,id_group:uuid.UUID):

    user = await models.User.filter(id=id_user).get_or_none()
    group= await models.Group.filter(id=id_group).get_or_none()

    if not user:
        return False

    try:
        user.group = group
        await user.save()
    except Exception as e:
        return {'status': 'error',
                'id_error': 'DATABASE_ERROR',
                'message': str(e)}

    return {
        'status': 'ok',
        'message': 'User dodat u grupu'}




