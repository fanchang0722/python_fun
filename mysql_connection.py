import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'aura',
  'password': 'aura-mfg',
  'host': '173.194.232.122',
  'database': 'aura_mfg',
  'raise_on_warnings': True,
}

FF_SID = {}

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = "SELECT * FROM camera_sfr"
    cursor.execute(query)
    count = 0
    for line in cursor:
        if line[4] not in FF_SID:
            FF_SID[line[4]] = 1
            count += 1
        else:
            FF_SID[line[4]] += 1

    print("The total number of device is %d" % count)
    for k, v in FF_SID.items():
        print (k, v)
    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Password does NOT match")
    else:
        print("Something went wrong: {}".format(err))
finally:
    exit()
