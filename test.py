from operator import itemgetter
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler, CommandHandler, conversationhandler
import numpy as np

api_key2 = '901492688:AAFyZ--uCmd4nMkg_a3PLNUINgY5YR-oKa4' # 조교 봇 키
bot2 = telegram.Bot(token=api_key2)                        # 조교 봇
updater2 = Updater(api_key2)                               # 조교 봇 업데이터
updater2.start_polling()                                   # 조교 봇에 주기적으로 텔레그램에 접근해서 메세지가 있다면 받아와라

def handler(bot, update):
    global solveNum  # 현재 풀고 있는 문제의 번호
    global nowSolve  # 현재 풀고 있는 문제의 답안

    text = update.message.text       # 보낸 메세지는 text에 저장된다
    sejongBot = update.message.chat_id # chat_id : 연결고리

    index = findNum(text)

    if index == -1:
        bot.send_message(chat_id=sejongBot, text=emojize('제가 도움을 드릴 수가 없어요\n유효한 문제번호를 입력해주세요:sweat_smile:',use_aliases=True))
        return

    solveNum = int(index)
    nowSolve = solve[index-1] # 문제의 번호는 1번부터 시작한다. 1번을 입력했을 때 list의 0번 원소를 선택해야한다.
    bot.send_message(chat_id=sejongBot, text=emojize(str(index)+'번 문제의 오류 케이스를 빈도 순으로 알려드릴게요. 파이팅!:clap:',use_aliases=True))
    hint_num = 1
    for i in solve[index-1]:
        bot.send_message(chat_id=sejongBot, text = '힌트 ' + str(hint_num) + ': ' + i[0] + '\n이 힌트에 투표한 학생 수 : ' + str(i[1]))
        hint_num += 1

    button_list = build_button(["네", "아니오"])
    show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list)-1))
    update.message.reply_text("해결이 되셨나요?", reply_markup = show_markup)

solve = [[['이렇게 저렇게 해보세요.', 0], ['이 케이스를 입력해보세요', 0], ['초기화는 잘 하셨나요?', 0]],
         [['초기화는 잘 하셨나요?', 0], ['반복문의 범위가 중요한 문제예요!', 0], ['이 케이스를 입력해보세요.', 0]],
         [['초기화는 잘 하셨나요?', 0], ['볼빨간 사춘기 노래를 들어보세요.', 0], ['조건문의 범위가 중요한 문제예요!', 0]],
         [['함수에서 변수의 값을 변경하는 방법을 알아보세요!', 0], ['이 케이스를 입력해보세요.', 0]],
         [['수식 관리가 중요한 문제예요!', 0], ['시간은 시, 분, 초 로 나눌 수 있어요 !', 0]],
         [['조건문의 범위가 중요한 문제예요!', 0], ['딘 노래를 들어보세요.', 0], ['이렇게 저렇게 해보세요.', 0]]]

updater2.dispatcher.add_handler(MessageHandler(Filters.text, handler))   # 메세지가 입력되었을 때 불릴 핸들러
