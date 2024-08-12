### 作者电报 @MaYiAdm 
### 交流群组 蚂蚁🐜俱乐部 @MaYi_Club
### 不会搭建 可以找作者 进行指导❕
//开始
import time , io , os ,string
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,ReplyKeyboardMarkup,ReplyKeyboardRemove,ChatShared,KeyboardButton,ChatPermissions
from telegram.ext import (Application,CallbackQueryHandler,CommandHandler,ContextTypes,filters,InvalidCallbackData,MessageHandler,PicklePersistence,ConversationHandler)
import time , io , os ,string
import random
from pathlib import Path
iimport time , io , os ,string
client = MongoClient //Mongodb数据库URL

bot_token = "1234567890" #机器人令牌

support = " @MaYiAdm"//客服用户名
bot_username = "MaYi888bot"//机器人用户名
owners = [12345678]//管理员UID
channel = "MaYi888bot"//机器人用户名

report  = 123456

usdt_address = "1234567890"//USDT收款地址


main_keyboard = [["🏠我的账户","🛍️商品列表"],["❓联系客服","💳充值余额"]]//机器人按钮中文

en_keyboard = [["👓User Center","🛒Product List"],["💳Recharge"],["📞Contact Service","🌐Switch Language"]]//机器人按钮英文


client = MongoClient("1234567890")//Mongodb数据库URL
main_db = "123456" //Mongodb数据库名字

helper = 'https://t.me/MaYiAdm'//客服用户名

last_record = {}
add_record = {}

dbm = client[db]//Mongodb数据库表
users = dbm['us']//Mongodb数据库表
settings = dbm['set']//Mongodb数据库表
products = dbm['pro']//Mongodb数据库表
payments = dbm['pay']//Mongodb数据库表
items = dbm['items']//Mongodb数据库表


if settings.count_documents({}) < 1:
    data = {"is_main" : True ,"base_time" : None}
    settings.insert_one(data)

def install_db():
    my_database = client[main_db]

    collections = ["us", "set", "pro" , "pay" , "items"]
    for i in collections:
        sample_document = {"key": "value"}

        my_collection = my_database[i]

        my_collection.insert_one(sample_document)

        result = my_collection.delete_one(sample_document)

install_db()

SELECT_MENU, BUY, BUY_FINAL, SET_RATE, GET_SELECT, ADD_ADDRESS2 ,ADD_ADDRESS3, ADD_ADDRESS4, REMOVE,ADMIN1,ADMIN2,\
    ADMIN3,ADMIN4,AUTO_REPLY3,AUTO_DEL1,AUTO_DEL2,AUTO_DEL3,SPAM,AUTO_TIME1,AUTO_TIME2,AUTO_TIME3= range(
    21)


def get_user(uid : int):
    res = users.find_one({"userid" : uid})
    if res != None:
        return res
    else:
        return None






