# 🔄 DIAGRAMMES VISUELS - Circuit Données

## 1️⃣ ARCHITECTURE COMPLÈTE

```
╔══════════════════════════════════════╗
║                                      ║
║   🖥️ NAVIGATEUR (Utilisateur)        ║
║                                      ║
╚════════════════┬═════════════════════╝
                 │ http://localhost:3000
                 ▼
╔══════════════════════════════════════════════════════════════════╗
║                    FRONTEND (React/TypeScript)                   ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │ 📄 Pages (Admin, Mobile)                                 │   ║
║  │ • Deliverers.tsx (affiche liste livreurs)               │   ║
║  │ • Dashboard.tsx  (affiche stats)                        │   ║
║  │ • Orders.tsx     (affiche commandes)                    │   ║
║  │                                                           │   ║
║  │ 🔧 Composants                                            │   ║
║  │ • Layout      (mise en page)                             │   ║
║  │ • Tables      (affichage données)                        │   ║
║  │ • Formulaires (création/modification)                   │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                          │                                       ║
║                          ▼                                       ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │ 📡 SERVICE API (src/services/api.ts)                    │   ║
║  │                                                           │   ║
║  │ const apiCall = async (endpoint, options) => {          │   ║
║  │    const url = API_BASE_URL + endpoint                  │   ║
║  │    return fetch(url, options).then(r => r.json())       │   ║
║  │ }                                                         │   ║
║  │                                                           │   ║
║  │ export delivererAPI = {                                 │   ║
║  │    getAll: () => apiCall('/deliverers')                │   ║
║  │    create: (d) => apiCall('/deliverers', POST)         │   ║
║  │    update: (id, d) => apiCall(`/deliverers/${id}`, PUT)│   ║
║  │    delete: (id) => apiCall(`/deliverers/${id}`, DELETE)│   ║
║  │ }                                                         │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                          │                                       ║
║                          │ HTTP Request                          ║
║                          │ JSON payload                          ║
║                          │ Content-Type: application/json        ║
║                          ▼                                       ║
║                                                                   ║
╚═══════════════════════════╤════════════════════════════════════╝
                            │
                            │ INTERNET / LOCALHOST
                            │
                            ▼
╔═══════════════════════════╤════════════════════════════════════╗
║                           │                                     ║
║   BACKEND (FastAPI/Python)                                     ║
║                           │                                     ║
║                           ▼                                     ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │ 🚀 POINT D'ENTRÉE: app/main.py                          │  ║
║  │                                                           │  ║
║  │ from fastapi import FastAPI                             │  ║
║  │ app = FastAPI()                                         │  ║
║  │                                                           │  ║
║  │ ⚙️  Configuration CORS:                                  │  ║
║  │   allow_origins = ["http://localhost:3000"]             │  ║
║  │   ✅ Autorise frontend à faire requêtes                 │  ║
║  │                                                           │  ║
║  │ app.include_router(api_router, prefix="/api/v1")        │  ║
║  │ ↓ Dirige vers            ↓                              │  ║
║  └──────────────────────────────────────────────────────────┘  ║
║                           │                                     ║
║                           ▼                                     ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │ 🔀 ROUTEUR: app/api/v1/router.py                        │  ║
║  │                                                           │  ║
║  │ api_router = APIRouter()                                │  ║
║  │                                                           │  ║
║  │ include_router(deliverers.router, prefix="/deliverers") │  ║
║  │ include_router(clients.router, prefix="/clients")       │  ║
║  │ include_router(orders.router, prefix="/orders")         │  ║
║  │ include_router(dashboard.router, prefix="/dashboard")   │  ║
║  │ ...                                                       │  ║
║  │                                                           │  ║
║  │ Route: GET /deliverers                                  │  ║
║  │ ↓ Saute à → endpoints/deliverers.py                    │  ║
║  └──────────────────────────────────────────────────────────┘  ║
║                           │                                     ║
║                           ▼                                     ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │ 📍 ENDPOINT: app/api/v1/endpoints/deliverers.py        │  ║
║  │                                                           │  ║
║  │ @router.get("/", response_model=List[DelivererResponse])│  ║
║  │ def get_deliverers(                                     │  ║
║  │     skip: int = 0,                                      │  ║
║  │     limit: int = 100,                                   │  ║
║  │     db: Session = Depends(get_db)  ← BD injection       │  ║
║  │ ):                                                       │  ║
║  │     query = db.query(Deliverer)                         │  ║
║  │     return query.offset(skip).limit(limit).all()        │  ║
║  │                                                           │  ║
║  │ Validation: Pydantic schemas/deliverer.py               │  ║
║  │ • DelivererCreate   (création)                          │  ║
║  │ • DelivererUpdate   (modification)                      │  ║
║  │ • DelivererResponse (réponse)                           │  ║
║  └──────────────────────────────────────────────────────────┘  ║
║                           │                                     ║
║                           ▼                                     ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │ 🗂️  ORM/MODÈLES: app/models/deliverer.py              │  ║
║  │                                                           │  ║
║  │ class Deliverer(Base):                                  │  ║
║  │     __tablename__ = "deliverers"                        │  ║
║  │                                                           │  ║
║  │     id = Column(String(36), primary_key=True)           │  ║
║  │     name = Column(String(200))                          │  ║
║  │     employee_id = Column(String(50), unique=True)       │  ║
║  │     email = Column(String(255))                         │  ║
║  │     phone_number = Column(String(20))                   │  ║
║  │     territory = Column(String(100))                     │  ║
║  │     is_available = Column(Boolean, default=True)        │  ║
║  │     created_at = Column(DateTime, default=now())        │  ║
║  │     updated_at = Column(DateTime, onupdate=now())       │  ║
║  │                                                           │  ║
║  │ ← Représente table "deliverers" en BD                  │  ║
║  └──────────────────────────────────────────────────────────┘  ║
║                           │                                     ║
║                           ▼                                     ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │ 💾 BD CONNECTION: app/core/database.py                 │  ║
║  │                                                           │  ║
║  │ DATABASE_URL = "sqlite:///./water_delivery.db"          │  ║
║  │ engine = create_engine(DATABASE_URL)                    │  ║
║  │ SessionLocal = sessionmaker(bind=engine)                │  ║
║  │                                                           │  ║
║  │ def get_db():  ← Utilisée dans endpoints via Depends()  │  ║
║  │     db = SessionLocal()                                 │  ║
║  │     yield db                                            │  ║
║  │     db.close()                                          │  ║
║  └──────────────────────────────────────────────────────────┘  ║
║                           │                                     ║
║                           ▼                                     ║
║                                                                  ║
╚═══════════════════════════╤══════════════════════════════════╝
                            │
                            ▼
        ╔════════════════════════════════════════╗
        ║                                        ║
        ║  💾 SQLITE BASE DE DONNÉES             ║
        ║  (water_delivery.db)                   ║
        ║                                        ║
        ║  Table: deliverers                     ║
        ║  ┌──────────────────────────────────┐  ║
        ║  │ id    | name   | employee_id ... │  ║
        ║  ├───────┼────────┼─────────────────┤  ║
        ║  │ uuid1 | Ahmed  | EMP001    ...  │  ║
        ║  │ uuid2 | Fatima | EMP002    ...  │  ║
        ║  │ uuid3 | Mohamed| EMP003    ...  │  ║
        ║  └──────────────────────────────────┘  ║
        ║                                        ║
        ║  Tables: clients, orders, products ... ║
        ║                                        ║
        ╚════════════════════════════════════════╝
```

