from app.extensions import db
from app.models import Era, Myth, Relationship, ParentChild, Category, Family, RelationType
from datetime import date

# Seed data
eras_data = [
    {"id": "pshd", "name": "پیشدادیان", "oldName": "اسطوره", "image": "eras/pishdadiyan.jpg", "color": "gold",
        "description": ""},
    {"id": "dzhk", "name": "دوران ضحاک", "oldName": "اسطوره", "image": "eras/doraneZahak.jpg", "color": "silver",
        "description": ""},
    {"id": "dfrydn", "name": "دوران فریدون", "oldName": "اسطوره", "image": "eras/doraneFereydoun.jpg", "color": "red",
        "description": ""},
    {"id": "dphlvn", "name": "دوران پهلوانی", "oldName": "اسطوره - حماسه", "image": "eras/doranePahlevani.jpg", "color": "red",
     "description": ""},
    {"id": "kyn", "name": "کیانیان", "oldName": "حماسه", "image": "eras/doraneKiyanian.jpg", "color": "red",
     "description": ""},
    {"id": "atrkh", "name": "آغاز دوران تاریخی", "oldName": "حماسه - تاریخ", "image": "eras/aghazeDoraneTarikhi.jpg", "color": "red",
     "description": ""},
    {"id": "trkh", "name": "تاریخ", "oldName": "-", "image": "eras/doraneTarikhi.jpg", "color": "red",
     "description": ""},
]

relation_types_data = [
    {"id": "mrig", "name": "marriage", "color": "blue"},
    {"id": "prnt", "name": "parent", "color": "green"},
    {"id": "frnd", "name": "friendship", "color": "green"},
    {"id": "empl", "name": "employee", "color": "green"},
    {"id": "enmy", "name": "enemy", "color": "red"},
    {"id": "adpt", "name": "adoptive", "color": "purple"}
]

category_data = [
    {"id": "pdsh", "title": "پادشاه", "imageProfile": "./padeshahanProfile.jpg",
        "imageBg": "./padeshahanBg.jpg", "description": ""},
    {"id": "shzd", "title": "شاهزاده", "imageProfile": "./shahzadeProfile.jpg",
        "imageBg": "./Bg.jpg", "description": ""},
    {"id": "plvn", "title": "پهلوان", "imageProfile": "./pahlevanProfile.jpg",
        "imageBg": "./pahlevanBg.jpg", "description": ""},
    {"id": "div", "title": "دیو", "imageProfile": "./divProfile.jpg",
        "imageBg": "./divBg.jpg", "description": ""},
    {"id": "vzr", "title": "وزیر", "imageProfile": "./vazirProfile.jpg",
        "imageBg": "./vazirBg.jpg", "description": ""},
    {"id": "khen", "title": "خائن", "imageProfile": "./khaenProfile.jpg",
        "imageBg": "./khaenBg.jpg", "description": ""},
    {"id": "jdgr", "title": "جادوگر", "imageProfile": "./jadougarProfile.jpg",
        "imageBg": "./jadougarBg.jpg", "description": ""},
    {"id": "afsngr", "title": "افسونگر", "imageProfile": "./afsoungarProfile.jpg",
        "imageBg": "./afsoungarBg.jpg", "description": ""},
    {"id": "ahrmn", "title": "اهریمن", "imageProfile": "./ahrimanProfile.jpg",
        "imageBg": "./ahrimanBg.jpg", "description": ""},
    {"id": "frsht", "title": "فرشته", "imageProfile": "./fereshteProfile.jpg",
        "imageBg": "./fereshteBg.jpg", "description": ""},
    {"id": "mrdm", "title": "مردم عادی", "imageProfile": "./mardomProfile.jpg",
     "imageBg": "./mardomBg.jpg", "description": ""},
]

