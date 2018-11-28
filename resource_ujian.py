from api_model import *
from api_field import *

# Resource yang berhubungan dengan ujian
class Ujian_Resources(Resource):
    # method untuk membuat ujian baru di tabel PaketKelasConj dan di tabel PaketSoal
    @guru_required
    def post(self):
        # input di body
        parser = reqparse.RequestParser()
        parser.add_argument("id_kelas",location='json',required=True)
        parser.add_argument("kode_soal",location='json',required=True)
        parser.add_argument("id_mapel",location='json',required=True)
        parser.add_argument("jumlah_soal",location='json',required=True)
        parser.add_argument("tanggal_ujian",location='json',required=True)
        args = parser.parse_args()
        # checking apakah kode_soal tersebut sudah pernah ada di tabel paket soal? jika iya maka return pesan error jika tidak maka proses dilanjutkan
        qry = PaketSoal.query
        qry = qry.filter_by(kode_soal = args['kode_soal']).first()
        if qry is not None:
            return {"message":"kode soal sudah ada di database!"}, 400
        else:
            # insert into table paket soal
            new_paket_soal = PaketSoal(id_mapel = args['id_mapel'],
                                    tanggal_ujian = args['tanggal_ujian'],
                                    jumlah_soal = args['jumlah_soal'],
                                    kode_soal=args['kode_soal'])
            db.session.add(new_paket_soal)
            db.session.commit()
            # ambil id_paket_soal terbaru 
            qry = PaketSoal.query
            new_id = qry.order_by(desc(PaketSoal.id_paket_soal)).first()
            new_id = new_id.id_paket_soal
            # checking apakah pasangan id_paket_soal dan id_kelas udah ada di tabel PaketKelasConj ? jika iya maka return pesan error jika tidak maka proses dilanjutkan
            qry = PaketKelasConj.query
            qry = qry.filter_by(id_kelas = args['id_kelas'], id_paket_soal = new_id).first()
            if qry is not None:
                return {"message":"data paket soal sudah ada dalam database kelas!"},400
            else:
                new_paket_kelas = PaketKelasConj(id_kelas = args['id_kelas'],
                                                id_paket_soal = new_id)
                db.session.add(new_paket_kelas)
                db.session.commit()
                return {"message":"sukses menginput paket soal ujian ",
                        "id_paket_soal":new_id,
                        "id_kelas":args['id_kelas']},200                                 

