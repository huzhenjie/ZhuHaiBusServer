'use strict';

const express = require('express');
const router = express.Router();

const CoreController = require('./controller/CoreController');
router.post('/feedback', CoreController.feedback);
router.get('/feedbacks', CoreController.feedbackList);
router.get('/news/:news_id', CoreController.getNewsDetail);
router.get('/news', CoreController.getNewsList);

module.exports = router;