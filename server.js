const express = require('express');
const app = express();
const MongoClient = require('mongodb').MongoClient;
app.set('view engine', 'ejs');

app.use(express.static('public'));

const mongourl = process.env.MONGOURL;
const apikey = process.env.APIKEY;

var dbCollection = process.env.DB_COLLECTION;

app.get('/', (req, res) => {
  db.collection(dbCollection).find().toArray((err, result) => {
    if (err) return console.log(err);
    res.render('index.ejs', {data: result});
  });
});

MongoClient.connect(mongourl, (err, database) => {
  if (err) return console.log(err);
  const db = database;
  app.listen(process.env.PORT || 5000);
});
