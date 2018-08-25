from login import Login
from Pub import Pub
from confing import Config
from utlis.dama import YDMHttp
import os
import time

conf = Config()
config = conf.config
ydm = YDMHttp()


def get_all_session(all_account,text):
    session = []
    ydm.text=text
    for user in all_account:
        login = Login(ydm)
        if not user:
            continue
        try:
            username, password = all_account.get(user)
        except Exception as e:
            text.insert('end', "获取账户信息错误，请检查账户,错误信息{}\n".format(str(e)))
            text.update()
            continue
        login_status = login.login(username, password)
        if login_status["code"] == 0:
            session.append(login_status["session"])
            text.insert('end', "{}登陆成功\n".format(user))
            text.update()
        else:
            text.insert('end', "用户{}登录失败，请检查账户正确性，以及是否有登录保护\n".format(user))
            text.update()
    return session


def get_all_video():
    video_list = os.listdir(config["path"]["video"])
    return video_list


def run(all_account, video_type,text,time_):
    all_session = get_all_session(all_account,text)
    all_video = get_all_video()
    if not all_session:
        text.insert('end', "没有可用的账号\n")
        text.update()
        return ""
    while all_video:
        video = all_video.pop(0)
        session = all_session.pop(0)
        if len(video)>33:
            text.insert('end', "{}标题超过30个字跳过\n".format(video))
            text.update()
            continue
        text.insert('end', "{}开始上传\n".format(video))
        text.update()
        try:
            pub = Pub(video, session, ydm)
        except:
            text.insert('end', "{}上传视频失败\n".format(video))
            text.update()
            all_video.append(video)
            time.sleep(10)
            all_session.append(session)
            continue
        text.insert('end', "{}开始发布\n".format(video))
        text.update()
        status = pub.pub(str(video_type), text)
        if status == 22:
            text.insert('end', "{}发文上限，切换帐号，\n".format(video))
            text.update()
            all_video.append(video)
            continue
        if status == 10:
            all_video.append(video)
            all_session.append(session)
            continue
        if not status:
            # all_video.append(video)
            all_session.append(session)
            text.insert('end', "{}发文失败请等待完成后，重新发布，\n".format(video))
            text.update()
            continue
        text.insert('end', "{}上传成功\n".format(video))
        text.update()
        all_session.append(session)
        time.sleep(time_)


if __name__ == '__main__':
    a = [1,2,3,4]
    while a:

        print(a.pop())
    print(1111)


