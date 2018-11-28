from api_model import *
from api_field import *
import decimal
# Resource yang berhubungan dengan scoring   
class Dashboard_Resources(Resource):
    # method untuk mendapatkan nilai raw data ujian berdasarkan id_paket_soal dan id_kelas tertentu
    @guru_required
    def get(self):
        # input di params
        parser = reqparse.RequestParser()
        parser.add_argument("id_paket_soal",location='args',required=True)
        parser.add_argument("id_kelas",location='args',required=True)
        args = parser.parse_args()
        # query
        sql = text ('select '
                    'kls.nama_kelas, '
                    'mpl.nama_mapel, '
                    'ps.kode_soal, '
                    'sis.nis,sis.nama, '
                    'ju.no_soal, ju.score_siswa '
                    'from jawaban_ujian ju '
                    'join siswa sis on sis.id_siswa = ju.id_siswa '
                    'join kelas kls on kls.id_kelas = sis.id_kelas '
                    'join paket_soal ps on ps.id_paket_soal = ju.id_paket_soal '
                    'join mapel mpl on mpl.id_mapel = ps.id_mapel '
                    'where '
                    'ju.id_paket_soal = ' + args['id_paket_soal'] +' '
                    'and sis.status = 1 '
                    'and kls.id_kelas = ' + args['id_kelas'])
        qry = db.engine.execute(sql)
        rows = []
        for row in qry:
            rows.append(marshal(row,raw_data_field))
        return {"data":rows},200

    # method untuk mendapatkan distribusi benar salah tiap soal berdasarkan id_kelas dan id_paket_soal
    @guru_required
    def post(self):
        # input di body
        parser = reqparse.RequestParser()
        parser.add_argument("id_paket_soal",location='json',required=True)
        parser.add_argument("id_kelas",location='json',required=True)
        args = parser.parse_args()
        # menghitung ada berapa banyak siswa di dalam id_kelas tersebut
        sql = text('SELECT count(nis) as jumlah_siswa '
                    'FROM sips_db.siswa '
                    'where id_kelas = 1 '
                    'group by id_kelas ')
        qry = db.engine.execute(sql)
        jumlah_siswa = ""
        for row in qry:
            jumlah_siswa += str(row[0])
        jumlah_siswa = int(jumlah_siswa)
        # query join 3 table: siswa, kelas, jawaban_ujian untuk mencari total score tiap soal
        sql = text('SELECT ' 
                    'ju.id_paket_soal, '
                    'kls.id_kelas, '
                    'ju.no_soal, '
                    'sum(ju.score_siswa) as total_score '
                    'FROM jawaban_ujian ju '
                    'join siswa sis on sis.id_siswa = ju.id_siswa '
                    'join kelas kls on kls.id_kelas = sis.id_kelas '
                    'WHERE '
                    'ju.id_paket_soal = ' +args['id_paket_soal'] + ' and kls.id_kelas = ' + args['id_kelas'] +' group by ju.no_soal ')
        qry = db.engine.execute(sql)
        no_soal = []
        total_score = []
        for row in qry:
            no_soal.append(str(row[2]))
            dec = decimal.Decimal(row[3])
            total_score.append(int(dec))
        # fungsi untuk mendapatkan persentase score tiap soal dibandingkan jumlah anak => untuk dashboard nilai
        persentase =[]
        for row in total_score:
            persentase.append(int(100 * row / jumlah_siswa))
        # return response
        return {'id_paket_soal':args['id_paket_soal'],
                'id_kelas':args['id_kelas'],
                'jumlah_siswa': jumlah_siswa,
                'no_soal':no_soal,
                'total_score':total_score,
                'persentase': persentase                        
                },200

class Dashboard_Resources_2(Resource):
    # method untuk mendapatkan nilai ujian berdasarkan id_paket_soal dan id_kelas tertentu ditampilkan dalam bentuk tabel
    @guru_required
    def get(self):
        # input di params
        parser = reqparse.RequestParser()
        parser.add_argument("id_paket_soal",location='args',required=True)
        parser.add_argument("id_kelas",location='args',required=True)
        args = parser.parse_args()
        # query
        sql = text('select '
                    'sis.nis, sis.nama, '
                    'scr.nilai '
                    'from scoring scr '
                    'join siswa sis on sis.id_siswa = scr.id_siswa '
                    'join paket_soal ps on ps.id_paket_soal = scr.id_paket_soal '
                    'join mapel mpl on mpl.id_mapel = ps.id_mapel '
                    'where '
                    'scr.id_paket_soal = ' + args['id_paket_soal'] + ' '
                    'and sis.status = 1 '
                    'and sis.id_kelas = '+ args['id_kelas'])
        qry = db.engine.execute(sql)
        rows = []
        for row in qry:
            rows.append(marshal(row,scoring_field))
        return {"data":rows},200
