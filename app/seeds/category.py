from app import create_app, db
from app.model.category_schema import CategorySchema

def category_seeds():
    app = create_app()

    with app.app_context():
        category_data = [
            CategorySchema(name="其他"), # 9
            CategorySchema(name="教育與課程"), # 1
            CategorySchema(name="音樂與表演"), # 2
            CategorySchema(name="藝術與文化"), # 3
            CategorySchema(name="商業與科技"), # 4
            CategorySchema(name="體育與健身"), # 5
            CategorySchema(name="社交與興趣"), # 6
            CategorySchema(name="慈善與公益"), # 7
            CategorySchema(name="健康與生活"), # 8
        ]

        db.session.add_all(category_data)
        db.session.commit()
        print("Category seeds added!")
        
if __name__ == '__main__':
    category_seeds()