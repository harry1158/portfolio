class Cards:
    def __init__(self, hp: int = 0, mp: int = 0, money: int = 0, skills: str = "", description: str = "",itemName:str = "") -> None:
        self.hp = hp
        self.mp = mp
        self.money = money
        self.skills = skills
        self.description = description
        self.itemName = itemName
        
def toJP(description:str = ""):
    if description == SkillsList[0]:
        return "攻"
    if description == SkillsList[1]:
        return "守"
    if description == SkillsList[2]:
        return "魔"
        

SkillsList = ["attack", "defense", "magic"]
stateList = ["attack","defensed","wait"]
userList = [
    "Taro", "Hana", "YamaG01", "Aki", "Shin",
    "Mika", "Ken", "Sana", "Yuki", "Hiro",
    "Kao", "Taka", "Mai", "Ryo", "Masa",
    "Nori", "Rika", "Sho", "Nao", "Kazu",
    "Rei", "Jun", "Aoi", "Sora", "Ren",
    "Kai", "Haru", "Momo", "Riku", "Tsubasa"
]

ItemList = {
    "Shadowfang":   Cards(-3, 0, 0, SkillsList[0], f"闇の力を宿した短剣。\n{' ' * 12}迅速な攻撃を可能にする。"),
    "Blazeblade":   Cards(-3, 0, 0, SkillsList[0], f"炎の魔法で鍛えられた剣。\n{' ' * 12}敵を焼き尽くす力を持つ。"),
    "Frostmourne":  Cards(-5, 0, 0, SkillsList[0], "凍てつく冷気を放ち、敵を鈍らせる。"),
    "Stormbreaker": Cards(-5, 0, 0, SkillsList[0], "嵐を操る力を秘めた伝説の大剣。"),
    "Duskreaver":   Cards(-10, 0, 0, SkillsList[0], "日没の闇から力を得る恐ろしい大鎌。"),
    "Nightpiercer": Cards(-10, 0, 0, SkillsList[0], "光を伴う矢で、闇の敵を撃ち抜く。"),
    "Thunderclaw":  Cards(-3, -3, 0, SkillsList[0], "稲妻のような速さで攻撃を繰り出す爪。"),
    "Voidfang":     Cards(-3, -2, 0, SkillsList[0], "空虚の力を持つ短剣で、敵の精神を蝕む。"),
    "Crimsonedge":  Cards(-5, -5, 0, SkillsList[0], f"血の呪いを受けた剣。\n{' ' * 12}攻撃する度に血を吸い取る。"),
    "Dragonsbane":  Cards(-5, -3, 0, SkillsList[0], "ドラゴン討伐のために鍛えられた伝説の剣。"),
    "Phoenixflare": Cards(-10, -10, 0, SkillsList[0], f"不死鳥の力を宿し、\n{' ' * 12}再生と破壊を象徴する剣。"),
    "Oblivionfang": Cards(-10, -5, 0, SkillsList[0], "敵の記憶を奪い去る不気味な短剣。"),
    "Skysplitter":  Cards(-15, 0, 0, SkillsList[0], "天空を断ち切るほどの力を持つ大剣。"),
    "Earthshaker":  Cards(-15, 0, 0, SkillsList[0], f"一撃で地面を割るほどの\n{' ' * 12}破壊力を持つ巨大な槌。"),
    "Venomspike":   Cards(-25, -30, 0, SkillsList[0], "敵を毒状態にする呪いが込められた槍。"),
    "Lightbringer": Cards(-2, -1, 0, SkillsList[0], "闇を切り裂く純粋な光を発する剣。"),
    "Darkcleaver":  Cards(-2, 0, 0, SkillsList[0], f"闇の魔力を断ち切るために\n{' ' * 12}作られた神秘の斧。"),
    "Starforged":   Cards(-4, 0, 0, SkillsList[0], "星の破片を用いて鍛えられた神秘の剣。"),
    "Hellrend":     Cards(-5, 0, 0, SkillsList[0], "地獄の炎を宿した剣で、灼熱の力を持つ。"),
    "Moonshadow":   Cards(-6, -3, 0, SkillsList[0], "月の光と闇を操る神秘の剣。"),
    
    "Shield of Guardian": Cards(-3, 0, 0, SkillsList[1], f"伝説の盾。\n{' ' * 12}持ち主をあらゆる危険から守る力を持つ。"),
    "Holy Barrier":       Cards(-5, 0, 0, SkillsList[1], f"神聖な力を宿した盾。\n{' ' * 12}悪しきものを寄せ付けない。"),
    "Iron Wall":          Cards(-8, 0, 0, SkillsList[1], f"純鉄で作られた頑丈な盾。\n{' ' * 12}物理攻撃に強い。"),
    "Dragon Shield":      Cards(-10, 0, 0, SkillsList[1], f"古代ドラゴンの鱗から作られた盾。\n{' ' * 12}炎をも防ぐ力を持つ。"),
    "Sacred Defender":    Cards(-12, 0, 0, SkillsList[1], f"神々の祝福を受けた盾。\n{' ' * 12}正義を守る者のために作られた。"),
    "Eternal Shield":     Cards(-15, 0, 0, SkillsList[1], f"時を越えて壊れない盾。\n{' ' * 12}永遠の守護を誓う。"),
    "Earth Guardian":     Cards(-20, 0, 0, SkillsList[1], f"大地の力を宿した盾。\n{' ' * 12}自然の防御を提供する。"),
    "Protection Blade":   Cards(-22, 0, 0, SkillsList[1], f"攻撃と防御を両立した武器盾。\n{' ' * 12}万能の一品。"),
    "Sword of Safety":    Cards(-25, 0, 0, SkillsList[1], f"持ち主の安全を保証する剣。\n{' ' * 12}防御力に特化している。"),
    "Light Shield":       Cards(-30, 0, 0, SkillsList[1], f"輝くオーラを放つ軽量の盾。\n{' ' * 12}素早い戦闘に適している。"),
    "Phoenix Shield":     Cards(-10, 0, 0, SkillsList[1], f"不死鳥の灰から再生した盾。\n{' ' * 12}再生力を持つ。"),
    "Storm Barrier":      Cards(-15, 0, 0, SkillsList[1], f"嵐の力を封じ込めた盾。\n{' ' * 12}強力なエネルギーで攻撃を跳ね返す。"),
    "Knight Wall":        Cards(-3, 0, 0, SkillsList[1], f"高潔な騎士が愛用する伝統的な盾。\n{' ' * 12}忠誠と防御の象徴。"),
    "Crystal Defense":    Cards(-5, 0, 0, SkillsList[1], f"魔法のクリスタルで作られた盾。\n{' ' * 12}魔法攻撃を防ぐ特性を持つ。"),
    "Gold Armor":         Cards(-8, 0, 0, SkillsList[1], f"黄金で作られた輝く盾。\n{' ' * 12}敵の目を眩ませる力がある。"),
    "Black Fortress":     Cards(-6, 0, 0, SkillsList[1], f"黒く不気味な盾。\n{' ' * 12}攻撃を吸収する呪いがかけられている。"),
    "Blessing Shield":    Cards(-7, 0, 0, SkillsList[1], f"祝福の力を宿した盾。\n{' ' * 12}味方全体に守護の効果を与える。"),
    "Shadow Protector":   Cards(-4, 0, 0, SkillsList[1], f"闇の中で存在を隠す盾。\n{' ' * 12}隠密行動に最適。"),
    "Mystic Guard":       Cards(-5, 0, 0, SkillsList[1], f"呪いや魔法攻撃を無効化する神秘的な盾。"),
    "Spell Barrier":      Cards(-3, 0, 0, SkillsList[1], f"魔法のバリアを展開する盾。\n{' ' * 12}強力な呪文をも遮る力を持つ。"),
    
    "Life Potion":      Cards(3, 0, 0, SkillsList[2], "生命力を回復する基本的なポーション。"),
    "Heal Herb":        Cards(5, 0, 0, SkillsList[2], "古くから使われる癒しの薬草。"),
    "Recovery Droplet": Cards(8, 0, 0, SkillsList[2], "神秘的な力を持つ回復の雫。"),
    "Healing Crystal":  Cards(10, 0, 0, SkillsList[2], "魔法の結晶がHPを回復してくれる。"),
    "Regen Elixir":     Cards(15, 0, 0, SkillsList[2], "飲むと徐々にHPが回復するエリクサー。"),
    "Sacred Fruit":     Cards(3, 0, 0, SkillsList[2], "神聖な力を秘めた果実。"),
    "Phoenix Tear":     Cards(5, 0, 0, SkillsList[2], "不死鳥の涙。傷ついた者を癒す奇跡の雫。"),
    "Mana Honey":       Cards(8, 0, 0, SkillsList[2], "魔力を含んだ特別な蜂蜜。"),
    "Healing Gem":      Cards(10, 0, 0, SkillsList[2], "持つだけで体が癒される宝石。"),
    "Energy Bread":     Cards(15, 0, 0, SkillsList[2], "食べると体力が回復する特製のパン。"),
    
    "Mana Potion":      Cards(0, 3, 0, SkillsList[2], "魔力を回復する基本的なポーション。"),
    "Ether Herb":       Cards(0, 5, 0, SkillsList[2], "魔法の力を秘めた神秘的な薬草。"),
    "Arcane Droplet":   Cards(0, 8, 0, SkillsList[2], "魔力が凝縮された神秘の雫。"),
    "Mystic Crystal":   Cards(0, 10, 0, SkillsList[2], "魔法の結晶がMPを回復してくれる。"),
    "Mana Elixir":      Cards(0, 3, 0, SkillsList[2], "飲むと魔力が瞬時に回復するエリクサー。"),
    "Celestial Fruit":  Cards(0, 5, 0, SkillsList[2], "天界の力を秘めた果実。"),
    "Sorcerer’s Tear":  Cards(0, 8, 0, SkillsList[2], "魔法使いの涙。魔力を取り戻す奇跡の雫。"),
    "Enchanted Honey":  Cards(0, 10, 0, SkillsList[2], "魔法のエネルギーを秘めた特別な蜂蜜。"),
    "Mana Gem":         Cards(0, 15, 0, SkillsList[2], "持つだけで魔力が回復する宝石。"),
    "Mystic Bread":     Cards(0, 15, 0, SkillsList[2], "食べると魔力が回復する特製のパン。")
}