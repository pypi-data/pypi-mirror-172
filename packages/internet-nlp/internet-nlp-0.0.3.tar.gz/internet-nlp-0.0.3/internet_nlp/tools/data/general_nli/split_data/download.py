import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
import combine_data

NLIDTC = combine_data.NLIDataToCsv()

def downloadData(snliCsv, multinliCsv, anliCsv, dataCsv):
    NLIDTC.setSnliCsv(snliCsv)
    NLIDTC.setMultinliCsv(multinliCsv)
    NLIDTC.setAnliCsv(anliCsv)
    NLIDTC.setDataCsv(dataCsv)
    NLIDTC.doAllCommands()

downloadData("./snli.csv", "./multinli.csv", "./anli.csv", "./data.csv")
