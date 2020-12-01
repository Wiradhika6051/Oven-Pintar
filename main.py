"""
Tubes Pengkom "Smart Oven"
Kelompok 2
Nama:
16520049-Rifqi Ananda
16520059-Fawwaz Anugrah Wiradhika Dharmasatya
16520079-Hani Rafifah
16520449-Rahadyanino Maheswara

Simulasi oven dengan cara:
0.Mulai
1.Memencet tombol buka oven
2.Memasukkan input makanan yang dimasukkan
3.Memencet tombol tutup oven
4.Jika ada metode preset,metode preset yang akan dipake.Metode preset hanya saran.Bisa diganti pengguna inputnya
5.Jika masukan tidak ada di metode preset atau pengguna ingin mengganti data input,maka pengguna memasukkan input suhu maksimum,metode memasak,dan lama waktu memasak(dalam menit dan detik)
6.Menekan tombol mulai
7.Oven akan disiapkan
8.Magnetron menyala
9.Proses memasak dimulai,timer berjalan dan suhu oven naik
10.Jika pengguna ingin menghentikan proses,tekan tombol berhenti,dan semua data suhu oven dan timer akan direset ke keadaan awal
11.Jika pengguna tidak menekan tombol berhenti,maka oven akan terus berjalan sampai timer mencapai 0.
12.Oven berhenti dan membunyikan alarm
13.Pengguna menekan tombol ambil makanan.
12.Selesai
"""
#Modul yang diimport
from tkinter import *               #Untuk membuat GUI
from PIL import ImageTk,Image       #Untuk menampilkan gambar oven
from pygame import mixer            #Untuk membunyikan indikator ketika oven telah selesai memasak
from tkinter import messagebox      #Untuk menampilkan prompt konfirmasi


#Kamus
#Mode/Metode memasak
modes = ['Traditional','Baking','Fast cooking','Multilevel','Pizza','Grill','Defrosting']
#List makanan yang sudah ada penaturan presetnya
makanan = [['bebek','sapi','biskuit','tart'],
           ['kue buah','kue spons dengan yoghurt','kue spons','pancake isi','kue kecil','cheese puff','cream puff','kue busa'],
           ['courgette and prawn pie','country style spinach pie','turnovers','lasagne','golden rolls','chicken bites','golden chicken wings'],
           ['domba','ayam + kentang','makerel','savoury pie'],
           ['pizza'],
           ['sotong','cumi','udang','kod','sayuran','stik sapi','sosis','hamburger','sandwich'],
           ['makanan beku','ice cream cake']
]
#Data suhu pemanggangan maksimum setiap preset
suhu_maks = [[200,200,180,180], 
             [180,180,160,200,190,210,180,90],
             [200,220,200,200,180,220,200],
             [180,200,180,200],
             [220],
             [260,260,260,260,260,260,260,260,260],
             [80,80]
]
#Data lama pemanggangan total tiap preset(dalam menit)
lama_masak = [[65,70,15,30], 
              [40,40,25,30,20,15,20,180],
              [20,30,25,35,25,15,20],
              [40,60,30,25],
              [15],
              [10,8,8,10,15,15,15,10,3],
              [20,20]
]
#Waktu preheat(waktu untuk mencapai suhu maksimum)dalam sekon
#0 berarti tidak ada waktu preheat dan oven akan terus dipanaskan sampai mencapai suhu maks
#Jika waktu preheat>0,maka oven akan dipanaskan selama waktu_preheat lalu suhunya konstan
waktu_preheat=[900,900,0,600,900,0,0]
#Menandakan apakah oven berhenti,diinisialisasi False karena pada awalnya ovennya jalan
berhenti = False
#Daftar makanan yang dimasukkan diinisialisasi dengan "Kosong" 
food = "udara"              #Kalo oven kosong isinya udara(Asumsikan oven tidak kedap udara)
#Suhu awal oven
temperatur = 25             #Suhu Kamar sekitar 25 derajat celcius
#Waktu untuk melakukan pemanasan oven
waktu_memanaskan = 0                
#Kenaikan suhu selama pemanasan
kenaikan_suhu = 0
#Digunakan untuk pengecekan interval kenaikan suhu agar cukup diperiksa sekali
cek = True
#Variabel untuk menyimpan lama waktu preheat
preheat = 0

