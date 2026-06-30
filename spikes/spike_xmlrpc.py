"""
Spike 1: XML-RPC Multi-Version Compatibility Test
Menguji konektivitas, pembacaan versi Odoo, introspeksi model, dan paginasi data.
"""
import xmlrpc.client
import sys

URL = 'http://localhost:8069'
DB = 'learn'
USERNAME = 'terrasurya88@gmail.com'
PASSWORD = 'admin123'

print("=== SPIKE 1: XML-RPC COMPATIBILITY TEST ===")
print(f"Target Server: {URL}")
print(f"Target DB    : {DB}")

# 1. Test Konektivitas & Versi Odoo
try:
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common', allow_none=True)
    version_info = common.version()
    print("\n[TEST 1] Konektivitas & Versi Odoo:")
    print(f"  Status   : SUKSES ✅")
    print(f"  Version  : {version_info.get('server_version')}")
    print(f"  Protocol : XML-RPC {version_info.get('protocol_version')}")
    print(f"  Metadata : {version_info}")
except Exception as e:
    print(f"\n[TEST 1] Gagal terhubung ke {URL}: {e}")
    sys.exit(1)

# 2. Test Autentikasi
try:
    uid = common.authenticate(DB, USERNAME, PASSWORD, {})
    if uid:
        print(f"\n[TEST 2] Autentikasi User:")
        print(f"  Status   : SUKSES ✅")
        print(f"  User UID : {uid}")
    else:
        print(f"\n[TEST 2] Autentikasi Gagal: Credential salah.")
        sys.exit(1)
except Exception as e:
    print(f"\n[TEST 2] Error saat Autentikasi: {e}")
    sys.exit(1)

# 3. Test Object CRUD & Paginasi (Search + Limit + Offset)
try:
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object', allow_none=True)
    
    # Ambil 2 partner dengan offset 1
    partners = models.execute_kw(DB, uid, PASSWORD, 'res.partner', 'search_read',
        [[['is_company', '=', False]]],
        {
            'fields': ['name', 'city', 'country_id'],
            'limit': 2,
            'offset': 1
        }
    )
    print(f"\n[TEST 3] Paginasi & Search Read:")
    print(f"  Status   : SUKSES ✅")
    print(f"  Data Read: {len(partners)} record(s)")
    for i, p in enumerate(partners):
        print(f"    - Partner {i+1}: {p.get('name')} | Kota: {p.get('city')} | Negara: {p.get('country_id')}")
except Exception as e:
    print(f"\n[TEST 3] Gagal melakukan search_read: {e}")

# 4. Test Introspeksi Skema Field (Fields Get)
try:
    # Mengambil skema field res.partner untuk memvalidasi tipe data
    fields_spec = models.execute_kw(DB, uid, PASSWORD, 'res.partner', 'fields_get',
        [[]],
        {'attributes': ['type', 'string', 'relation']}
    )
    print(f"\n[TEST 4] Introspeksi Struktur Fields (fields_get):")
    print(f"  Status   : SUKSES ✅")
    print(f"  Total Fld: {len(fields_spec)} fields")
    
    # Ambil sampel beberapa field penting
    sample_fields = ['name', 'parent_id', 'category_id', 'lang']
    for f in sample_fields:
        spec = fields_spec.get(f)
        if spec:
            print(f"    - Field '{f}': Label='{spec.get('string')}', Tipe='{spec.get('type')}', Relasi={spec.get('relation')}")
except Exception as e:
    print(f"\n[TEST 4] Gagal melakukan fields_get: {e}")

# 5. Test Deteksi Relasi ERD (Mencari relational fields)
try:
    print(f"\n[TEST 5] Pemetaan Relasi ERD:")
    relational_count = 0
    for fname, spec in fields_spec.items():
        ftype = spec.get('type')
        if ftype in ['many2one', 'one2many', 'many2many']:
            relational_count += 1
            if relational_count <= 5: # Batasi output cetak ke layar
                print(f"    - Relasi {relational_count}: Field '{fname}' ({ftype}) -> Model '{spec.get('relation')}'")
    print(f"  Total relational fields ditemukan: {relational_count}")
except Exception as e:
    print(f"\n[TEST 5] Gagal memetakan relasi: {e}")

print("\n=== SPIKE COMPLETED ===")
