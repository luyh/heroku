import time
from hpg import HPG
from hpg.zkb import ZKB


if __name__ == '__main__':
    hpg = HPG()
    zkb = ZKB()

    time.sleep(10)
    hpg.driver.quit()
    zkb.driver.quit()
