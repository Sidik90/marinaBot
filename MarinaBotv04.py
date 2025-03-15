import telebot
import logging
import os
from dotenv import load_dotenv
from telebot import types

logging.basicConfig(level=logging.DEBUG)
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

# Словари вопросов для каждой темы:
questions_gastro = {
    "Избыточная потливость беспокоит вас?":"Это может указывать на окислительный стресс и перегрузку систем детоксикации. Печень, почки и кишечник могут быть не в состоянии эффективно выводить токсины. Рекомендуется сдать анализы на биохимию крови для оценки функции печени и почек. Консультация с нутрициологом поможет улучшить ваше питание и поддержать работу органов детоксикации.",
    "В уголках рта часто появляются трещины (заеды)?":"Это может свидетельствовать о дисбиозе кишечника и дефиците витамина B2. Рекомендуется консультация врача и сдача анализов на уровень витаминов и микроэлементов. Консультация с нутрициологом также поможет сбалансировать ваш рацион.",
    "Страдаете от частых головных болей?":"Головные боли могут быть признаком проблем с детоксикацией или углеводным обменом. Также это может быть связано с накоплением аммиака или ацетона. Необходимо сдать анализы крови на метаболиты и проконсультироваться с нутрициологом. Консультация с нутрициологом поможет оценить ваш рацион и внести необходимые изменения.",
    "Изменения в стуле, такие как диарея или запор, стали частыми?":"Это может быть связано с нарушением работы желчного пузыря или непереносимостью определенных продуктов. Рекомендуется провести анализ на выявление непереносимости продуктов и обратиться к гастроэнтерологу. Консультация с нутрициологом поможет оптимизировать ваше питание.",
    "Мучает метеоризм?":"Метеоризм может быть следствием пищевой непереносимости или синдрома избыточного бактериального и грибкового роста в кишечнике. Необходимо провести тест на непереносимость пищи и дисбактериоз. Консультация с нутрициологом поможет выявить причины и предложит рацион для улучшения состояния.",
    "Часто испытываете отрыжку или изжогу?":"Эти симптомы могут быть связаны с пониженной кислотностью в желудке или гастроэзофагеальным рефлюксом. Рекомендуется консультация с гастроэнтерологом и, при необходимости, гастроскопия. Консультация с нутрициологом поможет выявить конкретные триггеры в питании.",
    "Боли в животе от спазмов и газов беспокоят вас?":"Это может указывать на проблемы с желчным пузырем или наличие бактериального/грибкового роста в кишечнике. Также не исключен паразитоз. Рекомендуется сдать соответствующие анализы и сделать УЗИ органов брюшной полости. Консультация с нутрициологом поможет скорректировать питание.",
    "Есть белый налет на языке?":"Это часто указывает на кандидоз и проблемы с кислотностью желудка. Необходимо провести анализы на наличие грибковых инфекций и проконсультироваться с нутрициологом. Консультация с нутрициологом поможет скорректировать ваш питание для восстановления здоровья.",
    "Обратите внимание на цвет склер глаз — они желтоватые?":"Это может указывать на синдром Жильбера или проблемы с желчным пузырем. Рекомендуется проведение биохимического анализа крови и консультация с нутрициологом для исключения серьезных заболеваний.",
    "Кал не тонет и пачкает унитаз?":"Это может быть признаком ферментативной недостаточности или проблем с оттоком желчи. Рекомендуется сдать анализ кала на содержание жиров и ферментов, а также проконсультироваться с гастроэнтерологом.",
    "Пятки слишком сухие и появляются натоптыши?":"Это может свидетельствовать о проблемах с желчным пузырем и дефиците жирорастворимых витаминов. Рекомендуется сдать анализы на витамины и желчные кислоты и обсудить результаты с нутрициологом. Консультация с нутрициологом поможет корректировать питание.",
    "Мало овощей в рационе?":"Это может способствовать развитию дисбиоза кишечника. Для диагностики рекомендуется провести анализы на микрофлору ЖКТ. Консультация с нутрициологом поможет вносить изменения в ваш рацион для поддержания баланса микробиома.",
    "Часто пьете жидкости сразу после еды?":"Это может негативно сказаться на пищеварении. Обсудите с гастроэнтерологом рекомендации по питанию. Консультация с нутрициологом поможет адаптировать привычки для оптимального здоровья ЖКТ.",
    "Часто выбираете сладкие продукты?":"Злоупотребление сладким может привести к инсулинорезистентности и дисбиозу. Рекомендуется сдача анализа на уровень глюкозы и инсулина в крови, и консультация с эндокринологом. Консультация с нутрициологом поможет сбалансировать питание для снижения этих рисков.",
    "Едите более 4 раз в день?":"Чрезмерное дробное питание может вызывать гормональные дисбалансы и нарушения углеводного обмена. Рекомендуется обсудить с эндокринологом и гастроэнтерологом подходящий для вас режим питания. Консультация с нутрициологом также поможет откорректировать питание для достижения оптимального здоровья."
}
questions_deficits = {
    "На ваших ногтях есть лунки?":"Возможно, присутствует риск гипоксии. Советую сдать кровь для проверки уровня гемоглобина, так как его понижение может быть одной из причин отсутствия лунок на ногтях.",
    "На ногтях - белые точки?":"Это может быть признаком дефицита цинка, минерала, отвечающего за правильное пищеварение, заживление ран и поддержку иммунитета. Цинк также участвует в регулировании гормональной активности. Рассмотрите возможность увеличения его потребления через пищу или добавки после консультации со специалистом.",
    "В уголках рта часто образуются трещины (“заеды”)?":"Это может указывать на дефицит витамина B2 и дисбиоз кишечника. Витамин B2 необходим для метаболизма, функционирования нервной системы и поддержания здоровья кожи и слизистых оболочек. Рекомендуется обсудить результаты со специалистом и рассмотреть корректировку диеты.",
    "Если “сыпятся” волосы?":"Обильное выпадение волос может свидетельствовать о проблемах с гормонами щитовидной железы или дефиците белка и цинка. Убедитесь, что ваше питание сбалансировано, и проконсультируйтесь со специалистом для детальной диагностики.",
    "Беспокоит кровоточивость десен?":"Это яркий признак дефицита витамина C, который важен для поддержания иммунной системы и улучшения абсорбции железа. Добавьте в рацион больше цитрусовых и других источников витамина C или обсудите со специалистом возможность приема добавок.",
    "У вас рано появилась седина?":"Это может быть связано с окислительным стрессом и дефицитом меди. Медь играет роль в формировании красных кровяных клеток и поддерживает здоровье нервной системы, костей и суставов. Рекомендуется пройти тестирование и, при необходимости, скорректировать рацион.",
    "Часто отмечаете у себя судороги, тики, мышечную слабость?":"Симптомы могут указывать на дефицит магния, который необходим для здоровья мышц, функционирования нервной системы и сердца. Рассмотрите увеличение потребления продуктов, богатых магнием, и обсудите симптомы с нутрициологом.",
    "Ваш язык напоминает географическую карту?":"Неоднородная поверхность языка может свидетельствовать о дефиците витаминов группы B, важных для метаболизма и функционирования нервной системы. Обсудите с нутрициологом возможность тестирования и введите в рацион больше источников этих витаминов.",
    "Часто и легко подхватываете простуды?":"Это может быть следствием сниженного иммунитета и дефицита нескольких витаминов. Важно поддерживать сбалансированную диету и, при необходимости, обсудить с нутрициологом прием добавок для укрепления иммунной системы.",
    "Вы значительно хуже видите в сумерках?":"Проблемы с видением в сумерках могут указывать на застой желчи и дефицит жирорастворимых витаминов, таких как A и E. Обсудите со специалистом правильные шаги для решения этих проблем.",
    "Ломкие, сухие, непослушные, секущиеся волосы и ломкие ногти?":"Это может говорить о дефиците белка и серы. Сера важна для образования белков и аминокислот и участвует в детоксикации. Обратите внимание на корректировку питания и, при необходимости, прием добавок.",
    "Постоянно испытываете слабость?":"Это может быть признаком анемии и нарушений работы щитовидной железы. Обсудите с нутрициологом тестирование уровня железа и гормонов щитовидной железы для постановки правильного диагноза.",
    "Испытываете сонливость в любое время суток?":"Сонливость может быть симптомом анемии или проблем с щитовидной железой и надпочечниками, а также указывать на дефициты. Проконсультируйтесь с нутрициологом для получения детального анализа и диагностики.",
    "Вы исключили из рациона животные продукты?":"Это может привести к дефициту половых гормонов, белка и витаминов, особенно B12 и D. Рассмотрите возможность введения растительных или дополнительных источников необходимых элементов. Обсудите с диетологом способы корректировки питания."
}
questions_thyroid = {
    "У вас наблюдается усталость и вялость, даже при достаточном отдыхе?":"Это может быть признаком гипотиреоза, когда щитовидная железа вырабатывает недостаточное количество гормонов. Это состояние может привести к снижению обмена веществ, что вызывает постоянную усталость. Рекомендуется сдать анализы на уровень ТТГ (тиреотропного гормона) и свободного Т4 (тироксина), а также проконсультироваться с эндокринологом для обсуждения возможного лечения, которое может включать в себя гормональную терапию.",
    "Замечаете ли частые изменения настроения или депрессию?":"Дисбаланс гормонов щитовидной железы может влиять на психическое состояние, вызывая депрессию или перепады настроения из-за изменения химии мозга. Актуально будет пройти анализы на уровень щитовидных гормонов, и, в зависимости от результатов, врач может назначить заместительную терапию или другие медицинские вмешательства. Поддержка психолога также может быть полезной.",
    "Вы потеряли или набрали вес без видимых причин?":"Необъяснимая потеря или набор веса могут быть связаны с гипертиреозом или гипотиреозом, соответственно. Эти состояния влияют на скорость метаболизма. Могут быть назначены тесты на ТТГ, Т3 и Т4, и, в зависимости от диагноза, может потребоваться коррекция диеты и режима физической активности, а также медикаментозное лечение.",
    "У вас сухая кожа и ломкие волосы?":"Недостаток гормонов щитовидной железы может привести к замедленному метаболизму, что, в свою очередь, вызывает сухость кожи и ломкость волос. Проверка уровня щитовидных гормонов в крови поможет подтвердить диагноз, и эндокринолог может порекомендовать увлажняющие средства и витамины (например, биотин и витамин Е), помимо основной терапии.",
    "Чувствуете ли вы холод даже в теплых условиях?":"Чувствительность к холоду может быть связана с гипотиреозом, так как сниженный уровень гормонов замедляет метаболизм, влияя на терморегуляцию. Анализ уровня тиреоидных гормонов поможет определить наличие проблемы и подобрать гормонозаместительную терапию.",
    "У вас есть проблемы с концентрацией внимания или памятью?":"Гормональный дисбаланс может влиять на когнитивные функции, снижая концентрацию и ухудшая память. Рекомендуется анализ на щитовидные гормоны и консультация с нутрициологом, который может порекомендовать когнитивные тренировки и коррекцию дефицита гормонов.",
    "Замечаете отечность лица или век по утрам?":"Отечность может быть признаком гипотиреоза из-за задержки жидкости в тканях. Проверка уровня ТТГ и Т4 поможет установить правильный диагноз, и лечение может включать в себя прием мочегонных препаратов или гормонозаместительной терапии.",
    "Страдаете от бессонницы или нарушенного сна?":"Избыток или недостаток гормонов может влиять на сон, вызывая либо бессонницу, либо чрезмерную сонливость. Исследование уровня гормонов щитовидной железы в сочетании с соблюдением режима сна и применением техник релаксации может помочь в решении проблемы.",
    "Есть ли у вас проблемы с пищеварением, такие как запор или диарея?":"Эти проблемы могут указывать на гипо- или гипертиреоз. Гипотиреоз склонен вызывать запоры, тогда как гипертиреоз может быть причиной ускоренного пищеварения и диареи. Анализы на ТТГ, Т4 и Т3 помогут уточнить диагноз и определить необходимое лечение, возможно, с применением пробиотиков и коррекции питания.",
    "Чувствуете ли вы, что у вас изменился голос или появились трудности с глотанием?":"Это может указывать на увеличение щитовидной железы или наличие узлов, влияющих на голосовые связки. Рекомендуется проведение УЗИ и консультация с эндокринологом, которые помогут установить причины и предложить методы вмешательства, которые могут варьироваться от наблюдения до хирургического вмешательства.",
    "Замечаете ли вы дрожь в руках или повышенное потоотделение?":"Эти симптомы могут быть связаны с гипертиреозом, так как гормоны в избытке возбуждают нервную систему. Необходимо сдать кровь на гормоны и обратиться к эндокринологу, который может назначить препараты для снижения активности щитовидной железы.",
    "У вас снизилось либидо?":"Гормональный дисбаланс, включая нарушения работы щитовидной железы, может влиять на половое влечение. Проверка уровня гормонов щитовидной железы и половых гормонов будет необходима для диагностики. Лечение может включать в себя гормонозаместительную терапию и консультации с сексологом или психологом.",
    "Появились ли у вас новые или увеличились ранее существующие узлы на шее?":"Это может указывать на изменения в щитовидной железе, такие как зоб или образование узлов. Рекомендуется консультация с эндокринологом и проведение УЗИ для оценки состояния щитовидной железы; возможно, потребуется провести биопсию для исключения злокачественных изменений и принять решение о дальнейшем лечении."
}
questions_insulin = {
    "Кожа на сгибах локтей и в промежностях имеет более темный оттенок?":"Это состояние известно как акантоз и является точным признаком нарушения углеводного обмена, такого как инсулинорезистентность и метаболический синдром. Рекомендуется консультация эндокринолога и сдача анализа на уровень инсулина и глюкозы в крови.",
    "У вас рано появились морщины, хотя вы всегда ухаживали за кожей?":"Это может указывать на процессы гликации в организме и дефицит коллагена. Гликация способствует старению кожи и может быть связана с нарушением обмена веществ. Сдача анализов на гликозилированный гемоглобин и консультация с нутрициологом помогут понять ситуацию.",
    "Диагностирован сахарный диабет II типа и есть лишний вес?":"Это прямое следствие нарушения углеводного обмена. Рекомендуется регулярный мониторинг уровня глюкозы в крови и поддержка специалиста по диетологии для оптимизации питания.",
    "Заметили за собой снижение когнитивных функций?":"Это может быть симптомом множества проблем, включая инсулинорезистентность, дисфункцию щитовидной железы и некоторых дефицитов. Рекомендуется анализ на гормоны щитовидной железы и инсулин, а также консультация с нутрициологом для выявления причин.",
    "Испытываете неудержимую тягу к сладкому?":"Это может быть свидетельством нарушенного углеводного обмена и сигналом о развитии инсулинорезистентности. Регулярное мониторирование уровня сахара в крови и консультация с эндокринологом помогут контролировать ситуацию.",
    "Чувствуете постоянную усталость и сонливость после еды?":"Это может быть связано с резкими колебаниями уровня глюкозы в крови, характерными для инсулинорезистентности. Рекомендуется сдать тест толерантности к глюкозе и обратиться за консультацией к эндокринологу.",
    "Наблюдается увеличение массе тела, несмотря на нормальный рацион?":"Набор веса без изменений в питании может указывать на инсулинорезистентность. Анализы на уровень инсулина, лептина и глюкозы помогут прояснить ситуацию.",
    "Шелушится и трескается кожа на руках и ногах?":"Это может быть связано с нарушениями метаболизма и инсулинорезистентностью. Рекомендуется анализ на уровень витаминов и минералов и консультация с дерматологом или эндокринологом.",
    "Сталкивались с частыми инфицирования кожи или грибковыми заболеваниями?":"Инфекционные заболевания могут свидетельствовать о повышенном уровне сахара в крови, что возможно при инсулинорезистентности. Анализ на гликемический профиль и консультация с дерматологом помогут с решением проблемы.",
    "У вас повышенное кровяное давление?":"Инсулинорезистентность может влиять на артериальное давление. Рекомендуется мониторинг уровня инсулина и сахара, и консультация с кардиологом.",
    "Заметили увеличение в объеме талии при неизменной массе тела?":"Увеличение объема талии может быть ранним признаком метаболического синдрома и инсулинорезистентности. Рекомендуется сдача анализов на липидный профиль и консультация с диетологом.",
    "Вы часто испытываете перепады настроения и раздражительность?":"Такие симптомы могут быть связаны с колебаниями уровня сахара в крови. Рекомендуется мониторинг уровня глюкозы и консультация с психологом или эндокринологом.",
    "Легко появляются синяки и долго заживают раны?":"Это может быть связано с нарушениями метаболизма, включая инсулинорезистентность. Рекомендуется сдача анализа на коагулограмму и консультация с нутрициологом для выявления причин."
}

