import os

# --- CONFIGURATION ---
# Change these variables to switch between Windows Auth (-E) and SQL Auth (-U/-P)
CONFIG = {
    "SERVER": r"192.168.1.148\duebit",
    "DATABASE": "DD_DUE",
    "USE_WINDOWS_AUTH": True,  # Set to False to use Username/Password
    "USERNAME": "sa",
    "PASSWORD": "YourPasswordHere",
    "OUTPUT_BAT_FILE": "export_tables.bat"
}

# List of queries and their respective output filenames
queries = [
    ("SELECT idarticolo, REPLACE(REPLACE(REPLACE(REPLACE(Descrizione, CHAR(13), ''), CHAR(10), ''), '|', ' '), '\', ' ') as Descrizione, CodiceIva, idFamiglia FROM dbo.TABARTICOLI", "TABARTICOLI.csv"),
    ("SELECT [IdArticolo], [IdFornitore], REPLACE(REPLACE(REPLACE(REPLACE([CodiceArticoloFornitore], CHAR(13), ''), CHAR(10), ''), '|', ''), '\', '') as CodiceArticoloFornitore, [Predefinito] FROM dbo.TabArticoliFornitori", "TabArticoliFornitori.csv"),
    ("SELECT [IdFamiglia], [NomeFamiglia], [AliquotaIva], [CodiceIva] FROM dbo.TabFamiglie", "TabFamiglie.csv"),
    ("SELECT idarticolo, prezzovendita, sconto1, idlistino FROM dbo.tabPrezziVendita", "tabPrezziVendita.csv"),
    ("SELECT Imponibile, Sconto1, Sconto2, Sconto3, Sconto4, PrezzoAcquisto,REPLACE(REPLACE(REPLACE(REPLACE(codicearticolofornitore, CHAR(13), ''), CHAR(10), ''), '|', ''), '\', '') as codicearticolofornitore, idfornitore FROM dbo.TabPrezziAcquisto", "TabPrezziAcquisto.csv"),
    ("SELECT idarticolo,REPLACE(REPLACE(REPLACE(REPLACE(barcode, CHAR(13), ''), CHAR(10), ''), '|', ' '), '\', ' ') as barcode FROM dbo.tabBarcode", "tabBarcode.csv"),
    ("SELECT idcliente, REPLACE(REPLACE(REPLACE(REPLACE(ragionesociale1, CHAR(13), ''), CHAR(10), ''), '|', ' '), '\', ' ') as ragionesociale1, indirizzo, cap, paese, provincia, telefono, email, partitaiva, codicefiscale, emailpec, codiceunivocoufficio, REPLACE(REPLACE(REPLACE(REPLACE(ragionesociale2, CHAR(13), ''), CHAR(10), ''), '|', ' '), '\', ' ') as ragionesociale2 FROM dbo.tabClienti", "tabClienti.csv"),
    ("SELECT [ID], [idMagazzino], [idCassa], [idTessera], [idCliente], [idTipoTransazione], [ImportoTransazione], [Punti_Conteggio], [Punti_Valore], [ProgressivoPunti_Conteggio], [ProgressivoPunti_Valore], [UtenteUltimoAccesso], [idArticolo], [Descrizione], [NumeroScontrino] FROM [dbo].[tabFidelity_Transazioni]", "tabFidelity_Transazioni.csv"),
    ("SELECT [ID], [idModelloTessera], [idCliente], [CodiceTessera], [TotalePunti], [TotaleImporto], [Attiva] FROM [dbo].[tabFidelity_Tessere]", "tabFidelity_Tessere.csv")
]

def generate_bat():
    # Build the authentication string
    if CONFIG["USE_WINDOWS_AUTH"]:
        auth_str = "-E"
    else:
        auth_str = f"-U {CONFIG['USERNAME']} -P {CONFIG['PASSWORD']}"

    lines = ["@echo off", f"echo Starting export from {CONFIG['DATABASE']}...", ""]

    for sql, filename in queries:
        # Construct the full sqlcmd string
        # -Q for query, -o for output, -s for separator, -W for stripping whitespace
        cmd = f'sqlcmd -S {CONFIG["SERVER"]} {auth_str} -d {CONFIG["DATABASE"]} -Q "SET NOCOUNT ON; {sql}" -o {filename} -s"|" -W'
        lines.append(cmd)

    lines.append("")
    lines.append("echo Export Complete.")
    lines.append("pause")

    # Write to file
    try:
        with open(CONFIG["OUTPUT_BAT_FILE"], "w") as f:
            f.write("\n".join(lines))
        print(f"Successfully generated: {CONFIG['OUTPUT_BAT_FILE']}")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    generate_bat()
