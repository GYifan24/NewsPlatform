var express = require('express');
var router = express.Router();
var path = require('path');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.sendFile('index.html', { root: path.join(__dirname, '../../client/build/')});
});

app.listen(3000, () => console.log('Server running on port 3000'))
module.exports = router;