def create_inline_keyboard(buttons, row_width=2):
    """
    Создаёт InlineKeyboardMarkup по списку вида [[text, callback_data], ...].
    """
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    btn_row = []
    for text, cb_data in buttons:
        btn = types.InlineKeyboardButton(text, callback_data=cb_data)
        btn_row.append(btn)
    markup.add(*btn_row)
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    """
    Приветственное сообщение: отправляем фото и кнопку «Начать диагностику».
    """
    chat_id = message.chat.id

    # 1) Создание инлайн-клавиатуры с кнопкой
    main_menu_buttons = [
        ('Начать диагностику➡️', 'diagnostics')
    ]
    markup = create_inline_keyboard(main_menu_buttons, row_width=1)

    # 2) Отправка фото с описанием и кнопкой
    bot.send_photo(
        chat_id,
        photo='AgACAgIAAxkBAAMLZ87Fb9t4GCZpmqcQ-9Th3dg8aj8AAlroMRsAAX54SvmtT9IvzW_wAQADAgADeQADNgQ',  # Замените на своё изображение или file_id
        caption=(
            f"Добро пожаловать, {message.from_user.first_name}!\n\n"
"""Я, Королёва Марина, дипломированный нутрициолог с пятилетним опытом! 🌟 
Моя миссия — помочь вам найти гармонию с вашим организмом и здоровьем, обучая понимать свои истинные потребности. 
Вместе мы составим индивидуальный план питания, который будет работать именно для вас. 🥗
С какими запросами я работаю?
- Дефициты витаминов и минералов
- Проблемы с желудочно-кишечным трактом
- Уровни холестерина
- Инсулинорезистентность
- Лишний вес
- Хроническую усталость
- Общий психоэмоциональный фон
Мой подход комплексный, что позволяет учитывать все аспекты здоровья и образа жизни для достижения устойчивых результатов.
Готовы начать свой путь к здоровью? Выберите тему диагностики и начнем трансформацию уже сегодня! 🚀"""
        ),
        reply_markup=markup
    )


