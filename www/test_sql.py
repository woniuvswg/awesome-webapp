import orm, asyncio, logging
from pymysql.err import IntegrityError
from models import User, Blog, Comment


async def test(loop):
    await orm.create_pool(loop=loop, user='josef', password='password', database='awesome')
    u = User(name='josef', email='josef_luo@qq.com', password='202107', image='about:blank')
    try:
        await u.save()
    except IntegrityError as e:
        logging.error(e)
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    loop.close()