family_data = [
    {"id": "irn", "title": "ایرانیان", "imageProfile": "./iranianProfile.jpg",
        "imageBg": "./iranianBg.jpg", "description": ""},
    {"id": "trn", "title": "تورانیان", "imageProfile": "./touranianProfile.jpg",
        "imageBg": "./touranianBg.jpg", "description": ""},
    {"id": "tzn", "title": "تازیان", "imageProfile": "./tazianProfile.jpg",
        "imageBg": "./tazianBg.jpg", "description": ""},
    {"id": "gdrz", "title": "گودرزیان", "imageProfile": "./goudarzianProfile.jpg",
        "imageBg": "./goudarzianBg.jpg", "description": ""},
    {"id": "sist", "title": "سیستانیان", "imageProfile": "./sistanianProfile.jpg",
        "imageBg": "./sistanianBg.jpg", "description": ""},
    {"id": "nzr", "title": "نوذریان", "imageProfile": "./nozarianProfile.jpg",
        "imageBg": "./nozarianBg.jpg", "description": ""},
    {"id": "anr", "title": "انیران", "imageProfile": "./aniranProfile.jpg",
        "imageBg": "./aniranBg.jpg", "description": ""},
    {"id": "dgr", "title": "دیگران", "imageProfile": "./digaranProfile.jpg",
        "imageBg": "./digaranBg.jpg", "description": "سایر"},

]

