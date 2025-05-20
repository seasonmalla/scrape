from nepse import Nepse

nepse = Nepse()
nepse.setTLSVerification(False)
date='2025-05-19'

data = nepse.getMarketStatus()
print(data)