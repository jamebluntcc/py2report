import configparser
conf_command = configparser.ConfigParser()
conf_command.read('test.conf')

secs = conf_command.sections()
ans = conf_command.get('parmA','a')
print(ans)
