import time
from typing import Dict,List, Optional, Tuple #型アノテーション
import os
from itemList import ItemList,SkillsList,Cards,userList,toJP,stateList
import random

'''
コンストラクタ: player, Cards, Item
MemberDict: playerの名前とPlayer
    ->Player: HP,MP,Money 
        -> playerの基本情報
Cards: HP, MP, Money 
    -> Cardは武器の詳細設定
        -> ItemList(dict)として扱われる
Item: 実際にPlayerの値をを変更する
'''
class Player():
    def __init__(self,hp:int = 30,mp:int = 20,money:int = 20,items:list[Cards] = None,usedItem:list[Cards] = None,state:str = "wait",died:bool = False) -> None:
        self.hp = hp
        self.mp = mp
        self.money = money
        self.items = items if items is not None else []
        self.usedItem = usedItem if usedItem is not None else []
        self.state = state
        self.died = died
        
    def __str__(self):
        return f"HP: {self.hp}, MP: {self.mp}, Money: {self.money}"
    
    def __repr__(self):
        # 開発者がデバッグしやすい形式で情報を返す
        return f"Player(hp={self.hp}, mp={self.mp}, money={self.money}, items={self.items})"

class Item():
    def __init__(self,player:Player = None,hp:int = 0,mp:int = 0,money:int = 0) -> None:
        self.hp = hp
        self.mp = mp
        self.money = money
    
    def apply(self, player: Player) -> None:
        """アイテムの効果をプレイヤーに適用"""
        player.hp += self.hp
        player.mp += self.mp
        player.money += self.money

class CardItem:
    def __init__(self, player: Player, card: Cards):
        """Cardの効果をプレイヤーに適用"""
        item = Item(hp=card.hp, mp=card.mp, money=card.money)
        item.apply(player)

class MemberDict():
    def __init__(self):
        self.members:Dict[str, Player] = {}
        
    def add_player(self, name: str, player: Player):
        if name not in tuple(self.members.keys()):
            self.members[name] = player 
        else:
            print("同じ名前は登録出来ません")
        
    def to_dict(self):   
        return self.members
    
    def get_info(self,player_name):
        return self.members.get(player_name)

