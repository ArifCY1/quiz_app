from app import app
from models import db, Quiz

with app.app_context():
    db.create_all()

    if Quiz.query.count() == 0:  
        questions = [
            Quiz(
                question="Discord.py kütüphanesi ne için kullanılır?",
                option_a="Veri analizi için",
                option_b="Discord botları geliştirmek için",
                option_c="Web sitesi oluşturmak için",
                option_d="Görüntü işleme için",
                correct_answer="B"
            ),
            Quiz(
                question="Flask uygulamasında bir URL'ye karşılık gelen işlev nasıl tanımlanır?",
                option_a="@flask.route",
                option_b="@app.route",
                option_c="@route.app",
                option_d="@flask.path",
                correct_answer="B"
            ),
            Quiz(
                question="Yapay zeka modellerini eğitmek için en çok kullanılan kütüphanelerden biri nedir?",
                option_a="NumPy",
                option_b="OpenCV",
                option_c="TensorFlow",
                option_d="Requests",
                correct_answer="C"
            ),
            Quiz(
                question="Computer Vision uygulamalarında hangi Python kütüphanesi yaygın kullanılır?",
                option_a="ImageAI",
                option_b="Pillow",
                option_c="Selenium",
                option_d="PyQt",
                correct_answer="A"
            ),
            Quiz(
                question="Doğal Dil İşleme (NLP) uygulamalarında NLTK kütüphanesi ne işe yarar?",
                option_a="Veritabanı yönetimi için",
                option_b="Metin verilerini analiz etmek için",
                option_c="Görüntü işlemek için",
                option_d="Sunucu barındırmak için",
                correct_answer="B"
            )
        ]

        db.session.bulk_save_objects(questions)
        db.session.commit()
        print("Sınav soruları başarıyla eklendi.")
    else:
        print("Sorular zaten veritabanında mevcut.")
