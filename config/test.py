
levels = {
    0: 'Outside',
    12: 'Junior-Intern',
    18: 'Junior',
    24: 'Pre-Middle',
    27: 'Middle',
    32: 'Pre-Senior',
    36: 'Senior',
    41: 'Lead',
}

level_f = {
    0: 'Outside',
    60: 'Junior-Intern',
    90: 'Junior',
    121: 'Pre-Middle',
    135: 'Middle',
    162: 'Pre-Senior',
    180: 'Senior',
}

level_text = {
    "Outside": "Outside: Не обладает необходимыми для Junior-intern навыками, не имеющий достаточно опыта работы с программными средствами (0-59 поинтов)",
    "Junior-Intern" : "Junior-intern: Специалист с начальными техническими навыками, способный выполнять задачи проекта/команды только под контролем наставника (60-89 поинтов)",
    "Junior": "Junior: Специалист с формирующимися навыками ответственности, требует привлечения наставника при необходимости (90-120 поинтов)", 
    "Pre-Middle": "Pre-Middle: Специалист с приемлемым уровнем самостоятельности, при котором формируются навыки ответственности и эффективности (121-134 поинтов)", 
    "Middle": "Middle: Специалист, с хорошо развитыми техническими навыками, тактическим мышлением, планированием и контролем поставленных задач. Полностью самостоятельный, достигает результата за счет личной эффективности (135-161 поинтов)", 
    "Pre-Senior" : "Pre-Senior: Специалист выступает техническим консультантом команды, мыслит и принимает стратегические решения на уровне проекта / отдела (162-179 поинтов)", 
    "Senior": "Senior: Специалист является техническим лидером команды с глубокими знаниями, опытом и экспертизой. Решает задачи на уровне проекта / отдела (180-200 поинтов)", 
    "Lead" : "Lead: Специалист является компетентным лидером команды, обеспечивает условия реализации стратегии компании. Основная функция - организация работы команды и контроль выполнения задач (180-200 поинтов)"
}

question_level = {
    'Не понимаю': 0,
    'Не знаю': 0,
    "Не владею": 0,
    "Знаю только": 1,
    "Знаю теорию": 2,
    "Испытываю сложности": 2,
    "Использую на": 3,
    "Владею и": 3,
    "Владею в": 4,
}

kcal = [
    [
        1.0,
        1.0,
        0.5,
        1.0,
        0.8,
        0.8,
        0.8,
        0.8,
        1.0,
        1.0,
    ],
    [
        0.5,
        0.8,
        0.8,
        1.0,
        1.0,
        1.0,
        0.8,
        0.8,
        1.0,
        1.0,
    ],
    [
        1.0,
        0.8,
        0.8,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        0.5,
        1.0,
    ],
    [

        0.8,
        0.8,
        0.8,
        1.0,
        0.8,
        0.2,
        0.8,
        0.8,
        0.8,
        0.8,
    ],
    [
        1.0,
        1.0,
        0.8,
        0.5,
        0.8,
        0.8,
        1.0,
        0.5,
        0.5,
        0.5,
    ]
]
    