def handle_service_support(chat_id):
    photo_url = 'AgACAgIAAxkBAAMYZ87sjY5ZG1ypyfG8WHV7oILQ93QAAlXpMRsAAX54StBxw8QjvwTgAQADAgADeQADNgQ'

    # Сокращенная подпись (не более 1024 символов)
    caption_text = """
Приглашаем на месячное сопровождение от дипломированного нутрициолога! 📅
- Индивидуальный анализ: обсудим ваши цели и здоровье.
- Разработка плана: личный план питания и образа жизни.
- Корректировка: регулярный мониторинг и корректировка рекомендаций.
- Еженедельная поддержка: консультации и мотивация.
- Обратная связь и рекомендации.\n
Начните свое трансформационное путешествие сегодня! 🌿
    """

    # Отправляем фото с укороченной подписью
    signup_button = create_inline_keyboard([
        ['Записаться', 'sign_up_service_support']
    ], row_width=1)

    bot.send_photo(
        chat_id=chat_id,
        photo=photo_url,
        caption=caption_text,
        reply_markup=signup_button
    )


def handle_service_group(chat_id):
    photo_url = 'AgACAgIAAxkBAAMZZ87srOkQT7RzpE9qBOEN0kqNeQQAAlbpMRsAAX54SlS60vQs86V_AQADAgADeQADNgQ'

    caption_text = """
Присоединяйтесь к групповому сопровождению "Шаги к здоровью"! 👥✨
- Индивидуальный и коллективный анализ.
- Персонализированная программа: план питания для улучшения здоровья.
- Групповые сессии и поддержка: делимся опытом и вдохновением.\n
Получите всестороннюю поддержку для долгосрочных изменений! 🌱🤝
    """

    signup_button = create_inline_keyboard([
        ['Записаться', 'sign_up_service_group']
    ], row_width=1)

    bot.send_photo(
        chat_id=chat_id,
        photo=photo_url,
        caption=caption_text,
        reply_markup=signup_button
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    chat_id = call.message.chat.id
    data = call.data

    if data == 'diagnostics':
        # Меню выбора тем диагностики
        topic_buttons = [
            ['ЖКТ 1️⃣', 'topic_1'],
            ['Дефициты 2️⃣', 'topic_2'],
            ['Щитовидка и гормоны 3️⃣', 'topic_3'],
            ['Инсулин 4️⃣', 'topic_4']
        ]
        markup = create_inline_keyboard(topic_buttons, row_width=2)
        bot.send_message(
            chat_id=chat_id,
            text="Выберите тему диагностики:",
            reply_markup=markup
        )

    elif data.startswith('topic_'):
        # Словарь «стартовых» видеозаметок (для демонстрации — одинаковые file_id)
        # Замените на свои реальные file_id, полученные от «video note»
        video_notes = {
            1: 'DQACAgIAAxkBAAMMZ87jzwV3IpQXKlHVvrNPFyLAVksAAtdhAAKnEkFKp3mmFZwDfG82BA',
            2: 'DQACAgIAAxkBAAMPZ87kYKlXTEmiSE7VW5ww0Tt18_AAAnpiAAKnEkFKZ8SKHdGMB3Y2BA',
            3: 'DQACAgIAAxkBAAMNZ87kAdUtiuyjO7w0nlUlQMEydaIAAu9hAAKnEkFKcSwlNDJygLc2BA',
            4: 'DQACAgIAAxkBAAMOZ87kLzozOrKA8PQyHQhGiu0tw2IAAitiAAKnEkFKh12R32bX6N42BA',
        }

        theme_id_str = data.split('_')[1]
        if not theme_id_str.isdigit():
            return
        theme_id = int(theme_id_str)

        # Получаем нужный file_id видеозаметки
        video_note_id = video_notes.get(theme_id)

        # Отправляем «стартовую» видеозаметку
        if video_note_id:
            bot.send_video_note(
                chat_id,
                video_note_id,
                duration=10,  # настройте по желанию
                length=240    # «диаметр» кружка
            )
        else:
            bot.send_message(chat_id, "Для этой темы пока нет начальной видеозаметки.")

        # Загружаем соответствующий словарь вопросов
        q_dict = get_question_dict(theme_id)
        questions_list = list(q_dict.items())

        if not questions_list:
            bot.send_message(chat_id, "Для выбранной темы пока нет вопросов.")
            return

        # Начинаем с первого вопроса (индекс 0)
        first_question = questions_list[0][0]
        buttons = [
            ['Да ✅', f'yes_{theme_id}_0'],
            ['Нет ❌', f'no_{theme_id}_0']
        ]
        bot.send_message(
            chat_id=chat_id,
            text=f"Первый вопрос:\n\n{first_question}",
            reply_markup=create_inline_keyboard(buttons, row_width=2)
        )

    elif data.startswith('yes_') or data.startswith('no_'):
        # Ответ "Да" или "Нет"
        answer_type, theme_str, index_str = data.split('_')
        theme_id = int(theme_str)
        q_index = int(index_str)

        q_dict = get_question_dict(theme_id)
        questions_list = list(q_dict.items())

        # Защита от выхода за границы списка
        if q_index >= len(questions_list):
            send_video_note_and_finish(chat_id, theme_id)
            return

        # Если «Да», показываем пояснение/ответ
        if answer_type == 'yes':
            question_text, answer_text = questions_list[q_index]
            bot.send_message(chat_id, f"Ответ по вопросу:\n\n{answer_text}")

        # Переходим к следующему вопросу
        next_q = q_index + 1
        if next_q < len(questions_list):
            # Есть ещё вопросы
            next_button = [
                ['Следующий вопрос ❓', f'next_{theme_id}_{next_q}']
            ]
            bot.send_message(
                chat_id=chat_id,
                text="Нажмите «Следующий вопрос», чтобы продолжить",
                reply_markup=create_inline_keyboard(next_button, row_width=1)
            )
        else:
            # Вопросы закончились — отправляем финальное видео и завершаем
            send_video_note_and_finish(chat_id, theme_id)

    elif data.startswith('next_'):
        # Переход к следующему вопросу
        _, theme_str, index_str = data.split('_')
        theme_id = int(theme_str)
        q_index = int(index_str)

        q_dict = get_question_dict(theme_id)
        questions_list = list(q_dict.items())

        if q_index >= len(questions_list):
            # Нет следующего вопроса
            send_video_note_and_finish(chat_id, theme_id)
            return

        next_question = questions_list[q_index][0]
        buttons = [
            ['Да ✅', f'yes_{theme_id}_{q_index}'],
            ['Нет ❌', f'no_{theme_id}_{q_index}']
        ]
        bot.send_message(
            chat_id=chat_id,
            text=f"Вопрос:\n\n{next_question}",
            reply_markup=create_inline_keyboard(buttons, row_width=2)
        )

    elif data == 'contact_me':
        # Кнопка «Связаться со мной» после завершения диагностики
        services_buttons = [
            ['Консультация 🤓', 'service_consultation'],
            ['Сопровождение 🔛', 'service_support'],
            ['Групповое сопровождение 👣', 'service_group']
        ]
        bot.send_message(
            chat_id=chat_id,
            text="Выберите интересующую вас услугу:",
            reply_markup=create_inline_keyboard(services_buttons, row_width=1)
        )

    elif data in ['service_consultation', 'service_support', 'service_group']:
        # При выборе услуги отправляем фотографию и кнопку «Записаться»
        if data == 'service_consultation':
            photo_url = 'AgACAgIAAxkBAAMUZ87nlq82VxS5tmVJWeFITrmFZPEAAr7rMRsUQSBKBDdSXLXlTtoBAAMCAAN5AAM2BA'
            caption_text = """
Приглашаю вас на консультацию у дипломированного нутрициолога! 🌿 Эта услуга предоставит вам персонализированный план питания, учитывающий ваши индивидуальные потребности и цели. 
На консультации вы получите:
- Анализ текущего состояния здоровья: Обсудим ваши привычки, самочувствие и лабораторные показатели.
- Индивидуальные рекомендации: Персонализированные советы по питанию и образу жизни, направленные на улучшение вашего здоровья и благополучия.
- План питания: Разработка сбалансированного рациона, включающего необходимые витамины и минералы.
- Поддержка и мотивация: Помощь в изменении пищевых привычек и настройка на позитивный результат.
    
Записавшись на консультацию, вы получите знания и инструменты для гармонизации своего организма и достижения лучших результатов в здоровье. Начните своё путешествие к благополучию уже сегодня! 🥗
            """
        elif data == 'service_support':
            handle_service_support(chat_id)
        else:  # 'service_group':
            handle_service_group(chat_id)
        signup_button = create_inline_keyboard([
            ['Записаться', f'sign_up_{data}']
        ], row_width=1)

        bot.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=caption_text,
            reply_markup=signup_button
        )

    elif data.startswith('sign_up_'):
        # Пользователь нажал «Записаться»
        service = data.split('_')[2]
        # Кнопка-ссылка на канал Telegram (замените на ваш канал)
        channel_link = "https://t.me/K_Marina_KMV"
        channel_button = types.InlineKeyboardMarkup()
        channel_button.add(types.InlineKeyboardButton("Перейти в наш канал", url=channel_link))

        bot.send_message(
            chat_id=chat_id,
            text=(f"Спасибо за выбор услуги: {service}.\n"
                  f"Нажмите кнопку ниже, чтобы перейти в наш Telegram-канал."),
            reply_markup=channel_button
        )
    elif data == 'view_reviews':
        handle_view_reviews(chat_id)

    else:
        pass