---

## 2️⃣ FLUX DÉTAILLÉ D'UNE REQUÊTE GET

```
┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 1: Utilisateur interagit avec UI                         │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  👤 Utilisateur clique sur "Deliverers" menu                  │
│                                                                 │
│          ↓                                                      │
│                                                                 │
│  React composant monte: DeliverersPage                        │
│                                                                 │
│  useEffect(() => {                                            │
│    fetchDeliverers();  ← Exécuté au chargement               │
│  }, [])                                                        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 2: React appelle le service API                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  const fetchDeliverers = async () => {                        │
│    setLoading(true);                                          │
│                                                                 │
│    const data = await delivererAPI.getAll();                 │
│       ↓                                                         │
│       Appelle fonction dans src/services/api.ts               │
│                                                                 │
│    setDeliverers(data);  ← Update React state                │
│    setLoading(false);                                         │
│  }                                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 3: Service API compose requête HTTP                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  // src/services/api.ts                                       │
│                                                                 │
│  const API_BASE_URL = 'http://localhost:8000/api/v1'         │
│                                                                 │
│  export const delivererAPI = {                                │
│    getAll: () => apiCall('/deliverers')                      │
│  };                                                             │
│                                                                 │
│  async function apiCall(endpoint, options = {}) {            │
│    const url = `${API_BASE_URL}${endpoint}`;                 │
│    // url = 'http://localhost:8000/api/v1/deliverers'        │
│                                                                 │
│    const response = await fetch(url, {                      │
│      headers: { 'Content-Type': 'application/json' }        │
│    });                                                         │
│    return await response.json();                              │
│  }                                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 4: Requête HTTP transmise au réseau                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GET /api/v1/deliverers HTTP/1.1                             │
│  Host: localhost:8000                                          │
│  Content-Type: application/json                                │
│  Accept: application/json                                      │
│  User-Agent: Mozilla/5.0 ...                                   │
│  Origin: http://localhost:3000  ← CORS check                  │
│                                                                 │
│  [Vide - GET n'a pas de corps]                                │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 5: Backend reçoit requête - CORS validation              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ Middleware CORS vérifie:                                  │
│     Origin: http://localhost:3000                              │
│     ← Est dans allow_origins? OUI ✅                          │
│                                                                 │
│     Method: GET                                                │
│     ← Est dans allow_methods? OUI ✅ ("*")                   │
│                                                                 │
│     Headers: Content-Type, Accept                              │
│     ← Sont dans allow_headers? OUI ✅ ("*")                  │
│                                                                 │
│  ✅ Requête autorisée, continue processing                    │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 6: FastAPI main app reçoit et route requête              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  # app/main.py                                                 │
│                                                                 │
│  app = FastAPI()                                               │
│  app.include_router(api_router, prefix="/api/v1")             │
│                                                                 │
│  Matching route: GET /api/v1/deliverers                       │
│         ↓                                                       │
│  Enlève prefix "/api/v1" → /deliverers                        │
│         ↓                                                       │
│  Trouve dans router: deliverers.router                        │
│         ↓                                                       │
│  Pattern matching: GET / correspond!                          │
│         ↓                                                       │
│  Appelle endpoint handler                                      │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 7: Endpoint exécute logique métier                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  # app/api/v1/endpoints/deliverers.py                         │
│                                                                 │
│  @router.get("/", response_model=List[DelivererResponse])    │
│  def get_deliverers(                                          │
│      skip: int = 0,         ← Query param ?skip=0             │
│      limit: int = 100,      ← Query param ?limit=100          │
│      active: Optional[bool] = None,                           │
│      territory: Optional[str] = None,                         │
│      db: Session = Depends(get_db)  ← Injection BD           │
│  ):                                                             │
│      query = db.query(Deliverer)                              │
│                                                                 │
│      if active is not None:                                   │
│          query = query.filter(Deliverer.is_available == active)│
│                                                                 │
│      if territory:                                            │
│          query = query.filter(Deliverer.territory == territory)│
│                                                                 │
│      deliverers = query.offset(skip).limit(limit).all()      │
│      # ← Retourne liste de Deliverer ORM objects             │
│      return deliverers                                        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 8: Injection dépendance - Get DB session                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  # app/core/database.py                                       │
│                                                                 │
│  def get_db():                                                 │
│      db = SessionLocal()  ← Crée session SQLAlchemy          │
│      try:                                                      │
│          yield db        ← Passe session au endpoint         │
│      finally:                                                  │
│          db.close()      ← Ferme après execution             │
│                                                                 │
│  Session connectée à: sqlite:///./water_delivery.db           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 9: Query BD - SQLAlchemy exécute query                   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  db.query(Deliverer)                                           │
│  .offset(0)                                                    │
│  .limit(100)                                                   │
│  .all()                                                        │
│                                                                 │
│  ↓ Traduit en SQL:                                             │
│                                                                 │
│  SELECT id, name, employee_id, email, phone_number,           │
│         territory, is_available, vehicle_info,                │
│         hire_date, current_location, last_location_update,   │
│         created_at, updated_at                                │
│  FROM deliverers                                              │
│  LIMIT 100 OFFSET 0;                                          │
│                                                                 │
│  ↓ SQLite exécute et retourne:                                │
│                                                                 │
│  [                                                              │
│    (1, "Ahmed", "EMP001", "ahmed@...", ...),                 │
│    (2, "Fatima", "EMP002", "fatima@...", ...),               │
│    (3, "Mohamed", "EMP003", "mohamed@...", ...)              │
│  ]                                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 10: Conversion ORM → Pydantic (Response Schema)          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SQLAlchemy Deliverer objects                                 │
│         ↓                                                      │
│  response_model=List[DelivererResponse]                       │
│         ↓                                                      │
│  Pydantic validation & serialization:                         │
│                                                                 │
│  class DelivererResponse(BaseModel):                          │
│      id: str                 ✅ Valide                        │
│      name: str               ✅ Valide                        │
│      employee_id: str        ✅ Valide                        │
│      email: Optional[str]    ✅ Valide                        │
│      phone_number: ...       ✅ Valide                        │
│      territory: ...          ✅ Valide                        │
│      is_available: bool      ✅ Valide                        │
│      vehicle_info: Optional  ✅ Valide                        │
│      created_at: datetime    ✅ Valide                        │
│      updated_at: datetime    ✅ Valide                        │
│                                                                 │
│      class Config:                                             │
│          from_attributes = True  ← SQLAlchemy→Pydantic       │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 11: Sérialisation JSON & HTTP Response                   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  JSON encoding (FastAPI auto):                                │
│                                                                 │
│  HTTP/1.1 200 OK                                               │
│  Content-Type: application/json                                │
│  Content-Length: 2450                                          │
│  Access-Control-Allow-Origin: http://localhost:3000           │
│  Date: Mon, 14 Feb 2026 15:30:45 GMT                          │
│                                                                 │
│  [                                                              │
│    {                                                            │
│      "id": "550e8400-e29b-41d4-a716-446655440000",            │
│      "name": "Ahmed",                                          │
│      "employee_id": "EMP001",                                 │
│      "email": "ahmed@company.com",                            │
│      "phone_number": "+212612345678",                         │
│      "territory": "Downtown",                                 │
│      "is_available": true,                                    │
│      "vehicle_info": {                                        │
│        "make": "Toyota",                                      │
│        "model": "Hiace",                                      │
│        "plate_number": "ABC123"                               │
│      },                                                        │
│      "hire_date": "2024-01-15",                              │
│      "current_location": null,                                │
│      "last_location_update": null,                            │
│      "created_at": "2025-02-10T10:30:00",                    │
│      "updated_at": "2025-02-14T15:45:00"                     │
│    },                                                          │
│    {                                                            │
│      "id": "660e8400-e29b-41d4-a716-446655440001",            │
│      "name": "Fatima",                                        │
│      ...                                                       │
│    }                                                            │
│  ]                                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 12: Réseau transmet réponse JSON au frontend             │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HTTP 200 avec JSON body transmis au navigateur                │
│                                                                 │
│  [La réponse traverse le réseau localhost]                    │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 13: Frontend reçoit et parse JSON                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  const response = await delivererAPI.getAll();               │
│  ↓                                                             │
│  fetch retourne response avec status 200 ✅                   │
│  ↓                                                             │
│  await response.json() parse JSON                              │
│  ↓                                                             │
│  data = [                                                      │
│    { id: "550e...", name: "Ahmed", ... },                    │
│    { id: "660e...", name: "Fatima", ... },                   │
│    ...                                                         │
│  ]                                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 14: React met à jour état et UI                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  const fetchDeliverers = async () => {                        │
│    setLoading(true);                                          │
│                                                                 │
│    try {                                                       │
│      const data = await delivererAPI.getAll();               │
│      setDeliverers(data);        ← Met à jour state           │
│      setError(null);                                          │
│    } catch (err) {                                            │
│      setError('Failed to fetch ...');                         │
│    } finally {                                                │
│      setLoading(false);         ← Arrête loading spinner      │
│    }                                                            │
│  }                                                              │
│                                                                 │
│  ↓ Déclenche re-render du composant:                          │
│                                                                 │
│  return (                                                      │
│    <div>                                                       │
│      <table>                                                   │
│        <tbody>                                                 │
│          {deliverers.map(d => (                               │
│            <tr key={d.id}>                                    │
│              <td>{d.name}</td>                                │
│              <td>{d.employee_id}</td>                         │
│              <td>{d.territory}</td>                           │
│              ...                                              │
│            </tr>                                              │
│          ))}                                                   │
│        </tbody>                                                │
│      </table>                                                  │
│    </div>                                                      │
│  )                                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
                           ↓

┌────────────────────────────────────────────────────────────────┐
│ ÉTAPE 15: Utilisateur voit résultat ✅                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ Deliverers                   [Add Deliverer]        │     │
│  ├─────────────────────────────────────────────────────┤     │
│  │ Deliverer │ Contact          │ Territory   │ Status│     │
│  ├───────────┼──────────────────┼─────────────┼───────┤     │
│  │ Ahmed     │ +212612345678    │ Downtown    │ ✅    │     │
│  │ Fatima    │ fatima@comp.com  │ West        │ ✅    │     │
│  │ Mohamed   │ +212612345679    │ North       │ ✅    │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                                 │
│  ✅ CYCLE COMPLET TERMINÉ!                                   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 3️⃣ FLUX D'UNE REQUÊTE POST (Création)

```
User Input                HTTP Request              Backend Processing           Database              Response
─────────────            ──────────────            ──────────────────           ────────             ────────

