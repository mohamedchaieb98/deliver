# 💻 GUIDE PRATIQUE - Exemples de Code

## 🎯 Comment fonctionnent les appels backend-frontend

---

## 📋 Récapitulatif du flux par type de requête

### 1️⃣ LE PLUS SIMPLE: Afficher une liste (READ)

**Frontend React (DeliverersReal.tsx):**
```typescript
import React, { useState, useEffect } from 'react';
import { delivererAPI } from '../../services/api';

const DeliverersPage: React.FC = () => {
  const [deliverers, setDeliverers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 1️⃣ Déclenche au montage du composant
  useEffect(() => {
    fetchDeliverers();
  }, []);

  // 2️⃣ Fonction qui récupère les données
  const fetchDeliverers = async () => {
    try {
      setLoading(true);
      // 3️⃣ Appelle le service API
      const data = await delivererAPI.getAll();
      // 4️⃣ Met à jour le state React
      setDeliverers(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch deliverers');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // 5️⃣ Affiche les données dans le tableau
  return (
    <table>
      <tbody>
        {deliverers.map((deliverer) => (
          <tr key={deliverer.id}>
            <td>{deliverer.name}</td>
            <td>{deliverer.employee_id}</td>
            <td>{deliverer.territory}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DeliverersPage;
```

**Service API (src/services/api.ts):**
```typescript
// 1️⃣ Configuration de base
const API_BASE_URL = 'http://localhost:8000/api/v1';

// 2️⃣ Fonction générique de requête HTTP
async function apiCall(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  // URL complète: http://localhost:8000/api/v1/deliverers

  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const config = { ...defaultOptions, ...options };

  try {
    // 3️⃣ Envoie la requête HTTP
    const response = await fetch(url, config);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 4️⃣ Parse et retourne JSON
    return await response.json();
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error);
    throw error;
  }
}

// 5️⃣ Exports pour les composants
export const delivererAPI = {
  // GET: Récupère tous les livreurs
  getAll: () => apiCall('/deliverers'),

  // GET: Récupère un livreur par ID
  getById: (id: string) => apiCall(`/deliverers/${id}`),

  // POST: Crée un nouveau livreur
  create: (deliverer: any) =>
    apiCall('/deliverers', {
      method: 'POST',
      body: JSON.stringify(deliverer),
    }),

  // PUT: Modifie un livreur
  update: (id: string, deliverer: any) =>
    apiCall(`/deliverers/${id}`, {
      method: 'PUT',
      body: JSON.stringify(deliverer),
    }),

  // DELETE: Supprime un livreur
  delete: (id: string) =>
    apiCall(`/deliverers/${id}`, {
      method: 'DELETE',
    }),
};
```

**Backend - Point d'entrée (app/main.py):**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router

# 1️⃣ Crée l'application FastAPI
app = FastAPI(
    title="Water Delivery Management System",
    version="1.0.0"
)

# 2️⃣ Configure CORS pour accepter requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # ← Frontend autorisé
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],            # ← GET, POST, PUT, DELETE
    allow_headers=["*"],            # ← Tous les headers autorisés
)

# 3️⃣ Inclut les routes API
app.include_router(
    api_router,
    prefix="/api/v1"  # ← Toutes routes commencent par /api/v1
)

# 4️⃣ Route racine (optionnelle)
@app.get("/")
async def root():
    return {"message": "Water Delivery Management System API"}
```

**Backend - Routeur (app/api/v1/router.py):**
```python
from fastapi import APIRouter
from app.api.v1.endpoints import (
    deliverers,
    clients,
    orders,
    dashboard,
    # ... autres endpoints
)

# 1️⃣ Crée le routeur principal
api_router = APIRouter()

# 2️⃣ Enregistre chaque modulee sous une route
# GET /api/v1/deliverers → deliverers.router
api_router.include_router(
    deliverers.router,
    prefix="/deliverers",
    tags=["deliverers"]
)

# GET /api/v1/clients → clients.router
api_router.include_router(
    clients.router,
    prefix="/clients",
    tags=["clients"]
)