def handle_view_reviews(chat_id):
    photo_url = 'AgACAgIAAxkBAAMaZ89E_mHiEXQ_p49ty7E09N0swK4AApHrMRsAAX54Sl_ctTX-G_IcAQADAgADeQADNgQ'

    caption_text = "От довольных покупателей"

    markup = create_inline_keyboard([['Связаться со мной', 'contact_me']], row_width=2)

    bot.send_photo(
        chat_id=chat_id,
        photo=photo_url,
        caption=caption_text,
        reply_markup=markup
    )

def send_video_note_and_finish(chat_id, theme_id):
    """
    По завершении всех вопросов отправляем «финальную» видеозаметку для данной темы,
    затем сообщение с кнопками «Связаться со мной» и «Посмотреть отзывы».
    """
    # >>> ДОБАВЛЕНА «финальная» видеозаметка <<<
    final_video_notes = {
        1: 'DQACAgIAAxkBAAMTZ87l3J8YLSDx8e0aVU2lZk_QAncAAl9qAAKA3EhKl1NgcyLuyGQ2BA',
        2: 'DQACAgIAAxkBAAMQZ87laPJ9OIRPokqNiXn_Eng12doAApFiAAKnEkFKSJbgOgE7syQ2BA',
        3: 'DQACAgIAAxkBAAMSZ87lwJqmRYvxPFWE7GtVD41AVLoAAtVdAAIdwkFKI_yW5EHSwuw2BA',
        4: 'DQACAgIAAxkBAAMRZ87llIhN0iaVmLGkSc1zS1GwAWsAAo1cAAIdwkFKkk4w0yRjTPs2BA',
    }
    final_note_id = final_video_notes.get(theme_id, None)
    if final_note_id:
        bot.send_video_note(chat_id, final_note_id, duration=10, length=240)
    else:
        bot.send_message(chat_id, "Для этой темы пока нет финальной видеозаметки.")

    # После отправки финального видео — кнопка «Связаться со мной» и «Посмотреть отзывы»
    finish_buttons = [
        ['Связаться со мной', 'contact_me'],
        ['Посмотреть отзывы', 'view_reviews']
    ]
    bot.send_message(
        chat_id=chat_id,
        text="Диагностика по данной теме завершена!\n"
             "Если хотите задать вопросы или узнать об услугах, нажмите «Связаться со мной».\n"
             "Для просмотра отзывов нажмите «Посмотреть отзывы»👇👇👇",
        reply_markup=create_inline_keyboard(finish_buttons, row_width=1)
    )




def get_question_dict(theme_id):
    """ Возвращает словарь вопросов по выбранной теме. """
    if theme_id == 1:
        return questions_gastro
    elif theme_id == 2:
        return questions_deficits
    elif theme_id == 3:
        return questions_thyroid
    elif theme_id == 4:
        return questions_insulin
    return {}

# Запуск «вечного» цикла опроса Telegram
bot.infinity_polling()
