#
# Write data to an ini file
#
def write_ini_file(filename, data):
    with open(filename, 'w') as ini_file:
        for section, properties in data.items():
            ini_file.write('[' + section + ']\n')
            for k, v in properties.items():
                ini_file.write(k + '=' + str(v) + "\n")
            ini_file.write('\n')
