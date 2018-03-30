function * getNewsList(index, size) {
    const sql = `select news_id,dt,pt,origin_id,title,news_ts,cover from news where news_id<? order by news_id desc limit ?`;
    return yield Conn.query(sql,
        {replacements: [index, size], type: Sequelize.QueryTypes.SELECT});
}

function * getNewsDetail(news_id) {
    const sql = `select * from news where news_id=? limit 1`;
    return yield Conn.query(sql, {replacements: [news_id], type: Sequelize.QueryTypes.SELECT});
}

module.exports = {
    getNewsList, getNewsDetail
};