#Fungsi dan prosedur
def buka():
    """
    Prosedur untuk menampilkan layar baru untuk mensimulasikan membuka oven
    """
    #Variabel global
    global food
    #Membuat layar baru 
    masuk = Toplevel()
    masuk.title("Simulasi Oven Pintar")
    #Memberi notifikasi khusus ke pengguna
    Label(masuk,text="Note:Pindahkan layar ini hingga latar belakang layar bukan program utama.").grid(row=0,column=0)
    Label(masuk,text="Hal ini untuk mencegah layar ini tersembunyi dibalik layar utama ketika anda menjawab prompt konfirmasi").grid(row=1,column=0)
    #Label untuk menampilkan pesan 
    Label(masuk,text="Masukkan bahan makanan:").grid(row=2,column=0)
    #Kolom untuk menerima masukan makanan yang dimasukkan pengguna
    bahan = Entry(masuk,width=20)
    bahan.grid(row=3,column=0)
    #Tombol untuk mengkonfirmasi masukan
    confirmation = Button(masuk,text="MASUKKAN BAHAN",command=lambda:konfirmasi_(bahan.get()))      #Akan memanggil fungsi konfirmasi_ bila ditekan
    confirmation.grid(row=4,column=0)
    #oven = Label(masuk,text="Isi Oven:"+food).grid(row=2,column=0)
    Button(masuk,text="TUTUP OVEN",command=masuk.destroy).grid(row=5,column=0)                      #Tombol untuk menutup oven.Akan menghancurkan layar bila ditekan
    #Note:Saat selesai memanggil fungsi konfirmasi_,layar isis oven akan mun

def konfirmasi_(bahan_):
    """
    Prosedur yang menghasilkan prompt untuk mengkonfirmasi masukan makanan pengguna
    """
    hasil = messagebox.askyesno("Menutup oven","Apakah Anda ingin memasak "+bahan_+"?")             #Prompt untuk konfirmasi
    if hasil == 1:                                                                                  #Jika pengguna menekan ya
        masak(bahan_)                                                                               #Memanggil fungsi masak
        mulai['state'] = ACTIVE                                                                     #Mengaktifkan tombol mulai

def masak(bahan_):
    """
    Prosedur untuk memproses data makanan yang dimasukkan
    """
    #Variabel global
    global food
    global mode_masak
    global modes
    #Masukan makanan tulisannya dijadikan huruf kecil semua agar bisa dibandingkan dengan kata kunci preset makanan di database
    food = bahan_.lower()
    #Mengupdate label status 
    status['text'] = "Anda memasukkan "+bahan_
    #Mengupdate label metode memasak
    metode_masak['text'] = "Metode memasak:"+mode_masak.get()
    #membandingkan masukan dengan basis data
    check_data(modes,food)

def check_data(modes_,inputan):
    """
    Prosedur untuk memeriksa inputan pengguna,menyesuaikan dengan database.Jika masukan ada di database,memasukkan data preset ke input
    """
    #Variabe global
    global makanan
    global suhu_maks
    global lama_masak
    #Variabel lokal:
    #Karena kolom tiap baris berbeda,maka akan sangat sulit dibanding biasanya untuk mencari indeks
    #Maka kami menggunakan kounter untuk menentukan berapa kali terjadi pengulangan.
    #Kounter ini akan digunakan untuk mencari jumlah pengulangan yang sesuai
    iterate = 0 
    #jumlah pengulangan yang sesuai.Diinisialisasi dengan 0 pada awalnya
    num_iterate = 0
    #Kounter untuk mencari baris dari array
    row = 0      
    #Variabel untuk mencari indeks baris dari array
    baris = -1          #-1 berarti masukan tidak ada di database preset
    #Loop untuk mencari nilai num_iterate dan baris
    for i in makanan:                           #Memeriksa setiap baris di array
        for j in i:                             #Memeriksa setiap kolom di array
            if(inputan == j):                   #Jika masukan dari pengguna ada di database
                num_iterate = iterate           #Memperbaharui nilai num_iterate                 
                baris = row                     #Memperbaharui nilai baris
            iterate += 1                        #Setiap pengulangan kolom,kounter iterate nilainya ditambah 1 
        row+=1                                  #Setiap penglangan baris,kounter row bertambah 1 nilainya
    #Jika masukan ada di database:
    if(baris != -1):
        method = modes_[baris]                  #Menginisialisasi metode memasak yang dpilih pengguna
        #Memasukkan data rekomendasi pengaturan dari database
        #Mencari nilai suhu maksimum dan waktu maksimum
        suhu_max =iterasi_matriks(suhu_maks,num_iterate)
        waktu_max = iterasi_matriks(lama_masak,num_iterate)
        #Suhu maksimal
        input_suhu.delete(0,END)                        #Labelnya dikosongkan dulu pada awalnya untuk mencegah glitch
        input_suhu.insert(0,str(suhu_max))              #Nilainya diperbaharui dengan nilai suhu_max
        #Metode memasak
        mode_masak.set(method)                          #Nilainya diperbaharui dengan nilai method
        #Memperbaharui label yang menunjukkan informasi tentang metode memasak
        metode_masak['text'] = "Metode memasak:"+mode_masak.get()
        #Menit memasak
        input_menit.delete(0,END)                       #Labelnya dikosongkan dulu pada awalnya untuk mencegah glitch
        input_menit.insert(0,str(waktu_max))            #Nilainya diperbaharui dengan nilai waktu_max(dalam menit)
        #Detik memasak
        input_detik.delete(0,END)                       #Labelnya dikosongkan dulu pada awalnya untuk mencegah glitch
        input_detik.insert(0,str((waktu_max % 1)*60))   #Karena di matriks lama_masak nilainya disimpan dalam menit,maka perlu dikonveri menjadi detik
                                                        #dengan cara dicari sisa pembagiannya dengan 1 lalu dikali 60