myths_data = [
    {
        "id": "kmrs",
        "name": "کیومرث",
        "nickname": "کیومرث",
        "pos": "10 10",
        "imageProfile": "path/to/KioumarsProfile.jpg",
        "imageBg": "path/to/KioumarsBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": True,
        "era_id": "pshd",
        "family_id": "irn",
        "category_id": "pdsh",
        "description": "اولین پادشاه جهان "
    },
    {
        "id": "simk",
        "name": "سیامک",
        "nickname": "سیامک",
        "pos": "10 40",
        "imageProfile": "path/to/SiamakProfile.jpg",
        "imageBg": "path/to/SiamakBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": True,
        "era_id": "pshd",
        "family_id": "irn",
        "category_id": "pdsh",
        "description": ""
    },
    {
        "id": "ahrmn",
        "name": "اهریمن",
        "nickname": "اهریمن",
        "pos": "40 40",
        "imageProfile": "path/to/AhrimanProfile.jpg",
        "imageBg": "path/to/AhrimanBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "description": "",
        "era_id": "pshd",
        "family_id": "dgr",
        "category_id": "ahrmn"
    },
    {
        "id": "ebls",
        "name": "ابلیس",
        "nickname": "ابلیس",
        "pos": "40 70",
        "imageProfile": "path/to/eblisProfile.jpg",
        "imageBg": "path/to/eblisBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "description": "",
        "era_id": "pshd",
        "family_id": "dgr",
        "category_id": "ahrmn"
    },
    {
        "id": "dvsh",
        "name": "دیو سیاه",
        "nickname": "دیو سیاه",
        "pos": "40 100",
        "imageProfile": "path/to/divSiyahProfile.jpg",
        "imageBg": "path/to/divSiyahBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "description": "",
        "era_id": "pshd",
        "family_id": "dgr",
        "category_id": "ahrmn"
    },

    {
        "id": "bdiv",
        "name": "بچه دیو",
        "nickname": "بچه دیو",
        "pos": "40 130",
        "imageProfile": "path/to/AhrimanProfile.jpg",
        "imageBg": "path/to/AhrimanBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "description": "",
        "era_id": "pshd",
        "family_id": "dgr",
        "category_id": "ahrmn"
    },
    {
        "id": "srsh",
        "name": "سروش",
        "nickname": "سروش آسمانی",
        "pos": "-30 70",
        "imageProfile": "path/to/SorushProfile.jpg",
        "imageBg": "path/to/SorushBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "description": "",
        "era_id": "pshd",
        "family_id": "dgr",
        "category_id": "frsht",
    },
    {
        "id": "hshng",
        "name": "هوشنگ",
        "nickname": "هوشنگ",
        "pos": "10 70",
        "imageProfile": "path/to/HoushangProfile.jpg",
        "imageBg": "path/to/HoushangBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": True,
        "era_id": "pshd",
        "family_id": "irn",
        "category_id": "pdsh",
        "description":
            "هوشنگ به نیرومند و دلیر بودن شهرت داشت \n" +
            "هوشنگ بعد از درگذشت کیومرث تاج پادشاهی بر سر نهاد و به آباد کردن زمین و خوشبختی مردمان کوشید. \n" +
            "در آن زمان مردم لباسی به جز برگ درختان و غذایی به جز میوه ها نداشتند \n" +
            "هوشنگ به نیروی دانش نخست آتش را کشف کرد و مردم را به جشن و شادمانی فراخواند و نام آن جشن را جشن سده گذاشتند \n" +
            "سپس به یاری آتش، آهن را از دل تخته سنگ ها بیرون کشید و به مردم پیشه وری و کشت گری آموخت \n" +
            "هوشنگ 40 سال پادشاهی کرد"
    },
    {
        "id": "tmrs",
        "name": "تهمورث",
        "nickname": "دیو بند",
        "pos": "10 100",
        "imageProfile": "path/to/tahmouresProfile.jpg",
        "imageBg": "path/to/tahmouresBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": True,
        "era_id": "pshd",
        "family_id": "irn",
        "category_id": "pdsh",
        "description":
            "تهمورث - دیو بند - پادشاهی بود که به دادگری می کوشید \n" +
            "آسودگی مردمان و آبادانی کشور در زمان تهمورث به جایی رسید که دیوان از روی حسد شورش کردند \n" +
            "تهمورث به نیرنگ دیوان پی برد و به جنگ آنها برخواست. گروهی را کشت و گروه بی شماری را به بند کشید. \n" +
            "دیوان از کار خود پشیمان شده و از شاه زینهار خواستند که اگر آنان را آزاد کند به شاه و مردمان ایران زمین خواندن و نوشتن یاد دهند. \n" +
            "تهمورث 30 سال پادشاه بود. "
    },
    {
        "id": "shdsp",
        "name": "شیداسپ",
        "nickname": "شیدسپ",
        "pos": "60 100",
        "imageProfile": "path/to/shidaspProfile.jpg",
        "imageBg": "path/to/shidaspBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "era_id": "pshd",
        "family_id": "irn",
        "category_id": "vzr",
        "description":
            "وزیر تهمورث بود که در مردم داری و دادگستری بی مانند بود. شیداسپ به تهمورث پادشاه کمک می کرد که شهر های مختلف را ببیند و از وضعیت مردم باخبر شود. \n" +
            "" +
            ""
    },
    {
        "id": "jmshd",
        "name": "جمشید",
        "nickname": "جمشید",
        "pos": "60 140",
        "imageProfile": "path/to/tahmouresProfile.jpg",
        "imageBg": "path/to/tahmouresBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "era_id": "pshd",
        "family_id": "irn",
        "category_id": "pdsh",
        "description":
            "جمشید ساختن ابزار جنگ و دوختن جامه ی رزم را به مردمان آموخت. \n" +
            "جمشید مردم را به 4 گروه بزرگان دین، جنگ آوران، کشت گران و پیشه وران بخش کرد. \n" +
            "جمشید شاه دیوان را به ساخت کاخ های بلند وا داشت. او گنج و گوهر بسیار گردآورد. عطر و بوهای خوش از گل و گیاه گرفت و دانش پزشکی را در کشور رواج داد و برای آشنایی با کار و زندگی مرمان چندی آهنگ سفر کرد. \n" +
            "او 50 سال برای ایران کوشید و در زمان او آبادتر از ایران زمین کشوری نبود و با شکوه ترین پادشاهی را در جهان داشت. \n" +
            "بزرگان در روز نخست فروردین بر درگاه این پادشاه پیروز بخت گردآمدند و بر سرش گوهر افشاندند و آن روز را نوروز نامیدند. "
            "پادشاهی جمشید 350 سال بود و در همه ی این سال ها زندگی مردم با آسایش و آرامش همراه بود. \n" +
            "سرانجام جمشید فریب اهریمن را خورد و از فرمان خدا سرپیچی کرد و به ستایش خود پرداخت. سپس فره ایزدی از او گرفته شد "
            "جمشید شاه خودکامگی پیشه کرد و در اندک زمانی به شور بختی افتاد"
    },
    {
        "id": "mrds",
        "name": "مرداس",
        "nickname": "مرداس",
        "pos": "-30 100",
        "imageProfile": "path/to/mrdsProfile.jpg",
        "imageBg": "path/to/mrdsBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "era_id": "dzhk",
        "category_id": "pdsh",
        "family_id": "tzn",
        "description":
            "پادشاهی خداشناس و دادگر از سرزمین تازیان \n" +
            ""
    },
    {
        "id": "zhk",
        "name": "ضحاک",
        "nickname": "ضحاک",
        "pos": "-30 140",
        "imageProfile": "path/to/zahakrofile.jpg",
        "imageBg": "path/to/zahakBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "era_id": "dzhk",
        "family_id": "tzn",
        "category_id": "pdsh",
        "description":
            "ضحاک بسیار تیره دل و ناسپاس بود. روزی ابلیس در برابر او نمایان شد و او را به کشتن پدرش - مرداس - فریب داد. \n" +
            "ضحاک پدرش را به چاهی ژرف انداخت و ابلیس به او گفت اگر از فرمان من سرپیچی نکنی تو را به پادشاهی سراسر گیتی خواهم رساند و تمام جانوران زمین به فرمان تو خواهند بود. . \n" +
            "دیگر بار ابلیس با چهره ی جوانی زیبا روی و سخندان درآورد و نزد ضحاک رفت و گفت من هنر آشپزی میدانم و اگر پادشاه بپذیرد می توانم هر روز خورش های خوشمزه بپزم. \n" +
            "در آن هنگام خوراک مردمان همه از سبزی و میوه و رستنی های دیگر بود و خوردن گوشت جانوران را کاری ناپسند می دانستند. \n" +
            "ابلیس برای اینکه ضحاک را به بیداد گری و خونریزی برانگیزد او را به گوشتخواری معتاد کرد. \n" +
            "ضحاک که از خوردن این غذاها بسیار خرسند بود از او خواست که هرچه می خواهد از شاه آرزو کند. \n" +
            "ابلیس چنین گفت که مهر شاه در دل اوست و دوست دارد که بر شانه های شاه بوسه زند. \n" +
            "ضحاک درخواست او را پذیرفت و پس از بوسه ی ابلیس بر شانه های ضحاک بی درنگ ابلیس ناپدید شد و دو مار سیاه بیرون آمدند \n" +
            "ضحاک بی درنگ سر آن دو مار را برید ولی آن دو مار چون شاخه ی درخت از کتف شاه بیرون آمدند. \n " +
            "همه ی پزشکان جمع شدند اما هیچ کدام چاره ای نیافتند \n" +
            "در آن هنگام ابلیس در جامه ی پزشکی نزد ضحاک رفت و گفت چاره ی کار این است هر روز از مغز سر دو جوان برای مارها خورشت بپزند تا آنها آرام گیرند و به تو آزاری نرسانند. \n" +

            "چون جمشید شاه به بیراهه رفت و فره ایزدی از او دور شد بزرگان کشور از پیش او پراکنده شدند و در هر گوشه ی کشور گروهی سر به شورش برداشتند و سرانجام چنان شد که مردم به جستجوی پادشاهی دادگر رو به سوی تازیان کرده و به ضحاک پیوستند. \n " +
            "ضحّاک از طریق حیله و نیرنگ، با حمایت اهریمن، خود را به گونه‌ای جلوه داد که گویا می‌تواند آشوب را پایان دهد. مردم، گرفتار در تنگنای ناامنی و نابسامانی، به چشم امید به او نگریستند. او می‌توانست به شکل نمادین مارهایش را زیر جامه پنهان دارد یا مردم را از رویارویی مستقیم با این پدیده ترسان و مرعوب سازد. \n" +
            "ضحاک لشکری از ایرانیان و تازیان گرد آورد و جمشید شاه را شکست داد و پیروزمندانه وارد تخت جمشید شد. \n" +
            "ضحّاک، که حالا مدعی پادشاهی ایران بود، در پی آن برآمد که جمشید را یافته و نابود کند تا پایه‌های قدرت خویش را استوار سازد. وی لشکری فرستاد و جمشید شاه را که در گریز به سر می‌برد، پس از مدتی جستجو پیدا کرد. \n" +
            "شاه بخت برگشته ی ایران صد سال پنهان از همه در آوارگی و بی پناهی میزیست تا اینکه سرانجام به چنگ ضحاک افتاد و آن سلطان ماردوش وی را بی درنگ با اره به دو نیم کرد \n" +
            "در این مدت هر روز مغز دو جوان ایرانی خوراک مارهای دوش ضحاک می شد و از بیم مرگ همه ی مردم سر در گریبان فرو برده و خاموشی پیشه کرده بودند \n" +
            "هیچ کس نبود که به دادخواهی برخیزد مگر دو تن از ایرانیان آزادمرد که دل به دریا زده و چاره ای اندیشیدند. نام آنها ارمایل و گرمایل بود. آنها هنر آشپزی را یادگرفته بودند و توانستند به آشپزخانه دربار راه یابند \n" +
            "آنها هر شب که گماشتگان ضحاک دو جوان را به خورش خانه می آوردند تا مغزشان را خوراک مارها کنند یکی از آن دو جوان را مخفیانه آزاد می کردند و او را به بیرون از شهر میفرستادند. آنگاه به جای مغز او مغز سرگوسفندی را خوراک مارهای شاه میکردند. \n" +
            "40 سال از پادشاهی ضحاک گذشته بود که در خواب دید سه مرد جنگ آور از ایوان شاهی بیرون آمدند. آنکه از همه جوان تر از همه بود گرزی گاوسر به دست گرفته و فره ایزدی در چهره اش نمایان بود. \n" +
            "آن جوان ناگهان بر ضحاک تاخت و او را بر خاک انداخت و کشان کشان به کوه دماوند برد و در بند کرد " +
            "ضحاک هراسان از خواب برخواست و خواب گزاران و پیشگویان را از هر گوشه فراخواند و خوابش را برای ایشان گفت و آنان خواست که او را آینده خود آگاه کنند \n" +
            "پیشگویان سه روز از بیم شاه لب به سخن نگشودند. روز چهارم ضحاک برآشفت و به آنان گفت که اگر او را از آینده آگاه نکنند، همه را بر دار خواهد کرد. \n" +
            "دانایی به نام زیرک از آن میان برخاست و او را از آینده شومی که در انتظارش بود خبر داد و گفت . \n" +
            "پس از این، کسی پدید خواهد آمد که تخت پادشاهی تو را از آنِ خود سازد و تو را به خاک افکند. \n" +
            "او از مادری آکنده  از هنر و کمال زاده شود، همچون درختی بارور است. نامش فریدون است و او برای جهان چون آسمانِ فرخنده‌ای خواهد بود. او گرزِ گاوسر خود را بر سرت فرود خواهد آورد، تو را به بند خواهد کشید و از ایوان کاخت به کوچه خواهد کشاند. \n" +
            "شاه ماردوش با شگفتی پرسید آخر چرا؟ " +
            "مگر آفریدون چه دشمنی با من دارد که بخواهد مرا به بند کشد؟ " +
            "زیرک گفت دشمنی او با تو بی سبب نیست." +
            "او کینه پدر و دایه اش پرمایه را که در خردی او را با شیر خود می پرورد از تو خواهد گرفت. \n" +
            "ضحاک از این سخن بیهوش شد و از تخت شاهی فرو افتاد اما چون به هوش باز آمد، دستور داد تا از هر کجا که شده نشانه آفریدون را بجویند و پیش از آنکه او به دنیا بیاید و پرورده شود، نابودش کنند. \n" +
            "از سوی دیگر دور از چشم روز بانان ضحاک، فریدون چشم به جهان گشود. مادرش فرانک او را پنهانی برداشت و به مرغزاری گریخت. اما پدر فریدون - آبتین - به دست روزبانان گرفتار آمد و کشته شد. \n" +
            "" +
            "" +
            "" +
            ""
    },
    {
        "id": "abtn",
        "name": "آبتین",
        "nickname": "آبتین",
        "pos": "100 100",
        "imageProfile": "path/to/abtinProfile.jpg",
        "imageBg": "path/to/abtinBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "era_id": "dzhk",
        "family_id": "irn",
        "category_id": "mrdm",
        "description":
            " \n" +
            ""
    },
    {
        "id": "frnk",
        "name": "فرانک",
        "nickname": "فرانک",
        "pos": "100 100",
        "imageProfile": "path/to/faranakProfile.jpg",
        "imageBg": "path/to/faranakBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "era_id": "dzhk",
        "family_id": "irn",
        "category_id": "mrdm",
        "description":
            " \n" +
            ""
    },
    {
        "id": "frydn",
        "name": "فریدون",
        "nickname": "آفریدون",
        "pos": "10 180",
        "imageProfile": "path/to/fereydounProfile.jpg",
        "imageBg": "path/to/fereydounBg.jpg",
        "age": 1000,
        "gender": 1,
        "khvarenah": False,
        "era_id": "dfrydn",
        "family_id": "irn",
        "category_id": "pdsh",
        "description":
            " \n" +
            ""
    },
]

