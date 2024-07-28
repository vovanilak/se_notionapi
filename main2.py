
from answer import *
def main():
    want = int(input('Куда добавить карточку?\n0 - Pro LIGA IT\n1 - AC/SE штатных сотрудников\n>>> '))
    number = int(input('Какой номер строки?\n>>> '))
    row = Row()
    person = Person(row)
    test = Test(row)
    imgs = Image(test)
    prop = get_prop(test)
    page = Page(test)
    post = Post(prop, page)

    if want:
        person = Anketa(url=Anketa.URL_STAFF,
                        row=number,
                        json_file='data/new_version2.json',
                        start_result_column=11)
        k = person.post_staff()
        print(k)
        
    else:
        person = Anketa(url=Anketa.URL_LIGA,
                        row=number,
                        json_file='data/new_version2.json',
                        start_result_column=13)
        res = person.post_liga()
        print(*res, sep='\n\n')