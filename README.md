# University Research Opportunity Portal

A full-stack web application where faculty members can post, view, update, and manage research opportunities in one place, replacing scattered emails, WhatsApp groups, and noticeboards.

**Course:** Computer Networks (CN), BS (AI 5A), Fall 2026  
**Assignment:** No. 1  
**Author:** Muhammad Atif Khan, 24P-0540

**GitHub Repository:** https://github.com/M-Atif-ML/research-opportunity-portal

**Demo Video:** [add link here, or see `demo/` folder in the submission ZIP]

---

## Tech Stack

| Layer     | Technology                                   |
|-----------|----------------------------------------------|
| Backend   | Python, Flask, Flask-SQLAlchemy, Flask-CORS  |
| Database  | MySQL (accessed through PyMySQL)             |
| Frontend  | HTML, CSS, vanilla JavaScript (`fetch` API)  |
| API Tests | Postman                                      |

---

## Features

**Backend (REST API)**
- Full CRUD on research opportunities, stored in MySQL
- Input validation with clear `400 Bad Request` responses
- Proper HTTP status codes: `200`, `201`, `400`, `404`, `500`

**Frontend**
- Lists all opportunities, loaded live from the API (no hard-coded data)
- Detail view for any selected opportunity
- Create and edit through a form with required-field validation
- One-click status change between Open and Closed
- Delete with confirmation
- Success and error banners for every action
- Search by title/area and filter by status

---

## Project Structure

```
research-opportunity-portal/
├── main.py            # Flask app: model + all API routes
├── index.html         # Frontend (HTML + CSS + JS in one file)
├── schema.sql         # Database and table setup
├── requirements.txt   # Python dependencies
├── .env.example       # Template for local configuration
├── postman/           # Exported Postman collection (.json)
└── README.md
```

---

## Setup and Run

### Prerequisites
- Python 3.10 or newer
- MySQL Server 8.x
- A web browser

### 1. Clone the repository
```bash
git clone https://github.com/M-Atif-ML/research-opportunity-portal.git
cd research-opportunity-portal
```

### 2. Create the database
Open `schema.sql` and **change the password** on the `CREATE USER` line, then run:
```bash
sudo mysql < schema.sql
```
This creates the `research_portal` database, a dedicated `flaskuser` account, and the `opportunity` table.

### 3. Configure the connection
```bash
cp .env.example .env
```
Edit `.env` and set the same password you chose in step 2:
```
DATABASE_URL=mysql+pymysql://flaskuser:YOUR_PASSWORD@localhost/research_portal
```
`.env` is git-ignored, so your password is never committed.

### 4. Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Start the backend
```bash
python3 main.py
```
The API is now running at `http://127.0.0.1:5000`.

### 6. Open the frontend
Open `index.html` in your browser (double-click it, or `Ctrl+O` in the browser).

The frontend calls the API at `http://localhost:5000/api/opportunities`. If you run the backend on a different port, change the `API_BASE` constant near the top of the `<script>` tag in `index.html`.

---

## Data Model

Each research opportunity contains:

| Field          | Type            | Required | Notes                         |
|----------------|-----------------|----------|-------------------------------|
| `id`           | integer         | auto     | Unique ID, auto-generated     |
| `title`        | string (200)    | yes      | Research title                |
| `description`  | text            | yes      | Research description          |
| `area`         | string (100)    | yes      | Research area                 |
| `faculty_name` | string (100)    | yes      | Faculty member's name         |
| `department`   | string (100)    | yes      |                               |
| `skills`       | string (255)    | no       | Required skills               |
| `positions`    | integer         | yes      | Number of available positions |
| `deadline`     | string (YYYY-MM-DD) | yes  | Application deadline          |
| `status`       | `Open`/`Closed` | no       | Defaults to `Open`            |

---

## API Reference

Base URL: `http://127.0.0.1:5000`

| Method | Endpoint                   | Description                      | Success | Errors        |
|--------|----------------------------|----------------------------------|---------|---------------|
| POST   | `/api/opportunities`       | Create a new opportunity         | `201`   | `400`, `500`  |
| GET    | `/api/opportunities`       | Get all opportunities            | `200`   | `500`         |
| GET    | `/api/opportunities/<id>`  | Get one opportunity by ID        | `200`   | `404`         |
| PUT    | `/api/opportunities/<id>`  | Update an opportunity (partial updates allowed) | `200` | `404`, `500` |
| DELETE | `/api/opportunities/<id>`  | Delete an opportunity            | `200`   | `404`         |

### Example: create an opportunity

`POST /api/opportunities`
```json
{
  "title": "Machine Learning Research Assistant",
  "description": "Assist in developing deep learning models for medical image classification.",
  "area": "Machine Learning",
  "faculty_name": "Dr. Sara Ahmed",
  "department": "Computer Science",
  "skills": "Python, TensorFlow, PyTorch",
  "positions": 2,
  "deadline": "2026-11-15",
  "status": "Open"
}
```
Response `201 Created`: the same object plus its generated `id`.

### Example: close an opportunity

`PUT /api/opportunities/3`
```json
{ "status": "Closed" }
```
Only the fields you send are changed; everything else keeps its current value.

### Example error responses

Missing required field, `400 Bad Request`:
```json
{ "error": "Missing required fields: title" }
```

Unknown ID, `404 Not Found`:
```json
{ "error": "Can't Find the opportunity" }
```

---

## API Testing (Postman)

The exported collection is in the [`postman/`](postman/) folder. To use it: open Postman, **Import**, and select the `.json` file. Start the backend first.

The collection demonstrates:
1. Creating three research opportunities
2. Retrieving all opportunities
3. Retrieving one opportunity by ID
4. Updating an existing opportunity
5. Changing an opportunity's status from Open to Closed
6. Deleting an opportunity
7. Requesting the deleted opportunity again (`404 Not Found`)
8. Sending a request with missing data (`400 Bad Request`)

---

## Notes

- No credentials are stored in this repository. Database configuration is read from the git-ignored `.env` file.
- The database table is created automatically on first run (`db.create_all()`), and `schema.sql` provides the same structure for manual setup.
