import logging
import os
import cv2


def log(level, content):
    logging.basicConfig(level=logging.DEBUG,filename='upload.log',filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    if level == 'warn':
        logging.warning(content)
    elif level == 'error':
        logging.error(content)
    elif level == 'debug':
        logging.debug(content)
    elif level == 'info':
        logging.info(content)
    else:
        logging.critical(content)


def retry(func):

    def repeat(*args, **kwargs):
        error = ''
        for i in range(3):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error = e
                log('warn', 'because {} : {} retry, args is {}'.format(e, i, args))

        raise Exception(error)
    return repeat


def screen_shot(filename, png):
    vc = cv2.VideoCapture(filename)  # 读入视频文件
    vc.isOpened()
    vc.isOpened()
    vc.set(cv2.CAP_PROP_POS_FRAMES, 100)
    ret, im = vc.read()
    png_path = png
    cv2.imwrite(png_path, im)
    vc.release()
    return png_path


def rm(path):
    os.remove(path)


if __name__ == '__main__':
    screen_shot("..\\video\\小品《相亲进行曲》宋小宝 赵海燕 闫光明.mp4",'')