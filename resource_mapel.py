from api_model import *
from api_field import *

# Resource yang berhubungan dengan mapel
class Mapel_Resources(Resource):  
    # method untuk mendapatkan semua id_paket_soal berdasarkan id_mapel dan id_kelas digunakan di dashboard
    @guru_required
    def post(self):
        # input di body
        parser = reqparse.RequestParser()
        parser.add_argument("id_mapel",location='json',required=True)
        parser.add_argument("id_kelas",location='json',required=True)
        args = parser.parse_args()
        # query join 4 table: paket_soal, mapel, paket_kelas_conj, dan kelas untuk mencari list paket soal
        sql = text('SELECT ' 
                    'ps.id_paket_soal, '
                    'ps.kode_soal '
                    'from paket_soal ps '
                    'join mapel mpl on mpl.id_mapel = ps.id_mapel '
                    'join paket_kelas_conj pkc on pkc.id_paket_soal = ps.id_paket_soal '
                    'join kelas kls on kls.id_kelas = pkc.id_kelas '
                    'where mpl.id_mapel =' +args['id_mapel'] +' and kls.id_kelas = '+args['id_kelas'])
        qry = db.engine.execute(sql)
        rows = []
        for row in qry:
            rows.append(marshal(row,paket_by_mapel_field))
        return {"data":rows},200

