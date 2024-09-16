from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Agents, AnnouncedPollingUnitResults, LgaScores
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/austin/coding/Bincom_Flask_Task/data.sqlite"
app.config['SECRET_KEY'] =  os.getenv('secret_key')
db.init_app(app)


@app.route('/', methods=["GET", "POST"], strict_slashes=False)
def pl_unit_score():
    """returns the the score for the 
    polling unit by receiving polling unit ID from users
    """

    if request.method == 'POST':
        if request.form:
            pu_id = request.form.get('pol_unit_id')

            print(pu_id) ##################

            records_for_pu_id = AnnouncedPollingUnitResults.query.filter_by(polling_unit_uniqueid=pu_id).all()
            
            print(records_for_pu_id) ##################

            if not records_for_pu_id:
                flash("Invalid polling uniqueID")
                return render_template('individual_poll_unit.html')
            elif records_for_pu_id:
                return render_template('individual_poll_unit.html', records=records_for_pu_id, pu=pu_id)
        else:
            flash("polling unit uniqueID cannot be empty, please enter a value")
            return render_template('individual_poll_unit.html')
    else:
        return render_template('individual_poll_unit.html')
        
    
    
    
@app.route('/lga-total-results', methods=["GET", "POST"], strict_slashes=False)
def lga_results():
    """ view that returns the total score of a
     selected lga 
     """
    
    if request.method == 'POST':
    
        lga_input = request.form.get('local_government')
        print(lga_input) ##############
        lgas = LgaScores.query.filter_by(lga_name=lga_input).all()
        print(lgas)
        lga_scores_sum = sum([int(score.party_score) for score in lgas])
        print(lga_scores_sum)
        return render_template('local_govt.html', lga_scores_sum=lga_scores_sum, lgas=lgas, lga_input=lga_input)

    else:
        lgas = LgaScores.query.all()
        lgas_list = sorted(set([int(lga.lga_name) for lga in lgas]))
        print(lgas_list)

        return render_template('local_govt.html', lgas_list=lgas_list)


@app.route('/store-party-results', methods=["GET", "POST"], strict_slashes=False)
def store_party_results():
   
   """ view that gets accepts result data and for new polling units
    and store to the database
   """

   if request.method == "POST":
    
       if request.form:
           result_id = request.form.get("result_id")
           polling_unit_uniqueid = request.form.get("polling_unit_uniqueid")
           party_abbreviation = request.form.get("party_abbreviation")
           party_score = request.form.get("party_score")
           entered_by_user = request.form.get("entered_by_user")
           user_ip_address = request.form.get("user_ip_address")

           
           if not result_id:
               flash("please enter a polling unit result_id")

           if not polling_unit_uniqueid:
               flash("please enter a polling unit uniqueID")
               return render_template("store_party_results.html")
           if not party_abbreviation:
               flash("please enter a party abbreviation")
               return render_template("store_party_results.html")
           if not party_score:
               flash("please enter party score")
               return render_template("store_party_results.html")
           if not entered_by_user:
               flash("please enter the user entering the score")
               return render_template("store_party_results.html")
           if not user_ip_address:
               flash("please enter IP address")
               return render_template("store_party_results.html")
           
           party_score = int(party_score)
           result_id = int(result_id)
            
           scores = AnnouncedPollingUnitResults(polling_unit_uniqueid=polling_unit_uniqueid, party_abbreviation=party_abbreviation,
                                             party_score=party_score, entered_by_user=entered_by_user, user_ip_address=user_ip_address, result_id=result_id)
           print(polling_unit_uniqueid, party_abbreviation,
                                             party_score, entered_by_user, user_ip_address, result_id)
           
           try:
               db.session.add(scores)
               db.session.commit()
               flash("Successfully added new result")
               return redirect(url_for('pl_unit_score'))

           except Exception as e:
               db.session.rollback()
               flash(f"An error occurred: {e}")
               return render_template("store_party_results.html")
       else:
            return render_template("store_party_results.html")
       
   else:
       return render_template("store_party_results.html")




        #    db.session.add(scores)

        #    db.session.commit()
        #    flash("sucessfully added new result")
        #    return render_template("store_party_results.html")
       
        

       
        
    
   
        







if __name__ == "__main__":
    app.run(debug=True)
