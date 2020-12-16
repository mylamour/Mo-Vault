# import yara

def malware(filepath):
    # rule = yara.compile(source='rule foo: bar {strings: $a = "lmn" condition: $a}')
    # matches = rule.match(data='abcdefgjiklmnoprstuvwxyz')

    print(filepath)

    return False