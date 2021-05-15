
def printlog(adderss, message):
    with open(adderss, "w+") as f:
        f.write(message)
    