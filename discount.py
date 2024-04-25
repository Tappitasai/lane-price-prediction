#discount based on the distance
def discount(val,rpm):
    total = val*rpm
    if val < 300:
        total = total - total*0.03
    elif val > 300 and val < 100:
        total = total - total*0.05
    else:
        total = total - total*0.1
    return total