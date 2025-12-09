# Location - Logan Simba

**Course:** Database Systems - Phase 3  
**Date:** December 2025

---

## What I Built

### 1. Location API (Flask)
File: `backend/app.py`

| Endpoint | Description |
|----------|-------------|
| `GET /api/locations` | Get all venues |
| `GET /api/locations?zip=04101` | Filter by ZIP code |
| `GET /api/locations/<id>` | Get single venue |
| `GET /api/locations/city/<city>` | Filter by city |
| `POST /api/locations` | Add new venue |

### 2. Venues Page (React)
File: `frontend/app/locations/page.js`

- Displays 25 Maine venues
- Search and city filter
- URL: `http://localhost:3001/locations`

### 3. Database Indexes (Advanced Feature)
File: `tables_/location_table.sql`
```sql
CREATE INDEX idx_zip_code ON Location(zip_code);
CREATE INDEX idx_city ON Location(city);
CREATE INDEX idx_venue_name ON Location(venue_name);
```

Indexes make queries faster by using B-tree lookup instead of scanning all rows.

---

## How to Run

**Backend:**
```bash
cd backend
pip install flask flask-cors mysql-connector-python
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**View:**
- API: http://127.0.0.1:5000/api/locations
- Page: http://localhost:3001/locations

---

## Files

| File | What it does |
|------|--------------|
| `backend/app.py` | Location API endpoints |
| `frontend/app/locations/page.js` | Venues page |
| `tables_/location_table.sql` | Table + indexes |