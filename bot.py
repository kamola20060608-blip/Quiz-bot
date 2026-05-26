import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN", "8838674970:AAE_v-6C-XL1HFaDFNf9lKAm7etrWURfKuk")

FANLAR = {
    "📐 Matematika": [
        {"savol": "2 + 2 = ?", "variantlar": ["3", "4", "5", "6"], "togri": 1},
        {"savol": "5 × 5 = ?", "variantlar": ["20", "25", "30", "35"], "togri": 1},
        {"savol": "10 ÷ 2 = ?", "variantlar": ["3", "4", "5", "6"], "togri": 2},
        {"savol": "3² = ?", "variantlar": ["6", "8", "9", "12"], "togri": 2},
        {"savol": "100 - 37 = ?", "variantlar": ["63", "67", "73", "57"], "togri": 0},
    ],
    "🔬 Fizika": [
        {"savol": "Yorug'lik tezligi?", "variantlar": ["200,000 km/s", "300,000 km/s", "400,000 km/s", "150,000 km/s"], "togri": 1},
        {"savol": "Gravitatsiya tezlanishi?", "variantlar": ["9.1 m/s²", "9.8 m/s²", "10.5 m/s²", "11 m/s²"], "togri": 1},
        {"savol": "Elektr o'lchov birligi?", "variantlar": ["Vatt", "Amper", "Volt", "Om"], "togri": 2},
        {"savol": "Ovoz tezligi (havoda)?", "variantlar": ["343 m/s", "500 m/s", "100 m/s", "1000 m/s"], "togri": 0},
        {"savol": "Issiqlik o'lchov birligi?", "variantlar": ["Vatt", "Joule", "Nyuton", "Paskal"], "togri": 1},
    ],
    "🧪 Kimyo": [
        {"savol": "Suvning formulasi?", "variantlar": ["CO2", "H2O", "NaCl", "O2"], "togri": 1},
        {"savol": "Osh tuzi formulasi?", "variantlar": ["KCl", "NaCl", "CaCl2", "MgCl2"], "togri": 1},
        {"savol": "Kislorod belgisi?", "variantlar": ["K", "O", "C", "N"], "togri": 1},
        {"savol": "CO2 nima gaz?", "variantlar": ["Kislorod", "Azot", "Karbonat angidrid", "Vodorod"], "togri": 2},
        {"savol": "Temir belgisi?", "variantlar": ["Ti", "Fe", "Cr", "Ni"], "togri": 1},
    ],
    "🌍 Geografiya": [
        {"savol": "O'zbekiston poytaxti?", "variantlar": ["Samarqand", "Buxoro", "Toshkent", "Namangan"], "togri": 2},
        {"savol": "Dunyoning eng baland tog'i?", "variantlar": ["K2", "Everest", "Elbrus", "Kilimanjaro"], "togri": 1},
        {"savol": "Eng katta okean?", "variantlar": ["Atlantika", "Hind", "Tinch", "Shimoliy Muz"], "togri": 2},
        {"savol": "O'zbekistonda nechta viloyat bor?", "variantlar": ["11", "12", "13", "14"], "togri": 2},
        {"savol": "Amudaryo qayerga quyiladi?", "variantlar": ["Kaspiy", "Orol", "Qora dengiz", "Fors ko'rfazi"], "togri": 1},
    ],
    "📚 Tarix": [
        {"savol": "O'zbekiston mustaqillik yili?", "variantlar": ["1990", "1991", "1992", "1993"], "togri": 1},
        {"savol": "Amir Temur qachon tug'ilgan?", "variantlar": ["1330", "1336", "1340", "1350"], "togri": 1},
        {"savol": "Temuriylar davlati poytaxti?", "variantlar": ["Buxoro", "Samarqand", "Hirot", "Toshkent"], "togri": 1},
        {"savol": "Ikkinchi jahon urushi tugagan yil?", "variantlar": ["1943", "1944", "1945", "1946"], "togri": 2},
        {"savol": "Buyuk ipak yo'li qayerdan o'tgan?", "variantlar": ["Faqat Xitoydan", "O'rta Osiyodan", "Faqat Yevropadan", "Afrikadan"], "togri": 1},
    ],
    "💻 Informatika": [
        {"savol": "1 GB = ? MB", "variantlar": ["512", "1024", "2048", "256"], "togri": 1},
        {"savol": "Python kim yaratgan?", "variantlar": ["James Gosling", "Guido van Rossum", "Dennis Ritchie", "Linus Torvalds"], "togri": 1},
        {"savol": "HTML nima?", "variantlar": ["Dasturlash tili", "Belgilash tili", "Ma'lumotlar bazasi", "Operatsion tizim"], "togri": 1},
        {"savol": "CPU nima?", "variantlar": ["Xotira", "Protsessor", "Grafik karta", "Qattiq disk"], "togri": 1},
        {"savol": "www nima?", "variantlar": ["World Wide Web", "World Web Wide", "Wide World Web", "Web World Wide"], "togri": 0},
    ],
}

