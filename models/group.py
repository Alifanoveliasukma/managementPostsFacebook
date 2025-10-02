from extensions import db

class Group(db.Model):
    __tablename__ = "groups"   # nama tabel di PostgreSQL

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    fb_group_id = db.Column(db.String(100), nullable=False, unique=True)
    rules = db.Column(db.Text)

    def to_dict(self):
        """Helper untuk mengubah object jadi dict (JSON friendly)."""
        return {
            "id": self.id,
            "name": self.name,
            "fb_group_id": self.fb_group_id,
            "rules": self.rules
        }
