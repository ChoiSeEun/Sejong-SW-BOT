from operator import itemgetter
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
import re
import numpy as np
import csv
import cv2, os

api_key2 = '901492688:AAFyZ--uCmd4nMkg_a3PLNUINgY5YR-oKa4' # 조교 봇 키
bot2 = telegram.Bot(token=api_key2)                        # 조교 봇
updater2 = Updater(api_key2)                               # 조교 봇 업데이터

FIRST, SECOND = range(2)
PERMISSION = range(1)
MYPHOTO = range(1)

def handler(bot, update):
    text = update.message.text       # 보낸 메세지는 text에 저장된다
    sejongBot = update.message.chat_id # chat_id : 연결고리

    index = findNum(text)

    if index == -1:
        bot.send_message(chat_id=sejongBot, text='제가 모르는 문제예요.\n문제 번호를 다시 입력해주세요 ㅠㅠ.')
        return

    bot.send_message(chat_id=sejongBot, text=str(index)+'번 문제를 보내드리겠습니다.')
    bot.send_photo(chat_id=sejongBot, photo=open(question[index-1], 'rb'))

def findNum(text):
    number = re.findall('\d+', text)
    if not number:
        return -1
    elif 30 < int(number[0]):
        return -1
    else:
        number = int(number[0])
        return number
def add_command(bot, update):
    sejongCoBot = update.message.chat_id  # chat_id : 연결고리
    bot.send_message(chat_id = sejongCoBot, text ="세종대학교 소융대 조교봇입니다."
                                                  "\n답안을 추가하실 문제의 번호를 입력해주세요.")
    return FIRST

def first(bot,update):
    global index
    hint_num=1

    sejongCoBot = update.message.chat_id
    text = update.message.text       # 보낸 메세지는 text에 저장된다

    index=findNum(text)

    if index == -1:
        bot.send_message(chat_id=sejongCoBot,
                         text="저장되어 있는 문제의 번호를 입력해주세요.")
        return

    bot.send_message(chat_id=sejongCoBot,
                     text="입력하신 문제 번호는 "+str(index)+"번 입니다"
                          "\n해당 문제의 기존 답안을 보여드릴게요.")

    for i in data[index - 1]:
        bot.send_message(chat_id=sejongCoBot,
                         text='힌트 ' + str(hint_num) + ': ' + i[0] + '\n이 힌트에 투표한 학생 수 : ' + str(i[1]))
        hint_num += 1

    return SECOND

def second(bot,update):
    hint_num=1
    text = update.message.text
    sejongCoBot = update.message.chat_id

    tmp = [text, 0]
    data[index-1].append(tmp)

    bot.send_message(chat_id=sejongCoBot,
                     text= "\""+text+"\""+ "가 해당 문제의 답안으로 추가되었습니다.")
    # for i in data[index - 1]:
    #     bot.send_message(chat_id=sejongCoBot,
    #                      text='힌트 ' + str(hint_num) + ': ' + i[0] + '\n이 힌트에 투표한 학생 수 : ' + str(i[1]))
    #     hint_num += 1
    return -1

def done_command(bot, update):
    sejongCoBot = update.message.chat_id
    bot.send_message(chat_id=sejongCoBot,
                     text = "항목 입력을 종료하겠습니다.")
    return -1

def save_command(bot, update):
    with open('myData.csv','w',newline='') as f:
        makeWrite = csv.writer(f)

        for value in data:
            data2=[]
            for cell in value:
                data3=cell[0]+':'+str(cell[1])
                data2.append(data3)

            makeWrite.writerow(data2)
    sejongBot = update.message.chat_id  # chat_id : 연결고리
    bot.send_message(chat_id=sejongBot, text="추가된 답안이 저장되었습니다.")
def findNumList(text):
    number = re.findall('\d+', text)
    for i in number:
        if not i:
            return -1
        elif int(i)>30:
            return -1

    return number
def pms_command(bot, update):
    sejongCoBot = update.message.chat_id  # chat_id : 연결고리
    bot.send_message(chat_id = sejongCoBot, text ="세종대학교 소융대 조교봇입니다."
                                                  "\n모범답안 접근권한을 변경할 문제들의 번호를 입력해주세요.")
    return PERMISSION

def permission_command(bot, update):
    sejongCoBot = update.message.chat_id
    text = update.message.text

    indexList = findNumList(text)

    with open("bestAnswer.csv", 'r') as f:
        reader = csv.reader(f)
        answerList=list(reader)
        for index in indexList:
            index=int(index)
            pms = answerList[index - 1][1]

            if (int(pms)):
                answerList[index - 1][1] = '0'
            else:
                answerList[index - 1][1] = '1'

    with open('bestAnswer.csv','w',newline='') as f:
        makeWrite = csv.writer(f)
        for value in answerList:
            makeWrite.writerow(value)
    bot.send_message(chat_id=sejongCoBot, text="해당 문제들의 모범답안 권한이 변경되었습니다.")
    return -1