import tkinter
from PIL import Image, ImageTk
import addon
class Appview(tkinter.Canvas):
    turnCounter = 0
    b_Submit = False
    def __init__(self, root:Optional[tkinter.Tk]=None):
        self.Screen_width = 1200
        self.Screen_height = 900

        super().__init__(root, width=self.Screen_width, height=self.Screen_height)
        self.root = root
        self.pack()
        self.pack_propagate(0)

        self.create_shape()
        self.load_field()
        self.On_click()
        
        #addon.ClickHandler(self)
        
    #対象の図形の始点を(0,0)として図形を描く    
    def relative_PS(self,Card_Shape,x,y,dx,dy,flg = False,outline:str = ""): #relative position Shape
        Shape = self.coords(Card_Shape)
        x1,y1,dx1,dy1 = list(map(int,Shape))
        name = self.itemcget(Card_Shape,"tags")
        if flg:
            print(name,dx1-x1,dy1-y1)
        if x1+x+dx > dx1 or y1+y+dy > dy1:
            print("図形の範囲外")            
        self.set_pos = self.create_rectangle(x1+x, y1+y, x1+x+dx, y1+y+dy, fill="",outline= outline)
        return self.set_pos
    
    def set_position(self,itemIdx,r_margin:int = 0,c_margin:int = 0,count:int = 1):
        Shape = self.coords(itemIdx)
        x,y,dx,dy = list(map(int,Shape))
        setR:int = (r_margin + (dx - x))*(count-1)
        setC:int = (c_margin + (dy - y))*(count-1)
        if r_margin > 0:
            return self.create_rectangle(x+setR,y,dx+setR,dy)
        elif c_margin > 0:
            return self.create_rectangle(x,y + setC,dx,dy+setC)
    
    def CreateText(self,baseShape,text,tag,fontSize:int=14,font_color:str = "black",anchor:str = "center"):
        Shape = self.coords(baseShape)
        x,y,dx,dy = list(map(int,Shape))
        centerPosX = (x + dx)//2
        centerPosY = (y + dy)//2
        return self.create_text(centerPosX,centerPosY,text=text, font=("Arial", fontSize), fill=font_color,tags = tag,anchor=anchor)
    
    def create_shape(self):
        #---図形---
            
        #アイテム 
        self.arrItem:list = []
        self.item_space = self.create_rectangle(31,607,765,875,tags="item_space",outline="") # item space 
        self.item = self.relative_PS(self.item_space,32,15,110,110) #item base
        
        #self.arrItem.append(self.item)
        i=0
        margin = 20
        self.col_shape = self.set_position(self.item,0,margin,2)
        for i in range(5):
            self.arrItem.append(self.set_position(self.item,margin+10,0,i+1))
            self.arrItem.append(self.set_position(self.col_shape,margin+10,0,i+1))
        
        for idx, i in enumerate(self.arrItem):
            you = list(memberDict.to_dict().items())[0]
            if you[1].items[idx].skills == SkillsList[0]:
                self.itemconfig(i,tags = (f'{idx}',"item"),fill = "#EFC4A2")
            elif you[1].items[idx].skills == SkillsList[1]:
                self.itemconfig(i,tags = (f'{idx}',"item"),fill = "lightblue")
            elif you[1].items[idx].skills == SkillsList[2]:
                self.itemconfig(i,tags = (f'{idx}',"item"),fill = "#F9E1FF")
        
        #メンバー        
        self.member_space = self.create_rectangle(783,27,1170,571,outline="") # member space x=785, y=27 800, 50, 1190, 620
        margin = 40
        self.member:list = []
        
        for _ in range(len(memberDict.to_dict())):
            self.member.append(self.relative_PS(self.member_space,18,10+margin,350,70))
            self.itemconfig(self.member[len(self.member)-1],fill = "#D8C8CF",tags = (f"{len(self.member)-1}","member"))
            margin += 80
            
        #ボタン
        self.submit = self.create_rectangle(780,620,1170,700,fill="silver",tags = "Submit",outline="black")# 820,695,1170,853 silver
    
        #----text---
            
        #メンバー
        #self.create_text(825,20,text="Members",font=("Arial", 20), fill="black",anchor = "nw")
        self.arrMembers_text = []
        for idx, (name, player) in enumerate(memberDict.to_dict().items()):
            self.arrMembers_text.append(self.CreateText(self.member[idx],f'{name}: {player}',tag=(f'{idx}',"member")))
            
        #アイテム
        self.arrItemText:list = []
        for idx,i in enumerate(self.arrItem):
            you = list(memberDict.to_dict().items())[0]
            
            if you[1].items[idx].hp != 0:
                num = str(abs(you[1].items[idx].hp))
            elif you[1].items[idx].mp != 0:
                num = str(abs(you[1].items[idx].mp))
                
            if len(num) == 1:
                num =  " " + num 
            text = f"{toJP(you[1].items[idx].skills)}\n{num}"

            if you[1].items[idx].skills == SkillsList[0]:
                self.arrItemText.append(self.CreateText(i,text = text,tag=(idx,"item"),fontSize=20,font_color="red"))
            elif you[1].items[idx].skills == SkillsList[1]:
                self.arrItemText.append(self.CreateText(i,text = text,tag=(idx,"item"),fontSize=20,font_color="blue"))
            else:
                self.arrItemText.append(self.CreateText(i,text = text,tag=(idx,"item"),fontSize=20,font_color="black"))
        #ボタン
        self.CreateText(self.submit,"決定","Submit")
        
        #画像    
        def img(img_path:str,resize:list,position:list):
                
            # PNG画像のパス
            image = Image.open(img_path)

            # 画像をリサイズ
            resized_image = image.resize((resize[0], resize[1]))  

            # tkinter用の画像に変換
            tk_image = ImageTk.PhotoImage(resized_image)
            self.image_reference = tk_image
            # Canvasに画像を貼り付け
            return self.create_image(position[0], position[1], image=tk_image, anchor="nw")
        
        #背景
        screen = [self.Screen_width,self.Screen_height]
        pos = [0,0]
        current_path = os.getcwd()
        path = os.path.join(current_path,"img\\background_design1.png")
        background_img = img(path,screen,pos)#background_design1
        self.tag_lower(background_img)
        
        #---battle field---
        self.battle_space = self.create_rectangle(31,27,385,571,tags = "battle_space",outline = "") #60,20,385,620
        attackField_item = self.relative_PS(self.battle_space,0,60,354,50,outline="")
        self.attackText = self.CreateText(attackField_item,"","text",font_color="red")
        self.attactMemberShape = self.relative_PS(self.battle_space,0,0,354,60,outline="")
        self.attackMemberText = self.CreateText(self.attactMemberShape,text = "",tag="attackMemberText",fontSize=18)
        
        self.defensed_space = self.create_rectangle(401,26,766,570,tags = "defense_space",outline = "")
        defenseField_item = self.relative_PS(self.defensed_space,0,60,365,50,outline="")
        self.defenseText = self.CreateText(defenseField_item,"","text",font_color="blue")
        self.defenseMemberShape = self.relative_PS(self.defensed_space,0,0,365,60,outline="")
        self.defenseMemberText = self.CreateText(self.defenseMemberShape,text = "",tag = "defenseMemberText",fontSize=18)
        
        #---battle finish---
        self.finished_space = self.create_rectangle(31,192,766,352,fill= "",outline="")
        self.finishedSpaceText = self.CreateText(self.finished_space,"",tag = "finishedSpaceText",fontSize=50)
        
        self.exitPageShape = self.create_rectangle(208,330,590,500,outline="",tags = "exitBtn")
        self.exitPageText = self.CreateText(self.exitPageShape,text="",tag="exitBtn",fontSize=30)
        
    #---turn switch
    def Finished_field(self):
        self.itemconfig(self.finishedSpaceText,text = f"aaaa win")
        self.itemconfig(self.exitPageShape,tags = "exitBtn_on",outline = "black", fill = "#B7F9DD")
        self.itemconfig(self.exitPageText,tags = "exitBtn_on",text = "ゲールを終了する")
        for name,plyer in memberDict.to_dict().items():
            if plyer.died == False:
                self.itemconfig(self.finishedSpaceText,text = f"{name} win")
        
    def attack_field(self,attack_player:tuple):
        atPlayer:Player = list(attack_player)[1]        
        #---テキスト---
        if not atPlayer.usedItem:
            text = "No attack item selected"
        else:
            text = f'{atPlayer.usedItem[0].itemName} {abs(atPlayer.usedItem[0].hp)} {atPlayer.usedItem[0].skills}'
        
        self.itemconfig(self.attackMemberText,text = attack_player[0])
        self.itemconfig(self.attackText,text = text)
    
    def defensed_field(self,defense_player:tuple):
        dfPlayer:Player = list(defense_player)[1]        
        #---テキスト---
        if not dfPlayer.usedItem:
            text = "No defense item selected"
        else:
            text = f'{dfPlayer.usedItem[0].itemName} {abs(dfPlayer.usedItem[0].hp)} {dfPlayer.usedItem[0].skills}'
            
        self.itemconfig(self.defenseMemberText,text = defense_player[0])
        self.itemconfig(self.defenseText,text = text)
                    
    #----Userのみの操作----始
    def On_click(self):
        #クリック位置を取得
        self.tag_bind("item","<Button-1>", self.ItemClick_event) #アイテムクリックした時のボタンリスナー
        self.tag_bind("Submit","<Button-1>", self.SubmitClik_event) #決定をクリックした時のボタンリスナー

        self.tag_bind("exitBtn_on","<Button-1>",self.on_exitBtn)
        self.tag_bind("item", "<Enter>", self.on_hover)
        self.tag_bind("item", "<Leave>", self.on_leave) 
    
    def on_hover(self,event):
        #アイテム説明
        def item_description(item_name):
            #850,440
            if item_name in ItemList:
                card = ItemList[item_name]

            text = (
                f"アイテム名: {item_name}\n"
                f"  HP: {abs(card.hp)}\n"
                f"  MP: {abs(card.mp)}\n"
                f"  Money: {card.money}\n"
                f"  説明: {card.description}"
            )
            return self.create_text(775,730,text=text, font=("Arial", 14), fill="black",anchor="nw")
            
        self.items = self.find_closest(event.x, event.y)[0]
        get_data = list(self.gettags(self.items))
        if get_data[0].isdigit() == False:
            return
        idx = int(get_data[0])
        selectItem:Player = list(memberDict.to_dict().items())[0][1]
        self.textid = item_description(selectItem.items[idx].itemName)
        self.itemconfig(self.arrItem[idx],outline = "blue")
        
    def on_leave(self,event):
        if self.textid != None:
            self.delete(self.textid)
        get_data = list(self.gettags(self.items))
        if get_data[0].isdigit() == False:
            return
        idx = int(get_data[0])
        self.itemconfig(self.arrItem[idx],outline = "black")

    def on_exitBtn(self,event):
        self.root.quit()
        self.root.destroy()
        #TODO 別のwindowを呼び出す
        
    def ItemClick_event(self, event):
        statepl:Player = list(memberDict.to_dict().items())[0][1]
        if statepl.state == stateList[2]: #wait
            return
        
        items = self.find_closest(event.x, event.y)[0]
        get_data = list(self.gettags(items))
        if get_data[0].isdigit() == False:
            return
        #-------------------------------------------------------------
        if statepl.state == stateList[0]: #attack
            attackPlayer = list(memberDict.to_dict().items())[0][1]
            selectItem = attackPlayer.items[int(get_data[0])]
            
            if selectItem.skills == SkillsList[1] or abs(selectItem.mp) > attackPlayer.mp:
                return
            
            if len(attackPlayer.usedItem) > 0:
                attackPlayer.usedItem.clear()
                
            attackPlayer.usedItem.append(selectItem)
            self.attack_field(list(memberDict.to_dict().items())[0])
        #--------------------------------------------------------------   
        if statepl.state == stateList[1]: #defense
            defensePlayer = list(memberDict.to_dict().items())[0][1]
            selectItem = defensePlayer.items[int(get_data[0])]
            if selectItem.skills != SkillsList[1]:
                return
            
            if len(defensePlayer.usedItem) > 0:
                defensePlayer.usedItem.clear()
                
            defensePlayer.usedItem.append(selectItem)
            self.defensed_field(list(memberDict.to_dict().items())[0])
        #----------------------------------------------------------------

    
    def SubmitClik_event(self,event):
        my_player = list(memberDict.to_dict().items())[0]
        for idx,(name,player) in enumerate(memberDict.to_dict().items()):
            if player.state == stateList[0]:
                attackplayer = list(memberDict.to_dict().items())[idx]
            elif player.state == stateList[1]:
                defenseplayer = list(memberDict.to_dict().items())[idx]
                
        if len(my_player[1].usedItem)>0:
            if len(defenseplayer[1].usedItem)>0:
                if defenseplayer[1].usedItem[0].skills == SkillsList[1]:
                    # if my_player[1].usedItem[0].skills != SkillsList[2]:
                    app_view.defensed_field(defenseplayer)
                    app_view.update_idletasks()
                    time.sleep(2)
            damageCalculation(attackplayer,defenseplayer)  
            Appview.turnCounter = (Appview.turnCounter + 1) % len(memberDict.to_dict())
            player_control()
        else:
            damageCalculation(attackplayer,defenseplayer)  
            Appview.turnCounter = (Appview.turnCounter + 1) % len(memberDict.to_dict())
            player_control()
        
    #----Userのみの操作----終
    
    def load_field(self):
        #メンバーの枠線に色をつける
        for idx,(name,player) in enumerate(memberDict.to_dict().items()):
            self.itemconfig(self.arrMembers_text[idx],text = f'{name} {player}')
            tuple_player = list(memberDict.to_dict().items())[idx]
            #アタックプレイヤーに赤枠縁、ディフェンスは青
            if player.state == stateList[0]:
                self.itemconfig(self.member[idx],outline = "red",width = 2)#A66767FF
                self.attack_field(tuple_player)
            elif player.state == stateList[1]:
                self.itemconfig(self.member[idx],outline = "blue",width = 2)
                if tuple_player[0] == list(memberDict.to_dict().items())[0][0]:
                    self.defensed_field(tuple_player)
            elif player.state == stateList[2]:
                self.itemconfig(self.member[idx],outline = "black",width = 2)  
                
            if player.hp == 0:
                self.itemconfig(self.member[idx],fill = "#B2B2B2",outline = "#505050") 
            if b_died() == True:
                for name,player in memberDict.to_dict().items():
                    if player.died == False:
                        player.state = stateList[2]
                        self.Finished_field()
                
        for i in range(10):
            you = list(memberDict.to_dict().items())[0]
            if you[1].items[i].hp != 0:
                num = str(abs(you[1].items[i].hp))
            elif you[1].items[i].mp != 0:
                num = str(abs(you[1].items[i].mp))
            if len(num) == 1:
                num =  " " + num 
            text = f"{toJP(you[1].items[i].skills)}\n{num}"
            
            if you[1].items[i].skills == SkillsList[0]:
                self.itemconfig(self.arrItemText[i],text=text,fill = "red")
                self.itemconfig(self.arrItem[i],fill = "#EFC4A2")
            elif you[1].items[i].skills == SkillsList[1]:
                self.itemconfig(self.arrItemText[i],text=text,fill = "blue")
                self.itemconfig(self.arrItem[i],fill = "lightblue")
            else:
                self.itemconfig(self.arrItemText[i],text=text,fill = "black")
                self.itemconfig(self.arrItem[i],fill = "#F9E1FF")
        
        self.update_idletasks()        
        self.after(100,self.load_field)

    def AI_battle(self):
        d = False
        a = False
        for i in range(len(memberDict.to_dict().items())-1):
            i += 1
            AI = list(memberDict.to_dict().items())[i]
            if AI[1].state == stateList[0]:
                attack = AI
                a = True
            elif AI[1].state == stateList[1]:
                defense = AI
                d = True
        if a == True and d == True:
            self.defensed_field(defense)
            self.attack_field(attack)
            self.update_idletasks()
            time.sleep(2)

