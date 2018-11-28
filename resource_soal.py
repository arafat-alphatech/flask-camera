from api_model import *
from api_field import *

# Resource yang berhubungan dengan soal
class Soal_Resources(Resource):
    # method untuk mendapatkan semua soal yang ada berdasarkan id_paket_soal digunakan di halaman ujian (untuk mengedit paket soal yang sudah ada)
    @guru_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id_paket_soal",location='args',required=True)
        args = parser.parse_args()
        datas = Soal.query.filter_by(id_paket_soal= args['id_paket_soal']).all()
        qry = PaketSoal.query.filter_by(id_paket_soal= args['id_paket_soal']).first()
        return {'jumlah_soal':qry.jumlah_soal,
                'data': marshal(datas,soal_field)},200    

    # method untuk membuat soal baru
    @guru_required
    def post(self):
         # input di body
        parser = reqparse.RequestParser()
        parser.add_argument("id_paket_soal",location='json',required=True)
        parser.add_argument("no_soal",location='json',required=True)
        parser.add_argument("narasi",location='json',required=True)
        parser.add_argument("option_A",location='json',required=True)
        parser.add_argument("option_B",location='json',required=True)
        parser.add_argument("option_C",location='json',required=True)
        parser.add_argument("option_D",location='json',required=True)
        parser.add_argument("option_E",location='json',required=True)
        parser.add_argument("jawaban",location='json',required=True)
        args = parser.parse_args()
        # insert into table soal
        new_soal=Soal(id_paket_soal = args['id_paket_soal'],
                      no_soal = args['no_soal'],
                      narasi = args['narasi'],
                      option_A = args['option_A'],
                      option_B = args['option_B'],
                      option_C = args['option_C'],
                      option_D = args['option_D'],
                      option_E = args['option_E'],
                      jawaban = args['jawaban'])
        db.session.add(new_soal)
        db.session.commit()
        # ambil id_soal terbaru 
        qry = Soal.query
        new_id = qry.order_by(desc(Soal.id_soal)).first()
        new_id = new_id.id_soal
        return {"message":"sukses menginput soal ujian ",
                "id_paket_soal":args['id_paket_soal'],
                "id_soal":new_id},200 
    
    # method untuk mengupdate soal yang sudah ada
    @guru_required
    def put(self):
         # input di body
        parser = reqparse.RequestParser()
        parser.add_argument("id_paket_soal",location='json',required=True)
        parser.add_argument("no_soal",location='json',required=True)
        parser.add_argument("narasi",location='json',required=True)
        parser.add_argument("option_A",location='json',required=True)
        parser.add_argument("option_B",location='json',required=True)
        parser.add_argument("option_C",location='json',required=True)
        parser.add_argument("option_D",location='json',required=True)
        parser.add_argument("option_E",location='json',required=True)
        parser.add_argument("jawaban",location='json',required=True)
        args = parser.parse_args()
        # ambil data soal dari database
        qry = Soal.query
        qry = qry.filter_by(id_paket_soal = args ['id_paket_soal'], no_soal = args['no_soal'])
        # update into table soal
        qry = qry.update({'narasi' : args['narasi'],
                            'option_A' : args['option_A'],
                            'option_B' : args['option_B'],
                            'option_C' : args['option_C'],
                            'option_D' : args['option_D'],
                            'option_E' : args['option_E'],
                            'jawaban' : args['jawaban']})
        db.session.commit()
        return {"message":"sukses mengupdate soal ujian "},200 