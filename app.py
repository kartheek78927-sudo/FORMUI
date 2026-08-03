from flask import Flask, render_template, request, redirect, url_for, flash, session
import secrets

app = Flask(__name__)
app.secret_key = 'replace-this-with-a-secure-key'

def login_required(view):
    def wrapped_view(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in before accessing the form.', 'error')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    wrapped_view.__name__ = view.__name__
    return wrapped_view

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        contact = request.form.get('contact', '').strip()
        if not contact:
            flash('Enter an email or phone number to receive an OTP.', 'error')
            return redirect(url_for('login'))

        otp = f"{secrets.randbelow(900000) + 100000}"
        session['otp'] = otp
        session['contact'] = contact
        flash('OTP generated and sent. For demo, the OTP is shown on the screen.', 'success')
        return redirect(url_for('verify'))

    return render_template('login.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'otp' not in session or 'contact' not in session:
        flash('Please start login first.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        code = request.form.get('otp_code', '').strip()
        if code == session.get('otp'):
            session['logged_in'] = True
            session['user_contact'] = session.get('contact')
            session.pop('otp', None)
            flash('Login successful! You can now access the form.', 'success')
            return redirect(url_for('index'))

        flash('OTP is incorrect. Please try again.', 'error')
        return redirect(url_for('verify'))

    return render_template('verify.html', otp=session.get('otp'), contact=session.get('contact'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user_contact=session.get('user_contact'))

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    user_data = {
        'full_name': request.form.get('full_name', ''),
        'email': request.form.get('email', ''),
        'phone': request.form.get('phone', ''),
        'address': request.form.get('address', ''),
        'city': request.form.get('city', ''),
        'state': request.form.get('state', ''),
        'zip_code': request.form.get('zip_code', ''),
        'country': request.form.get('country', ''),
        'birthdate': request.form.get('birthdate', ''),
        'gender': request.form.get('gender', ''),
        'occupation': request.form.get('occupation', ''),
        'company': request.form.get('company', ''),
        'website': request.form.get('website', ''),
        'about': request.form.get('about', ''),
    }

    missing = [key for key, value in user_data.items() if not value]
    if missing:
        flash('Please fill out all fields before submitting.', 'error')
        return redirect(url_for('index'))

    return render_template('success.html', user_data=user_data)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