Formulaire rempli         POST /deliverers
│                         {
│                           "name": "Karim",
│                           "employee_id": "EMP004",
│                           "territory": "East",
│                           "is_available": true
│                         }
│                                          ↓
│                                    CORS Check ✅
│                                          ↓
│                                    FastAPI main.py
│                                          ↓
│                                    Router.include_router
│                                          ↓
│                                    endpoint: POST /
│                                          ↓
│                                    Pydantic Validate
│                                    DelivererCreate
│                                          ↓
│                                    Check email_id unique? ✅
│                                          ↓
│                                    Create SQLAlchemy object
│                                          ↓
│                                    db.add(instance)         INSERT INTO deliverers
│                                          ↓               (name, employee_id...)
│                                    db.commit()             VALUES (...)
│                                          ↓                        ↓
│                                    db.refresh                  ✅ Enregistrement créé
│                                    (get generated id)              ↓
│                                          ↓               id = uuid auto-generated
│                                    DelivererResponse
│                                    serialization
│                                          ↓
│                                    HTTP 201
                                    {id, name, created_at...}    ← Reply
│
└── setDeliverers([...old, new])
    Re-render tableau
    Nouvelle ligne apparaît
```

---

## 4️⃣ FLUX COMPLET CRUD

```
╔════════════════════╗
║    UTILISATEUR     ║
║   (Navigateur)     ║
╚════════════════════╝
        │
        ├─────────────────────────────────────────────────────┬──────────────────┬──────────────────┐
        │                                                     │                  │                  │
        ▼                                                     ▼                  ▼                  ▼
   ┌─────────┐                                         ┌───────────┐      ┌────────────┐      ┌─────────┐
   │  R E A D │                                         │  CREATE   │      │   UPDATE   │      │  DELETE │
   │ (GET)    │                                         │ (POST)    │      │   (PUT)    │      │ (DEL)   │
   └─────────┘                                         └───────────┘      └────────────┘      └─────────┘
        │                                                     │                  │                  │
        │ delivererAPI.getAll()                              │ create({...})    │ update(id, {...})  │ delete(id)
        │                                                     │                  │                  │
        ▼                                                     ▼                  ▼                  ▼
   fetch GET                                           fetch POST            fetch PUT          fetch DEL
   /deliverers                                         /deliverers           /deliverers/{id}   /deliverers/{id}
        │                                              body: JSON            body: JSON              │
        │                                                    │                  │                  │
        └────────────────────────────────┬───────────────────┴──────────────────┴──────────────────┘
                                         │
                                         ▼
                            ┌───────────────────────────┐
                            │   CORS Middleware         │
                            │   (VALIDATION)            │
                            │ allow_origins = [":3000"] │
                            │ ✅ PASS                   │
                            └────────┬──────────────────┘
                                     │
                                     ▼
                            ┌──────────────────────┐
                            │  FastAPI main.py     │
                            │  CORSMiddleware      │
                            │  include_router      │
                            └────────┬─────────────┘
                                     │
                                     ▼
                            ┌──────────────────────┐
                            │  Router.py           │
                            │  Route matching      │
                            └────────┬─────────────┘
                                     │
                ┌────────────────────┼────────────────────┬──────────────────┐
                │                    │                    │                  │
                ▼                    ▼                    ▼                  ▼
           GET /              POST /               PUT /{id}            DELETE /{id}
           endpoint           endpoint             endpoint             endpoint
                │                    │                    │                  │
                ▼                    ▼                    ▼                  ▼
         db.query().all()  Validate Pydantic   Find by ID +        Find by ID +
                           Create new ORM      Update fields       db.delete()
                           db.add()
                           db.commit()
                │                    │                    │                  │
                └────────────────────┼────────────────────┼──────────────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │  SQLAlchemy ORM        │
                        │  Conversion Python/SQL │
                        └────────┬───────────────┘
                                 │
                                 ▼
                        ┌────────────────────────┐
                        │  SQLite Database       │
                        │  water_delivery.db     │
                        │                        │
                        │  SELECT / INSERT /     │
                        │  UPDATE / DELETE       │
                        │                        │
                        │  deliverers table      │
                        └────────┬───────────────┘
                                 │
                ┌────────────────┼────────────────┬──────────────────┐
                │                │                │                  │
                ▼                ▼                ▼                  ▼
         List records      New record         Updated record    Null/empty
         [{...}, {...}]    {id, ...}          {id, ...}         {}
                │                │                │                  │
                └────────────────┼────────────────┼──────────────────┘
                                 │
                                 ▼
                        ┌────────────────────────┐
                        │  Pydantic Response     │
                        │  Schema Serialization  │
                        └────────┬───────────────┘
                                 │
                                 ▼
                        ┌────────────────────────┐
                        │  JSON Encoding         │
                        │  HTTP 200/201/204      │
                        └────────┬───────────────┘
                                 │
                                 ▼
                        ┌────────────────────────┐
                        │  HTTP Response body    │
                        │  Content-Type: JSON    │
                        │  CORS Headers          │
                        └────────┬───────────────┘
                                 │
                ┌────────────────┼────────────────┬──────────────────┐
                │                │                │                  │
                ▼                ▼                ▼                  ▼
         JSON array         JSON object      JSON object        JSON message
         [d1, d2, ...]      {id, name...}    {id, name...}      {"message": "..."}
                │                │                │                  │
                └────────────────┼────────────────┼──────────────────┘
                                 │
                                 ▼
                        ┌────────────────────────┐
                        │  Frontend receive      │
                        │  await response.json() │
                        └────────┬───────────────┘
                                 │
                ┌────────────────┼────────────────┬──────────────────┐
                │                │                │                  │
                ▼                ▼                ▼                  ▼
         setDeliverers    data = {...}       Update in state    Remove from state
         (data)           setDeliverers      setDeliverers      setDeliverers
                         ([...old, data])    (updated_list)     (filtered_list)
                │                │                │                  │
                └────────────────┼────────────────┼──────────────────┘
                                 │
                                 ▼
                        ┌────────────────────────┐
                        │  React Re-render       │
                        │  Tableau mis à jour    │
                        └────────┬───────────────┘
                                 │
                                 ▼
                        ┌────────────────────────┐
                        │  📊 Affichage UI       │
                        │  Utilisateur voit      │
                        │  les changements ✅    │
                        └────────────────────────┘
