from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder=".")

class Rule:
    def __init__(self, condition, conclusion):
        self.condition = condition  # Daftar kode gejala
        self.conclusion = conclusion  # Kesimpulan penyakit

class ExpertSystem:
    def __init__(self):
        self.rules = []  # Daftar aturan
        self.facts = []  # Fakta (gejala yang dimasukkan pengguna)
        self.gejala = {}  # Kamus untuk kode dan nama gejala

    def add_rule(self, rule):
        """Menambahkan aturan ke sistem."""
        self.rules.append(rule)

    def add_fact(self, fact):
        """Menambahkan fakta (gejala)."""
        if fact not in self.facts:
            self.facts.append(fact)

    def add_gejala(self, kode, nama):
        """Menambahkan kode gejala dan keterangannya."""
        self.gejala[kode] = nama

    def get_gejala(self, kode):
        """Mengambil nama gejala berdasarkan kodenya."""
        return self.gejala.get(kode, "Gejala tidak ditemukan")

    def tampilkan_daftar_gejala(self):
        """Menampilkan daftar kode dan nama gejala."""
        print("\nDaftar Gejala:")
        for kode, nama in self.gejala.items():
            print(f"{kode}: {nama}")

    def forward_chaining(self):
        """Inferensi menggunakan forward chaining."""
        diagnosis = []
        while True:
            new_inference = False
            for rule in self.rules:
                if all(cond in self.facts for cond in rule.condition) and rule.conclusion not in self.facts:
                    conditions = [self.get_gejala(cond) for cond in rule.condition]
                    diagnosis.append(rule.conclusion)
                    self.facts.append(rule.conclusion)
                    new_inference = True
            if not new_inference:
                break
        return diagnosis

# Membuat sistem pakar
expert_system = ExpertSystem()

# Menambahkan gejala (sesuaikan dengan tabel Anda)
gejala_list = [
    ('G1', 'Ikan mengapung di permukaan air'),
    ('G2', 'Ikan malas berenang'),
    ('G3', 'Insang berwarna kemerahan'),
    ('G4', 'Bercak putih pada tubuh'),
    ('G5', 'Insang membusuk dan menghitam'),
    ('G6', 'Nafsu makan menurun'),
    ('G7', 'Ikan menggosokkan badan ke benda keras'),
    ('G8', 'Tubuh ikan pucat dan berlendir'),
    ('G9', 'Warna tubuh gelap'),
    ('G10', 'Pertumbuhan ikan lambat'),
    ('G11', 'Sirip ikan sobek'),
    ('G12', 'Pendarahan pada insang'),
    ('G13', 'Mata ikan menonjol'),
    ('G14', 'Perut ikan bengkak'),
    ('G15', 'Ikan mengalami kejang'),
    ('G16', 'Sirip membusuk'),
    ('G17', 'Ikan bernafas dengan cepat'),
    ('G18', 'Ikan terlihat lesu'),
    ('G19', 'Badan ikan bengkok'),
    ('G20', 'Luka terbuka pada tubuh'),
    ('G21', 'Parasit menempel pada kulit ikan'),
    ('G22', 'Ikan mengalami gangguan keseimbangan'),
    ('G23', 'Ikan sering melompat dari air'),
    ('G24', 'Sirip menggumpal'),
    ('G25', 'Ikan tidak merespon rangsangan'),
    ('G26', 'Ikan kehilangan keseimbangan saat berenang'),
    ('G27', 'Kotoran ikan tidak normal'),
    ('G28', 'Ikan berdiam di dasar kolam'),
    ('G29', 'Muncul lendir berlebihan di insang'),
    ('G30', 'Kulit ikan mengelupas')
]

# Menambahkan gejala ke dalam sistem
for kode, nama in gejala_list:
    expert_system.add_gejala(kode, nama)

# Menambahkan aturan penyakit berdasarkan tabel Anda
rules = [
    Rule(['G1', 'G2', 'G3', 'G4', 'G5'], 'Penyakit Branchiomycosis'),
    Rule(['G1', 'G4', 'G6', 'G7', 'G8'], 'Penyakit White Spot'),
    Rule(['G1', 'G6', 'G9', 'G11', 'G12', 'G14'], 'Penyakit Dactylograsis'),
    Rule(['G23', 'G24', 'G25', 'G26'], 'Penyakit Columnaris'),
    Rule(['G27', 'G28'], 'Penyakit Saprolegniasi'),
    Rule(['G10', 'G15', 'G29', 'G30'], 'Penyakit Lerneasi'),
    Rule(['G11', 'G14', 'G15'], 'Penyakit Gyrodactyliasis'),
    Rule(['G6', 'G13', 'G16', 'G17', 'G18', 'G19', 'G20', 'G21', 'G22'], 'Penyakit Streptococciasis')
]

for rule in rules:
    expert_system.add_rule(rule)

@app.route('/')
def index():
    return render_template('index.html', gejala_list=gejala_list)

@app.route('/api/gejala', methods=['GET'])
def api_gejala():
    return jsonify({"gejala_list": gejala_list})

@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    selected_gejala = data.get('selected_gejala', [])

    if not selected_gejala:
        return jsonify({"error": "Silakan pilih setidaknya satu gejala."}), 400

    # Reset fakta sebelum memulai diagnosa baru
    expert_system.facts = []

    # Tambahkan fakta baru dari input pengguna
    for gejala in selected_gejala:
        expert_system.add_fact(gejala)

    # Proses diagnosa
    diagnosis = expert_system.forward_chaining()

    if not diagnosis:
        return jsonify({"result": "Tidak dapat menentukan penyakit berdasarkan gejala yang dipilih."})

    return jsonify({"result": diagnosis})

if __name__ == '__main__':
    app.run(debug=True)
