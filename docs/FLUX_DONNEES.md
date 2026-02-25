# 📊 Flux de Circulation des Données - Frontend ↔ Backend

## 🎯 Vue d'ensemble

Votre application fonctionne selon l'architecture **Client-Serveur** avec:
- **Frontend** : React (TypeScript) sur `http://localhost:3000`
- **Backend** : FastAPI (Python) sur `http://localhost:8000`
- **Base de données** : SQLite

---

## 🔄 CIRCUIT COMPLET D'UNE REQUÊTE

### Exemple: Récupérer la liste des livreurs

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. FRONTEND (React) - Déclenchement de la demande              │
└─────────────────────────────────────────────────────────────────┘
   ↓
   📄 Fichier: src/pages/admin/DeliverersReal.tsx

   const [deliverers, setDeliverers] = useState<Deliverer[]>([]);

   useEffect(() => {
     fetchDeliverers();  // ← Appel au chargement du composant
   }, []);

   const fetchDeliverers = async () => {
     const data = await delivererAPI.getAll();  // ← Utilise le service API
     setDeliverers(data);  // ← Met à jour l'état React
   };

┌─────────────────────────────────────────────────────────────────┐
│ 2. SERVICE API (TypeScript) - Formation et envoi requête HTTP   │
└─────────────────────────────────────────────────────────────────┘
   ↓
   📄 Fichier: src/services/api.ts

   const API_BASE_URL = 'http://localhost:8000/api/v1';

   export const delivererAPI = {
     getAll: () => apiCall('/deliverers'),  // ← URL complète
   };

   async function apiCall(endpoint: string, options: RequestInit = {}) {
     const url = `${API_BASE_URL}${endpoint}`;
     // URL finale: http://localhost:8000/api/v1/deliverers

     const response = await fetch(url, config);
     return await response.json();
   }

┌─────────────────────────────────────────────────────────────────┐
│ 3. RÉSEAU HTTP - Transmission au serveur                        │
└─────────────────────────────────────────────────────────────────┘
   ↓
   🌐 Requête HTTP:
   GET http://localhost:8000/api/v1/deliverers HTTP/1.1
   Content-Type: application/json

┌─────────────────────────────────────────────────────────────────┐
│ 4. BACKEND FastAPI - Point d'entrée principal                   │
└─────────────────────────────────────────────────────────────────┘
   ↓
   📄 Fichier: app/main.py

   from fastapi import FastAPI
   from app.api.v1.router import api_router

   app = FastAPI()

   # Configuration CORS (autoriser requêtes depuis le frontend)
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_methods=["*"],
       allow_headers=["*"],
   )

   # Inclusion des routes API
   app.include_router(api_router, prefix="/api/v1")

┌─────────────────────────────────────────────────────────────────┐
│ 5. ROUTEUR API - Aiguillage vers les endpoints                  │
└─────────────────────────────────────────────────────────────────┘
   ↓
   📄 Fichier: app/api/v1/router.py

   api_router = APIRouter()
   api_router.include_router(deliverers.router, prefix="/deliverers")
   # Aiguille vers: app/api/v1/endpoints/deliverers.py

┌─────────────────────────────────────────────────────────────────┐
│ 6. ENDPOINT - Traitement de la requête                          │
└─────────────────────────────────────────────────────────────────┘
   ↓
   📄 Fichier: app/api/v1/endpoints/deliverers.py

   @router.get("/", response_model=List[DelivererResponse])
   def get_deliverers(
       skip: int = 0,
       limit: int = 100,
       active: Optional[bool] = None,
       territory: Optional[str] = None,
       db: Session = Depends(get_db)  # ← Injection de dépendance pour DB
   ):
       """Récupère tous les livreurs avec filtres optionnels"""

       query = db.query(Deliverer)

       if active is not None:
           query = query.filter(Deliverer.is_available == active)
       if territory:
           query = query.filter(Deliverer.territory == territory)

       deliverers = query.offset(skip).limit(limit).all()
       return deliverers  # ← Retourne la liste