# ... autres
```

**Backend - Endpoint (app/api/v1/endpoints/deliverers.py):**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.deliverer import Deliverer
from app.schemas.deliverer import DelivererResponse

# 1️⃣ Crée un routeur local pour ce module
router = APIRouter()

# 2️⃣ Endpoint GET - Récupère tous les livreurs
@router.get("/", response_model=List[DelivererResponse])
def get_deliverers(
    skip: int = 0,              # Query param: ?skip=0
    limit: int = 100,          # Query param: ?limit=100
    db: Session = Depends(get_db)  # ← Injection de dépendance (BD)
):
    """
    Récupère tous les livreurs avec pagination

    - **skip**: Nombre de résultats à sauter
    - **limit**: Nombre maximum de résultats
    """
    # 3️⃣ Récupère session BD et exécute query
    query = db.query(Deliverer)
    deliverers = query.offset(skip).limit(limit).all()

    # 4️⃣ FastAPI sérialise automatiquement avec response_model
    return deliverers  # ← Converti en JSON via Pydantic


# 3️⃣ Endpoint GET par ID
@router.get("/{deliverer_id}", response_model=DelivererResponse)
def get_deliverer(deliverer_id: str, db: Session = Depends(get_db)):
    """Récupère un livreur spécifique"""
    deliverer = db.query(Deliverer).filter(
        Deliverer.id == deliverer_id
    ).first()

    if not deliverer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deliverer not found"
        )

    return deliverer


# 4️⃣ Endpoint POST - Crée un nouveau livreur
@router.post("/", response_model=DelivererResponse, status_code=201)
def create_deliverer(
    deliverer: DelivererCreate,      # ← Corps de la requête validé par Pydantic
    db: Session = Depends(get_db)
):
    """Crée un nouveau livreur"""

    # Vérifie si employee_id est unique
    existing = db.query(Deliverer).filter(
        Deliverer.employee_id == deliverer.employee_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee ID '{deliverer.employee_id}' already exists"
        )

    # Crée l'objet SQLAlchemy
    db_deliverer = Deliverer(**deliverer.dict())

    # Sauvegarde en BD
    db.add(db_deliverer)
    db.commit()
    db.refresh(db_deliverer)  # ← Récupère l'ID généré

    return db_deliverer


# 5️⃣ Endpoint PUT - Modifie un livreur
@router.put("/{deliverer_id}", response_model=DelivererResponse)
def update_deliverer(
    deliverer_id: str,
    deliverer: DelivererUpdate,  # ← Corps de la requête (champs optionnels)
    db: Session = Depends(get_db)
):
    """Modifie un livreur existant"""

    db_deliverer = db.query(Deliverer).filter(
        Deliverer.id == deliverer_id
    ).first()

    if not db_deliverer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deliverer not found"
        )

    # Met à jour seulement les champs fournis
    update_data = deliverer.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_deliverer, field, value)

    db.commit()
    db.refresh(db_deliverer)

    return db_deliverer


# 6️⃣ Endpoint DELETE - Supprime un livreur
@router.delete("/{deliverer_id}")
def delete_deliverer(deliverer_id: str, db: Session = Depends(get_db)):
    """Supprime un livreur"""

    db_deliverer = db.query(Deliverer).filter(
        Deliverer.id == deliverer_id
    ).first()

    if not db_deliverer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deliverer not found"
        )

    db.delete(db_deliverer)
    db.commit()

    return {"message": "Deliverer deleted successfully"}
```

**Schemas - Validation (app/schemas/deliverer.py):**
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 1️⃣ Schema de base (champs communs)
class DelivererBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    employee_id: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    territory: Optional[str] = Field(None, max_length=100)
    is_available: bool = True


# 2️⃣ Schema pour CREATE (pas d'ID, pas de created_at)
class DelivererCreate(DelivererBase):
    pass  # ← Hérite de DelivererBase


# 3️⃣ Schema pour UPDATE (tous les champs optionnels)
class DelivererUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    territory: Optional[str] = Field(None, max_length=100)
    is_available: Optional[bool] = None


# 4️⃣ Schema pour RESPONSE (avec métadonnées BD)
class DelivererResponse(DelivererBase):
    id: str                                    # ← ID généré
    created_at: datetime                       # ← Créé par BD
    updated_at: datetime                       # ← Mis à jour par BD

    class Config:
        from_attributes = True  # ← Accepte objets SQLAlchemy
```

**Modèle BD (app/models/deliverer.py):**
```python
from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

# 1️⃣ Classe représentant la table "deliverers"
class Deliverer(Base):
    __tablename__ = "deliverers"

    # 2️⃣ Colonnes
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    name = Column(String(200), nullable=False)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    territory = Column(String(100), nullable=True, index=True)
    is_available = Column(Boolean, default=True, index=True)
    vehicle_info = Column(JSON, nullable=True)  # ← Données complexes

    created_at = Column(
        DateTime,
        server_default=func.now()  # ← Auto-rempli par BD
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()  # ← Auto-mis à jour
    )
