from modules.repositorio_concreto import RepositorioReclamosSQLAlchemy, RepositorioUsuariosSQLAlchemy
from modules.config import db

def crear_repositorio():
    repo_reclamo = RepositorioReclamosSQLAlchemy(db.session)  #pasan db.session
    repo_usuario = RepositorioUsuariosSQLAlchemy(db.session)
    return repo_reclamo, repo_usuario