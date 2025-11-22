# 🎮 PokéDex v1.0.1

A fast, secure Pokédex API & web interface built with FastAPI and MySQL.

## 🚀 Quick Start

### 1. Setup
```bash
pip install -r requirements.txt
mysql -u root -p < db.sql
```

### 2. Configure
Create `.env`:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=pokemons_db
```

### 3. Run
```bash
python run.py
# Visit http://localhost:8000
```

## 📡 API Endpoints

- `GET /api/total_pokemons` - List all Pokémon
- `GET /api/search?q=fire` - Search Pokémon
- `POST /api/add_pokemon/` - Add new Pokémon
- `GET /api/pokemon_stats` - Get statistics
- `GET /health` - Health check

## 📄 Pages

- `/` - Pokémon list
- `/pokemon/{name}` - Pokémon details
- `/add` - Add new Pokémon

## ✨ Features

✅ Fast async database operations (10x faster)  
✅ XSS protection & secure CORS  
✅ Complete request logging  
✅ Enhanced form validation  
✅ Fully documented API  

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn, MySQL
- **Frontend**: Bootstrap 5, Vanilla JS
- **Async**: run_in_threadpool for non-blocking DB

## 📁 Project Structure

```
PokéDex/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── database.py             # Async DB operations
│   ├── schemas.py              # Pydantic models
│   ├── controllers/
│   │   ├── api.py              # API controllers
│   │   └── views.py            # Page controllers
│   ├── routers/
│   │   ├── pokemon.py          # Pokemon routes
│   │   ├── views.py            # Page routes
│   │   └── health.py           # Health check
│   └── frontend/
│       ├── templates/          # HTML templates
│       │   ├── base.html
│       │   ├── index.html
│       │   ├── detail.html
│       │   └── add.html
│       └── static/
│           ├── css/            # Stylesheets
│           ├── js/             # JavaScript
│           │   ├── index.js
│           │   └── add.js
│           └── img/            # Images
├── run.py                      # Entry point
├── requirements.txt            # Dependencies
├── db.sql                      # Database schema
├── Dockerfile                  # Docker config
└── docker-compose.yml          # Docker Compose
```

## 🌍 Deploy

See `DEPLOYMENT.md` for:
- Docker setup
- Linux (Nginx + Supervisor)
- Heroku deployment
- Production configurations

## 📜 License

MIT

This project is open-source under the MIT license. See the **LICENSE** file for more information.

---

## 👨‍💻 Author

Developed by **Acinox** – Full-stack developer and student, passionate about modular, secure, and maintainable systems.

---

**Version**: 1.0.1 | **Status**: ✅ Production Ready