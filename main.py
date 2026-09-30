from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://flaskuser:atif123@localhost/research_portal"

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

    required = ["title", "description", "area", "faculty_name", "department", "positions", "deadline"]
    missing = [f for f in required if f not in data or data[f] in (None, "")]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400



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

@app.route("/api/opportunities/<int:opp_id>",methods = ["PUT"])
def edit_opportinities(opp_id):
    opportunity = Opportunity.query.get(opp_id)

    if not opportunity:
        return jsonify({"Error":"Can't Find the opportunity"}),404
    
    data = request.get_json()
    try:
        opportunity.title = data.get("title", opportunity.title)
        opportunity.description = data.get("description", opportunity.description)
        opportunity.area = data.get("area", opportunity.area)
        opportunity.faculty_name = data.get("faculty_name", opportunity.faculty_name)
        opportunity.department = data.get("department", opportunity.department)
        opportunity.skills = data.get("skills", opportunity.skills)
        opportunity.positions = data.get("positions", opportunity.positions)
        opportunity.deadline = data.get("deadline", opportunity.deadline)
        opportunity.status = data.get("status", opportunity.status)

        db.session.commit()
        return jsonify(opportunity.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),500


@app.route("/api/opportunities/<int:opt_id>", methods=["GET"])
def get_by_id(opt_id):
    opportunity = Opportunity.query.get(opt_id)

    if opportunity:
        return jsonify(opportunity.to_dict())
    else:
        return jsonify({"Error":"Opps i think you didnt gave me the correct id number"}),404
    
@app.route("/api/opportunities/<int:opt_id>",methods = ["DELETE"])
def delete_opportunity(opt_id):
    opportunity = Opportunity.query.get(opt_id)

    if opportunity:
        db.session.delete(opportunity)
        db.session.commit()
        return jsonify({"message":f"Opportunity with id {opt_id} is deleted"})
    else:
        return jsonify({"Error":f"Can't find the opportunity having id = {opt_id}"}), 404





if __name__ == "__main__":
    app.run(debug=True)