def china_time(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    chinese_date_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    return chinese_date_time





def is_trc20_address(address):
    trc20_pattern = r'^T[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{33}$'
    return re.match(trc20_pattern, address) is not None


def check_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    while True:
        actives = db.execute("SELECT * FROM incheck_pay WHERE status=?",["ACTIVE"]).fetchall()
        if len(actives) > 0:
            try:
                for i in actives:
                    if (time.time() - float(i[3])) > 1800:
                        db.execute(f"UPDATE incheck_pay SET status=? WHERE amount=? AND create_time=?",
                                   ["EXPIRED",i[2],i[3]])

            except Exception as e:
                print("Err ",e)
                continue
        else:
            time.sleep(5)
            continue


async def check_input_usdt(context = ContextTypes.DEFAULT_TYPE):
    print("checker is on - 1")
    while True:
        #print("checker is on1")

        base_time = settings.find_one({"is_main" : True})
        base_time = base_time["base_time"]

        if base_time == None:
            base_time = round(time.time()) * 1000



        #check usdt input
        url = requests.get(
            f"1234567890")//TRC20的api调用

        if len(url.json()['data']) > 0:
            for i in url.json()['data']:

                if i['transferToAddress'] == usdt_address:
                    pass
                else:
                    continue

                trc20_balance = float(i['amount']) / 1000000

                check = payments.find_one({"amount" : trc20_balance, "status": {"$in": [None]}})

                if check != None:
                    try:


                        await context.bot.send_message(chat_id=check['userid'],text=f"一笔比您价值 {trc20_balance}USDT 的交易正在处理中")
                    except Exception as e:
                        print(e)

                    payments.update_one({"userid": int(check['userid']),"amount": trc20_balance},
                                       {"$set": {"status": 1, "paid_time": i['timestamp'], 'tx_hash': i['transactionHash']}})

        settings.update_one({"is_main" : True},{"$set": {"base_time": round(time.time() - 700) * 1000}})

        await asyncio.sleep(1)







headers = {"Content-Type": "application/json"}
async def check_confirms(context : ContextTypes.DEFAULT_TYPE):
    while True:
        await asyncio.sleep(0.1)
        check = list(payments.find({"status": 1}))

        if len(check) < 1:
            continue
        await asyncio.sleep(0.5)
        for i in check:
            await asyncio.sleep(0.5)
            try:

                print(i['tx_hash'])
                response = requests.get(
                    f"https://apilist.tronscan.org/api/transaction-info?hash={i['tx_hash']}",
                    headers=headers, timeout=100)

                if response.json()["confirmed"] == True:

                    payments.update_one({"userid" : i["userid"],'amount' : i['amount']},{"$set": {"status": 2}})

                    # add balance
                    search = users.find_one({"userid" : int(i["userid"])})

                    old_usdt = round(search["balance"], 4)
                    new_usdt = old_usdt + i['amount']
                    users.update_one({"userid": i["userid"]}, {"$set": {"balance": new_usdt}})


                    text = f"""✅ 增加库存
您的账户已被扣费 {i['amount']}U"""

                    try:


                        await context.bot.send_message(chat_id=i["userid"],
                                                       text=text)
                    except:
                        pass

                    try:
                        await context.bot.send_message(chat_id=report,
                                                       text=f"""⭕️收到了一份传单

🟢来自用户：<a href="tg://user?id={i["userid"]}">{i["userid"]}</a>
🔸收到金额：<code>{i['amount']}U</code>

➕哈希：<code>{i['tx_hash']}</code>""",parse_mode=ParseMode.HTML)
                    except:
                        pass


            except Exception as e:
                print("error in conf checker:",e)

        await asyncio.sleep(5)




async def expire_check(context : ContextTypes.DEFAULT_TYPE):
    while True:
        await asyncio.sleep(5)
        check = list(payments.find({"status": None}))
        if len(check) > 0:
            for i in check:
                if (time.time() - i['expire']) > 1800:
                    payments.delete_one({'amount' : i['amount']})
                    try:
                        await context.bot.send_message(chat_id=i['userid'], text = "<b>❌ 订单支付超时(或金额错误)</b>",parse_mode=ParseMode.HTML)
                    except:
                        pass




def loop1(update,context):
    asyncio.run(check_confirms(context))

def loop2(update,context):
    asyncio.run(check_input_usdt(context))
def loop3(update,context):
    asyncio.run(expire_check(context))



checker = [0]




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userid = update.message.from_user.id

    if checker[0] == 0:
        checker[0] = True
        threading.Thread(target=loop1, args=(update, context)).start()
        threading.Thread(target=loop2, args=(update, context)).start()
        threading.Thread(target=loop3, args=(update, context)).start()

    if update.message.chat.type != "private":
        return

    if not get_user(userid):
        data = {"userid" : userid,"name" : update.message.from_user.first_name[0:10] , 'total_buy' : 0, "balance" : 0, "used_balance" : 0,"lang" : 'zh',"register_time" : round(time.time())}
        users.insert_one(data)
    name = update.message.from_user.first_name


    user = get_user(userid)

    if user['lang'] == "zh":

        //欢迎信息 处理/start命令 中文
        await update.message.reply_text(f"""<b>这里是欢迎信息
        
☎️ 客服： @MaYiAdm 
🏦 频道： @MaYiBaiHuo

⚙️ /start   ⬅️点击命令打开底部菜单!
</b>""",parse_mode=ParseMode.HTML,disable_web_page_preview=True,
                              reply_markup=ReplyKeyboardMarkup(main_keyboard,
                                                               resize_keyboard=True))
      
       //欢迎信息 处理/start命令 英文
    else:
        await update.message.reply_text(f"""<b>欢迎信息

☎️Customer service:
🔊 Channel: @{channel}


⚙️ /start ⬅️Click the command to open the bottom menu‼️ 
        </b>""", parse_mode=ParseMode.HTML, disable_web_page_preview=True,
                                        reply_markup=ReplyKeyboardMarkup(en_keyboard,
                                                                         resize_keyboard=True))
    return SELECT_MENU



def get_count(path , file = None):
    contents = os.listdir(path)



    folders = [name for name in contents if os.path.isdir(os.path.join(path, name))]



    num_folders = len(folders)
    return num_folders


def get_files(path, all = False):

    if all == False:

        contents = os.listdir(path)

        session_files = [name for name in contents if
                         name.endswith('.session') and os.path.isfile(f"{path}/{name}")]

        if session_files:
            # اگر فایل‌های .session وجود دارند، تعداد آنها را برگردانید
            return len(session_files)
        else:
            # اگر فایل‌های .session وجود ندارند، تعداد فولدرها را برگردانید
            folders = [name for name in contents if os.path.isdir(f"{path}/{name}")]
            return len(folders)

        #folders = [name for name in contents if os.path.isdir(os.path.join(path, name))]

        #num_folders = len(folders)
        #return num_folders
    else:
        base_path = path

        try:
            contents = os.listdir(base_path)
        except FileNotFoundError:
            print(f"The directory {base_path} does not exist.")
            return 0

        folders = [name for name in contents if os.path.isdir(f"{base_path}/{name}")]

        full = 0

        for folder in folders:
            current_path = f"{base_path}/{folder}"
            #print(f"Current path: {current_path}")

            try:
                contents = os.listdir(current_path)
            except FileNotFoundError:
                print(f"The directory {current_path} does not exist.")
                continue

            session_files = [name for name in contents if
                             name.endswith('.session') and os.path.isfile(f"{current_path}/{name}")]
            #print(f"Session files in {current_path}: {len(session_files)}")

            if session_files:
                full += len(session_files)
            else:
                subfolders = [name for name in contents if os.path.isdir(f"{current_path}/{name}")]
                full += len(subfolders)

        return full

            # folders = [name for name in contents if os.path.isdir(os.path.join(path, name))]
            #
            # num_folders = len(folders)
            # return num_folders






userbuy = {}


async def buyacc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.message.from_user.id

    user = get_user(uid)

    if text.startswith("购买"):
        numb = text.split(" ")[1].strip()
    else:
         numb = text
    try:
        numb = int(numb)
    except:
        return BUY

    if userbuy.get(uid):
        suds = userbuy[uid]



        idems = items.find_one({"tid" : suds})



        dddd = products.find_one({"pid": idems['from_pid']})

        total = get_files(f"{dddd['ch']}/{idems['ch']}", all=False)


        if numb > total:

            if user['lang'] == "zh":

                await update.message.reply_text(f"""<b>❌库存不足，请重新选择数量！当前库存为：{total}</b>""",parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text(f"""<b>❌Out of stock, please select another quantity! Current inventory is: {total}</b>""", parse_mode=ParseMode.HTML)

            return BUY

        full_cost = numb * idems['price']

        print(full_cost)
        if full_cost > user['balance']:
            if user['lang'] == "zh":

                await update.message.reply_text(f"""<b>❌余额不足，请及时充值！</b>""",parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text(f"""<b>❌The balance is insufficient, please recharge in time!</b>""", parse_mode=ParseMode.HTML)

            return BUY
        else:
            if user['lang'] == 'zh':

                inline = [[InlineKeyboardButton("❌取消购买", callback_data="backpu"),InlineKeyboardButton("✅购买确认", callback_data=f"acc_{suds}_{numb}")],
                      [InlineKeyboardButton("↩️主菜单", callback_data="backpu")]]
                await update.message.reply_text(f"""✅您正在购买:  {idems['ch']}
            
✅数字：{numb}

💰 价格： {idems['price']} USDT

✅总价：{round(full_cost,3)} USDT
            """,reply_markup=InlineKeyboardMarkup(inline),parse_mode=ParseMode.HTML)
            else:
                inline = [[InlineKeyboardButton("❌Cancel", callback_data="backpu"),InlineKeyboardButton("✅Accept", callback_data=f"acc_{suds}_{numb}")],
                      [InlineKeyboardButton("↩️Back menu", callback_data="backpu")]]
                await update.message.reply_text(f"""✅You are buying: {idems['ch']}
            
✅Count: {numb}

💰 Price: {idems['price']} USDT

✅Total price: {round(full_cost,3)} USDT
            """,reply_markup=InlineKeyboardMarkup(inline),parse_mode=ParseMode.HTML)

            return BUY_FINAL





    else:
        await update.message.reply_text("错误稍后重试", reply_markup=ReplyKeyboardMarkup(admin_keybaord,
                                                                                  resize_keyboard=True))

        return SELECT_MENU





def check_files(path):


    contents = os.listdir(path)


    session_files = [name for name in contents if
                     name.endswith('.session') and os.path.isfile(os.path.join(path, name))]

    if session_files:
        # اگر فایل‌های .session وجود دارند، تعداد آنها را برگردانید
        return {"session" : len(session_files)}
    else:
        # اگر فایل‌های .session وجود ندارند، تعداد فولدرها را برگردانید
        folders = [name for name in contents if os.path.isdir(os.path.join(path, name))]
        return {"tdata" : len(folders)}





def zip_file(path , format , zipname , count):

    if format == "session":
        session_files = glob.glob(os.path.join(path, '*.session'))
        json_files = glob.glob(os.path.join(path, '*.json'))

        selected_files = random.sample(session_files, count)
        selected_files += [file for file in json_files if
                           Path(file).stem in [Path(session).stem for session in selected_files]]

        with zipfile.ZipFile(f"sold/{zipname}", 'w') as zipf:
            for file in selected_files:
                zipf.write(file, os.path.basename(file))

        for i in selected_files:
            os.remove(i)


        return True
    elif format == "tdata":
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

        # Select 10 random folders
        selected_folders = random.sample(folders, count)
        print(selected_folders)

        # Create a zip file and add the selected folders
        with zipfile.ZipFile(os.path.join('sold', zipname), 'w') as zipf:
            for folder in selected_folders:
                folder_path = os.path.join(path, folder)
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, path))

        # Delete the selected folders
        for folder in selected_folders:
            folder_path = os.path.join(path, folder)
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(folder_path)
        return True

async def final_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id



    tid = query.data.split("_")[1]
    count = query.data.split("_")[2]
    count = int(count)
    user = get_user(uid)
    utem = items.find_one({"tid" : tid})

    if user['balance'] >= utem['price'] * count:
        dddd = products.find_one({"pid": utem['from_pid']})
        total : dict = check_files(f"{dddd['ch']}/{utem['ch']}")
        if total.get('session'):
            zname = f"{round(time.time())}_{uid}.zip"

            tryzip = zip_file(f"{dddd['ch']}/{utem['ch']}" , 'session',zname , count)
            if tryzip:
                new_balance = user['balance'] - utem['price'] * count
                new_used = user["used_balance"] + utem['price'] * count
                new_total = user['total_buy'] + count

                users.update_one({"userid" : uid} , {"$set" : {"balance" : new_balance , "used_balance" : new_used, 'total_buy' : new_total}})

                try:
                    await context.bot.send_message(chat_id=report,
                                                   text=f"""✅购买成功报告✅
🛍购物自：{utem['ch']}
🆔来自用户：<a href="tg://user?id={uid}">{uid}</a>
🔢购买数量：<code>{count}</code>
💠每件价格: {utem['price']}
✳️总价：{round(utem['price'] * count,3)}U""", parse_mode=ParseMode.HTML)
                except:
                    pass

                if user['lang'] == "en":

                    await query.edit_message_text("✅The purchase was made successfully")
                    await context.bot.send_document(chat_id=uid , document=open(f"sold/{zname}", 'rb'))
                    return SELECT_MENU
                else:
                    await query.edit_message_text("✅购买成功")
                    await context.bot.send_document(chat_id=uid, document=open(f"sold/{zname}", 'rb'))
                    return SELECT_MENU





        elif total.get("tdata"):
            zname = f"{round(time.time())}_{uid}.zip"

            tryzip = zip_file(f"{dddd['ch']}/{utem['ch']}", 'tdata', zname, count)
            if tryzip:
                new_balance = user['balance'] - utem['price'] * count
                new_used = user["used_balance"] + utem['price'] * count
                new_total = user['total_buy'] + count

                users.update_one({"userid": uid},
                                 {"$set": {"balance": new_balance, "used_balance": new_used, 'total_buy': new_total}})

                if user['lang'] == "en":

                    await query.edit_message_text("✅The purchase was made successfully")
                    await context.bot.send_document(chat_id=uid, document=open(f"sold/{zname}", 'rb'))
                    return SELECT_MENU
                else:
                    await query.edit_message_text("✅购买成功")
                    await context.bot.send_document(chat_id=uid, document=open(f"sold/{zname}", 'rb'))
                    return SELECT_MENU

        else:
            if user['lang'] == "en":

                await query.edit_message_text("try again later")
                await context.bot.send_document(chat_id=uid, document=open(f"sold/{zname}", 'rb'))
                return SELECT_MENU
            else:
                await query.edit_message_text("稍后再试")
                await context.bot.send_document(chat_id=uid, document=open(f"sold/{zname}", 'rb'))
                return SELECT_MENU


    else:
        if user['lang'] == "zh":
            inline = [[InlineKeyboardButton("↩️主菜单", callback_data="backpu")]]
            await query.edit_message_text("你的库存不足。",reply_markup=InlineKeyboardMarkup(inline))
        else:
            inline = [[InlineKeyboardButton("↩️Return", callback_data="backpu")]]
            await query.edit_message_text("Your inventory is insufficient.", reply_markup=InlineKeyboardMarkup(inline))

        return SELECT_MENU



async def makepay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.message.from_user.id
    user = get_user(uid)

    try:
        count = int(text)
    except:
        if user['lang'] == 'zh':
            await update.message.reply_text("号码不正确。输入正确的数字：")
        else:
            await update.message.reply_text("Incorrect number . Enter the correct number:")
        return GET_SELECT

    if count > 0 and count <= 10000:
        data = count

        while True:
            random_number = round(random.uniform(0.0001, 0.0999), 4)
            amount = data + random_number

            check = payments.find_one({"amount": amount})

            if check == None:
                now_time = round(time.time())
                expires_in = round(time.time()) + 1800

                payments.insert_one(
                    {"amount": amount, "userid": uid, "expire": expires_in, "status": None})

                break
            else:
                continue

        if user['lang'] == 'zh':
            await update.message.reply_text(f"""<b>充值详情

实际支付金额：<code>{amount}</code> USDT

收款地址：<code>{usdt_address}</code>

❗️❗️❗️❗️请一定按照金额后面小数点转账，否则未到账概不负责❗️❗️❗️❗️

创建时间：{china_time(now_time)}
结束时间：{china_time(expires_in)}

请在30分钟内支付完成，否则订单失效</b>
                    """, parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text(f"""<b>Recharge Details

Actual payment amount: <code>{amount}</code> USDT

Receiving Address: <code>{usdt_address}</code>

❗️❗️❗️❗️ Please make sure to transfer the exact amount including decimals, we will not be responsible for any discrepancies due to incorrect amounts ❗️❗️❗️❗️

Creation Time: {china_time(now_time)}
End Time: {china_time(expires_in)}

Please complete the payment within 30 minutes, otherwise the order will expire
</b>
                                    """, parse_mode=ParseMode.HTML)
        return SELECT_MENU
    else:
        if user['lang'] == 'zh':
            await update.message.reply_text("号码不正确。输入正确的数字：")
        else:
            await update.message.reply_text("Incorrect number . Enter the correct number:")
        return GET_SELECT











async def text_manage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.callback_query
        data = update.callback_query.data

        uid = query.from_user.id
        user = get_user(uid)

        if data == 'custom':
            #back = [[InlineKeyboardButton("",callback_data="backpay")]]
            if user['lang'] == 'zh':
                await query.edit_message_text("输入 1 到 10000 之间的所需值:")
            else:
                await query.edit_message_text("Enter the desired value between 1 and 10000:")

            return GET_SELECT

        elif data.startswith('usd'):
            data = int(data[3:])

            while True:
                random_number = round(random.uniform(0.0001, 0.0999), 4)
                amount =data + random_number



                check = payments.find_one({"amount" : amount})

                if check == None:
                    now_time = round(time.time())
                    expires_in = round(time.time()) + 1800

                    payments.insert_one({"amount" : amount , "userid" : query.from_user.id , "expire" : expires_in , "status" : None})

                    break
                else:
                    continue

            if user['lang'] == 'zh':
                await query.edit_message_text(f"""<b>充值详情

实际支付金额：<code>{amount}</code> USDT

收款地址：<code>{usdt_address}</code>

❗️❗️❗️❗️请一定按照金额后面小数点转账，否则未到账概不负责❗️❗️❗️❗️

创建时间：{china_time(now_time)}
结束时间：{china_time(expires_in)}

请在30分钟内支付完成，否则订单失效</b>
            """,parse_mode=ParseMode.HTML)
            else:
                await query.edit_message_text(f"""<b>Recharge Details

Actual payment amount: <code>{amount}</code> USDT

Receiving Address: <code>{usdt_address}</code>

❗️❗️❗️❗️ Please make sure to transfer the exact amount including decimals, we will not be responsible for any discrepancies due to incorrect amounts ❗️❗️❗️❗️

Creation Time: {china_time(now_time)}
End Time: {china_time(expires_in)}

Please complete the payment within 30 minutes, otherwise the order will expire
</b>
                            """, parse_mode=ParseMode.HTML)
            return SELECT_MENU


        elif data == "cancel" or data == 'close':
            await update.callback_query.delete_message()
            return SELECT_MENU


        elif data.startswith('subpid'):
            pid = data[6:]
            idems = list(items.find({"from_pid": pid}))

            plist = [

            ]


            for i in idems:
                dddd = products.find_one({"pid": i['from_pid']})

                #total = get_count(f"{dddd['ch']}/{i['ch']}")

                total = get_files(f"{dddd['ch']}/{i['ch']}", all=False)


                if user['lang'] == "zh":

                    plist.append([InlineKeyboardButton(f'{i["ch"]}({total})', callback_data=f'utem{i["tid"]}')])
                else:
                    plist.append([InlineKeyboardButton(f'{i["en"]}({total})', callback_data=f'utem{i["tid"]}')])


            if user['lang'] == "zh":
                plist.append([InlineKeyboardButton('❌关闭', callback_data=f'close'),
                 InlineKeyboardButton('返回↩', callback_data=f'backpu')])
                await query.edit_message_text("您可以使用以下按钮删除、添加或更改产品类别:", reply_markup=InlineKeyboardMarkup(plist))
            else:
                plist.append([InlineKeyboardButton('❌close', callback_data=f'close'),
                              InlineKeyboardButton('return↩', callback_data=f'backpu')])
                await query.edit_message_text("You can delete, add or change product categories using the following buttons:", reply_markup=InlineKeyboardMarkup(plist))


            return SELECT_MENU


        elif data == "backpu":
            if user['lang'] == 'zh':
                inline_buttons = [

                ]

                pros = list(products.find({}))

                for i in pros:
                    total = get_files(i['ch'], all=True)

                    inline_buttons.append(
                        [InlineKeyboardButton(f"{i['ch']}({total})", callback_data=f'subpid{i["pid"]}')])

                inline_buttons.append([
                    InlineKeyboardButton("❌关闭", callback_data='cancel'),
                ])

                keyboard = InlineKeyboardMarkup(inline_buttons)

                await query.edit_message_text("""<b>🛒选择你需要的商品：
                        ❗️没使用过本店商品的，请先少量购买测试，以免造成不必要的争执！谢谢合作</b>""", reply_markup=keyboard, parse_mode=ParseMode.HTML)
                return SELECT_MENU
            else:
                inline_buttons = [

                ]

                pros = list(products.find({}))

                for i in pros:
                    total = get_files(i['ch'], all=True)
                    inline_buttons.append(
                        [InlineKeyboardButton(f"{i['en']}({total})", callback_data=f'subpid{i["pid"]}')])

                inline_buttons.append([
                    InlineKeyboardButton("❌close", callback_data='cancel'),
                ])

                keyboard = InlineKeyboardMarkup(inline_buttons)

                await query.edit_message_text("""<b>🛒 Choose the items you need:
❗️ If you have not used our products before, please make a small test purchase first to avoid unnecessary disputes! Thank you for your cooperation</b>""",
                                                reply_markup=keyboard, parse_mode=ParseMode.HTML)
                return SELECT_MENU




        elif data.startswith('utem'):


            tid = data[4:]
            idems = items.find_one({"tid": tid})

            dddd = products.find_one({"pid": idems['from_pid']})

            #total = get_count(f"{dddd['ch']}/{idems['ch']}")
            total = get_files(f"{dddd['ch']}/{idems['ch']}", all=False)







            if total <= 0:
                if user['lang'] == 'zh':
                    await query.answer("❌暂无服务请联系客服添加@{support}", show_alert=True)
                    return SELECT_MENU
                else:
                    await query.answer(f"❌no service available please contact customer service to add @{support}", show_alert=True)
                    return SELECT_MENU

            if user['lang'] == 'zh':
                inline = [[InlineKeyboardButton("✅购买", callback_data=f"buy{tid}"),InlineKeyboardButton("联系客服", url=helper)],
                          [InlineKeyboardButton("💒主菜单", callback_data=f"backpu"),InlineKeyboardButton("返回↩️", callback_data=f"subpid{idems['from_pid']}")]]

                await query.edit_message_text(f"""<b>✅您正在购买:  {idems['ch']}

💰 价格： {idems['price']} USDT

🏢 库存： {total}

❗️ 未使用过的本店商品的，请先少量购买测试，以免造成不必要的争执！谢谢合作！</b>""",reply_markup=InlineKeyboardMarkup(inline),parse_mode=ParseMode.HTML)
                return SELECT_MENU
            else:
                inline = [[InlineKeyboardButton("✅Buy", callback_data=f"buy{tid}"),
                           InlineKeyboardButton("customer support", url=helper)],
                          [InlineKeyboardButton("💒Main menu", callback_data=f"backpu"),
                           InlineKeyboardButton("Return↩️", callback_data=f"subpid{idems['from_pid']}")]]   

                await query.edit_message_text(f"""<b>✅ You are buying: {idems['en']}

💰 Price: {idems['price']} USDT

🏢 Stock: {total}

❗️ If you have not used our products before, please make a small test purchase first to avoid unnecessary disputes! Thank you for your cooperation!</b>""", reply_markup=InlineKeyboardMarkup(inline),parse_mode=ParseMode.HTML)

            return SELECT_MENU


        elif data.startswith('buy'):
            cuds = data[3:]

            if user['lang'] == "en":
                await context.bot.send_message(chat_id=uid, text= f"""Enter quantity:\nFormat: <code>Buy 10</code> Or <code>10</code>""",parse_mode=ParseMode.HTML)
            else:
                await context.bot.send_message(chat_id=uid, text= f"""请输入数量：格式：<code>购买 10</code> 或 <code>10</code>""",parse_mode=ParseMode.HTML)
            print(cuds)
            userbuy[uid] = cuds
            return BUY







        elif data == "instract":
           await context.bot.send_message(chat_id=uid,text=helper)
           return SELECT_MENU



    text = update.message.text
    uid = update.message.from_user.id

    user = get_user(uid)


//处理联系客服按钮 
    if text == "❓联系客服" or text == "📞Contact Service":
        if user['lang'] == "zh":


            await update.message.reply_text(f"""☎️ 客服: @MaYiAdm
🔉 频道 @MaYiBaiHuo

🌈新客户必读：
🌈未购买过本店商品的 请少量购    
     买测试 以免产成纠纷 谢谢合作‼️
            """,parse_mode=ParseMode.HTML,disable_web_page_preview=True,
                              reply_markup=ReplyKeyboardMarkup(main_keyboard,
                                                               resize_keyboard=True))

        else:
            await update.message.reply_text(f"""☎️ Customer Service:8
☎️ Our Channe

🌈 New customers must read:
🌈 If you have not used our products before, please make a small test purchase first to avoid unnecessary disputes! Thank you for your cooperation!!!""", parse_mode=ParseMode.HTML, disable_web_page_preview=True,
                                            reply_markup=ReplyKeyboardMarkup(en_keyboard,
                                                                             resize_keyboard=True))
        return SELECT_MENU

//处理个人账户按钮
    elif text == "🏠我的账户" or text == '👓User Center':

        inline = [[InlineKeyboardButton(text="☎️联系客服", url=f"https://t.me/{support}")]]

        inline2 = [[InlineKeyboardButton(text="☎Contact Service", url=f"https://t.me/{support}")]]

        user = get_user(uid)

        if user['lang'] == "zh":


            await update.message.reply_text(f"""<b>您的ID:  {uid}
您的用户名:  <a href="http://t.me/{update.message.from_user.username}">{update.message.from_user.username or ''}</a>
注册日期:  {china_time(user["register_time"])}

总购数量:  {user["total_buy"]}

您的余额:  {user['balance']} USDT

总购金额: {user['used_balance']} USDT</b>
        """,reply_markup=InlineKeyboardMarkup(inline),parse_mode=ParseMode.HTML , disable_web_page_preview=True)
            return SELECT_MENU
        else:
            await update.message.reply_text(f"""<b>Your ID:  {uid}
        Your username:  <a href="http://t.me/{update.message.from_user.username}">{update.message.from_user.username or ''}</a>
Registration date:  {china_time(user["register_time"])}

Total purchase quantity:  {user["total_buy"]}

Your balance: {user['balance']} USDT

Total purchase amount:  {user['used_balance']} USDT</b>
                """, reply_markup=InlineKeyboardMarkup(inline2), parse_mode=ParseMode.HTML,
                                        disable_web_page_preview=True)
        return SELECT_MENU


//处理多语言切换
    elif text == "🌐语言切换" or text == "🌐Switch Language":

        if user['lang'] == 'zh':
            users.update_one({"userid" : uid}, {"$set" : {'lang' : 'en'}})
            await update.message.reply_text("Switch language successful",parse_mode=ParseMode.HTML,disable_web_page_preview=True,
                              reply_markup=ReplyKeyboardMarkup(en_keyboard,
                                                               resize_keyboard=True))
        else:
            users.update_one({"userid": uid}, {"$set": {'lang': 'zh'}})
            await update.message.reply_text("切换语言成功", parse_mode=ParseMode.HTML,
                                            disable_web_page_preview=True,
                                            reply_markup=ReplyKeyboardMarkup(main_keyboard,
                                                                             resize_keyboard=True))
        return SELECT_MENU


    elif text == "🛍️商品列表" or text == "🛒Product List":

        if user['lang'] == 'zh':
            inline_buttons = [

            ]

            pros = list(products.find({}))

            for i in pros:

                total = get_files(i['ch'],all=True)

                if total == None:
                    total = 0


                inline_buttons.append([InlineKeyboardButton(f"{i['ch']}({total})", callback_data=f'subpid{i["pid"]}')])

            inline_buttons.append([
                InlineKeyboardButton("❌关闭", callback_data='cancel'),
            ])

            keyboard = InlineKeyboardMarkup(inline_buttons)

            await update.message.reply_text("""<b>🛒选择你需要的商品：
            ❗️没使用过本店商品的，请先少量购买测试，以免造成不必要的争执！谢谢合作</b>""", reply_markup=keyboard, parse_mode=ParseMode.HTML)
            return SELECT_MENU
        else:
            inline_buttons = [

            ]

            pros = list(products.find({}))

            for i in pros:
                total = get_files(i['ch'], all=True)

                if total == None:
                    total = 0

                inline_buttons.append([InlineKeyboardButton(f"{i['en']}({total})", callback_data=f'subpid{i["pid"]}')])

            inline_buttons.append([
                InlineKeyboardButton("❌close", callback_data='cancel'),
            ])

            keyboard = InlineKeyboardMarkup(inline_buttons)

            await update.message.reply_text("""<b>🛒 Choose the items you need:
❗️ If you have not used our products before, please make a small test purchase first to avoid unnecessary disputes! Thank you for your cooperation</b>""", reply_markup=keyboard, parse_mode=ParseMode.HTML)
            return SELECT_MENU





//处理充值按钮
    elif text == "💳充值余额" or text == "💳Recharge":
        inline_buttons = [
            [
                InlineKeyboardButton("5U", callback_data="usd5"),
                InlineKeyboardButton("10U", callback_data='usd10'),
                InlineKeyboardButton("20U", callback_data='usd20'),],
            [
                InlineKeyboardButton("50U", callback_data="usd50"),
                InlineKeyboardButton("100U", callback_data="usd100"),
                InlineKeyboardButton("300U", callback_data="usd300"),

            ],
            [
                InlineKeyboardButton("500U", callback_data="usd500"),
                InlineKeyboardButton("1000U", callback_data="usd1000"),],

            [InlineKeyboardButton("自定义金额", callback_data="custom")],

            [
                InlineKeyboardButton("取消充值", callback_data="cancel"),

            ],
        ]

        inline_buttons2 = [
            [
                InlineKeyboardButton("5U", callback_data="usd5"),
                InlineKeyboardButton("10U", callback_data='usd10'),
                InlineKeyboardButton("20U", callback_data='usd20'), ],
            [
                InlineKeyboardButton("50U", callback_data="usd50"),
                InlineKeyboardButton("100U", callback_data="usd100"),
                InlineKeyboardButton("300U", callback_data="usd300"),

            ],
            [
                InlineKeyboardButton("500U", callback_data="usd500"),
                InlineKeyboardButton("1000U", callback_data="usd1000"), ],
            [InlineKeyboardButton("Custom Pay", callback_data="custom")],

            [
                InlineKeyboardButton("取消充值", callback_data="cancel"),

            ],
        ]


        keyboard = InlineKeyboardMarkup(inline_buttons)
        keyboard2 = InlineKeyboardMarkup(inline_buttons2)

        if user['lang'] == 'zh':

            await update.message.reply_text("""<b>💰请选择下面充值订单金额 

💹点击对应金额 请严格按照提示小数点转账‼️</b>""", reply_markup=keyboard, parse_mode=ParseMode.HTML)
            return SELECT_MENU
        else:

            await update.message.reply_text("""<b>💰 Please select the recharge order amount below

💹 Please transfer the exact amount‼️</b>""", reply_markup=keyboard2, parse_mode=ParseMode.HTML)
            return SELECT_MENU




def id_generator(size=7, chars=string.ascii_lowercase):
    return str(''.join(random.choice(chars) for _ in range(size)))



#
admin_keybaord = [["产品列表"],["通知所有人"],["后退"]] #"地位"

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id in owners:
        pass
    else:
        return SELECT_MENU

    await update.message.reply_text("你好管理员\n\n获取用户个人资料 <code>/info UID</code>\n增加或减少用户余额 : /bal UID +/-AMOUNT (例如 : <code>/bal 12343344 +40</code>)\n\n/status 查看用户数量",reply_markup=ReplyKeyboardMarkup(admin_keybaord,
                                                               resize_keyboard=True),parse_mode=ParseMode.HTML)


    return ADMIN1



last_info = {}

async def manage(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print(update.callback_query)
    if update.callback_query:



        query = update.callback_query
        data = query.data
        uid = query.from_user.id



        back_inline = [[InlineKeyboardButton("返回主菜单", callback_data='backmain')]]

        if data == 'addp':
            await query.edit_message_text("输入产品类别中英文名称:\n例如：\n\n<code>🌍飞机编号✈印度尼西亚️tdata|🌍number✈Indonesiatdata</code>\n\n"
                                          "不要忘记名称以 | 开头。分离",reply_markup=InlineKeyboardMarkup(back_inline),parse_mode=ParseMode.HTML)

            last_info[uid] = 'getsubname'

            return ADMIN3
        elif data == 'delp':
            plist = [
                [
                 InlineKeyboardButton('↩️关闭', callback_data='back')]
            ]

            pros = list(products.find())

            for i in pros:
                plist.append([InlineKeyboardButton(i['ch'], callback_data=f'rem{i["pid"]}')])

            await query.edit_message_text("选择其类别以将其删除:", reply_markup=InlineKeyboardMarkup(plist))
            return ADMIN1

        elif data == 'back':
            await query.delete_message()
            return ADMIN1
        elif data == 'backmain':
            await query.delete_message()
            await context.bot.send_message(chat_id=uid , text="你好管理员",reply_markup=ReplyKeyboardMarkup(admin_keybaord,
                                                               resize_keyboard=True))
            return ADMIN1

        elif data.startswith('pid'):
            pid = data[3:]
            idems = list(items.find({"from_pid" : pid}))

            plist = [
                [InlineKeyboardButton('➕新增项目',callback_data=f'addi{pid}'),InlineKeyboardButton('返回↩',callback_data='backpid')]
            ]

            for i in idems:
                plist.append([InlineKeyboardButton(i['ch'], callback_data=f'itim{i["tid"]}')])

            await query.edit_message_text("您可以使用以下按钮删除、添加或更改产品类别:", reply_markup=InlineKeyboardMarkup(plist))
            return ADMIN1

        elif data.startswith("addi"):
            from_pid = data[4:]

            back_inline = [[InlineKeyboardButton('返回↩', callback_data='backpid')]]

            await query.edit_message_text(
                "输入产品类别中英文名称:\n例如：\n\n<code>🇺🇸美国Tdata|🇺🇸USA tdata</code>\n\n"
                "不要忘记名称以 | 开头。分离", reply_markup=InlineKeyboardMarkup(back_inline), parse_mode=ParseMode.HTML)

            last_info[uid] = {'status' : 'getitemname' ,'from_pid' : from_pid}

            return ADMIN3
        elif data == "backpid":
            plist = [
                [InlineKeyboardButton('➕添加产品', callback_data='addp'),
                 InlineKeyboardButton('❌删除类别', callback_data='delp'),
                 InlineKeyboardButton('↩️后退', callback_data='back')]
            ]

            pros = list(products.find())

            for i in pros:
                plist.append([InlineKeyboardButton(i['ch'], callback_data=f'pid{i["pid"]}')])

            await query.edit_message_text("您可以使用以下按钮删除、添加或更改产品类别", reply_markup=InlineKeyboardMarkup(plist))
            return ADMIN1

        elif data.startswith('itim'):
            cods = data[4:]
            check = items.find_one({"tid" : cods})
            pback = [
                [
                 InlineKeyboardButton('返回↩', callback_data=f'backtid{check["from_pid"]}')]
            ]
            await query.edit_message_text(f"""💴每件价格：{check["price"]} USDT

使用以下命令，您可以更改价格、更改名称或删除它

更改价格
<code>/setprice {cods} 0.9</code>

删除服务
<code>/delete {cods}</code>

名称变更
<code>/rename {cods} 姓名|NAME</code>

            """,reply_markup=InlineKeyboardMarkup(pback),parse_mode=ParseMode.HTML)
            return ADMIN1


        elif data.startswith("backtid"):
            pid = data[7:]
            idems = list(items.find({"from_pid": pid}))

            plist = [
                [InlineKeyboardButton('➕新增项目', callback_data=f'addi{pid}'),
                 InlineKeyboardButton('返回↩', callback_data='backpid')]
            ]

            for i in idems:
                plist.append([InlineKeyboardButton(i['ch'], callback_data=f'itim{i["tid"]}')])

            await query.edit_message_text("您可以使用以下按钮删除、添加或更改产品类别:", reply_markup=InlineKeyboardMarkup(plist))
            return ADMIN1








        elif data.startswith('rem'):
            todel = data[3:]
            products.delete_one({"pid" : todel})

            plist = [
                [InlineKeyboardButton('➕添加产品', callback_data='addp'),
                 InlineKeyboardButton('❌删除类别', callback_data='delp'),
                 InlineKeyboardButton('↩️后退', callback_data='back')]
            ]

            pros = list(products.find())

            for i in pros:
                plist.append([InlineKeyboardButton(i['ch'], callback_data=f'pid{i["pid"]}')])

            await query.edit_message_text("所需类别已被删除✅\n\n您可以使用以下按钮删除、添加或更改产品类别", reply_markup=InlineKeyboardMarkup(plist))
            return ADMIN1








    text = update.message.text

    if context.args and len(context.args) > 0:
        if text.startswith("/setprice"):
            cuds = context.args[0]
            new_price = float(context.args[1])
            items.update_one({"tid" : cuds} , {"$set" : {'price' : new_price}})

            await update.message.reply_text("价格已更改")
            return ADMIN1

        if text.startswith("/rename"):
            cuds = context.args[0]
            name = context.args[1]

            try:

                ch = name.split("|")[0]
                en = name.split("|")[1]

                idm = items.find_one({"tid" : cuds})

                prd = products.find_one({"pid" : idm['from_pid']})

                os.rename(f"{prd['ch']}/{idm['ch']}",f"{prd['ch']}/{ch}")
                items.update_one({"tid" : cuds} , {"$set" : {'ch' : ch , "en" : en}})

                await update.message.reply_text("名称已更改")


            except Exception as e:
                await update.message.reply_text(f"ERORR! {e}")




            return ADMIN1


        if text.startswith("/delete"):
            cuds = context.args[0]
            items.delete_one({"tid" : cuds})

            await update.message.reply_text("已删除")
            return ADMIN1
        if text.startswith("/bal") and len(context.args) > 1:
            userid = context.args[0]
            bals = float(context.args[1])

            print(userid , bals)

            user = users.find_one({"userid" : int(userid)})
            if not user:
                await update.message.reply_text("未找到用户!")
                return ADMIN1
            newbl = user['balance'] + bals
            users.update_one({"userid": int(userid)}, {"$set": {'balance': newbl}})

            await update.message.reply_text(f"库存发生变化。用户新增余额：{user['balance']+bals}")
            return ADMIN1


    if text.startswith("/info"):
        if len(context.args) > 0:
            userid = context.args[0]
            info = users.find_one({"userid": int(userid)})
            if info == None:
                await update.message.reply_text("未找到用户")
                return SELECT_MENU

            await update.message.reply_text(f"""
🔹用户库存 :  {info['balance']}U
🔹用过的： {info['used_balance']}U
🔹购买数量 :  {info['total_buy']}
注册日期 : {china_time(info["register_time"])}

""")

    if text.startswith("/status"):
        total_users = users.count_documents({})
        totalpays = payments.count_documents({"status" : 2})


        await update.message.reply_text(F"用户数量：{total_users}\n\n付款次数：{totalpays}")
        return ADMIN1








    if text == "产品列表":


        plist = [
            [InlineKeyboardButton('➕添加产品',callback_data='addp'), InlineKeyboardButton('❌删除类别',callback_data='delp'), InlineKeyboardButton('↩️后退',callback_data='back')]
        ]

        pros = list(products.find())

        for i in pros:
            plist.append([InlineKeyboardButton(i['ch'], callback_data=f'pid{i["pid"]}')])

        await update.message.reply_text("您可以使用以下按钮删除、添加或更改产品类别",reply_markup=InlineKeyboardMarkup(plist))
        return ADMIN1

#     elif text == "地位":
#         get_address = listen_addresses.count_documents({})
#         get_users = users.count_documents({})
#
#         await update.message.reply_text(f"""
# 用户总数：{get_users}
# 用户添加的总地址：{get_address}
# """,reply_markup=ReplyKeyboardMarkup(admin_keybaord,resize_keyboard=True))
#         return ADMIN1
    elif text == "通知所有人":
        await update.message.reply_text(f"""发送您的短信：""", reply_markup=ReplyKeyboardMarkup(admin_keybaord, resize_keyboard=True))
        return ADMIN2




async def sender(context: ContextTypes.DEFAULT_TYPE , userid , text):
    get_users = list(users.find({}))
    for i in get_users:
        try:
            await context.bot.send_message(chat_id=i['userid'], text=text, parse_mode=ParseMode.HTML)
        except:
            pass
    await context.bot.send_message(chat_id=userid, text= "发送完成")

    return


async def manage2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text_html
    uid = update.message.from_user.id

    context.job_queue.run_once(lambda n: sender(context, uid, text),1)

    await update.message.reply_text("排队等待发送", reply_markup=ReplyKeyboardMarkup(admin_keybaord, resize_keyboard=True))
    return ADMIN1

def create_directory(path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory '{path}' created successfully.")
        return True
    except OSError as error:
        return False



#input(111)

async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.message.from_user.id
    if uid not in owners:
        return SELECT_MENU

    #back_inline = [[InlineKeyboardButton("返回主菜单", callback_data='backmain')]]

    if last_info.get(uid):
        edata = last_info[uid]


        if edata == "getsubname":
            if '|' not in text:
                await update.message.reply_text(f"""-未知的命令。再试一次!""",
                                                reply_markup=ReplyKeyboardMarkup(admin_keybaord, resize_keyboard=True))
                return ADMIN1

            ch = text.split('|')[0].strip()
            en = text.split('|')[1].strip()

            if create_directory(f"{ch}"):
                pass
            else:
                await update.message.reply_text(f"""未知的命令。再试一次!""",
                                                reply_markup=ReplyKeyboardMarkup(admin_keybaord, resize_keyboard=True))
                return ADMIN1



            products.insert_one({"pid" : id_generator(),"ch" : ch, "en" : en})

            await update.message.reply_text(
                "类别名称已设置✅")
            plist = [
                [InlineKeyboardButton('➕添加产品', callback_data='addp'),
                 InlineKeyboardButton('❌删除类别', callback_data='delp'),
                 InlineKeyboardButton('↩️后退', callback_data='back')]
            ]

            pros = list(products.find())

            for i in pros:
                plist.append([InlineKeyboardButton(i['ch'], callback_data=f'pid{i["pid"]}')])

            await update.message.reply_text("您可以使用以下按钮删除、添加或更改产品类别", reply_markup=InlineKeyboardMarkup(plist))
            last_info.clear()

            return ADMIN1


        elif edata['status'] == 'getitemname':
            if '|' not in text:
                await update.message.reply_text(f"""你来自 |你没有使用""",
                                                reply_markup=ReplyKeyboardMarkup(admin_keybaord, resize_keyboard=True))
                return ADMIN1

            ch = text.split('|')[0].strip()
            en = text.split('|')[1].strip()



            last_info[uid]['ch'] = ch
            last_info[uid]['en'] = en



            prod = products.find_one({"pid" : edata['from_pid']})

            if create_directory(f"{prod['ch']}/{ch}"):
                pass
            else:
                await update.message.reply_text(f"""未知的命令。再试一次!.""",
                                                reply_markup=ReplyKeyboardMarkup(admin_keybaord, resize_keyboard=True))
                return ADMIN1

            #products.insert_one({"pid": id_generator(), "ch": ch, "en": en})

            await update.message.reply_text(
                "输入每件的价格：")
            last_info[uid]['status'] = "getprice"

            return ADMIN3

        elif edata['status'] == 'getprice':
            try:
                count = float(text)
            except:
                await update.message.reply_text(f"""输入的号码不正确!""")
                return ADMIN3

            items.insert_one({"tid" : id_generator() , "from_pid" : last_info[uid]['from_pid'] , "ch" : last_info[uid]["ch"] , "en" : last_info[uid]['en'], 'price' : count})

            await update.message.reply_text(
                "类别名称已设置✅")
            idems = list(items.find({"from_pid": last_info[uid]['from_pid']}))

            plist = [
                [InlineKeyboardButton('➕新增项目', callback_data=f'addi{last_info[uid]["from_pid"]}'),
                 InlineKeyboardButton('返回↩', callback_data='backpid')]
            ]

            for i in idems:
                plist.append([InlineKeyboardButton(i['ch'], callback_data=f'itim{i["tid"]}')])

            await update.message.reply_text("您可以使用以下按钮删除、添加或更改产品类别:", reply_markup=InlineKeyboardMarkup(plist))
            last_info.clear()

            return ADMIN1






        else:
            await update.message.reply_text(f"""未知的命令。再试一次!""",
                                            reply_markup=ReplyKeyboardMarkup(admin_keybaord, resize_keyboard=True))
            return ADMIN2



    else:
        await update.message.reply_text(f"""未知的命令。再试一次""",
                                        reply_markup=ReplyKeyboardMarkup(admin_keybaord, resize_keyboard=True))
        return ADMIN2




#
# is_admin = [False]
#
#

#
#

#
#
#
#
#
#
# async def manage2(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text_html
#
#     get_users = list(users.find({}))
#
#     for i in get_users:
#         try:
#             await context.bot.send_message(chat_id=i['userid'],text=text,parse_mode=ParseMode.HTML)
#         except:
#             pass
#
#     await update.message.reply_text("完毕", reply_markup=ReplyKeyboardMarkup(admin_keybaord, resize_keyboard=True))
#     return ADMIN1

def main() -> None:
    """Run the bot."""
    # We use persistence to demonstrate how buttons can still work after the bot was restarted
    persistence = PicklePersistence(filepath="main")

    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token(bot_token)
        .persistence(persistence).concurrent_updates(True)
        .arbitrary_callback_data(True).connect_timeout(10).read_timeout(10).write_timeout(10).pool_timeout(10).get_updates_connect_timeout(10).get_updates_pool_timeout(10).get_updates_write_timeout(10)
        #.proxy("http://127.0.0.1:10809")
        #.get_updates_proxy("http://127.0.0.1:10809")
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start),



                      ],
        states={
            SELECT_MENU : [
                CommandHandler("start", start), #
                CommandHandler("admin", admin),  #
                MessageHandler(filters.Regex("🏠我的账户|🛍️商品列表|❓联系客服|💳充值余额|✅转账套餐|✈️电报会员 Center|🛒Product List|♻TRX&Energy|💳Recharge|📞Contact Service|🌐Switch Language"), text_manage),
                CallbackQueryHandler(text_manage, pattern='^usd|cancel|number|^subpid|backpu|instract|^buy|^utem|custom'),
                #MessageHandler(filters.Regex("◀️后退|🔙 返回上级"), start),
                #MessageHandler(filters.StatusUpdate.CHAT_SHARED | filters.StatusUpdate.USER_SHARED, send_id),

            ],
            ADMIN1 : [ #
                MessageHandler(filters.Regex("产品列表|通知所有人"), manage),
                MessageHandler(filters.Regex("后退"), start),
                CallbackQueryHandler(manage, pattern='^addp|delp|back|^rem|^pid|backmain|^addi|backpid|^itim'),
                CommandHandler("setprice", manage),  #
                CommandHandler("bal", manage),  #
                CommandHandler("delete", manage),  #
                CommandHandler("info", manage),  #
                CommandHandler("status", manage),  #
                CommandHandler("rename", manage),  #
            ],
            ADMIN3 : [
                MessageHandler(filters.Regex("产品列表|通知所有人"), manage),
                MessageHandler(filters.Regex("后退"), start),
                CallbackQueryHandler(manage, pattern='^addp|delp|back|^rem|^pid|backmain|^addi|backpid|^itim'),
                MessageHandler(filters.TEXT, get_info),

            ],
            BUY: [
                CommandHandler("start", start),  #
                CommandHandler("admin", admin),  #
                CommandHandler("status", manage),  #
                MessageHandler(filters.Regex(
                    "🏠我的账户|🛍️商品列表|❓联系客服|💳充值余额|✅转账套餐|✈️电报会员 Center|🛒Product List|♻TRX&Energy|💳Recharge|📞Contact Service|🌐Switch Language"),
                               text_manage),
                CallbackQueryHandler(text_manage, pattern='^usd|cancel|number|^subpid|backpu|instract|^buy|^utem'),
                MessageHandler(filters.TEXT, buyacc),

            ],
            BUY_FINAL : [
                CommandHandler("start", start),  #
                CommandHandler("admin", admin),  #
                MessageHandler(filters.Regex(
                    "🏠我的账户|🛍️商品列表|❓联系客服|💳充值余额|✅转账套餐|✈️电报会员 Center|🛒Product List|♻TRX&Energy|💳Recharge|📞Contact Service|🌐Switch Language"),
                    text_manage),
                CallbackQueryHandler(text_manage, pattern='^usd|cancel|number|^subpid|backpu|instract|^buy|^utem'),
                CallbackQueryHandler(final_buy, pattern='^acc'),
            ],
            ADMIN2: [
                MessageHandler(filters.Regex("产品列表|通知所有人"), manage),
                MessageHandler(filters.Regex("后退"), start),
                CallbackQueryHandler(manage, pattern='^addp|delp|back|^rem|^pid|backmain|^addi|backpid|^itim'),
                CommandHandler("setprice", manage),  #
                CommandHandler("delete", manage),  #
                CommandHandler("status", manage),  #
                MessageHandler(filters.TEXT, manage2),
            ],
            GET_SELECT : [
                CommandHandler("start", start),  #
                CommandHandler("admin", admin),  #
                MessageHandler(filters.Regex(
                    "🏠我的账户|🛍️商品列表|❓联系客服|💳充值余额|✅转账套餐|✈️电报会员 Center|🛒Product List|♻TRX&Energy|💳Recharge|📞Contact Service|🌐Switch Language"),
                               text_manage),
                CallbackQueryHandler(text_manage,
                                     pattern='^usd|cancel|number|^subpid|backpu|instract|^buy|^utem|custom'),
                MessageHandler(filters.TEXT,
                    makepay),


            ]








        },
        fallbacks=[CommandHandler("start", start),]
    )

    #application.add_handler(
    #    MessageHandler(filters.ChatType.GROUP | filters.ChatType.GROUPS | filters.ChatType.SUPERGROUP, group_manage), )

    application.add_handler(conv_handler)






    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    #threading.Thread(target=online_checker).start()
    main()
  机器人启动ing



