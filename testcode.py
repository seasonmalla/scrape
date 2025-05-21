from nepse import Nepse

nepse = Nepse()
nepse.setTLSVerification(False)
date='2025-05-17'

data = nepse.getPriceVolumeHistory(date)
print(data['content'])