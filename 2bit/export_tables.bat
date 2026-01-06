@echo off
echo Starting export from DD_3DSRLUNIONE...

sqlcmd -S DESKTOP-BNR4IKC\DUEBIT -E -d DD_3DSRLUNIONE -Q "SET NOCOUNT ON; SELECT idarticolo, REPLACE(REPLACE(Descrizione, CHAR(13), ''), CHAR(10), ''), CodiceIva, idFamiglia FROM dbo.TABARTICOLI" -o TABARTICOLI.csv -s"|" -W
sqlcmd -S DESKTOP-BNR4IKC\DUEBIT -E -d DD_3DSRLUNIONE -Q "SET NOCOUNT ON; SELECT [IdArticolo], [IdFornitore], [CodiceArticoloFornitore], [Predefinito] FROM dbo.TabArticoliFornitori" -o TabArticoliFornitori.csv -s"|" -W
sqlcmd -S DESKTOP-BNR4IKC\DUEBIT -E -d DD_3DSRLUNIONE -Q "SET NOCOUNT ON; SELECT [IdFamiglia], [NomeFamiglia], [AliquotaIva], [CodiceIva] FROM dbo.TabFamiglie" -o TabFamiglie.csv -s"|" -W
sqlcmd -S DESKTOP-BNR4IKC\DUEBIT -E -d DD_3DSRLUNIONE -Q "SET NOCOUNT ON; SELECT idarticolo, prezzovendita, sconto1, idlistino FROM dbo.tabPrezziVendita" -o tabPrezziVendita.csv -s"|" -W
sqlcmd -S DESKTOP-BNR4IKC\DUEBIT -E -d DD_3DSRLUNIONE -Q "SET NOCOUNT ON; SELECT Imponibile, Sconto1, Sconto2, Sconto3, Sconto4, PrezzoAcquisto, codicearticolofornitore, idfornitore FROM dbo.TabPrezziAcquisto" -o TabPrezziAcquisto.csv -s"|" -W
sqlcmd -S DESKTOP-BNR4IKC\DUEBIT -E -d DD_3DSRLUNIONE -Q "SET NOCOUNT ON; SELECT idarticolo, barcode FROM dbo.tabBarcode" -o tabBarcode.csv -s"|" -W
sqlcmd -S DESKTOP-BNR4IKC\DUEBIT -E -d DD_3DSRLUNIONE -Q "SET NOCOUNT ON; SELECT idcliente, ragionesociale1, indirizzo, cap, paese, provincia, telefono, email, partitaiva, codicefiscale, emailpec, codiceunivocoufficio, ragionesociale2 FROM dbo.tabClienti" -o tabClienti.csv -s"|" -W
sqlcmd -S DESKTOP-BNR4IKC\DUEBIT -E -d DD_3DSRLUNIONE -Q "SET NOCOUNT ON; SELECT [ID], [idMagazzino], [idCassa], [idTessera], [idCliente], [idTipoTransazione], [DataTransazione], [ImportoTransazione], [Punti_Conteggio], [Punti_Valore], [ProgressivoPunti_Conteggio], [ProgressivoPunti_Valore], [UtenteUltimoAccesso], [idArticolo], [Descrizione], [NumeroScontrino] FROM [dbo].[tabFidelity_Transazioni]" -o tabFidelity_Transazioni.csv -s"|" -W
sqlcmd -S DESKTOP-BNR4IKC\DUEBIT -E -d DD_3DSRLUNIONE -Q "SET NOCOUNT ON; SELECT [ID], [idModelloTessera], [idCliente], [CodiceTessera], [TotalePunti], [TotaleImporto], [Attiva] FROM [dbo].[tabFidelity_Tessere]" -o tabFidelity_Tessere.csv -s"|" -W

echo Export Complete.
pause