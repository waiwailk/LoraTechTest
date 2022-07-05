# Loratech code test

<ins><h2>Introduction</h2></ins>

The question is finding out any outlier stocks during 2020 distinctive and higher prices in comparing with current year HSI. This workshop I have been ready a python DbReader program to fetch out the data price ticks at 2020 and creates the outperformer table to show those stocks item who are out perform (tri_return > tri_return of HSI) or lower. All the source code can be running either windows or Linux.

![Screenshot](screenCap/LoraDBInfo.JPG)

The application gendata.py will able to compare the HSI tri_return of 1-12 months and iterate each stock with 12 months to justify the outlier which is high (true) or low (false). As given by the question, the tri_return rate is calculated by a month end/last month end -1 basis.

![Screenshot](screenCap/gendata.JPG)

By this gendata.py python script, I can altogether to render “postgres_mktoutlier_verify.sql” for PostgresSQL DB and “mongo_mktoutlier_verify.json” for Mongo DB.

By the Docker cp and insert, The Docker PostgresSQL will contain those tri_return data and they can be enquiry by another python Flask to return the monthly basis stock tri_return list in JSON. And insertMongo.js will be helped to insert those JSON format tri_return data into MongoDB.

![Screenshot](screenCap/insertMongo.JPG)






