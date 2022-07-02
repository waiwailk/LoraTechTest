var file=cat('/tmp/mongo_mktoutlier.json')
use loratech_db
var o = JSON.parse(file);
db.monthly_market_outperformer.insert(o)
show collections

db.monthly_market_outperformer.find().pretty()
db.monthly_market_outperformer.count()
