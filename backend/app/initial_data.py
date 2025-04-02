'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-02 16:32:19
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-02 17:49:59
FilePath: /server/backend/app/initial_data.py
Description: 初始数据
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
import logging

from sqlmodel import Session

from app.core.db import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("创建初始数据")
    init()
    logger.info("初始数据创建完成")


if __name__ == "__main__":
    main()