relationships_data = [
    {"myth1_id": "kmrs", "myth2_id": "simk", "relation_type": "prnt", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": "کیومرث فرزندش سیامک را به جنگ با اهریمن رهسپار می کند"
     },
    {"myth1_id": "ahrmn", "myth2_id": "kmrs", "relation_type": "enmy", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": " بعد از کشته شدن فرزندش به کین خواهی سیامک به نبرد اهریمن می رود"
     },
    {"myth1_id": "ahrmn", "myth2_id": "bdiv", "relation_type": "prnt", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": ""
     },
    {"myth1_id": "bdiv", "myth2_id": "simk", "relation_type": "enmy", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": "سیامک به جنگ بجه دیو می رود. ولی بچه دیو سیامک  را شکست داده و می کشد"
     },

    {"myth1_id": "srsh", "myth2_id": "simk", "relation_type": "frnd", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": "سروش آسمانی سیامک را از بد اندیشی بچه دیو آگاه می کند"
     },

    {"myth1_id": "simk", "myth2_id": "hshng", "relation_type": "prnt", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": ""
     },

    {"myth1_id": "hshng", "myth2_id": "dvsh", "relation_type": "enmy", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description":
        "بعد از کشته شدن پدرش، کیومرث از او در کارهای کشور یاری می جست و زمانی که سپاهی بزرگ از همه ی جانوران زمین فراهم شد کیومرث فرماندهی سپاه را به او داد و خود از پس سپاه رهسپار نبرد با اهریمن شد \n" +
        "جنگی بزرک میان آن ها در گرفت، سپاه هوشنگ پیروز شد و دیو سیاه بدست هوشنگ کشته شد"
     },

    {"myth1_id": "hshng", "myth2_id": "tmrs", "relation_type": "prnt", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": ""
     },

    {"myth1_id": "tmrs", "myth2_id": "shdsp", "relation_type": "empl", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": ""
     },

    {"myth1_id": "tmrs", "myth2_id": "jmshd", "relation_type": "prnt", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": ""
     },

    {"myth1_id": "mrds", "myth2_id": "zhk", "relation_type": "prnt", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": ""
     },

    {"myth1_id": "zhk", "myth2_id": "jmshd", "relation_type": "enmy", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description": ""
     },

    {"myth1_id": "zhk", "myth2_id": "jmshd", "relation_type": "frnd", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
     "description":
        "روزی ابلیس در برابر او نمایان شد و او را به کشتن پدرش - مرداس - فریب داد. \n" +
        "ضحاک پدرش را به چاهی ژرف انداخت و ابلیس به او گفت اگر از فرمان من سرپیچی نکنی تو را به پادشاهی سراسر گیتی خواهم رساند و تمام جانوران زمین به فرمان تو خواهند بود. . \n" +
        "دیگر بار ابلیس با چهره ی جوانی زیبا روی و سخندان درآورد و نزد ضحاک رفت و گفت من هنر آشپزی میدانم و اگر پادشاه بپذیرد می توانم هر روز خورش های خوشمزه بپزم. \n" +
        "در آن هنگام خوراک مردمان همه از سبزی و میوه و رستنی های دیگر بود و خوردن گوشت جانوران را کاری ناپسند می دانستند. \n" +
        "ابلیس برای اینکه ضحاک را به بیداد گری و خونریزی برانگیزد او را به گوشتخواری معتاد کرد. \n" +
        "ضحاک که از خوردن این غذاها بسیار خرسند بود از او خواست که هرچه می خواهد از شاه آرزو کند. \n" +
        "ابلیس چنین گفت که مهر شاه در دل اوست و دوست دارد که بر شانه های شاه بوسه زند. \n" +
        "ضحاک درخواست او را پذیرفت و پس از بوسه ی ابلیس بر شانه های ضحاک بی درنگ ابلیس ناپدید شد و دو مار سیاه بیرون آمدند \n" +
        "ضحاک بی درنگ سر آن دو مار را برید ولی آن دو مار چون شاخه ی درخت از کتف شاه بیرون آمدند. \n " +
        "همه ی پزشکان جمع شدند اما هیچ کدام چاره ای نیافتند \n" +
        "در آن هنگام ابلیس در جامه ی پزشکی نزد ضحاک رفت و گفت چاره ی کار این است هر روز از مغز سر دو جوان برای مارها خورشت بپزند تا آنها آرام گیرند و به تو آزاری نرسانند. \n" +
        ""
     },
    {"myth1_id": "abtn", "myth2_id": "frnk", "relation_type": "mrig", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
         "description": ""
     },
    {"myth1_id": "abtn", "myth2_id": "frydn", "relation_type": "prnt", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
         "description": ""
     },
    {"myth1_id": "frnk", "myth2_id": "frydn", "relation_type": "prnt", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
         "description": ""
     },

    {"myth1_id": "frydn", "myth2_id": "zhk", "relation_type": "enmy", "start_date": date(1000, 1, 1), "end_date": date(950, 1, 1), "relation_status": "active",
         "description": ""
     },
]

