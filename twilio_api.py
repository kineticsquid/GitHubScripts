import os
from twilio.rest import Client

def main():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    phone_numbers = client.incoming_phone_numbers.list()
    trunks = client.trunking.trunks.list()
    print("Retrieved %s phone numbers." % len(phone_numbers))
    print("Retrieves %s trunks." % len(trunks))

    for trunk in trunks:
        phone_numbers = trunk.phone_numbers.list()
        print(trunk.friendly_name)
        if len(phone_numbers) > 0:
            for number in phone_numbers:
                print("\t%s - %s" % (number.friendly_name, number.phone_number))
        else:
            print("\t** No associated phone numbers **")

if __name__ == '__main__':
    main()