def iterasi_matriks(matriks,jumlah_iterasi):
    """
    Fungsi untuk mencari nilai elemen di suatu matriks dengan input total perulangan yang dilakukan(int) dan matriks(tipe data elemen bebas), lalu
    mengembalikan nilai dari elemen tersebut(tipe data bebas)
    """
    #Variabel lokal
    iterasi = 0                                 #Kounter untuk iterasi
    nilai = 0                                   #Isi elemen yang dicari
    #Melakukan looping di dalam matriks untuk setiap baris dan kolom     
    for i in matriks:                                      
        for j in i:
            if(iterasi == jumlah_iterasi):      #Jika jumlah iterasi fungsi sama dengan jumlah iterasi untuk mendapatkan nilai
                nilai = j                       #Memperbaharui nilai isi elemen
            iterasi += 1                        #Setiap pengulangan kolom,nilai iterasi bertambah 1
    return nilai                                #Mengembalikan nilai berupa isi elemen yang dicari
def iterasi_array(array,metode_):
    """
    Fungsi untuk mencari nilai elemen di suatu array dengan input array tersebut(tipe data elemen bebas) dan elemen yang dicaritipe data elemen bebas), lalu
    mengembalikan indeks dari elemen tersebut(int)
    """
    kounter = 0                                                         #Kounter untuk mencari baris dari array
    line = -1                                                           #Baris dari elemen array
    for i in array:                                                     #Looping setiap elemen array                                
        if(i == metode_):                                               #Jika nilai i dan metode_ sama
            line = kounter                                              #Line diperbaharui nilainya menjadi senilai dengan kounter
        kounter += 1                                                    #Setiap baris,nilai kounter ditambah 1
    return line                                                         #Mengembalikan indeks dari nilai tersebut

def start(minutes,seconds,suhu_kamar,max_temp,makanan,array_):
    """
    Prosedur yang mempersiapkan oven agar siap digunakan setelah pengguna menekan tombol "MULAI"
    """
    #Variabel global
    global berhenti
    global preheat
    metode = mode_masak.get()                                   #Metode memasak yang dipilih
    berhenti = False                                            #Jika nilainya False,oven akan berjalan
    #Variabel lokal
    metode_masak['text'] = "Metode memasak:"+metode             #Memperbaharui label yang menunjukkan metode memasak 
    #Kondisional
    if(max_temp>suhu_kamar):                                                #Jika nilai masukan temperatur maksimum lebih besar dari suhu kamar         
        info_temperatur['text'] = "Temperatur:"+str(suhu_kamar)+"°C"        #Memperbaharui label yang menunjukkan suhu oven
        status['text'] = "Oven sedang disiapkan"                            #Memperbaharui label yang menunjukkan status oven
        seconds = int(minutes)*60 + int(seconds)                            #Mengkonversi waktu input(menit dan detik) ke dalam variabel detik
        masukkan_makanan.config(state="disabled")                           #Menonaktifkan tombol untuk membuka oven
        #Mencari waktu preheat
        preheat = waktu_preheat[iterasi_array(modes,metode)]
        #Menyalakan magnetron
        menu.after(3000,menyalakan_magnetron,seconds,suhu_kamar,max_temp,makanan)   #Memanggil fungsi menyalakan_magnetron setelah 3000 ms(3 detik)
    else:                                                                   #Jika suhu masukan lebih kecil dari suhu kamar
        status['text']= "Masukan salah"                                     #Memperbaharui label yang menunjukkan status oven

