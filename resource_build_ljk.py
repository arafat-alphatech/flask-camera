from api_model import *
from api_field import *
import sys, zipfile, os, shutil
from run import grading
from create_test_sheets import build
import requests
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

		# codes, answer = grading(args['data_uri'])
		# codes 2.1 (id_siswa.id_paket_soal)
		codes = '16.6'
		answer = 'AAAAEACACD'

		# opencv menemukan qrcode dan jawaban
		if (codes != '' or codes != -1) and answer != '':
			codes = codes.split('.')
			id_siswa = codes[0]
			id_paket_soal = codes[1]
			data, http_code = self.doScoring(id_siswa, id_paket_soal, answer)

			return {
				"http_code": http_code,
				"data": data
			}, 200 
		
		# opencv tidak menemukan qecode dan jawaban
		return {
			"http_code": 404,
			"data": {
				"message": "Mohon scan ulang kembali"
			}
		}, 200 
		
	def doScoring(self, id_siswa, id_paket_soal, answer):
		# input lewat parameter fungsi
		args = {}
		args["id_siswa"] = id_siswa
		args["id_paket_soal"] = id_paket_soal
		args["input"] = answer

		# checking apakah id_siswa dan id_paket_soal sudah ada di tabel scoring? jika ya maka return pesan error, jika tidak maka proses dilanjutkan
		qry = Scoring.query
		qry = qry.filter_by(id_siswa = args['id_siswa'], id_paket_soal = args["id_paket_soal"]).first()
		if qry is not None:
			return {
				"message":"Nilai sudah terdata sebelumnya, silahkan LJK yang lain"
			},400
		else:
			# ambil kunci jawaban dari semua soal berdasarkan id_paket_soal yang dicari
			answer = []
			qry = Soal.query.filter_by(id_paket_soal=args['id_paket_soal'])
			qry = qry.order_by(Soal.no_soal)
			data_siswa = Siswa.query.filter_by(id_siswa = args["id_siswa"]).first()

			for item in qry.all():
				answer.append(item.jawaban)
			# split string jawaban siswa kemudian dibandingkan dengan kunci jawaban apabila sama nilainya 1 jika tidak sama nilainya 0 semua dimasukkan ke tabel jawaban_ujian
			output = []
			nilai = []
			index = 0
			total_nilai = 0
			for item in args['input']:
				output.append(item)
				if output[index] == answer[index]:
					nilai.append(1)
				else:
					nilai.append(0)
				new_jawaban_ujian = JawabanUjian(id_siswa = args['id_siswa'],
												id_paket_soal = args['id_paket_soal'],
												no_soal = index+1,
												jawaban_siswa = output[index],
												score_siswa = nilai[index] )
				db.session.add(new_jawaban_ujian)
				db.session.commit()
				total_nilai += nilai[index]
				index += 1
			total_nilai = total_nilai / len(answer) * 100
			# rekapan total nilai setiap siswa dimasukkan ke tabel scoring
			new_scoring = Scoring(id_siswa = args['id_siswa'],
								id_paket_soal = args['id_paket_soal'],
								nilai = total_nilai)
			db.session.add(new_scoring)
			db.session.commit()
			return {
					'message': 'Koreksi jawaban berhasil',
					'id_siswa':args['id_siswa'],
					'nama_siswa': data_siswa.nama,
					'id_paket_soal':args['id_paket_soal'],
					'jawaban_siswa': output,
					'kunci_jawaban': answer,
					'total_nilai': total_nilai
				}, 200