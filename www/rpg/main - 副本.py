import copy
import json
import xlrd

outList = []
line0 = {}
txtDict = {}
roleDict = {'黄2':1, '绿':2, '蓝':3, '金':4, '水晶':5, '路比':6, '沙菲雅':7, '米拉特':8, '沙菲雅树叶':7, '士兵1':9, '士兵2':9, '莉拉':10}
blockStart = 0
blockId = 1
lastLeft = {}
lastRight = {}
fileNum = 0

def wrap(string, max_width):
    result1 = [string[i:i + max_width] for i in range(0, len(string), max_width)]
    result = '\n'.join(result1)
    return result
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def readJsonBaseData(filename):
    with open(file=filename, mode='r',encoding='utf-8') as f:
        roleData = json.load(f)
    # 0 黄 1 绿 2 蓝 3 金 4 水晶 5 路比 6 沙菲雅 7 米拉特 8 路人
    return roleData

def addBlock(block):
    global blockId, outList
    block['blockId'] = blockId
    blockId = blockId + 1
    outList.append(copy.deepcopy(block))
    return block

def addOneLine(role, face, txt):
    global blockId, roleDict, roleConfigData, txtDict, blockStart,outList,lastLeft,lastRight
    num = roleDict[role] - 1
    if len(txt) > 24:
        txt = wrap(txt,24)
    tempRole = copy.deepcopy(roleConfigData[num])
    tempRole['eventData']['imageName'] = f'{role}_{face}'
    tempRole['eventData']['blockStart'] = blockStart
    tempTxt = copy.deepcopy(txtDict)

    if num == 0:  # 当说话角色为黄时
        tempTxt['eventData']['messageText'] = f'【黄】\n{txt}'
    elif num == 6:
        tempTxt['eventData']['messageText'] = f'【沙菲雅】\n{txt}'
    else:
        tempTxt['eventData']['messageText'] = f'【{role}】\n{txt}'
    tempTxt['eventData']['blockStart'] = blockStart
    tempRole = copy.deepcopy(addBlock(tempRole))
    addBlock(tempTxt)
    if num == 0: #当说话角色为黄时
        lastLeft = copy.deepcopy(tempRole)
        if len(lastRight) != 0:
            lastRight['eventData']['blockStart'] = blockStart
            addBlock(lastRight)
    else:
        lastRight = copy.deepcopy(tempRole)
        if len(lastLeft) != 0:
            lastLeft['eventData']['blockStart'] = blockStart
            addBlock(lastLeft)
    blockStart = blockStart + 16 # 一个block的固定时长


def saveFile():
    global outList, txtDict, line0,blockStart, blockId, lastLeft, lastRight, fileNum
    filename = f'{fileNum}.json'
    fileNum = fileNum + 1
    with open(file=filename, mode='w') as f:
        # obj：欲存储为json格式的数据，fp：欲存储的文件对象
        json.dump(obj=outList, fp=f)
    outList.clear()
    blockStart = 0
    blockId = 1
    lastLeft = {}
    lastRight = {}

def readLogFile(filename):
    talkData = xlrd.open_workbook(filename)
    table = talkData.sheet_by_name('Sheet1')
    # 获取总行数
    nrows = table.nrows
    # 获取总列数
    ncols = table.ncols
    lastIsEmpty = True
    for number in range(1, nrows):
        if not len(table.cell(number, 4).value) == 0 :
            role = table.cell(number, 4).value
            face = table.cell(number, 5).value
            txt = table.cell(number, 6).value
            addOneLine(role, face, txt)
            lastIsEmpty = False
        else:
            if not lastIsEmpty:
                saveFile() #保存out文件
                lastIsEmpty = True
    # 获取一行的全部数值，例如第5行
    #row_value = table.row_values(5)
    # 获取一列的全部数值，例如第6列
    #col_values = table.col_values(6)
    # 获取一个单元格的数值，例如第5行第6列
    #cell_value = table.cell(5, 6).value



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #global roleConfigData, txtDict, outList, line0
    print_hi('PyCharm')
    roleConfigData = readJsonBaseData('roleConfig.json')
    txtDict = readJsonBaseData('txtConfig.json')[0] # 文字配置文件，只有一个文字block块
    readLogFile('c1.xls')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
