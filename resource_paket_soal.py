from api_model import *
from api_field import *

class Paket_Soal_Resources(Resource):
    # method untuk mendapatkan data soal yang sudah ada berdasarkan id_paket_soal dan id_soal
    @guru_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id_paket_soal",location='json',required=True)
        parser.add_argument("id_soal",location='json',required=True)
        args = parser.parse_args()
        qry = Soal.query
        qry = qry.filter_by(id_paket_soal = args['id_paket_soal'], id_soal = args['id_soal']).first()
        return {'data':marshal(qry,soal_field)},200