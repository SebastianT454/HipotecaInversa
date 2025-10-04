from flask import Flask, request, jsonify, send_from_directory
import random
import sys
sys.path.append('src')

from ReverseMortgage import MonthlyPayment
from model.User import User
from controller.Controlador_usuarios import ClientController

app = Flask(__name__, static_folder='../frontend', static_url_path='')
ClientController.create_table()

@app.route('/api/calculate', methods=['POST'])
def calculate():
    if MonthlyPayment is None:
        return jsonify({'status':'error','error':'ReverseMortgage module not available on server'}), 500
    data = request.get_json() or {}
    try:
        age = int(data.get('age',0))
        gender = data.get('gender','M')
        marital_status = data.get('marital_status','Single')
        spouse_age = data.get('spouse_age', None)
        spouse_age = int(spouse_age) if spouse_age not in (None, '', 'None') else None
        spouse_gender = data.get('spouse_gender', None)
        property_value = float(data.get('property_value',0))
        interest = float(data.get('interest_rate',0))
        
        # Generate unique ID
        user_id = str(random.randint(0, 9999999999)) # Random number of max 10 digits

        # Create User object
        user = User(
            id=user_id,
            age=str(age),
            gender=gender,
            marital_status=marital_status,
            spouse_age=str(spouse_age) if spouse_age is not None else None,
            spouse_gender=spouse_gender,
            property_value=str(property_value),
            interest_rate=str(interest)
        )
        print(user)
        # Insert user into database using insert_client method
        ClientController.insert_client(user)

        # Continue with existing calculation
        client = MonthlyPayment.Client(age, gender, marital_status, spouse_age, spouse_gender)
        reverse = MonthlyPayment.ReverseMortgage(int(property_value), float(interest), client)
        quotas = reverse.calculate_quotas()
        monthly_rate = reverse.calculate_monthly_rate()
        monthly_fee = reverse.calculate_monthly_fee()
        result = {
            'status':'ok',
            'quotas': quotas,
            'monthly_rate': monthly_rate,
            'monthly_fee': monthly_fee,
            'repr': str(reverse)
        }
        print("Usuario de la DB:", ClientController.find_client(user.id))
        return jsonify(result)
    except Exception as e:
        return jsonify({'status':'error','error': str(e)}), 400

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)