parent_child_data = [
    {"parent_id": 3, "child_id": 4, "relation_type": "biological", "color": "green"},
    {"parent_id": 1, "child_id": 5, "relation_type": "adoptive", "color": "purple"}
]


# Function to insert seed data into the database


def seed_data():
    # Insert Era data
    for era in eras_data:
        new_era = Era(id=era['id'], name=era['name'], oldName=era['oldName'], image=era['image'],
                      color=era['color'], description=era['description'])
        db.session.add(new_era)

    # Insert Category data
    for category in category_data:
        new_category = Category(id=category['id'], title=category['title'], imageProfile=category['imageProfile'],
                                imageBg=category['imageBg'], description=category['description'])
        db.session.add(new_category)

    # Insert Family data
    for family in family_data:
        new_family = Family(id=family['id'], title=family['title'], imageProfile=family['imageProfile'],
                            imageBg=family['imageBg'], description=family['description'])
        db.session.add(new_family)

    # Insert RelationType data
    for relation_type in relation_types_data:
        new_relation_type = RelationType(
            id=relation_type['id'],
            name=relation_type['name'],
            color=relation_type['color']
        )
        db.session.add(new_relation_type)

    # Insert Myth data
    for myth in myths_data:
        new_myth = Myth(id=myth['id'], name=myth['name'], nickname=myth['nickname'],
                        pos=myth['pos'], age=myth['age'], gender=myth['gender'],
                        era_id=myth['era_id'], category_id=myth['category_id'], family_id=myth['family_id'])
        db.session.add(new_myth)

    # Insert Relationship data
    for relationship in relationships_data:
        new_relationship = Relationship(
            myth1_id=relationship['myth1_id'],
            myth2_id=relationship['myth2_id'],
            relation_type=relationship['relation_type'],
            start_date=relationship['start_date'],
            end_date=relationship['end_date'],
            relation_status=relationship['relation_status'],
        )
        db.session.add(new_relationship)

    # Insert Parent-Child data
    # for parent_child in parent_child_data:
    #     new_parent_child = ParentChild(
    #         parent_id=parent_child['parent_id'],
    #         child_id=parent_child['child_id'],
    #         relation_type=parent_child['relation_type'],
    #         color=parent_child['color']
    #     )
    #     db.session.add(new_parent_child)

    # Commit the session to save data to the database
    db.session.commit()
    print("Seed data inserted successfully.")


# Run the seeding function if the DB is empty
if __name__ == "__main__":
    # Check if the DB is empty
    if db.session.query(Era).count() == 0:
        seed_data()
