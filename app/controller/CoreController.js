const FeedbackDao = require('../dao/FeedbackDao');

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

module.exports = {
    feedback
};