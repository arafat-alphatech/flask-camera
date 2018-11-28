from api_model import *
from api_field import *

class PaketSoal_Kelas_Resources(Resource):
	@guru_required
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("id_kelas", location='args', type= int, required=True)
		parser.add_argument("id_mapel", location='args', type= int, required=True)
		args = parser.parse_args()
	
		datas = PaketKelasConj.query.join(PaketSoal).filter(PaketKelasConj.id_kelas == args['id_kelas'], PaketSoal.id_mapel == args['id_mapel']).all() 
		return {'data': marshal(datas,paket_soal_kelas_field)},200    
	# method untuk mendapatkan detail siswa untuk dijadikan input di barcode berdasarkan id_paket_soal dan id_kelas
	@guru_required
	def post(self):
		# input di body
		parser = reqparse.RequestParser()
		parser.add_argument("id_paket_soal",location='json',required=True)
		parser.add_argument("id_kelas",location='json',required=True)
		args = parser.parse_args()
		# query join 5 table: siswa, kelas, paket_kelas_conj, paket_soal, mapel
		sql = text('SELECT ' 
					'ps.id_paket_soal, '
					'pkc.id_kelas, '
					'kls.nama_kelas, '
					'sis.id_siswa, '
					'sis.nama, '
					'mpl.id_mapel, '
					'mpl.nama_mapel, '
					'ps.kode_soal, '
					'ps.tanggal_ujian '
					'FROM '
					'paket_soal ps '
					'JOIN paket_kelas_conj pkc ON ps.id_paket_soal = pkc.id_paket_soal '
					'JOIN mapel mpl ON ps.id_mapel = mpl.id_mapel '
					'JOIN kelas kls ON kls.id_kelas = pkc.id_kelas '
					'JOIN siswa sis ON sis.id_kelas = kls.id_kelas '
					'WHERE pkc.id_paket_soal = '+args['id_paket_soal']+' AND pkc.id_kelas = '+ args['id_kelas'])
		qry = db.engine.execute(sql)
		rows = []
		for row in qry:
			rows.append(marshal(row,qrcode_field))
		return {'data':rows},200
