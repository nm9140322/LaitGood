# 後台設定

from app_LaitGood import db

# 行銷活動：全館運費、滿額免運、全館打折、買一送多
class SaleActivity(db.Model):
    __tablename__='LaitGood_Saleactivity'
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(10), nullable=False)
    activity_on = db.Column(db.Boolean)
    activity_dataset = db.Column(db.Integer)
    activity_intro = db.Column(db.String(30))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f'可選用之相關行銷活動：{ self.activity_name }'
