from App import create_app, db
from App.models import User, Book
from werkzeug.security import generate_password_hash
from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # admin user with Werkzeug hash
    admin_pw = generate_password_hash("BookStore@223")
    admin = User(username="admin", email="BookStoreAdmin@.com", is_admin=True)
    admin.set_password_raw_hash(admin_pw)  
    db.session.add(admin)

    
    books = [
        Book(title="A Little Life", author="Hanya Yanagihara", publication="Doubleday & Co Inc.", publication_date=date(2015, 3, 10), language="English",reading_age="16+", price=250.0, piece=10, image_file="little.png",
             ISBN="978-0385539258", content="NEW YORK TIMES BESTSELLER • A stunning “portrait of the enduring grace of friendship” (NPR)  "\
               "about the families we are born into, and those that we make for ourselves. A masterful depiction of love in the twenty-first century."),


        Book(title="The Things We Leave Unfinished", author="Rebecca Yarros", publication="Penguin (Transworld)", publication_date=date(2022, 11, 24), language="English",reading_age="16+", price=450.0, piece=15, image_file="Things.png",
             ISBN="978-1804992326", content="When Georgia Stanton discovers that her late grandmother, Scarlett, the infamous romance author," \
             " didn't get the chance to finish her last book, she is determined to share her story. But first, it needs to be written. Enter Noah Harrison," \
             "the bestselling and most charismatic romance author of his generation. When Georgia meets him, she is distraught - athough he's charming and handsome," \
             "there's nothing beneath the surface. But as they start working together, Georgia begins to see that there might be more to Noah than meets the eye. Together,"\
             "they realize that Scarlett was saving the greatest love story of all until last - her own. While serving in World War Two, she fell in love with the handsome and enigmatic pilot,"\
             "Jameson. But are Georgia and Noah about to discover that not all love stories have a happy ending...?"),


        Book(title="Forgiving What You Can't Forget", author="Lysa TerKeurst", publication="Thomas Nelson Publishers", publication_date=date(2020,11,17), language="English",reading_age="16+", price=300.0, piece=8, image_file="You.png",
             ISBN="978-1400225194", content="Have you ever felt stuck in a cycle of unresolved pain, playing offenses over and over in your mind?" \
             "You know you can't go on like this, but you don't know what to do next. Lysa TerKeurst has wrestled through this journey. " \
             "But in surprising ways, she’s discovered how to let go of bound-up resentment and overcome the resistance to forgiving people who aren’t willing to make things right."),

             
        Book(title="The 100", author="Kass Morgan", publication=" Little, Brown & Company", publication_date=date(2017,1,3), language="English",reading_age="16+", price=700.0, piece=12, image_file="100.png",
             ISBN="978-0316551366", content=" Ever since nuclear war destroyed our planet, humanity has been living on city-like spaceships hovering" \
             " above the toxic surface. As far as anyone knows, no one has stepped foot on Earth in centuries--that is," \
             " until one hundred juvenile delinquents are sentenced to return and recolonize the hostile land." \
             " The future of the human race rests in their hands, but nothing can prepare the 100 for what they find on this" \
             " strange and savage planet." \
             "Don't miss the book series that inspired the hit TV show. New York Times bestseller The 100, Day 21, Homecoming, and" \
             " Rebellion are gathered together for the first time in this striking box set, perfect for fans and series newcomers alike."),
          
        Book(title="Believe In Yourself", author="Dr Joseph Murphy", publication="True Sign Publishing House Private Limited", publication_date=date(2023,7,6), language="English",reading_age="16+", price=150.0, piece=5, image_file="believe.png",
             ISBN="978-9358058796", content="Believe in Yourself by Joseph Murphy is a motivational book that empowers readers to embrace their inner potential"\
               "and cultivate a positive mindset for success. Through a combination of inspiring stories, practical techniques, and transformative"),

        Book(title="The Long Walk", author="Stephen King", publication="Gallery Books", publication_date=date(2016,2,1), language="English",reading_age="16+", price=170.0, piece=4, image_file="king.png",
             ISBN="978-1501144264", content="In this #1 national bestseller, master storyteller (Houston Chronicle) Stephen King, writing as Richard Bachman,"\
              "tells the tale of the contestants of a grueling walking competition where there can only be one winner--the one that survives"),

        Book(title="The Mamba Mentality", author="Kobe Bryant", publication="Farrar, Straus & Giroux Inc", publication_date=date(2020,2,28), language="English",reading_age="16+", price=220.0, piece=12, image_file="alchemist.jpg",
             ISBN="978-0374201234", content="The Mamba Mentality: How I Play is Kobe Bryant's personal perspective of his life and career on the basketball court and his exceptional," \
             " insightful style of playing the game--a fitting legacy from the late Los Angeles Laker superstar. In the wake of his retirement from professional basketball," \
             " 'Kobe The Black Mamba' Bryant decided to share his vast knowledge and understanding of the game to take readers on an unprecedented journey to the core of the legendary 'Mamba mentality." \
             " Citing an obligation and an opportunity to teach young players, hardcore fans, and devoted students of the game how to play it the right way," \
             " The Mamba Mentality takes us inside the mind of one of the most intelligent, analytical, and creative basketball players ever. In his own words," \
             " Bryant reveals his famously detailed approach and the steps he took to prepare mentally and physically to not just succeed at the game, but to excel." \
             " Readers will learn how Bryant studied an opponent, how he channeled his passion for the game, how he played through injuries. They'll also get fascinating granular" \
             " detail as he breaks down specific plays and match-ups from throughout his career. Bryant's detailed accounts are paired with stunning photographs by the Hall of Fame photographer" \
             " Andrew D. Bernstein. Bernstein, long the Lakers and NBA official photographer, captured Bryant's very first NBA photo in 1996 and his last in 2016--and hundreds of thousands in between," \
             "the record of a unique, twenty-year relationship between one athlete and one photographer. The combination of Bryant's narrative and Bernstein's photos make The Mamba Mentality an unprecedented" \
             " look behind the curtain at the career of one of the world's most celebrated and fascinating athletes."),

    ]
    db.session.add_all(books)
    db.session.commit()
    print("Database seeded successfully!")
