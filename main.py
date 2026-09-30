from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy 



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:yourpassword@localhost/research_portal"
db = SQLAlchemy(app)


class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    area = db.Column(db.String(100), nullable=False)
    faculty_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(255))
    positions = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.String(20), nullable=False)  # or db.Date
    status = db.Column(db.String(10), default="Open")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "area": self.area,
            "faculty_name": self.faculty_name,
            "department": self.department,
            "skills": self.skills,
            "positions": self.positions,
            "deadline": self.deadline,
            "status": self.status,
        }
with app.app_context():
    db.create_all()
# create Database
@app.route("/")
def home():
    return jsonify({"message":"hello welcome hooooooome"})


@app.route("/api/opportunities",methods = ["GET"])
def get_opportunities():
    opportunities = Opportunity.query.all()

    return jsonify([opportunity.to_dict() for opportunity in opportunities])


@app.route("/api/opportunities",methods=["POST"])
def post_opportunities():
    data = request.get_json()
    new_opportunity = Opportunity(
        title=data["title"],
        description=data["description"],
        area=data["area"],
        faculty_name=data["faculty_name"],
        department=data["department"],
        skills=data.get("skills", ""),          
        positions=data["positions"],
        deadline=data["deadline"],
        status=data.get("status", "Open")
    )
    db.session.add(new_opportunity)
    db.session.commit()

    return jsonify(new_opportunity.to_dict()),201



if __name__ == "__main__":
    app.run(debug=True)