## Add the following methods to `twisted/names/client.py`
def getHostByNameV4(name, timeout=None, effort=10):
    return getResolver().getHostByNameV4(name, timeout, effort)
def getHostByNameV6Address(name, timeout=None, effort=10):
    return getResolver().getHostByNameV6Address(name, timeout, effort)
def getHostByName6(name, timeout=None, effort=10):
    return getResolver().getHostByName6(name, timeout, effort)