```

**Connexion BD (app/core/database.py):**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1️⃣ URL de connexion
DATABASE_URL = "sqlite:///./water_delivery.db"

# 2️⃣ Crée l'engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # ← Spécifique à SQLite
)

# 3️⃣ Classe de session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 4️⃣ Classe de base pour les modèles
Base = declarative_base()

# 5️⃣ Dépendance FastAPI - Injectée dans les endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db  # ← Fournit la session à l'endpoint
    finally:
        db.close()  # ← Ferme après réponse
```

---

## 📊 Exemple Complet: Créer un Livreur

### Le flux complet d'une création (CREATE - POST)

**1️⃣ Utilisateur remplit le formulaire en React:**
```typescript
const [formData, setFormData] = useState({
  name: '',
  employee_id: '',
  email: '',
  territory: '',
});

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  try {
    // Appelle l'API
    const newDeliverer = await delivererAPI.create(formData);

    // Ajoute à la liste
    setDeliverers([...deliverers, newDeliverer]);

    // Réinitialise le formulaire
    setFormData({
      name: '',
      employee_id: '',
      email: '',
      territory: '',
    });

    alert('Deliverer created successfully!');
  } catch (error) {
    alert('Error creating deliverer: ' + error.message);
  }
};
```

**2️⃣ Service API envoie POST HTTP:**
```typescript
// Dans src/services/api.ts
create: (deliverer: any) =>
  apiCall('/deliverers', {
    method: 'POST',
    body: JSON.stringify(deliverer),
  })

// Résultat:
// URL: http://localhost:8000/api/v1/deliverers
// Méthode: POST
// Corps: {
//   "name": "Karim",
//   "employee_id": "EMP004",
//   "email": "karim@company.com",
//   "territory": "East"
// }
```

**3️⃣ Backend reçoit et valide:**
```python
@router.post("/", response_model=DelivererResponse, status_code=201)
def create_deliverer(
    deliverer: DelivererCreate,  # ← Pydantic valide JSON
    db: Session = Depends(get_db)
):
    # Pydantic validation:
    # ✅ name: str - nonempty
    # ✅ employee_id: str - nonempty, unique
    # ✅ email: str - format email valide
    # ✅ territory: str - optional

    # Vérifie unicité
    existing = db.query(Deliverer).filter(
        Deliverer.employee_id == deliverer.employee_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists"
        )

    # Crée enregistrement
    db_deliverer = Deliverer(
        name=deliverer.name,
        employee_id=deliverer.employee_id,
        email=deliverer.email,
        territory=deliverer.territory,
        is_available=True
    )

    db.add(db_deliverer)
    db.commit()
    db.refresh(db_deliverer)  # ← Récupère ID généré

    return db_deliverer
```

**4️⃣ BD exécute INSERT:**
```sql
INSERT INTO deliverers
  (id, name, employee_id, email, territory, is_available, created_at, updated_at)
VALUES
  (
    'f47ac10b-58cc-4372-a567-0e02b2c3d479',
    'Karim',
    'EMP004',
    'karim@company.com',
    'East',
    true,
    '2025-02-14 15:35:00',
    '2025-02-14 15:35:00'
  );
```

**5️⃣ Backend retourne JSON:**
```json
HTTP/1.1 201 Created
Content-Type: application/json
Access-Control-Allow-Origin: http://localhost:3000

{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "Karim",
  "employee_id": "EMP004",
  "email": "karim@company.com",
  "phone_number": null,
  "territory": "East",
  "is_available": true,
  "created_at": "2025-02-14T15:35:00",
  "updated_at": "2025-02-14T15:35:00"
}
```

**6️⃣ Frontend reçoit et affiche:**
```typescript
const newDeliverer = {
  id: "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  name: "Karim",
  ...
};

setDeliverers([...deliverers, newDeliverer]);

// React re-render → Nouveau livreur dans le tableau ✅
```

---

## 🔍 Débogage: Comment voir le flux en action

### Terminal: Frontend
```bash
cd frontend
npm start
# Logs:
# > vite
# Local: http://localhost:3000
```

### Terminal: Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
# Logs:
# INFO: Started server process
# INFO: Uvicorn running on http://0.0.0.0:8000
# INFO: Application startup complete
```

### Navigateur: DevTools
```
F12 → Network → Colonne "All"

