import sys
import binascii
""" Refer sunny's document on how to decode camera serial ID """

def moduleSid_2str(filename):
    with open(filename, 'rb') as fsock:
        raw_data = fsock.read()
    # use module_flag to determine the serial number of camera module
    module_flag = bin(int(raw_data[229].encode('hex'),16))[2:].zfill(8) 
    # print module_flag
#    print binascii.hexlify(raw_data[230:232])
    if module_flag[0:2] == '01':
        year = str(int(binascii.hexlify(raw_data[244]), 16))
        week = str(int(binascii.hexlify(raw_data[245]), 16))
        number=binascii.hexlify(raw_data[246:248])        
        dec_number = int(number, 16) 
        # nvmfile = '6520018801BPRXNANA'+year+week+num2str(dec_number)
        nvmfile = '6520018801BPRXNANA' + year + week + number
        print number
    if module_flag[2:4] == '01':
        year = str(int(binascii.hexlify(raw_data[263]),16))
        week = str(int(binascii.hexlify(raw_data[264]),16))
        number=binascii.hexlify(raw_data[265:267])        
        dec_number = int(number, 16) 
        # nvmfile = '6520018801BPRXNANA'+year+week+num2str(dec_number)
        nvmfile = '6520018801BPRXNANA' + year + week + number
        print number
    if module_flag[4:6] == '01':
        year = str(int(binascii.hexlify(raw_data[282]),16))
        week = str(int(binascii.hexlify(raw_data[283]),16))
        number=binascii.hexlify(raw_data[284:286])        
        dec_number = int(number, 16) 
        # nvmfile = '6520018801BPRXNANA'+year+week+num2str(dec_number)
        nvmfile = '6520018801BPRXNANA' + year + week + number
        print number
    return nvmfile


def num2str(number):
    if len(str(number)) == 4:
        return str(number)
    else:
        return '0'*(4-len(str(number)))+str(number)


def main1():
    print moduleSid_2str(r'/Users/fanchang/Desktop/Phoenix/P2/FATP/SID/BSJ1P0M916232731_camera_module_sid')


def main2(camera_module_sid):
    print moduleSid_2str(camera_module_sid)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main2(sys.argv[1])
    else:
        main1()
