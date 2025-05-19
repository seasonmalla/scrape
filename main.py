import sys
import os
from nepse import Nepse

nepse = Nepse()
nepse.setTLSVerification(False)
data='2025-05-19'
print(nepse.getPriceVolumeHistory(data))
