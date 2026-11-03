// founderAid MVP — response logger
// Paste into Google Sheet > Extensions > Apps Script, then Deploy > New deployment > Web app
// (Execute as: Me, Who has access: Anyone). Copy the /exec URL into CONFIG.captureUrl in index.html.

function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('events')
    || SpreadsheetApp.getActiveSpreadsheet().insertSheet('events');
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['received', 'ts', 'session', 'source', 'event', 'version', 'details']);
  }
  let row = {};
  try { row = JSON.parse(e.postData.contents); } catch (err) { row = { event: 'parse_error', details: e.postData.contents }; }
  sheet.appendRow([
    new Date(), row.ts || '', row.session || '', row.source || '',
    row.event || '', row.version || '', JSON.stringify(row.details || {})
  ]);
  return ContentService.createTextOutput('ok');
}