memberDict = MemberDict()
def User_input():
    player_name = input("User name: ") #player name
    print("2～5人までです")
    num_player = int(input("player_of_people: ")) #対戦人数
    
    while num_player < 1 or num_player > 5:
         num_player = int(input("player_of_people: "))
         
    you = Player()
    memberDict.add_player(player_name,you)
    NPC:list[Player] = []
    arrItemlist = list(ItemList.keys())

    for i in range(num_player-1): #Member Class add
        NPC.append(Player())
        randChoice = random.choice(userList)
        memberDict.add_player(randChoice,NPC[i])
        userList.remove(randChoice)
        

    for name,player in memberDict.to_dict().items(): #player item append
        for i in range(10):
            random_itemName = random.choice(arrItemlist)
            random_item = ItemList[random_itemName]
            player.items.append(random_item)
            player.items[i].itemName = random_itemName
    list(memberDict.to_dict().items())[0][1].hp = 1
        
def damageCalculation(attackPlayer:tuple[str,Player],defensePlayer:tuple[str,Player]):
    
    if len(attackPlayer[1].usedItem) == 0:
        return 0,defensePlayer
    
    if attackPlayer[1].usedItem[0].skills == SkillsList[2]: #魔法か判定(HP,MP回復)
        defensePlayer[1].usedItem.clear()
        if abs(attackPlayer[1].usedItem[0].hp) > 0:
            list(attackPlayer)[1].hp += attackPlayer[1].usedItem[0].hp
            
        elif abs(attackPlayer[1].usedItem[0].mp) > 0:
            list(attackPlayer)[1].mp += attackPlayer[1].usedItem[0].mp
        onlyItems(attackPlayer)
        return
    
    elif attackPlayer[1].usedItem[0].skills == SkillsList[0]: #MPによる攻撃武器
        if len(defensePlayer[1].usedItem) == 0:
            damage = attackPlayer[1].usedItem[0].hp
            list(attackPlayer)[1].mp += list(attackPlayer)[1].usedItem[0].mp
            onlyItems(attackPlayer)
        else:
            damage =  list(attackPlayer)[1].usedItem[0].hp - list(defensePlayer)[1].usedItem[0].hp
            list(attackPlayer)[1].mp += list(attackPlayer)[1].usedItem[0].mp
            onlyItems(attackPlayer)
            onlyItems(defensePlayer)
            
    elif len(defensePlayer[1].usedItem) == 0: #MP消費なしの攻撃
        damage = attackPlayer[1].usedItem[0].hp
        list(attackPlayer)[1].mp += list(attackPlayer)[1].usedItem[0].mp
        onlyItems(attackPlayer)
    else:    
        damage =  list(attackPlayer)[1].usedItem[0].hp - list(defensePlayer)[1].usedItem[0].hp
        list(attackPlayer)[1].mp += list(attackPlayer)[1].usedItem[0].mp
        onlyItems(attackPlayer)
        onlyItems(defensePlayer)
    view = Appview()
    view.attack_field(attackPlayer)
    view.defensed_field(defensePlayer)
    if damage < 0:
        list(defensePlayer)[1].hp += damage
        if defensePlayer[1].hp <= 0:
            defensePlayer[1].hp = 0
            defensePlayer[1].died = True
        
    return damage,defensePlayer

