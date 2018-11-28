from api_model import *
from api_field import *

# Resource yang berhubungan dengan kelas
class Kelas_Mapel_Conj_Resources(Resource):
    # method untuk mengambil smeua mata pelajaran pada kelas tertentu berdasarkan id kelas dan id_guru
    @guru_required
    def get(self,id):
        # ambil id_guru dari token
        claims = get_jwt_claims()  
        id_guru = claims['id_guru']
        qry = KelasMapelConj.query.filter_by(id_guru=id_guru,id_kelas = id)
        rows = []
        for row in qry.all():
            rows.append(marshal(row,kelas_mapel_field))
        return {'data':rows}, 200