┌─────────────────────────────────────────────────────────────────┐
│ 7. MODÈLE DE DONNÉES - Structure de la table SQL                │
└─────────────────────────────────────────────────────────────────┘
   ↓
   📄 Fichier: app/models/deliverer.py

   class Deliverer(Base):
       __tablename__ = "deliverers"

       id = Column(String(36), primary_key=True)
       name = Column(String(200), nullable=False)
       employee_id = Column(String(50), unique=True)
       email = Column(String(255))
       phone_number = Column(String(20))
       territory = Column(String(100), index=True)
       is_available = Column(Boolean, default=True)
       # ... autres champs
       created_at = Column(DateTime, server_default=func.now())
       updated_at = Column(DateTime)

┌─────────────────────────────────────────────────────────────────┐
│ 8. BASE DE DONNÉES - Récupération des données                   │
└─────────────────────────────────────────────────────────────────┘
   ↓
   💾 Fichier: water_delivery.db (SQLite)

   SELECT * FROM deliverers
   WHERE (is_available = ? OR is_available IS NULL)
   AND (territory = ? OR territory IS NULL)
   OFFSET 0 LIMIT 100;

┌─────────────────────────────────────────────────────────────────┐
│ 9. SCHÉMA PYDANTIC - Validation & transformation données         │
└─────────────────────────────────────────────────────────────────┘
   ↓
   📄 Fichier: app/schemas/deliverer.py

   class DelivererResponse(DelivererBase):
       id: str
       created_at: datetime
       updated_at: datetime
       current_location: Optional[str] = None

       class Config:
           from_attributes = True  # Convertit modèle SQLAlchemy → Pydantic

┌─────────────────────────────────────────────────────────────────┐
│ 10. RÉPONSE JSON - Sérialisation et transmission retour          │
└─────────────────────────────────────────────────────────────────┘
   ↓
   200 OK HTTP/1.1
   Content-Type: application/json

   [
     {
       "id": "uuid-1234",
       "name": "Ahmed",
       "employee_id": "EMP001",
       "email": "ahmed@example.com",
       "phone_number": "+212612345678",
       "territory": "Downtown",
       "is_available": true,
       "vehicle_info": {
         "make": "Toyota",
         "model": "Hiace",
         "plate_number": "ABC123"
       },
       "created_at": "2025-02-10T10:30:00",
       "updated_at": "2025-02-14T15:45:00"
     },
     ...
   ]

┌─────────────────────────────────────────────────────────────────┐
│ 11. FRONTEND - Réception et affichage données                   │
└─────────────────────────────────────────────────────────────────┘
   ↓
   ✅ Dans React:

   const data = await delivererAPI.getAll();  // ← Reçoit JSON
   setDeliverers(data);  // ← Met à jour state React

   ✅ L'interface affiche le tableau avec les données

```

---

## 🏗️ ARCHITECTURE EN COUCHES

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Composants UI (tsx)            [Affichage des données]    │ │
│  │ - DeliverersReal.tsx                                       │ │
│  │ - Dashboard.tsx                                            │ │
│  │ - Orders.tsx                                               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           ↓                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Services API (src/services/api.ts)  [Requêtes HTTP]       │ │
│  │ - delivererAPI.getAll()                                    │ │
│  │ - delivererAPI.create()                                    │ │
│  │ - delivererAPI.update()                                    │ │
│  │ - delivererAPI.delete()                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                          ↓ HTTP
                   ↓ JSON → ↑ JSON
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Point d'entrée (app/main.py)  [Configuration CORS]        │ │
│  │ - app = FastAPI()                                          │ │
│  │ - app.include_router(api_router, prefix="/api/v1")         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           ↓                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Routeur (app/api/v1/router.py)     [Aiguillage routes]    │ │
│  │ - include_router(deliverers)                               │ │
│  │ - include_router(clients)                                  │ │
│  │ - include_router(orders)                                   │ │
│  │ - include_router(...)                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           ↓                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Endpoints (app/api/v1/endpoints/)   [Logique métier]      │ │
│  │ - deliverers.py           [GET, POST, PUT, DELETE]        │ │
│  │ - clients.py                                               │ │
│  │ - orders.py                                                │ │
│  │ - ...                                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           ↓                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Schémas Pydantic (app/schemas/)     [Validation I/O]      │ │
│  │ - DelivererCreate (données à créer)                        │ │
│  │ - DelivererUpdate (données à modifier)                     │ │
│  │ - DelivererResponse (format réponse)                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           ↓                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Modèles (app/models/)               [Tables de BD]         │ │
│  │ - Deliverer (classe SQLAlchemy)                            │ │
│  │ - Client                                                   │ │
│  │ - Order                                                    │ │
│  │ - ...                                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           ↓                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Base de données (app/core/database.py) [Connexion BD]      │ │
│  │ - SQLite: water_delivery.db                                │ │
│  │ - SessionLocal (gestion des sessions)                      │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BASE DE DONNÉES                               │
│  💾 water_delivery.db (SQLite)                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Tables:                                                     │ │
│  │ - deliverers                                               │ │
│  │ - clients                                                  │ │
│  │ - orders                                                   │ │
│  │ - products                                                 │ │
│  │ - ...                                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 OPÉRATIONS CRUD COMPLÈTES

### ✅ **1. READ (Lecture) - GET**
```
Frontend → GET /api/v1/deliverers
Backend  → Query BD → JSON Response
Frontend → setDeliverers(data)
```

**Code Frontend:**
```typescript
const fetchDeliverers = async () => {
  const data = await delivererAPI.getAll();  // GET request
  setDeliverers(data);
};
```

**Code Backend:**
```python
@router.get("/", response_model=List[DelivererResponse])
def get_deliverers(db: Session = Depends(get_db)):
    deliverers = db.query(Deliverer).all()
    return deliverers  # Automatiquement convertie en JSON
