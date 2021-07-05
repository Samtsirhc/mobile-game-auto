import os
import time

from nonebot import on_command, on_message, on_startswith
from nonebot.adapters import Bot, Event
from nonebot.rule import startswith, to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.utils import escape, unescape
from nonebot.adapters.cqhttp import MessageSegment
from .data import Question
from requests import get

answers = {}

def union(group_id, user_id):
    return (group_id << 32) | user_id


# recovery from database
for qu in Question.select():
    if qu.quest not in answers:
        answers[qu.quest] = {}
    answers[qu.quest][union(qu.rep_group, qu.rep_member)] = qu.answer

ask = on_message(priority=99)

@ask.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    a = await nothing()
    state = {'raw_message':str(event.get_message()), 'group_id':0,'user_id':0}
    state['user_id'] = int(event.get_user_id())
    session = str(event.get_session_id())
    if 'group' in session:
        state['group_id'] = int(session.split('_')[1])
    message = state['raw_message']
    if message.startswith('我问'):
        msg = message[2:].split('你答', 1)
        if len(msg) == 1:
            await ask.finish('发送“我问xxx你答yyy”我才能记住')
        q, a = msg
        if q not in answers:
            answers[q] = {}
        answers[q][union(state['group_id'], state['user_id'])] = a
        Question.replace(
            quest=q,
            rep_group=state['group_id'],
            rep_member=state['user_id'],
            answer=a,
            creator=state['user_id'],
            create_time=time.time(),
        ).execute()
        await ask.finish('好的我记住了')
    elif message.startswith('大家问') or message.startswith('有人问'):
        msg = message[3:].split('你答', 1)
        if len(msg) == 1:
            await ask.finish(f'发送“{message[:3]}xxx你答yyy”我才能记住')
        q, a = msg
        if q not in answers:
            answers[q] = {}
        answers[q][union(state['group_id'], 1)] = a
        Question.replace(
            quest=q,
            rep_group=state['group_id'],
            rep_member=1,
            answer=a,
            creator=state['user_id'],
            create_time=time.time(),
        ).execute()
        await ask.finish('好的我记住了')
    elif message.startswith('不要回答'):
        q = state['raw_message'][4:]
        ans = answers.get(q)
        if ans is None:
            await ask.finish('我不记得有这个问题')

        specific = union(state['group_id'], state['user_id'])
        a = ans.get(specific)
        if a:
            Question.delete().where(
                Question.quest == q,
                Question.rep_group == state['group_id'],
                Question.rep_member == state['user_id'],
            ).execute()
            del ans[specific]
            if not ans:
                del answers[q]
            await ask.finish(f'我不再回答“{a}”了')


        wild = union(state['group_id'], 1)
        a = ans.get(wild)
        if a:
            Question.delete().where(
                Question.quest == q,
                Question.rep_group == state['group_id'],
                Question.rep_member == 1,
            ).execute()
            del ans[wild]
            if not ans:
                del answers[q]
            await ask.finish(f'我不再回答“{a}”了')


@ask.handle()
async def answer(bot: Bot, event: Event, state: T_State):
    a = await nothing()
    state = {'raw_message':str(event.get_message()), 'group_id':0,'user_id':0}
    state['user_id'] = int(event.get_user_id())
    session = str(event.get_session_id())
    if 'group' in session:
        state['group_id'] = int(session.split('_')[1])
    ans = answers.get(state['raw_message'])
    if ans:
        a = ans.get(union(state['group_id'], state['user_id']))
        print(state['group_id'])
        if a:
            if state['group_id'] != 0:
                get(f'http://127.0.0.1:5700/send_group_msg?group_id={state["group_id"]}&&message={a}')
            else:
                get(f'http://127.0.0.1:5700/send_private_msg?&user_id={state["user_id"]}&message={a}')
            await ask.finish()
        a = ans.get(union(state['group_id'], 1))
        if a:
            get(f'http://127.0.0.1:5700/send_group_msg?group_id={state["group_id"]}&message={a}')
            await ask.finish()

async def nothing():
    return None