def menyalakan_magnetron(time,temperature,maximum_temp,food_):
    """
    Prosedur yang menyimulasikan menyalakan magnetron.Prosedur ini hanya menjadi perantara untuk
    memindahkan parameter time,temperatur,dan maximum_temp ke fungsi timer_start
    """
    #Variabel global
    status['text'] = "Menyalakan magnetron"                                 #Memperbaharui label yang menunjukkan proses menyalakan magnetron
    #menampilkan timer
    sisa_waktu['text'] = "%02d:%02d" % (time//60,time%60)                   #Menformat keluaran timer agar berbentuk MM:DD
    #Memulai memasak
    menu.after(2000,timer_start,time,temperature,maximum_temp,food_)              #Setelah 2000ms(2 sekon),akan memanggil fungsi timer_start

def timer_start(times,temp,temperatur_maks,masukan_makanan):
    """
    Prosedur untuk memproses timer dan mengupdate nilai suhu oven
    """
    #Variabel global
    global berhenti
    global preheat
    global waktu_memanaskan
    global kenaikan_suhu
    global cek
    #Mengaktifkan tombol berhenti
    berhenti_['state'] = ACTIVE
    #Menonaktifkan tombol mulai(karena proses telah dimulai)
    mulai['state'] = DISABLED
    #Inisiasi
    if(preheat != 0):                                                      #Jika ada waktu preheat
        kenaikan_suhu = (temperatur_maks-temp)/preheat                     #Hitung kenaikan suhu tiap detik
        #Karena oven menghitung waktu mundur,maka kita harus mencari batas waktu sampai oven berhenti naik suhunya
        waktu_memanaskan = times - preheat                          
        preheat = 0                                                        #Agar kondisionalnya tidak diproses lagi
        cek = False                                                        #Cek diset jadi False agar kondisi ini tidak diproses lagi
    elif(cek):                                                                   #Jika tidak ada waktu preheat
        kenaikan_suhu = (temperatur_maks-temp)/times                        #Hitung kenaikan suhu tiap detik
        cek = False                                                         #Agar perhitungan kenaikan suhu tidak diproses lagi
    #Kondisional
    if(not berhenti):                                                       #Jika variabel berhenti bernilai False
        status['text'] = "Oven sedang menyala"                              #Memperbaharui label status
        #Update suhu
        if(times >0):                                                               #Jika waktu timer lebih besar dari 0  
            if(waktu_memanaskan != 0):                                              #Jika ada waktu preheat                                          
                if(times>waktu_memanaskan):                                         #Jika timer sekarang lebih besar dari batas waktu untuk preheat
                    temp += kenaikan_suhu                                           #Suhu ditambahkan
                    info_temperatur['text'] ="Temperatur:"+str(round(temp,2))+"°C"  #Menampilkan suhu
                    #Dibulatkan 2 angka di belakang koma 
                    #Dikurangi kenaikan suhu agar pas mulai,suhu yang ditampilkan sesuai suhu kamar
            else:                                                                   #Jika tidak ada waktu preheat
                temp += kenaikan_suhu                                               #Suhu ditambahkan
                info_temperatur['text'] ="Temperatur:"+str(round(temp,2))+"°C"      #Menampilkan suhu
                #Dibulatkan 2 angka di belakang koma 
                #Dikurangi kenaikan suhu agar pas mulai,suhu yang ditampilkan sesuai suhu kamar
            times -= 1                                                              #Kounter waktu dikurangi 1(menandakan timernya mundur )
            #Menampilkan timer
            timer_ = "%02d:%02d" % (times//60,times%60)                         #Untuk menformat agar keluaran waktu timer menjadi MM:DD
            sisa_waktu['text'] = timer_                                         #Menampilkan timer
            #Mengulang lagi prosedur time_start setiap 1000ms(1 sekon)
            menu.after(1000,timer_start,times,temp,temperatur_maks,masukan_makanan)
        else:                                                                   #Jika timer ==0(waktu masak sudah selesai)
            status['text'] = "Masakan anda telah matang("+masukan_makanan+")"   #Memperbaharui status di frame info
            masukkan_makanan['state'] = ACTIVE                                  #Mengaktifkan tombol membuka oven
            #Menyalakan alarm(beep)
            mixer.init()                                                        #Menginisialisasi mixer
            mixer.music.load("selesai.mp3")                                     #Memuat file audio alarm(beep)
            mixer.music.play(loops=0)                                           #Memutar alarm tanpa pengulangan
            ambil['state'] = ACTIVE                                             #Mengaktifkan tombol ambil makanan
            berhenti_['state'] = DISABLED                                           #Karena proses telah selesai
            mulai['state'] = ACTIVE                                                 #Karena proses bisa dimulai lagi   
    else:                                                                       #Jika oven dipaksa berhenti saat sedang berjalan(berhenti==true)
        status['text'] = "Oven berhenti"                                        #Memperbaharui status di frame info
        info_temperatur['text'] = "Temperatur:25.0°C"                           #Mereset indikator temperatur ke suhu kamar
        sisa_waktu['text'] = "00:00"                                            #Mereset tulisan sisa waktu di frame info
        masukkan_makanan['state'] = ACTIVE                                      #Mengaktifkan tombol membuka oven
        ambil['state'] = ACTIVE                                                 #Mengaktifkan tombol ambil makanan
        berhenti_['state'] = DISABLED                                           #Karena proses telah selesai
        mulai['state'] = ACTIVE                                                 #Karena proses bisa dimulai lagi                                       
    #Karena times merupakan variabel lokal di prosedur ini,maka begitu prosedur ini selesai,
    #besar temperaturnya akan kembali ke suhu kamar lagi

def stop():
    """
    Prosedur untuk memberhentikan oven
    """
    #Variabel global
    global berhenti                 
    berhenti = True                 #Jika berhenti = True,maka oven akan berhenti bekerja
#Karena proses update timer dan suhu oven dilakukan di prosedur yang terpisah dengan prosedur berhenti serta prosedur tersebut
#Sedang berjalan ketika tombol "berhenti" ditekan,
#Maka akan sangat rumit jika menjadikan berhenti sebagai parameter fungsi.
#Karena itu,berhenti dijadikan varibale global

def ambil_makanan():
    """
    Prosedur untuk menyimulasikan mengambil makanan dari oven
    """
    #variabel global
    global food
    status['text'] = "Anda telah mengambil "+food+" dari oven"      #Menampilkan status di frame info
    food = "udara"                                                 #Mereset nilai food menjadi "udara" karena kalo ovennya sudah kosong,isinya tinggal udara(asumsikan oven tidak kedap udara)
    info_temperatur['text'] = "Temperatur:25°C"                     #Mereset indikator temperatur ke suhu kamar
    ambil['state'] = DISABLED                                       #Menonaktifkan tombol ambil makan lagi(Karena makanan sudah diambil)


#Algoritma
#Menginisialisasi GUI
root = Tk()                                                                     #Harus dilakukan di awal agar program bisa jalan
root.title("Simulasi Oven Pintar")                                              #Judul atas program
root.iconbitmap("icon.ico")
#Menampilkan widget gambar oven
oven = LabelFrame(root,width=200,height=200)                                    #Frame untuk menampilkan gambar oven
oven.grid(row=0,column=0,rowspan=2)                                             #Posisi si frame di layar
gambar_oven = ImageTk.PhotoImage(Image.open("download.jpg"))                    #Memuat gambar oven
kaitan = Label(oven,image=gambar_oven)                                          #Menampilkan gambar oven
kaitan.grid(row=0,column=0)                                                     #Posisi gambar oven

#Tombol membuka oven
masukkan_makanan = Button(root,text="MASUKKAN MAKANAN",command=buka)                   
masukkan_makanan.grid(row=2,column=0)                                           #Posisi tombol 
#Tombol akan memanggil fungsi buka ketika ditekan

#Menampilkan widget masukan suhu dan temperatur
menu = LabelFrame(root,width=200,height=200)                                    #Frame untuk menu
menu.grid(row=0,column=1,sticky=N)                                              #Posisi si Frame
perintah_input_suhu = Label(menu,text="Masukkan suhu maksimum:")                #Perintah untuk memasukkan suhu maksimum
perintah_input_suhu.grid(row=0,column=0)                                        #Posisi si perintah di frame
input_suhu = Entry(menu,width=5)                                                #Kolom untuk memasukkan suhu maksimum yang diinginkan
input_suhu.grid(row=1,column=0)                                                 #Posisi si kolom di frame
perintah_input_menit = Label(menu,text="Masukkan menit:")                       #Perintah untuk memasukkan lama memanggang(menit)
perintah_input_menit.grid(row=2,column=0)                                       #Posisi si perintah di frame
input_menit = Entry(menu,width=5)                                               #Kolom untuk memasukkan menit yang diinginkan(waktu memasak)                                 
input_menit.grid(row=3,column=0)                                                #Posisi si kolom di frame
perintah_input_detik = Label(menu,text="Masukkan detik:")                       #Perintah untuk memasukkan lama memanggang(detik)
perintah_input_detik.grid(row=2,column=1)                                       #Posisi si perintah di frame
input_detik = Entry(menu,width=5)                                               #Kolom untuk memasukkan detik yang diinginkan(waktu memasak)  
input_detik.grid(row=3,column=1)                                                #Posisi si kolom di frame
#Dropdown menu untuk memilih metode pemanggangan
mode_masak = StringVar()                                                        #Variabel metode memanggang yang dipilih
mode_masak.set(modes[0])                                                        #Untuk menginisialisasi nilai awal variabel
Label(menu,text="Pilih mode memanggang:").grid(row=0,column=1)                  #Menampilkan perintah untuk memilih mode memanggang
metode = OptionMenu(menu,mode_masak,*modes)                                     #Dropdown menu untuk memilih metode memasak
metode.grid(row=1,column=1)                                                     #Posisi dropdown menu di frame
#Tombol untuk memulai proses memanggang
mulai = Button(menu,text="MULAI",command=lambda:start(int(input_menit.get()),int(input_detik.get()),temperatur,int(input_suhu.get()),food,lama_masak),state=DISABLED)
mulai.grid(row=4,column=0)                                                      #Posisi si tombol di frame
#Tombol akan memanggil fungsi start()
#Tombol untuk menghentikan proses memanggang yang sedang berlagsung
berhenti_ = Button(menu,text="BERHENTI",command=lambda:stop(),state=DISABLED)
berhenti_.grid(row=4,column=1)                                                  #Posisi si tombol di frame
#Tombol akan memanggil fungsi stop()
#Kedua tombol tersebut awalnya berada pada keadaan tidak aktif

#Frame info
info = LabelFrame(root,text="Informasi")                                        #Frame untuk menampilkan informasi
info.grid(row=1,column=1)                                                       #Posisi si frame di layar 
status = Label(info,text="Oven Kosong")                                         #Status awal si oven      
status.grid(row=0,column=0)                                                     #Posisi tulisan status di frame
info_temperatur = Label(info,text="Temperatur:"+str(temperatur)+"°C")           #Menampilkan temperatur
info_temperatur.grid(row=1,column=0)                                            #Posisi tulisan yang menampilkan temperatur
Label(info,text="Waktu sampai matang:").grid(row=2,column=0)                    #Tulisan mengenai sisa waktu memasak di frame
sisa_waktu = Label(info,text="00:00")                                           #Menampilkan sisa waktu memasak
sisa_waktu.grid(row=3,column=0)                                                 #Posisi tulisan sisa waktu memasak di frame
metode_masak = Label(info,text="Metode memasak:")                               #Menampilkan metode memasak
metode_masak.grid(row=4,column=0)                                               #Posisi tulisan yang menampilkan meyode memasak di frame
#Mengeluarkan makanan dari oven
ambil = Button(root,text="AMBIL MAKANAN",command=ambil_makanan,state=DISABLED)  #Awalnya tombol tidak aktif
ambil.grid(row=2,column=1)

#Loop utama untuk menjalankan program agar GUI bekerja
root.mainloop()

