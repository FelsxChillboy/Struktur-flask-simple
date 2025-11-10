from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Simulasi data dalam memori ---
data = [
    {"id": 1, "NIM": 23260028, "nama": "Ahmad Azarruddin", "semester": 5, "fakultas": "Teknik Informatika"},
    {"id": 2, "NIM": 23260029, "nama": "Budi Santoso", "semester": 3, "fakultas": "Sistem Informasi"}
]

# --- GET (Menampilkan semua data) ---
@app.route('/get', methods=['GET'])
def get_data():
    return jsonify({
        "status": "success",
        "data": data
    })


# --- POST (Menambahkan data baru) ---
@app.route('/post', methods=['POST'])
def post_data():
    new_data = request.get_json()

    # Pastikan JSON diterima
    if not new_data:
        return jsonify({"message": "Tidak ada data JSON", "status": "error"}), 400

    # Ambil data dari body
    NIM = new_data.get('NIM')
    nama = new_data.get('nama')
    semester = new_data.get('semester')
    fakultas = new_data.get('fakultas')

    # Validasi
    if not NIM or not nama:
        return jsonify({"message": "Data tidak valid", "status": "error"}), 400

    # Tambah ID baru otomatis
    new_id = max([d["id"] for d in data]) + 1 if data else 1
    new_item = {
        "id": new_id,
        "NIM": NIM,
        "nama": nama,
        "semester": semester,
        "fakultas": fakultas
    }
    data.append(new_item)

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "status": "success",
        "data": new_item
    }), 201


# --- DETAIL (Ambil 1 data berdasarkan ID) ---
@app.route('/detail/<int:item_id>', methods=['GET'])
def get_detail(item_id):
    item = next((d for d in data if d["id"] == item_id), None)
    if not item:
        return jsonify({"status": "error", "message": "Data tidak ditemukan"}), 404
    return jsonify({"status": "success", "data": item})


# --- DELETE (Hapus data berdasarkan ID) ---
@app.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    global data
    item = next((d for d in data if d["id"] == item_id), None)

    if not item:
        return jsonify({"status": "error", "message": f"Data dengan id {item_id} tidak ditemukan"}), 404

    data = [d for d in data if d["id"] != item_id]
    return jsonify({"status": "success", "message": f"Data dengan id {item_id} berhasil dihapus"})


# --- Menjalankan server ---
if __name__ == '__main__':
    app.run(debug=True)
