from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models.deliverer import Deliverer


# Create : ajout d'un livreur
def create_deliverer(db: Session, deliverer_data: dict):
    deliverer_data = Deliverer(
        **deliverer_data
    )  # Transforme le dictionnaire en objet Deliverer
    db.add(deliverer_data)  # Prépare l'insertion
    db.commit()  # equivalent a INSERT INTO deliverers ... cad sauvegarde dans la base de données
    db.refresh(deliverer_data)  # Recharge l'objet pour avoir l'ID généré
    return deliverer_data


# READ : Lire un livreur par son ID
def get_deliverer_by_id(db: Session, deliverer_id: UUID):
    return db.query(Deliverer).filter(Deliverer.id == str(deliverer_id)).first()


# READ ALL : Liste des livreurs
def get_all_deliverers(db: Session):
    return db.query(Deliverer).all()


# UPDATE : Mettre à jour un livreur
def update_deliverer(db: Session, deliverer_id: UUID, update_data: dict):
    deliverer_obj = (
        db.query(Deliverer).filter(Deliverer.id == str(deliverer_id)).first()
    )

    if deliverer_obj:
        for key, value in update_data.items():
            setattr(deliverer_obj, key, value)
        db.commit()  # Sauvegarder les changements
        db.refresh(deliverer_obj)  # Recharger l'objet pour avoir les données à jour
    return deliverer_obj


# DELETE : Supprimer un livreur
def delete_deliverer(db: Session, deliverer_id: UUID):
    deliverer = db.query(Deliverer).filter(Deliverer.id == str(deliverer_id)).first()
    if deliverer:
        db.delete(deliverer)  # Supprimer l'objet de la session
        db.commit()  # Sauvegarder les changements
        return True  # Retourner succès après suppression
    return False  # Retourner échec si non trouvé