def asosiy_menyu():
    keyboard = [
        [KeyboardButton("📚 Fanlar"), KeyboardButton("📊 Natijam")],
        [KeyboardButton("ℹ️ Yordam")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def fanlar_keyboard():
    keyboard = []
    for fan in FANLAR.keys():
        keyboard.append([InlineKeyboardButton(fan, callback_data=f"fan_{fan}")])
    return InlineKeyboardMarkup(keyboard)

def quiz_keyboard(fan, savol_index, variantlar):
    harflar = ["A", "B", "C", "D"]
    keyboard = []
    for i, variant in enumerate(variantlar):
        keyboard.append([InlineKeyboardButton(
            f"{harflar[i]}) {variant}",
            callback_data=f"j_{fan}_{savol_index}_{i}"
        )])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Salom! Quiz Botga xush kelibsiz!\n\n"
        "🎯 6 ta fandan testlar ishlang\n"
        "📊 Natijalaringizni kuzating\n\n"
        "⬇️ Pastdagi tugmalardan birini bosing:",
        reply_markup=asosiy_menyu()
    )

async def xabar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text

    if matn == "📚 Fanlar":
        await update.message.reply_text(
            "📖 Qaysi fanni tanlaysiz?\n\nHar bir fanda 5 ta savol bor:",
            reply_markup=fanlar_keyboard()
        )
    elif matn == "📊 Natijam":
        natijalar = context.user_data.get("natijalar", {})
        if not natijalar:
            await update.message.reply_text("❌ Hali hech qanday test ishlamagansiz!\n\n📚 Fanlar tugmasini bosing va boshlang!")
        else:
            text = "📊 Sizning natijalaringiz:\n\n"
            umumiy_togri = 0
            umumiy_jami = 0
            for fan, n in natijalar.items():
                foiz = (n['togri'] / n['jami']) * 100
                text += f"{fan}\n✅ {n['togri']}/{n['jami']} — {foiz:.0f}%\n\n"
                umumiy_togri += n['togri']
                umumiy_jami += n['jami']
            if umumiy_jami > 0:
                umumiy_foiz = (umumiy_togri / umumiy_jami) * 100
                text += f"━━━━━━━━━━━━\n🏆 Umumiy: {umumiy_togri}/{umumiy_jami} — {umumiy_foiz:.0f}%"
            await update.message.reply_text(text)
    elif matn == "ℹ️ Yordam":
        await update.message.reply_text(
            "ℹ️ Qanday ishlaydi:\n\n"
            "1️⃣ 'Fanlar' tugmasini bosing\n"
            "2️⃣ Fan tanlang\n"
            "3️⃣ Savollarga A/B/C/D javob bering\n"
            "4️⃣ Har savoldan keyin natija chiqadi\n"
            "5️⃣ Test tugagach umumiy ball ko'rsatiladi\n\n"
            "📊 'Natijam' — barcha natijalaringiz"
        )

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("fan_"):
        fan = data[4:]
        context.user_data["fan"] = fan
        context.user_data["index"] = 0
        context.user_data["togri"] = 0

        savol = FANLAR[fan][0]
        await query.edit_message_text(
            f"🎯 {fan}\n"
            f"━━━━━━━━━━━━\n"
            f"❓ Savol 1/{len(FANLAR[fan])}:\n\n"
            f"{savol['savol']}",
            reply_markup=quiz_keyboard(fan, 0, savol["variantlar"])
        )

    elif data.startswith("j_"):
        qismlar = data.split("_", 3)
        fan = qismlar[1]
        index = int(qismlar[2])
        tanlangan = int(qismlar[3])

        savol = FANLAR[fan][index]
        harflar = ["A", "B", "C", "D"]

        if tanlangan == savol["togri"]:
            context.user_data["togri"] = context.user_data.get("togri", 0) + 1
            natija = "✅ To'g'ri javob!"
        else:
            togri_var = savol["variantlar"][savol["togri"]]
            natija = f"❌ Noto'g'ri!\nTo'g'ri javob: {harflar[savol['togri']]}) {togri_var}"

        keyingi = index + 1

        if keyingi < len(FANLAR[fan]):
            savol2 = FANLAR[fan][keyingi]
            await query.edit_message_text(
                f"{natija}\n"
                f"━━━━━━━━━━━━\n"
                f"🎯 {fan}\n\n"
                f"❓ Savol {keyingi + 1}/{len(FANLAR[fan])}:\n\n"
                f"{savol2['savol']}",
                reply_markup=quiz_keyboard(fan, keyingi, savol2["variantlar"])
            )
        else:
            togri = context.user_data.get("togri", 0)
            jami = len(FANLAR[fan])
            foiz = (togri / jami) * 100

            if foiz == 100:
                baho = "🏆 Mukammal!"
            elif foiz >= 80:
                baho = "🥇 A'lo!"
            elif foiz >= 60:
                baho = "🥈 Yaxshi"
            elif foiz >= 40:
                baho = "🥉 Qoniqarli"
            else:
                baho = "📖 Ko'proq o'qing"

            if "natijalar" not in context.user_data:
                context.user_data["natijalar"] = {}
            context.user_data["natijalar"][fan] = {"togri": togri, "jami": jami}

            tugmalar = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Qayta urinish", callback_data=f"fan_{fan}")],
                [InlineKeyboardButton("📚 Boshqa fan", callback_data="fanlar")]
            ])

            await query.edit_message_text(
                f"{natija}\n"
                f"━━━━━━━━━━━━\n"
                f"🎉 Test yakunlandi!\n\n"
                f"📊 Natija: {togri}/{jami}\n"
                f"📈 Foiz: {foiz:.0f}%\n"
                f"🎯 Baho: {baho}",
                reply_markup=tugmalar
            )

    elif data == "fanlar":
        await query.edit_message_text(
            "📖 Qaysi fanni tanlaysiz?\n\nHar bir fanda 5 ta savol bor:",
            reply_markup=fanlar_keyboard()
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabar))
    app.add_handler(CallbackQueryHandler(callback))
    print("✅ Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
