import time
import os
from .data import Question
from nonebot import on_command, on_startswith, on_message
from nonebot.rule import to_me, startswith
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


answers = {}


def union(group_id, user_id):
    return (group_id << 32) | user_id


# recovery from database
for qu in Question.select():
    if qu.quest not in answers:
        answers[qu.quest] = {}
    answers[qu.quest][union(qu.rep_group, qu.rep_member)] = qu.answer


I_ask =  on_startswith("我问", priority=2)
everyone_ask =  on_startswith("大家问", priority=3)
no_reply = on_startswith("不要回答", priority=4)

@I_ask.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    message = str(event.get_message())
    session = str(event.get_session_id())
    context = {'group_id':'', 'user_id':''}
    if 'group_id' in session:
        session = session.split('_')
        context['group_id'] = session[1]
        context['user_id'] = session[2]
    else:
        context['user_id'] = session
    msg = message[2:].split('你答', 1)
    if len(msg) == 1:
        return {'reply': '发送“我问xxx你答yyy”我才能记住', 'at_sender': False}
    q, a = msg
    if q not in answers:
        answers[q] = {}
    answers[q][union(context['group_id'], context['user_id'])] = a
    Question.replace(
        quest=q,
        rep_group=context['group_id'],
        rep_member=context['user_id'],
        answer=a,
        creator=context['user_id'],
        create_time=time.time(),
    ).execute()
    return {'reply': '好的我记住了', 'at_sender': False}