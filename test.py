#ВАЖНО
#Для работы программы необходим Python 3.
#На вход программа получает hash
#Далее идет выбор режима атаки(bruteforce/dictionary)
#Задаются критерии для атаки
#Производится атака
#В случае успеха программа выводит прообраз
#
#Кузнецов Максим Дмитриевич ККСО-01-16


''' импорт нужных библиотек (для взятя хешей,работы со временем,работы со словарем)'''
import hashlib, sys, time, random
from itertools import product
    
''' функция, которая выбирает нужный алгоритм '''
def get_alg( type ):
    def alg( string ):
        h = type()
        h.update(string.encode('utf-8'))
        return h.hexdigest()
    return alg

'''список алгоритмов(выбирается алгоритм из библиотеки hashlib и размер хеша)'''

dict = { 32  : get_alg( hashlib.md5 ),
         40  : get_alg( hashlib.sha1 ),
         56  : get_alg( hashlib.sha224 ),
         64  : get_alg( hashlib.sha256 ),
         96  : get_alg( hashlib.sha384 ),
         128 : get_alg( hashlib.sha512 ) }


''' класс main '''
class Control( object ):
    ''' настройки по умолчанию '''
    def __init__( self ):
        self.decrypt_method = None
        self.decrypted_hash = None
        self.user_file = None
    
    ''' main '''
    def main( self ):
        self.user_hash = self.get_hash() #вызываем метод get_hash(в нем хеш подается в программу) и помещаем полученный(введенный) хеш в переменную user_hash
        
        while self.decrypted_hash == None: #пока не найдено совпадение
            self.attack_mode = self.get_attack_mode()# вызываем метод attack_mode(для выбора режима атаки)
            
            if self.attack_mode == 'd':#если режим атаки  = 'd'(dictionary attack)
                self.wordlist = self.gen_wordlist() # вызываем метод gen_wordlist(для генерации словаря)
                self.decrypted_hash = self.dictionary_attack()#вызываем метод dictionary_attack,реализующий атаку по словарю
            elif self.attack_mode == 'b':#если режим атаки  = 'b'(bruteforce attack)
                self.decrypted_hash = self.bruteforce_arrack()#вызываем методa bruteforce_arrack, реализующий брутфорс атаку
            elif self.attack_mode == 'h':
                self.decrypted_hash = self.happyBirthdayParadox_attack()
            if self.decrypted_hash != None: # Если удалось провести атаку(успешно)
                self.elapsed = (time.time() - self.start) # высчитываем время, за которое атака была проведена
                print('Атака на хеш была произведена за '+str(self.elapsed)+' секунд. Правильное слово: '+self.decrypted_hash)# выводим его на экран и правильное слово
                sys.exit()#завершаем программу
            else:#если не удалось провести атаку
                self.retry('Атаку не удалось произвести')#вызываем метод retry (для повторной попытки)

    '''метод считывания хеша(с помощью этого метода,фактически, программа определяет с помощью какой функции хеширования было произведено хеширование'''
    def get_hash(self):
        while True:
            hash_input = input('Введите хеш: ')#считывается строка(хеш) с клавиатуры
            if hash_input.isalnum(): #Проверка на то,что во входной строке есть И цифры И буквы
                length = len(hash_input)#Длина строки(хеша)
                if dict.get( length, None ):#если такая длина есть в списке алгоритмов
                    self.hashtype = dict[length]#выбираем алгоритм с данной длиной хеша
                    return hash_input

                else:#если такой длины нет, то хеш введен неверно
                    self.retry('Неверный хеш')
            
            else:# если в последовательности только цифры или только буквы,то хеш введен неверно
                self.retry('Неверный хеш')
    
    '''метод генерации списка слов(для dictionary attack)'''
    def gen_wordlist(self):
        while self.user_file == None:
            self.filename = input('Введите имя файла со словарем: ')#вводим имя файла со словарем(или путь,если проиграмма и файл находятся в разных каталогах)
            #exeption на существование файла 
            try:
                self.user_file = open(self.filename, 'r', encoding='utf-8')
            except FileNotFoundError:
                self.retry('файл не найден '+self.filename)
        
        #считываение с файла и формирование списка
        words = self.user_file.read()
        self.user_file.close()
        return words.split()
         
    '''метод выбора режима атаки'''
    def get_attack_mode(self):
        while True:
            attack_mode = input("Введите 'b' для брутфорс атаки, 'd' для атаки по словарю, 'h' для атаки парадокса дней рождения: ")
            if attack_mode.lower() == 'b':
                return attack_mode
            elif attack_mode.lower() == 'd':
                return attack_mode
            elif attack_mode.lower() == 'h':
               return attack_mode
            else:
                self.retry('неверно введен режим атаки')
            
    '''метод,который реализует атаку по словарю'''
    def dictionary_attack(self):
        # Проходим по каждому слову в словаре и высчитываем его хеш,затем сравниваем с поданным на вход начением.
        self.start = time.time()#засекаем время начала
        print('Производится атака \n\n\n')
        for word in self.wordlist:
            test = self.hashtype(word)
            if test == self.user_hash:
                return word
                
    '''метод,который реализует брутфорс атаку'''
    def bruteforce_arrack(self):
        # Слова генерируются из входной последовательности в зависимости от минимальной и максимальной длины с помощью метода 
        # itertools.product() перебирает всевозможные комбинации входных символов,в зависимости от необходимой длины
        charset = input('Введите необходимый набор символов: ')
        minlen = int(input('Введите минимальную длину '))
        maxlen = int(input('Введите макисмальную длину '))
        
        print('Производится атака \n\n\n')
        self.start = time.time()#засекаем время начала
        for i in range(minlen, maxlen+1):#выбираем длину слова,начинаем в 1
            for p in product(charset, repeat=i):#в зависимости от длины и входной последовательности,формируем слова,далее аналогично атаке по словарю
                word = ''.join(p)
                if self.hashtype(word) == self.user_hash:
                    return word

    def happyBirthdayParadox_attack(self):
        dict = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        minlen = int(input('Введите минимальную длину '))
        maxlen = int(input('Введите макисмальную длину '))
        print('Производится атака \n\n\n')
        self.start = time.time()#засекаем время начала
        for i in range (pow(2,len(self.user_hash) - 1)):
            word = ''
            for j in range (random.randint(minlen, maxlen)):
                word += random.choice( dict )
            if(self.hashtype(word) == self.user_hash):
                break;
        return word

    
    '''Метод повторного действия(если что то пошло не так)'''            
    def retry(self, failure_type):
        # используется для неверного хеша, неправильного пути/типа словаря,если введен неправильный ответ на выбор атаки
        # выводится строчка,которая передана в этот метод и предложение попробовать снова или завершить программу
        print(failure_type+'. Повторить? (y/n)')
        while True:
            choice = input()
            if choice.lower() == 'y':
                return
            elif choice.lower() == 'n':

                sys.exit()
            else:
                print('Введен неверный ответ')

                    
                    
if __name__ == "__main__":
    run_it = Control()
    run_it.main()

