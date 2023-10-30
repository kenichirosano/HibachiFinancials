def fiscalYearCovnert(year, month):
    if month >= 7:
        return year
    else:
        return year + 1

def yyyymm_ReturnYear(yyyymm):
    if int(yyyymm[-2:]) >= 7:
        return int(yyyymm[0:4])
    else:
        return int(int(yyyymm[0:4]) -1)
