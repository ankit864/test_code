from flask import Flask, render_template, redirect, request, url_for
import os
import subprocess
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        shell = request.form['shell']
        sudo_access = request.form['sudo']
        home_dir = request.form['home']
        if sudo_access == "yes":
            returned_output = subprocess.check_output(cmd)
            print "adduser -d " +  home_dir +  " -p " + password  + " -s " + shell + " -G wheel "+ username
        else:
            print "adduser -d " +  home_dir +  " -p " + password  + " -s " + shell + " " + username

        # os.system("sudo useradd " +username)
        return "user successfully created."
    return render_template('add.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        username = request.form['user']
        os.system("sudo userdel " +username)
        return redirect(url_for('index'))
    return render_template('delete.html')

@app.route('/modify', methods=['GET', 'POST'])
def advanced_access():
    if request.method == 'POST':
        username = request.form['user']
        select_value = request.form["selectedopt"]
        modify_value = request.form["modify"]
        if select_value == "password":
            print 'echo ' + modify_value  + '| passwd --stdin ' + username
        print select_value
        # os.system("sudo usermod -a -G sudo " +username)
        return redirect(url_for('index'))


    return render_template('modify.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