```

---

### ✨ **2. CREATE (Création) - POST**
```
Frontend → POST /api/v1/deliverers {data}
Backend  → Valide (Pydantic) → Crée enregistrement → Retourne objet créé
Frontend → Reçoit nouvel objet avec ID
```

**Code Frontend:**
```typescript
const createDeliverer = (newDeliverer) => {
  return delivererAPI.create((newDeliverer);  // POST request
};

// Utilisation:
const newData = {
  name: "Mohamed",
  employee_id: "EMP002",
  territory: "North"
};
const created = await createDeliverer(newData);
```

**Code Backend:**
```python
@router.post("/", response_model=DelivererResponse)
def create_deliverer(
    deliverer: DelivererCreate,  # ← Pydantic valide les données
    db: Session = Depends(get_db)
):
    db_deliverer = Deliverer(**deliverer.dict())
    db.add(db_deliverer)
    db.commit()  # Sauvegarde en BD
    db.refresh(db_deliverer)  # Récupère l'ID généré
    return db_deliverer
```

**Flux Validation:**
```
JSON reçu → Pydantic valide les champs →
Si valide: crée instance SQLAlchemy →
Si invalide: retourne erreur 422
```

---

### 📝 **3. UPDATE (Modification) - PUT**
```
Frontend → PUT /api/v1/deliverers/{id} {data}
Backend  → Trouve enregistrement → Met à jour champs → Retourne modifié
Frontend → Reçoit objet mis à jour
```

**Code Frontend:**
```typescript
const updateDeliverer = (id, updatedData) => {
  return delivererAPI.update(id, updatedData);  // PUT request
};
```

**Code Backend:**
```python
@router.put("/{deliverer_id}", response_model=DelivererResponse)
def update_deliverer(
    deliverer_id: str,
    deliverer: DelivererUpdate,  # ← Champs optionnels
    db: Session = Depends(get_db)
):
    db_deliverer = db.query(Deliverer).filter(
        Deliverer.id == deliverer_id
    ).first()

    if not db_deliverer:
        raise HTTPException(status_code=404, detail="Not found")

    update_data = deliverer.dict(exclude_unset=True)  # Seulement champs modifiés
    for field, value in update_data.items():
        setattr(db_deliverer, field, value)  # Met à jour

    db.commit()
    db.refresh(db_deliverer)
    return db_deliverer
```

---

### 🗑️ **4. DELETE (Suppression) - DELETE**
```
Frontend → DELETE /api/v1/deliverers/{id}
Backend  → Trouve enregistrement → Supprime → Retourne confirmation
Frontend → Enlève de la liste
```

**Code Frontend:**
```typescript
const deleteDeliverer = (id) => {
  return delivererAPI.delete(id);  // DELETE request
};
```

**Code Backend:**
```python
@router.delete("/{deliverer_id}")
def delete_deliverer(deliverer_id: str, db: Session = Depends(get_db)):
    db_deliverer = db.query(Deliverer).filter(
        Deliverer.id == deliverer_id
    ).first()

    if not db_deliverer:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(db_deliverer)
    db.commit()
    return {"message": "Deliverer deleted successfully"}
```

---

## 🔐 FLUX DE SÉCURITÉ

### Configuration CORS (Cross-Origin Resource Sharing)
```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ← Autorise seulement le frontend
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE autorisés
    allow_headers=["*"],  # Tous les headers autorisés
)
```

**Cela signifie:**
- ✅ Requêtes depuis `http://localhost:3000` passent
- ❌ Requêtes depuis d'autres domaines sont bloquées
- ⚠️ Améliorer en production avec JWT, API Keys, etc.

