from flask_restful import fields
#============================================FIELD===========================================================
tingkat_field = {
    'id_tingkat':fields.Integer,
    'nama_kelas':fields.String
}
kelas_field = {
    'id_kelas':fields.Integer,
    'nama_kelas':fields.String
}
admin_kelas_field = {
    'id_tingkat':fields.Integer,
    'id_kelas':fields.Integer,
    'nama_kelas':fields.String,
    'wali_kelas':fields.String
}
mapel_field = {
    'id_mapel':fields.Integer,
    'nama_mapel': fields.String,
    'jadwal': fields.DateTime
}
siswa_field = {
    'id_siswa' :fields.Integer,
    'id_kelas' :fields.Integer,
    'nis':fields.Integer,
    'nama' :fields.String,
    'alamat' :fields.String,
    'jenis_kelamin' :fields.String,    
    'telepon' :fields.String
}
guru_field = {
    'id_guru' :fields.Integer,
    'nip' :fields.Integer,
    'nama' :fields.String,
    'alamat' :fields.String,
    'jenis_kelamin' :fields.String,    
    'telepon' :fields.String,
    'username' :fields.String,
    'password' :fields.String
}
kelas_mapel_conj_field = {
    'id_guru': fields.Integer,
    'id_kelas':fields.Integer,
    'id_mapel':fields.Integer    
}
kelas_mapel_field = {
    'id_mapel':fields.Integer,
    'mapel.nama_mapel':fields.String
}
paket_soal_field = {
    'id_paket_soal':fields.Integer,
    'id_mapel':fields.Integer,
    'kode_soal':fields.String,
    'tanggal_ujian': fields.String
}
soal_by_paket_field = {
    'id_paket_soal':fields.Integer,
    'id_soal': fields.Integer,
    'narasi': fields.String,
    'narasi': fields.String,
    'option_A': fields.String,
    'option_B': fields.String,
    'option_C': fields.String,
    'option_D': fields.String,
    'option_E': fields.String,
    'jawaban': fields.String
}
soal_field = {
    'id_soal':fields.Integer,
    'id_paket_soal': fields.Integer,
    'no_soal': fields.Integer,
    'narasi': fields.String,
    'option_A': fields.String,
    'option_B': fields.String,
    'option_C': fields.String,
    'option_D': fields.String,
    'option_E': fields.String,
    'jawaban': fields.String,
}
qrcode_field = {
    'id_paket_soal':fields.Integer,
    'kode_soal':fields.String,
    'tanggal_ujian': fields.String,
    'nama_mapel':fields.String,
    'id_mapel':fields.Integer,
    'id_kelas':fields.Integer,
    'nama_kelas':fields.String,
    'id_siswa':fields.Integer,
    'nama':fields.String 
}
dashboard_field = {
    'id_paket_soal': fields.Integer,
    'id_kelas': fields.Integer,
    'no_soal': fields.Integer,
    'total_score': fields.Integer
}

paket_soal_kelas_field = {
    'id_kelas': fields.Integer,
    'id_paket_soal': fields.Integer,
    'paket_soal.kode_soal': fields.String,
    'paket_soal.tanggal_ujian': fields.String
}
paket_by_mapel_field = {
    'id_paket_soal':fields.Integer,
    'kode_soal':fields.String
}
raw_data_field = {
    'nama_kelas':fields.String,
    'nama_mapel':fields.String,
    'kode_soal':fields.String,
    'nis':fields.Integer,
    'nama':fields.String,
    'no_soal':fields.Integer,
    'score_siswa':fields.Integer
}
scoring_field = {
    'nis':fields.Integer,
    'nama':fields.String,
    'nilai':fields.Float
}