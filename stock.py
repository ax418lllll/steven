import requests
import json
import time
from datetime import datetime


def get_gold_price():
    """获取实时金价"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # 获取美元黄金价格
        url = "http://push2.eastmoney.com/api/qt/stock/get?secid=101.GC00Y&fields=f43,f44,f45,f46,f47,f169,f170"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = json.loads(response.text)
            if data.get('data'):
                price_usd = data['data']['f43'] / 100
                change_pct = data['data']['f170'] / 100  # 涨跌幅
                print(f"黄金价格: {price_usd} 美元/盎司 ({change_pct:+.2f}%)")
            else:
                print("获取美元金价失败: 数据格式错误")
                
        # 获取人民币黄金价格
        url_cny = "http://push2.eastmoney.com/api/qt/stock/get?secid=113.aum&fields=f43,f44,f45,f46,f47,f169,f170"
        response = requests.get(url_cny, headers=headers, timeout=10)
        if response.status_code == 200:
            data = json.loads(response.text)
            if data.get('data'):
                price_cny = data['data']['f43'] / 100
                change_pct = data['data']['f170'] / 100  # 涨跌幅
                print(f"黄金价格: {price_cny} 元/克 ({change_pct:+.2f}%)")
            else:
                print("获取人民币金价失败: 数据格式错误")
    except Exception as e:
        print(f"获取金价失败: {str(e)}")

def get_stock_indices():
    """获取股票指数"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # 使用东方财富网API获取指数数据
    indices = {
        "上证指数": "1.000001",
        "深证成指": "0.399001", 
        "创业板指": "0.399006",
        "纳斯达克": "100.NDX"
    }

    try:
        for name, code in indices.items():
            url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={code}&fields=f43,f44,f45,f46,f47,f169,f170"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = json.loads(response.text)
                if data.get('data'):
                    price = data['data']['f43'] / 100
                    change_pct = data['data']['f170'] / 100  # 涨跌幅
                    print(f"{name}: {price} ({change_pct:+.2f}%)")
                else:
                    print(f"获取{name}失败: 数据格式错误")
            time.sleep(0.5)  # 添加短暂延时
    except Exception as e:
        print(f"获取股票指数失败: {str(e)}")

def get_exchange_rate():
    """获取美元人民币汇率"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # 使用东方财富网汇率API
        url = "http://push2.eastmoney.com/api/qt/stock/get?secid=133.USDCNH&fields=f43,f44,f45,f46,f47,f169,f170"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = json.loads(response.text)
            if data and data.get('data'):
                current_rate = data['data']['f43'] / 10000
                change_pct = data['data']['f170'] / 100
                print(f"美元兑人民币汇率: {current_rate:.3f} ({change_pct:+.2f}%)")
            else:
                print("获取汇率失败: 数据为空")
    except Exception as e:
        print(f"获取汇率失败: {str(e)}")

if __name__ == "__main__":
    print(f"正在获取最新行情... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    get_gold_price()
    time.sleep(1)
    get_stock_indices()
    time.sleep(1)
    get_exchange_rate()
