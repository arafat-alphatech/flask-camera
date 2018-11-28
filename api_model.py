from api_config import *

#==========================================MODEL===========================================================

# tabel guru
class Guru(db.Model):
    id_guru = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.Integer,unique=True,nullable=False)
    nama = db.Column(db.String(100),nullable=False)
    alamat = db.Column(db.String(1000),nullable=False)
    jenis_kelamin = db.Column(db.String(1),nullable=False)
    telepon = db.Column(db.String(15),nullable=False)
    username = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    status = db.Column(db.Boolean,nullable=False)
    kelasmapelconj = relationship("KelasMapelConj", back_populates="guru")

    def __repr__(self):
        return '<Guru %r>' %self.id_guru

# tabel guru
class Admin(db.Model):
    id_admin = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.Integer,unique=True,nullable=False)
    nama = db.Column(db.String(100),nullable=False)
    alamat = db.Column(db.String(1000),nullable=False)
    jenis_kelamin = db.Column(db.String(1),nullable=False)
    telepon = db.Column(db.String(15),nullable=False)
    username = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)

    def __repr__(self):
        return '<Admin %r>' %self.id_admin

# tabel tingkat
class Tingkat(db.Model):
    id_tingkat = db.Column(db.Integer,primary_key=True)
    nama_tingkat = db.Column(db.String(100),nullable=False) 

    def __repr__(self):
        return '<Tingkat %r>' %self.id_tingkat       

# tabel mapel
class Mapel(db.Model):
    id_mapel = db.Column(db.Integer, primary_key=True)
    nama_mapel = db.Column(db.String(100),nullable=False)
    jadwal = db.Column(db.DateTime,nullable=False)
    kelasmapelconj = relationship("KelasMapelConj", back_populates="mapel")
    status = db.Column(db.Boolean,nullable=False,default=1)

    def __repr__(self):
        return '<Mapel %r>' %self.id_mapel

# tabel kelas
class Kelas(db.Model):
    id_tingkat = db.Column(db.Integer,ForeignKey('tingkat.id_tingkat',ondelete='CASCADE'))
    id_kelas = db.Column(db.Integer, primary_key=True)
    nama_kelas = db.Column(db.String(100),nullable=False)
    wali_kelas = db.Column(db.String(100),nullable=False)
    kelasmapelconj = relationship("KelasMapelConj", back_populates="kelas")
    paketkelasconj = relationship("PaketKelasConj", back_populates="kelas")
    siswa = relationship("Siswa", back_populates="kelas")
    
    def __repr__(self):
        return '<Kelas %r>' %self.id_kelas

# tabel kelas_mapel_conj
class KelasMapelConj(db.Model):
     id_kelas = db.Column(db.Integer,db.ForeignKey('kelas.id_kelas', ondelete="CASCADE"),nullable=False,primary_key=True)
     kelas = relationship("Kelas",uselist=False, back_populates="kelasmapelconj")
     id_mapel = db.Column(db.Integer, db.ForeignKey('mapel.id_mapel', ondelete="CASCADE"),nullable=False,primary_key=True)
     mapel = relationship("Mapel", uselist=False,back_populates="kelasmapelconj")
     id_guru = db.Column(db.Integer, db.ForeignKey('guru.id_guru', ondelete="CASCADE"),nullable=False,primary_key=True,default=1)
     guru = relationship("Guru", uselist=False,back_populates="kelasmapelconj")
    
# tabel siswa 
class Siswa(db.Model):
    id_siswa = db.Column(db.Integer, primary_key=True)
    id_kelas = db.Column(db.Integer,ForeignKey('kelas.id_kelas', ondelete='CASCADE'))
    nis = db.Column(db.Integer,unique=True,nullable=False)
    nama = db.Column(db.String(100),nullable=False)
    alamat = db.Column(db.String(1000),nullable=False)
    jenis_kelamin = db.Column(db.String(1),nullable=False)
    telepon = db.Column(db.String(15),nullable=False)
    jawaban_ujian = relationship("JawabanUjian", back_populates="siswa")
    scoring = relationship("Scoring", back_populates="siswa")
    kelas = relationship("Kelas",back_populates="siswa")
    status = db.Column(db.Boolean,nullable=False,default=1)

    def __repr__(self):
        return '<Siswa %r>' %self.id_siswa