def AI_choiceItem(NPCplayer:tuple[str,Player]) -> tuple[str,Player]:
    
    ChoiceItem:Cards = random.choice(list(NPCplayer)[1].items)
    b_attackSkills = True
    b_defenseSkills = True
    
    for playerItems in NPCplayer[1].items:
        if playerItems.skills == SkillsList[0] or (playerItems.mp > 0 and playerItems.hp == 0) or (playerItems.hp > 0 and playerItems.mp == 0):
            b_attackSkills = False
    
        if playerItems.skills == SkillsList[1]:
            b_defenseSkills = False
        
        if b_attackSkills == False and b_defenseSkills == False:
            break
    
    i = 1

    while True:
        i = i+1
        if NPCplayer[1].state == stateList[0]: #NPCの攻撃武器(magic or attack)  
            if b_attackSkills:
                ChoiceItem = None
                break
            elif ChoiceItem.skills != SkillsList[1]: #Item state get attack
                break
            else:
                ChoiceItem:Cards = random.choice(list(NPCplayer)[1].items)
            
        if NPCplayer[1].state == stateList[1]:
            if b_defenseSkills:
                ChoiceItem = None
                break
            elif ChoiceItem.skills == SkillsList[1]:
                break
            else:
                ChoiceItem:Cards = random.choice(NPCplayer[1].items)        
    if ChoiceItem != None:            
        list(NPCplayer)[1].usedItem.append(ChoiceItem)
        
    return NPCplayer