def pmsList_command(bot, update):
    sejongCoBot = update.message.chat_id

    with open("bestAnswer.csv", 'r') as f:
        reader = csv.reader(f)
        answerList=list(reader)
        idx=0
        tmp=""
        for row in answerList:
            idx+=1
            if row[1] == '0':
                tmp = tmp + str(idx) + "번 : 불가\n"
            else:
                tmp = tmp + str(idx) + "번 : 가능\n"
    bot.send_message(chat_id=sejongCoBot, text=tmp)

    return -1
def aQ_command(bot, update):
    sejongCoBot = update.message.chat_id
    bot.send_message(chat_id=sejongCoBot, text="추가할 문제의 사진을 보내주세요.")

    return MYPHOTO

def get_photo(bot, update):
    global filename
    global ext
    global ori_img
    global src
    file_path = os.path.join('', 'abc.jpg')
    photo_id = update.message.photo[-1].file_id  # photo 번호가 높을수록 화질이 좋음
    photo_file = bot.getFile(photo_id)
    photo_file.download(file_path)

    img_path = 'abc.jpg'
    filename, ext = os.path.splitext(os.path.basename(img_path))
    ori_img = cv2.imread(img_path)
    src = []

    cv2.namedWindow('img')
    cv2.setMouseCallback('img', mouse_handler)

    cv2.imshow('img', ori_img)
    cv2.waitKey(0)
    return -1
def mouse_handler(event, x, y, flags, param):
  global ori_img
  global src
  global filename
  global ext
  if event == cv2.EVENT_LBUTTONUP:
    img = ori_img.copy()

    src.append([x, y])

    for xx, yy in src:
      cv2.circle(img, center=(xx, yy), radius=5, color=(0, 255, 0), thickness=-1, lineType=cv2.LINE_AA)

    cv2.imshow('img', img)

    # perspective transform
    if len(src) == 4:
      src_np = np.array(src, dtype=np.float32)

      width = max(np.linalg.norm(src_np[0] - src_np[1]), np.linalg.norm(src_np[2] - src_np[3]))
      height = max(np.linalg.norm(src_np[0] - src_np[3]), np.linalg.norm(src_np[1] - src_np[2]))

      dst_np = np.array([
        [0, 0],
        [width, 0],
        [width, height],
        [0, height]
      ], dtype=np.float32)

      M = cv2.getPerspectiveTransform(src=src_np, dst=dst_np)
      result = cv2.warpPerspective(ori_img, M=M, dsize=(width, height))

      cv2.imshow('result', result)
      cv2.imwrite('image\\31.jpg', result)
    return -1
with open("myData.csv",'r') as f:
    # reader = 파일 전체 / data = 구조체 2차원 배열 / row = csv를 위에서 부터 한 행씩 불러온 것
    # cell = csv 상에서 한 칸 / struct = 구조체 1개 / data2 = 구조체로 이루어진 한 행
    reader = csv.reader(f)
    data = []
    for row in reader:
        data2=[]
        for cell in row:
            struct=[]
            struct=cell.split(':')
            struct[1]=int(struct[1])
            data2.append(struct)
        data.append(data2)

question = []
for i in range (1, 31):
    question.append('image\\'+str(i)+'.jpg')

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add_command)],
    states={
     FIRST: [MessageHandler(Filters.text, first)],
     SECOND: [MessageHandler(Filters.text, second)]
    },
    fallbacks=[CommandHandler('done', done_command)]
)
conv_handler2 = ConversationHandler(
    entry_points=[CommandHandler('pms', pms_command)],
    states={
     PERMISSION: [MessageHandler(Filters.text, permission_command)]
    },
    fallbacks=[CommandHandler('done', done_command)]
)
conv_handler3 = ConversationHandler(
    entry_points=[CommandHandler('add_Question', aQ_command)],
    states={
     MYPHOTO: [MessageHandler(Filters.photo, get_photo)]
    },
    fallbacks=[CommandHandler('done', done_command)]
)
global ori_img
global src
global filename
global ext

updater2.dispatcher.add_handler(conv_handler)
updater2.dispatcher.add_handler(conv_handler2)
updater2.dispatcher.add_handler(conv_handler3)

updater2.dispatcher.add_handler(MessageHandler(Filters.text, handler))   # 메세지가 입력되었을 때 불릴 핸들러
updater2.dispatcher.add_handler(CommandHandler('save',  save_command))
updater2.dispatcher.add_handler(CommandHandler('pmsList',  pmsList_command))
updater2.start_polling()                                                 # 조교 봇에 주기적으로 텔레그램에 접근해서 메세지가 있다면 받아와라
updater2.idle()