---

## 📊 SCHÉMAS DE DONNÉES

### **Flux des Schémas:**

```
Frontend (TypeScript Interface)
    ↓
Service API (.getAll(), .create())
    ↓
HTTP JSON
    ↓
Backend Route Handler
    ↓
Pydantic Schema (Validation)
    ↓
SQLAlchemy Model (ORM)
    ↓
SQLite Table
    ↓
Requête SQL
    ↓
Résultats
    ↓
SQLAlchemy Model → Pydantic Response
    ↓
JSON
    ↓
Service API
    ↓
Frontend State (useState)
    ↓
Affichage UI
```

### **Exemple Livreal:**

```
Frontend:
type Deliverer = {
  id: string;
  name: string;
  employee_id: string;
  ...
}

Pydantic (Backend):
class DelivererCreate(BaseModel):
  name: str
  employee_id: str
  ...

class DelivererResponse(BaseModel):
  id: str
  name: str
  created_at: datetime
  ...

SQLAlchemy:
class Deliverer(Base):
  id = Column(String(36), primary_key=True)
  name = Column(String(200))
  ...

SQLite:
CREATE TABLE deliverers (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(200),
  ...
);
```

---

## ⚡ FLUX D'UNE REQUÊTE EN DÉTAIL

### **Exemple: Créer un livreur**

**1️⃣ Frontend déclenche l'action:**
```tsx
const handleCreateDeliverer = async (formData) => {
  try {
    const response = await delivererAPI.create(formData);
    setDeliverers([...deliverers, response]);
  } catch (error) {
    console.error(error);
  }
};
```

**2️⃣ Service API compose la requête:**
```typescript
create: (deliverer: any) => apiCall('/deliverers', {
  method: 'POST',
  body: JSON.stringify(deliverer),
  // Content-Type: application/json
})
```

**3️⃣ HTTP POST:**
```
POST http://localhost:8000/api/v1/deliverers HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Content-Length: 256

{
  "name": "Fatima",
  "employee_id": "EMP003",
  "email": "fatima@company.com",
  "phone_number": "+212612345679",
  "territory": "West",
  "is_available": true,
  "vehicle_info": {
    "make": "Mercedes",
    "model": "Sprinter"
  }
}
```

**4️⃣ FastAPI reçoit et valide:**
```
❶ Reçoit JSON brut
❷ Pydantic (DelivererCreate) valide:
   - name: string non-vide ✅
   - employee_id: string unique ✅
   - email: format valide ✅
❸ Crée instance Python
❸ Conversion en SQLAlchemy Deliverer
```

**5️⃣ Base de données:**
```sql
INSERT INTO deliverers
  (id, name, employee_id, email, phone_number, territory, is_available, vehicle_info, created_at)
VALUES
  ('uuid-1234-...', 'Fatima', 'EMP003', 'fatima@company.com',
   '+212612345679', 'West', true,
   '{"make": "Mercedes", "model": "Sprinter"}', '2025-02-14 15:30:00')
```

