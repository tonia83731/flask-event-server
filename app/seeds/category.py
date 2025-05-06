from app import create_app, db
from app.model.category_schema import CategorySchema

def category_seeds():
    app = create_app()

    with app.app_context():
        category_data = [
            CategorySchema(name="教育與課程", code="education"), # 1
            CategorySchema(name="音樂與表演", code="music"), # 2
            CategorySchema(name="藝術與文化", code="art_culture"), # 3
            CategorySchema(name="商業與科技", code="business_tech"), # 4
            CategorySchema(name="體育與健身", code="sports_fitness"), # 5
            CategorySchema(name="社交與興趣", code="social_hobby"), # 6
            CategorySchema(name="慈善與公益", code="charity"), # 7
            CategorySchema(name="健康與生活", code="wellness"), # 8
            CategorySchema(name="其他", code="OTH"), # 9
        ]

        db.session.add_all(category_data)
        db.session.commit()
        print("Category seeds added!")
        
if __name__ == '__main__':
    category_seeds()