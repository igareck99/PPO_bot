from app import app,db
import views
if __name__ == '__main__':
    app.run(port=5000,debug=True)