from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import Form
from flask_wtf import FlaskForm
from flask_wtf import Form
import pandas as pd
import boto3

whitelist = ['mfairch@givens.com']

def send_email(email,orgin,dest, miles):
    client = boto3.client('ses')
    response = client.send_email(
        Destination={
            'ToAddresses': [
                'jack@givens.awsapps.com'
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': f'<p>A potential customer, {email}, wants to load moved from {orgin} to {dest}, a total of {miles} miles.</p><br><p> Here are their additional comments: XXXXX </p><br><p>Here is the average rate from DAT given total miles, orgin, and destination: $XXXXX</p>',
                    
                },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': 'This is for those who cannot read HTML.',
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Qoute Form Input',
            },
        },
        Source='jack.dunlap2@gmail.com',)




# CREATE APP
app = Flask(__name__)
app.secret_key = "jndlap"

# PAGE ONE
@app.route('/')
def index():
    return render_template('index.html')

# THANK YOU PAGE
@app.route('/thankyou', methods=['POST', 'GET'])
def thankyou():
    email = str(request.form['email'])
    miles = str(request.form['miles'])
    dest = str(request.form['dest'])
    orgin = str(request.form['orgin'])

    if email is not None:
        send_email(email,orgin,dest, miles)
    
    for email_ in whitelist:
        if email == email_:
            flash(f"Thank you {str(request.form['email'])}, please check your email for an demo qoute alert")
        
    return render_template('thankyou.html', email = email)


app.run(debug=True)
