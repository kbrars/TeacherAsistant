const fs = require('fs');

fs.readFile('src/assets/fonts/DejaVuSans.ttf', (err, data) => {
  if (err) throw err;
  console.log(Buffer.from(data).toString('base64'));
});
