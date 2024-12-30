import logging
import requests
from bs4 import BeautifulSoup
import time
import threading
from collections import defaultdict
import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from datetime import datetime, timedelta
import g4f

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
file_handler = logging.FileHandler('bot.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def write_msg(peer_id, message):
    vk.method('messages.send', {'peer_id': peer_id, 'message': message, 'random_id': 0})


key = 'vk1.a.5xdkXpJP_X0eCNetM_zLAy38WFdVZOsCt1Pcy5-jFZXJDm3x9r9e9p4RVl6MTReuI9dKOfbt3xPFES016WeBHVrWT5OsDr-ebAiR3hfceQWUwLy703PTywr44XW3czjjXjLp9_9WcoS66fROUtOyLsWQilDkhGhCM7rqPHCi6RgK8AC3uvsi872iGD-TpLvZdqozon0e6njXKZWiBd9AKw'
url = 'https://forum.mordor-rp.com/index.php?reports/'
url_1 = 'https://forum.mordor-rp.com/index.php?reports/closed'
url_2 = 'https://forum.mordor-rp.com/index.php?forums/Общая-курилка.560/'
url_3 = 'https://forum.mordor-rp.com/index.php?forums/Транспорт.178/'
url_4 = 'https://forum.mordor-rp.com/index.php?forums/Недвижимость.179/'
url_5 = 'https://forum.mordor-rp.com/index.php?forums/Предприятия.180/'
url_6 = 'https://forum.mordor-rp.com/index.php?forums/Аксессуары-Одежда-Материалы.320/'
url_7 = 'https://forum.mordor-rp.com/index.php?whats-new/latest-activity'
url_8 = 'https://forum.mordor-rp.com/index.php?forums/Жалобы-на-модераторов-форума.310/'
url_9 = 'https://forum.mordor-rp.com/index.php?members/romeo-auditore.110059/'
url_10 = 'https://forum.mordor-rp.com/index.php?members/enrique_thompson.74606/'
url_11 = 'https://forum.mordor-rp.com/index.php?members/kirill_veselov.70053/'
url_12 = 'https://forum.mordor-rp.com/index.php?members/adam_raizen.52477/'
url_13 = 'https://forum.mordor-rp.com/index.php?forums/Заявления-модерации.704/'
last = ['лох', 'шлюха', 'мать', 'пидорас']
user_agents = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 "
               "Safari/537.36 OPR/105.0.0.0")

vk = vk_api.VkApi(token=key)
longpoll = VkBotLongPoll(vk, 226970140)


def log_message(request, peer_id, user_id):
    user_info = vk.method('users.get', {'user_ids': user_id})
    username = user_info[0]['first_name'] + ' ' + user_info[0]['last_name']
    if peer_id == 2000000006:
        peer_id = 'Репорт'
    elif peer_id == 2000000006:
        peer_id == 'Курилка'
    logger.info(f"Сообщение от {username} (ID: {user_id}) in chat {peer_id}: {request}")


cookies = {
    'xf_csrf': 'v7sngPZ2rs1wcmeS',
    'xf_session': 'e_M0rUQKO4k_9q5TMKQ3bevARmT69myE'
}


