from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.config.mysqlconnection import connectToMySQL # Import your MySQL connection function
import boto3
import os

#defining what file extensions are allowed
ALLOWED_EXTENSIONS = {'png', 'jpeg'}
def allowed_file(filename):
    #taking the filename, indicating on what chracter I should use to breakdown the filename into multiple parts
    #then making everything lowercase for easier processing
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#boto3 is for connecting to AWS, s3
#initializing my s3 and defining variables for s3 bucket
#using flask os.getenv to get the access key and secret from my .env file
s3 = boto3.client('s3', 
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
                  aws_secret_access_key=os.getenv('AWS_SECRET'))



@app.route("/surfboards/new", methods = ['GET', 'POST'])
def index():
    mysql = connectToMySQL('s3bucket')
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if not allowed_file(uploaded_file.filename):
            return "FILE NOT ALLOWED"
        

        file = request.files['file']
        if file:
            # Upload file to S3
            s3.upload_fileobj(file, 'surfboardscodingdojo', file.filename)
            
            # Insert metadata into MySQL
            s3_url = f"https://surfboardscodingdojo.s3.amazonaws.com/{file.filename}"
            mysql = connectToMySQL('s3bucket')  
            query = "INSERT INTO s3bucket (file_name, s3_url) VALUES (%(file_name)s,%(s3_url)s );"
            data = {'file_name': file.filename, 's3_url': s3_url}
            mysql.query_db(query, data)
            try:
                result = mysql.query_db(query, data)
                print(f"Executing query: {query} with data: {data}")
                print("Insert result:", result)
            except Exception as e:
                print("Failed to insert into database:", e)
            return redirect('/')
        #retrieving S3 content links 
    query = "SELECT s3_url FROM s3bucket;"
    image_urls = mysql.query_db(query)
    print("Image URLs:", image_urls)
    #returning results as "image_urls"
    return render_template('index.html', image_urls=image_urls)