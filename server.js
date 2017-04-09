const express = require('express');
const app = express();
const MongoClient = require('mongodb').MongoClient
app.set('view engine', 'ejs')

mongourl = process.env.MONGOURL

app.get('/', (req, res) => {
  db.collection('data').find().toArray((err, result) => {
    if (err) return console.log(err)
    res.render('index.ejs', {data: result})
})
  })

MongoClient.connect(mongourl, (err, database) => {
  if (err) return console.log(err)
  db = database
  app.listen(3000, () => {
    console.log('listening on 3000')
  })
})
