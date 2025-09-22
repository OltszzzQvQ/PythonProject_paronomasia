import sys
import time

#定义物品类，代表游戏中的一个可拾取物品
class Item:
    def __init__(self,name,description):
        self.name =name
        self.description = description
    def __str__(self):
        return f"{self.name}:{self.description}"

#定义房间类 代表游戏中的一个房间
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}  # 往哪走
        self.items = []  # 房间里有啥
        self.locked_exits = {}#上锁的出口
        #self.unlocked_exits={}

    def add_item(self, item):#在房间里放置一个物品
        self.items.append(item)

    def add_locked_exit(self, direction, room):
        self.locked_exits[direction] = room  # 添加上锁出口

    def unlock_exit(self,direction):#添加解锁的出口
        if direction in self.locked_exits:
            self.exits[direction] = self.locked_exits[direction]
            del self.locked_exits[direction]
            return True
        return False
        # self.unlocked_exits[direction] = room#解锁出口
        # if direction in self.locked_exits:
        #     del self.locked_exits[direction]
        # self.exits[direction]=room

    def add_exit(self,direction,room):
            self.exits[direction]=room#添加出口

    def get_item(self,item_name):#从房间里拿走一个物品
            for item in self.items:
                if item.name.lower()==item_name.lower():
                    self.items.remove(item)
                    return item
            return None
#定义玩家类 负责追踪玩家的状态
class Player:
    def __init__(self,start_room):
        self.current_room = start_room
        self.inventory=[]#玩家的背包

    def move(self,direction):#尝试向某个方向移动
        if direction in self.current_room.exits:
            self.current_room = self.current_room.exits[direction]
            return True
        else:
            return False
    def take_item(self,item_name):#从当前房间拾取物品
        item = self.current_room.get_item(item_name)
        if item:
            self.inventory.append(item)#添加此物到玩家背包中
            print(f"你捡起了{item_name}.")
        else:
            print(f"这里没有{item_name}")


    def show_inventory(self):#显示玩家背包里的物品
        if not self.inventory:
            print("背包是空的")
        else:
            print("背包里面有：")
            for item in self.inventory:
                print(f"-{item.name}")
def validate_input(user_ipt,right_num):
    return user_ipt ==right_num,user_ipt
