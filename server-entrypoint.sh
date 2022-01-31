python migrate_db.py;
gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn-conf.py server:app;
