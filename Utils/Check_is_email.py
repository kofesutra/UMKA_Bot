
def is_email_correct(email):
    if '@' in email and '.' in email.split('@')[1]:
        return True
    else:
        return False
