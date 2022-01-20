from app import db

class Persona(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    apellidos = db.Column(db.String(250))
    email = db.Column(db.String(250))

    def __str__(self):
        return (
            f'ID: {self.id}'
            f'Nombre: {self.nombre}'
            f'Apellidos: {self.apellidos}'
            f'Email: {self.email}'
        )