def read(direct = "settings.ini"):
    with open(direct) as f:
        data = dict()
        for line in f.readlines():
            if '=' not in line:
                continue
            line = line.replace('\n','').replace(' ', '')
            key, value = line.split('=')
            data[key] = value
    f.close()
    return data

def save(data, direct = "settings.ini"):
    with open(direct, 'w') as f:
        for key in data:
            f.write(f"{key}={data[key]}\n")
    f.close()
