def ip_str2Int(ipstr):
    ch3 = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
    return ch3(ipstr)
