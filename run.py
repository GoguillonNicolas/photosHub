from photohub import app, db
import click

@app.cli.command("create-db")
def create_db():
    """Crée les tables de la base de données."""
    with app.app_context():
        db.create_all()
    click.echo("Base de données initialisée.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