# def parse_forum_messages():
#     i = 0
#     response = requests.get(url_13, cookies=cookies)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     block = soup.find_all('span', class_='structItem-pageJump')
#     links = block[2]
#     temp = links.find_all('a')
#     link_1 = f'https://forum.mordor-rp.com{temp[0].get('href')}'
#     link_2 = f'https://forum.mordor-rp.com{temp[1].get('href')}'
#     link_3 = f'https://forum.mordor-rp.com{temp[2].get('href')}'
#     response_1 = requests.get(link_1, cookies=cookies)
#     soup_1 = BeautifulSoup(response_1.text, 'html.parser')
#     article_1 = soup_1.find_all('div', class_='message-content js-messageContent')
#     while len(article_1) > i:
#         message = article_1[i].text
#         i += 1
#         write_msg(647539469, message)
#     i = 0
#     response_2 = requests.get(link_2, cookies=cookies)
#     soup_2 = BeautifulSoup(response_2.text, 'html.parser')
#     article_2 = soup_2.find_all('div', class_='message-content js-messageContent')
#     while len(article_2) > i:
#         message = article_2[i].text
#         i += 1
#         write_msg(647539469, message)
#     i = 0
#     response_3 = requests.get(link_3, cookies=cookies)
#     soup_3 = BeautifulSoup(response_3.text, 'html.parser')
#     article_3 = soup_3.find_all('div', class_='message-content js-messageContent')
#     while len(article_3) > i:
#         message = article_3[i].text
#         i += 1
#         print(len(article_3))
#         write_msg(647539469, message)
    # write_msg(647539469, f'Первая ссылка {link_1}\n'
    #                      f'Вторая ссылка {link_2}\n'
    #                      f'Третья ссылка {link_3}\n')


def send_weekly_report():
    week = get_week()
    counter = counter1()
    text = (f'✨ Статистика обработки жалоб на форуме за неделю ✨\n\n'
            f'📊 Всего обработано: {counter}\n\n')
    for name, count in week:
        text += f'🔹{name} — 📝{count} жалоб(а)\n'
    write_msg(2000000006, text)


def check_time_for_weekly_report():
    while True:
        now = datetime.now()
        if now.weekday() == 6 and now.hour == 23 and now.minute == 59:
            send_weekly_report()
            time.sleep(60)
        time.sleep(1)


def get_status_():
    response_1 = requests.get(url_9, cookies=cookies)
    response_2 = requests.get(url_10, cookies=cookies)
    response_3 = requests.get(url_11, cookies=cookies)
    response_4 = requests.get(url_12, cookies=cookies)
    soup_1 = BeautifulSoup(response_1.text, 'html.parser')
    soup_2 = BeautifulSoup(response_2.text, 'html.parser')
    soup_3 = BeautifulSoup(response_3.text, 'html.parser')
    soup_4 = BeautifulSoup(response_4.text, 'html.parser')
    dox_1 = soup_1.find('div', class_='memberHeader-main')
    dox_2 = soup_2.find('div', class_='memberHeader-main')
    dox_3 = soup_3.find('div', class_='memberHeader-main')
    dox_4 = soup_4.find('div', class_='memberHeader-main')
    status_1 = dox_1.find('dd').text
    status_2 = dox_2.find('dd').text
    status_3 = dox_3.find('dd').text
    status_4 = dox_4.find('dd').text

    return status_1, status_2, status_3, status_4


def get_message():
    response = requests.get(url=url_7, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.find('div', class_='contentRow-title')
    full_link = link.find_all('a')[0].find_next('a').get('href')
    data = soup.find('div', class_='contentRow-snippet').text
    for item in last:
        if item in data:
            return item, full_link
    return None, None


class DialogueBuffer:
    def __init__(self, word_limit=100):
        self.messages = []
        self.word_limit = word_limit

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_history(self):
        return self.messages

    def remaining_words(self):
        total_words = sum(len(message['content'].split()) for message in self.messages)
        return self.word_limit - total_words

    def is_within_limit(self):
        return self.remaining_words() > 0


# Инициализация буфера с лимитом слов
dialogue_buffer = DialogueBuffer(word_limit=10000)


def ai_response(message):
    try:
        # Добавляем сообщение пользователя в буфер
        dialogue_buffer.add_message("user", message)

        if not dialogue_buffer.is_within_limit():
            return "Достигнут лимит слов. Пожалуйста, начните новый диалог."

        # Получаем историю сообщений для API
        messages_for_api = dialogue_buffer.get_history()

        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=messages_for_api
        )

        print("Response from API:", response, dialogue_buffer.is_within_limit())

        if isinstance(response, str):
            return response

        elif isinstance(response, dict) and 'choices' in response:
            ai_message = response['choices'][0]['message']['content']
            # Добавляем ответ AI в буфер
            dialogue_buffer.add_message("assistant", ai_message)
            return ai_message

        else:
            return "Неизвестный формат ответа от API."

    except Exception as e:
        logger.error(f"Error in AI response: {e}")
        return "Извините, возникла ошибка при обработке вашего запроса."


