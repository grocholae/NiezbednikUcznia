import bcrypt

def hash_password(password):
    """
    Kodowanie haseł pod przechowywanie ich w bazie danych
    :param password:
    :return:
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """
    Weryfikacja poprawności hasła
    :param password:
    :param hashed:
    :return:
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))