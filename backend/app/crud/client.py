from sqlalchemy.orm import Session

from app.models.client import Client


# Create : ajout d'un client
def create_client(db: Session, client_data: dict):
    client_data = Client(**client_data)  # Transforme le dictionnaire en objet Client
    db.add(client_data)  # Prépare l'insertion
    db.commit()  # equivalent a INSERT INTO clients ... cad sauvegarde dans la base de données
    db.refresh(client_data)  # Recharge l'objet pour avoir l'ID généré
    return client_data


# READ : Lire un client par son ID
def get_client_by_id(db: Session, client_id):
    # On s'assure que client_id est bien une string pour la comparaison SQLite
    return db.query(Client).filter(Client.id == str(client_id)).first()


# READ ALL : Liste des clients
def get_all_clients(db: Session):
    return db.query(Client).all()


# READ ALL : Liste des clients actifs
def get_active_clients(db: Session, skip: int = 0, limit: int = 12):
    return (
        db.query(Client)
        .filter(Client.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


# UPDATE : Mettre à jour un client
def update_client(db: Session, client_id, update_data: dict):
    client_obj = db.query(Client).filter(Client.id == str(client_id)).first()

    if client_obj:
        for key, value in update_data.items():
            setattr(client_obj, key, value)
        db.commit()
        db.refresh(client_obj)
    return client_obj


# DELETE (soft delete) : Supprimer un client (cad désactiver au lieu de supprimer directement)
def delete_client(db: Session, client_id):
    client = db.query(Client).filter(Client.id == str(client_id)).first()
    if client:
        client.is_active = False  # Désactiver le client au lieu de le supprimer
        db.commit()  # Sauvegarder les changements
        db.refresh(client)  # Recharger l'objet pour avoir les données à jour
    return client
