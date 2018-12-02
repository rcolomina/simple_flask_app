import string,random

ascii_uppercase="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ascii_lowercase="abcdefghijklmnopqrstuvwxyz"

def get_random_string(size=12,chars= ascii_uppercase + ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    
def get_random_email():
    return ''.join([get_random_string(),'@',
                    get_random_string(),'.',
                    get_random_string(size=3,chars=ascii_uppercase+ascii_lowercase)])

def get_random_contact_json():
    r_contact = {}
    r_contact['username'] = get_random_string()
    r_contact['email'] = [get_random_email(),get_random_email()] 
    r_contact['firstname'] = get_random_string()
    r_contact['surname'] = get_random_string()
    
    return r_contact

if __name__ == "__main__":
    print(get_random_contact_json())

