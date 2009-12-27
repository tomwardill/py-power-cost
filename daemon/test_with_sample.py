from convert_and_upload import convert_and_upload


def do(msg):

    return convert_and_upload(msg)
        
    #return convert_and_upload(test)

if __name__ == '__main__':
    f = open('sample.log')
    for msg in f.read().split('\n'):
    
        if msg:
            print do(msg)

