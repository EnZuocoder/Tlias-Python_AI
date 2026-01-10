from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
# 数据库连接URL
DATABASE_URL = "mysql+aiomysql://root:1234@localhost:3306/tilas?charset=utf8"
# 创建数据库异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True, # 是否输出SQL日志(调试时可开启)
    pool_size=10,
    max_overflow=20,
)
# 创建异步会话工厂,用于生成异步会话对象
AsyncSessionLocal = async_sessionmaker(
    bind=engine,#绑定数据库引擎
    class_=AsyncSession,#指定会话类
    expire_on_commit=False # 提交后不失效对象
)
# 依赖注入函数,用于在请求中获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            # 发生异常回滚事务,保证数据一致性
            await session.rollback()
            raise e
        finally:
            await session.close()
