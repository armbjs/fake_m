import redis
import json
import time
import os
import sys
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Redis 설정
redis_server_addr = 'vultr-prod-3a00cfaa-7dc1-4fed-af5b-19dd1a19abf2-vultr-prod-cd4a.vultrdb.com'
redis_server_port = '16752'
redis_server_db_index = '0'
redis_server_username = 'armbjs'
redis_server_password = 'xkqfhf12'
redis_server_ssl = 'True'

redis_publish_channel_name_prefix = 'CF_NEW_NOTICES'
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

def publish_test_notices():
    current_time = int(time.time() * 1000)
    coin_symbol = f"TST{current_time % 1000:03d}"
    
    # UPBIT 형식의 공지사항
    upbit_notice_en1 = {
        "type": "NOTICE",
        "action": "NEW",
        "title": f"Market Support for {coin_symbol}(Tasdas), XRP(Ripple Network) (BTC, USDT Market)",
        "content": None,
        "exchange": "UPBIT",
        "url": "https://upbit.com/service_center/notice?id=4695",
        "category": "Trade",
        "listedAt": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "listedTs": current_time,
        "receivedTs": current_time + 100
    }

    upbit_notice_en2 = {
        "type": "NOTICE",
        "action": "NEW",
        "title": f"Market Support for Tasdas({coin_symbol}), Ripple Network(XRP) (BTC, USDT Market)",
        "content": None,
        "exchange": "UPBIT",
        "url": "https://upbit.com/service_center/notice?id=4695",
        "category": "Trade",
        "listedAt": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "listedTs": current_time,
        "receivedTs": current_time + 100
    }
    
    upbit_notice_kr1 = {
        "type": "NOTICE",
        "action": "NEW",
        "title": f"[거래] {coin_symbol}(TestCoin), XRP(리플) 신규 거래지원 안내 (BTC, USDT 마켓)",
        "content": None,
        "exchange": "UPBIT",
        "url": "https://upbit.com/service_center/notice?id=4695",
        "category": None,
        "listedAt": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "listedTs": current_time,
        "receivedTs": current_time + 100
    }

    upbit_notice_kr2 = {
        "type": "NOTICE", 
        "action": "NEW",
        "title": f"렌더토큰({coin_symbol}) KRW, USDT 마켓 디지털 자산 추가",
        "content": None,
        "exchange": "UPBIT",
        "url": "https://upbit.com/service_center/notice?id=4695",
        "category": None,
        "listedAt": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "listedTs": current_time,
        "receivedTs": current_time + 100
        }
    
    try:
        # UPBIT 공지 발송
        upbit_notice_en1_json = json.dumps(upbit_notice_en1, ensure_ascii=False)
        redis_client.publish(redis_publish_channel_name_prefix, upbit_notice_en1_json)
        logger.info(f"Published UPBIT test notice for {coin_symbol}")
        logger.info(f"UPBIT notice data: {upbit_notice_en1_json}")
        
        # 2초 대기
        time.sleep(2)

        # UPBIT 공지 발송
        upbit_notice_en2_json = json.dumps(upbit_notice_en2, ensure_ascii=False)
        redis_client.publish(redis_publish_channel_name_prefix, upbit_notice_en2_json)
        logger.info(f"Published UPBIT test notice for {coin_symbol}")
        logger.info(f"UPBIT notice data: {upbit_notice_en2_json}")
        
        # 2초 대기
        time.sleep(2)
        
        # UPBIT2 공지 발송
        upbit_notice_kr1_json = json.dumps(upbit_notice_kr1, ensure_ascii=False)
        redis_client.publish(redis_publish_channel_name_prefix, upbit_notice_kr1_json)
        logger.info(f"Published BITHUMB test notice for {coin_symbol}")
        logger.info(f"UPBIT notice data: {upbit_notice_kr1_json}")

        # 2초 대기
        time.sleep(2)
            
        # 디지털 자산 추가 공지 발송
        upbit_notice_kr2_json = json.dumps(upbit_notice_kr2, ensure_ascii=False)
        redis_client.publish(redis_publish_channel_name_prefix, upbit_notice_kr2_json)
        logger.info(f"Published UPBIT digital asset addition notice for {coin_symbol}")
        logger.info(f"UPBIT notice data: {upbit_notice_kr2_json}")
        
    except Exception as e:
        logger.error(f"Error publishing notices: {e}")

def run_tests():
    logger.info("Executing test notices")
    publish_test_notices()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # 시작할 때 한 번 실행
    run_tests()
    
    # 10분마다 테스트 실행
    scheduler.add_job(run_tests, 'interval', minutes=10)
    
    logger.info("Scheduler started. Tests will run every 10 minutes.")
    scheduler.start()