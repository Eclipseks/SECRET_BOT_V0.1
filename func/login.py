import requests

def check_acs(login):
    try:
        headers = {
            'accept': 'application/json',
            'Authorization': 'key 2aeef075-5e8b-40ea-a978-a65137c5d0e8',
        }

        params = {
            'format': 'json',
        }

        response = requests.get('https://pridelounge.api.enes.tech/account/', params=params, headers=headers)
        
        for acount in response.json():
            if acount['login'] == str(login):
                return acount
    except:
        return {'name': 'Error', 'last_name': 'Error', 'middle_name': None, 'login': 'Error', 'birth_date': 'Error', 'email': 'Error', 'gender': 'Error', 'phone_number': 'Error', 'registration_date': 'Error', 'account_amount': 'Error', 'last_login_date': 'Error', 'number_of_visits': 0}

def check_all_amount(login):
    try:
        headers = {
            'accept': 'application/json',
            'Authorization': 'key 2aeef075-5e8b-40ea-a978-a65137c5d0e8',
        }

        params = {
            'format': 'json',
        }

        response = requests.get(f'https://pridelounge.api.enes.tech/account/{login}/balance-history/', params=params, headers=headers)
        amount = float()
        for data in response.json():
            if data["action_name"] == "Поповнення балансу":
                amount += float(data["spent_sum"]) 
        return amount
    except:
        return 0.0
