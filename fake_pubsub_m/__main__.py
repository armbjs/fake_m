import redis
import json
import time
import os
import sys
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

# 상위 디렉토리를 sys.path에 추가하여 configs.py를 import할 수 있게 합니다.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fake_pubsub_m import configs

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Redis 설정
redis_server_addr = 'vultr-prod-3a00cfaa-7dc1-4fed-af5b-19dd1a19abf2-vultr-prod-cd4a.vultrdb.com'
redis_server_port = '16752'
redis_server_db_index = '0'
redis_server_username = 'armbjs'
redis_server_password = 'xkqfhf12'
redis_server_ssl = 'True'

redis_publish_channel_name_prefix = 'UPBIT_NEW_NOTICES'
redis_publish_binance_channel = 'BINANCE_NEW_NOTICES'
redis_stream_key_buy = 'fake_pubsub_massage:purchased_coins'

# Redis 클라이언트 생성
redis_client = redis.Redis(
    host=redis_server_addr,
    port=int(redis_server_port),
    db=int(redis_server_db_index),
    username=redis_server_username,
    password=redis_server_password,
    ssl=redis_server_ssl,
    decode_responses=True
)

def remove_xrp_from_purchased_coins():
    purchased_coins = redis_client.get(redis_stream_key_buy)
    if purchased_coins:
        coins = set(json.loads(purchased_coins))
        if 'XRP' in coins:
            coins.remove('XRP')
            redis_client.set(redis_stream_key_buy, json.dumps(list(coins)))
            logger.info("XRP removed from purchased coins list")
        else:
            logger.info("XRP not found in purchased coins list")
    else:
        logger.info("No purchased coins found")

def publish_test_notice():
    current_time = int(time.time() * 1000)  # milliseconds로 변환
    coin_symbol = f"TST{current_time % 1000:03d}"  # 유니크한 코인 심볼 생성
    
    # 업비트 공지사항 포맷에 맞춘 메시지 생성
    notice_data = {
        "title": f"{coin_symbol} 거래 지원 안내",
        "content": f"{coin_symbol} 코인이 업비트에 상장됩니다.",
        "url": "https://api-manager.upbit.com/api/v1/notices/319",
        "language": "ko-KR",
        "senderAddr": "",
        "receiverAddr": "",
        "listedTs": current_time,
        "receivedTs": current_time + 100  # 100ms 후 수신된 것으로 설정
    }

    # 바이낸스 공지사항 포맷에 맞춘 메시지 생성
    binance_notice = {
        "title": f"Binance Futures Will Launch USDⓈ-Margined {coin_symbol} Perpetual Contract With up to 50x Leverage",
        "content": f"Binance will list {coin_symbol} perpetual contracts",
        "url": "https://www.binance.com/en/support/announcement/test",
        "listedTs": current_time,
        "receivedTs": current_time + 100
    }
    
    try:
        # JSON으로 직렬화하여 전송
        redis_client.publish(redis_publish_channel_name_prefix, json.dumps(notice_data))
        redis_client.publish(redis_publish_binance_channel, json.dumps(binance_notice))
        
        logger.info(f"Published Upbit test notice for {coin_symbol}")
        logger.info(f"Notice data: {json.dumps(notice_data, indent=2)}")
        logger.info(f"Published Binance test notice for {coin_symbol}")
        logger.info(f"Binance notice data: {json.dumps(binance_notice, indent=2)}")
        
    except Exception as e:
        logger.error(f"Error publishing notices: {e}")

def run_tests():
    logger.info("Executing hourly test")
    publish_test_notice()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    run_tests()
    # 1시간 간격으로 실행 예약
    scheduler.add_job(run_tests, 'interval', hours=1)
    
    logger.info("Scheduler started. Tests will run every hour.")
    scheduler.start()