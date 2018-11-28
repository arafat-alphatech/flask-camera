from api_model import *
from api_field import *
# Resource yang berhubungan dengan scoring   
class Scoring_Resources(Resource):
    # Method untuk mengambil jawaban siswa berupa string, kemudian split per karakter, kemudian masuk ke tabel scoring
    @guru_required
    def post(self):
        # input di body
        parser = reqparse.RequestParser()
        parser.add_argument("id_siswa",location='json',required=True)
        parser.add_argument("id_paket_soal",location='json',required=True)
        parser.add_argument("input",location='json',required=True)
        args = parser.parse_args()
        # checking apakah id_siswa dan id_paket_soal sudah ada di tabel scoring? jika ya maka return pesan error, jika tidak maka proses dilanjutkan
        qry = Scoring.query
        qry = qry.filter_by(id_siswa = args['id_siswa'], id_paket_soal = args["id_paket_soal"]).first()
        if qry is not None:
            return {"message":"data siswa sudah ada dalam database"},400
        else:
            # ambil kunci jawaban dari semua soal berdasarkan id_paket_soal yang dicari
            answer = []
            qry = Soal.query.filter_by(id_paket_soal=args['id_paket_soal'])
            qry = qry.order_by(Soal.no_soal)
            for item in qry.all():
                answer.append(item.jawaban)
            # split string jawaban siswa kemudian dibandingkan dengan kunci jawaban apabila sama nilainya 1 jika tidak sama nilainya 0 semua dimasukkan ke tabel jawaban_ujian
            output = []
            nilai = []
            index = 0
            total_nilai = 0
            for item in args['input']:
                output.append(item)
                if output[index] == answer[index]:
                    nilai.append(1)
                else:
                    nilai.append(0)
                new_jawaban_ujian = JawabanUjian(id_siswa = args['id_siswa'],
                                                id_paket_soal = args['id_paket_soal'],
                                                no_soal = index+1,
                                                jawaban_siswa = output[index],
                                                score_siswa = nilai[index] )
                db.session.add(new_jawaban_ujian)
                db.session.commit()
                total_nilai += nilai[index]
                index += 1
            # rekapan total nilai setiap siswa dimasukkan ke tabel scoring
            new_scoring = Scoring(id_siswa = args['id_siswa'],
                                id_paket_soal = args['id_paket_soal'],
                                nilai = total_nilai)
            db.session.add(new_scoring)
            db.session.commit()
            return {'message': 'sukses mengkoreksi soal',
                    'id_siswa':args['id_siswa'],
                    'id_paket_soal':args['id_paket_soal'],
                    'jawaban_siswa': output,
                    'kunci jawaban': answer,
                    'total nilai': total_nilai}, 200
