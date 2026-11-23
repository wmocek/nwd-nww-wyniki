// Wklej do: Arkusz Google → Rozszerzenia → Apps Script
// Potem: Wdróż → Nowe wdrożenie → Aplikacja internetowa
//        Wykonaj jako: Ja,  Kto ma dostęp: Każdy
const ARKUSZ = 'Wyniki';

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const d = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sh = ss.getSheetByName(ARKUSZ);
    if (!sh) {
      sh = ss.insertSheet(ARKUSZ);
      sh.appendRow(['Data', 'Imię', 'Test', 'Punkty', 'Na ile', 'Procent', 'Ocena', 'Czas (min)', 'Błędne zadania']);
      sh.setFrozenRows(1);
      sh.getRange('A1:I1').setFontWeight('bold');
    }
    const txt = v => { v = String(v == null ? '' : v).slice(0, 3000); return /^[=+\-@]/.test(v) ? "'" + v : v; };
    sh.appendRow([new Date(), txt(d.name).slice(0, 60), txt(d.test), Number(d.ok), Number(d.n),
                  Number(d.pc), txt(d.grade), Number(d.minutes), txt(d.mistakes)]);
    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
                         .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false }))
                         .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}
