from flask import Flask, escape, request, render_template
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/prediction', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        gender = request.form['gender']
        marrried_status = request.form['married_status']
        dependents = request.form['dependents']
        eduaction = request.form['eduaction']
        self_employed = request.form['self_employed']
        credit_history = request.form['credit_history']
        property_area = request.form['property_area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # gender
        if (gender == "Male"):
            Male = 1
        else:
            Male = 0

        # married
        if (marrried_status == "Yes"):
            marrried_status_yes = 1
        else:
            marrried_status_no = 0

        # dependents
        if (dependents == '1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif (dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif (dependents == '3+'):
            dependents_1 = 0    
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0   
            dependents_3 = 0

        # education
        if (eduaction == "Not Graduate"):
            graduate = 1
        else:
            not_graduate = 0

        # self_employed
        if (self_employed == "Yes"):
            self_employed_yes = 1
        else:
            self_employed_no = 0

        # property area
        if (property_area == "Semiurban"):
            semiurban = 1
            urban = 0
        elif(property_area == "Urban"):
            semiurban = 0
            urban = 1
        else:
            semiurban = 0
            urban = 0

        ApplicantIncomeLog = np.log(ApplicantIncome)
        TotalIncomeLog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountLog = np.log(LoanAmount)
        Loan_Amount_Term_Log = np.log(Loan_Amount_Term)

        inp=np.array([[credit_history, ApplicantIncomeLog, LoanAmountLog, Loan_Amount_Term_Log, TotalIncomeLog]])
        prediction = model.predict(inp)

        if (prediction == "N"):
            prediction = "No"
        else:
            prediction = "Yes" 

        return render_template("prediction.html", prediction_text = "loan status is {}".format(prediction))
    

    return render_template("prediction.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000,debug=True)


