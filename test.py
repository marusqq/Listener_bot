try:
    import socks
except ImportError:
    print('import failed')
    import pysocks
    pass

print(socks.HTTP)