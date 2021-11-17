import os

cur_path = os.path.abspath(os.path.dirname(__file__))
files = os.listdir(cur_path)
py_files = []
i = 0

print('将要执行程序：')
for file in files:
    file_path = os.path.join(cur_path, file)
    if 'checkin' in file and file.endswith('.py') and os.path.isfile(file_path):
        print(file)
        py_files.append(file_path)
        i += 1

print('\n\n*****开始执行*****\n\n')

m = 0
for py in py_files:
    # print(py)
    os.system('python ' + py)
    m += 1

if i == m:
    print('\n\n*****全部程序执行完毕*****')
    print('*****共计' + str(m) + '个程序*****')
else:
    print('\n\n 少执行了程序？！')
