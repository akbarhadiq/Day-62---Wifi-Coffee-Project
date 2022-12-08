from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv
from load_dotenv import load_dotenv
import os

load_dotenv('environ.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)


class CafeForm(FlaskForm):

    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)',validators=[DataRequired()])
    opening_time = StringField('Opening Time, e.g 9AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time, e.g 9PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[('☕️'), ('☕️☕️'), ('☕️☕️☕️'), ('☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️')], validators=[DataRequired()])
    wifi_rating = SelectField('WiFi Rating', choices=[('🔌'), ('🔌🔌'), ('🔌🔌🔌'), ('🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    power_rating = SelectField('Power Rating', choices=[('💪'), ('💪💪'), ('💪💪💪'), ('💪💪💪💪'), ('💪💪💪💪💪')], validators=[DataRequired()])
        
    submit = SubmitField('Submit')
    
# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():

        print("True")
        cafe_name=form.cafe.data
        cafe_location=form.location.data
        opening_time=form.opening_time.data
        closing_time = form.closing_time.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi_rating.data
        power_rating = form.power_rating.data

        cafe_data_as_list = [cafe_name, cafe_location, opening_time, closing_time, coffee_rating, wifi_rating, power_rating]

        # Open our existing CSV file in append mode
        # Create a file object for this file
        with open('cafe-data.csv', 'a', encoding='utf-8') as file:
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = csv.writer(file)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(cafe_data_as_list)

            # close file object
            file.close()

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit() done.
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
