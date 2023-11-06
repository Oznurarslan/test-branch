from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from datetime import datetime
from database_practice import cheksql, insert_or_update_session, get_logout_users

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Parameters:
     giriş sayfasını yönetmek için kullanılır
     get ile erişildiğinde giriş sayfasını gösterir
     post ile erişildiğinde giriş sayfasının gönderimini sağlar
     bunların kontrolünü sağladıktan sonra başarılı olursa gösterge paneline atar

     Returns:
      get herhangi bir mesaj ile geri dönüş sağlar    """
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        usernamef = request.form['username']
        passwordf = request.form['password']
        results = cheksql(usernamef,passwordf)
        if results:
            session['loggedin'] = True
            session['id'] = usernamef
            session['username'] = usernamef
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msg = 'Logged in successfully !'
            insert_or_update_session(session,1)
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect username / password !'
            return render_template('login.html', msg=msg)
    return render_template('login.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    """ Parameters
   kullanıcı eğer giriş yaptıysa gösterge paneli sağlanır

    return:
        Kullanıcı giriş yapmışsa: Güncel zaman ile birlikte gösterge paneli şablonunu render eder.
        Kullanıcı giriş yapmamışsa: Giriş sayfasına yönlendirir."""
    if 'login_time' in session:
        return render_template('pres-secim-ekrani.html', current_time=session['login_time'])
    else:
        return redirect(url_for('login'))

@app.route('/parca_secim_ekrani')
def parca_secim_ekrani():
    """ Parameters:
    Yalnızca giriş yapmış kullanıcılar için erişilebilir olan parça seçim ekranı için rota.

    Return:
        Kullanıcı giriş yapmışsa: Güncel zaman ile birlikte parça seçim ekranı şablonunu render eder.
        Kullanıcı giriş yapmamışsa: Giriş sayfasına yönlendirir."""
    if 'login_time' in session:
        return render_template('parca-secim-ekrani.html', current_time=session['login_time'])
    else:
        return redirect(url_for('login'))

@app.route('/talimatlar')
def talimatlar():
    """Parameters:
    yalnızca giriş yapmış kullanıcılar için erişilebilir olan talimatlar ekranı için sağlanan rota

     Returns:
      kullanıcı giriş yapmışsa: Güncel zaman ile birlikte talimatlar ekranını render eder    """
    if 'login_time' in session:
        return render_template('talimatlar.html')
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Parameters:
    yeni kullanıcı kayıtlarını işlemek için kullanılır
    get ile erişildiğinde kayıt sayfasını gösterir
    post ile erişildiğinde kayıt formu gönderimini işler

    Returns: get ile kayıt sayfasını render eder post ile ise bu kısımda uygulama gerektirir"""
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']



@app.route('/logout')
def logout():
    """Parameters:
    kullanıcıyı çıkış yapmak için kullanılan rotadır oturum durumunu günceller ve tarayıcıdaki oturumu session.pop metodu ile temizler

    Returns: giriş sayfasına yönlendirme sağlar  """
    if 'username' in session:
        insert_or_update_session(session,0)
        # logout_users = get_logout_users()
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        session.pop('login_time', None)
    return redirect(url_for('login'))






if __name__ == '__main__':
    app.run(debug=True)



