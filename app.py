import json
from tokenize import Name
from flask import Flask, render_template, request
import pickle
import math
from datetime import date

app = Flask(__name__)
# load the model
# model = pickle.load(open('savedmodel.sav', 'rb'))


@app.route('/PremiumCalculation', methods=['POST'])
def predict():
    print(request.form);
    C_YoE = request.form.get("C_YoE")
    C_Education = request.form.get("C_Education")
    C_Income = request.form.get("C_Income")
    C_Age = request.form.get("C_Age")
    C_Gender = request.form.get("C_Gender")
    C_MStatus = request.form.get("C_MStatus")
    C_Parrent = request.form.get("C_Parrent")
    C_Location = request.form.get("C_Location")
    V_Vehicle_Ownership = request.form.get("V_Vehicle_Ownership")
    V_Vehicle_Manufacture_Year = request.form.get("V_Vehicle_Manufacture_Year")
    V_Estimated_Market_Value = request.form.get("V_Estimated_Market_Value")
    V_Vehicle_Type = request.form.get("V_Vehicle_Type")
    V_Model = request.form.get("V_Model")
    V_Make = request.form.get("V_Make")
    A_Violation_Code = request.form.get("A_Violation_Code")
    A_Number_of_Accidents = request.form.get("A_Number_of_Accidents")
    A_Number_of_Claims = request.form.get("A_Number_of_Claims")


    count = 0
    Severe = 0
    Rank = 0
    Penalty = 0
    Depreciation_Percentage = 0
   
    print(A_Violation_Code)
    json_object_A_Violation_Code = json.loads(A_Violation_Code)
    for i in json_object_A_Violation_Code:

        if i == 101:
            Severe 	= Severe +  8
            Rank 	= Rank  + 2
            Penalty = Penalty + 5000
            count = count + 1
        elif i == 102:
            Severe 	= Severe +  2
            Rank 	= Rank  + 2
            Penalty = Penalty + 5000
            count = count + 1
        elif i == 103:
            Severe 	= Severe +  1
            Rank 	= Rank  + 10
            Penalty = Penalty + 2000
            count = count + 1
        elif i == 104:
            Severe 	= Severe +  3
            Rank 	= Rank  + 7
            Penalty = Penalty + 2000
            count = count + 1
        elif i == 105:
            Severe 	= Severe +  1
            Rank 	= Rank  + 8
            Penalty = Penalty + 2000
            count = count + 1
        elif i == 106:
            Severe 	= Severe +  0
            Rank 	= Rank  + 16
            Penalty = Penalty + 0
            count = count + 1
        elif i == 107:
            Severe 	= Severe +  8
            Rank 	= Rank  + 1
            Penalty = Penalty + 25000
            count = count + 1
        elif i == 108:
            Severe 	= Severe +  4
            Rank 	= Rank  + 4
            Penalty = Penalty + 25000
            count = count + 1
        elif i == 109:
            Severe 	= Severe +  2
            Rank 	= Rank  + 6
            Penalty = Penalty + 25000
            count = count + 1
        elif i == 110:
            Severe 	= Severe +  1
            Rank 	= Rank  + 11
            Penalty = Penalty + 15000
            count = count + 1
        elif i == 111:
            Severe 	= Severe +  1
            Rank 	= Rank  + 12
            Penalty = Penalty + 25000
            count = count + 1
        elif i == 112:
            Severe 	= Severe +  1
            Rank 	= Rank  + 19
            Penalty = Penalty + 25000
            count = count + 1
        elif i == 113:
            Severe 	= Severe +  0
            Rank 	= Rank  + 23
            Penalty = Penalty + 10000
            count = count + 1
        elif i == 114:
            Severe 	= Severe +  0
            Rank 	= Rank  + 25
            Penalty = Penalty + 2000
            count = count + 1
        elif i == 115:
            Severe 	= Severe +  1
            Rank 	= Rank  + 24
            Penalty = Penalty + 2000
            count = count + 1
        elif i == 116:
            Severe 	= Severe +  1
            Rank 	= Rank  + 15
            Penalty = Penalty + 2000
            count = count + 1
        elif i == 117:
            Severe 	= Severe +  0
            Rank 	= Rank  + 21
            Penalty = Penalty + 2000
            count = count + 1
        elif i == 118:
            Severe 	= Severe +  0
            Rank 	= Rank  + 18
            Penalty = Penalty + 2000
            count = count + 1
        elif i == 119:
            Severe 	= Severe +  0
            Rank 	= Rank  + 17
            Penalty = Penalty + 1000
            count = count + 1
        elif i == 120:
            Severe 	= Severe +  5
            Rank 	= Rank  + 3
            Penalty = Penalty + 30000
            count = count + 1
        elif i == 121:
            Severe 	= Severe +  5
            Rank 	= Rank  + 3
            Penalty = Penalty + 25000
            count = count + 1

    # print(count)
    # print(math.ceil(Severe/count))
    # print(math.ceil(Penalty/count))
    # print(math.ceil(Rank/count))

    #model_severe = math.ceil(Severe/count)
    
    #Gender
    if C_Gender == 'male':
        C_Gender_Val = 1
    else:
        C_Gender_Val = 0



    model_rank = math.ceil(Rank/count)
    model_penalty = math.ceil(Penalty/count)

    
    #Customer Segment

    filename = 'customer_segment_model.sav'
    load_model = pickle.load(open(filename,'rb'))
    customer_segment = load_model.predict([[C_Gender_Val,model_rank,model_penalty]])
    C_customer_segment = customer_segment[0]


    if C_customer_segment == 0:#Safe
        C_customer_segment = -10
    elif C_customer_segment == 1:#Medium
        C_customer_segment = 5
    else:#Risky
        C_customer_segment = 20


    #Number of Accidents
    A_Number_of_Accidents = json.loads(A_Number_of_Accidents)
    if A_Number_of_Accidents >= 2:
        A_Number_of_Accidents_Percent = 15
    
    #Number of Claims
    A_Number_of_Claims = json.loads(A_Number_of_Claims)
    if A_Number_of_Claims >= 2:
        A_Number_of_Claims_Percent = 15


    #C_Education

    if C_Education == 'College':
        C_Education_Percentage = 9
    elif C_Education == 'University':
        C_Education_Percentage = 4
    else:
        C_Education_Percentage = 15
    

    #Age of Car
    todays_date = date.today()

    V_Vehicle_Manufacture_Year = json.loads(V_Vehicle_Manufacture_Year)
    Age_of_Car = todays_date.year - V_Vehicle_Manufacture_Year
  
    if Age_of_Car >= 0 and Age_of_Car <= 1:
        Depreciation_Percentage = 5 
    elif Age_of_Car > 1 and Age_of_Car <= 3:
        Depreciation_Percentage = 15 
    elif Age_of_Car > 3 and Age_of_Car <= 5:
        Depreciation_Percentage = 20 
    elif Age_of_Car > 5 and Age_of_Car <= 7:
        Depreciation_Percentage = 30 
    elif Age_of_Car > 7 and Age_of_Car <= 9:
        Depreciation_Percentage = 40     
    else:
        Depreciation_Percentage = 50


    #Year of Experience

    if C_YoE == '0-2y':
        C_YoE_Percent = 30
    elif C_YoE == '3-9y':
        C_YoE_Percent = 20
    elif C_YoE == '10-19y':
        C_YoE_Percent = 15
    elif C_YoE == '20-29y':
        C_YoE_Percent = 10
    elif C_YoE == '30y+':
        C_YoE_Percent = 0

    #Location
   
    if C_Location == 'Urban':
        C_Location_Percent = 5
    else: 
        C_Location_Percent = 0
    





    V_Estimated_Market_Value = json.loads(V_Estimated_Market_Value)
    #IDV = V_Estimated_Market_Value - (V_Estimated_Market_Value * Depreciation_Percentage/100)

    Depreciation_Percentage_Amount = V_Estimated_Market_Value * Depreciation_Percentage/100
    
    IDV = V_Estimated_Market_Value - Depreciation_Percentage_Amount

    Own_Damage_Premium = IDV * (1.970/100)

    NCB_Discount = Own_Damage_Premium * (10/100)

    Total_OD_Premium = Own_Damage_Premium - NCB_Discount

    GST = 10/100

    Compulsory_Third_Party_Cover = 1110

    Total_Premium = Total_OD_Premium + Compulsory_Third_Party_Cover

    Net_GST = Total_Premium * GST
    Net_C_YoE_Percent = Total_Premium * C_YoE_Percent/100
    Net_C_Location_Percent = Total_Premium * C_Location_Percent/100
    Net_C_customer_segment = Total_Premium * C_customer_segment/100
    Net_C_Education_Percentage = Total_Premium * C_Education_Percentage/100
    Net_A_Number_of_Accidents_Percent = Total_Premium * A_Number_of_Accidents_Percent/100
    Net_A_Number_of_Claims_Percent = Total_Premium * A_Number_of_Claims_Percent/100

    Total_Premium = Total_Premium + Net_GST + Net_C_YoE_Percent + Net_C_Location_Percent + Net_C_customer_segment + Net_C_Education_Percentage + Net_A_Number_of_Accidents_Percent + Net_A_Number_of_Claims_Percent

    Total_Premium = math.ceil(Total_Premium)
    Total_Premium_Str = str(Total_Premium)
    Total_Premium_Str
   
    print('Total_Premium_Str : ', Total_Premium_Str )
    return Total_Premium_Str, 200, {"Access-Control-Allow-Origin": "*"}
    

if __name__ == '__main__':
    app.run(debug=True)
