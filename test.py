from zxcvbn import zxcvbn

result = zxcvbn('passwordsssss')

print(result)
print(result["guesses_log10"])