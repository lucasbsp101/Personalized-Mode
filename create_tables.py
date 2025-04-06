from personalized import app, db, Person

with app.app_context():
    db.create_all()
    print("✅ Tabela 'person' criada com sucesso!")