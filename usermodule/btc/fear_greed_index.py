import requests
import time
import pandas as pd


class Fear_Greed_Index():
    def __init__(self):
        self.url = 'https://api.alternative.me/fng/'

    def getNewDataJson(self):
        r = requests.get( self.url )

        if r.status_code != 200:
            print( 'fail get fear_greed_index', r.status_code, r.text )
            return

        return r.json()['data'][0]

    def getLimitCSV(self,Limit):
        pass


    def getAllDf(self,limit = 0):
        url = (self.url+'?limit={}').format(limit)
        #print(url)
        r = requests.get(url)

        if r.status_code != 200:
            print( 'fail get fear_greed_index', r.status_code, r.text )
            return
        r = r.json()['data']

        for i in range( len( r ) ):
            times_tamp = int( r[i]['timestamp'] )
            time_local = time.localtime( times_tamp )
            time_str = time.strftime( "%Y-%m-%d", time_local )
            r[i]['time'] = time_str
            r[i]['value'] = int( r[i]['value'] )

        fgi = r[::-1]
        fgi_df = pd.DataFrame( fgi, columns=['time', 'value', 'value_classification'] )

        return fgi_df

    def fgi_plt_save(self):
        pass



def main():
    fgi = Fear_Greed_Index()
    print(fgi.getNewDataJson())



    # btc = BTCQuant()
    # fgi = BTCQuant.get_fear_greed_index()
    # print(fgi.tail())
    #
    # candle = BTCQuant.get_candles()
    #
    # print(candle.tail())
    #
    # res = pd.merge(fgi,candle)
    # print(res.head())
    #
    # res.to_csv(path_or_buf = './test.csv',index = False)
    # print('save csv done')
    #
    # res.plot(x = 'time',y = ['value','close'],\
    #          secondary_y=['value'], logy=True,grid = True)
    #
    #
    # plt.savefig('./plt')
    # print('plot save test.csv done')

if __name__ == '__main__':
    main()
