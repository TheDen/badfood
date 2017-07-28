const express = require('express');
const app = express();
const MongoClient = require('mongodb').MongoClient
app.set('view engine', 'ejs')

app.use(express.static('public'))

mongourl = process.env.MONGOURL
apikey = process.env.APIKEY

app.get('/', (req, res) => {
  db.collection('data2').find().toArray((err, result) => {
    if (err) return console.log(err)
    res.render('index.ejs', {data: result})
})
  })

MongoClient.connect(mongourl, (err, database) => {
  if (err) return console.log(err)
  db = database
  app.listen(process.env.PORT || 5000)
})
