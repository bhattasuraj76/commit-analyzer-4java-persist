flask --app  app/models/crud.py db migrate -m "Initial migration"
export FLASK_APP=main.py
export FLASK_ENV=development
export FLASK_DEBUG=1

After running query, sqlalchemy result could be attached of one the mentioned methods
https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result

return jsonify(repositories = [item.to_json() for item in repositories])