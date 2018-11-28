from api_model import *
from api_field import *

# Resource yang berhubungan dengan kelas dan admin
class Admin_Kelas_Resources(Resource):
    # method yang digunakan oleh admin untuk mengambil semua kelas yang ada di database
    @admin_required
    def get(self):
        qry = Kelas.query
        rows = []
        for row in qry.all():
            rows.append(marshal(row,admin_kelas_field))
        return {'data':rows}, 200
    
    # method yang digunakan oleh admin untuk menambah kelas baru
    @admin_required
    def post(self):
        # input di body JSON
        parser = reqparse.RequestParser()
        parser.add_argument("id_tingkat",type=int,location='json',required=True)
        parser.add_argument("nama_kelas",type=str,location='json',required=True)
        parser.add_argument("wali_kelas",type=str,location='json',required=True)
        args = parser.parse_args()
        # insert into table kelas
        new_kelas = Kelas(id_tingkat = args['id_tingkat'],
                        nama_kelas = args['nama_kelas'],
                        wali_kelas = args['wali_kelas'])
        db.session.add(new_kelas)
        db.session.commit()
        # ambil id_kelas terbaru 
        qry = Kelas.query
        new_id = qry.order_by(desc(Kelas.id_kelas)).first()
        new_id = new_id.id_kelas
        return {"message":"sukses menginput kelas baru",
                "id_kelas":new_id},200 

class Admin_Kelas_Resources_2(Resource):
    # method yang digunakan oleh admin untuk mengambil kelas yang ada di database berdasarkan id_kelas
    @admin_required
    def get(self,id):
        qry = Kelas.query.filter_by(id_kelas = id).first()
        # checking apakah id_kelas tersebut ada di dalam database?
        if qry is None:
            return {"message":"id_kelas tidak ditemukan"},404
        else:
            rows = []
            rows.append(marshal(qry,admin_kelas_field))
            return {'data':rows}, 200
    
    # method yang digunakan oleh admin untuk mengubah data kelas berdasarkan id_kelas
    @admin_required
    def put(self,id):
        # ambil data kelas berdasarkan id_kelas di params
        qry = Kelas.query.filter_by(id_kelas = id).first()
        # checking apakah id_kelas tersebut ada di dalam database?
        if qry is None:
            return {"message":"id_kelas tidak ditemukan"},404
        else:
            # input di body JSON
            parser = reqparse.RequestParser()
            parser.add_argument("nama_kelas",type=str,location='json',required=True)
            parser.add_argument("wali_kelas",type=str,location='json',required=True)
            args = parser.parse_args()
            # update into table kelas
            qry.nama_kelas = args['nama_kelas']
            qry.wali_kelas = args['wali_kelas']
            db.session.commit()
            return {"message":"sukses mengupdate data kelas"},200