```

---

## 5️⃣ STRUCTURE RÉPERTOIRES

```
deliver/
│
├── 📄 docker-compose.yml  (Configuration multi-container)
├── 📄 README.md
│
├── 🖥️ FRONTEND/
│   ├── 📦 package.json
│   ├── 📄 tailwind.config.js
│   ├── 📄 postcss.config.js
│   │
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   │
│   └── src/
│       ├── 📄 index.tsx  (Point d'entrée React)
│       ├── 📄 App.tsx    (Composant racine)
│       │
│       ├── services/
│       │   └── 🔌 api.ts  ← Service HTTP (POINT CLÉ)
│       │
│       ├── pages/
│       │   ├── admin/
│       │   │   ├── DeliverersReal.tsx  ← Page livreurs
│       │   │   ├── Deliverers.tsx
│       │   │   ├── Dashboard.tsx
│       │   │   ├── Orders.tsx
│       │   │   └── ...
│       │   │
│       │   └── mobile/
│       │       ├── Expenses.tsx
│       │       └── Route.tsx
│       │
│       ├── components/
│       │   └── Layout/
│       │       ├── AdminLayout.tsx
│       │       └── Layout.tsx
│       │
│       └── utils/
│           └── deviceDetection.ts
│
│
├── 🐍 BACKEND/
│   ├── 📦 requirements.txt
│   ├── 📄 Dockerfile
│   ├── 📄 alembic.ini  (DB migrations)
│   ├── 📄 create_tables.py
│   │
│   ├── 📁 uploads/
│   │   └── [Fichiers uploadés]
│   │
│   ├── 📁 migrations/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 0bd716fbaf60_create_all_tables.py
│   │
│   └── app/
│       │
│       ├── 📄 main.py  ← Point d'entrée FastAPI (POINT CLÉ)
│       │
│       ├── core/
│       │   ├── 📄 config.py        (Settings)
│       │   └── 📄 database.py      (DB connexion - POINT CLÉ)
│       │
│       ├── api/
│       │   └── v1/
│       │       ├── 📄 router.py            (Aiguillage routes - POINT CLÉ)
│       │       │
│       │       └── endpoints/  ← Logique métier
│       │           ├── 📄 deliverers.py   ← GET/POST/PUT/DELETE livreurs
│       │           ├── 📄 clients.py
│       │           ├── 📄 orders.py
│       │           ├── 📄 products.py
│       │           ├── 📄 dashboard.py
│       │           ├── 📄 routes.py
│       │           ├── 📄 inventory.py
│       │           ├── 📄 expenses.py
│       │           ├── 📄 payments.py
│       │           ├── 📄 suppliers.py
│       │           ├── 📄 resellers.py
│       │           └── 📄 deliverers_old.py
│       │
│       ├── models/  ← ORM SQLAlchemy (POINT CLÉ)
│       │   ├── 📄 deliverer.py    (Table deliverers)
│       │   ├── 📄 client.py        (Table clients)
│       │   ├── 📄 common.py        (Champs communs)
│       │   └── 📄 __init__.py
│       │
│       ├── schemas/  ← Validation Pydantic (POINT CLÉ)
│       │   ├── 📄 deliverer.py    (DelivererCreate, Update, Response)
│       │   ├── 📄 client.py
│       │   └── 📄 __init__.py
│       │
│       ├── crud/
│       │   ├── 📄 client.py       (Opérations BD si needed)
│       │   └── 📄 __init__.py
│       │
│       └── routes/
│           └── 📄 client.py
│
├── 💾 water_delivery.db  (Base SQLite - Données)
│
└── 📁 docs/
    ├── 📄 project-overview.md
    ├── 📄 api-specification.md
    ├── 📄 database-schema.md
    ├── 📄 user-stories.md
    ├── 📄 implementation-roadmap.md
    ├── 📄 system-changes-summary.md
    ├── 📄 uml-diagrams.md
    └── 📄 FLUX_DONNEES.md  ← Ce document!
```

---

## 6️⃣ Flux Services API - Tous les endpoints disponibles

```
Frontend API Call              → HTTP Method                   → Backend Endpoint              → BD Query
─────────────────            ─────────────────               ──────────────────             ─────────

delivererAPI.getAll()         GET /api/v1/deliverers          /endpoints/deliverers.py        SELECT * FROM deliverers
delivererAPI.getById(id)      GET /api/v1/deliverers/{id}     /endpoints/deliverers.py        SELECT * FROM deliverers WHERE id=?
delivererAPI.create(data)     POST /api/v1/deliverers         /endpoints/deliverers.py        INSERT INTO deliverers VALUES(...)
delivererAPI.update(id,d)     PUT /api/v1/deliverers/{id}     /endpoints/deliverers.py        UPDATE deliverers SET ... WHERE id=?
delivererAPI.delete(id)       DELETE /api/v1/deliverers/{id}  /endpoints/deliverers.py        DELETE FROM deliverers WHERE id=?
delivererAPI.getStats()       GET /api/v1/deliverers/stats/summary  /endpoints/deliverers.py  SELECT COUNT(*), ...

dashboardAPI.getStats()       GET /api/v1/dashboard/stats     /endpoints/dashboard.py         SELECT COUNT(*), SUM(...) ...

clientAPI.getAll()            GET /api/v1/clients             /endpoints/clients.py           SELECT * FROM clients
clientAPI.create(d)           POST /api/v1/clients            /endpoints/clients.py           INSERT INTO clients ...

orderAPI.getAll()             GET /api/v1/orders              /endpoints/orders.py            SELECT * FROM orders
orderAPI.create(d)            POST /api/v1/orders             /endpoints/orders.py            INSERT INTO orders ...

inventoryAPI.getAll()         GET /api/v1/inventory           /endpoints/inventory.py         SELECT * FROM inventory
```