def b_died():

    countMember = len(memberDict.to_dict().items())
    flg_player = list(memberDict.to_dict().items())
    diedCounter = 0
    for i in range(countMember):
        if flg_player[i][1].died:
            diedCounter += 1
    if diedCounter == countMember-1:
        return True
    else:
        return False
    
def player_control():
    
    #playerのステータスの初期化
    for name,player in memberDict.to_dict().items():
        player.state = stateList[2]
    
    attackPlayer:tuple[str,Player] = list(memberDict.to_dict().items())[Appview.turnCounter] #攻撃するplyer
    defencePlayer:tuple[str,Player] = random.choice(list(memberDict.to_dict().items())) #守備するplayer

    member_keys = list(memberDict.to_dict().keys())
    defencePlayerValue = member_keys.index(list(defencePlayer)[0])
    
    while True:
        flg = True
        if b_died() == False:
            if attackPlayer[1].died == True:
                Appview.turnCounter = (Appview.turnCounter + 1) % len(memberDict.to_dict())
                attackPlayer = list(memberDict.to_dict().items())[Appview.turnCounter]
                flg = False
                
            if defencePlayer[1].died == True or defencePlayer[0] == attackPlayer[0]:
                defencePlayerValue = (defencePlayerValue + 1) % len(memberDict.to_dict())
                defencePlayer = list(memberDict.to_dict().items())[defencePlayerValue]
                flg = False
            
            if flg:
                break
        else:
            app_view.load_field()
            break
    
    #playerのステータスを変更
    defencePlayer[1].state = stateList[1]
    attackPlayer[1].state = stateList[0]
    
    #player item 選択    
    if defencePlayer[0] != list(memberDict.to_dict().items())[0][0]:
        defencePlayer = AI_choiceItem(defencePlayer)
    if attackPlayer[0] != list(memberDict.to_dict().items())[0][0]:
        attackPlayer = AI_choiceItem(attackPlayer)
        while True:
            if abs(attackPlayer[1].usedItem[0].mp) > attackPlayer[1].mp and abs(attackPlayer[1].usedItem[0].hp) >0:
                attackPlayer[1].usedItem.clear()
                attackPlayer = AI_choiceItem(attackPlayer)
            else:
                break
    
    list(memberDict.to_dict().items())[Appview.turnCounter] = attackPlayer
    list(memberDict.to_dict().items())[defencePlayerValue] = defencePlayer
    
    app_view.load_field()
    AI_checker()

