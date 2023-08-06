import json

import requests
import traceback
import json
class XrpBalanceSpider:
    def __init__(self, print_flag=False):
        '''
        :param print_flag:
        '''
        self.print_flag = print_flag
        #need update
        with open('xrp_spider_pool.json', 'r') as f:
            pool = json.load(f)
        self.xrpApiPools = pool['api']

    def pprint(self,*args,**kwargs):
        if self.print_flag :
            print(*args,**kwargs)

    def getXRPBalance(self,address):
        '''
        :param adress:
        :return: XRP Balance
        '''
        url = self.xrpApiPools['XRP']
        balancePool = []
        try:
            self.pprint('{}/{}'.format(url,address))
            wbdata = requests.get('{}/{}'.format(url,address)).json()
            self.pprint(wbdata)
            balancePool.append(int(float(wbdata['xrpBalance'])*1000000))
            print(balancePool)
            return max(balancePool)
        except Exception:
            print('Get XRP Balance failed due to {}'.format(traceback.format_exc()))


if __name__ == '__main__':
    bb = XrpBalanceSpider(True)
    print(bb.getXRPBalance('rpzp36VUHCzYeTRuuVYGkzzBPAs2p8XK2A'))