import os

def main(request_input):

    print("Request Input:")
    print(request_input)
    print("Environment Variables:")
    for key in os.environ.keys():
        print("%s - %s" %  (key, os.environ[key]))
    return {"statusCode": 200, "body": "Test Really is OK"}

if __name__ == '__main__':
    main({"foo": "bar"})
