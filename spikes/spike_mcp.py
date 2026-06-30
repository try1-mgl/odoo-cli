"""
Spike 2: MCP Stdio Protocol Server Test
Menguji instalasi dan inisialisasi pustaka resmi mcp (FastMCP) untuk memastikan AI Agent tools dapat berjalan stabil.
"""
import sys

print("=== SPIKE 2: MCP PROTOCOL SERVER TEST ===")

try:
    # 1. Cek Import Pustaka MCP
    print("\n[TEST 1] Memeriksa import modul 'mcp'...")
    import mcp
    from mcp.server.fastmcp import FastMCP
    print("  Import modul 'mcp' & 'FastMCP': SUKSES ✅")
except ImportError as e:
    print(f"  Gagal import pustaka 'mcp': {e}")
    print("  Pastikan pustaka mcp terinstal (misal via 'uv pip install mcp')")
    sys.exit(1)

# 2. Inisialisasi Server FastMCP
try:
    print("\n[TEST 2] Inisialisasi objek FastMCP server...")
    mcp_server = FastMCP("Spike-Odoo-CLI")
    print(f"  Server '{mcp_server.name}' terinisialisasi: SUKSES ✅")
except Exception as e:
    print(f"  Gagal inisialisasi FastMCP: {e}")
    sys.exit(1)

# 3. Registrasi Tool Sederhana
try:
    print("\n[TEST 3] Meregistrasikan dummy tool ke server...")
    
    @mcp_server.tool()
    def check_connection(host: str = "http://localhost:8069") -> str:
        """Menghubungkan ke Odoo host untuk memvalidasi."""
        return f"Koneksi ke {host} sukses (Dummy)."
        
    print("  Registrasi tool '@mcp_server.tool()': SUKSES ✅")
    print(f"  Daftar tools terdaftar: {list(mcp_server._tool_manager.list_tools())}")
except Exception as e:
    print(f"  Gagal registrasi tool: {e}")
    sys.exit(1)

print("\n=== SPIKE COMPLETED ===")
