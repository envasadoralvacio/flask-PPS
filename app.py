from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect

from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__)

# configuración de la bd
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'pps'

#cadena de conexión
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

# configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

# configurar flask-wtf
app.config['SECRET_KEY']='llave9213123kasd.1231asd###'

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    #Listado de Personas
    #Regresa todos los objetos de tipo persona
    personas = Persona.query.all()
    # Cuenta todos los ojetos que hay
    total_personas = Persona.query.count()
    # Comprobamos por la terminal que está saliendo
    app.logger.debug(f'Listado Personas:{personas}')
    app.logger.debug(f'Total Personas:{total_personas}')
    # Renderiamos a un template
    return render_template('index.html', personas=personas, total_personas=total_personas)

@app.route('/persona/<int:id>')
def ver_detalle(id):
    #Recuperamos la persona según el id proporcionado
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona', (persona))
    return render_template('perfil.html', persona=persona)


# Mostrar el formulario -> GET
# Guardar los cambios en la BBDD -> POST
@app.route('/agregar', methods=['GET','POST'])
def agregar():
    # python -m pip install flask-wtf  // Para manejar mejor los formularios
    # Nuevo objeto de tipo persona
    persona = Persona()
    # Nueva clase de persona asociada al formulario, indicamos la clase de modelo que está asociada obj=persona.
    personaForm = PersonaForm(obj=persona)
    # Si hacemos POST es que estamos enviado el fomulario
    if request.method == 'POST':
        # Comprobamos si el formulario es correcto al enviarlo.
        if personaForm.validate_on_submit():
           # Método populate_obj indicamos cual es el objeto de tipo de modelo que queremos llenar
           personaForm.populate_obj(persona)
           # Comprobación
           app.logger.debug(f'Persona a insertar: {persona}')
           # Insertamos el nuevo registro con SQLAlchemy
           db.session.add(persona)
           db.session.commit()
           return redirect(url_for('inicio'))
    return render_template('agregar.html', forma = personaForm)


@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    #Recuperamos el objeto persona a editar
    persona = Persona.query.get_or_404(id)
    personaForma = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForma.validate_on_submit():
           personaForma.populate_obj(persona)
           app.logger.debug(f'Persona a actualizar: {persona}')
           db.session.commit()
        return redirect(url_for('inicio'))
    return render_template('editar.html', forma = personaForma)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Persona a eliminar: {persona}')
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('inicio'))