Cliquez sur un endpoint:
{
  "Request Method": "GET",
  "Request URL": "http://localhost:8000/api/v1/deliverers",
  "Status Code": "200",
  "Response Headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "http://localhost:3000"
  },
  "Response Body": [
    {
      "id": "...",
      "name": "Ahmed",
      ...
    }
  ]
}
```

### VSCode: Debug FastAPI
```python
# Dans vs code, ajouter breakpoint dans endpoints/deliverers.py:

@router.get("/", response_model=List[DelivererResponse])
def get_deliverers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    breakpoint()  # ← Pause ici lors de requête GET
    query = db.query(Deliverer)
    return query.offset(skip).limit(limit).all()
```

---

## 🎯 Points clés pour comprendre le flux

```
1. INITIATION
   ├─ Frontend: useEffect / onClick
   └─ Appelle: delivererAPI.getAll()

2. SERVICE API
   ├─ Frontend: src/services/api.ts
   └─ Crée: fetch(URL, options)

3. HTTP REQUEST
   ├─ Frontend → Backend
   └─ Contient: method, headers, body(optionnel)

4. CORS MIDDLEWARE
   ├─ Backend: app.add_middleware(CORSMiddleware)
   └─ Vérifie: Origin autorisée?

5. ROUTING
   ├─ main.py: include_router(prefix="/api/v1")
   ├─ router.py: include_router(prefix="/deliverers")
   └─ Pattern matching à l'endpoint

6. ENDPOINT HANDLER
   ├─ Logique métier
   ├─ Validation Pydantic
   └─ Dépendance BD: get_db()

7. SQLALCHEMY + BD
   ├─ ORM: db.query(Model)
   ├─ SQL: SELECT/INSERT/UPDATE/DELETE
   └─ SQLite: water_delivery.db

8. RESPONSE SCHEMA
   ├─ Pydantic: response_model
   └─ Sérialisation en JSON

9. HTTP RESPONSE
   ├─ Status: 200/201/404/etc
   ├─ Headers: Content-Type: application/json
   └─ Body: JSON

10. FRONTEND RECEIVE
    ├─ await response.json()
    ├─ setState(data)
    └─ Re-render UI ✅
```

---

## 📋 Tableau de tous les endpoints disponibles

| Fonc | Méthode | Route | Frontend | Backend | React |
|------|---------|-------|----------|---------|-------|
| Lire | GET | `/api/v1/deliverers` | `delivererAPI.getAll()` | `endpoints/deliverers.py` | `useState() + setDeliverers()` |
| Lire 1 | GET | `/api/v1/deliverers/{id}` | `delivererAPI.getById(id)` | `endpoints/deliverers.py` | `useParams()` |
| Créer | POST | `/api/v1/deliverers` | `delivererAPI.create(data)` | `endpoints/deliverers.py` | Form + `handleSubmit()` |
| Modifier | PUT | `/api/v1/deliverers/{id}` | `delivererAPI.update(id, data)` | `endpoints/deliverers.py` | Form + `handleUpdate()` |
| Supprimer | DELETE | `/api/v1/deliverers/{id}` | `delivererAPI.delete(id)` | `endpoints/deliverers.py` | `handleDelete()` |
| Stats | GET | `/api/v1/deliverers/stats/summary` | `delivererAPI.getStats()` | `endpoints/deliverers.py` | Dashboard |

---

## 🚀 Commandes utiles

### Démarrer tout
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm start

# Terminal 3: Visualiser BD (optionnel)
sqlite3 backend/water_delivery.db
```

### Tester les endpoints directement (curl)
```bash
# GET tous les livreurs
curl http://localhost:8000/api/v1/deliverers

# GET un livreur
curl http://localhost:8000/api/v1/deliverers/uuid-ici

# POST créer
curl -X POST http://localhost:8000/api/v1/deliverers \
  -H "Content-Type: application/json" \
  -d '{"name":"Karim","employee_id":"EMP004","territory":"East"}'

# PUT modifier
curl -X PUT http://localhost:8000/api/v1/deliverers/uuid-ici \
  -H "Content-Type: application/json" \
  -d '{"name":"Karim Updated","is_available":false}'

# DELETE supprimer
curl -X DELETE http://localhost:8000/api/v1/deliverers/uuid-ici
```

### Voir la BD dirente
```bash
sqlite3 backend/water_delivery.db

# Dans le prompt sqlite3:
sqlite> .tables
sqlite> SELECT * FROM deliverers;
sqlite> .exit
```

### Voir API documentation (Swagger)
```
http://localhost:8000/docs
http://localhost:8000/redoc
```
