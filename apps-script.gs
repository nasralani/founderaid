// founderAid MVP — response logger (GET + POST)
// Paste into Google Sheet > Extensions > Apps Script.
// Deploy > Manage deployments > Edit > Version: New version > Deploy (keeps the same /exec URL).

function doGet(e)  { return handle_(e && e.parameter ? e.parameter.d : ''); }
function doPost(e) { return handle_(e && e.postData ? e.postData.contents : ''); }

function handle_(raw) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('events') || ss.insertSheet('events');
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['received', 'ts', 'session', 'source', 'event', 'version', 'details']);
  }
  if (!raw) return ContentService.createTextOutput('ready');
  let row = {};
  try { row = JSON.parse(raw); } catch (err) { row = { event: 'parse_error', details: String(raw).slice(0, 500) }; }
  sheet.appendRow([
    new Date(), row.ts || '', row.session || '', row.source || '',
    row.event || '', row.version || '', JSON.stringify(row.details || {})
  ]);
  return ContentService.createTextOutput('ok');
}
