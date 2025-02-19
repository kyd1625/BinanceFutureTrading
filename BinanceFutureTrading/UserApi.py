from binance.client import Client
from config.secrets import APIKey, secretKey
from config.settings import testnetYN, leverage

client = Client(APIKey, secretKey)

if testnetYN == "Y" :
    client.FUTURES_URL = client.FUTURES_TESTNET_URL  # testnetYN = "Y" 일시 테스트넷으로 적용

def get_all_positions():
    """
    선물 계좌에 열린 모든 포지션 정보를 가져오는 함수.
    """
    try:
        # 선물 계좌의 포지션 정보 가져오기
        positions = client.futures_position_information()

        # 열린 포지션만 필터링 (positionAmt가 0이 아닌 경우)
        open_positions = []
        for position in positions:
            symbol = position['symbol']
            position_amt = float(position['positionAmt'])

            if position_amt != 0:  # 포지션이 열려 있을 경우
                # 필드가 존재하는지 확인하고 값이 없으면 기본값을 할당
                unrealized_profit = position.get('unrealizedProfit', '0.00')
                entry_price = position.get('entryPrice', '0.00')
                liquidation_price = position.get('liquidationPrice', '0.00')
                leverage = position.get('leverage', '1')
                isolated = position.get('isolated', 'FALSE')

                open_positions.append({
                    "symbol": symbol,
                    "positionAmt": position_amt,
                    "entryPrice": entry_price,  # 진입 가격
                    "unrealizedProfit": unrealized_profit,  # 미실현 이익
                    "liquidationPrice": liquidation_price,  # 청산 가격
                    "leverage": leverage,  # 레버리지
                    "isolated": isolated,  # 고립 모드 여부
                })

        if open_positions:
            print("열린 포지션들:")
            for position in open_positions:
                print(position)
        else:
            print("열린 포지션이 없습니다.")

    except Exception as e:
        print(f"에러 발생: {e}")


def get_position_for_symbol(symbol):
    """
    특정 심볼에 대한 열린 포지션 정보를 가져오는 함수.
    """
    try:
        # 선물 계좌의 포지션 정보 가져오기
        positions = client.futures_position_information()

        # 특정 심볼에 대한 포지션 찾기
        for position in positions:
            if position['symbol'] == symbol:
                position_amt = float(position['positionAmt'])

                if position_amt != 0:  # 포지션이 열려 있을 경우
                    # 필드가 존재하는지 확인하고 값이 없으면 기본값을 할당
                    unrealized_profit = position.get('unrealizedProfit', '0.00')
                    entry_price = position.get('entryPrice', '0.00')
                    liquidation_price = position.get('liquidationPrice', '0.00')
                    leverage = position.get('leverage', '1')
                    isolated = position.get('isolated', 'FALSE')

                    position_info = {
                        "symbol": symbol,
                        "positionAmt": position_amt,
                        "entryPrice": entry_price,  # 진입 가격
                        "unrealizedProfit": unrealized_profit,  # 미실현 이익
                        "liquidationPrice": liquidation_price,  # 청산 가격
                        "leverage": leverage,  # 레버리지
                        "isolated": isolated,  # 고립 모드 여부
                    }
                    print("특정 심볼 포지션 정보:")
                    print(position_info)
                    return position_info
        print(f"{symbol}에 열린 포지션이 없습니다.")

    except Exception as e:
        print(f"에러 발생: {e}")

def get_position_for_symbol_with_pnl(symbol):
    """
    특정 심볼에 대한 열린 포지션 정보 및 수익률(PnL)을 가져오는 함수.
    """
    try:
        # 선물 계좌의 모든 포지션 정보 가져오기
        positions = client.futures_position_information()

        # 특정 심볼에 대한 포지션 검색
        for position in positions:
            if position['symbol'] == symbol:
                position_amt = float(position.get('positionAmt', 0.0))
                unrealized_profit = float(position.get('unRealizedProfit', 0.0))
                entry_price = float(position.get('entryPrice', 0.0))
                liquidation_price = float(position.get('liquidationPrice', 0.0))
                leverages = int(position.get('leverage', leverage))
                isolated = position.get('isolated', 'FALSE') == 'TRUE'

                # 포지션이 없는 경우
                if position_amt == 0:
                    print(f"{symbol}에 열린 포지션이 없습니다.")
                    return None

                # 디버깅용 로그
                print(f"[DEBUG] positionAmt: {position_amt}")
                print(f"[DEBUG] entryPrice: {entry_price}")
                print(f"[DEBUG] unRealizedProfit: {unrealized_profit}")
                print(f"[DEBUG] liquidationPrice: {liquidation_price}")

                # 수익률 계산
                pnl_percentage = 0.0
                if entry_price > 0 and abs(position_amt) > 0:
                    pnl_percentage = (unrealized_profit / (entry_price * abs(position_amt))) * 100 * leverages

                position_info = {
                    "symbol": symbol,
                    "positionAmt": position_amt,
                    "entryPrice": entry_price,
                    "unRealizedProfit": unrealized_profit,
                    "liquidationPrice": liquidation_price,
                    "leverage": leverage,
                    "isolated": isolated,
                    "PnL": round(pnl_percentage, 2),
                }

                # 결과 출력
                print("특정 심볼 포지션 정보:")
                print(position_info)
                return position_info

        # 심볼에 대한 포지션이 없는 경우
        print(f"{symbol}에 대한 포지션 정보가 없습니다.")
        return None

    except Exception as e:
        print(f"포지션 정보를 가져오는 중 오류 발생: {e}")
        return None


    except Exception as e:
        print(f"에러 발생: {e}")
        return None

# 테스트 실행
#get_all_positions()
#get_position_for_symbol("BCHUSDT")
#print(get_position_for_symbol("XRPUSDT"))
#get_position_for_symbol_with_pnl("ADAUSDT")
#positions = client.futures_position_information()
#print("API 응답 데이터 확인:")
#for pos in positions:
#    print(pos)
#if(get_position_for_symbol("XRPUSDT") != None):
#    print("해당 포지션 존재 함")
