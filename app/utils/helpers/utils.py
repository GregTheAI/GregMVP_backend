def generate_otp_code(length: int = 6) -> str:
    """
    Generate a random OTP code of specified length.
    :param length: Length of the OTP code to generate.
    :return: A string representing the OTP code.
    """
    import random
    import string

    if length <= 0:
        raise ValueError("Length must be a positive integer")

    otp_code = ''.join(random.choices(string.digits, k=length))
    return otp_code