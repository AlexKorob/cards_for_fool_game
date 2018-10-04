#python 3.7.0
# в колоде 54 карты
import random

def create_pack_cards():
    colors = ['Пика', 'Черва', 'Бубна', 'Креста']
    # создаем список карт без мастей - 13 карт
    cards_not_color = [str(i) for i in range(2, 11)] + ['Валет', 'Дама', 'Король', 'Туз']
    cards = []

    # дублируем каждую карту на 4 и добавляем к карте масть, также кладем карту в список "cards"
    for i in range(13):
        for color in colors:
            cards.append(cards_not_color[i] + ' "' + color +'"')
        
    # определяем козырную карту
    trump_card = cards[random.randint(0, 51)]
    cards.extend(['Black Joker', 'Red Joker'])

    # применяем метод для рандомной сортировки списка с картами
    random.shuffle(cards)

    # кладем козырную карту вниз колоды в нашем случае низ колоды это начало массива
    cards.remove(trump_card)
    cards.insert(0, trump_card)

    return cards, trump_card

def distribution_cards(N):
    players = []

    # каждому игроку раздаем по шесть карт, создаем одномерный массив для каждого игрока
    # состоящий из шести карт после чего добавляем массив с картами в основной массив - players
    for i in range(N):
        player = []
        for j in range(6):
            # при добавлении карты игроку, карта из колоды извлекается
            player.append(cards.pop())
        players.append(player)
        
    return players

def max_score(force):
    score = []
    
    # в цикле проходимся по всем игрокам и затем во вложенном цикле по картам каждого игрока,
    # суммируем карты каждого игрока и добавляем результат в список score
    for hand in force:
        summ = 0
        for card in hand:
            summ += card
        score.append(summ)
        
    strong_hand = max(score)
    
    # возвращаем карты лучшего игрока
    return players[score.index(strong_hand)]
    
    
def view():
    print('Козырь - ', trump_card)
    print()
    
    for num, hand in enumerate(players):
        print('Игрок №'+str(num+1) + ':  ', end='')
        for card in hand:
            if card == hand[-1]:
                print(card)
                continue
            print(card + ',  ', end='')
    print()
    print('Лучшие карты у игрока под номером: '+ str(players.index(strong_hand) + 1))
    print(*strong_hand, sep=', ')
    
    
    
def force_cards(hands, trump_card):

    force_top_cards = {'Валет': 11, 'Дама': 12, 'Король': 13, 'Туз': 14, 'Joker': 15}
    # Определяем масть козырной карты
    trump_color = trump_card.split(' ')[1][1:-1]
    force = []

    # В цилке перебираем всех игроков с картами
    for hand in hands:
        force_one_hand = []

        # Перебираем все карты в руке игрока
        for card in hand:
            # определяем масть одной карты
            card_color = card.split(' ')[1][1:-1]

            # если карта выше 10, тоесть для её обозначения используется слово:
            if not card.split(' ')[0].isdigit():
                if card.split(' ')[1] == 'Joker':
                    if (trump_color == 'Пика' or trump_color == 'Креста') and card == 'Black Joker':
                        force_one_hand.append(force_top_cards.get('Joker') + 13)
                    elif (trump_color == 'Черва' or trump_color == 'Бубна') and card == 'Red Joker':
                        force_one_hand.append(force_top_cards.get('Joker') + 13)
                    else:
                        force_one_hand.append(force_top_cards.get('Joker'))
                    continue

                if trump_color == card_color:
                    # по названию карты достаем из словаря числовое значение соотвествующее силе карты
                    # прибавляем к этому значению число 13 поскольку
                    # Число 13 выбранно из-за того что сила карты - некозырного туза равна 14,
                    # что бы козырная карта двойка была сильнее некозырного туза её значение должно быть 15
                    # козырная тройка должна быть равна 16 и т.д.
                    force_card = force_top_cards.get(card.split(' ')[0]) + 13
                    force_one_hand.append(force_card)
                    continue
                
                force_card = force_top_cards.get(card.split(' ')[0])
                force_one_hand.append(force_card)
            # если значение карты равно или меньше 10:
            else:
                if trump_color == card_color:
                    force_one_hand.append(int(card.split(' ')[0]) + 13)
                else:
                    force_one_hand.append(int(card.split(' ')[0])) 
        force.append(force_one_hand)
        
    return force

cards, trump_card = create_pack_cards()     # создаем колоду, определяем козырную карту

N = input('Введите число игроков: ')  

while not N.isdigit():
    print('Введите числовое значение!')
    N = input('Введите число игроков: ')
    
players = distribution_cards(int(N))         # раздаем карты всем игрокам

force = force_cards(players, trump_card)    # определяем значимость карт в руке каждого игрока

strong_hand = max_score(force)      # определяем игрока с лучшими картами

view()          # вывести необходимую информацию в консоль
