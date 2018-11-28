from api_model import *
from api_field import *

# Resource yang berhubungan dengan kelasmapelconj dan admin
class Admin_kelasmapelconj_Resources(Resource):
    # method yang digunakan oleh admin untuk mengambil data kelasmapelconj yang ada di database
    @admin_required
    def get(self):
        sql = text('select kmc.id_guru, kmc.id_kelas, kmc.id_mapel '
                    'from kelas_mapel_conj kmc '
                    'join guru gur on gur.id_guru = kmc.id_guru '
                    'where gur.status = 1 '
                )
        qry = db.engine.execute(sql)
        rows = []
        for row in qry:
            rows.append(marshal(row,kelas_mapel_conj_field))
        return {'data':rows}, 200

    # method yang digunakan oleh admin untuk menambah kelasmapelconj baru
    @admin_required
    def post(self):
        # input di body JSON
        parser = reqparse.RequestParser()
        parser.add_argument("id_kelas",type=int,location='json',required=True)
        parser.add_argument("id_mapel",type=int,location='json',required=True)
        parser.add_argument("id_guru",type=int,location='json',required=True)
        args = parser.parse_args()
        # insert into table kelasmapelconj
        new_kelasmapelconj = KelasMapelConj(id_kelas = args['id_kelas'],
                                            id_mapel = args['id_mapel'],
                                            id_guru = args['id_guru'])
        db.session.add(new_kelasmapelconj)
        db.session.commit()
        return {"message":"sukses menginput kelasmapelconj baru"},200 
    
    # method yang digunakan oleh admin untuk mengubah data kelasmapelconj 
    @admin_required
    def put(self):
        # input di body JSON
        parser = reqparse.RequestParser()
        parser.add_argument("id_kelas_old",type=int,location='json',required=True)
        parser.add_argument("id_mapel_old",type=int,location='json',required=True)
        parser.add_argument("id_guru_old",type=int,location='json',required=True)
        parser.add_argument("id_kelas_new",type=int,location='json',required=True)
        parser.add_argument("id_mapel_new",type=int,location='json',required=True)
        parser.add_argument("id_guru_new",type=int,location='json',required=True)
        args = parser.parse_args()
        # checking apakah inputan data tersebut sudah ada di database?
        qry = KelasMapelConj.query.filter_by(id_kelas = args['id_kelas_new'], id_mapel=args['id_mapel_new'],id_guru=args['id_guru_new']).first()
        if qry is not None:
            return {"message":"duplicate primary key"}, 400
        else:
            qry = KelasMapelConj.query.filter_by(id_kelas = args["id_kelas_old"], id_mapel=args["id_mapel_old"],id_guru=args["id_guru_old"]).first()
            qry.id_guru = args['id_guru_new']
            qry.id_kelas = args['id_kelas_new']
            qry.id_mapel = args['id_mapel_new']
            db.session.commit()
            return {"message":"sukses mengupdate data kelasmapelconj"},200
        