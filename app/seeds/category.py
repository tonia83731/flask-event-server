from app import create_app, db
from app.model.category_schema import CategorySchema

def category_seeds():
    app = create_app()

    with app.app_context():
        category_data = [
            CategorySchema(name="教育與課程", code="education"),
            CategorySchema(name="音樂與表演", code="music"),
            CategorySchema(name="藝術與文化", code="art_culture"),
            CategorySchema(name="商業與科技", code="business_tech"),
            CategorySchema(name="體育與健身", code="sports_fitness"),
            CategorySchema(name="社交與興趣", code="social_hobby"),
            CategorySchema(name="慈善與公益", code="charity"),
            CategorySchema(name="健康與生活", code="wellness"),
            CategorySchema(name="其他", code="OTH"),
        ]

        db.session.add_all(category_data)
        db.session.commit()
        print("Category seeds added!")
        
if __name__ == '__main__':
    category_seeds()