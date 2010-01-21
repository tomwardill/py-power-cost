from convert_and_upload import convert_and_upload
from convert_and_upload import bulk_convert_and_upload

def do(msg):

    #return convert_and_upload(msg)
    return bulk_convert_and_upload(msg)


    #return convert_and_upload(test)

if __name__ == '__main__':
    f = open('sample.log')
    
    do(f.read().split('\n'))