# tabel paket_soal 
class PaketSoal(db.Model):
    id_paket_soal = db.Column(db.Integer, primary_key=True)
    id_mapel = db.Column(db.Integer,ForeignKey('mapel.id_mapel', ondelete='CASCADE'))
    kode_soal = db.Column(db.String(100),nullable=False)  
    jumlah_soal = db.Column(db.Integer, nullable=False) 
    tanggal_ujian = db.Column(db.DateTime,nullable=False)
    jawaban_ujian = relationship("JawabanUjian", back_populates="paket_soal")
    scoring = relationship("Scoring", back_populates="paket_soal")
    paket_kelas_conj = relationship("PaketKelasConj", back_populates="paket_soal")
    
    def __repr__(self):
        return '<Paket_Soal %r>' %self.id_paket_soal
# tabel paket kelas
class PaketKelasConj(db.Model):
     id_kelas = db.Column(db.Integer,db.ForeignKey('kelas.id_kelas', ondelete="CASCADE"),nullable=False,primary_key=True)
     kelas = relationship("Kelas",uselist=False, back_populates="paketkelasconj")
     id_paket_soal = db.Column(db.Integer, db.ForeignKey('paket_soal.id_paket_soal', ondelete="CASCADE"),nullable=False,primary_key=True)
     paket_soal = relationship("PaketSoal", back_populates="paket_kelas_conj")

# tabel soal 
class Soal(db.Model):
    id_soal = db.Column(db.Integer, primary_key=True)
    id_paket_soal = db.Column(db.Integer,ForeignKey('paket_soal.id_paket_soal', ondelete='CASCADE'))
    no_soal = db.Column(db.Integer,nullable=False) 
    narasi = db.Column(db.String(255),nullable=False)   
    option_A = db.Column(db.String(255),nullable=False) 
    option_B = db.Column(db.String(255),nullable=False) 
    option_C = db.Column(db.String(255),nullable=False) 
    option_D = db.Column(db.String(255),nullable=False) 
    option_E = db.Column(db.String(255),nullable=False)
    jawaban = db.Column(db.String(1),nullable=False) 
     
    def __repr__(self):
        return '<Soal %r>' %self.id_soal

# tabel jawaban_ujian
class JawabanUjian(db.Model):
    id_jawaban_ujian = db.Column(db.Integer, primary_key=True)
    id_siswa = db.Column(db.Integer,db.ForeignKey('siswa.id_siswa', ondelete="CASCADE"),nullable=False)
    siswa = relationship("Siswa",uselist=False, back_populates="jawaban_ujian")
    id_paket_soal = db.Column(db.Integer, db.ForeignKey('paket_soal.id_paket_soal', ondelete="CASCADE"),nullable=False)
    paket_soal = relationship("PaketSoal", uselist=False,back_populates="jawaban_ujian")
    no_soal = db.Column(db.Integer,nullable=False)
    jawaban_siswa = db.Column(db.String(1),nullable=False)
    score_siswa = db.Column(db.Integer,nullable=False)
  
# tabel scoring
class Scoring(db.Model):
    id_scoring = db.Column(db.Integer, primary_key=True)
    id_siswa = db.Column(db.Integer,db.ForeignKey('siswa.id_siswa', ondelete="CASCADE"),nullable=False)
    siswa = relationship("Siswa",uselist=False, back_populates="scoring")
    id_paket_soal = db.Column(db.Integer, db.ForeignKey('paket_soal.id_paket_soal', ondelete="CASCADE"),nullable=False)
    paket_soal = relationship("PaketSoal", uselist=False,back_populates="scoring")
    nilai = db.Column(db.Integer,nullable=False)