**6️⃣ Retour JSON avec ID généré:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Fatima",
  "employee_id": "EMP003",
  "email": "fatima@company.com",
  "phone_number": "+212612345679",
  "territory": "West",
  "is_available": true,
  "vehicle_info": {
    "make": "Mercedes",
    "model": "Sprinter"
  },
  "created_at": "2025-02-14T15:30:00",
  "updated_at": "2025-02-14T15:30:00"
}
```

**7️⃣ Frontend reçoit et affiche:**
```tsx
const response = { id: "550e...", name: "Fatima", ... }
setDeliverers([...deliverers, response]);
// Tableau rafraîchit automatic UI nouvelle ligne
```

---

## 🔧 CONFIGURATION RÉSEAU

### **Ports & Adresses:**

```
┌────────────────────────────────────────────┐
│  Frontend (React)                          │
│  URL: http://localhost:3000                │
│  Port: 3000 (Vite Dev Server)              │
└────────────────────────────────────────────┘
           ↓ HTTP Requests
     ↓ fetch() calls
┌────────────────────────────────────────────┐
│  Backend (FastAPI)                         │
│  URL: http://localhost:8000                │
│  Port: 8000 (Uvicorn Server)               │
│  API Base: /api/v1                         │
└────────────────────────────────────────────┘
           ↓ SQL Queries
┌────────────────────────────────────────────┐
│  Base de Données (SQLite)                  │
│  Fichier: ./water_delivery.db              │
│  Connexion: SQLite local (pas de port)    │
└────────────────────────────────────────────┘
```

---

## 📈 RÉSUMÉ CIRCUIT COMPLET

```
Utilisateur clique → handleClick() / useEffect()
    ↓
React state change → fetchData()
    ↓
delivererAPI.getAll() → apiCall()
    ↓
fetch() HTTP GET http://localhost:8000/api/v1/deliverers
    ↓
CORS validation ✅
    ↓
FastAPI main.py reçoit requête
    ↓
Router aiguille → endpoints/deliverers.py
    ↓
@router.get("/") handler exécutée
    ↓
Dépendance get_db() injectée → session BD
    ↓
db.query(Deliverer).all() → SELECT * FROM deliverers
    ↓
SQLAlchemy ORM → dictionnaires Python
    ↓
Pydantic response_model=List[DelivererResponse]
    ↓
Sérialisation JSON
    ↓
HTTP 200 Response [{ id, name, ... }, ...]
    ↓
fetch() parse JSON
    ↓
setDeliverers(data)
    ↓
React re-render composant
    ↓
utilisateur voit le tableau rempli ✅
```

---

## 🎯 POINTS CLÉS À RETENIR

1. **Frontend initie** : React composant déclenche requête via `delivererAPI`
2. **Service API intermédiaire** : `src/services/api.ts` gère toutes requêtes HTTP
3. **FastAPI réceptionne** : `app/main.py` configure l'app, CORS, routes
4. **Router aiguille** : `router.py` dirige vers endpoints
5. **Endpoint traite** : `endpoints/deliverers.py` logique métier
6. **Validation Pydantic** : Schémas vérifient données avant/après
7. **ORM SQLAlchemy** : Modèles SQL conversions Python/BD
8. **Base SQLite** : Stockage persistant données
9. **Réponse JSON** : Retour sérialisé vers frontend
10. **React actualise** : `useState` met à jour UI

---

## 🚀 Démarrage des serveurs

```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm start  # ou yarn dev pour Vite
# Accessible sur http://localhost:3000
```

---

## 📋 Requêtes HTTP Principales

| Méthode | Route | Fonction | Frontend |
|---------|-------|----------|----------|
| GET | `/deliverers` | Récupère tous | `delivererAPI.getAll()` |
| GET | `/deliverers/{id}` | Récupère un | `delivererAPI.getById(id)` |
| POST | `/deliverers` | Crée un | `delivererAPI.create(data)` |
| PUT | `/deliverers/{id}` | Modifie un | `delivererAPI.update(id, data)` |
| DELETE | `/deliverers/{id}` | Supprime un | `delivererAPI.delete(id)` |
| GET | `/dashboard/stats` | Stats | `dashboardAPI.getStats()` |
| GET | `/clients` | Clients | `clientAPI.getAll()` |
| GET | `/orders` | Commandes | `orderAPI.getAll()` |

Ce flux s'applique à tous les autres modèles (clients, orders, products, etc.)
