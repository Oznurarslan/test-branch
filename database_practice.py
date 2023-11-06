import datetime
import pyodbc

server = '172.30.134.12'
database = 'VALFSAN604T'
username = 'kemal'
password = '1212casecase..'

conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
#veri tabanı bağlantı cümleciği

users_data = [
    {"username": "user1", "status": "login"},
    {"username": "user2", "status": "login"},
    {"username": "user3", "status": "logout"},
    {"username": "user4", "status": "logout"},
    {"username": "user5", "status": "logout"}
]
#username kullanıcı adını status kullanıcı oturum bilgisini tanımlamış olup login(kullanıcı giriş) ve logout(kullanıcı çıkış) verilerini verir.

def cheksql(usernamef = '',passwordf = ''):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT USERNAME,PASSW FROM IASUSERS WHERE USERNAME = '{usernamef}' AND PASSW = '{passwordf}'")
        results = cursor.fetchone()
        return results
#kullanıcı adı ve şifre bilgisini ıasusers tablosundan çekerek doğruluğu kontrol eder


def insert_or_update_session(session={},dbtype=1):
    with conn.cursor() as cursor:
        if dbtype:
            cursor.execute("INSERT INTO VLFIOTLOGINSTATUS (USERID, LOGINTIME, LOGINSTATUS) VALUES (?, ?, ?)",
                           session["username"], session["login_time"], 1)
        else:
            current_time = datetime.datetime.now()
            cursor.execute("""
                UPDATE VLFIOTLOGINSTATUS 
                SET LOGOUTTIME = ?, LOGINSTATUS = 0 
                WHERE USERID = ?
                """, (current_time, session["username"]))
        conn.commit()
#bu tablo vlfıotlogınstatus tablosunda dbtype=1 olan giriş kaydı ekler bu kayıt kullanıcının adı(userıd),giriş zamanı(logıntime) ve giriş durumu(logınstatus)bilgisi içerir logınstatus 1 olarak auarlanır ve bu kullanıcının aktif olduğunu gösterir daha sonra çıkış işlemi yapar ve lologınstatus 0 olarak güncellenir

def get_logout_users():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM VLFIOTLOGINSTATUS WHERE LOGINSTATUS = 0")
        results = cursor.fetchall()
        return results
#logınstatus 0 olan kullanıcının sisteme giriş yapmış ve daha sonra çıkış yapmış olduğunu gösterir