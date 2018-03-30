const FeedbackDao = require('../dao/FeedbackDao');
const NewsDao = require('../dao/NewsDao');

const Res = {
    success: function (res, data) {
        res.json({
            code: 200,
            msg: 'ok',
            data
        })
    },
    error: function (res, code, msg) {
        res.json({
            code,
            msg
        })
    }
};

//  curl -X POST 'http://localhost:8484/api/feedback' -H 'Content-type: application/json' -H 'app: zhuhaibus' -H 'ch:xiaomi' -H 'vc:1' -H 'vn:1.0' -d '{"contact":"","content": "test"}'
const feedback = (req, res) => {
    const {app, ch, vc, vn} = req.headers;
    const {contact, content} = req.body;

    if (!content || content === '') {
        return Res.error(res, 400, '内容不能为空');
    }

    Co(function *() {
        yield FeedbackDao.addFeedback(app, vc, vn, ch, contact, content);
        Res.success(res);
    });
};

// curl 'http://localhost:8484/api/news?index=0&size=2'
const getNewsList = (req, res) => {
    let {index, size} = req.query;
    if (!index || !size || size <= 0 || index < 0) {
        return Res.success(res, []);
    }

    if (index == 0) {
        index = Number.MAX_SAFE_INTEGER;
    }

    Co(function *() {
        const news = yield NewsDao.getNewsList(index, parseInt(size));
        let res_index = -1;
        for (let item of news) {
            if (res_index == -1 || item.news_id < res_index) {
                res_index = item.news_id;
            }
        }
        if (news.length < size) {
            res_index = -1;
        }
        Res.success(res, {items: news, index: res_index});
    });
};

// curl 'http://localhost:8484/api/news/14'
const getNewsDetail = (req, res) => {
    let {news_id} = req.params;
    Co(function *() {
        const [news_detail] = yield NewsDao.getNewsDetail(news_id);
        if (news_detail) {
            return Res.success(res, news_detail);
        }
        return Res.error(res, 404, '没有找到相关数据');
    });
};

module.exports = {
    feedback, getNewsList, getNewsDetail
};