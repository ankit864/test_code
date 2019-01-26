from flask import Flask, render_template, redirect, request, url_for
import os
import subprocess
import crypt
import random
import string

app = Flask(__name__)

def random_string_generator(str_size):
    return ''.join(random.choice(string.ascii_letters) for x in range(str_size))


def crypt_password(password):
    salt_string = random_string_generator(16)
    print salt_string
    # print salt_string.len()
    crypted_password = crypt.crypt(password,salt_string)
    return crypted_password

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    try:
        if request.method == 'POST':
            username = request.form['user']
            password = request.form['password']
            crypted_password = crypt_password(password)
            print crypted_password
            shell = request.form['shell']
            sudo_access = request.form['sudo']
            home_dir = request.form['home']
            if sudo_access == "yes":
                cmd = "adduser -d " +  home_dir +  " -p " + crypted_password  + " -s " + shell + " -G wheel "+ username
                cmd_output = subprocess.check_output(cmd, shell=True)
            else:
                cmd = "adduser -d " +  home_dir +  " -p " + crypted_password  + " -s " + shell + " " + username
                cmd_output = subprocess.check_output(cmd, shell=True)
            return "user successfully created."
    except:
        return "Something went wrong user not created!!!!!"
    return render_template('add.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    try:
        if request.method == 'POST':
            username = request.form['user']
            cmd = "userdel " + username
            check_output = subprocess.check_output(cmd, shell=True)
            return "user deleted successfully"
    except:
        return "Something went wrong user not deleted!!!!!"
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
    app.run(host='0.0.0.0', port=5000, debug=True)
