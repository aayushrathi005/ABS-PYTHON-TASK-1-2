def check_password_strength(password):
    length = len(password) >= 8
    contain_upper = any(char.isupper() for char in password)
    contain_lower = any(char.islower() for char in password)
    contain_digit = any(char.isdigit() for char in password)
    contain_spec_char = any(char in '!@#$%^&*<>/-' for char in password)

    if length and contain_upper and contain_lower and contain_digit and contain_spec_char:
        return "Strong Password"
    elif length and (contain_upper or contain_lower) and contain_digit:
        return "Moderate Password"
    elif length and (contain_upper or contain_lower) and contain_spec_char:
        return "Moderate Password"
    else:
        return "Weak Passowrd"
password = input("Enter a Paswword: ")
print("")
print("Password Strength: ", check_password_strength(password))