def get_aks():
    response = requests.get(url=url_6, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find('div', class_='structItemContainer-group js-threadList')
    if data is None:
        return 1, 1
    else:
        first = data.find('div', class_='structItem-title')
        l = first.find_all('a')[0].find_next('a').get('href')
        answers = data.find('dd').text
        return l, answers


def get_pred():
    response = requests.get(url=url_5, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find('div', class_='structItemContainer-group js-threadList')
    if data is None:
        return 1, 1
    else:
        first = data.find('div', class_='structItem-title')
        l = first.find_all('a')[0].find_next('a').get('href')
        answers = data.find('dd').text
        return l, answers


def get_ned():
    response = requests.get(url=url_4, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find('div', class_='structItemContainer-group js-threadList')
    if data is None:
        return 1, 1
    else:
        first = data.find('div', class_='structItem-title')
        l = first.find_all('a')[0].find_next('a').get('href')
        answers = data.find('dd').text
        return l, answers


def get_transport():
    response = requests.get(url=url_3, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find('div', class_='structItemContainer-group js-threadList')
    if data is None:
        return 1, 1
    else:
        first = data.find('div', class_='structItem-title')
        l = first.find_all('a')[0].find_next('a').get('href')
        answers = data.find('dd').text
        return l, answers


def get_smoking():
    response = requests.get(
        url='https://forum.mordor-rp.com/index.php?forums/%D0%9E%D0%B1%D1%89%D0%B0%D1%8F-%D0%BA%D1%83%D1%80%D0%B8%D0%BB%D0%BA%D0%B0.560/',
        cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    sort = soup.find('div', class_='structItemContainer-group js-threadList')
    a = sort.find('a', class_="").get('href')
    answers = sort.find('dl', class_='pairs pairs--justified')
    answers_1 = int(answers.find('dd').text.strip())
    return f'https://forum.mordor-rp.com{a}', answers_1


def get_week():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    response = requests.get(url_1, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    name_counts = defaultdict(int)

    data = soup.find_all('div', class_='structItem structItem--report')
    for item in data:
        time_element = item.find('time', class_='structItem-latestDate u-dt')
        if time_element:
            date_str = time_element['data-date-string']
            date_obj = datetime.strptime(date_str, '%d.%m.%Y')

            if start_of_week.date() <= date_obj.date() <= end_of_week.date():
                step = item.find('div', class_='structItem-cell structItem-cell--latest')
                if step:
                    step1 = step.find('div', class_='structItem-minor').text.strip()
                    name_counts[step1] += 1

    sorted_names = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_names


def get_status():
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find('div', class_='p-pageWrapper')

    ll = data.find('div', class_='xb-page-wrapper')
    two = ll.find('div', class_='structItem-cell structItem-cell--main')
    status = two.find('li').text
    return status.strip()


def get_report_data():
    try:
        response = requests.get(url, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find('div', class_='p-pageWrapper')
        line = soup.find_all('div', class_='structItem-cell structItem-cell--latest')

        one = data.find('a').get('data-badge')
        if one is None:
            one = 0
        ll = data.find('div', class_='xb-page-wrapper')
        two = ll.find('div', class_='structItem-cell structItem-cell--main')
        link = two.find('a').get('href')
        full_link = 'https://forum.mordor-rp.com' + link

        hrefs = []
        for item in line:
            a_tag = item.find('a')
            if a_tag:
                href = a_tag.get('href')
                if href:
                    full_href = 'https://forum.mordor-rp.com' + href
                    hrefs.append(full_href)

        return one, full_link, hrefs
    except AttributeError:
        logging.info("Обновите куки")


def get_report_on_moderators():
    response = requests.get(url_8, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    data_1 = soup.find_all("div", class_='structItemContainer-group js-threadList')
    data = data_1[0]
    report = data.find('div', class_='structItem-title')
    link = report.find('a').get('href')
    full_link = 'https://forum.mordor-rp.com' + link
    answers = data.find('dl', class_='pairs pairs--justified')
    answers_1 = int(answers.find('dd').text.strip())
    title = report.text
    return full_link, answers_1, title.strip()


def check_for_new_reports_on_moderators(last_link):
    link, answers, title = get_report_on_moderators()
    if link != last_link and answers == 0:
        write_msg(2000000009, f'❄️⛄️Пришла новая жалоба на модератора ⛄️❄️\n'
                              f'\n🔷🎅{title}🎅\n'
                              f'🔷 {link}\n')
        return link
    return last_link


def check_for_new_reports(last_link):
    try:
        one, link, hrefs = get_report_data()
        status = get_status()
        if link != last_link and status == 'Открыто':
            message = (f' 🚨@all Поступила новая жалоба!🚨\n\n'
                       f'Уже: {one} жалоб\n\n'
                       f'🔗 Ссылка(и) на рассмотрение:\n') if int(one) >= 3 else (
                f'🚨@online Поступила новая жалоба!🚨\n\n'
                f'🔗 Ссылка(и) на рассмотрение:\n')
            for i, href in enumerate(hrefs, start=1):
                if i <= int(one):
                    message += f'{i}. {href}\n'
            write_msg(2000000006, message)
            return link
        return last_link
    except Exception:
        logging.info("Проверка жалоб не работает")


def check_aks(last_link):
    link, answers = get_aks()
    if link != last_link and int(answers) == 0:
        write_msg(2000000005, f'@online Создана новая тема в Аксессуарах/Одежде/Материалах:\n'
                              f'Ссылка на тему: https://forum.mordor-rp.com{link[0:-5]}')
        return link
        logging.info(f"Создана тема в Аксессуарах/Одежде/Материалах")
    return last_link


def check_ned(last_link):
    link, answers = get_ned()
    if link != last_link and int(answers) == 0:
        write_msg(2000000005, f'@online Создана новая тема в Недвижимости:\n'
                              f'Ссылка на тему: https://forum.mordor-rp.com{link[0:-5]}')
        return link
        logging.info(f"Создана тема в Недвижимости")
    return last_link


def check_ts(last_link):
    link, answers = get_transport()
    if link != last_link and int(answers) == 0:
        write_msg(2000000005, f'@online Создана новая тема в Транспорте:\n'
                              f'Ссылка на тему: https://forum.mordor-rp.com{link[0:-5]}')
        return link
        logging.info(f"Создана тема в Транспорте")
    return last_link


def check_pred(last_link):
    link, answers = get_pred()
    if link != last_link and int(answers) == 0:
        write_msg(2000000005, f'@online Создана новая тема в Предприятиях:\n'
                              f'Ссылка на тему: https://forum.mordor-rp.com{link[0:-5]}')
        return link
        logging.info(f"Создана тема в Предприятиях")
    return last_link


def check_for_new_titles(last_link):
    link, answers = get_smoking()
    if link != last_link and answers == 0:
        write_msg(2000000005, '@online Создана новая тема в Курилке!\n'
                              f'Ссылка на тему: {link}\n')
        return link
        logging.info(f"Создана тема в Курилке")
    return last_link


def counter1():
    counter = 0
    week = get_week()
    for name, count in week:
        counter += count
    return counter


is_ai_active = False
ai_thread = None


# write_msg(2000000006, "Бот активирован")
# write_msg(2000000005, "Бот активирован")


def listen_for_messages():
    global is_ai_active

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            request = event.object.message['text']
            peer_id = event.object.message['peer_id']
            user_id = event.object.message['from_id']
            log_message(request, peer_id, user_id)
            if request.lower() == 'жалобы':
                one, link, _ = get_report_data()
                status = get_status()
                message = (f'✨ Текущая статистика жалоб ✨\n\n'
                           f'🔢Количество жалоб: {int(one)}\n'
                           f'🔗Последняя жалоба: {link}\n')
                if status == "Решено":
                    message += "📌Статус жалобы: Решено ✔️"
                elif status.startswith("Обрабатывается"):
                    message += "📌Статус жалобы: Обрабатывается ⚙️"
                elif status == "Открыто":
                    message += "📌Статус жалобы: Открыто  🗸️"
                else:
                    message += "📌Статус жалобы: Отказано ❌"
                write_msg(peer_id, message)
            elif request.lower() == 'send':
                write_msg(2000000006, 'А вы пожелали сладких снов всем своим близким?\n'
                                      'Напишите ответ: Да/Нет')

            elif request.lower() == 'отчеты':
                week = get_week()
                counter = counter1()
                text = (f'✨ Статистика обработки жалоб на форуме ✨\n\n'
                        f'📊 Всего обработано: {counter}\n\n')
                for name, count in week:
                    text += f'🔹{name} — 📝{count} жалоб(а)\n'
                write_msg(peer_id, text)

            elif request.lower().startswith('привет'):
                user_info = vk.method('users.get', {'user_ids': user_id})
                username = user_info[0]['first_name'] + ' ' + user_info[0]['last_name']
                write_msg(peer_id, f'Ну привет, {username}')

            # elif request.lower() == "начдиалог":
            #
            #     is_ai_active = True
            #
            #     write_msg(peer_id, "AI диалог начат.")
            #
            #     continue
            #
            # elif request.lower() == "закдиалог":
            #
            #     is_ai_active = False
            #     write_msg(peer_id, "AI диалог завершен.")
            #     continue
            #
            #     # Respond with AI if active
            #
            # elif is_ai_active and (request.startswith('[club226970140|MRP BOT]') or request.startswith('mbot')):
            #     ai_reply = ai_response(request)
            #     write_msg(peer_id, ai_reply)
            #     continue
            #
            # elif is_ai_active == False and (
            #         request.startswith('[club226970140|MRP BOT]') or request.startswith('mbot')):
            #     write_msg(peer_id, "Нужно включить AI\n"
            #                        "Команда - начдиалог")

            elif request.lower() == 'ponline':
                Shamarov, Vlad, Kirill, Misha = get_status_()
                write_msg(peer_id, f'🎅❄️ Online Head Stuff ❄️🎅\n\n'
                                   f'🔹Roman Shamarov - {Shamarov.strip()}\n\n'
                                   f'🔹Vladimir Putin - {Vlad.strip()}\n\n'
                                   f'🔹Kirill Veselov - {Kirill.strip()}\n\n'
                                   f'🔹Micheal Muchamed - {Misha.strip()}\n\n')

            # elif request.lower() == 'работа':
            #     try:
            #         parse_forum_messages()
            #     except Exception as e:
            #         print(e)
            elif request.lower() == 'пока':
                write_msg(peer_id, 'Иди в задницу, Миша!')


message_thread = threading.Thread(target=listen_for_messages)
message_thread.start()

weekly_report_thread = threading.Thread(target=check_time_for_weekly_report)
weekly_report_thread.start()

last_link_aks = ""
last_link_ned = ""
last_link_ts = ""
last_link_pred = ""
last_link_reports = ""
last_link_titles = ""
last_link_reports_moderators = ""

while True:
    last_link_aks = check_aks(last_link_aks)
    last_link_ned = check_ned(last_link_ned)
    last_link_ts = check_ts(last_link_ts)
    last_link_pred = check_pred(last_link_pred)
    last_link_reports = check_for_new_reports(last_link_reports)
    last_link_titles = check_for_new_titles(last_link_titles)
    last_link_reports_moderators = check_for_new_reports_on_moderators(last_link_reports_moderators)
    time.sleep(5)