#Game类 负责创建世界、初始化玩家，并包含主游戏循环和命令解析
class  Game:
    def scan_input(self,right_num ="1024"):#设置解锁密码为1024
        max_attempt = 3#最大尝试次数
        attempts =0#定义尝试次数
        right_num="1024"

        while attempts<=max_attempt:
            user_ipt = input().strip()#检测用户输入
            if len(user_ipt) != 4:#用户输入的数字不为4位因此减一次机会
                return False, "输入位数不对，减一次机会"
            if not user_ipt.isdigit():#用户输入非数字 扣一次机会
                return False, "请输入数字，减一次机会"
            if user_ipt =="retry" and attempts>0:#用户输入retry重试
                print(f"第{attempts}次机会已经使用")
                continue
            correct,numbr=validate_input(user_ipt,right_num)#密码验证
            if correct:
                print("密码正确！门外似乎有一声解锁的声音")
                return True
            else:
                attempts+=1
                print("密码错误,输入'retry'重试")
        else:
            print("次数用完，逃离失败")
            return True


    def __init__(self):#游戏主类，负责整个游戏的流程
        self.player = None
        self.game_over = False
        self.time = None
        self.create_world()


    def create_world(self):#创建游戏世界、房间和物品
        #创建房间
        center =Room("密室中央","你站在密室中央，左侧有一扇锁着的铁门，右侧是一扇铁门后布满代码的显示屏（输入help查看指令）")
        control_room = Room("代码控制室","你站在布满代码的大屏幕前似乎在找什么东西......(输入help查看指令)")
        escape_way = Room("逃生通道入口","你来到了逃生入口面前想必你已经通过你的手段打开了铁门吧。输入最后的指令（escape）逃生吧勇士！！如果没有的话请在到处走走解开迷题吧")
        #创建物品
        key = Item("钥匙","一把生锈的钥匙，似乎是用来打开右侧铁门的")
        Udisk = Item("u盘","一个u盘不知道有什么用，先收着为妙！")
        #创建出口以及被锁住的门
        center.add_locked_exit("east",control_room)

        center.add_locked_exit("west",escape_way)
        control_room.add_locked_exit("north", escape_way)
        control_room.add_exit("west",center)

        escape_way.add_exit("north",control_room)

        escape_way.add_exit("east",center)
        #在房间中添加物品
        center.add_item(key)
        control_room.add_item(Udisk)
        #设立角色初始位置
        self.player = Player(center)

    def play_game(self):#游戏主循环
        print("你好玩家！欢迎来到本次的文字冒险游戏，在本次游戏中你作为一个逃生者被困在“虚空未来工作室密室”，通过输入指令在10min之内逃出这个诡异的地方吧！\n")
        print("在游戏中您可以输入关键词“help”查看指令说明，输入“quit”退出游戏，开始计时咯！\n")
        print("press start Enter the Game")
        while True:
            start_order = input().strip().lower()
            if start_order == 'start':#输入start游戏开始！
                break
            else:
                print("请输入'start'开始逃离")
        print("GAME START!")
        self.time = time.time()
        while not self.game_over:
            if time.time() - self.time >= 600:#定义如果超过10分钟则游戏失败
                print("\n时间到咯！很遗憾您没能掏出密室，游戏结束")
                break
            center_room = self.player.current_room
            # center_room.unlock_exit("east")##用于调试代码直接解锁代码控制室出口
            # self.player.move("east")
            # while True:
            self.describe_scene()
            command = input().strip().lower()#识别玩家指令 不区分大小写
            if not command:
                continue
            if self.handle_command(command):
                break
            if self.player.current_room.name == "逃生通道入口" and command == "escape":#在逃离通道阶段输入escape即可逃离
                print("恭喜逃离密室，成功获得虚空未来工作室资格")
                break
    def describe_scene(self):#描述场景
        room = self.player.current_room
        print(f"\n{room.name}")#显示环境名称
        print(room.description)

        if room.items:#显示房间里面有什么
            item_name = ",".join([item.name for item in room.items])
            print(f"你看到这里有：{item_name}")
        exits = ",".join(room.exits.keys())
        print(f"你可以选择的方向：{exits}")#使用.keys()获取出口方向

    def handle_command(self,command):#解析并处理玩家的指令
        parts = command.split(' ',1)#分割命令与参数
        verb = parts[0]
        noun = parts[1] if len(parts)>1 else ""
        if verb =='quit':
            print("欢迎下次游玩 拜拜:)")
            return True#return True表示游戏结束
        elif verb == 'help':
            self.show_help()

        elif verb == 'go':
            if self.player.move(noun):
                # 移动成功后不需要额外打印，describe_scene会处理
                pass
            else:
                print("这里没路了")
        elif verb == 'take':
            if noun:
                self.player.take_item(noun)
            else:
                print("你想要什么？")

        elif verb == 'inventory' or verb =='i':
            self.player.show_inventory()

        elif verb =='look':
            #look命令只是重新描述场景，循环开始时会自动做
            pass

        elif verb =='use':
            self.handle_use_command(noun)
        elif verb =='escape':
            return False#为了不让else与结束语句冲突
        else:
            print("何意呢？想要输入指令的话可以输入'help'哦，如果还是不行的话可以检查一下大小写")
        return False

    def handle_use_command(self, noun):
        room = self.player.current_room
        if self.player.current_room.locked_exits:#如果用户要往锁的门走
            if noun == "east":
                print("右侧的门锁着，你需要找到方法过去")
            elif noun == "west":
                print("左侧的门锁着，你需要找到方法过去")
            else:
                print("这里没路咯")

        if room.name == "密室中央":

            have_key = any(item.name == "钥匙" for item in self.player.inventory)#定义have_key 检查玩家背包中是否有钥匙 如果玩家背包中有物品的名称是钥匙
            if have_key and ("钥匙" in noun) and ("east" in noun or "右侧" in noun or "代码控制室" in noun):#用钥匙打开右侧大门
                if room.unlock_exit("east"):
                    print("你用钥匙打开了右侧的门，可以进到控制室咯")
                else:
                    print("你已经打开过右侧的门了")
            elif have_key and ("钥匙" in noun) and ("左侧" in noun or "west" in noun):
                print("此钥匙无法打开左侧的大门")
            else:
                print("输入指令错误！请重试")

        elif room.name == "代码控制室":#捡到u盘后
            have_udisk = any(item.name == "u盘" for item in self.player.inventory)#定义have_udisk
            if have_udisk and ("u盘" in noun or "udisk" in noun) and ("代码控制室" in noun or "电脑" in noun):#用u盘插入电脑
                print("你将u盘插入了电脑中")
                print("电脑打印出了一串你看不懂的符号：•----,-----，••---，••••-")
                print("你对着纸条沉思许久，你突然想到在之前看带战争电影时传输机密文件的一种加密方式，即摩斯电码！")
                print("摩斯电码对照表：\n•---- 1\n••---2\n•••--3\n••••-4\n•••••5\n-••••6\n--•••7\n---••8\n----•9\n-----0")
                print("输入最终的密码吧！少年！")
                #password = input_num("请输入密码：")
                result = self.scan_input("1024")#检测用户输入的密码
                if result:#如果正确
                    room.unlock_exit("north")
                else:
                    print("解锁失败")
                    return True



    def show_help(self):
        print("\n---指令列表---")
        print("go [where](比如：go north/east/west)")
        print("take -物品")
        print("use <空格> [物品名] <空格> [目标] 在目标上使用物品（eg：use u盘 电脑）")
        print("inventory  查看背包")
        print("look 查看环境")
        print("help 显示帮助")
        print("quit 退出游戏")
        print("---------------")
if __name__ =='__main__':
    game=Game()
    game.play_game()

