const mongoose = require('mongoose');

// connect to mlab
module.exports.connect = (uri) => {
  mongoose.connect(uri);

  mongoose.connection.on('error', (err) => {
    console.error(`Mongoose connection error: $(err)`);
    process.exit(1);
  });

  // load models.
  require('./user');
}
