#coding=utf-8
import mysql.connector

config = {
    'host': '118.89.54.75',
    'user': 'cyy',
    'password': 'slXXiqtFrSN1jS2O.',
    'port': 3306,
    'database': 'video',
    'charset': 'utf8'
}

#connect MySQL
def mysql_conn():
    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect error!{}'.format(e))
        return None
    else:
        #print('connect success!')
        return conn

#close connector
def mysql_close(conn):
    '''
    :param conn: mysql_connector
    :return:
    '''
    if conn.is_connected:
        conn.close()

    #print('connect close!')

#MySQL select
def mysql_sel(conn, sqlStr, param):
    '''
    :param conn: mysql_connector
    :param sqlStr: sql命令
    :param param: 参数
    :return: results or None
    '''
    if not conn.is_connected():
        print("Connection is disconnected")
        return None
    cursor = conn.cursor()
    #print(sqlStr+str(param))
    try:
        cursor.execute(sqlStr, param)
        results = cursor.fetchall()
    except mysql.connector.Error as e:
        print('query error!{}'.format(e))
        return None
    else:
        return results
    finally:
        cursor.close()

#Mysql insert
def mysql_ins(conn, sqlStr, param):
    '''
    :param conn: mysql_connector
    :param sqlStr: sql命令
    :param param: 参数
    :return: 0失败/1成功
    '''
    if not conn.is_connected():
        print("Connection is disconnected")
        return 0
    cursor = conn.cursor()
    # print(sqlStr+str(param))
    try:
        cursor.execute(sqlStr, param)
        conn.commit()
    except mysql.connector.Error as e:
        print('insert error!{}'.format(e))
        conn.rollback()
        return 0
    else:
        return 1
    finally:
        cursor.close()

#Mysql update
def mysql_upd(conn, sqlStr, param):
    '''
    :param conn: mysql_connector
    :param sqlStr: sql命令
    :param param: 参数
    :return: 0失败/1成功
    '''
    if not conn.is_connected():
        print("Connection is disconnected")
        return 0
    cursor = conn.cursor()
    # print(sqlStr+str(param))
    try:
        cursor.execute(sqlStr, param)
        conn.commit()
    except mysql.connector.Error as e:
        print('update error!{}'.format(e))
        conn.rollback()
        return 0
    else:
        return 1
    finally:
        cursor.close()

#Mysql delete
def mysql_del(conn, sqlStr, param):
    '''
    :param conn: mysql_connector
    :param sqlStr: sql命令
    :param param: 参数
    :return: 0失败/1成功
    '''
    if not conn.is_connected():
        print("Connection is disconnected")
        return 0
    cursor = conn.cursor()
    # print(sqlStr+str(param))
    try:
        cursor.execute(sqlStr, param)
        conn.commit()
    except mysql.connector.Error as e:
        print('delete error!{}'.format(e))
        conn.rollback()
        return 0
    else:
        return 1
    finally:
        cursor.close()