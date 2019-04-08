import requests
import time
import pandas as pd
import os
from modle.ulity import getChinaTime


def get_candles(self, contract='okex/btc.usdt', since='2018-02-01', until=None, duration='1d'):
    ot_key = os.environ.get( 'OTK_EY' )

    if (until == None):
        until = getChinaTime()['day']
        print( until )

    url = 'http://hist-quote.1tokentrade.cn/candles?since={}&until={}&contract={}&duration={}&format=json'.format(
        since, until, contract, duration )

    r = requests.get( url, headers={'ot-key': ot_key} )

    if r.status_code != 200:
        print( 'fail get candles', r.status_code, r.text )
        return
    r = r.json()

    for i in range( len( r ) ):
        time_local = time.localtime( r[i]['timestamp'] )
        time_str = time.strftime( "%Y-%m-%d", time_local )
        r[i]['time'] = time_str

    candle_df = pd.DataFrame( r, \
                              columns=['time', 'close', 'open', 'high', 'low', 'volume'] )

    return candle_df