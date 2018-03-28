'use strict';

const express = require('express');
const router = express.Router();

const CoreController = require('./controller/CoreController');
router.post('/feedback', CoreController.feedback);

module.exports = router;