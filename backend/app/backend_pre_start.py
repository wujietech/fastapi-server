'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-02 16:32:19
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-02 17:50:36
FilePath: /server/backend/app/backend_pre_start.py
Description: 服务启动前初始化
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.db import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # 尝试创建会话以检查数据库是否正在运行
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("初始化服务")
    init(engine)
    logger.info("服务初始化完成")


if __name__ == "__main__":
    main()
