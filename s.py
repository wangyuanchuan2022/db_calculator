import json
import re


class User:
    def __init__(self):
        self.move_seq = []
        self.move_type = None
        self.basic_r_text2num = {
            '大臂': 0,
            '攒': 1,
            '方盾': 2,
            '圆盾': 3,
            '小闪': 4,
            '超闪': 5
        }
        self.basic_a_text2num = {
            '刀': 0,
            'ber': 1,
            '拳': 2,
            '踢': 3,
        }
        self.attack2shield = {
            "闪击": '闪电盾',
            '雷击': '雷电盾',
            '元素打击': '元素盾',
            '超级雷击': '超级雷电盾',
        }
        self.curse = {'寒冰剑': '方盾', '金釜刀': '攒', '猿斧斩': '大臂', '贯石斧': '方盾'}
        with open('./data.json', encoding='utf-8') as f:
            self.attack_text2num = json.load(f)
        with open('./defense.json', encoding='utf-8') as f:
            self.attack_defense = json.load(f)
        with open('./attack.json', encoding='utf-8') as f:
            self.attack2num = json.load(f)
        with open('./shield.json', encoding='utf-8') as f:
            self.shield_text2num = json.load(f)
        with open('./shield_num.json', encoding='utf-8') as f:
            self.shield2num = json.load(f)
        self.generator_num = {
            '小型': [2, 1],  # cost generate num
            '中型': [3, 2],
            '大型': [5, 3]
        }
        self.basic_resource = [0 for i in self.basic_r_text2num]
        self.generator_list = []
        self.shield_list = []
        self.shield_num_list = []
        self.special_attack = {
            "资源加倍": "6踢合一",
            "气吞山河": "6拳合一",
            "六脉神剑": "6刀合一",
            "如来神ber": "6ber合一"
        }
        self.heyi_list = []

    def restart(self):
        self.move_seq = []
        self.generator_list = []
        self.shield_num_list = []
        self.shield_list = []
        self.move_type = None
        self.basic_resource = [0 for i in self.basic_r_text2num]

    def calculate_shield_layer(self, shield_list):
        res = 0
        for shield in shield_list:
            res += self.shield2num[shield]
        return res

    def complete_shield_index(self, shield_name):
        res = []
        for i in range(len(self.shield_list)):
            if self.shield_list[i] == shield_name and self.shield_num_list[i] == self.shield2num[shield_name]:
                res.append(i)
        return res

    def generator_move(self):
        _len = len(self.generator_list)
        for i in range(_len):
            generator = self.generator_list[i]
            res = re.match(r'(大|中|小)型([\u4e00-\u9fa5]{2,}?)生产器(的(大|中|小)型生产器){0,}$', generator).groups()
            if res:
                _resource = res[1]
                if '的' in generator:
                    seq = generator.split('的')
                    generator = generator[:-len(seq[-1]) - 1]
                    for j in range(self.generator_num[seq[-1][:2]][1]):
                        self.generator_list.append(generator)
                else:
                    for basic in self.basic_r_text2num.keys():
                        if basic == _resource:
                            self.basic_resource[self.basic_r_text2num[basic]] += self.generator_num[generator[:2]][1]
                            break
                    for basic in self.attack_text2num.keys():
                        if basic == _resource:
                            for j in range(len(self.attack_text2num[basic])):
                                self.basic_resource[j] += (self.attack_text2num[basic][j] *
                                                           self.generator_num[generator[:2]][1])
                            break

    def hecheng_dun(self):
        return_string = ''

        dun_list = self.complete_shield_index('元素盾')
        for i in range(int(len(dun_list) / 2)):
            self.shield_list.pop(dun_list[i] - 2 * i)
            self.shield_list.pop(dun_list[i + 1] - 2 * i - 1)
            self.shield_num_list.pop(dun_list[i] - 2 * i)
            self.shield_num_list.pop(dun_list[i + 1] - 2 * i - 1)
            self.shield_list.append('雷电盾')
            self.shield_num_list.append(self.shield2num['雷电盾'])
            return_string += '两个元素盾合一个雷电盾\n'

        dun_list = self.complete_shield_index('闪电盾')
        for i in range(int(len(dun_list) / 2)):
            self.shield_list.pop(dun_list[i] - 2 * i)
            self.shield_list.pop(dun_list[i + 1] - 2 * i - 1)
            self.shield_num_list.pop(dun_list[i] - 2 * i)
            self.shield_num_list.pop(dun_list[i + 1] - 2 * i - 1)
            self.shield_list.append('雷电盾')
            self.shield_num_list.append(self.shield2num['雷电盾'])
            return_string += '两个闪电盾合一个雷电盾\n'

        dun_list = self.complete_shield_index('雷电盾')
        for i in range(int(len(dun_list) / 2)):
            self.shield_list.pop(dun_list[i] - 2 * i)
            self.shield_list.pop(dun_list[i + 1] - 2 * i - 1)
            self.shield_num_list.pop(dun_list[i] - 2 * i)
            self.shield_num_list.pop(dun_list[i + 1] - 2 * i - 1)
            self.shield_list.append('超级雷电盾')
            self.shield_num_list.append(self.shield2num['超级雷电盾'])
            return_string += '两个雷电盾合一个超级雷电盾\n'

        return return_string

    def move_calculation(self, move, cost=True, is_try=False):
        if move.startswith('丢下个'):
            _move = move[3:]
            if (self.move_seq[-2] == _move and self.move_seq[-3] == _move) or \
                    (self.move_seq[-2] == _move and self.move_seq[-1] == _move):
                if not is_try:
                    self.move_calculation(_move, cost=False)
                else:
                    self.move_calculation(_move, is_try=True)
            else:
                raise Exception('自暴自弃')
        elif move in self.basic_r_text2num.keys():
            if not is_try:
                self.basic_resource[self.basic_r_text2num[move]] += 1

        elif move in self.curse.keys() or move == '雷劈剑':
            if not is_try:
                self.move_type = '攻击'

        elif move in self.attack_text2num.keys():
            if not is_try:
                self.move_type = '攻击'
            if cost:
                for i in range(len(self.attack_text2num[move])):
                    if self.basic_resource[i] < self.attack_text2num[move][i]:
                        raise Exception('自暴自弃')
                    if not is_try:
                        self.basic_resource[i] -= self.attack_text2num[move][i]
        elif move in self.special_attack.values():
            if self.move_type == '回合无敌':
                raise Exception('自暴自弃')
            if not is_try:
                self.move_type = '回合无敌'
            if cost:
                if self.basic_resource[self.basic_a_text2num[move[1:-2]]] < 6:
                    raise Exception('自暴自弃')
                if not is_try:
                    self.basic_resource[self.basic_a_text2num[move[1:-2]]] -= 6
            if not is_try:
                self.heyi_list.append(move)
        elif move == '资源加倍':
            if cost:
                if self.heyi_list.count('6踢合一') < 1:
                    if self.basic_resource[self.basic_a_text2num['踢']] < 6:
                        raise Exception('自暴自弃')
                    else:
                        if not is_try:
                            self.basic_resource[self.basic_a_text2num['踢']] -= 6
                else:
                    if not is_try:
                        self.heyi_list.remove('6踢合一')
            if not is_try:
                self.generator_list += self.generator_list
                self.shield_list += self.shield_list
                self.shield_num_list += self.shield_num_list
                for i in range(5):
                    self.basic_resource[i] *= 2
        elif move.startswith('气吞山河'):
            if cost:
                if self.heyi_list.count('6拳合一') < 1:
                    raise Exception('自暴自弃')
                else:
                    if not is_try:
                        self.heyi_list.remove('6拳合一')
            if not is_try:
                tun_list = move.split(' ')[1:]
                for t in tun_list:
                    if '个' in t:
                        _move = t.split('个')
                        try:
                            num = int(_move[0])
                        except ValueError:
                            num = 2
                        for i in range(num):
                            self.move_calculation(_move[1], cost=False, is_try=is_try)
                    else:
                        self.move_calculation(t, cost=False, is_try=is_try)
        elif move.startswith('吞'):
            if cost:
                if self.basic_resource[self.basic_r_text2num['攒']] < 1 or \
                        self.basic_resource[self.basic_r_text2num['方盾']] < 1:
                    raise Exception('自暴自弃')
                else:
                    if not is_try:
                        self.basic_resource[self.basic_r_text2num['攒']] -= 1
                        self.basic_resource[self.basic_r_text2num['方盾']] -= 1
                _move = move.split(' ')
                try:
                    self.move_calculation(_move[1], cost=False, is_try=is_try)
                except IndexError:
                    pass

        elif re.match(r'([1-9])/([1-9])([\u4e00-\u9fa5]{1,8})', move):
            res = re.match(r'([1-9])/([1-9])([\u4e00-\u9fa5]{1,8})', move).groups()
            true_shield_num = res[0]
            shield_num = res[1]
            shield = self.attack2shield[res[2]]
            is_ok = False
            for i in range(len(self.shield_list)):
                if self.shield_num_list[i] == true_shield_num and self.shield2num[shield] == shield_num:
                    if not is_try:
                        self.shield_list.pop(i)
                        self.shield_num_list.pop(i)
                    is_ok = True
            if not is_ok:
                raise Exception('自暴自弃')

        elif '连' in move:
            if cost:
                _attack = move.split('连')
                try:
                    num = int(_attack[0])
                except ValueError:
                    num = 2
                if _attack[1] in self.attack_text2num.keys():
                    for i in range(len(self.attack_text2num[_attack[1]])):
                        if self.basic_resource[i] < self.attack_text2num[_attack[1]][i] * num:
                            raise Exception('自暴自弃')
                        if not is_try:
                            self.basic_resource[i] -= self.attack_text2num[_attack[1]][i] * num
                else:
                    raise Exception('输入错误！')

        elif move.endswith('生产器'):
            if not is_try:
                self.move_type = '生产器'
            generator = move
            res = re.match(r'(大|中|小)型([\u4e00-\u9fa5]{2,}?)生产器(的(大|中|小)型生产器){0,}$', generator).groups()
            if res:
                _resource = res[1]
                if (_resource not in self.basic_r_text2num.keys()) and (_resource not in self.attack_text2num.keys()):
                    raise Exception('非法输入')
                elif _resource == '打断' or _resource == '超级打断':
                    raise Exception('非法输入')
            else:
                raise Exception('非法输入')
            if '的' in generator:
                if cost:
                    seq = generator.split('的')
                    _generator = generator[:-len(seq[-1]) - 1]
                    num = self.generator_list.count(_generator)
                    if num < self.generator_num[seq[-1][:2]][0]:
                        raise Exception('自暴自弃！')
                    if not is_try:
                        for j in range(self.generator_num[seq[-1][:2]][0]):
                            self.generator_list.remove(_generator)
                if not is_try:
                    self.generator_list.append(generator)
            else:
                for basic in self.basic_r_text2num.keys():
                    if basic == _resource:
                        if cost:
                            if self.basic_resource[self.basic_r_text2num[basic]] < self.generator_num[generator[:2]][0]:
                                raise Exception('自暴自弃')
                            if not is_try:
                                self.basic_resource[self.basic_r_text2num[basic]] -= self.generator_num[generator[:2]][
                                    0]
                        if not is_try:
                            self.generator_list.append(generator)
                for basic in self.attack_text2num.keys():
                    if basic == _resource:
                        if cost:
                            is_over = False
                            for i in range(len(self.attack_text2num[basic])):
                                if (self.basic_resource[i] < self.attack_text2num[basic][i]
                                        * self.generator_num[generator[:2]][0]):
                                    is_over = True
                                    break
                            if is_over:
                                raise Exception('自暴自弃！')
                            if not is_try:
                                for i in range(len(self.attack_text2num[basic])):
                                    self.basic_resource[i] -= (self.attack_text2num[basic][i]
                                                               * self.generator_num[generator[:2]][0])
                        if not is_try:
                            self.generator_list.append(generator)
                        break

        elif move in self.shield_text2num.keys():
            if not is_try:
                self.move_type = '盾'
            if cost:
                for i in range(len(self.shield_text2num[move])):
                    if self.basic_resource[i] < self.shield_text2num[move][i]:
                        raise Exception('自暴自弃！')
                    else:
                        if not is_try:
                            self.basic_resource[i] -= self.shield_text2num[move][i]
            if not is_try:
                self.shield_list.append(move)
                self.shield_num_list.append(self.shield2num[move])
        else:
            if is_try:
                raise Exception('无效')

    def show_shield(self):
        return_string = ''
        for i in range(len(self.shield_list)):
            if self.shield_num_list[i] == self.shield2num[self.shield_list[i]]:
                return_string += self.shield_list[i] + '\n'
            else:
                return_string += (f'{self.shield_num_list[i]}/{self.shield2num[self.shield_list[i]]}'
                                  f'个{self.shield_list[i]}\n')
        return return_string

    def step(self, move, attack):
        self.move_seq.append(move)
        return_string = ''
        self.move_type = None

        # self.generator_move()

        return_string += self.hecheng_dun()

        self.move_calculation(move)

        for att in attack.split(' '):
            return_string += self.attack_calculation(move, att)
        # print(self.generator_list)
        return return_string

    def attack_calculation(self, move, attack):
        return_string = ''
        attack_num_list = [0, 0, 0]
        if self.move_type == '回合无敌':
            return return_string

        if move in self.attack_defense.keys():
            if attack in self.attack_defense[move]:
                return ''
        if attack in self.attack2num.keys():
            attack_num_list = self.attack2num[attack].copy()
            attack_num_list.append(1)
            # print(attack_num_list)

        elif move in self.curse.keys() and attack == '雷劈剑':
            raise Exception('你租了')

        elif attack in self.curse.keys():
            if move == self.curse[attack]:
                raise Exception('你租了')
            else:
                return return_string

        elif '连' in attack:
            _attack = attack.split('连')
            try:
                num = int(_attack[0])
            except ValueError:
                num = 2
            if _attack[1] in self.attack2num.keys():
                attack_num_list = self.attack2num[_attack[1]].copy()
                attack_num_list.append(num)
            else:
                raise Exception('输入错误！')
        elif attack == '打断' and self.move_type != '攻击':
            if self.move_type == '盾':
                return_string += f'{self.shield_list.pop(-1)}掉了\n'
                self.shield_num_list.pop(-1)
            elif self.move_type == '生产器':
                return_string += f'{self.generator_list.pop(-1)}掉了\n'
            return return_string

        elif attack == '超级打断' and self.move_type != '攻击':
            _move = self.move_seq[-2]
            try:
                if _move.endswith('盾'):
                    if self.shield_list[-1] == _move and not self.move_seq[-1].endswith('盾'):
                        return_string += f'{self.shield_list.pop(-1)}掉了\n'
                        self.shield_num_list.pop(-1)
                    elif self.shield_list[-2] == _move and self.move_seq[-1].endswith('盾'):
                        return_string += f'{self.shield_list.pop(-2)}掉了\n'
                        self.shield_num_list.pop(-2)
                elif _move.endswith('生产器'):
                    if self.generator_list[-1] == _move and not self.move_seq[-1].endswith('生产器'):
                        return_string += f'{self.generator_list.pop(-1)}掉了\n'
                    elif self.generator_list[-2] == _move and self.move_seq[-1].endswith('生产器'):
                        return_string += f'{self.generator_list.pop(-2)}掉了\n'
            except IndexError:
                return return_string
            return return_string
        else:
            return ''
        # print(attack_num_list)

        if move == '小闪':
            rest_layers = self.shan_calculate(attack_num_list, 4)
        elif move == '超闪':
            rest_layers = self.shan_calculate(attack_num_list, 14)
        elif move == 'piapia打脸':
            if self.basic_resource[self.basic_r_text2num['小闪']] < 1 or \
                    self.basic_r_text2num[self.basic_r_text2num['超闪']] < 1:
                raise Exception("自暴自弃")
            self.basic_resource[self.basic_r_text2num['小闪']] -= 1
            self.basic_resource[self.basic_r_text2num['超闪']] -= 1
            rest_layers = self.shan_calculate(attack_num_list, 2)
        elif move == '反弹盾':
            if self.basic_resource[self.basic_r_text2num['大臂']] < 1 or \
                    self.basic_resource[self.basic_r_text2num['超闪']] < 1:
                raise Exception("自暴自弃")
            self.basic_resource[self.basic_r_text2num['大臂']] -= 1
            self.basic_resource[self.basic_r_text2num['超闪']] -= 1
            rest_layers = attack_num_list[0] * attack_num_list[1]
            if rest_layers < 6:
                return_string += '反弹了\n'
                return return_string
        else:
            rest_layers = attack_num_list[2] * attack_num_list[1]

        # print(self.shield_list)
        # print(self.shield_num_list)
        if rest_layers > self.rest_layers():
            raise Exception('你zu了！')
        else:
            if rest_layers >= sum(self.shield_num_list):
                for i in range(rest_layers - self.calculate_shield_layer(self.shield_list)):
                    return_string += f'掉了个{self.generator_list.pop(-1)}\n'
                for shield in self.shield_list:
                    return_string += f'掉了个{shield}\n'
                self.shield_list = []
                self.shield_num_list = []
            else:
                while True:
                    if rest_layers < self.shield_num_list[-1]:
                        break
                    shield = self.shield_list.pop(-1)
                    return_string += f'掉了个{shield}\n'
                    rest_layers -= self.shield_num_list.pop(-1)

                self.shield_num_list[-1] -= rest_layers
        return return_string

    @staticmethod
    def shan_calculate(attack_num_list, shan_num):
        defensed_num = int(shan_num / attack_num_list[0])
        # return_string += (defensed_num)
        if defensed_num >= attack_num_list[2]:
            return 0
        else:
            attack_num_list[2] -= defensed_num + 1
        rest_layers = 1 if (attack_num_list[0] * (defensed_num + 1) > shan_num + 1) else \
            int(attack_num_list[0] * (defensed_num + 1) - shan_num - 1)
        rest_layers += attack_num_list[2] * attack_num_list[1]
        return rest_layers

    def rest_layers(self):
        return len(self.generator_list) + sum(self.shield_num_list)

    def __str__(self):
        res = ''.join([i + ': ' + str(self.basic_resource[self.basic_r_text2num[i]]) + ' '
                       for i in self.basic_r_text2num.keys()])
        res += f' 层数 {self.rest_layers()}'
        return res
