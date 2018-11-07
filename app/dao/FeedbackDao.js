function * addFeedback(app, vc, vn, ch, contact, content) {
    const create_ts = new Date().getTime();
    const sql = 'insert ignore into feedback set app=?, vc=?, vn=?, ch=?, contact=?, content=?, create_ts=?';
    yield Conn.query(sql,
        {replacements: [app, vc, vn, ch, contact, content, create_ts], type: Sequelize.QueryTypes.INSERT});
}

function * getFeedbackList(index, size) {
    const sql = 'select * from feedback order by create_ts desc limit ?, ?';
    return yield Conn.query(sql,
        {replacements: [index, size], type: Sequelize.QueryTypes.SELECT});
}

module.exports = {
    addFeedback, getFeedbackList
};