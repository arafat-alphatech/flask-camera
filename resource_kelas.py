from api_model import *
from api_field import *

# Resource yang berhubungan dengan kelas
class Kelas_Resources(Resource):
    # method untuk mengambil semua kelas yang ada di database
    @guru_required
    def get(self,id):
        qry = Kelas.query.filter_by(id_tingkat=id)
        rows = []
        for row in qry.all():
            rows.append(marshal(row,kelas_field))
        return {'data':rows}, 200

   