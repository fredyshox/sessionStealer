/**
 * Copyright (c) 2018 Kacper Raczy
 */

var express = require('express')
var session = require('express-session')
var port = 1337

// Initialization
var app = express()
var sessionOpts = {
  saveUninitialized: true,
  resave: false,
  secret: 'mysecret'
}
app.use(session(sessionOpts))

var incrementViews = (req) => {
  if (req.session.pageViews) {
    req.session.pageViews += 1
  } else {
    req.session.pageViews = 1
  }
}

// Routes
app.get('/', (req, res) => {
  incrementViews(req)
  var html = `
  <html>
  <head></head>
  <body>
  <h2>Security - session stealing</h2>
  <p>Session id: ${req.session.id}</p>
  <p>Session key: ${sessionOpts.secret}</p>
  <p id="counter">No of visits: ${req.session.pageViews}</p>
  <a href='/restore'>Restore session</a>
  </body>
  </html>
  `
  res.status(200).send(html)
})

app.get('/restore', (req, res) => {
  req.session.regenerate((err) => {
    if (!err) {
      res.redirect(301, '/')
    } else {
      res.status(500).send("Error")
    }
  })
})

// Listening
app.listen(port, () => {
  console.log("Listening on port " + port)
})
