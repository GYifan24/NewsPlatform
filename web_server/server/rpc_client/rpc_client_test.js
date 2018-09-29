var client = require('./rpc_client');

// invoke 'add'
client.add(1, 3, function(result) {
  console.assert(result === 4);
  console.log("pass")
});

client.getNewsSummariesForUser('test_user', 1, function(response) {
  // console.log(response)
  console.assert(response != null);
});
