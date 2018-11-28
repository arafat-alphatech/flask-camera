from api_model import *
from api_field import *

# Resource yang berhubungan dengan siswa dan admin
class Admin_Siswa_Resources(Resource):
    # method yang digunakan oleh admin untuk mengambil data siswa yang ada di database
    @admin_required
    def get(self):
        qry = Siswa.query.filter_by(status = 1)
        rows = []
        for row in qry.all():
            rows.append(marshal(row,siswa_field))
        return {'data':rows}, 200

    # method yang digunakan oleh admin untuk menambah siswa baru
    @admin_required
    def post(self):
        # input di body JSON
        parser = reqparse.RequestParser()
        parser.add_argument("id_kelas",type=int,location='json',required=True)
        parser.add_argument("nis",type=int,location='json',required=True)
        parser.add_argument("nama",type=str,location='json',required=True)
        parser.add_argument("alamat",type=str,location='json',required=True)
        parser.add_argument("jenis_kelamin",type=str,location='json',required=True)
        parser.add_argument("telepon",type=str,location='json',required=True)
        args = parser.parse_args()
        # checking di database kalau nis sudah pernah dimasukkan tidak boleh, karena nis sifatnya unik
        qry = Siswa.query.filter_by(nis=args['nis']).first()
        if qry is not None:
            return {"message":"duplikat nis"},400
        else:
            # insert into table kelas
            new_siswa = Siswa(nis = args['nis'],
                        id_kelas = args['id_kelas'],
                        nama = args['nama'],
                        alamat = args['alamat'],
                        jenis_kelamin = args['jenis_kelamin'],
                        telepon = args['telepon'],
                        status = 1)
            db.session.add(new_siswa)
            db.session.commit()
            # ambil id_siswa terbaru 
            qry = Siswa.query
            new_id = qry.order_by(desc(Siswa.id_siswa)).first()
            new_id = new_id.id_siswa
            return {"message":"sukses menginput siswa baru",
                    "new_siswa":new_id},200 

    # method yang digunakan oleh admin untuk mengubah data siswa berdasarkan id_siswa
    @admin_required
    def put(self,id):
        # ambil data siswa berdasarkan id_siswa di params
        qry = Siswa.query.filter_by(id_siswa = id, status = 1).first()
        # checking apakah id_siswa tersebut ada di dalam database?
        if qry is None:
            return {"message":"id_siswa tidak ditemukan"},404
        else:
            # input di body JSON
            parser = reqparse.RequestParser()
            parser.add_argument("id_kelas",type=int,location='json',required=True)
            parser.add_argument("nis",type=int,location='json',required=True)
            parser.add_argument("nama",type=str,location='json',required=True)
            parser.add_argument("alamat",type=str,location='json',required=True)
            parser.add_argument("jenis_kelamin",type=str,location='json',required=True)
            parser.add_argument("telepon",type=str,location='json',required=True)
            args = parser.parse_args()
            # update into table siswa
            qry.nis = args['nis']
            qry.id_kelas = args['id_kelas']
            qry.nama = args['nama']
            qry.alamat = args['alamat']
            qry.jenis_kelamin = args['jenis_kelamin']
            qry.telepon = args['telepon']
            db.session.commit()
            return {"message":"sukses mengupdate data siswa"},200

    # method yang digunakan oleh admin untuk meghapus data siswa berdasarkan id_siswa
    @admin_required
    def delete(self,id):
        # ambil data siswa berdasarkan id_siswa di params
        qry = Siswa.query.filter_by(id_siswa = id, status = 1).first()
        # checking apakah id_siswa tersebut ada di dalam database?
        if qry is None:
            return {"message":"id_siswa tidak ditemukan"},404
        else:
            qry.status = 0
            db.session.commit()
            return {'message': 'deleted success'},200