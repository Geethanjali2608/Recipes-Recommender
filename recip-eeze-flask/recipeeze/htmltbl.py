def mk_tbl(rows):
    #this function appends the appropriate column value to the array
    arr = []
    for row in rows:
        pred = row[1]
        ttl = row[2]
        r_t = row[7]
        p_t = row[5]
        c_t = row[6]
        url = row[10]
        arr.append([pred,ttl,r_t,p_t,c_t,url])
    return arr
