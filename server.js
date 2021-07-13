const express = require('express');
const app = express();
app.set('view engine', 'ejs');
app.use(express.static('public'));

global.apikey = process.env.APIKEY;
global.dbCollection = process.env.DB_COLLECTION;

app.get('/', (req, res) => {
  db.collection(dbCollection).find().toArray((err, result) => {
    if (err) return console.log(err);
    res.render('index.ejs', {data: result});
  });
});


const { MongoClient } = require('mongodb');
const uri = process.env.MONGOURL;
const client = new MongoClient(uri, { useNewUrlParser: true });

client.connect(err => {
  db = client.db("badfood")
  client.close();
  app.listen(process.env.PORT || 5000);
});
