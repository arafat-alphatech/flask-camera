from api_model import *
from api_field import *

# Resource yang berhubungan dengan login
class Admin_Login_Resources(Resource):
    # method yang digunakan guru untuk login
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username",location='json',required=True)
        parser.add_argument("password",location='json',required=True)
        args = parser.parse_args()
        # checking data guru yang mempunyai username dan password sesuai inputan
        qry = Admin.query.filter_by(username=args['username'], password=args['password']).first()
        if qry is None:
            return {'message':'UNAUTHORIZED'}, 401
        # token dibuat dengan mengandung identitas yang sama dengan id_guru
        token = create_access_token(identity=qry.id_admin,expires_delta=datetime.timedelta(days=30))
        return {'token': token}, 200