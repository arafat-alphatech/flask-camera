from api_model import *
from api_field import *
import sys, zipfile, os, shutil
from run import grading
from create_test_sheets import build

class BuildLJKResource(Resource):
	# method untuk download zip file ljk yang sudah di generate
	@guru_required
	def get(self):
		# input di body
		parser = reqparse.RequestParser()
		parser.add_argument("id_paket_soal",location='args',required=True)
		parser.add_argument("id_kelas",location='args',required=True)
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
		
		if rows != []:
			path_zip = build(rows)
			return send_file(path_zip, as_attachment=True)
		return {"data": rows}

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("data_uri",location='json')
		args = parser.parse_args()

		codes, answers = grading(args['data_uri'])

		return {"codes": codes, "answer": answers}, 200 
		
