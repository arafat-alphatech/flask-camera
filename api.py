from api_field import *
#==========================================IMPORT SEMUA RESOURCE=========================
from resource_scoring import *
from resource_kelas import *
from resource_kelasmapelcoj import *
from resource_ujian import *
from resource_soal import *
from resource_paket_soal import *
from resource_paketsoal_kelas import *
from resource_dashboard import *
from resource_build_ljk import *
from resource_mapel import *
from resource_login import *
from resource_admin_login import *
from resource_admin_kelas import *
from resource_admin_mapel import *
from resource_admin_guru import *
from resource_admin_kelasmapelconj import *
from resource_admin_siswa import *
#===========================================END POINT===========================================================

api.add_resource(Scoring_Resources,'/scoring')
api.add_resource(Kelas_Resources,'/kelas/<int:id>')
api.add_resource(Kelas_Mapel_Conj_Resources,'/kelas-mapel/<int:id>')
api.add_resource(Ujian_Resources,'/ujian')
api.add_resource(Soal_Resources,'/soal')
api.add_resource(PaketSoal_Kelas_Resources,'/paket-kelas')
api.add_resource(Paket_Soal_Resources,'/soal_detail')
api.add_resource(Dashboard_Resources,'/dashboard')
api.add_resource(Dashboard_Resources_2,'/dashboard-table')
api.add_resource(BuildLJKResource,'/build')
api.add_resource(Mapel_Resources,'/mapel')
api.add_resource(Login_Resources,'/login')
api.add_resource(Admin_Login_Resources,'/admin/login')
api.add_resource(Admin_Kelas_Resources,'/admin/kelas')
api.add_resource(Admin_Kelas_Resources_2,'/admin/kelas-detail/<int:id>')
api.add_resource(Admin_Mapel_Resources,'/admin/mapel','/admin/mapel/<int:id>')
api.add_resource(Admin_Guru_Resources,'/admin/guru','/admin/guru/<int:id>')
api.add_resource(Admin_kelasmapelconj_Resources,'/admin/kelasmapelconj')
api.add_resource(Admin_Siswa_Resources,'/admin/siswa','/admin/siswa/<int:id>')


@app.route("/")
def home():
    return jsonify({'message': 'SIPPS API in ONLINE'}), 200

@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({'message':'EXPIRED_TOKEN'}),401

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    data = Guru.query.filter_by(id_guru=identity).first()
    if data is None:
        admin_data = Admin.query.filter_by(id_admin=identity).first()
        if admin_data is None:
            return {'type' : 'public'}
        else: 
            return {'id_admin':admin_data.id_admin,
                    'nip':admin_data.nip}
    else:
        return {'id_guru': data.id_guru,
                'nip':data.nip}

@jwt.unauthorized_loader
def unathorized_message(error_string):
    return jsonify({'message': error_string}), 401

if __name__=='__main__':
    try:
        if sys.argv[1]=='db':
            manager.run()
        else:
            app.run(debug=True,host='0.0.0.0',port=5000)
    except IndexError as p:
        app.run(debug=True,host='0.0.0.0',port=5000)
