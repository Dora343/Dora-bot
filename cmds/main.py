from types import prepare_class
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from core.classes import Cog_Extension
import typing as t
import json
import math
import random
import secrets
import re


class Main(Cog_Extension):

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('**Pong!**')
        await ctx.send(F'**網絡延遲: {round(self.bot.latency*1000)} ms**')

    @commands.command()
    async def roll(self, ctx, msg: t.Optional[str]):    

        if msg:
            temp = msg.split("-")
            # await ctx.send(str(temp))
            if len(temp) > 2:
                await ctx.send('無效的範圍')
            else:
                # await ctx.send('Valid range.')

                for i in range(len(temp)):
                    for j in range(len(temp[i])):
                        if not temp[i][j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                            return await ctx.send('無效的範圍')

                if len(temp) == 1:
                    temp = list(map(int, temp))
                    if temp[0] in [0, 1]:
                        await ctx.send('無效的範圍')
                    else:
                        await ctx.send(F'**{ctx.author.name}** rolls **{random.randrange(1,temp[0])}** (1-{temp[0]})')
                else:
                    temp = list(map(int, temp))
                    await ctx.send(F'**{ctx.author.name}** rolls **{random.randrange(temp[0],temp[1])}** ({temp[0]}-{temp[1]})')

        else:
            await ctx.send(F'**{ctx.author.name}** rolls **{random.randrange(1,100)}** (1-100)')

    @commands.command()
    async def extra(self, ctx, dmg, hp):
        remain = math.ceil(90-90*int(hp)/int(dmg)+20)
        if remain > 90:
            remain = 90
        await ctx.send(f'**補償秒數：{remain}秒**')

    @commands.command()
    async def wash(self, ctx):
        if ctx.author.guild_permissions.administrator:
            msg = '.'
            for i in range(1998):
                msg = msg + '\n'
            msg = msg + '.'
            await ctx.send(msg)
        else:
            await ctx.send('你沒有足夠權限使用此指令')

    @commands.command()
    async def go(self, ctx, top: t.Optional[str]):
        data = 12345
        data = f'{float(f"{data:.1g}"):g}'
        
        await ctx.send(data)

    @commands.command()
    async def shift(self, ctx, second, *, msg):

        # 計算剩餘秒數
        n = int(second)
        if n >= 100:
            n -= 40
        n = 90 - n

        nodigit = []
        # 把整段文字分行拆開
        m = re.split('\n', msg)
        content = []
        for i in range(len(m)):

            # 移除冒號
            m[i] = m[i].replace(':', '', 1)

            # 偵測字串內的數字
            flag1 = False
            flag2 = False
            ind = [0]

            for j in range(len(m[i])):
                if not flag1:
                    if m[i][j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        flag1 = True
                        ind.append(j)
                else:
                    if (not flag2) and (not m[i][j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                        flag2 = True
                        ind.append(j)

            ind.append(len(m[i]))

            # 分拆字串中第一組數字
            content.append([])
            for k in range(len(ind)-1):
                content[i].append(m[i][ind[k]:ind[k+1]])

            # 偵測無數字的字串
            if len(content[i]) == 1:
                nodigit.append(i)

        # 排除無數字的字串
        copy = []
        for i in range(len(content)):
            if i in nodigit:
                continue
            else:
                copy.append(content[i])

        # 提取所有指定數字
        time = []
        for i in range(len(copy)):
            time.append(int(copy[i][1]))

        # 補償秒數計算
        num = []
        for x in time:
            if x >= 100:
                x-=40
                x -= n
                if x < 100 and x > 60:
                    x += 40
            else:
                x -= n
                if x >= 60:
                    x += 40
            num.append(x)

        # 把數字及字串重組成一組文字
        result = '```glsl\n'
        for i in range(len(copy)):
            if i in nodigit:
                y = content[i][0] + '\n'
                result = result + y

            y = copy[i][0] + str(num[i]) + copy[i][2] + '\n'
            result = result + y
        result = result + '```'
        await ctx.send(result)

    @commands.command(name='pu',aliases=['p','u','o'])
    async def draw_pool(self, ctx):
        
        three_star = 0.03
        two_star = 0.18
        one_star = 1-two_star-three_star
        
        pool_up = 0.007

        if ctx.message.content == '.p':
        
            three_star = 0.06
            two_star = 0.18
            one_star = 1-two_star-three_star
            
            pool_up = 0.014

        if ctx.message.content == '.o':
            
            three_star = 0.03
            two_star = 0.18
            one_star = 1-two_star-three_star
            
            pool_up = 0.004
                
        one_star_amount = 0
        two_star_amount = 0
        three_star_amount = 0

        check = False
        result = []
        stone = 0
        amount = 0
        #msg = ''
        
        for i in range(200):
            temp = random.randrange(1, 1000)
            if i % 10 == 0 and i != 0:
                result.append(2)
                if temp <= three_star*1000:
                    result[i] = 3
                if temp <= pool_up*1000:
                    result[i] = 4
                    amount = i + 1
                    break
            else:
                result.append(1)
                if temp <= two_star*1000:
                    result[i] = 2
                if temp <= three_star*1000:
                    result[i] = 3
                if temp <= pool_up*1000:
                    result[i] = 4
                    amount = i + 1
                    break
                if i == 199:
                    check = True
                    amount = i + 1
        
        for i in range(amount):
                if result[i] == 1:
                    stone += 1
                    one_star_amount += 1
                if result[i] == 2:
                    stone += 10
                    two_star_amount += 1
                if result[i] == 3:
                    stone += 50
                    three_star_amount += 1
                if result[i] == 4:
                    stone += 50
                    three_star_amount += 1

        if check:
            
            msg = '**'+ctx.author.name + '** 花了**'+str(amount)+'**抽保底了<:QQ:841720948481851433><:QQ:841720948481851433><:QQ:841720948481851433>\n\n' 
            
        else:
            msg = '**'+ctx.author.name + '** 花了**' + \
                str(amount) + f'**抽才抽到** PICKUP ({round(100*pool_up,2)}%)**\n\n'
           

        msg = msg + '<:card_rainbow:840146360874696705>' + \
                str(three_star_amount) + '個，其中有' + str(1) + \
                '個' + '<:card_up:840146439778205741>\n'

        msg = msg + '<:card_gold:840146246295617578>' + \
            str(two_star_amount) + '個\n'

        msg = msg + '<:card_silver:840146174459772948>' + \
            str(one_star_amount) + '個\n\n'

        msg = msg + '總計抽到了**' + str(stone) + '**個女神石'
    
        if ctx.message.content=='.p':
                msg = '*[PICKUP 1.4%]*\n' + msg

        if ctx.message.content=='.o':
                msg = '*[PICKUP 0.4%]*\n' + msg

        '''
        if ctx.message.content=='.u':
                msg = '*[PICKUP 0.7%]*\n' + msg
        '''
        
        await ctx.send(msg)

        #await ctx.send(ctx.message.content)

    @commands.command(name="draw", aliases=["d", "D"])
    async def draw_card(self, ctx, number: t.Optional[str]):
        digit_emoji = ['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
        three_star = 0.03
        two_star = 0.18
        one_star = 1-two_star-three_star

        pool_up = 0.007

        if not number:
            ray = []
            result = []
            msg = ''
            stone = 0
            for i in range(9):
                ray.append(secrets.randbelow(1000)+1)
                result.append(1)
                if ray[i] <= 1000-one_star*1000:
                    result[i] = 2
                if ray[i] <= 1000-one_star*1000-two_star*1000:
                    result[i] = 3
                if ray[i] <= pool_up*1000:
                    result[i] = 4

            ray.append(secrets.randbelow(1000)+1)
            result.append(2)
            if ray[9] <= 1000-one_star*1000-two_star*1000:
                result[9] = 3
            if ray[9] <= pool_up*1000:
                result[9] = 4

            doramsg = ''

            for i in range(10):
                if result[i] == 1:
                    stone += 1
                    msg = msg + '<:card_silver:840146174459772948>'
                if result[i] == 2:
                    stone += 10
                    msg = msg + '<:card_gold:840146246295617578>'
                if result[i] == 3:
                    stone += 50
                    msg = msg + '<:card_rainbow:840146360874696705>'
                if result[i] == 4:
                    stone += 50
                    msg = msg + '<:card_up:840146439778205741>'


                if i == 4:
                    msg = msg + '\n\n'

            stone = str(stone)
            stone_msg = '<:plus:841710694679838730>'
            for i in range(len(stone)):
                stone_msg = stone_msg + digit_emoji[int(stone[i])]
            stone_msg = stone_msg + '<:stone:841707955543212123>\n\n'

            msg = stone_msg + msg  
            await ctx.send(msg)

        else:
            for i in range(len(number)):
                if not number[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return await ctx.send('無效的輸入數值')
            number = int(number)
            if number <= 0:
                return await ctx.send('無效的輸入數值')
            if number > 100000 and ctx.author.id != 400941378395439104:
                return await ctx.send('為什麼要欺負我<:rushia_cry:840144461870923777> <:rushia_cry:840144461870923777> <:rushia_cry:840144461870923777>')
            tens = math.floor(number/10)
            # await ctx.send(tens)
            number -= tens

            ray = []
            result = []

            one_star_amount = 0
            two_star_amount = 0
            three_star_amount = 0
            pu_amount = math.floor((tens+number)/200)
            # await ctx.send(pu_amount)

            stone = 0
            for i in range(number):
                ray.append(secrets.randbelow(1000)+1)
                result.append(1)
                if ray[i] <= 1000-one_star*1000:
                    result[i] = 2
                if ray[i] <= 1000-one_star*1000-two_star*1000:
                    result[i] = 3
                if ray[i] <= pool_up*1000:
                    result[i] = 4

            for i in range(tens):
                ray.append(secrets.randbelow(1000)+1)
                result.append(2)
                if ray[i+number] <= 1000-one_star*1000-two_star*1000:
                    result[i+number] = 3
                if ray[i+number] <= pool_up*1000:
                    result[i+number] = 4

            for i in range(tens+number):
                if result[i] == 1:
                    stone += 1
                    one_star_amount += 1
                if result[i] == 2:
                    stone += 10
                    two_star_amount += 1
                if result[i] == 3:
                    stone += 50
                    three_star_amount += 1
                if result[i] == 4:
                    stone += 50
                    pu_amount += 1

            three_star_amount += pu_amount
            # await ctx.send(str(ray))

            msg = '**'+ctx.author.name + '** 抽了**' + \
                str(number+tens) + '**抽\n\n'
            msg = msg + '<:card_rainbow:840146360874696705>' + \
                str(three_star_amount) + '個，其中有' + str(pu_amount) + \
                '個' + '<:card_up:840146439778205741>\n'
            msg = msg + '<:card_gold:840146246295617578>' + \
                str(two_star_amount) + '個\n'
            msg = msg + '<:card_silver:840146174459772948>' + \
                str(one_star_amount) + '個\n\n'

            msg = msg + '總計抽到了**' + str(stone) + '**個女神石\n'

            await ctx.send(msg)

    @commands.command(name="drawspecial", aliases=["ds", "DS"])
    async def draw_special_card(self, ctx, number: t.Optional[str]):
        prize_emoji = ['<:1_:845872250167361566>','<:2_:845872264493793281>','<:3_:845872276901855282>','<:4_:845872290075639849>','<:5_:845872311210475521>','<:6_:845872328999174164>']
        first_prize=5
        second_prize=10
        third_prize=50
        fourth_prize=100
        fifth_prize=235
        sixth_prize=600

        if not number:
            ray = []
            result = []
            msg = ''
            

            for i in range(9):
                ray.append(secrets.randbelow(1000)+1)
                result.append(6)
                if ray[i] <= 1000-sixth_prize:
                    result[i] = 5
                if ray[i] <= 1000-sixth_prize-fifth_prize:
                    result[i] = 4
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize:
                    result[i] = 3
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize:
                    result[i] = 2
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize-second_prize:
                    result[i] = 1

            ray.append(secrets.randbelow(1000)+1)
            result.append(5)
            if ray[9] <= 1000-sixth_prize-fifth_prize:
                result[9] = 4
            if ray[9] <= 1000-sixth_prize-fifth_prize-fourth_prize:
                result[9] = 3
            if ray[9] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize:
                result[9] = 2
            if ray[9] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize-second_prize:
                result[9] = 1


            for i in range(10):
                if result[i] == 1:
                    msg = msg + prize_emoji[0]
                if result[i] == 2:
                    msg = msg + prize_emoji[1]
                if result[i] == 3:
                    msg = msg + prize_emoji[2]
                if result[i] == 4:
                    msg = msg + prize_emoji[3]
                if result[i] == 5:
                    msg = msg + prize_emoji[4]
                if result[i] == 6:
                    msg = msg + prize_emoji[5]


                if i == 4:
                    msg = msg + '\n\n'

            await ctx.send(msg)
        
        else:
            for i in range(len(number)):
                if not number[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return await ctx.send('無效的輸入數值')
            number = int(number)
            if number <= 0:
                return await ctx.send('無效的輸入數值')
            if number > 100000 and ctx.author.id != 400941378395439104:
                return await ctx.send('為什麼要欺負我<:rushia_cry:840144461870923777> <:rushia_cry:840144461870923777> <:rushia_cry:840144461870923777>')
            tens = math.floor(number/10)
            # await ctx.send(tens)
            number -= tens

            ray = []
            result = []

            first_amount=0
            second_amount=0
            third_amount=0
            fourth_amount=0
            fifth_amount=0
            sixth_amount=0

            shard_amount=0
            heart_amount=0
            stone_amount=0

            tess=''
            for i in range(number):
                ray.append(secrets.randbelow(1000)+1)
                tess+=str(ray[i]) + ' '

                result.append(6)
                if ray[i] <= 1000-sixth_prize:
                    result[i] = 5
                if ray[i] <= 1000-sixth_prize-fifth_prize:
                    result[i] = 4
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize:
                    result[i] = 3
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize:
                    result[i] = 2
                if ray[i] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize-second_prize:
                    result[i] = 1

            for i in range(tens):
                ray.append(secrets.randbelow(1000)+1)
                tess+=str(ray[i]) + ' '
                result.append(5)
                if ray[i+number] <= 1000-sixth_prize-fifth_prize:
                    result[i+number] = 4
                if ray[i+number] <= 1000-sixth_prize-fifth_prize-fourth_prize:
                    result[i+number] = 3
                if ray[i+number] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize:
                    result[i+number] = 2
                if ray[i+number] <= 1000-sixth_prize-fifth_prize-fourth_prize-third_prize-second_prize:
                    result[i+number] = 1

            for i in range(tens+number):
                if result[i] == 1:
                    first_amount += 1
                    shard_amount+=40
                    stone_amount+=5
                    heart_amount+=5

                if result[i] == 2:
                    second_amount += 1
                    shard_amount+=20
                    stone_amount+=5
                    heart_amount+=3

                if result[i] == 3:
                    third_amount += 1
                    shard_amount+=5
                    stone_amount+=1
                    heart_amount+=3

                if result[i] == 4:
                    fourth_amount += 1
                    shard_amount+=1
                    stone_amount+=1
                    heart_amount+=2

                if result[i] == 5:
                    fifth_amount += 1
                    stone_amount+=1
                    heart_amount+=1

                if result[i] == 6:
                    sixth_amount += 1
                    stone_amount+=1


            msg = '**'+ctx.author.name + '** 抽了**' + \
                str(number+tens) + f'**抽\n總計抽到了\n**{str(shard_amount)}**個記憶碎片\n**{str(heart_amount)}**個公主之心碎片\n**{str(stone_amount)}**個女神石\n'
            msg = msg + prize_emoji[0] + \
                str(first_amount) + '個\n'
            msg = msg + prize_emoji[1] + \
                str(second_amount) + '個\n'
            msg = msg + prize_emoji[2] + \
                str(third_amount) + '個\n'
            msg = msg + prize_emoji[3] + \
                str(fourth_amount) + '個\n'
            msg = msg + prize_emoji[4] + \
                str(fifth_amount) + '個\n'
            msg = msg + prize_emoji[5] + \
                str(sixth_amount) + '個'

            await ctx.send(msg)
            #await ctx.send(tess)


def setup(bot):
    bot.add_cog(Main(bot))
