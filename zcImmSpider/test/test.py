s = 'http://liansai.500.com/zuqiu-4838/jifen-13090/'

i = s.find('jifen-')
print(i)
s = s[i+6:][:-1]
print(s)
# s = s[:10]
s = s[-5:]
print(s)