def onlyItems(player:tuple[str,Player]):
    arrItemlist = list(ItemList.keys())
    for idx,i in enumerate(list(player[1].items)):
        if not player[1].usedItem:
            return
        if player[1].usedItem[0] == i:
            random_itemName = random.choice(arrItemlist)
            random_item = ItemList[random_itemName]
            if abs(player[1].usedItem[0].mp) > 0:
                CountItems = len(player[1].items)-1
                idx = random.randint(0,CountItems)
            list(player)[1].items[idx] = random_item
            list(player)[1].items[idx].itemName = random_itemName
            list(player)[1].usedItem.clear()

def AI_checker():

    for idx in range(len(memberDict.to_dict().items())-1):
        idx += 1
        AIplayer = list(memberDict.to_dict().items())[int(idx)]
        if AIplayer[1].state == stateList[0]:
            attactplayer = AIplayer
        elif AIplayer[1].state == stateList[1]:
            defenseplayer = AIplayer
    
    UserPlayer = list(memberDict.to_dict().items())[0]
    if UserPlayer[1].state == stateList[0]:
        return
    
    if UserPlayer[1].state == stateList[1]:
        app_view.attack_field(attactplayer)
    
    if UserPlayer[1].state == stateList[2]:
        app_view.AI_battle()
        damageCalculation(attactplayer,defenseplayer)
        Appview.turnCounter = (Appview.turnCounter + 1) % len(memberDict.to_dict())
        player_control()
        
app_view = None          
def main():
    global app_view
    
    User_input()
    root = tkinter.Tk()
    root.title("test")
    app_view = Appview(root)
    player_control()
    root.mainloop()
    
main()

