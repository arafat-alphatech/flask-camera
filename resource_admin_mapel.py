from api_model import *
from api_field import *

# Resource yang berhubungan dengan mapel dan admin
class Admin_Mapel_Resources(Resource):
    # method yang digunakan oleh admin untuk mengambil semua mata pelajaran yang ada di database
    @admin_required
    def get(self):
        qry = Mapel.query.filter_by(status=1)
        rows = []
        for row in qry.all():
            rows.append(marshal(row,mapel_field))
        return {'data':rows}, 200

    # method yang digunakan oleh admin untuk menambah mapel baru
    @admin_required
    def post(self):
        # input di body JSON
        parser = reqparse.RequestParser()
        parser.add_argument("nama_mapel",type=str,location='json',required=True)
        parser.add_argument("jadwal",type=str,location='json',required=True)
        args = parser.parse_args()
        # checking di database kalau nama_mapel sudah pernah dimasukkan tidak boleh, karena nama_mapel sifatnya unik
        qry = Mapel.query.filter_by(nama_mapel=args['nama_mapel']).first()
        if qry is not None:
            return {"message":"duplikat nama_mapel"},400
        else:
            # insert into table kelas
            new_mapel = Mapel(nama_mapel = args['nama_mapel'],
                            jadwal = args['jadwal'],
                            status=1)
            db.session.add(new_mapel)
            db.session.commit()
            # ambil id_kelas terbaru 
            qry = Mapel.query
            new_id = qry.order_by(desc(Mapel.id_mapel)).first()
            new_id = new_id.id_mapel
            return {"message":"sukses menginput mapel baru",
                    "new_mapel":new_id},200 

    # method yang digunakan oleh admin untuk mengubah data mapel berdasarkan id_mapel
    @admin_required
    def put(self,id):
        # ambil data mapel berdasarkan id_mapel di params
        qry = Mapel.query.filter_by(id_mapel = id, status=1).first()
        # checking apakah id_mapel tersebut ada di dalam database?
        if qry is None:
            return {"message":"id_mapel tidak ditemukan"},404
        else:
            # input di body JSON
            parser = reqparse.RequestParser()
            parser.add_argument("nama_mapel",type=str,location='json',required=True)
            parser.add_argument("jadwal",type=str,location='json',required=True)
            args = parser.parse_args()
            # update into table mapel
            qry.nama_mapel = args['nama_mapel']
            qry.jadwal = args['jadwal']
            db.session.commit()
            return {"message":"sukses mengupdate data mapel"},200

    # method yang digunakan oleh admin untuk menghapus data mapel berdasarkan id_mapel
    @admin_required
    def delete(self,id):
        # ambil data guru berdasarkan id_mapel di params
        qry = Mapel.query.filter_by(id_mapel = id, status = 1).first()
        # checking apakah id_mapel tersebut ada di dalam database?
        if qry is None:
            return {"message":"id_mapel tidak ditemukan"},404
        else:
            qry.status = 0
            db.session.commit()
            return {'message': 'deleted success'},200