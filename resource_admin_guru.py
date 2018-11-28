from api_model import *
from api_field import *

# Resource yang berhubungan dengan guru dan admin
class Admin_Guru_Resources(Resource):
    # method yang digunakan oleh admin untuk mengambil data guru yang ada di database
    @admin_required
    def get(self):
        qry = Guru.query.filter_by(status = 1)
        rows = []
        for row in qry.all():
            rows.append(marshal(row,guru_field))
        return {'data':rows}, 200

    # method yang digunakan oleh admin untuk menambah guru baru
    @admin_required
    def post(self):
        # input di body JSON
        parser = reqparse.RequestParser()
        parser.add_argument("nip",type=str,location='json',required=True)
        parser.add_argument("nama",type=str,location='json',required=True)
        parser.add_argument("alamat",type=str,location='json',required=True)
        parser.add_argument("jenis_kelamin",type=str,location='json',required=True)
        parser.add_argument("telepon",type=str,location='json',required=True)
        parser.add_argument("username",type=str,location='json',required=True)
        parser.add_argument("password",type=str,location='json',required=True)
        args = parser.parse_args()
        # checking di database kalau nip sudah pernah dimasukkan tidak boleh, karena nip sifatnya unik
        qry = Guru.query.filter_by(nip=args['nip']).first()
        if qry is not None:
            return {"message":"duplikat nip"},400
        else:
            # insert into table kelas
            new_guru = Guru(nip = args['nip'],
                        nama = args['nama'],
                        alamat = args['alamat'],
                        jenis_kelamin = args['jenis_kelamin'],
                        telepon = args['telepon'],
                        username = args['username'],
                        password = args['password'],
                        status = 1)
            db.session.add(new_guru)
            db.session.commit()
            # ambil id_guru terbaru 
            qry = Guru.query
            new_id = qry.order_by(desc(Guru.id_guru)).first()
            new_id = new_id.id_guru
            return {"message":"sukses menginput guru baru",
                    "new_guru":new_id},200 

    # method yang digunakan oleh admin untuk mengubah data guru berdasarkan id_guru
    @admin_required
    def put(self,id):
        # ambil data guru berdasarkan id_guru di params
        qry = Guru.query.filter_by(id_guru = id, status = 1).first()
        # checking apakah id_guru tersebut ada di dalam database?
        if qry is None:
            return {"message":"id_guru tidak ditemukan"},404
        else:
            # input di body JSON
            parser = reqparse.RequestParser()
            parser.add_argument("nip",type=str,location='json',required=True)
            parser.add_argument("nama",type=str,location='json',required=True)
            parser.add_argument("alamat",type=str,location='json',required=True)
            parser.add_argument("jenis_kelamin",type=str,location='json',required=True)
            parser.add_argument("telepon",type=str,location='json',required=True)
            parser.add_argument("username",type=str,location='json',required=True)
            parser.add_argument("password",type=str,location='json',required=True)
            args = parser.parse_args()
            # update into table guru
            qry.nip = args['nip']
            qry.nama = args['nama']
            qry.alamat = args['alamat']
            qry.jenis_kelamin = args['jenis_kelamin']
            qry.telepon = args['telepon']
            qry.username = args['username']
            qry.password = args['password']
            db.session.commit()
            return {"message":"sukses mengupdate data guru"},200

    # method yang digunakan oleh admin untuk meghapus data guru berdasarkan id_guru
    @admin_required
    def delete(self,id):
        # ambil data guru berdasarkan id_guru di params
        qry = Guru.query.filter_by(id_guru = id, status = 1).first()
        # checking apakah id_guru tersebut ada di dalam database?
        if qry is None:
            return {"message":"id_guru tidak ditemukan"},404
        else:
            qry.status = 0
            db.session.commit()
            return {'message': 'deleted success'},200